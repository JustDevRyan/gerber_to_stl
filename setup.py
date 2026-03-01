import os
import sys
import django
from cx_Freeze import setup, Executable

# --- Path Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_SITE_PACKAGES = os.path.join(BASE_DIR, "venv", "Lib", "site-packages")

sys.path.insert(0, os.path.join(BASE_DIR, "core"))

DJANGO_PATH = os.path.dirname(django.__file__)
DJANGO_LOCALE = os.path.join(DJANGO_PATH, "conf", "locale")

include_files = [
    (os.path.join(BASE_DIR, "icon.ico"), "icon.ico"),
    
    # --- MANDATORY ----------------------------------------------------------
    (os.path.join(VENV_SITE_PACKAGES, "django_bootstrap3-23.1.dist-info"),
     "lib/django_bootstrap3-23.1.dist-info"),
    # ------------------------------------------------------------------------

    (DJANGO_LOCALE, os.path.join("lib", "django", "conf", "locale")),

    (os.path.join(BASE_DIR, "core", "openscad"), "lib/core/openscad"),
]

for folder in ["templates", "static", "media"]:
    folder_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(folder_path):
        include_files.append((folder_path, folder))

# --- Build options ---
build_options = {
    "optimize": 2,
    "include_msvcr": True,
    "packages": [
        "os", "sys", "django", "webview", "gerber", "core",
        "PyQt5.QtCore", "PyQt5.QtWidgets", "PyQt5.QtGui",
        "bootstrap3", 
        "django.core.management",
        "django.template.loaders",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.db.backends.sqlite3",
        "asyncio", "pydoc",
    ],
    "includes": [
        "core.gts_service.wsgi",
        "core.gts_service.settings",
        "core.gts_service.urls",
    ],
    # Massive size reduction by excluding this many unused libraries and dlls
    "excludes": [
        "tkinter", "unittest", "email", "pydoc", "test", 
        "PyQt5.QtQml", "PyQt5.QtQuick", "PyQt5.QtSql", "PyQt5.QtXml",
        "PyQt5.QtWebEngine", "PyQt5.QtWebEngineCore", "PyQt5.QtWebEngineWidgets",
        "PyQt5.QtMultimedia", "PyQt5.QtMultimediaWidgets",
        "PyQt5.QtDesigner", "PyQt5.QtNetwork", "PyQt5.QtScript",
        "PyQt5.QtSql", "PyQt5.QtTest", "PyQt5.QtXmlPatterns",
        "lib2to3", "setuptools", "distutils",
    ],
    "bin_excludes": [
        "Qt5WebEngineCore.dll", "Qt5WebEngine.dll", "Qt5Quick.dll", 
        "Qt5Qml.dll", "Qt5Designer.dll", "Qt5Network.dll", 
        "Qt5Multimedia.dll", "Qt5VirtualKeyboard.dll", "Qt5Xml.dll",
        "Qt5Test.dll", "Qt5Positioning.dll", "Qt5Sensors.dll"
    ],
    "include_files": include_files,
    "include_msvcr": True,
    "zip_include_packages": [], 
    "zip_exclude_packages": ["*"], 
}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        script="Gerber to STL.py",
        base=base,
        icon=os.path.join(BASE_DIR, "icon.ico"),
        target_name="GerberToSTL.exe",
    ),
    Executable(
        script="core/webview_app.py",
        base=base,
        icon=os.path.join(BASE_DIR, "icon.ico"),
        target_name="webview_app.exe",
    ),
]

setup(
    name="GerberToSTL",
    version="2.5.2",
    description="Gerber to STL converter",
    options={"build_exe": build_options},
    executables=executables,
)
