"""
Конфигурация приложения — загрузка/сохранение config.json.
Последний трек плеера живёт отдельно в last_play.json, чтобы не раздувать конфиг.
"""
import json
import os
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"
LAST_PLAY_FILE = Path(__file__).parent / "last_play.json"


def get_base_dir() -> Path:
    """
    База приложения:
    - PyInstaller → папка рядом с exe
    - dev → папка проекта
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def get_user_data_dir() -> Path:
    """
    Писаемые пользовательские данные (не музыка, не {app}/_internal):
    - собранное приложение → %LOCALAPPDATA%\\YaMD
    - разработка → папка проекта, рядом с config.json
    """
    if getattr(sys, "frozen", False):
        local = os.environ.get("LOCALAPPDATA")
        if local:
            path = Path(local) / "YaMD"
        else:
            path = Path.home() / "AppData" / "Local" / "YaMD"
        path.mkdir(parents=True, exist_ok=True)
        return path
    return Path(__file__).resolve().parent


def lyrics_dir() -> Path:
    path = get_user_data_dir() / "lyrics"
    path.mkdir(parents=True, exist_ok=True)
    return path


DEFAULT_DOWNLOAD_DIR = get_base_dir() / "downloads"


DEFAULT_CONFIG: dict = {
    "token": "",
    "quality": "2",
    "path_pattern": r"#album-artist - #title",
    "cover_resolution": "original",
    "skip_existing": True,
    "embed_cover": True,
    "lyrics_format": "none",
    "download_lyrics": False,
    "delay": "0",
    "compatibility_level": "1",
    "timeout": "20",
    "tries": "20",
    "retry_delay": "5",
    "stick_to_artist": False,
    "only_music": False,
    "download_dir": str(DEFAULT_DOWNLOAD_DIR),
    "ui_theme": "amber",
    "ui_mode": "dark",
    "crossfade_sec": "0",
}


def load() -> dict:
    cfg = DEFAULT_CONFIG.copy()
    migrated = None

    if CONFIG_FILE.exists():
        try:
            saved = json.loads(CONFIG_FILE.read_text("utf-8"))
            migrated = saved.pop("last_play", None)
            had_download_lyrics = "download_lyrics" in saved
            cfg.update(saved)
            if not had_download_lyrics:
                fmt = str(cfg.get("lyrics_format") or "none").lower()
                cfg["download_lyrics"] = fmt not in ("", "none")
        except Exception:
            pass

    download_dir = Path(cfg["download_dir"])
    download_dir.mkdir(parents=True, exist_ok=True)

    if migrated:
        if not LAST_PLAY_FILE.exists():
            save_last_play(migrated)
        save(cfg)

    return cfg


def save(cfg: dict) -> None:
    out = {k: v for k, v in cfg.items() if k != "last_play"}
    CONFIG_FILE.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        "utf-8"
    )


def load_last_play():
    if not LAST_PLAY_FILE.exists():
        return None
    try:
        data = json.loads(LAST_PLAY_FILE.read_text("utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    data.pop("queue", None)
    data.pop("waveSeenIds", None)
    return data


def save_last_play(data) -> None:
    if not data:
        try:
            LAST_PLAY_FILE.unlink(missing_ok=True)
        except TypeError:
            if LAST_PLAY_FILE.exists():
                LAST_PLAY_FILE.unlink()
        except Exception:
            pass
        return
    LAST_PLAY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        "utf-8",
    )
