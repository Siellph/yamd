import os
import threading
import time
import webview

from api import Api
from desktop import DesktopHost, claim_single_instance, keep_webview_alive
from local_play_server import start_server

os.environ["PYTHONUTF8"] = "1"

SERVER_PORT = 5000


def main():
    if not claim_single_instance():
        return

    keep_webview_alive()
    api = Api()

    threading.Thread(target=start_server, args=(SERVER_PORT,), daemon=True).start()

    # Ждём, пока Flask поднимется
    time.sleep(0.3)

    window = webview.create_window(
        title="Yandex Music Downloader",
        url=f"http://127.0.0.1:{SERVER_PORT}/",
        js_api=api,
        width=1080,
        height=740,
        min_size=(960, 680),
        background_color="#0f0f11",
    )

    api._window = window
    host = DesktopHost(window, api)
    host.attach()

    try:
        webview.start(debug=False, private_mode=False)
    except TypeError:
        webview.start(debug=False)
    finally:
        host.shutdown()


if __name__ == "__main__":
    main()
