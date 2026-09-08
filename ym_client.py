"""
Обёртка над yandex_music.Client.
Отвечает за: авторизацию (Device Flow + токен), получение треков,
получение прямой ссылки для превью.
"""
from __future__ import annotations

import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Optional
from urllib.request import Request, urlopen

from yandex_music import Client, Playlist, Track
from yandex_music.exceptions import DeviceAuthError

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def fmt_duration(ms: int | None) -> str:
    if not ms:
        return "—"
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"


_LRC_TS = re.compile(r"\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]")
_LRC_OFFSET = re.compile(r"\[offset:([+-]?\d+)\]", re.I)


def _lrc_frac_to_sec(frac: str | None) -> float:
    """LRC: 1–2 знака — сотые/десятые, 3 знака — миллисекунды."""
    if not frac:
        return 0.0
    if len(frac) >= 3:
        return int(frac[:3]) / 1000.0
    return int(frac) / (10 ** len(frac))


def parse_lrc(raw: str | None) -> list[dict]:
    """Разбирает LRC в [{t: секунды, text}]. Учитывает [offset:мс]."""
    text = raw or ""
    off = 0.0
    m = _LRC_OFFSET.search(text)
    if m:
        try:
            off = int(m.group(1)) / 1000.0
        except ValueError:
            off = 0.0
    out: list[dict] = []
    for row in text.splitlines():
        stamps = _LRC_TS.findall(row)
        if not stamps:
            continue
        line = _LRC_TS.sub("", row).strip()
        for mm, ss, frac in stamps:
            t = int(mm) * 60 + int(ss) + _lrc_frac_to_sec(frac) + off
            out.append({"t": max(0.0, t), "text": line})
    out.sort(key=lambda x: x["t"])
    return out


def cover_urls(uri: str | None, size: str = "100x100") -> tuple[str, str]:
    """(готовый url нужного размера, шаблон с %%) для cover_uri из API."""
    if not uri:
        return "", ""
    raw = str(uri).lstrip("/")
    if raw.startswith("http://") or raw.startswith("https://"):
        tmpl = raw
    else:
        tmpl = "https://" + raw
    return tmpl.replace("%%", size), tmpl


def _cover_uri_list(*values) -> list[str]:
    """Собирает uri обложек из строк, Cover-объектов и списков items_uri."""
    uris: list[str] = []

    def add(value):
        if not value:
            return
        if isinstance(value, (list, tuple)):
            for item in value:
                add(item)
            return
        if not isinstance(value, str):
            add(getattr(value, "uri", None))
            add(getattr(value, "items_uri", None))
            return
        text = value.strip()
        if text and text not in uris:
            uris.append(text)

    for value in values:
        add(value)
    return uris


def playlist_cover_url(pl) -> str:
    """
    Обложка из ответа списка плейлистов, без загрузки треков.
    Cover.get_url() нельзя: если uri уже с https://, библиотека клеит
    второй https:// и картинка 404. Размер 100x100; другие размеры
    пробует интерфейс, если CDN не отдаёт этот.
    """
    for uri in _cover_uri_list(
        getattr(pl, "cover", None),
        getattr(pl, "og_image", None),
        getattr(pl, "cover_without_text", None),
    ):
        url, _ = cover_urls(uri, "100x100")
        if url:
            return url
    return ""


def artist_to_dict(a) -> dict:
    """Краткая карточка исполнителя для интерфейса."""
    if a is None:
        return {"id": "", "name": "", "cover": "", "cover_tmpl": ""}
    uri = None
    if getattr(a, "cover", None) and getattr(a.cover, "uri", None):
        uri = a.cover.uri
    elif getattr(a, "og_image", None):
        uri = a.og_image
    cover, tmpl = cover_urls(uri, "200x200")
    counts = getattr(a, "counts", None)
    return {
        "id": str(a.id) if a.id is not None else "",
        "name": a.name or "",
        "cover": cover,
        "cover_tmpl": tmpl,
        "tracks_count": getattr(counts, "tracks", 0) or 0,
        "albums_count": getattr(counts, "direct_albums", 0) or 0,
    }


def playlist_to_dict(pl, group: str) -> dict:
    """Карточка плейлиста для интерфейса."""
    cover = playlist_cover_url(pl)
    owner_login = ""
    if getattr(pl, "owner", None) and getattr(pl.owner, "login", None):
        owner_login = pl.owner.login
    url_owner = owner_login or "yandexmusic"
    return {
        "id": str(pl.kind),
        "title": pl.title or "Плейлист",
        "owner": owner_login,
        "count": pl.track_count or 0,
        "cover": cover,
        "url": f"https://music.yandex.ru/users/{url_owner}/playlists/{pl.kind}",
        "group": group,
    }


def album_to_dict(al) -> dict:
    """Краткая карточка альбома для интерфейса."""
    cover, tmpl = cover_urls(getattr(al, "cover_uri", None), "200x200")
    return {
        "id": str(al.id) if al.id is not None else "",
        "title": al.title or "Без названия",
        "year": al.year or getattr(al, "original_release_year", None) or "",
        "track_count": al.track_count or 0,
        "genre": getattr(al, "genre", "") or "",
        "cover": cover,
        "cover_tmpl": tmpl,
        "artists": [artist_to_dict(x) for x in (al.artists or []) if x],
    }


def _coerce_track(t):
    """TrackShort / обёртки с .track → сам Track. Иначе объект как есть."""
    if t is None:
        return None
    inner = getattr(t, "track", None)
    if inner is not None and inner is not t and (
        getattr(inner, "id", None) is not None or getattr(inner, "title", None)
    ):
        return inner
    return t


def _track_available(t) -> bool:
    """False только если API явно говорит, что трека нет (available is False / error)."""
    t = _coerce_track(t)
    if t is None:
        return False
    if getattr(t, "available", None) is False:
        return False
    if getattr(t, "error", None):
        return False
    return True


def _unavailable_track_dict(track_id, source_url: str, num: int, title: str = "") -> dict:
    return {
        "id": str(track_id or f"unknown_{num}"),
        "num": num,
        "title": title or "Недоступный трек",
        "artist": "",
        "artists": [],
        "album": "",
        "album_id": None,
        "duration": "—",
        "duration_ms": 0,
        "cover_uri": "",
        "cover_uri_tmpl": "",
        "status": "idle",
        "source_url": source_url,
        "available": False,
    }


def track_to_dict(t, source_url: str, num: int) -> dict:
    """Конвертирует yandex_music.Track → словарь для JS."""
    t = _coerce_track(t)
    if t is None:
        return _unavailable_track_dict(f"unknown_{num}", source_url, num)
    artist_list = [
        {"id": str(a.id) if a.id is not None else "", "name": a.name}
        for a in (t.artists or []) if a and a.name
    ]
    artists = ", ".join(a["name"] for a in artist_list)
    album = ""
    album_id = None
    cover_uri = ""
    cover_uri_tmpl = ""
    if t.albums:
        a0 = t.albums[0]
        if a0:
            album = a0.title or ""
            album_id = str(a0.id) if a0.id is not None else None
            cover_uri, cover_uri_tmpl = cover_urls(a0.cover_uri, "100x100")
    return {
        "id": str(t.id),
        "num": num,
        "title": t.title or "Без названия",
        "artist": artists or "Неизвестный исполнитель",
        "artists": artist_list,
        "album": album,
        "album_id": album_id,
        "cover_uri": cover_uri,
        "cover_uri_tmpl": cover_uri_tmpl,
        "duration": fmt_duration(t.duration_ms),
        "duration_ms": t.duration_ms or 0,
        "status": "idle",
        "source_url": source_url,
        "available": _track_available(t),
    }


def _track_is_stub(t) -> bool:
    """Нет названия — это TrackShort/заглушка, не полноценный трек."""
    t = _coerce_track(t)
    if t is None:
        return True
    if type(t).__name__ == "TrackShort":
        return True
    return not bool(getattr(t, "title", None))


def _short_id_keys(short) -> list[str]:
    """id и id:album — tracks() иногда отвечает только на один из них."""
    if short is None:
        return []
    keys: list[str] = []
    prop = getattr(short, "track_id", None)
    if prop:
        keys.append(str(prop))
    tid = str(getattr(short, "id", "") or "")
    album = getattr(short, "album_id", None)
    if tid and album not in (None, "", 0, "0"):
        keys.append(f"{tid}:{album}")
    if tid:
        keys.append(tid)
    out, seen = [], set()
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


def _index_ym_tracks(tracks) -> dict:
    by_id: dict = {}
    for t in tracks or []:
        if t is None or getattr(t, "id", None) is None:
            continue
        tid = str(t.id)
        by_id[tid] = t
        albums = getattr(t, "albums", None) or []
        a0 = albums[0] if albums else None
        if a0 is not None and getattr(a0, "id", None) is not None:
            by_id[f"{tid}:{a0.id}"] = t
    return by_id


_PL_PAGE_SIZE = 1000
_PL_TIMEOUT = 60
_TRACKS_BATCH = 80


def _playlist_query(page: int, page_size: int = _PL_PAGE_SIZE) -> dict:
    """Query-параметры плейлиста. В _request.get их надо передавать как params, не kwargs."""
    return {
        "rich-tracks": "true",
        "page-size": page_size,
        "pageSize": page_size,
        "page": page,
    }


def _account_uid(client):
    me = getattr(client, "me", None)
    acc = getattr(me, "account", None) if me else None
    return getattr(acc, "uid", None)


def _short_from_raw(client, item, parsed_by_id: dict):
    """TrackShort из JSON, если de_json выкинул UGC/битую карточку."""
    if item is None:
        return None
    if not isinstance(item, dict):
        tid = str(getattr(item, "id", "") or "")
        return parsed_by_id.get(tid) or item
    tid = item.get("id")
    nested = item.get("track")
    if tid is None and isinstance(nested, dict):
        tid = nested.get("id")
    key = str(tid) if tid is not None else ""
    if key and key in parsed_by_id:
        return parsed_by_id[key]
    album = item.get("albumId") if item.get("albumId") is not None else item.get("album_id")
    if album in (None, "", 0, "0") and isinstance(nested, dict):
        albums = nested.get("albums") or []
        if albums and isinstance(albums[0], dict):
            album = albums[0].get("id")
    track_id = f"{tid}:{album}" if tid is not None and album not in (None, "", 0, "0") else (str(tid) if tid is not None else "")
    return SimpleNamespace(
        id=tid,
        album_id=album,
        track=None,
        track_id=track_id,
        client=client,
    )


def _restore_dropped_shorts(client, result, pl):
    """В JSON треков больше, чем после de_json — библиотека роняет UGC."""
    if pl is None or not isinstance(result, dict):
        return pl
    raw = result.get("tracks") or []
    parsed = list(pl.tracks or [])
    if len(raw) <= len(parsed):
        return pl
    by_id = {}
    for s in parsed:
        if s is not None and getattr(s, "id", None) is not None:
            by_id[str(s.id)] = s
    pl.tracks = [_short_from_raw(client, item, by_id) for item in raw]
    return pl


def _get_playlist_by_url(client, url: str, page: int):
    """Прямой GET: users_playlists(kind, user, **kwargs) не кладёт kwargs в query."""
    params = _playlist_query(page)
    result = client._request.get(url, params, timeout=_PL_TIMEOUT)
    try:
        pl = Playlist.de_json(result, client)
    except Exception:
        pl = None
        if isinstance(result, dict):
            pl = SimpleNamespace(
                tracks=[],
                track_count=result.get("trackCount") or result.get("track_count") or 0,
                title=result.get("title") or "",
                client=client,
                pager=None,
            )
    return _restore_dropped_shorts(client, result, pl)


def _collect_playlist_pages(fetch_page):
    """Догружает страницы, пока len(tracks) < track_count."""
    first = None
    collected: list = []
    prev_sig = None
    expected = 0
    for page in range(40):
        pl = fetch_page(page)
        if not pl:
            break
        if first is None:
            first = pl
        chunk = list(pl.tracks or [])
        expected = max(
            expected,
            int(getattr(pl, "track_count", 0) or 0),
            int(getattr(getattr(pl, "pager", None), "total", 0) or 0),
        )
        sig = tuple(str(getattr(s, "id", "") or "") for s in chunk)
        if page and sig and sig == prev_sig:
            # Повтор страницы: дальше листать бесполезно (остаток доберём likes / raw JSON).
            break
        prev_sig = sig
        collected.extend(chunk)
        if not chunk:
            break
        if expected and len(collected) >= expected:
            break
    if first is not None:
        first.tracks = collected
        if expected:
            first.track_count = max(int(first.track_count or 0), expected)
    return first


def _tracks_chunk(client, ids: list[str]) -> list:
    if not ids:
        return []
    try:
        return list(client.tracks(ids, timeout=_PL_TIMEOUT) or [])
    except Exception:
        if len(ids) <= 1:
            return []
        mid = max(1, len(ids) // 2)
        out = []
        out.extend(_tracks_chunk(client, ids[:mid]))
        out.extend(_tracks_chunk(client, ids[mid:]))
        return out


def _hydrate_tracks(client, ids: list[str]) -> dict:
    """Пакетно тянет Track по id / id:album (пачками — /tracks режет длинные списки)."""
    uniq, seen = [], set()
    for i in ids:
        if i and i not in seen:
            seen.add(i)
            uniq.append(i)
    if not client or not uniq:
        return {}
    by_id: dict = {}
    for i in range(0, len(uniq), _TRACKS_BATCH):
        by_id.update(_index_ym_tracks(_tracks_chunk(client, uniq[i:i + _TRACKS_BATCH])))
    missing = [i for i in uniq if i not in by_id and i.split(":")[0] not in by_id]
    if missing:
        bare = []
        for i in missing:
            b = i.split(":")[0]
            if b and b not in bare:
                bare.append(b)
        for i in range(0, len(bare), _TRACKS_BATCH):
            by_id.update(_index_ym_tracks(_tracks_chunk(client, bare[i:i + _TRACKS_BATCH])))
    return by_id


def _bare_track_id(short) -> str:
    tid = str(getattr(short, "id", "") or "")
    return tid.split(":", 1)[0] if tid else ""


def _unique_shorts(shorts) -> list:
    """Один трек — одна строка (id и id:album у лайков часто дублируются)."""
    out, seen = [], set()
    for s in shorts or []:
        key = _bare_track_id(s)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def liked_track_shorts(client) -> list:
    likes = client.users_likes_tracks()
    return _unique_shorts(list(getattr(likes, "tracks", None) or []))


def _merge_liked_tracks(client, pl):
    """
    «Мне нравится»: только users_likes_tracks(), без склейки со страницами
    плейлиста kind=3 — иначе дубли id / id:album и число больше, чем в вебе.
    """
    if pl is None:
        return pl
    try:
        shorts = liked_track_shorts(client)
    except Exception:
        shorts = _unique_shorts(list(pl.tracks or []))
    if shorts:
        pl.tracks = shorts
    else:
        pl.tracks = _unique_shorts(list(pl.tracks or []))
    pl.track_count = len(pl.tracks or [])
    if getattr(pl, "client", None) is None:
        pl.client = client
    return pl


def fetch_user_playlist(client, kind, user_id=None):
    """Плейлист со всеми страницами и rich-tracks (без этого .track часто пустой)."""
    uid = user_id if user_id is not None else _account_uid(client)
    url = f"{client.base_url}/users/{uid}/playlists/{kind}"
    pl = _collect_playlist_pages(lambda page: _get_playlist_by_url(client, url, page))
    if str(kind) == "3":
        pl = _merge_liked_tracks(client, pl)
    return pl


def fetch_shared_playlist(client, playlist_id):
    """Общий плейлист по UUID — те же page-size / rich-tracks / страницы."""
    url = f"{client.base_url}/playlist/{playlist_id}"
    return _collect_playlist_pages(lambda page: _get_playlist_by_url(client, url, page))


def tracks_from_playlist(pl, url: str) -> list[dict]:
    """TrackShort из плейлиста часто без .track — дотягиваем пакетно через tracks()."""
    shorts = list(pl.tracks or [])
    client = getattr(pl, "client", None)
    need: list[str] = []
    for short in shorts:
        if short is None:
            continue
        inner = getattr(short, "track", None)
        if inner is None or _track_is_stub(inner):
            need.extend(_short_id_keys(short))
            if client is None:
                client = getattr(short, "client", None)
    fetched = _hydrate_tracks(client, need)
    result = []
    leftovers = 0
    for i, short in enumerate(shorts, 1):
        if short is None:
            result.append(_unavailable_track_dict(f"unknown_{i}", url, i))
            continue
        t = getattr(short, "track", None)
        if t is None or _track_is_stub(t):
            t = None
            for key in _short_id_keys(short):
                t = fetched.get(key) or fetched.get(key.split(":")[0])
                if t is not None:
                    break
            if t is None and leftovers < 15 and client is not None:
                leftovers += 1
                try:
                    keys = _short_id_keys(short)[:1]
                    got = _tracks_chunk(client, keys) if keys else []
                    t = got[0] if got else None
                except Exception:
                    t = None
        if t is None or _track_is_stub(t):
            result.append(_unavailable_track_dict(getattr(short, "id", None), url, i))
            continue
        result.append(track_to_dict(t, url, i))
    return result


def parse_url(url: str) -> dict | None:
    """Разбирает URL Яндекс.Музыки → тип + id."""
    import re
    from urllib.parse import urlparse
    p = urlparse(url.strip())
    clean = p.scheme + "://" + p.netloc + p.path

    m = re.search(r"/album/(\d+)/track/(\d+)", clean)
    if m:
        return {"type": "track", "album_id": m.group(1), "track_id": m.group(2)}
    m = re.search(r"/album/(\d+)", clean)
    if m:
        return {"type": "album", "album_id": m.group(1)}
    m = re.search(r"/users/([^/]+)/playlists/(\d+)", clean)
    if m:
        return {"type": "playlist", "user": m.group(1), "kind": m.group(2)}
    m = re.search(r"/playlists/(lk\.[a-zA-Z0-9\-]+)", clean)
    if m:
        return {"type": "playlist_shared", "playlist_id": m.group(1)}
    m = re.search(r"/artist/(\d+)", clean)
    if m:
        return {"type": "artist", "artist_id": m.group(1)}
    return None


def _pick_download_info(infos, quality: str):
    """quality 0/1/2 как у CLI: хуже / среднее / лучшее. Предпочитаем mp3."""
    if not infos:
        return None
    mp3s = [i for i in infos if str(getattr(i, "codec", "") or "").lower() == "mp3"]
    pool = mp3s or list(infos)
    pool.sort(key=lambda i: i.bitrate_in_kbps or 0)
    if quality == "0":
        return pool[0]
    if quality == "1" and len(pool) > 1:
        return pool[len(pool) // 2]
    return pool[-1]


def _cover_bytes(track, resolution: str) -> bytes:
    size = "1000x1000" if not resolution or resolution == "original" else str(resolution)
    if "x" not in size:
        size = f"{size}x{size}"
    try:
        data = track.download_cover_bytes(size=size)
        return data or b""
    except Exception:
        return b""


def _http_download(url: str, dest: Path, timeout: int = 60) -> None:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urlopen(req, timeout=timeout) as resp, tmp.open("wb") as out:
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        tmp.replace(dest)
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
        raise


def _tag_fields(path: Path, ym_track, track_id: str) -> tuple[str, str, str, str]:
    title = getattr(ym_track, "title", None) or path.stem
    artists = ", ".join(a.name for a in (getattr(ym_track, "artists", None) or []) if a and a.name)
    album = ""
    if getattr(ym_track, "albums", None):
        a0 = ym_track.albums[0]
        if a0:
            album = a0.title or ""
    return title, artists, album, str(track_id or "")


def _write_mp4_tags(path: Path, ym_track, track_id: str, cover_bytes: bytes) -> None:
    try:
        from mutagen.mp4 import MP4, MP4Cover
    except Exception:
        return
    try:
        audio = MP4(path)
    except Exception:
        return
    title, artists, album, tid = _tag_fields(path, ym_track, track_id)
    audio["\xa9nam"] = [title]
    if artists:
        audio["\xa9ART"] = [artists]
    if album:
        audio["\xa9alb"] = [album]
    if tid:
        audio["\xa9cmt"] = [tid]
    if cover_bytes:
        fmt = MP4Cover.FORMAT_PNG if cover_bytes[:8] == b"\x89PNG\r\n\x1a\n" else MP4Cover.FORMAT_JPEG
        audio["covr"] = [MP4Cover(cover_bytes, imageformat=fmt)]
    try:
        audio.save()
    except Exception:
        pass


def _write_audio_tags(path: Path, ym_track, track_id: str, cover_bytes: bytes) -> None:
    """Теги + обложка: ID3 для mp3, covr для m4a. Слэш в названии в файле допустим."""
    suffix = path.suffix.lower()
    if suffix in {".m4a", ".mp4", ".aac"}:
        _write_mp4_tags(path, ym_track, track_id, cover_bytes)
        return
    try:
        from mutagen.id3 import APIC, COMM, ID3, TALB, TIT2, TPE1, WOAR
        try:
            from mutagen.id3 import ID3NoHeaderError
        except ImportError:
            ID3NoHeaderError = Exception
    except Exception:
        return
    try:
        tags = ID3(path)
    except ID3NoHeaderError:
        tags = ID3()
    except Exception:
        return
    title, artists, album, tid = _tag_fields(path, ym_track, track_id)
    tags["TIT2"] = TIT2(encoding=3, text=title)
    if artists:
        tags["TPE1"] = TPE1(encoding=3, text=artists)
    if album:
        tags["TALB"] = TALB(encoding=3, text=album)
    if tid:
        tags.add(COMM(encoding=3, lang="eng", desc="yandex", text=tid))
        tags.add(WOAR(url=f"https://music.yandex.ru/track/{tid}"))
    if cover_bytes:
        mime = "image/png" if cover_bytes[:8] == b"\x89PNG\r\n\x1a\n" else "image/jpeg"
        tags.delall("APIC")
        tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover", data=cover_bytes))
    try:
        tags.save(path)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Менеджер клиента
# ---------------------------------------------------------------------------

class YMClient:
    """Синглтон-обёртка над Client. Все методы — синхронные, для фоновых потоков."""

    def __init__(self) -> None:
        self._client: Optional[Client] = None
        self._lock = threading.Lock()
        self._wave_station = self.WAVE_STATION
        self._wave_session_id: str | None = None
        self._wave_batch_id: str | None = None
        self._wave_last_id: str | None = None
        self._lyrics_cache: dict[str, dict | None] = {}
        self.last_playlist_meta: dict | None = None

    def _require(self) -> Client:
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        return c

    def _clear_session(self) -> None:
        self._client = None
        self._wave_session_id = None
        self._wave_batch_id = None
        self._wave_last_id = None
        self._lyrics_cache.clear()

    # ── Авторизация ────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Сбрасывает клиент и сессию волны — после выхода или смены токена."""
        with self._lock:
            self._clear_session()

    def ensure(self, token: str) -> bool:
        """Инициализирует клиент по токену. Возвращает True при успехе."""
        with self._lock:
            if self._client and getattr(self._client, "token", None) == token:
                return True
            try:
                self._client = Client(token).init()
                self._client._request.set_timeout(_PL_TIMEOUT)
                return True
            except Exception:
                self._client = None
                return False

    def start_device_auth(self, on_code, on_done, on_error, cancel_flag: threading.Event) -> None:
        """
        Запускает Device Flow в фоновом потоке.
        on_code(user_code, verification_url, expires_in) — показать пользователю код
        on_done(token_str) — авторизация успешна
        on_error(msg) — ошибка
        cancel_flag — Event, который нужно установить для отмены
        """
        def _worker():
            tmp = Client()
            try:
                def _cb(code):
                    on_code(code.user_code, code.verification_url, code.expires_in)

                token_obj = tmp.device_auth(
                    on_code=_cb,
                    should_cancel=lambda: cancel_flag.is_set(),
                )
                with self._lock:
                    self._client = Client(token_obj.access_token).init()
                on_done(token_obj.access_token)
            except DeviceAuthError as e:
                if cancel_flag.is_set():
                    on_error("cancelled")
                else:
                    on_error(str(e))
            except Exception as e:
                on_error(str(e))

        threading.Thread(target=_worker, daemon=True).start()

    @property
    def client(self) -> Optional[Client]:
        return self._client

    # ── Список своих плейлистов ────────────────────────────────────────────

    def get_my_playlists(self) -> list[dict]:
        return self._get_my_playlists()

    def _get_my_playlists(self) -> list[dict]:
        c = self._client
        if not c:
            return []

        uid = c.me.account.uid if c.me and c.me.account else None

        def _system() -> list[dict]:
            if not uid:
                return []
            liked_pl = None
            # Карточке нужны только метаданные. users_playlists(kind=3) тянет
            # все лайкнутые треки и из-за этого тормозит всю сетку.
            try:
                items = c.playlists_list([f"{uid}:3"]) or []
                liked_pl = items[0] if items else None
            except Exception:
                liked_pl = None
            if liked_pl is None:
                liked_pl = c.users_playlists(kind=3, user_id=uid)
            if not liked_pl:
                return []
            if not liked_pl.title:
                liked_pl.title = "Мне нравится"
            card = playlist_to_dict(liked_pl, "system")
            try:
                card["count"] = len(liked_track_shorts(c))
            except Exception:
                pass
            return [card]

        def _smart() -> list[dict]:
            feed = c.feed()
            if not feed or not getattr(feed, "generated_playlists", None):
                return []
            return [
                playlist_to_dict(g.data, "smart")
                for g in feed.generated_playlists if getattr(g, "data", None)
            ]

        def _created() -> list[dict]:
            return [playlist_to_dict(pl, "created") for pl in (c.users_playlists_list() or [])]

        def _liked() -> list[dict]:
            return [
                playlist_to_dict(item.playlist, "liked")
                for item in (c.users_likes_playlists() or []) if getattr(item, "playlist", None)
            ]

        sections = [
            ("Мне нравится", _system),
            ("умные плейлисты", _smart),
            ("созданные плейлисты", _created),
            ("лайкнутые плейлисты", _liked),
        ]
        result: list[dict] = []
        with ThreadPoolExecutor(max_workers=len(sections)) as pool:
            futures = [(name, pool.submit(fn)) for name, fn in sections]
            for name, fut in futures:
                try:
                    result.extend(fut.result())
                except Exception as e:
                    print(f"Ошибка получения раздела «{name}»: {e}")
        return result

    def create_playlist(self, title: str) -> dict:
        """Создаёт свой плейлист (приватный) и возвращает карточку для интерфейса."""
        return self._create_playlist(title)

    def _create_playlist(self, title: str) -> dict:
        c = self._require()
        name = (title or "").strip()
        if not name:
            raise ValueError("Введите название плейлиста")
        pl = c.users_playlists_create(name, visibility="private")
        if not pl:
            raise RuntimeError("Яндекс не вернул созданный плейлист")
        return playlist_to_dict(pl, "created")

    def rename_playlist(self, playlist_kind, title: str) -> dict:
        """Переименовывает плейлист, созданный самим пользователем."""
        return self._rename_playlist(playlist_kind, title)

    def _rename_playlist(self, playlist_kind, title: str) -> dict:
        self._require()
        kind = int(str(playlist_kind).strip())
        if kind == self.LIKED_PLAYLIST_KIND:
            raise RuntimeError("Системный плейлист «Мне нравится» переименовать нельзя")
        name = (title or "").strip()
        if not name:
            raise ValueError("Введите название плейлиста")
        pl = self._require().users_playlists_name(kind, name)
        if pl:
            return playlist_to_dict(pl, "created")
        return {
            "id": str(kind),
            "title": name,
            "owner": "",
            "count": 0,
            "cover": "",
            "url": "",
            "group": "created",
        }

    def delete_playlist(self, playlist_kind) -> bool:
        """Удаляет плейлист, созданный самим пользователем."""
        return self._delete_playlist(playlist_kind)

    def _delete_playlist(self, playlist_kind) -> bool:
        c = self._require()
        kind = int(playlist_kind)
        if kind == self.LIKED_PLAYLIST_KIND:
            raise RuntimeError("Системный плейлист «Мне нравится» удалить нельзя")
        if kind not in self._own_playlist_kinds():
            raise RuntimeError("Удалять можно только свои плейлисты")
        return bool(c.users_playlists_delete(kind))

    # ── Страницы исполнителя и альбома ────────────────────────────────────

    def get_artist(self, artist_id) -> dict:
        """Исполнитель: популярные треки + дискография (один запрос к API)."""
        return self._get_artist(artist_id)

    def _get_artist(self, artist_id) -> dict:
        c = self._require()
        info = c.artists_brief_info(artist_id)
        if not info or not info.artist:
            raise ValueError("Исполнитель не найден")

        source = f"https://music.yandex.ru/artist/{artist_id}"
        tracks = [
            track_to_dict(t, source, i)
            for i, t in enumerate(info.popular_tracks or [], 1)
        ]
        if not tracks:
            try:
                res = c.artists_tracks(artist_id, page_size=50)
                tracks = [track_to_dict(t, source, i)
                          for i, t in enumerate((res.tracks if res else []) or [], 1)]
            except Exception:
                pass
        tracks = tracks[:10]

        albums, seen = [], set()
        for al in list(info.albums or []) + list(info.also_albums or []):
            if not al or al.id is None or str(al.id) in seen:
                continue
            seen.add(str(al.id))
            albums.append(album_to_dict(al))
        albums.sort(key=lambda a: (a["year"] or 0), reverse=True)

        return {"artist": artist_to_dict(info.artist), "tracks": tracks, "albums": albums}

    def get_artist_tracks(self, artist_id, page: int = 0, page_size: int = 200) -> dict:
        """Все треки исполнителя одним ответом (страницы API запрашиваются внутри)."""
        return self._get_artist_tracks(artist_id, page, page_size)

    def _get_artist_tracks(self, artist_id, page: int = 0, page_size: int = 200) -> dict:
        c = self._require()
        source = f"https://music.yandex.ru/artist/{artist_id}/tracks"
        tracks, total, page_i = [], None, 0
        while page_i < 80:
            res = c.artists_tracks(artist_id, page=page_i, page_size=page_size)
            raw = (res.tracks if res else None) or []
            start = len(tracks)
            tracks.extend(track_to_dict(t, source, start + i) for i, t in enumerate(raw, 1))
            pager = getattr(res, "pager", None)
            if pager is not None:
                total = getattr(pager, "total", total)
            if not raw or len(raw) < page_size:
                break
            if total is not None and len(tracks) >= int(total):
                break
            page_i += 1
        return {
            "tracks": tracks,
            "page": 0,
            "has_more": False,
            "total": int(total) if total is not None else len(tracks),
        }

    def get_album(self, album_id) -> dict:
        """Альбом со списком треков."""
        return self._get_album(album_id)

    def _get_album(self, album_id) -> dict:
        c = self._require()
        al = c.albums_with_tracks(album_id)
        if not al:
            raise ValueError("Альбом не найден")
        source = f"https://music.yandex.ru/album/{album_id}"
        tracks, num = [], 1
        for vol in (al.volumes or []):
            for t in (vol or []):
                tracks.append(track_to_dict(t, source, num))
                num += 1
        return {"album": album_to_dict(al), "tracks": tracks}

    def fetch_tracks(self, url: str) -> list[dict]:
        """Возвращает список треков для одного URL."""
        return self._fetch_tracks(url)

    def _playlist_tracks(self, pl, url: str) -> list[dict]:
        tracks = tracks_from_playlist(pl, url)
        expected = int(getattr(pl, "track_count", 0) or 0)
        title = getattr(pl, "title", None) or ""
        self.last_playlist_meta = {
            "title": title,
            "track_count": expected,
            "returned": len(tracks),
        }
        return tracks

    def _fetch_tracks(self, url: str) -> list[dict]:
        self.last_playlist_meta = None
        c = self._require()
        parsed = parse_url(url)
        if not parsed:
            raise ValueError(f"Не удалось распознать URL: {url}")

        kind = parsed["type"]

        if kind == "track":
            results = c.tracks([f"{parsed['track_id']}:{parsed['album_id']}"])
            if not results:
                raise ValueError("Трек не найден")
            return [track_to_dict(results[0], url, 1)]

        if kind == "album":
            album = c.albums_with_tracks(parsed["album_id"])
            if not album:
                raise ValueError("Альбом не найден")
            out, num = [], 1
            for vol in (album.volumes or []):
                for t in (vol or []):
                    out.append(track_to_dict(t, url, num))
                    num += 1
            return out

        if kind == "playlist":
            pl = fetch_user_playlist(c, parsed["kind"], parsed["user"])
            if not pl:
                raise ValueError("Плейлист не найден")
            return self._playlist_tracks(pl, url)

        if kind == "playlist_shared":
            pl = fetch_shared_playlist(c, parsed["playlist_id"])
            if not pl:
                raise ValueError("Плейлист не найден")
            return self._playlist_tracks(pl, url)

        if kind == "artist":
            result = c.artists_tracks(parsed["artist_id"], page_size=50)
            if not result:
                return []
            return [track_to_dict(t, url, i) for i, t in enumerate(result.tracks or [], 1)]

        return []

    def search_tracks(self, text: str) -> list[dict]:
        """Полнотекстовый поиск треков в Яндекс.Музыке."""
        return self._search_tracks(text)

    def _search_tracks(self, text: str) -> list[dict]:
        c = self._require()
        result = c.search(text, type_="track")
        if not result or not result.tracks:
            return []
        tracks = result.tracks.results or []
        return [track_to_dict(t, f"search:{text}", i) for i, t in enumerate(tracks, 1)]

    def search_all(self, text: str) -> dict:
        """Поиск сразу по трекам, исполнителям и альбомам — один запрос к API."""
        return self._search_all(text)

    def _search_all(self, text: str) -> dict:
        c = self._require()
        result = c.search(text, type_="all")
        if not result:
            return {"tracks": [], "artists": [], "albums": []}

        def _results(section):
            block = getattr(result, section, None)
            return (block.results if block else None) or []

        return {
            "tracks": [track_to_dict(t, f"search:{text}", i)
                       for i, t in enumerate(_results("tracks"), 1)],
            "artists": [artist_to_dict(a) for a in _results("artists") if a],
            "albums": [album_to_dict(al) for al in _results("albums") if al],
        }

    # ── Моя волна ────────────────────────────────────────────────────────

    WAVE_STATION = "user:onyourwave"

    def _reset_wave_session(self, station: str) -> None:
        self._wave_station = station
        self._wave_session_id = None
        self._wave_batch_id = None
        self._wave_last_id = None

    def _rotor_post(self, path: str, payload: dict):
        c = self._require()
        url = f"{c.base_url.rstrip('/')}/{path.lstrip('/')}"
        return c.request.post(url, json=payload)

    @staticmethod
    def _pick(data: dict, *keys):
        for key in keys:
            val = data.get(key)
            if val not in (None, ""):
                return val
        return None

    def _wave_session_feedback(self, event_type: str, **extra) -> None:
        sid = self._wave_session_id
        if not sid:
            return
        body = {
            "event": {
                "type": event_type,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                **extra,
            },
            "batchId": self._wave_batch_id,
        }
        try:
            self._rotor_post(f"rotor/session/{sid}/feedback", body)
        except Exception:
            pass

    def _wave_session_feedback_async(self, event_type: str, **extra) -> None:
        threading.Thread(
            target=self._wave_session_feedback,
            args=(event_type,),
            kwargs=extra,
            daemon=True,
        ).start()

    def _tracks_from_sequence(
        self,
        sequence,
        seen: list[str],
        seen_set: set[str],
        start_num: int,
        limit: int,
    ) -> list[dict]:
        collected: list[dict] = []
        c = self._client
        for item in sequence or []:
            raw = item.get("track") if isinstance(item, dict) else getattr(item, "track", None)
            if raw is None:
                continue
            t = Track.de_json(raw, c) if isinstance(raw, dict) else raw
            if t is None or t.id is None:
                continue
            tid = str(t.id)
            if tid in seen_set:
                continue
            seen_set.add(tid)
            seen.append(tid)
            self._wave_last_id = tid
            collected.append(track_to_dict(t, "wave", start_num + len(collected)))
            if len(collected) >= limit:
                break
        return collected

    def _wave_session_new(self, station: str) -> dict:
        data = self._rotor_post("rotor/session/new", {
            "seeds": [station],
            "includeTracksInResponse": True,
            "includeWaveModel": True,
            "interactive": True,
        })
        if not isinstance(data, dict):
            raise RuntimeError("Пустой ответ session/new")
        sid = self._pick(data, "radio_session_id", "radioSessionId")
        if not sid:
            raise RuntimeError("Нет radioSessionId")
        self._wave_session_id = str(sid)
        bid = self._pick(data, "batch_id", "batchId")
        if bid:
            self._wave_batch_id = str(bid)
        self._wave_session_feedback_async("radioStarted", **{"from": f"radio-web-{station}"})
        return data

    def _wave_session_more(self) -> dict:
        sid = self._wave_session_id
        if not sid:
            raise RuntimeError("Нет сессии волны")
        payload = {}
        if self._wave_last_id:
            payload["queue"] = [self._wave_last_id]
        data = self._rotor_post(f"rotor/session/{sid}/tracks", payload)
        if not isinstance(data, dict):
            raise RuntimeError("Пустой ответ session/tracks")
        bid = self._pick(data, "batch_id", "batchId")
        if bid:
            self._wave_batch_id = str(bid)
        return data

    def get_wave_tracks(
        self,
        seen_ids: list[str] | None = None,
        target: int = 8,
        start_num: int = 1,
        station: str | None = None,
    ) -> tuple[list[dict], list[str]]:
        """
        Одна порция волны — один запрос. Не крутим цикл до N треков:
        первую пачку отдаём сразу, следующую UI подгружает в фоне.

        Сначала /rotor/session/* (треки уже в ответе session/new).
        Если сессия недоступна — старый rotor_station_tracks.
        """
        return self._get_wave_tracks(seen_ids, target, start_num, station)

    def _get_wave_tracks(
        self,
        seen_ids: list[str] | None,
        target: int,
        start_num: int,
        station: str | None,
    ) -> tuple[list[dict], list[str]]:
        self._require()
        st = (station or "").strip() or self.WAVE_STATION
        seen = list(seen_ids or [])
        seen_set = set(seen)
        if st != self._wave_station or not seen:
            self._reset_wave_session(st)
        else:
            self._wave_station = st

        try:
            data = (self._wave_session_new(st) if not self._wave_session_id else self._wave_session_more())
            seq = self._pick(data, "sequence") or []
            collected = self._tracks_from_sequence(seq, seen, seen_set, start_num, target)
            if collected:
                return collected, seen
            if self._wave_session_id:
                self._reset_wave_session(st)
                data = self._wave_session_new(st)
                seq = self._pick(data, "sequence") or []
                collected = self._tracks_from_sequence(seq, seen, seen_set, start_num, target)
                if collected:
                    return collected, seen
        except Exception:
            self._reset_wave_session(st)

        return self._get_wave_legacy(st, seen, seen_set, start_num, target)

    def _get_wave_legacy(
        self,
        station: str,
        seen: list[str],
        seen_set: set[str],
        start_num: int,
        target: int,
    ) -> tuple[list[dict], list[str]]:
        """Запасной путь: один вызов старого rotor_station_tracks."""
        c = self._require()
        queue = seen[-1] if seen else None
        result = c.rotor_station_tracks(station, queue=queue)
        if not result or not result.sequence:
            return [], seen
        collected: list[dict] = []
        for item in result.sequence:
            t = getattr(item, "track", None)
            if t is None or t.id is None:
                continue
            tid = str(t.id)
            if tid in seen_set:
                continue
            seen_set.add(tid)
            seen.append(tid)
            self._wave_last_id = tid
            collected.append(track_to_dict(t, "wave", start_num + len(collected)))
            if len(collected) >= target:
                break
        return collected, seen

    # ── Добавление / удаление трека в плейлисте ─────────────────────────

    # Системный плейлист «Мне нравится» — им управляют только лайки,
    # users_playlists_* для него не работают.
    LIKED_PLAYLIST_KIND = 3

    def _own_playlist_kinds(self) -> set[int]:
        """kind всех плейлистов, созданных самим пользователем."""
        c = self._require()
        kinds: set[int] = set()
        try:
            for pl in (c.users_playlists_list() or []):
                if pl and pl.kind is not None:
                    kinds.add(int(pl.kind))
        except Exception as e:
            raise RuntimeError(f"Не удалось проверить список своих плейлистов: {e}")
        return kinds

    def _own_playlist(self, kind: int):
        """Возвращает свой плейлист по kind (с треками и актуальной revision)."""
        c = self._require()
        uid = c.me.account.uid if c.me and c.me.account else None
        pl = fetch_user_playlist(c, kind, uid)
        if not pl:
            raise RuntimeError("Плейлист не найден")
        return pl

    def add_track_to_playlist(self, playlist_kind, track_id, album_id) -> bool:
        """
        Добавляет трек в начало плейлиста, СОЗДАННОГО самим пользователем.
        В системные («Мне нравится»), умные (Плейлист дня и т.п.) и чужие
        плейлисты Яндекс добавлять треки не позволяет.
        """
        return self._add_track_to_playlist(playlist_kind, track_id, album_id)

    def _add_track_to_playlist(self, playlist_kind, track_id, album_id) -> bool:
        c = self._require()
        kind = int(playlist_kind)
        if kind not in self._own_playlist_kinds():
            raise RuntimeError("В этот плейлист нельзя добавлять треки — он не создан вами")
        pl = self._own_playlist(kind)
        c.users_playlists_insert_track(
            kind=kind,
            track_id=int(track_id),
            album_id=int(album_id) if album_id else 0,
            at=0,
            revision=pl.revision,
        )
        return True

    def remove_track_from_playlist(self, playlist_kind, track_id) -> bool:
        """
        Удаляет трек из плейлиста, созданного пользователем.
        Для «Мне нравится» (kind=3): снятие лайка, а если трек уже снят
        с сервиса и остался серой строкой — вырезаем его из системного плейлиста.
        """
        return self._remove_track_from_playlist(playlist_kind, track_id)

    def _remove_track_from_playlist(self, playlist_kind, track_id) -> bool:
        self._require()
        kind = int(playlist_kind)
        if kind == self.LIKED_PLAYLIST_KIND:
            return self._remove_from_liked_playlist(track_id)
        self._delete_playlist_track_at(kind, track_id)
        return True

    def remove_tracks_from_playlist(self, playlist_kind, track_ids) -> int:
        """
        Удаляет набор треков одним проходом.
        Позиции с конца, диапазонами — иначе revision плейлиста разъедется.
        """
        return self._remove_tracks_from_playlist(playlist_kind, track_ids)

    def _remove_tracks_from_playlist(self, playlist_kind, track_ids) -> int:
        self._require()
        kind = int(str(playlist_kind).strip())
        ids = [str(x) for x in (track_ids or []) if str(x)]
        if not ids:
            return 0
        if kind == self.LIKED_PLAYLIST_KIND:
            return self._remove_tracks_from_liked(ids)
        return self._remove_tracks_by_ids(kind, ids)

    def _merge_index_ranges(self, indices: list[int]) -> list[tuple[int, int]]:
        """Индексы → полуинтервалы [from, to), как ждёт users_playlists_delete_track."""
        if not indices:
            return []
        xs = sorted(set(indices))
        ranges: list[tuple[int, int]] = []
        start = prev = xs[0]
        for i in xs[1:]:
            if i == prev + 1:
                prev = i
                continue
            ranges.append((start, prev + 1))
            start = prev = i
        ranges.append((start, prev + 1))
        return ranges

    def _remove_tracks_by_ids(self, kind: int, track_ids: list[str]) -> int:
        """Удаляет указанные id из своего плейлиста, с конца и с обновлением revision."""
        c = self._require()
        wanted = set(track_ids)
        removed = 0
        for _ in range(400):
            pl = self._own_playlist(kind)
            indices = [
                i for i, short in enumerate(pl.tracks or [])
                if short is not None and str(getattr(short, "id", "")) in wanted
            ]
            if not indices:
                break
            a, b = self._merge_index_ranges(indices)[-1]
            c.users_playlists_delete_track(
                kind=kind,
                from_=a,
                to=b,
                revision=pl.revision,
            )
            removed += b - a
        return removed

    def _remove_tracks_from_liked(self, track_ids: list[str]) -> int:
        removed = 0
        seen: set[str] = set()
        for tid in track_ids:
            if not tid or tid in seen:
                continue
            seen.add(tid)
            try:
                self._remove_from_liked_playlist(tid)
                removed += 1
            except Exception:
                continue
        return removed

    def _delete_playlist_track_at(self, kind: int, track_id) -> None:
        """Удаляет трек из плейлиста по позиции — API не умеет удалять по id."""
        c = self._require()
        pl = self._own_playlist(kind)
        target = str(track_id)
        index = None
        for i, short in enumerate(pl.tracks or []):
            if short is not None and str(getattr(short, "id", "")) == target:
                index = i
                break
        if index is None:
            raise RuntimeError("Трек не найден в плейлисте")
        c.users_playlists_delete_track(
            kind=kind,
            from_=index,
            to=index + 1,
            revision=pl.revision,
        )

    def _remove_from_liked_playlist(self, track_id) -> bool:
        """
        «Мне нравится»: живой трек уходит снятием лайка.
        Удалённый с сервиса трек Яндекс сам снимает лайк, но строка остаётся
        в системном плейлисте — её нужно вырезать по позиции.
        """
        try:
            self._set_track_liked(track_id, False)
        except Exception:
            pass
        try:
            self._delete_playlist_track_at(self.LIKED_PLAYLIST_KIND, track_id)
        except RuntimeError:
            return True
        return True

    def get_liked_track_ids(self) -> list[str]:
        """Id всех треков, отмеченных «Мне нравится»."""
        return self._get_liked_track_ids()

    def _get_liked_track_ids(self) -> list[str]:
        c = self._client
        if not c:
            return []
        likes = c.users_likes_tracks()
        if not likes:
            return []
        seen, out = set(), []
        for t in likes.tracks or []:
            tid = str(getattr(t, "id", "") or "").split(":", 1)[0]
            if tid and tid not in seen:
                seen.add(tid)
                out.append(tid)
        return out

    def set_track_liked(self, track_id: str, liked: bool) -> bool:
        """Ставит/снимает отметку «Мне нравится» треку."""
        return self._set_track_liked(track_id, liked)

    def _set_track_liked(self, track_id: str, liked: bool) -> bool:
        c = self._require()
        if liked:
            return bool(c.users_likes_tracks_add(track_id))
        return bool(c.users_likes_tracks_remove(track_id))

    def get_liked_library(self) -> dict:
        """Любимые исполнители и понравившиеся альбомы — как в коллекции Яндекса."""
        return self._get_liked_library()

    def _get_liked_library(self) -> dict:
        c = self._client
        if not c:
            return {"artists": [], "albums": []}

        def _artists() -> list[dict]:
            out = []
            for item in (c.users_likes_artists() or []):
                a = getattr(item, "artist", None)
                if a:
                    out.append(artist_to_dict(a))
            return out

        def _albums() -> list[dict]:
            out = []
            for item in (c.users_likes_albums() or []):
                al = getattr(item, "album", None)
                if al:
                    out.append(album_to_dict(al))
            return out

        with ThreadPoolExecutor(max_workers=2) as pool:
            fa = pool.submit(_artists)
            fb = pool.submit(_albums)
            try:
                artists = fa.result()
            except Exception as e:
                print(f"Ошибка любимых исполнителей: {e}")
                artists = []
            try:
                albums = fb.result()
            except Exception as e:
                print(f"Ошибка понравившихся альбомов: {e}")
                albums = []
        return {"artists": artists, "albums": albums}

    def set_artist_liked(self, artist_id: str, liked: bool) -> bool:
        """Добавляет/убирает исполнителя из любимых."""
        return self._set_artist_liked(artist_id, liked)

    def _set_artist_liked(self, artist_id: str, liked: bool) -> bool:
        c = self._require()
        if liked:
            return bool(c.users_likes_artists_add(artist_id))
        return bool(c.users_likes_artists_remove(artist_id))

    def set_album_liked(self, album_id: str, liked: bool) -> bool:
        """Добавляет/убирает альбом из понравившихся."""
        return self._set_album_liked(album_id, liked)

    def _set_album_liked(self, album_id: str, liked: bool) -> bool:
        c = self._require()
        if liked:
            return bool(c.users_likes_albums_add(album_id))
        return bool(c.users_likes_albums_remove(album_id))

    def get_disliked_library(self) -> dict:
        """Треки и исполнители с отметкой «Не рекомендовать»."""
        return self._get_disliked_library()

    def _get_disliked_library(self) -> dict:
        c = self._client
        if not c:
            return {"tracks": [], "artists": []}

        def _tracks() -> list[dict]:
            likes = c.users_dislikes_tracks()
            if not likes:
                return []
            out = []
            for i, short in enumerate(likes.tracks or [], 1):
                t = getattr(short, "track", None)
                if t is None:
                    try:
                        t = short.fetch_track()
                    except Exception:
                        t = None
                if t is None:
                    out.append(_unavailable_track_dict(getattr(short, "id", None), "dislikes", i))
                else:
                    out.append(track_to_dict(t, "dislikes", i))
            return out

        def _artists() -> list[dict]:
            out = []
            for item in (c.users_dislikes_artists() or []):
                a = getattr(item, "artist", None) or item
                if a and getattr(a, "id", None) is not None:
                    out.append(artist_to_dict(a))
            return out

        with ThreadPoolExecutor(max_workers=2) as pool:
            ft = pool.submit(_tracks)
            fa = pool.submit(_artists)
            try:
                tracks = ft.result()
            except Exception as e:
                print(f"Ошибка дизлайков треков: {e}")
                tracks = []
            try:
                artists = fa.result()
            except Exception as e:
                print(f"Ошибка дизлайков исполнителей: {e}")
                artists = []
        return {"tracks": tracks, "artists": artists}

    def set_track_disliked(self, track_id: str, disliked: bool) -> bool:
        """Ставит/снимает отметку «Не рекомендовать» треку."""
        return self._set_track_disliked(track_id, disliked)

    def _set_track_disliked(self, track_id: str, disliked: bool) -> bool:
        c = self._require()
        if disliked:
            return bool(c.users_dislikes_tracks_add(track_id))
        return bool(c.users_dislikes_tracks_remove(track_id))

    def set_artist_disliked(self, artist_id: str, disliked: bool) -> bool:
        """Ставит/снимает отметку «Не рекомендовать» исполнителю."""
        return self._set_artist_disliked(artist_id, disliked)

    def _set_artist_disliked(self, artist_id: str, disliked: bool) -> bool:
        c = self._require()
        if disliked:
            return bool(c.users_dislikes_artists_add(artist_id))
        return bool(c.users_dislikes_artists_remove(artist_id))

    def get_lyrics_files(self, track_id: str) -> dict:
        """Сырые LRC и TEXT с API. Не выдумывает текст."""
        return self._get_lyrics_files(track_id)

    def _get_lyrics_files(self, track_id: str) -> dict:
        c = self._require()
        out: dict[str, str | None] = {"lrc": None, "text": None}
        for fmt, key in (("LRC", "lrc"), ("TEXT", "text")):
            try:
                lyrics = c.tracks_lyrics(track_id, format_=fmt)
                raw = lyrics.fetch_lyrics() if lyrics else None
            except Exception:
                continue
            if raw:
                out[key] = raw
        return out

    def get_lyrics(self, track_id: str) -> dict | None:
        """Текст песни. Сначала LRC (тайминг строк), иначе обычный TEXT."""
        return self._get_lyrics(track_id)

    def _get_lyrics(self, track_id: str) -> dict | None:
        if track_id in self._lyrics_cache:
            return self._lyrics_cache[track_id]
        c = self._require()
        payload = {"text": None, "sync": None}
        for fmt in ("LRC", "TEXT"):
            try:
                lyrics = c.tracks_lyrics(track_id, format_=fmt)
                raw = lyrics.fetch_lyrics() if lyrics else None
            except Exception:
                continue
            if not raw:
                continue
            if fmt == "LRC":
                sync = parse_lrc(raw)
                if sync:
                    payload["sync"] = sync
                    payload["text"] = "\n".join(x["text"] for x in sync)
                    break
            else:
                payload["text"] = raw
                break
        out = payload if (payload["text"] or payload["sync"]) else None
        self._lyrics_cache[track_id] = out
        return out

    def download_track_to(self, track_id: str, dest: Path, cfg: dict | None = None) -> Path:
        """
        Качает трек средствами yandex_music в уже безопасный dest.
        Нужен для названий со слэшем и другими символами, на которых
        консольный yandex-music-downloader падает с PYI-ошибкой.
        """
        cfg = cfg or {}
        token = str(cfg.get("token") or "").strip()
        if token:
            self.ensure(token)
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        link, ym_track, cover_bytes = self._download_meta(track_id, cfg)
        if not link:
            raise RuntimeError("Пустая ссылка на файл")
        timeout = 60
        try:
            timeout = max(20, int(cfg.get("timeout") or 60))
        except (TypeError, ValueError):
            pass
        _http_download(link, dest, timeout=timeout)
        _write_audio_tags(dest, ym_track, track_id, cover_bytes)
        return dest

    def _download_meta(self, track_id: str, cfg: dict) -> tuple[str, object, bytes]:
        c = self._require()
        infos = c.tracks_download_info(track_id, get_direct_links=True)
        tracks = c.tracks(track_id) or []
        ym_track = tracks[0] if tracks else None
        best = _pick_download_info(infos, str(cfg.get("quality", "2")))
        if not best:
            raise RuntimeError("Нет ссылки на скачивание")
        link = best.direct_link
        if not link:
            link = best.get_direct_link()
        cover_bytes = b""
        if cfg.get("embed_cover") and ym_track is not None:
            cover_bytes = _cover_bytes(ym_track, cfg.get("cover_resolution", "original"))
        return link, ym_track, cover_bytes

    def get_preview_url(self, track_id: str) -> str:
        """Возвращает прямую ссылку на аудио (лучшее mp3) для превью."""
        return self._get_preview_url(track_id)

    def _get_preview_url(self, track_id: str) -> str:
        c = self._require()
        infos = c.tracks_download_info(track_id, get_direct_links=True)
        if not infos:
            raise ValueError("Нет ссылок на скачивание")
        mp3s = [i for i in infos if i.codec == "mp3"]
        best = max(mp3s or infos, key=lambda i: i.bitrate_in_kbps or 0)
        return best.direct_link or best.get_direct_link()
