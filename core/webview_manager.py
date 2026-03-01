# webview_manager.py
import os
import sys
import subprocess
import json


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

            config = {"url": url, "save_path": save_path}
            config_path = os.path.join(self.base_dir, "_webview_config.json")
            with open(config_path, "w") as f:
                json.dump(config, f)

            launcher = os.path.join(self.base_dir, "webview_app.py")

            self.webview_process = subprocess.Popen(
                [sys.executable, launcher, config_path],
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

        config_path = os.path.join(self.base_dir, "_webview_config.json")
        if os.path.exists(config_path):
            try:
                os.remove(config_path)
            except Exception:
                pass

    def is_running(self):
        return self.webview_process is not None and self.webview_process.poll() is None