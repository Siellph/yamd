"""
Менеджер параллельного скачивания через yandex-music-downloader.
Каждый трек скачивается в отдельном потоке (до MAX_PARALLEL одновременно).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Optional

import config as cfg_module
from ym_client import parse_lrc


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

# Символы, из-за которых Windows/загрузчик ломают путь: «Cha Cha Cha / …»
_UNSAFE_PATH = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WIN_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def _safe_part(text, fallback: str = "track") -> str:
    s = _UNSAFE_PATH.sub(" ", str(text or ""))
    s = re.sub(r"\s+", " ", s).strip(" .")
    stem = s.split(".")[0].upper() if s else ""
    if not s or stem in _WIN_RESERVED:
        s = str(fallback or "track")
    return s[:180]


def _has_unsafe_names(track: dict) -> bool:
    for key in ("title", "artist", "album"):
        if _UNSAFE_PATH.search(str(track.get(key) or "")):
            return True
    return False


def lyrics_download_enabled(cfg: dict) -> bool:
    """Чекбокс «Скачивать текст песен» или старый lyrics_format ≠ none."""
    if "download_lyrics" in cfg:
        return bool(cfg.get("download_lyrics"))
    fmt = str(cfg.get("lyrics_format") or "none").lower()
    return fmt not in ("", "none")


def _safe_lyrics_id(track_id: str) -> str:
    """Имя файла по id трека Яндекса: без пути, без шаблона аудио."""
    s = str(track_id or "").strip().replace(":", "_")
    s = re.sub(r"[^\w.\-]", "", s)
    if not s or s in {".", ".."} or len(s) > 80:
        return ""
    return s


def lyrics_paths_for_track(track_id: str) -> tuple[Path, Path]:
    """<user_data>/lyrics/lrc/<id>.lrc и .../txt/<id>.txt."""
    safe = _safe_lyrics_id(track_id)
    root = cfg_module.lyrics_dir()
    return root / "lrc" / f"{safe}.lrc", root / "txt" / f"{safe}.txt"


def _iter_lyrics_files(kind: str, track_id: str):
    """Точный <id>.ext и варианты <id> - *.ext внутри lyrics/<kind>/."""
    safe = _safe_lyrics_id(track_id)
    if not safe or kind not in ("lrc", "txt"):
        return
    folder = cfg_module.lyrics_dir() / kind
    ext = f".{kind}"
    exact = folder / f"{safe}{ext}"
    seen: set[Path] = set()
    if exact.is_file():
        seen.add(exact)
        yield exact
    if not folder.is_dir():
        return
    prefix = f"{safe} - "
    try:
        for path in folder.iterdir():
            if path in seen or not path.is_file():
                continue
            if path.suffix.lower() != ext:
                continue
            stem = path.stem
            if stem == safe or stem.startswith(prefix):
                yield path
    except Exception:
        return


def find_lyrics_file(kind: str, track_id: str) -> Path | None:
    for path in _iter_lyrics_files(kind, track_id):
        return path
    return None


def lyrics_files_exist(track_id: str) -> bool:
    return bool(find_lyrics_file("lrc", track_id) or find_lyrics_file("txt", track_id))


def read_local_lyrics(track_id: str) -> dict:
    """
    Читает локальный текст по id трека Яндекса.
    Предпочитает LRC (синхрон), иначе TXT. Без сети.
    """
    lrc_path = find_lyrics_file("lrc", track_id)
    if lrc_path and lrc_path.is_file():
        try:
            raw = lrc_path.read_text(encoding="utf-8")
        except Exception:
            raw = ""
        sync = parse_lrc(raw)
        if sync:
            return {"text": "\n".join(x["text"] for x in sync), "sync": sync}
        if raw.strip():
            return {"text": raw, "sync": None}
    txt_path = find_lyrics_file("txt", track_id)
    if txt_path and txt_path.is_file():
        try:
            raw = txt_path.read_text(encoding="utf-8")
        except Exception:
            raw = ""
        if raw.strip():
            return {"text": raw, "sync": None}
    return {"text": None, "sync": None}


def delete_lyrics_for_track(track_id: str) -> None:
    """Удаляет lrc/txt этого id, включая варианты «id - название»."""
    if not _safe_lyrics_id(track_id):
        return
    try:
        root = cfg_module.lyrics_dir().resolve()
    except Exception:
        return
    for kind in ("lrc", "txt"):
        for path in _iter_lyrics_files(kind, track_id):
            try:
                resolved = path.resolve()
                resolved.relative_to(root)
                if resolved.is_file():
                    resolved.unlink()
            except Exception:
                pass


def write_lyrics_files(track_id: str, files: dict) -> list[str]:
    """
    Пишет LRC и/или TXT в данные приложения, ключ — id трека.
    Если есть только LRC — дополнительно сохраняет текст без таймкодов.
    Возвращает список записанных расширений.
    """
    if not _safe_lyrics_id(track_id):
        return []
    lrc_raw = (files or {}).get("lrc") or None
    text_raw = (files or {}).get("text") or None
    if not lrc_raw and not text_raw:
        return []
    lrc_path, txt_path = lyrics_paths_for_track(track_id)
    written: list[str] = []
    if lrc_raw:
        lrc_path.parent.mkdir(parents=True, exist_ok=True)
        lrc_path.write_text(lrc_raw, encoding="utf-8")
        written.append("lrc")
        if not text_raw:
            sync = parse_lrc(lrc_raw)
            if sync:
                text_raw = "\n".join(x["text"] for x in sync)
    if text_raw:
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(text_raw, encoding="utf-8")
        written.append("txt")
    return written


def dest_path_for_track(track: dict, cfg: dict) -> Path:
    """Путь файла по шаблону, каждый сегмент без запрещённых символов."""
    base = Path(cfg.get("download_dir") or ".")
    pattern = cfg.get("path_pattern") or "#album-artist - #title"
    mapping = {
        "#number-padded": str(track.get("num") or 0).zfill(2),
        "#number": str(track.get("num") or ""),
        "#track-artist": _safe_part(track.get("artist"), "Unknown"),
        "#album-artist": _safe_part(track.get("artist"), "Unknown"),
        "#track-id": _safe_part(track.get("id"), "id"),
        "#album-id": _safe_part(track.get("album_id"), "album"),
        "#title": _safe_part(track.get("title"), str(track.get("id") or "track")),
        "#album": _safe_part(track.get("album"), "Unknown"),
        "#year": _safe_part(track.get("year") or "", ""),
    }
    out = pattern
    for key in sorted(mapping, key=len, reverse=True):
        out = out.replace(key, mapping[key])
    parts = [_safe_part(p, "x") for p in re.split(r"[\\/]+", out) if p.strip()]
    dest = base.joinpath(*parts) if parts else base / _safe_part(track.get("id"), "track")
    if dest.suffix.lower() not in {".mp3", ".flac", ".m4a", ".aac", ".ogg", ".opus"}:
        dest = dest.with_suffix(".mp3")
    return dest


def _cli_error_text(stderr: str) -> str:
    lines = [ln.strip() for ln in (stderr or "").splitlines() if ln.strip()]
    if not lines:
        return "ошибка загрузчика"
    useful = [ln for ln in lines if "PYI-" not in ln and "Failed to execute script" not in ln]
    return (useful[-1] if useful else lines[-1])[:300]


class DownloadManager:
    """
    Управляет очередью скачивания.
    Колбэки вызываются из рабочих потоков → нужно emit через pywebview.
    """

    def __init__(
        self,
        on_status: Callable[[str, str], None],   # (track_id, status)
        on_log: Callable[[str, str], None],       # (msg, kind)
        native_download: Optional[Callable] = None,
        fetch_lyrics: Optional[Callable] = None,
    ) -> None:
        self._on_status = on_status
        self._on_log = on_log
        self._native_download = native_download
        self._fetch_lyrics = fetch_lyrics
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

        dest = dest_path_for_track(track, cfg)
        if cfg.get("skip_existing") and dest.is_file() and dest.stat().st_size > 0:
            self._maybe_save_lyrics(track, dest, cfg)
            self._on_status(tid, "done")
            self._on_log(f"✓ Уже скачан: {track['title']}", "ok")
            return

        # Названия со слэшем и «запрещёнными» символами CLI часто роняет
        # целиком (PYI Failed to execute script). Качаем сами.
        if self._native_download and _has_unsafe_names(track):
            if self._download_native(track, dest, cfg):
                return
            self._on_status(tid, "error")
            return

        cli_err = self._run_cli(track, cfg)
        if cli_err is None:
            self._maybe_save_lyrics(track, dest, cfg)
            self._on_status(tid, "done")
            self._on_log(f"✓ {track['title']}", "ok")
            return

        if self._native_download and self._download_native(track, dest, cfg, after_cli=True):
            return

        self._on_status(tid, "error")
        self._on_log(f"✗ {track['title']}: {cli_err}", "err")

    def _maybe_save_lyrics(self, track: dict, dest: Path, cfg: dict) -> None:
        """После аудио — LRC/TXT в данные приложения по id трека."""
        if not lyrics_download_enabled(cfg) or not self._fetch_lyrics:
            return
        tid = str(track.get("id") or "")
        if not tid or lyrics_files_exist(tid):
            return
        try:
            files = self._fetch_lyrics(tid, cfg) or {}
            written = write_lyrics_files(tid, files)
            if written:
                title = track.get("title") or dest.stem
                self._on_log(f"📝 Текст: {title} ({', '.join(written)})", "ok")
        except Exception as e:
            self._on_log(f"Текст песни «{track.get('title') or dest.stem}»: {e}", "err")

    def _download_native(self, track: dict, dest: Path, cfg: dict, after_cli: bool = False) -> bool:
        if not self._native_download:
            return False
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            self._native_download(str(track["id"]), dest, cfg)
            self._maybe_save_lyrics(track, dest, cfg)
            self._on_status(track["id"], "done")
            prefix = "✓ скачан напрямую" if after_cli else "✓"
            self._on_log(f"{prefix} {track['title']}", "ok")
            return True
        except Exception as e:
            self._on_log(f"✗ Прямое скачивание «{track['title']}»: {e}", "err")
            return False

    def _run_cli(self, track: dict, cfg: dict) -> Optional[str]:
        """None — успех, иначе текст ошибки."""
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
            return None
        except subprocess.CalledProcessError as e:
            return _cli_error_text(e.stderr or "")
        except subprocess.TimeoutExpired:
            return "таймаут"
        except FileNotFoundError:
            return "yandex-music-downloader не найден. Положите его рядом с программой или добавьте в PATH"

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
        # Текст песен пишем сами в данные приложения по id трека — CLI не трогаем.

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
