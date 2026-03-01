# core/main.py
import os
import sys
import signal
import multiprocessing
multiprocessing.freeze_support()

# Add current directory to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Third-party imports
from PyQt5.QtWidgets import QApplication

# Now these should work
from config import *
from utils import setup_exception_handler
from ui_components import WebServerUI

# Django imports
from gts_service.wsgi import application

def run_app():
    # Setup signal handlers
    def handle_exit(sig, frame):
        print(f"\n{WARNING} Shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Setup exception handler
    setup_exception_handler()
    
    # Create and run application
    app = QApplication(sys.argv)
    window = WebServerUI()
    window.resize(380, 450)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()