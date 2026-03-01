# webview_app.py — standalone window using pywebview
import sys
import os
import json
import time
import urllib.request


def wait_for_server(url, timeout=15):
    """Wait until the Django server is responding before opening the window."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: webview_app.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        with open(config_path) as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to read config: {e}")
        sys.exit(1)

    url = config.get("url", "http://127.0.0.1:8000")
    save_path = config.get("save_path", os.path.join(os.path.expanduser("~"), "Documents"))

    # Wait for server to be ready (fixes blank/slow load)
    if not wait_for_server(url):
        print(f"Server at {url} did not respond in time.")
        sys.exit(1)

    try:
        import webview

        class SaveAPI:
            def __init__(self, path):
                self._save_path = path

            def get_save_path(self):
                return self._save_path

            def save_file(self, filename, hex_data):
                """Called from JS: receives filename + hex file bytes, writes to disk."""
                try:
                    os.makedirs(self._save_path, exist_ok=True)
                    # Sanitize filename
                    safe_name = os.path.basename(filename)
                    full_path = os.path.join(self._save_path, safe_name)
                    data = bytes.fromhex(hex_data)
                    with open(full_path, "wb") as f:
                        f.write(data)
                    print(f"[SUCCESS] Saved to: {full_path}")
                    return {"ok": True, "path": full_path}
                except Exception as ex:
                    print(f"[ERROR] Save failed: {ex}")
                    return {"ok": False, "error": str(ex)}

        api = SaveAPI(save_path)

        window = webview.create_window(
            "Gerber to STL Converter",
            url,
            width=1280,
            height=760,
            resizable=True,
            background_color="#fefefe",
            js_api=api,
        )

        def on_loaded():
            window.evaluate_js("window.__STANDALONE__ = true;")

        window.events.loaded += on_loaded

        webview.start(debug=False, http_server=False)

    except ImportError:
        print("pywebview not installed. Run: pip install pywebview")
        import webbrowser
        webbrowser.open(url)


if __name__ == "__main__":
    main()