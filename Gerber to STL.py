import os
import sys

# Add core directory to path
CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

# Now import from core
from core.main import run_app

if __name__ == "__main__":
    run_app()