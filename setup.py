import os
import sys
from cx_Freeze import setup, Executable

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_SITE_PACKAGES = os.path.join(BASE_DIR, "venv", "Lib", "site-packages")
sys.path.insert(0, os.path.join(BASE_DIR, "django_bootstrap3-23.1.dist-info"))

# Include necessary folders
include_files = [
    (os.path.join(BASE_DIR, "gts_service"), "gts_service"),
    (os.path.join(BASE_DIR, "openscad"), "openscad"),
    (os.path.join(BASE_DIR, "gerber_to_scad"), "gerber_to_scad"),
    (os.path.join(BASE_DIR, "icon.ico"), "icon.ico"),    
    # Bootstrap3 metadata (DO NOT TOUCH!) cx_freeze does not detect it if it's not explicitly pointed out like it's here!
    (os.path.join(VENV_SITE_PACKAGES, "django_bootstrap3-23.1.dist-info"), "lib/django_bootstrap3-23.1.dist-info"),
]

build_options = {
    "packages": [
        "os",
        "sys",
        "subprocess",
        "django",
        "bootstrap3",
        "gerber",
        "gerber_to_scad",
        "gts_service",
    ],
    "include_files": include_files,
}

exe = Executable(
    script="main.py",
    base="Win32GUI",
    icon=os.path.join(BASE_DIR, "icon.ico"),
)

setup(
    name="GerberToSTL",
    version="0.1.4",
    description="Gerber to STL converter",
    options={"build_exe": build_options},
    executables=[exe],
)
