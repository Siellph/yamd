"""
JS-API: все методы, доступные из JavaScript через window.pywebview.api.*
Тонкий слой — только маршрутизация, никакой бизнес-логики.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote
import os
import platform
import subprocess
import webview

import config as cfg_module
from downloader import DownloadManager
from local_play_server import read_audio_meta, read_ym_track_id
from ym_client import YMClient, fmt_duration


class Api:
    def __init__(self) -> None:
        self._cfg = cfg_module.load()
        self._ym = YMClient()
        self._window: Optional[webview.Window] = None

        self._dl = DownloadManager(
            on_status=self._on_dl_status,
            on_log=self._on_dl_log,
        )

        # Флаг отмены Device Flow
        self._auth_cancel = threading.Event()
        # Флаг отмены fetch_tracks (не блокирует, только сигнал)
        self._fetch_cancel = threading.Event()
        self._fetch_thread: Optional[threading.Thread] = None
        self._search_seq = 0
        self._dl_index_lock = threading.Lock()

    # ── Утилиты ───────────────────────────────────────────────────────────

    def _emit(self, event: str, payload) -> None:
        if self._window:
            js = f"window.dispatchEvent(new CustomEvent('py:{event}',{{detail:{json.dumps(payload)}}}));"
            self._window.evaluate_js(js)

    def _log(self, msg: str, kind: str = "info") -> None:
        self._emit("log", {"msg": msg, "kind": kind})

    def _on_dl_status(self, track_id: str, status: str) -> None:
        self._emit("track_status", {"id": track_id, "status": status})

    def _on_dl_log(self, msg: str, kind: str) -> None:
        self._log(msg, kind)

    # ── Конфиг ────────────────────────────────────────────────────────────

    def get_config(self) -> dict:
        return self._cfg

    def save_config(self, data: dict) -> bool:
        self._cfg.update(data)
        cfg_module.save(self._cfg)
        # Сбросить клиент если изменился токен
        return True

    # ── Авторизация: Device Flow ──────────────────────────────────────────

    def start_device_auth(self) -> None:
        """Запускает Device Flow. Результат → события py:auth_code / py:auth_done / py:auth_error."""
        self._auth_cancel.clear()

        def on_code(user_code, url, expires_in):
            self._emit("auth_code", {
                "user_code": user_code,
                "url": url,
                "expires_in": expires_in,
            })

        def on_done(token: str):
            self._cfg["token"] = token
            cfg_module.save(self._cfg)
            self._emit("auth_done", {"token": token})
            self._log("✓ Авторизация успешна! Токен сохранён.", "ok")

        def on_error(msg: str):
            if msg != "cancelled":
                self._emit("auth_error", {"msg": msg})
                self._log(f"✗ Ошибка авторизации: {msg}", "err")

        self._ym.start_device_auth(on_code, on_done, on_error, self._auth_cancel)

    def cancel_device_auth(self) -> None:
        self._auth_cancel.set()

    def login_with_token(self, token: str) -> bool:
        """Авторизоваться по готовому токену."""
        token = token.strip()
        if not token:
            self._log("Токен не может быть пустым", "err")
            return False
        ok = self._ym.ensure(token)
        if ok:
            self._cfg["token"] = token
            cfg_module.save(self._cfg)
            self._log("✓ Авторизация по токену успешна", "ok")
        else:
            self._log("✗ Неверный токен", "err")
        return ok

    # ── Плейлисты пользователя ────────────────────────────────────────────

    def get_my_playlists(self) -> None:
        """Возвращает список своих плейлистов через событие py:my_playlists."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("my_playlists", [])
                self._log("Нет авторизации для загрузки плейлистов", "err")
                return
            try:
                pls = self._ym.get_my_playlists()
                self._emit("my_playlists", pls)
            except Exception as e:
                self._log(f"Ошибка загрузки плейлистов: {e}", "err")
                self._emit("my_playlists", [])

        threading.Thread(target=_worker, daemon=True).start()

    # ── Получение треков ──────────────────────────────────────────────────

    def fetch_tracks(self, urls: list[str]) -> None:
        """Результат → py:tracks_ready."""
        if self._fetch_thread and self._fetch_thread.is_alive():
            self._log("Уже идёт загрузка", "err")
            return
        self._fetch_cancel.clear()

        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token:
                self._log("Введите токен в настройках", "err")
                self._emit("tracks_ready", [])
                return
            if not self._ym.ensure(token):
                self._emit("tracks_ready", [])
                return

            all_tracks: list[dict] = []
            for url in urls:
                if self._fetch_cancel.is_set():
                    break
                try:
                    tracks = self._ym.fetch_tracks(url)
                    all_tracks.extend(tracks)
                    self._log(f"Найдено {len(tracks)} трек(ов) — {url[:60]}", "ok")
                except Exception as e:
                    self._log(f"Ошибка: {e}", "err")

            self._emit("tracks_ready", all_tracks)

        self._fetch_thread = threading.Thread(target=_worker, daemon=True)
        self._fetch_thread.start()

    # ── Поиск треков ──────────────────────────────────────────────────────

    def search_tracks(self, query: str, seq: int = 0) -> None:
        """
        Поиск по трекам, исполнителям и альбомам → py:search_results.
        seq возвращается как есть: интерфейс печатает быстрее, чем отвечает API,
        и по нему отбрасывает ответы на уже неактуальные запросы.
        """
        self._search_seq = seq

        def _worker():
            empty = {"query": query, "seq": seq, "tracks": [], "artists": [], "albums": []}
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("search_results", empty)
                self._log("Нет авторизации для поиска", "err")
                return
            try:
                data = self._ym.search_all(query)
                data.update({"query": query, "seq": seq})
                # Пока ходили в сеть, пользователь мог набрать уже другой запрос
                if seq != getattr(self, "_search_seq", seq):
                    return
                self._emit("search_results", data)
            except Exception as e:
                self._log(f"Ошибка поиска: {e}", "err")
                self._emit("search_results", empty)

        threading.Thread(target=_worker, daemon=True).start()

    # ── Открытие плейлиста ────────────────────────────────────────────────

    def open_playlist(self, url: str) -> None:
        """Загружает треки плейлиста для просмотра. Результат → py:playlist_tracks."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("playlist_tracks", {"url": url, "tracks": []})
                self._log("Нет авторизации для открытия плейлиста", "err")
                return
            try:
                tracks = self._ym.fetch_tracks(url)
                self._emit("playlist_tracks", {"url": url, "tracks": tracks})
            except Exception as e:
                self._log(f"Ошибка открытия плейлиста: {e}", "err")
                self._emit("playlist_tracks", {"url": url, "tracks": []})

        threading.Thread(target=_worker, daemon=True).start()

    # ── Страницы исполнителя и альбома ────────────────────────────────────

    def open_artist(self, artist_id: str) -> None:
        """Результат → py:artist_page."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("artist_page", {"ok": False, "id": artist_id, "msg": "Нет авторизации"})
                return
            try:
                data = self._ym.get_artist(artist_id)
                data.update({"ok": True, "id": artist_id, "msg": ""})
                self._emit("artist_page", data)
            except Exception as e:
                self._emit("artist_page", {"ok": False, "id": artist_id, "msg": str(e)})
                self._log(f"Ошибка загрузки исполнителя: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def open_artist_tracks(self, artist_id: str, page: int = 0) -> None:
        """Порция треков исполнителя → py:artist_tracks_page."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("artist_tracks_page", {
                    "ok": False, "id": artist_id, "page": page,
                    "tracks": [], "has_more": False, "total": 0, "msg": "Нет авторизации",
                })
                return
            try:
                data = self._ym.get_artist_tracks(artist_id, page=int(page or 0))
                data.update({"ok": True, "id": artist_id, "msg": ""})
                self._emit("artist_tracks_page", data)
            except Exception as e:
                self._emit("artist_tracks_page", {
                    "ok": False, "id": artist_id, "page": page,
                    "tracks": [], "has_more": False, "total": 0, "msg": str(e),
                })
                self._log(f"Ошибка загрузки треков исполнителя: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def open_album(self, album_id: str) -> None:
        """Результат → py:album_page."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("album_page", {"ok": False, "id": album_id, "msg": "Нет авторизации"})
                return
            try:
                data = self._ym.get_album(album_id)
                data.update({"ok": True, "id": album_id, "msg": ""})
                self._emit("album_page", data)
            except Exception as e:
                self._emit("album_page", {"ok": False, "id": album_id, "msg": str(e)})
                self._log(f"Ошибка загрузки альбома: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    # ── Моя волна ─────────────────────────────────────────────────────────

    def start_wave(self, station: str = "") -> None:
        """Запускает волну (моя / по треку). Результат → py:wave_tracks."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            st = (station or "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("wave_tracks", {
                    "tracks": [], "seen": [], "append": False, "station": st,
                })
                self._log("Нет авторизации для запуска волны", "err")
                return
            try:
                tracks, seen = self._ym.get_wave_tracks(target=8, start_num=1, station=st or None)
                used = getattr(self._ym, "_wave_station", st) or st
                self._emit("wave_tracks", {
                    "tracks": tracks, "seen": seen, "append": False, "station": used,
                })
                self._log(f"🌊 Волна запущена: {len(tracks)} трек(ов)", "ok")
            except Exception as e:
                self._log(f"Ошибка запуска волны: {e}", "err")
                self._emit("wave_tracks", {
                    "tracks": [], "seen": [], "append": False, "station": st,
                })

        threading.Thread(target=_worker, daemon=True).start()

    def wave_next(self, seen_ids: list[str], start_num: int = 1, station: str = "") -> None:
        """Подгружает следующую порцию треков волны. Результат → py:wave_tracks (append)."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            st = (station or "").strip() or None
            if not token or not self._ym.ensure(token):
                self._emit("wave_tracks", {
                    "tracks": [], "seen": seen_ids or [], "append": True, "station": st or "",
                })
                return
            try:
                tracks, seen = self._ym.get_wave_tracks(
                    seen_ids=seen_ids, target=8, start_num=start_num, station=st
                )
                used = getattr(self._ym, "_wave_station", st) or st or ""
                self._emit("wave_tracks", {
                    "tracks": tracks, "seen": seen, "append": True, "station": used,
                })
                if tracks:
                    self._log(f"🌊 Добавлено {len(tracks)} новых трек(ов)", "ok")
                else:
                    self._log("🌊 Волна больше не выдаёт новых треков", "err")
            except Exception as e:
                self._log(f"Ошибка загрузки волны: {e}", "err")
                self._emit("wave_tracks", {
                    "tracks": [], "seen": seen_ids or [], "append": True, "station": st or "",
                })

        threading.Thread(target=_worker, daemon=True).start()

    def create_playlist(self, title: str) -> None:
        """Создаёт плейлист → py:playlist_created."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("playlist_created", {"ok": False, "playlist": None, "msg": "Нет авторизации"})
                return
            try:
                pl = self._ym.create_playlist(title)
                self._emit("playlist_created", {"ok": True, "playlist": pl, "msg": ""})
                self._log(f"✓ Создан плейлист «{pl.get('title', '')}»", "ok")
            except Exception as e:
                self._emit("playlist_created", {"ok": False, "playlist": None, "msg": str(e)})
                self._log(f"✗ Не удалось создать плейлист: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def delete_playlist(self, playlist_id: str) -> None:
        """Удаляет свой плейлист → py:playlist_deleted."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("playlist_deleted", {
                    "ok": False, "playlist_id": playlist_id, "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.delete_playlist(playlist_id)
                self._emit("playlist_deleted", {
                    "ok": True, "playlist_id": playlist_id, "msg": "",
                })
                self._log("✓ Плейлист удалён", "ok")
            except Exception as e:
                self._emit("playlist_deleted", {
                    "ok": False, "playlist_id": playlist_id, "msg": str(e),
                })
                self._log(f"✗ Не удалось удалить плейлист: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    # ── Добавление трека в плейлист ───────────────────────────────────────

    def add_to_playlist(self, playlist_id: str, track_id: str, album_id: Optional[str]) -> None:
        """Результат → py:add_to_playlist_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("add_to_playlist_result", {
                    "ok": False, "track_id": track_id, "playlist_id": playlist_id,
                    "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.add_track_to_playlist(playlist_id, track_id, album_id)
                self._emit("add_to_playlist_result", {
                    "ok": True, "track_id": track_id, "playlist_id": playlist_id, "msg": "",
                })
                self._log("✓ Трек добавлен в плейлист", "ok")
            except Exception as e:
                self._emit("add_to_playlist_result", {
                    "ok": False, "track_id": track_id, "playlist_id": playlist_id, "msg": str(e),
                })
                self._log(f"✗ Не удалось добавить трек в плейлист: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    # ── Удаление трека из плейлиста ───────────────────────────────────────

    def remove_from_playlist(self, playlist_id: str, track_id: str) -> None:
        """Результат → py:remove_from_playlist_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("remove_from_playlist_result", {
                    "ok": False, "track_id": track_id, "playlist_id": playlist_id,
                    "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.remove_track_from_playlist(playlist_id, track_id)
                self._emit("remove_from_playlist_result", {
                    "ok": True, "track_id": track_id, "playlist_id": playlist_id, "msg": "",
                })
                self._log("✓ Трек удалён из плейлиста", "ok")
            except Exception as e:
                self._emit("remove_from_playlist_result", {
                    "ok": False, "track_id": track_id, "playlist_id": playlist_id, "msg": str(e),
                })
                self._log(f"✗ Не удалось удалить трек из плейлиста: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    # ── Лайки ("Мне нравится") ──────────────────────────────────────────────

    def get_liked_ids(self) -> None:
        """Id всех лайкнутых треков → py:liked_ids."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("liked_ids", [])
                return
            try:
                ids = self._ym.get_liked_track_ids()
                self._emit("liked_ids", ids)
            except Exception as e:
                self._log(f"Ошибка загрузки лайков: {e}", "err")
                self._emit("liked_ids", [])

        threading.Thread(target=_worker, daemon=True).start()

    def get_liked_library(self) -> None:
        """Любимые исполнители и альбомы → py:liked_library."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("liked_library", {"artists": [], "albums": []})
                return
            try:
                self._emit("liked_library", self._ym.get_liked_library())
            except Exception as e:
                self._log(f"Ошибка загрузки коллекции: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def toggle_artist_like(self, artist_id: str, liked: bool) -> None:
        """Результат → py:artist_like_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("artist_like_result", {
                    "id": artist_id, "liked": not liked, "ok": False, "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.set_artist_liked(artist_id, liked)
                self._emit("artist_like_result", {
                    "id": artist_id, "liked": liked, "ok": True, "msg": "",
                })
            except Exception as e:
                self._emit("artist_like_result", {
                    "id": artist_id, "liked": not liked, "ok": False, "msg": str(e),
                })
                self._log(f"✗ Не удалось изменить лайк исполнителя: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def toggle_album_like(self, album_id: str, liked: bool) -> None:
        """Результат → py:album_like_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("album_like_result", {
                    "id": album_id, "liked": not liked, "ok": False, "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.set_album_liked(album_id, liked)
                self._emit("album_like_result", {
                    "id": album_id, "liked": liked, "ok": True, "msg": "",
                })
            except Exception as e:
                self._emit("album_like_result", {
                    "id": album_id, "liked": not liked, "ok": False, "msg": str(e),
                })
                self._log(f"✗ Не удалось изменить лайк альбома: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def toggle_like(self, track_id: str, liked: bool) -> None:
        """Результат → py:like_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("like_result", {
                    "track_id": track_id, "liked": not liked, "ok": False, "msg": "Нет авторизации",
                })
                return
            try:
                self._ym.set_track_liked(track_id, liked)
                self._emit("like_result", {
                    "track_id": track_id, "liked": liked, "ok": True, "msg": "",
                })
            except Exception as e:
                self._emit("like_result", {
                    "track_id": track_id, "liked": not liked, "ok": False, "msg": str(e),
                })
                self._log(f"✗ Не удалось изменить лайк: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    # ── Текст песни ──────────────────────────────────────────────────────────

    def get_lyrics(self, track_id: str) -> None:
        """Результат → py:lyrics_result."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("lyrics_result", {"track_id": track_id, "text": None})
                return
            try:
                text = self._ym.get_lyrics(track_id)
                self._emit("lyrics_result", {"track_id": track_id, "text": text})
            except Exception as e:
                self._log(f"Ошибка загрузки текста песни: {e}", "err")
                self._emit("lyrics_result", {"track_id": track_id, "text": None})

        threading.Thread(target=_worker, daemon=True).start()

    # ── Скачивание ────────────────────────────────────────────────────────

    def start_download(self, tracks: list[dict]) -> bool:
        """Запускает параллельное скачивание. Не ждёт завершения."""
        if not tracks:
            return False
        self._dl.submit(tracks, self._cfg)
        return True

    def cancel_downloads(self) -> None:
        self._dl.cancel_all()

    # ── Превью трека ──────────────────────────────────────────────────────

    def get_preview_url(self, track_id: str) -> None:
        """Результат → py:preview_url или py:preview_error."""
        def _worker():
            try:
                url = self._ym.get_preview_url(track_id)
                self._emit("preview_url", {"track_id": track_id, "url": url})
            except Exception as e:
                self._emit("preview_error", {"track_id": track_id, "msg": str(e)})
                self._log(f"Ошибка превью: {e}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def prefetch_track(self, track_id: str) -> None:
        """
        Готовит ссылку на следующий трек заранее → py:track_prefetched.
        Получение прямой ссылки занимает около секунды — без этого пауза была
        бы слышна на каждом переключении.
        """
        def _worker():
            try:
                url = self._ym.get_preview_url(track_id)
                self._emit("track_prefetched", {"track_id": track_id, "url": url})
            except Exception:
                # Не вышло — трек просто загрузится обычным путём, молча
                self._emit("track_prefetched", {"track_id": track_id, "url": ""})

        threading.Thread(target=_worker, daemon=True).start()

    # ── Скачанные треки ───────────────────────────────────────────────────

    def scan_downloaded(self) -> None:
        """
        Сканирует папку загрузки и возвращает список аудио-файлов
        → py:downloaded_files.
        rel_path используется для /audio/<rel_path> на локальном сервере.
        """
        def _worker():
            base_str = self._cfg.get("download_dir", "") or "."
            base = Path(base_str).resolve()
            exts = {".mp3", ".flac", ".aac", ".m4a", ".ogg", ".opus"}
            files = []
            if base.exists():
                for f in sorted(base.rglob("*")):
                    if f.suffix.lower() in exts:
                        try:
                            rel = f.relative_to(base).as_posix()
                        except ValueError:
                            rel = f.name
                        meta = read_audio_meta(f)
                        cover = (
                            f"http://127.0.0.1:5000/cover/{quote(rel, safe='/')}"
                            if meta["has_cover"] else ""
                        )
                        files.append({
                            "id": rel,
                            "path": str(f),
                            "rel_path": rel,
                            "name": f.stem,
                            "title": meta["title"] or f.stem,
                            "artist": meta["artist"],
                            "album": meta["album"],
                            "cover_uri": cover,
                            "duration": fmt_duration(meta["duration_ms"] or None),
                            "duration_ms": meta["duration_ms"],
                            "ext": f.suffix.lstrip(".").upper(),
                            "size": f.stat().st_size,
                            "track_id": read_ym_track_id(f),
                        })
            files, ids = self._merge_dl_index(files)
            self._emit("downloaded_files", files)
            self._emit("downloaded_ids", ids)

        threading.Thread(target=_worker, daemon=True).start()

    def get_file_url(self, rel_path: str) -> str:
        """Возвращает http://... URL для воспроизведения через локальный сервер."""
        return f"http://127.0.0.1:5000/audio/{rel_path}"

    def delete_downloaded(self, rel_path: str) -> None:
        """Удаляет скачанный файл с диска → py:downloaded_deleted."""
        def _worker():
            ok, msg = self._delete_one(rel_path)
            self._emit("downloaded_deleted", {"rel_path": rel_path, "ok": ok, "msg": msg})
            if ok:
                self._log(f"🗑 Файл удалён: {Path(rel_path).name}", "ok")
            else:
                self._log(f"✗ Не удалось удалить файл: {msg}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def delete_downloaded_many(self, rel_paths: list) -> None:
        """Массовое удаление скачанных файлов → py:downloaded_deleted_many."""
        def _worker():
            deleted, failed = [], []
            for rel_path in (rel_paths or []):
                ok, msg = self._delete_one(str(rel_path))
                (deleted if ok else failed).append(
                    rel_path if ok else {"rel_path": rel_path, "msg": msg}
                )
            self._emit("downloaded_deleted_many", {"deleted": deleted, "failed": failed})
            if deleted:
                self._log(f"🗑 Удалено файлов: {len(deleted)}", "ok")
            for f in failed:
                self._log(f"✗ Не удалось удалить {Path(f['rel_path']).name}: {f['msg']}", "err")

        threading.Thread(target=_worker, daemon=True).start()

    def _delete_one(self, rel_path: str) -> tuple[bool, str]:
        """Удаляет один файл внутри папки загрузок. Возвращает (успех, сообщение)."""
        base = Path(self._cfg.get("download_dir", "") or ".").resolve()
        try:
            target = (base / rel_path).resolve()
            # rel_path приходит из UI — не даём выйти за пределы папки загрузок
            target.relative_to(base)
        except Exception:
            return False, "Недопустимый путь"

        try:
            if not target.is_file():
                raise FileNotFoundError("Файл не найден")
            self._unlink_with_retry(target)
            self._remove_empty_dirs(target.parent, base)
            self._forget_download_path(rel_path)
            return True, ""
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _unlink_with_retry(target: Path, attempts: int = 8, delay: float = 0.15) -> None:
        """
        Windows не даёт удалить файл, пока его кто-то читает. Плеер уже получил
        команду переключиться, но поток закрывается не мгновенно — ждём его.
        """
        for i in range(attempts):
            try:
                target.unlink()
                return
            except PermissionError:
                if i == attempts - 1:
                    raise
                time.sleep(delay)

    @staticmethod
    def _remove_empty_dirs(folder: Path, base: Path) -> None:
        """Подчищает опустевшие подпапки альбомов/артистов внутри папки загрузок."""
        try:
            while folder != base and base in folder.parents:
                if any(folder.iterdir()):
                    break
                folder.rmdir()
                folder = folder.parent
        except Exception:
            pass

    # ── Индекс скачанных (track_id ↔ файл) ───────────────────────────────

    def _dl_index_path(self) -> Path:
        base = Path(self._cfg.get("download_dir", "") or ".").resolve()
        return base / ".yamd_index.json"

    def _load_dl_index(self) -> dict:
        path = self._dl_index_path()
        if not path.is_file():
            return {}
        try:
            data = json.loads(path.read_text("utf-8"))
        except Exception:
            return {}
        if not isinstance(data, dict):
            return {}
        # старый формат {id: rel_path}
        out = {}
        for tid, val in data.items():
            tid = str(tid)
            if isinstance(val, str):
                out[tid] = {"rel_path": val, "title": "", "artist": ""}
            elif isinstance(val, dict):
                out[tid] = {
                    "rel_path": str(val.get("rel_path") or ""),
                    "title": str(val.get("title") or ""),
                    "artist": str(val.get("artist") or ""),
                }
        return out

    def _save_dl_index(self, index: dict) -> None:
        path = self._dl_index_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(index, ensure_ascii=False, indent=2), "utf-8")
        except Exception:
            pass

    @staticmethod
    def _dl_key(artist: str, title: str) -> str:
        def norm(s: str) -> str:
            s = (s or "").lower().replace("ё", "е")
            return " ".join("".join(ch if ch.isalnum() else " " for ch in s).split())
        t = norm(title)
        return f"{norm(artist)}\t{t}" if t else ""

    def _merge_dl_index(self, files: list[dict]) -> tuple[list[dict], list[str]]:
        """Сверяет индекс с файлами на диске и проставляет track_id."""
        with self._dl_index_lock:
            index = self._load_dl_index()
            by_path = {f["rel_path"]: f for f in files}
            by_key = {}
            for f in files:
                key = self._dl_key(f.get("artist") or "", f.get("title") or "")
                if key:
                    by_key[key] = f

            for tid in list(index.keys()):
                info = index[tid]
                rel = info.get("rel_path") or ""
                if rel and rel not in by_path:
                    del index[tid]
                    continue
                if rel and rel in by_path and not by_path[rel].get("track_id"):
                    by_path[rel]["track_id"] = tid
                elif not rel:
                    key = self._dl_key(info.get("artist") or "", info.get("title") or "")
                    hit = by_key.get(key)
                    if hit:
                        info["rel_path"] = hit["rel_path"]
                        if not hit.get("track_id"):
                            hit["track_id"] = tid

            for f in files:
                tid = str(f.get("track_id") or "")
                if tid:
                    index[tid] = {
                        "rel_path": f["rel_path"],
                        "title": f.get("title") or "",
                        "artist": f.get("artist") or "",
                    }
            self._save_dl_index(index)
        return files, [str(k) for k in index.keys()]

    def remember_download(self, track_id: str, title: str = "", artist: str = "") -> None:
        """Запоминает, что трек скачан — чтобы пометить его в плейлистах."""
        tid = str(track_id or "")
        if not tid:
            return
        with self._dl_index_lock:
            index = self._load_dl_index()
            prev = index.get(tid) or {}
            index[tid] = {
                "rel_path": prev.get("rel_path") or "",
                "title": title or prev.get("title") or "",
                "artist": artist or prev.get("artist") or "",
            }
            self._save_dl_index(index)

    def _forget_download_path(self, rel_path: str) -> None:
        with self._dl_index_lock:
            index = self._load_dl_index()
            changed = False
            for tid in list(index.keys()):
                if (index[tid].get("rel_path") or "") == rel_path:
                    del index[tid]
                    changed = True
            if changed:
                self._save_dl_index(index)

    # ── Папка загрузок ───────────────────────────────────────────────────

    def open_download_folder(self) -> None:
        """Открывает папку загрузки в проводнике ОС."""
        folder = self._cfg.get("download_dir") or "."
        folder_path = os.path.realpath(folder)

        if not os.path.exists(folder_path):
            self._log(f"Папка не существует: {folder_path}", "err")
            return

        # Для Windows
        if platform.system() == "Windows":
            os.startfile(folder_path)
        # Для macOS
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", folder_path])
        # Для Linux
        else:
            subprocess.Popen(["xdg-open", folder_path])

    # ── Системные диалоги ─────────────────────────────────────────────────

    def choose_folder(self) -> Optional[str]:
        result = self._window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            return result[0]
        return None

    def open_link(self, url: str) -> None:
        import webbrowser
        webbrowser.open(url)
