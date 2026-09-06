"""
Менеджер параллельного скачивания через yandex-music-downloader.
Каждый трек скачивается в отдельном потоке (до MAX_PARALLEL одновременно).
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable


def _find_cli() -> str:
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent

    for name in ('yandex-music-downloader.exe', 'yandex-music-downloader'):
        local = base / name
        if local.is_file():
            return str(local)

    return 'yandex-music-downloader'


_CLI = _find_cli()

MAX_PARALLEL = 4


class DownloadManager:
    """
    Управляет очередью скачивания.
    Колбэки вызываются из рабочих потоков → нужно emit через pywebview.
    """

    def __init__(
        self,
        on_status: Callable[[str, str], None],   # (track_id, status)
        on_log: Callable[[str, str], None],       # (msg, kind)
    ) -> None:
        self._on_status = on_status
        self._on_log = on_log
        self._parallel = MAX_PARALLEL
        self._executor = ThreadPoolExecutor(max_workers=MAX_PARALLEL, thread_name_prefix="dl")
        self._futures: dict[str, Future] = {}
        self._lock = threading.Lock()

    # ── Публичный API ──────────────────────────────────────────────────────

    def submit(self, tracks: list[dict], cfg: dict) -> None:
        """Ставит треки в очередь. Возвращает сразу."""
        self._apply_parallel(cfg)
        for track in tracks:
            tid = track["id"]
            with self._lock:
                # Не дублируем уже активные загрузки
                f = self._futures.get(tid)
                if f and not f.done():
                    continue
                fut = self._executor.submit(self._download_one, track, cfg)
                self._futures[tid] = fut

    def cancel_all(self) -> None:
        """Отменяет ещё не начатые задачи (начатые не прерываем — subprocess)."""
        with self._lock:
            for tid, f in list(self._futures.items()):
                if not f.running():
                    f.cancel()

    def is_busy(self) -> bool:
        with self._lock:
            return any(not f.done() for f in self._futures.values())

    # ── Внутренние методы ─────────────────────────────────────────────────

    def _apply_parallel(self, cfg: dict) -> None:
        """
        Подхватывает настройку «Параллельных загрузок» из конфига.
        Пул нельзя менять на лету, поэтому пересоздаём его только когда
        очередь пуста — иначе настройка применится к следующей пачке.
        """
        try:
            want = max(1, min(16, int(cfg.get("parallel", MAX_PARALLEL))))
        except (TypeError, ValueError):
            return

        with self._lock:
            if want == self._parallel:
                return
            if any(not f.done() for f in self._futures.values()):
                return
            old = self._executor
            self._executor = ThreadPoolExecutor(max_workers=want, thread_name_prefix="dl")
            self._parallel = want
            self._futures.clear()
        old.shutdown(wait=False)

    def _download_one(self, track: dict, cfg: dict) -> None:
        tid = track["id"]
        self._on_status(tid, "downloading")
        self._on_log(f"⬇ {track['artist']} — {track['title']}", "info")

        cmd = self._build_cmd(track, cfg)
        try:
            subprocess.run(
                cmd,
                check=True,
                text=True,
                timeout=600,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=0x08000000,
                env={**os.environ, "PYTHONUTF8": "1"},
                cwd=cfg.get("download_dir") or str(Path.home())
            )
            self._on_status(tid, "done")
            self._on_log(f"✓ {track['title']}", "ok")
        except subprocess.CalledProcessError as e:
            self._on_status(tid, "error")
            err = (e.stderr or "").strip().splitlines()
            self._on_log(f"✗ {track['title']}: {err[-1] if err else 'ошибка'}", "err")
        except subprocess.TimeoutExpired:
            self._on_status(tid, "error")
            self._on_log(f"✗ Таймаут: {track['title']}", "err")
        except FileNotFoundError:
            self._on_status(tid, "error")
            self._on_log("✗ yandex-music-downloader не найден.\nПоложите его рядом с программой или добавьте в PATH", "err")

    @staticmethod
    def _build_cmd(track: dict, cfg: dict) -> list[str]:
        url = track["source_url"]
        cmd = [_CLI, "--token", cfg["token"]]

        # Целевой трек
        if track.get("id") and "/track/" not in url:
            cmd += ["--track-id", str(track["id"])]
        else:
            cmd += ["-u", url]

        # Аудио
        cmd += ["--quality", cfg.get("quality", "2")]
        if cfg.get("embed_cover"):
            cmd.append("--embed-cover")
        cmd += ["--cover-resolution", cfg.get("cover_resolution", "original")]
        lyrics = cfg.get("lyrics_format", "none")
        if lyrics and lyrics != "none":
            cmd += ["--lyrics-format", lyrics]

        # Файлы
        if cfg.get("skip_existing"):
            cmd.append("--skip-existing")
        if cfg.get("path_pattern"):
            cmd += ["--path-pattern", cfg["path_pattern"]]
        if cfg.get("download_dir"):
            cmd += ["--dir", cfg["download_dir"]]

        # Сеть
        for flag, key in [("--delay", "delay"), ("--timeout", "timeout"),
                          ("--tries", "tries"), ("--retry-delay", "retry_delay")]:
            val = cfg.get(key, "")
            if val and not (key == "delay" and val == "0"):
                cmd += [flag, str(val)]

        # Фильтры
        compat = cfg.get("compatibility_level", "1")
        if compat:
            cmd += ["--compatibility-level", compat]
        if cfg.get("stick_to_artist"):
            cmd.append("--stick-to-artist")
        if cfg.get("only_music"):
            cmd.append("--only-music")

        return cmd
