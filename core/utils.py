# utils.py
import os
import sys
import traceback
import subprocess
from PyQt5.QtWidgets import QMessageBox

def setup_exception_handler():
    def excepthook(exc_type, exc_value, exc_traceback):
        error_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # Print to console
        print(error_text, file=sys.stderr)
        
        # Save to file
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(error_text)
        
        # Show popup
        try:
            QMessageBox.critical(None, "Application Error", error_text)
        except Exception:
            pass
        
        sys.exit(1)
    
    sys.excepthook = excepthook

def is_port_valid(port):
    return 1 <= port <= 65535

def create_webview_script(url, base_dir, save_path=None):
    if save_path is None:
        save_path = os.path.join(os.path.expanduser("~"), "Documents")
    
    # Escape backslashes for Windows paths
    save_path_escaped = save_path.replace("\\", "\\\\")
    
    script_content = f'''
import webview
import os

url = "{url}"
save_path = "{save_path_escaped}"

window = webview.create_window(
    "Gerber to STL Converter",
    url,
    width=1200,
    height=700,
    resizable=True,
    background_color="#ffffff",
)
webview.start()
'''
    temp_script = os.path.join(base_dir, "webview_temp.py")
    with open(temp_script, 'w') as f:
        f.write(script_content)
    return temp_script

def cleanup_temp_files(base_dir):
    temp_script = os.path.join(base_dir, "webview_temp.py")
    if os.path.exists(temp_script):
        try:
            os.remove(temp_script)
            return True
        except Exception:
            return False
    return False