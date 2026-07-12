import os
import threading
import time
import webview

from api import Api
from local_play_server import start_server

os.environ["PYTHONUTF8"] = "1"

SERVER_PORT = 5000


def main():
    api = Api()

    threading.Thread(target=start_server, args=(SERVER_PORT,), daemon=True).start()

    # Ждём, пока Flask поднимется
    time.sleep(0.3)

    window = webview.create_window(
        title="Yandex Music Downloader",
        url=f"http://127.0.0.1:{SERVER_PORT}/",
        js_api=api,
        width=1020,
        height=720,
        min_size=(820, 560),
        background_color="#0f0f11",
    )

    api._window = window

    webview.start(debug=False)


if __name__ == "__main__":
    main()
