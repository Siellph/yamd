"""
Системный трей и медиаклавиши Windows.

Закрытие окна скрывает его в трей (hide в отдельном потоке — иначе pywebview
зависает). Выход только из меню трея: flush_last_play без evaluate_js.
"""
from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path
from typing import Callable, Optional


_WV2_KEEPALIVE = (
    "--disable-background-timer-throttling "
    "--disable-renderer-backgrounding "
    "--disable-backgrounding-occluded-windows "
    "--disable-features=CalculateNativeWinOcclusion"
)

_JS_MEDIA = {
    "playpause": "if(typeof mediaPlayPause==='function') mediaPlayPause();",
    "prev": "if(typeof mediaPrev==='function') mediaPrev();",
    "next": "if(typeof mediaNext==='function') mediaNext();",
}


def keep_webview_alive() -> None:
    """Не дать WebView2 уснуть, когда окно спрятано в трей — иначе встанет звук."""
    if sys.platform != "win32":
        return
    prev = (os.environ.get("WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS") or "").strip()
    if _WV2_KEEPALIVE in prev:
        return
    os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = (
        f"{prev} {_WV2_KEEPALIVE}".strip()
    )


def _base_dirs() -> list[Path]:
    here = Path(__file__).resolve().parent
    dirs = [here]
    if getattr(sys, "frozen", False):
        dirs.append(Path(sys.executable).resolve().parent)
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            dirs.append(Path(meipass))
    return dirs


def _load_tray_image():
    from PIL import Image, ImageDraw

    names = ("icon-music.png", "icon-music.ico")
    for base in _base_dirs():
        assets = base / "assets"
        for name in names:
            path = assets / name
            if path.is_file():
                try:
                    im = Image.open(path)
                    im.load()
                    return im.convert("RGBA")
                except Exception:
                    pass

    img = Image.new("RGBA", (64, 64), (15, 15, 17, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, 60, 60), fill=(245, 158, 11, 255))
    draw.ellipse((16, 36, 30, 50), fill=(15, 15, 17, 255))
    draw.rectangle((26, 16, 32, 42), fill=(15, 15, 17, 255))
    draw.polygon([(32, 16), (46, 22), (46, 28), (32, 22)], fill=(15, 15, 17, 255))
    return img


class DesktopHost:
    def __init__(self, window, api) -> None:
        self.window = window
        self.api = api
        self.exit_requested = False
        self._hidden = False
        self._icon = None
        self._tray_thread: Optional[threading.Thread] = None
        self._media: Optional[_WinMediaKeys] = None
        self._invoke_lock = threading.Lock()
        self._last_invoke = 0.0

    def attach(self) -> None:
        self._start_tray()
        self._start_media_keys()
        try:
            self.window.events.closing += self.on_closing
        except Exception:
            pass

    def on_closing(self):
        # Без иконки трея прятать нельзя — иначе не из чего выйти.
        if self.exit_requested or self._icon is None:
            self.api.flush_last_play()
            return True
        self.api.flush_last_play()
        self._hidden = True
        threading.Thread(target=self._hide_window, daemon=True).start()
        return False

    def _hide_window(self) -> None:
        try:
            self.window.hide()
        except Exception:
            pass

    def show_window(self, *_args) -> None:
        def _show():
            try:
                self.window.show()
                try:
                    self.window.restore()
                except Exception:
                    pass
                self._hidden = False
            except Exception:
                pass

        threading.Thread(target=_show, daemon=True).start()

    def quit_app(self, *_args) -> None:
        if self.exit_requested:
            return
        self.exit_requested = True
        self.api.flush_last_play()
        self.stop_media_keys()
        icon = self._icon
        self._icon = None
        if icon is not None:
            try:
                icon.stop()
            except Exception:
                pass
        try:
            self.window.destroy()
        except Exception:
            pass

    def shutdown(self) -> None:
        self.exit_requested = True
        self.api.flush_last_play()
        self.stop_media_keys()
        icon = self._icon
        self._icon = None
        if icon is not None:
            try:
                icon.stop()
            except Exception:
                pass

    def invoke_player(self, action: str) -> None:
        if self.exit_requested:
            return
        js = _JS_MEDIA.get(action)
        if not js or not self.window:
            return
        now = time.monotonic()
        with self._invoke_lock:
            if now - self._last_invoke < 0.16:
                return
            self._last_invoke = now
        threading.Thread(target=self._run_player_js, args=(js,), daemon=True).start()

    def _run_player_js(self, js: str) -> None:
        # run_js, не evaluate_js: не ждём результат и не ловим дедлок закрытия.
        try:
            run = getattr(self.window, "run_js", None)
            if run:
                run(js)
            else:
                self.window.evaluate_js(js)
        except Exception:
            pass

    def _start_tray(self) -> None:
        try:
            import pystray
            from pystray import Menu, MenuItem
        except Exception:
            return

        image = _load_tray_image()
        menu = Menu(
            MenuItem("Показать", self.show_window, default=True),
            MenuItem("Выход", self.quit_app),
        )
        self._icon = pystray.Icon(
            "yamd",
            image,
            "Yandex Music Downloader",
            menu,
        )
        self._tray_thread = threading.Thread(target=self._icon.run, daemon=True)
        self._tray_thread.start()

    def _start_media_keys(self) -> None:
        if sys.platform != "win32":
            return
        self._media = _WinMediaKeys(self.invoke_player)
        self._media.start()

    def stop_media_keys(self) -> None:
        if self._media:
            self._media.stop()
            self._media = None


class _WinMediaKeys:
    """Глобальный WH_KEYBOARD_LL только для Play/Pause, Next, Prev."""

    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_PLAY_PAUSE = 0xB3
    WH_KEYBOARD_LL = 13
    WM_KEYDOWN = 0x0100
    WM_SYSKEYDOWN = 0x0104
    WM_QUIT = 0x0012

    def __init__(self, on_action: Callable[[str], None]) -> None:
        self._on_action = on_action
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._thread_id = 0
        self._hook = None
        self._proc = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, name="ym-media-keys", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if sys.platform != "win32":
            return
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            if self._hook:
                user32.UnhookWindowsHookEx(self._hook)
                self._hook = None
            tid = self._thread_id
            if tid:
                user32.PostThreadMessageW(tid, self.WM_QUIT, 0, 0)
        except Exception:
            pass

    def _loop(self) -> None:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        LRESULT = ctypes.c_ssize_t
        HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

        class KBDLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [
                ("vkCode", wintypes.DWORD),
                ("scanCode", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_void_p),
            ]

        user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int,
            HOOKPROC,
            wintypes.HINSTANCE,
            wintypes.DWORD,
        ]
        user32.SetWindowsHookExW.restype = wintypes.HHOOK
        user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        user32.CallNextHookEx.restype = LRESULT
        user32.GetMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
        ]
        user32.GetMessageW.restype = wintypes.BOOL
        kernel32.GetCurrentThreadId.restype = wintypes.DWORD

        self._thread_id = kernel32.GetCurrentThreadId()

        def _proc(n_code, w_param, l_param):
            if n_code >= 0 and w_param in (self.WM_KEYDOWN, self.WM_SYSKEYDOWN) and not self._stop.is_set():
                info = ctypes.cast(l_param, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                vk = info.vkCode
                action = None
                if vk == self.VK_MEDIA_PLAY_PAUSE:
                    action = "playpause"
                elif vk == self.VK_MEDIA_NEXT_TRACK:
                    action = "next"
                elif vk == self.VK_MEDIA_PREV_TRACK:
                    action = "prev"
                if action:
                    try:
                        self._on_action(action)
                    except Exception:
                        pass
                    return 1
            return user32.CallNextHookEx(self._hook, n_code, w_param, l_param)

        self._proc = HOOKPROC(_proc)
        self._hook = user32.SetWindowsHookExW(self.WH_KEYBOARD_LL, self._proc, None, 0)
        if not self._hook:
            return
        msg = wintypes.MSG()
        while not self._stop.is_set():
            r = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if r == 0 or r == -1:
                break
        if self._hook:
            try:
                user32.UnhookWindowsHookEx(self._hook)
            except Exception:
                pass
            self._hook = None
