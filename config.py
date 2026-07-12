"""
Конфигурация приложения — загрузка/сохранение config.json.
"""
import json
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"


def get_base_dir() -> Path:
    """
    База приложения:
    - PyInstaller → папка рядом с exe
    - dev → папка проекта
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent


DEFAULT_DOWNLOAD_DIR = get_base_dir() / "downloads"


DEFAULT_CONFIG: dict = {
    "token": "",
    "quality": "2",
    "path_pattern": r"#album-artist - #title",
    "cover_resolution": "original",
    "skip_existing": True,
    "embed_cover": True,
    "lyrics_format": "none",
    "delay": "0",
    "compatibility_level": "1",
    "timeout": "20",
    "tries": "20",
    "retry_delay": "5",
    "stick_to_artist": False,
    "only_music": False,
    "download_dir": str(DEFAULT_DOWNLOAD_DIR),
}


def load() -> dict:
    cfg = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            saved = json.loads(CONFIG_FILE.read_text("utf-8"))
            cfg.update(saved)
        except Exception:
            pass

    download_dir = Path(cfg["download_dir"])
    download_dir.mkdir(parents=True, exist_ok=True)

    return cfg


def save(cfg: dict) -> None:
    CONFIG_FILE.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2),
        "utf-8"
    )
