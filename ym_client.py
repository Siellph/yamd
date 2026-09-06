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
            "album_id": None,
            "duration": "—",
            "cover_uri": "",
            "cover_uri_tmpl": "",
            "status": "idle",
            "source_url": source_url,
        }
    artists = ", ".join(a.name for a in (t.artists or []) if a and a.name)
    album = ""
    album_id = None
    cover_uri = ""
    cover_uri_tmpl = ""
    if t.albums:
        a0 = t.albums[0]
        if a0:
            album = a0.title or ""
            album_id = a0.id
            if a0.cover_uri:
                cover_uri_tmpl = "https://" + a0.cover_uri
                cover_uri = cover_uri_tmpl.replace("%%", "100x100")
    return {
        "id": str(t.id),
        "num": num,
        "title": t.title or "Без названия",
        "artist": artists or "Неизвестный исполнитель",
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

        result = []
        uid = c.me.account.uid if c.me and c.me.account else None

        # Вспомогательная функция для форматирования в словарь
        def _format_playlist(pl, group: str) -> dict:
            cover = ""
            if pl.cover and getattr(pl.cover, 'uri', None):
                cover = "https://" + pl.cover.uri.replace("%%", "100x100")

            owner_login = ""
            if getattr(pl, 'owner', None) and getattr(pl.owner, 'login', None):
                owner_login = pl.owner.login

            url_owner = owner_login or "yandexmusic"

            return {
                "id": str(pl.kind),
                "title": pl.title or "Плейлист",
                "owner": owner_login,
                "count": pl.track_count or 0,
                "cover": cover,
                "url": f"https://music.yandex.ru/users/{url_owner}/playlists/{pl.kind}",
                "group": group
            }

        # 1. Системный плейлист "Мне нравится" (Лайкнутые треки)
        if uid:
            try:
                liked_pl = c.users_playlists(kind=3, user_id=uid)
                if liked_pl:
                    if not liked_pl.title:
                        liked_pl.title = "Мне нравится"
                    result.append(_format_playlist(liked_pl, "system"))
            except Exception as e:
                print(f"Ошибка получения 'Мне нравится': {e}")

        # 2. Умные плейлисты Яндекса (Плейлист дня, Премьера, Дежавю и т.д.)
        try:
            feed = c.feed()
            if feed and getattr(feed, 'generated_playlists', None):
                for gpl in feed.generated_playlists:
                    if getattr(gpl, 'data', None):
                        result.append(_format_playlist(gpl.data, "smart"))
        except Exception as e:
            print(f"Ошибка получения умных плейлистов: {e}")

        # 3. Созданные пользователем плейлисты
        try:
            pls = c.users_playlists_list() or []
            for pl in pls:
                result.append(_format_playlist(pl, "created"))
        except Exception as e:
            print(f"Ошибка получения созданных плейлистов: {e}")

        # 4. Лайкнутые чужие плейлисты
        try:
            pls_likes = c.users_likes_playlists() or []
            for item in pls_likes:
                if getattr(item, 'playlist', None):
                    result.append(_format_playlist(item.playlist, "liked"))
        except Exception as e:
            print(f"Ошибка получения лайкнутых плейлистов: {e}")

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

    # ── Моя волна ────────────────────────────────────────────────────────

    WAVE_STATION = "user:onyourwave"
    WAVE_MAX_REQUESTS = 12  # потолок запросов за один вызов, чтобы не зациклиться

    def _wave_feedback(self, method: str, *args, **kwargs) -> None:
        """
        Мягкая обёртка над rotor_station_feedback_* — сигнатуры отличаются
        между версиями библиотеки, а без обратной связи станция не двигается
        вперёд и начинает повторять уже выданные треки.
        """
        c = self._client
        fn = getattr(c, method, None)
        if not fn:
            return
        try:
            fn(*args, **kwargs)
        except Exception:
            pass

    def _wave_feedback_async(self, method: str, *args, **kwargs) -> None:
        """
        Как _wave_feedback, но не блокирует сбор треков: trackStarted/trackFinished
        не нужны станции немедленно, а ждать их ответа синхронно — то, из-за чего
        загрузка волны занимала секунды на каждую порцию треков.
        """
        threading.Thread(
            target=self._wave_feedback, args=(method, *args), kwargs=kwargs, daemon=True
        ).start()

    def get_wave_tracks(
        self,
        seen_ids: list[str] | None = None,
        target: int = 20,
        start_num: int = 1,
    ) -> tuple[list[dict], list[str]]:
        """
        Возвращает очередную порцию НОВЫХ треков «Моей волны».

        Как это работает:
          * `queue` в API — это id ОДНОГО последнего проигранного трека,
            а не список. Передаём последний известный id.
          * После каждой порции отправляем station_feedback (trackStarted /
            trackFinished), иначе станция считает, что треки не прослушаны,
            и на следующий запрос выдаёт ровно тот же набор.
          * Всё равно дополнительно фильтруем по seen_ids — сервер иногда
            повторяет треки даже при корректной обратной связи.

        seen_ids  — id всех треков, уже полученных в текущей сессии волны
        target    — сколько новых треков набрать (делает несколько запросов подряд)
        start_num — с какого номера нумеровать треки в списке

        Возвращает (новые_треки, обновлённый_seen_ids).
        """
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")

        seen = list(seen_ids or [])
        seen_set = set(seen)
        collected: list[dict] = []
        requests_made = 0
        empty_streak = 0

        # Стартуем радио только в самом начале сессии волны
        if not seen:
            self._wave_feedback(
                "rotor_station_feedback_radio_started",
                self.WAVE_STATION,
                f"radio-web-{self.WAVE_STATION}",
            )

        while len(collected) < target and requests_made < self.WAVE_MAX_REQUESTS:
            requests_made += 1
            queue = seen[-1] if seen else None

            result = c.rotor_station_tracks(self.WAVE_STATION, queue=queue)
            if not result or not result.sequence:
                break

            batch_id = getattr(result, "batch_id", None)
            got_new = 0

            for item in result.sequence:
                t = getattr(item, "track", None)
                if t is None:
                    continue
                tid = str(t.id)
                if tid in seen_set:
                    continue  # дубликат — пропускаем
                seen_set.add(tid)
                seen.append(tid)
                collected.append(track_to_dict(t, "wave", start_num + len(collected)))
                got_new += 1

                # Сообщаем станции, что трек прослушан — так она сдвигает поток.
                # Асинхронно: ответ станции не нужен, чтобы продолжить сбор треков.
                self._wave_feedback_async(
                    "rotor_station_feedback_track_started",
                    self.WAVE_STATION, tid, batch_id,
                )
                self._wave_feedback_async(
                    "rotor_station_feedback_track_finished",
                    self.WAVE_STATION, tid, float(t.duration_ms or 0) / 1000, batch_id,
                )

                if len(collected) >= target:
                    break

            if got_new == 0:
                empty_streak += 1
                # Две пустые порции подряд — станция исчерпалась, дальше смысла нет
                if empty_streak >= 2:
                    break
            else:
                empty_streak = 0

        return collected, seen

    # ── Добавление трека в плейлист ─────────────────────────────────────

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

        # Проверяем, что плейлист действительно свой и редактируемый
        own_kinds = set()
        try:
            for pl in (c.users_playlists_list() or []):
                if pl and pl.kind is not None:
                    own_kinds.add(int(pl.kind))
        except Exception as e:
            raise RuntimeError(f"Не удалось проверить список своих плейлистов: {e}")

        if kind not in own_kinds:
            raise RuntimeError("В этот плейлист нельзя добавлять треки — он не создан вами")

        uid = c.me.account.uid if c.me and c.me.account else None
        pl = c.users_playlists(kind, uid) if uid else c.users_playlists(kind)
        if not pl:
            raise RuntimeError("Плейлист не найден")

        c.users_playlists_insert_track(
            kind=kind,
            track_id=int(track_id),
            album_id=int(album_id) if album_id else 0,
            at=0,
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

    # ── Текст песни ───────────────────────────────────────────────────────

    def get_lyrics(self, track_id: str) -> str | None:
        """Текст песни (обычный, без таймкодов). None — если недоступен."""
        c = self._client
        if not c:
            raise RuntimeError("Клиент не инициализирован")
        try:
            lyrics = c.tracks_lyrics(track_id, format_="TEXT")
        except Exception:
            return None
        if not lyrics:
            return None
        try:
            return lyrics.fetch_lyrics()
        except Exception:
            return None

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
