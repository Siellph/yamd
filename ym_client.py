"""
Обёртка над yandex_music.Client.
Отвечает за: авторизацию (Device Flow + токен), получение треков,
получение прямой ссылки для превью.
"""
from __future__ import annotations

import threading
from typing import Optional

from yandex_music import Client
from yandex_music.exceptions import DeviceAuthError

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def fmt_duration(ms: int | None) -> str:
    if not ms:
        return "—"
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"


def track_to_dict(t, source_url: str, num: int) -> dict:
    """Конвертирует yandex_music.Track → словарь для JS."""
    if t is None:
        return {
            "id": f"unknown_{num}",
            "num": num,
            "title": "Неизвестный трек",
            "artist": "",
            "album": "",
            "duration": "—",
            "cover_uri": "",
            "status": "idle",
            "source_url": source_url,
        }
    artists = ", ".join(a.name for a in (t.artists or []) if a and a.name)
    album = ""
    cover_uri = ""
    if t.albums:
        a0 = t.albums[0]
        if a0:
            album = a0.title or ""
            if a0.cover_uri:
                cover_uri = "https://" + a0.cover_uri.replace("%%", "100x100")
    return {
        "id": str(t.id),
        "num": num,
        "title": t.title or "Без названия",
        "artist": artists or "Неизвестный исполнитель",
        "album": album,
        "cover_uri": cover_uri,
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
        pls = c.users_playlists_list() or []
        result = []
        for pl in pls:
            cover = ""
            if pl.cover and pl.cover.uri:
                cover = "https://" + pl.cover.uri.replace("%%", "100x100")
            result.append({
                "id": str(pl.kind),
                "title": pl.title or "Плейлист",
                "owner": pl.owner.login if pl.owner else "",
                "count": pl.track_count or 0,
                "cover": cover,
                "url": f"https://music.yandex.ru/users/{pl.owner.login}/playlists/{pl.kind}" if pl.owner else "",
            })
        return result

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
