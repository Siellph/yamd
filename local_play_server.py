"""
Локальный HTTP-сервер для воспроизведения аудиофайлов.
pywebview блокирует file://, поэтому отдаём файлы через 127.0.0.1:5000.

Маршруты:
  GET /              — главная страница (HTML-интерфейс)
  GET /audio/<path>  — файл по относительному пути от download_dir
  GET /find/<name>   — поиск файла по имени рекурсивно
"""
from __future__ import annotations

import re
from pathlib import Path

from flask import Flask, Response, send_file, send_from_directory

import config as cfg_module
from gui.html import HTML

app = Flask(__name__)

_SIDECARS = ("cover.jpg", "cover.jpeg", "cover.png", "folder.jpg", "album.jpg", "AlbumArt.jpg")
_YM_TRACK_URL = re.compile(r"(?:music\.yandex\.[a-z.]+/.+?)?/?track/(\d+)", re.I)
_YM_TRACK_ID = re.compile(r"^\d{3,}$")


def read_ym_track_id(path: Path) -> str:
    """Yandex track id из тегов, если загрузчик его туда положил."""
    try:
        from mutagen import File
        audio = File(path)
        easy = File(path, easy=True)
        if easy is not None:
            for key in ("website", "comment", "description"):
                for val in easy.get(key) or []:
                    found = _ym_id_from_text(str(val))
                    if found:
                        return found
        tags = getattr(audio, "tags", None) if audio is not None else None
        if not tags:
            return ""
        keys = list(tags.keys()) if hasattr(tags, "keys") else []
        for key in keys:
            frame = tags[key]
            text = _tag_text(frame)
            found = _ym_id_from_text(text)
            if found:
                return found
            desc = str(
                getattr(frame, "desc", "") or getattr(frame, "description", "") or key
            ).lower()
            raw = text.strip()
            if _YM_TRACK_ID.match(raw) and any(x in desc for x in ("yandex", "track", "ym")):
                return raw
    except Exception:
        return ""
    return ""


def _tag_text(frame) -> str:
    if frame is None:
        return ""
    if hasattr(frame, "url") and frame.url:
        return str(frame.url)
    text = getattr(frame, "text", None)
    if text is not None:
        if isinstance(text, (list, tuple)):
            return " ".join(str(x) for x in text)
        return str(text)
    data = getattr(frame, "data", None)
    if data:
        try:
            return bytes(data).decode("utf-8", "ignore")
        except Exception:
            return ""
    if isinstance(frame, (list, tuple)):
        return " ".join(str(x) for x in frame)
    return str(frame)


def _ym_id_from_text(text: str) -> str:
    if not text:
        return ""
    m = _YM_TRACK_URL.search(text)
    if m:
        return m.group(1)
    return ""


def _first_tag(easy, *keys) -> str:
    if not easy:
        return ""
    for key in keys:
        vals = easy.get(key)
        if vals:
            return str(vals[0]).strip()
    return ""


def read_audio_meta(path: Path) -> dict:
    """Название / исполнитель / альбом / есть ли картинка — из тегов или рядом лежащей обложки."""
    title, artist, album = path.stem, "", ""
    duration_ms = 0
    has_cover = _sidecar_cover(path) is not None
    try:
        from mutagen import File
        audio = File(path)
        easy = File(path, easy=True)
        if easy is not None:
            title = _first_tag(easy, "title") or title
            artist = _first_tag(easy, "artist", "albumartist")
            album = _first_tag(easy, "album")
        if audio is not None and getattr(audio.info, "length", None):
            duration_ms = int(audio.info.length * 1000)
        if not has_cover:
            has_cover = _embedded_art(audio) is not None
    except Exception:
        pass
    return {
        "title": title,
        "artist": artist,
        "album": album,
        "duration_ms": duration_ms,
        "has_cover": has_cover,
    }


def _sidecar_cover(path: Path) -> Path | None:
    folder = path.parent
    for name in _SIDECARS:
        cand = folder / name
        if cand.is_file():
            return cand
    return None


def _embedded_art(audio) -> tuple[bytes, str] | None:
    if audio is None:
        return None
    pics = getattr(audio, "pictures", None)
    if pics:
        p = pics[0]
        return bytes(p.data), (p.mime or "image/jpeg")
    tags = getattr(audio, "tags", None)
    if not tags:
        return None
    # MP3 / ID3
    for key in list(getattr(tags, "keys", lambda: [])()):
        if str(key).startswith("APIC"):
            pic = tags[key]
            data = getattr(pic, "data", None)
            if data:
                return bytes(data), getattr(pic, "mime", None) or "image/jpeg"
    # M4A
    covr = tags.get("covr") if hasattr(tags, "get") else None
    if covr:
        pic = covr[0]
        fmt = getattr(pic, "imageformat", None)
        mime = "image/png" if fmt == 14 else "image/jpeg"
        return bytes(pic), mime
    return None


def cover_bytes(path: Path) -> tuple[bytes, str] | None:
    side = _sidecar_cover(path)
    if side:
        suffix = side.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        return side.read_bytes(), mime
    try:
        from mutagen import File
        return _embedded_art(File(path))
    except Exception:
        return None


def _add_cors(resp: Response) -> Response:
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Accept-Ranges"] = "bytes"
    return resp


def _base() -> Path:
    cfg = cfg_module.load()
    base = cfg.get("download_dir") or "."
    return Path(base).resolve()


@app.after_request
def after(resp: Response) -> Response:
    return _add_cors(resp)


@app.route("/")
def index():
    """Отдаёт HTML-интерфейс — страница грузится с реального origin,
    поэтому localStorage и cookies работают нормально."""
    return Response(HTML, mimetype="text/html; charset=utf-8")


@app.route("/audio/<path:filename>")
def audio(filename: str):
    """Отдаёт файл по относительному пути от базовой папки."""
    return send_from_directory(_base(), filename)


@app.route("/find/<path:filename>")
def find(filename: str):
    """
    Ищет файл по имени рекурсивно в базовой папке.
    Нужно для вкладки «Скачанные», где хранится только имя файла.
    """
    base = _base()
    for p in base.rglob(filename):
        if p.is_file():
            return send_file(p)
    return Response("Not found", status=404)


@app.route("/cover/<path:filename>")
def cover(filename: str):
    """Обложка из тегов файла или cover.jpg в папке альбома."""
    base = _base()
    try:
        target = (base / filename).resolve()
        target.relative_to(base)
    except Exception:
        return Response("Forbidden", status=403)
    if not target.is_file():
        return Response("Not found", status=404)
    art = cover_bytes(target)
    if not art:
        return Response("No cover", status=404)
    data, mime = art
    resp = Response(data, mimetype=mime)
    resp.cache_control.max_age = 86400
    return resp


@app.route("/ping")
def ping():
    return "ok"


def start_server(port: int = 5000) -> None:
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
