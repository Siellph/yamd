"""
Обёртка над yandex_music.Client.
Отвечает за: авторизацию (Device Flow + токен), получение треков,
получение прямой ссылки для превью.
"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional

from yandex_music import Client, Track
from yandex_music.exceptions import DeviceAuthError

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def fmt_duration(ms: int | None) -> str:
    if not ms:
        return "—"
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"


def cover_urls(uri: str | None, size: str = "100x100") -> tuple[str, str]:
    """(готовый url нужного размера, шаблон с %%) для cover_uri из API."""
    if not uri:
        return "", ""
    tmpl = "https://" + uri
    return tmpl.replace("%%", size), tmpl


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
    cover = ""
    if pl.cover and getattr(pl.cover, "uri", None):
        cover = "https://" + pl.cover.uri.replace("%%", "100x100")
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


def track_to_dict(t, source_url: str, num: int) -> dict:
    """Конвертирует yandex_music.Track → словарь для JS."""
    if t is None:
        return {
            "id": f"unknown_{num}",
            "num": num,
            "title": "Неизвестный трек",
            "artist": "",
            "artists": [],
            "album": "",
            "album_id": None,
            "duration": "—",
            "cover_uri": "",
            "cover_uri_tmpl": "",
            "status": "idle",
            "source_url": source_url,
        }
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
    }


def tracks_from_playlist(pl, url: str) -> list[dict]:
    """
    Извлекает треки из Playlist.
    TrackShort.track содержит полный Track — fetch_track() не нужен.
    """
    result = []
    for i, short in enumerate(pl.tracks or [], 1):
        if short is None:
            continue
        t = short.track if (short.track is not None) else None
        if t is None:
            try:
                t = short.fetch_track()
            except Exception:
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
        self._lyrics_cache: dict[str, str | None] = {}

    # ── Авторизация ────────────────────────────────────────────────────────

    def ensure(self, token: str) -> bool:
        """Инициализирует клиент по токену. Возвращает True при успехе."""
        with self._lock:
            if self._client and getattr(self._client, "token", None) == token:
                return True
            try:
                self._client = Client(token).init()
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
        c = self._client
        if not c:
            return []

        uid = c.me.account.uid if c.me and c.me.account else None

        # 1. Системный плейлист "Мне нравится" (Лайкнутые треки)
        def _system() -> list[dict]:
            if not uid:
                return []
            liked_pl = c.users_playlists(kind=3, user_id=uid)
            if not liked_pl:
                return []
            if not liked_pl.title:
                liked_pl.title = "Мне нравится"
            return [playlist_to_dict(liked_pl, "system")]

        # 2. Умные плейлисты Яндекса (Плейлист дня, Премьера, Дежавю и т.д.)
        def _smart() -> list[dict]:
            feed = c.feed()
            if not feed or not getattr(feed, 'generated_playlists', None):
                return []
            return [
                playlist_to_dict(g.data, "smart")
                for g in feed.generated_playlists if getattr(g, 'data', None)
            ]

        # 3. Созданные пользователем плейлисты
        def _created() -> list[dict]:
            return [playlist_to_dict(pl, "created") for pl in (c.users_playlists_list() or [])]

        # 4. Лайкнутые чужие плейлисты
        def _liked() -> list[dict]:
            return [
                playlist_to_dict(item.playlist, "liked")
                for item in (c.users_likes_playlists() or []) if getattr(item, 'playlist', None)
            ]

        # Четыре независимых запроса к API: последовательно это заметная пауза
        # перед показом страницы, поэтому запускаем их одновременно.
        sections = [("Мне нравится", _system), ("умные плейлисты", _smart),
                    ("созданные плейлисты", _created), ("лайкнутые плейлисты", _liked)]
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
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        name = (title or "").strip()
        if not name:
            raise ValueError("Введите название плейлиста")
        pl = c.users_playlists_create(name, visibility="private")
        if not pl:
            raise RuntimeError("Яндекс не вернул созданный плейлист")
        return playlist_to_dict(pl, "created")

    def delete_playlist(self, playlist_kind) -> bool:
        """Удаляет плейлист, созданный самим пользователем."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        kind = int(playlist_kind)
        if kind == self.LIKED_PLAYLIST_KIND:
            raise RuntimeError("Системный плейлист «Мне нравится» удалить нельзя")
        if kind not in self._own_playlist_kinds():
            raise RuntimeError("Удалять можно только свои плейлисты")
        return bool(c.users_playlists_delete(kind))

    # ── Страницы исполнителя и альбома ────────────────────────────────────

    def get_artist(self, artist_id) -> dict:
        """Исполнитель: популярные треки + дискография (один запрос к API)."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

        info = c.artists_brief_info(artist_id)
        if not info or not info.artist:
            raise ValueError("Исполнитель не найден")

        source = f"https://music.yandex.ru/artist/{artist_id}"
        tracks = [
            track_to_dict(t, source, i)
            for i, t in enumerate(info.popular_tracks or [], 1)
        ]
        if not tracks:
            # У некоторых исполнителей popular_tracks пуст — берём обычный список
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

    def get_artist_tracks(self, artist_id, page: int = 0, page_size: int = 80) -> dict:
        """Страница «все треки» исполнителя — как на music.yandex.ru/artist/.../tracks."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

        res = c.artists_tracks(artist_id, page=page, page_size=page_size)
        raw = (res.tracks if res else None) or []
        source = f"https://music.yandex.ru/artist/{artist_id}/tracks"
        start = page * page_size
        tracks = [track_to_dict(t, source, start + i) for i, t in enumerate(raw, 1)]

        pager = getattr(res, "pager", None)
        total = getattr(pager, "total", None) if pager else None
        loaded = start + len(tracks)
        has_more = len(raw) >= page_size
        if total is not None:
            has_more = loaded < int(total)
        return {
            "tracks": tracks,
            "page": page,
            "has_more": has_more,
            "total": int(total) if total else loaded,
        }

    def get_album(self, album_id) -> dict:
        """Альбом со списком треков."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

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

    # ── Получение треков по URL ────────────────────────────────────────────

    def fetch_tracks(self, url: str) -> list[dict]:
        """Возвращает список треков для одного URL."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

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
            pl = c.users_playlists(parsed["kind"], parsed["user"])
            if not pl:
                raise ValueError("Плейлист не найден")
            return tracks_from_playlist(pl, url)

        if kind == "playlist_shared":
            pl = c.playlist(parsed["playlist_id"])
            if not pl:
                raise ValueError("Плейлист не найден")
            return tracks_from_playlist(pl, url)

        if kind == "artist":
            result = c.artists_tracks(parsed["artist_id"], page_size=50)
            if not result:
                return []
            return [track_to_dict(t, url, i) for i, t in enumerate(result.tracks or [], 1)]

        return []

    # ── Поиск треков ───────────────────────────────────────────────────────

    def search_tracks(self, text: str) -> list[dict]:
        """Полнотекстовый поиск треков в Яндекс.Музыке."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        result = c.search(text, type_="track")
        if not result or not result.tracks:
            return []
        tracks = result.tracks.results or []
        return [track_to_dict(t, f"search:{text}", i) for i, t in enumerate(tracks, 1)]

    def search_all(self, text: str) -> dict:
        """Поиск сразу по трекам, исполнителям и альбомам — один запрос к API."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

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
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
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
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

        st = (station or "").strip() or self.WAVE_STATION
        seen = list(seen_ids or [])
        seen_set = set(seen)
        # Пустой seen — новый запуск волны, сессию сбрасываем
        if st != self._wave_station or not seen:
            self._reset_wave_session(st)
        else:
            self._wave_station = st

        try:
            data = self._wave_session_new(st) if not self._wave_session_id else self._wave_session_more()
            seq = self._pick(data, "sequence") or []
            collected = self._tracks_from_sequence(seq, seen, seen_set, start_num, target)
            if collected:
                return collected, seen
            if self._wave_session_id:
                # пустая порция — пробуем ещё раз со свежей сессией
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
        c = self._client
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
        c = self._client
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
        c = self._client
        uid = c.me.account.uid if c.me and c.me.account else None
        pl = c.users_playlists(kind, uid) if uid else c.users_playlists(kind)
        if not pl:
            raise RuntimeError("Плейлист не найден")
        return pl

    def add_track_to_playlist(self, playlist_kind, track_id, album_id) -> bool:
        """
        Добавляет трек в начало плейлиста, СОЗДАННОГО самим пользователем.
        В системные («Мне нравится»), умные (Плейлист дня и т.п.) и чужие
        плейлисты Яндекс добавлять треки не позволяет.
        """
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

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
        Для «Мне нравится» (kind=3) удаление — это снятие лайка.
        """
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

        kind = int(playlist_kind)
        if kind == self.LIKED_PLAYLIST_KIND:
            self.set_track_liked(track_id, False)
            return True

        if kind not in self._own_playlist_kinds():
            raise RuntimeError("Из этого плейлиста нельзя удалять треки — он не создан вами")

        pl = self._own_playlist(kind)

        # Индекс нужен точный и свежий: API удаляет по позиции, а не по id
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
        return True

    # ── Лайки ("Мне нравится") ───────────────────────────────────────────

    def get_liked_track_ids(self) -> list[str]:
        """Id всех треков, отмеченных «Мне нравится»."""
        c = self._client
        if not c:
            return []
        likes = c.users_likes_tracks()
        if not likes:
            return []
        # Не likes.tracks_ids — там id в виде "trackId:albumId" (TrackShort.track_id),
        # а весь остальной код (превью, скачивание, сердечки в списках) сверяется
        # по чистому numeric id (TrackShort.id), из-за чего лайки нигде не совпадали.
        return [str(t.id) for t in likes.tracks]

    def set_track_liked(self, track_id: str, liked: bool) -> bool:
        """Ставит/снимает отметку «Мне нравится» треку."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        if liked:
            return bool(c.users_likes_tracks_add(track_id))
        return bool(c.users_likes_tracks_remove(track_id))

    def get_liked_library(self) -> dict:
        """Любимые исполнители и понравившиеся альбомы — как в коллекции Яндекса."""
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

        artists, albums = [], []
        with ThreadPoolExecutor(max_workers=2) as pool:
            fa, fb = pool.submit(_artists), pool.submit(_albums)
            try:
                artists = fa.result()
            except Exception as e:
                print(f"Ошибка любимых исполнителей: {e}")
            try:
                albums = fb.result()
            except Exception as e:
                print(f"Ошибка понравившихся альбомов: {e}")
        return {"artists": artists, "albums": albums}

    def set_artist_liked(self, artist_id: str, liked: bool) -> bool:
        """Добавляет/убирает исполнителя из любимых."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        if liked:
            return bool(c.users_likes_artists_add(artist_id))
        return bool(c.users_likes_artists_remove(artist_id))

    def set_album_liked(self, album_id: str, liked: bool) -> bool:
        """Добавляет/убирает альбом из понравившихся."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        if liked:
            return bool(c.users_likes_albums_add(album_id))
        return bool(c.users_likes_albums_remove(album_id))

    # ── Текст песни ───────────────────────────────────────────────────────

    def get_lyrics(self, track_id: str) -> str | None:
        """Текст песни (обычный, без таймкодов). None — если недоступен."""
        if track_id in self._lyrics_cache:
            return self._lyrics_cache[track_id]
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        try:
            lyrics = c.tracks_lyrics(track_id, format_="TEXT")
        except Exception:
            self._lyrics_cache[track_id] = None
            return None
        if not lyrics:
            self._lyrics_cache[track_id] = None
            return None
        try:
            text = lyrics.fetch_lyrics()
        except Exception:
            text = None
        self._lyrics_cache[track_id] = text
        return text

    # ── Превью / прямая ссылка ────────────────────────────────────────────

    def get_preview_url(self, track_id: str) -> str:
        """Возвращает прямую ссылку на аудио (лучшее mp3) для превью."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        infos = c.tracks_download_info(track_id, get_direct_links=True)
        if not infos:
            raise ValueError("Нет ссылок на скачивание")
        # Берём лучший mp3 (не flac) — для превью в браузере
        mp3s = [i for i in infos if i.codec == "mp3"]
        best = max(mp3s or infos, key=lambda i: i.bitrate_in_kbps or 0)
        return best.direct_link or best.get_direct_link()
