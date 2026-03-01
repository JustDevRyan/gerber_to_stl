# config.py
import os
import sys

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gts_service.settings")

# Constants
INFO = '<span style="color:#00b5de;">[INFO]</span>'
ERROR = '<span style="color:red;">[ERROR]</span>'
WARNING = '<span style="color:orange;">[WARNING]</span>'
SUCCESS = '<span style="color:green;">[SUCCESS]</span>'

DEFAULT_PORT = 8000
HOST = "127.0.0.1"

# Get the user's Documents folder dynamically
DEFAULT_SAVE_PATH = os.path.join(os.path.expanduser("~"), "Documents")

APP_DEFAULTS = {
    "port": str(DEFAULT_PORT),
    "customize_port": False,
    "auto_open": False,
    "open_target": "app",
    "theme": "system",
    "save_path": DEFAULT_SAVE_PATH
}