"""
Локальный HTTP-сервер для воспроизведения аудиофайлов.
pywebview блокирует file://, поэтому отдаём файлы через 127.0.0.1:5000.

Маршруты:
  GET /              — главная страница (HTML-интерфейс)
  GET /audio/<path>  — файл по относительному пути от download_dir
  GET /find/<name>   — поиск файла по имени рекурсивно
"""
from __future__ import annotations

from pathlib import Path

from flask import Flask, Response, send_file, send_from_directory

import config as cfg_module
from gui.html import HTML

app = Flask(__name__)


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


@app.route("/ping")
def ping():
    return "ok"


def start_server(port: int = 5000) -> None:
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
