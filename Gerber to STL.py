import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script_path = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        f'"{script_path}" {params}',
        None,
        1
    )
    sys.exit(0)

CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

from core.main import run_app

if __name__ == "__main__":
    run_app()
