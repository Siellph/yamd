"""
JS-API: все методы, доступные из JavaScript через window.pywebview.api.*
Тонкий слой — только маршрутизация, никакой бизнес-логики.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Optional
import os
import platform
import subprocess
import webview

import config as cfg_module
from downloader import DownloadManager
from ym_client import YMClient


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

    def search_tracks(self, query: str) -> None:
        """Результат → py:search_results."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("search_results", [])
                self._log("Нет авторизации для поиска", "err")
                return
            try:
                results = self._ym.search_tracks(query)
                self._emit("search_results", results)
            except Exception as e:
                self._log(f"Ошибка поиска: {e}", "err")
                self._emit("search_results", [])

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

    # ── Моя волна ─────────────────────────────────────────────────────────

    def start_wave(self) -> None:
        """Запускает «Мою волну» с начала. Результат → py:wave_tracks."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("wave_tracks", {"tracks": [], "seen": [], "append": False})
                self._log("Нет авторизации для запуска волны", "err")
                return
            try:
                tracks, seen = self._ym.get_wave_tracks(target=10, start_num=1)
                self._emit("wave_tracks", {"tracks": tracks, "seen": seen, "append": False})
                self._log(f"🌊 Волна запущена: {len(tracks)} трек(ов)", "ok")
            except Exception as e:
                self._log(f"Ошибка запуска волны: {e}", "err")
                self._emit("wave_tracks", {"tracks": [], "seen": [], "append": False})

        threading.Thread(target=_worker, daemon=True).start()

    def wave_next(self, seen_ids: list[str], start_num: int = 1) -> None:
        """Подгружает следующую порцию треков волны. Результат → py:wave_tracks (append)."""
        def _worker():
            token = self._cfg.get("token", "").strip()
            if not token or not self._ym.ensure(token):
                self._emit("wave_tracks", {"tracks": [], "seen": seen_ids or [], "append": True})
                return
            try:
                tracks, seen = self._ym.get_wave_tracks(
                    seen_ids=seen_ids, target=15, start_num=start_num
                )
                self._emit("wave_tracks", {"tracks": tracks, "seen": seen, "append": True})
                if tracks:
                    self._log(f"🌊 Добавлено {len(tracks)} новых трек(ов)", "ok")
                else:
                    self._log("🌊 Волна больше не выдаёт новых треков", "err")
            except Exception as e:
                self._log(f"Ошибка загрузки волны: {e}", "err")
                self._emit("wave_tracks", {"tracks": [], "seen": seen_ids or [], "append": True})

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
                        files.append({
                            "path": str(f),
                            "rel_path": rel,
                            "name": f.stem,
                            "ext": f.suffix.lstrip(".").upper(),
                            "size": f.stat().st_size,
                        })
            self._emit("downloaded_files", files)

        threading.Thread(target=_worker, daemon=True).start()

    def get_file_url(self, rel_path: str) -> str:
        """Возвращает http://... URL для воспроизведения через локальный сервер."""
        return f"http://127.0.0.1:5000/audio/{rel_path}"

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
