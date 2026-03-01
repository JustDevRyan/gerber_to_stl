# webview_manager.py — lives in core/
import os
import sys
import subprocess
import json

# sys.executable always points to GerberToSTL.exe in the build root (frozen)
# or the Python interpreter (dev). Either way, dirname gives us the right root.
if getattr(sys, "frozen", False):
    BUILD_ROOT = os.path.dirname(sys.executable)
else:
    # dev: go one level up from core/
    BUILD_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE_DIR = os.path.join(BUILD_ROOT, "core")


def _get_webview_executable():
    """
    - Frozen: webview_app.exe is in the build root (must be there for DLLs)
    - Dev: run core/webview_app.py with the Python interpreter
    """
    if getattr(sys, "frozen", False):
        exe = os.path.join(BUILD_ROOT, "webview_app.exe")
        if not os.path.exists(exe):
            raise FileNotFoundError(
                f"webview_app.exe not found at {exe}. "
                "Make sure webview_app is included as a separate executable in setup.py."
            )
        return [exe]
    else:
        script = os.path.join(CORE_DIR, "webview_app.py")
        return [sys.executable, script]


class WebViewManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.webview_process = None

    def launch_webview(self, url, save_path=None, on_launch_callback=None, on_error_callback=None):
        try:
            if self.is_running():
                if on_error_callback:
                    on_error_callback("Standalone already running.")
                return False

            if save_path is None:
                save_path = os.path.join(os.path.expanduser("~"), "Documents")

            # Config JSON in build root — accessible by both manager and webview_app.exe
            config = {"url": url, "save_path": save_path}
            config_path = os.path.join(BUILD_ROOT, "_webview_config.json")
            with open(config_path, "w") as f:
                json.dump(config, f)

            cmd = _get_webview_executable() + [config_path]

            self.webview_process = subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )

            if on_launch_callback:
                on_launch_callback(url)
            return True

        except Exception as e:
            if on_error_callback:
                on_error_callback(str(e))
            return False

    def close_webview(self):
        if self.webview_process and self.webview_process.poll() is None:
            try:
                self.webview_process.terminate()
                self.webview_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.webview_process.kill()
            finally:
                self.webview_process = None

        config_path = os.path.join(BUILD_ROOT, "_webview_config.json")
        if os.path.exists(config_path):
            try:
                os.remove(config_path)
            except Exception:
                pass

    def is_running(self):
        return self.webview_process is not None and self.webview_process.poll() is None