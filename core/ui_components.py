from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QLineEdit, QTextEdit, QPushButton, QLabel,
    QFrame, QTabWidget,
    QRadioButton, QButtonGroup, QScrollArea, QMessageBox
)

from PyQt5.QtCore import Qt, QMetaObject, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

import sys
from PyQt5.QtCore import QObject, pyqtSignal

import os

# Internal imports
from config import *
from utils import is_port_valid
from server import ServerManager
from webview_manager import WebViewManager

# --- IMPORT NEW MANAGER ---
from settings_manager import SettingsManager

# ------------------------- Console redirection -------------------------
class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def __init__(self, text_edit):
        super().__init__()
        self.defaults = {
            "port": str(DEFAULT_PORT),
            "customize_port": False,
            "auto_open": False,
            "open_target": "app",
            "theme": "system",
            "save_path": DEFAULT_SAVE_PATH
        }

        global DEFAULT_SETTINGS
        DEFAULT_SETTINGS = self.defaults

        self.text_edit = text_edit
        self.text_written.connect(self._append_text)

    def write(self, text):
        if text.strip():
            self.text_written.emit(text)

    def flush(self):
        pass

    def _append_text(self, text):
        self.text_edit.append(text)
        self.text_edit.moveCursor(self.text_edit.textCursor().End)


# ------------------------- Main UI -------------------------
class WebServerUI(QWidget):
    def __init__(self):
        super().__init__()

        # --- INITIALIZE SETTINGS ---
        self.settings_manager = SettingsManager(default_port=DEFAULT_PORT)
        
        self.server_manager = ServerManager()
        self.webview_manager = WebViewManager(BASE_DIR)

        self.setup_ui()
        
        # --- LOAD SAVED SETTINGS ---
        self.load_user_settings()
        
        self.setup_connections()

        sys.stdout = EmittingStream(self.console)
        sys.stderr = EmittingStream(self.console)

    def setup_ui(self):
        self.setWindowTitle("Gerber to STL")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(500, 570)

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #222;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
            }
            WebServerUI {
                background-color: #F7F7F7;
            }
            QLabel {
                border: none;
                background: transparent;
            }
            QLineEdit:disabled, QCheckBox:disabled, QPushButton:disabled, QLabel:disabled {
                color: #9a9a9a;
            }
            QLineEdit:disabled { background: #f1f1f1; }
            QLineEdit { background: white; padding: 6px; border-radius: 6px; border: 1px solid #ccc; }
            QCheckBox { 
                spacing: 6px; 
                background-color: transparent;
            }
            QTextEdit {
                background: white;
                border-radius: 6px;
                border: 1px solid #ccc;
                padding: 8px;
                color: #333;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d1d1d1;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #b5b5b5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
            QTabWidget::pane { border: 1px solid #ccc; border-radius: 6px; background: #fff; }
            QTabBar::tab { padding: 10px 18px; background: #e9e9e9; border: 1px solid #ccc; border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
            QTabBar::tab:selected { background: #ffffff; border-bottom: none; }
            QPushButton { background: #ededed; border-radius: 6px; border: 1px solid #bfbfbf; padding: 8px 14px; }
            QPushButton:hover { background: #e2e2e2; }
            QRadioButton { background-color: transparent; }
        """)

        root = QVBoxLayout()
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)
        self.setLayout(root)

        header = QLabel(
            "<span style='font-size:22px; font-weight:600;'>Gerber to STL</span><br>"
            "<span style='font-size:13px; color:#777;'>by JustDevRyan</span>"
        )
        header.setAlignment(Qt.AlignCenter)
        root.addWidget(header)

        tabs = QTabWidget()
        root.addWidget(tabs)

        # TAB 1 - WEB SERVER CONTROL
        tab_server = QWidget()
        tabs.addTab(tab_server, "Web Server")
        layout_server = QVBoxLayout()
        layout_server.setSpacing(16)
        layout_server.setContentsMargins(16, 16, 16, 16)
        tab_server.setLayout(layout_server)

        def card(title):
            frame = QFrame()
            frame.setStyleSheet(".QFrame { background: #ffffff; border-radius: 10px; border: 1px solid #dcdcdc; }")
            v = QVBoxLayout(frame)
            v.setContentsMargins(16, 16, 16, 16)
            v.setSpacing(12)
            v.addWidget(QLabel(f"<span style='font-size:16px; font-weight:600;'>{title}</span>"))
            return frame, v

        card_console, card_console_layout = card("Console")
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        card_console_layout.addWidget(self.console)
        layout_server.addWidget(card_console, stretch=1)

        btn_row = QHBoxLayout()
        self.start_button = QPushButton("Start Server")
        self.start_button.setStyleSheet("QPushButton { background: #0078ff; color: white; border-radius: 6px; padding: 10px; border: none; } QPushButton:hover { background: #0068e6; }")
        
        self.open_button_standalone = QPushButton("Open Standalone")
        self.open_button_browser = QPushButton("Open in Browser")
        self.open_button_standalone.setEnabled(False)
        self.open_button_browser.setEnabled(False)

        # SET CURSORS MANUALLY (STOPS CONSOLE SPAM)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.open_button_standalone.setCursor(Qt.PointingHandCursor)
        self.open_button_browser.setCursor(Qt.PointingHandCursor)

        btn_row.addWidget(self.start_button)
        btn_row.addWidget(self.open_button_standalone)
        btn_row.addWidget(self.open_button_browser)
        layout_server.addLayout(btn_row)

        # =========================================================
        # TAB 2 - SETTINGS
        # =========================================================
        settings_scroll = QScrollArea()
        settings_scroll.setWidgetResizable(True)
        settings_scroll.setFrameShape(QFrame.NoFrame)
        settings_scroll.setStyleSheet("background: transparent;")
        
        tabs.addTab(settings_scroll, "Settings")

        settings_content = QWidget()
        settings_scroll.setWidget(settings_content)

        layout_settings = QVBoxLayout(settings_content)
        layout_settings.setSpacing(12)
        layout_settings.setContentsMargins(16, 16, 16, 16)

        # 1. Application Settings Card
        card_pref, pref_layout = card("Application Settings")
        pref_layout.setSpacing(10)
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("background-color: #eee; margin: 1px 0px;")
        pref_layout.addWidget(line1)

        # Misc
        misc_label = QLabel("Misc")
        misc_label.setStyleSheet("font-weight: 600; color: #222; font-size: 15px;")
        misc_label.setContentsMargins(15, 0, 0, 0)
        pref_layout.addWidget(misc_label)

        self.auto_open_check = QCheckBox("Auto open server")
        self.auto_open_check.setStyleSheet("margin-left: 15px;")
        
        self.choice_container = QWidget()
        choice_row = QHBoxLayout(self.choice_container)
        choice_row.setContentsMargins(40, 0, 0, 0)
        
        self.open_app_radio = QRadioButton("App")
        self.open_browser_radio = QRadioButton("Browser")
        self.open_app_radio.setCursor(Qt.PointingHandCursor)
        self.open_browser_radio.setCursor(Qt.PointingHandCursor)
        
        sep = QLabel("|")
        sep.setStyleSheet("color: #ccc; font-weight: bold;")

        choice_row.addWidget(self.open_app_radio)
        choice_row.addWidget(sep)
        choice_row.addWidget(self.open_browser_radio)
        choice_row.addStretch()

        pref_layout.addWidget(self.auto_open_check)
        pref_layout.addWidget(self.choice_container)

        # Appearance
        appearance_label = QLabel("Appearance (coming soon.)")
        appearance_label.setStyleSheet("font-weight: 600; color: #222; font-size: 15px;")
        appearance_label.setContentsMargins(15, 0, 0, 0)
        pref_layout.addWidget(appearance_label)
        
        theme_row = QHBoxLayout()
        theme_row.setContentsMargins(25, 0, 0, 0)
        self.theme_light = QRadioButton("Light")
        self.theme_dark = QRadioButton("Dark")
        self.theme_system = QRadioButton("System")
        self.theme_light.setCursor(Qt.PointingHandCursor)
        self.theme_dark.setCursor(Qt.PointingHandCursor)
        self.theme_system.setCursor(Qt.PointingHandCursor)
        
        self.theme_group = QButtonGroup(self)
        self.theme_group.addButton(self.theme_light)
        self.theme_group.addButton(self.theme_dark)
        self.theme_group.addButton(self.theme_system)

        theme_row.addWidget(self.theme_light)
        theme_row.addWidget(self.theme_dark)
        theme_row.addWidget(self.theme_system)
        theme_row.addStretch()
        pref_layout.addLayout(theme_row)
        layout_settings.addWidget(card_pref)

        # 2. Server Settings Card
        card_settings, card_settings_layout = card("Server Settings")
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("background-color: #eee; margin: 1px 0px;")
        card_settings_layout.addWidget(line2)

        port_row = QHBoxLayout()
        port_row.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit()
        self.port_input.setFixedWidth(120)
        self.port_checkbox = QCheckBox("Customize")
        port_row.addWidget(self.port_input)
        port_row.addStretch()
        port_row.addWidget(self.port_checkbox)
        card_settings_layout.addLayout(port_row)
        layout_settings.addWidget(card_settings)

        # --- Save Path Option ---
        path_label = QLabel("Default Save Path")
        path_label.setStyleSheet("font-weight: 600; color: #222; font-size: 15px;")
        path_label.setContentsMargins(15, 5, 0, 0)
        pref_layout.addWidget(path_label)

        path_row = QHBoxLayout()
        path_row.setContentsMargins(15, 0, 0, 0)
        self.path_input = QLineEdit(DEFAULT_SAVE_PATH)
        self.path_input.setReadOnly(True) # Better to force use of the browse button
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setStyleSheet("QPushButton { background: #ededed; border: 1px solid #bfbfbf; border-radius: 6px; } QPushButton:hover { background: #e2e2e2; }")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setFixedWidth(80)
        
        path_row.addWidget(self.path_input)
        path_row.addWidget(self.browse_btn)
        pref_layout.addLayout(path_row)

        # 3. RESET CARD (New Box at the bottom)
        card_reset, reset_layout = card("Danger Zone")
        reset_layout.setSpacing(10)
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setStyleSheet("background-color: #eee; margin: 1px 0px;")
        reset_layout.addWidget(line3)

        self.reset_button = QPushButton("Reset to Default Settings")
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.setStyleSheet("""
            QPushButton { 
                background: #fff; color: #d64545; border: 1px solid #d64545; 
                padding: 8px; border-radius: 6px; font-weight: 600;
            }
            QPushButton:hover { background: #fff5f5; }
        """)
        reset_layout.addWidget(self.reset_button)
        layout_settings.addWidget(card_reset)

        layout_settings.addStretch()

    def reset_to_defaults(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmation")
        
        msg.setText("<b style='color: #222; font-size: 15px;'>Restore default settings?</b>")
        msg.setInformativeText("<span style='color: #555;'>All your settings will be reset to default values. Are you sure?</span>")
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QLabel {
                background: transparent;
            }
            QPushButton {
                background-color: #ededed;
                color: #222;
                border: 1px solid #bfbfbf;
                border-radius: 6px;
                padding: 6px 15px;
                min-width: 80px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e2e2e2;
            }
            QPushButton[text="Yes, reset"] {
                background-color: #fff;
                color: #d64545;
                border: 1px solid #d64545;
                font-weight: 600;
            }
            QPushButton[text="Yes, reset"]:hover {
                background-color: #fff5f5;
            }
        """)
        
        yes_button = msg.addButton("Yes, reset", QMessageBox.YesRole)
        no_button = msg.addButton("Cancel", QMessageBox.NoRole)
        msg.setDefaultButton(no_button)

        msg.exec_()

        if msg.clickedButton() == yes_button:
            d = DEFAULT_SETTINGS
            
            self.port_input.setText(d["port"])
            self.port_checkbox.setChecked(d["customize_port"])
            self.auto_open_check.setChecked(d["auto_open"])
            
            if d["open_target"] == "browser":
                self.open_browser_radio.setChecked(True)
            else:
                self.open_app_radio.setChecked(True)
                
            t = d["theme"]
            if t == "light": self.theme_light.setChecked(True)
            elif t == "dark": self.theme_dark.setChecked(True)
            else: self.theme_system.setChecked(True)
            
            self.path_input.setText(d["save_path"])

            self.save_user_settings()

    def setup_connections(self):
        self.port_checkbox.stateChanged.connect(self.toggle_port)
        self.start_button.clicked.connect(self.toggle_webserver)
        self.open_button_standalone.clicked.connect(self.open_standalone)
        self.open_button_browser.clicked.connect(self.open_in_browser)

        self.port_input.textChanged.connect(self.save_user_settings)
        self.port_checkbox.stateChanged.connect(self.save_user_settings)
        self.auto_open_check.stateChanged.connect(self.save_user_settings)

        self.auto_open_check.toggled.connect(self.choice_container.setEnabled)
        self.open_app_radio.toggled.connect(self.save_user_settings)
        self.open_browser_radio.toggled.connect(self.save_user_settings)
        
        self.theme_light.toggled.connect(self.save_user_settings)
        self.theme_dark.toggled.connect(self.save_user_settings)
        self.theme_system.toggled.connect(self.save_user_settings)

        self.reset_button.clicked.connect(self.reset_to_defaults)
    
        self.choice_container.setEnabled(self.auto_open_check.isChecked())

        self.browse_btn.clicked.connect(self.browse_save_path)

    def browse_save_path(self):
        from PyQt5.QtWidgets import QFileDialog
        existing_path = self.path_input.text()
        new_dir = QFileDialog.getExistingDirectory(self, "Select Save Directory", existing_path)
        if new_dir:
            self.path_input.setText(new_dir)
            self.save_user_settings()

    def load_user_settings(self):
        data = self.settings_manager.load()
        self.port_input.setText(data.get("port", str(DEFAULT_PORT)))
        self.port_checkbox.setChecked(data.get("customize_port", False))
        self.auto_open_check.setChecked(data.get("auto_open", False))
        if data.get("open_target") == "browser":
            self.open_browser_radio.setChecked(True)
        else: self.open_app_radio.setChecked(True)
        self.choice_container.setEnabled(self.auto_open_check.isChecked())
        self.toggle_port(self.port_checkbox.checkState())
        theme = data.get("theme", "system")
        if theme == "light": self.theme_light.setChecked(True)
        elif theme == "dark": self.theme_dark.setChecked(True)
        else: self.theme_system.setChecked(True)
        self.path_input.setText(data.get("save_path", DEFAULT_SAVE_PATH))

    def save_user_settings(self):
        theme_choice = "system"
        if self.theme_light.isChecked(): theme_choice = "light"
        elif self.theme_dark.isChecked(): theme_choice = "dark"

        data = {
            "port": self.port_input.text(),
            "customize_port": self.port_checkbox.isChecked(),
            "auto_open": self.auto_open_check.isChecked(),
            "open_target": "app" if self.open_app_radio.isChecked() else "browser",
            "theme": theme_choice,
            "save_path": self.path_input.text(),
        }
        self.settings_manager.save(data)

    def toggle_port(self, state):
        self.port_input.setEnabled(state == Qt.Checked)
        if not state:
            self.port_input.setText(str(DEFAULT_PORT))

    def toggle_webserver(self):
        if self.start_button.text() == "Stop Server":
            print(f"{INFO} Stopping server...")
            self.stop_webserver()
        else:
            print(f"{INFO} Attempting to start server...")
            self.start_webserver()

    def start_webserver(self):
        try:
            port = int(self.port_input.text())
            if not is_port_valid(port): raise ValueError("Port must be 1-65535")
            
            self.console.clear()
            print(f"{INFO} Starting webserver on {HOST}:{port}...")
            
            def on_server_start(host, port):
                print(f"{SUCCESS} Serving at http://{host}:{port}")
                self.start_button.setText("Stop Server")
                self.start_button.setStyleSheet("""
                    QPushButton { background: #d64545; color: white; border-radius: 6px; padding: 10px; border: none; }
                    QPushButton:hover { background: #c0392b; }
                """)
                self.open_button_standalone.setEnabled(True)
                self.open_button_browser.setEnabled(True)

                if self.auto_open_check.isChecked():
                    if self.open_app_radio.isChecked():
                        QMetaObject.invokeMethod(self, "open_standalone", Qt.QueuedConnection)
                    else:
                        import webbrowser
                        webbrowser.open(f"http://{HOST}:{port}")

            self.server_manager.start_server(HOST, port, on_server_start, print)
        except Exception as e:
            print(f"{ERROR} {e}")

    def stop_webserver(self):
        try:
            self.server_manager.stop_server()
            self.start_button.setText("Start Server")
            self.start_button.setStyleSheet("""
                QPushButton { background: #0078ff; color: white; border-radius: 6px; padding: 10px; border: none; }
                QPushButton:hover { background: #0068e6; }
            """)
            self.port_checkbox.setEnabled(True)
            if self.port_checkbox.isChecked(): self.port_input.setEnabled(True)
            self.open_button_standalone.setEnabled(False)
            self.open_button_browser.setEnabled(False)
            print(f"{SUCCESS} Server stopped successfully.")
        except Exception as e:
            print(f"{ERROR} Shutdown error: {e}")

    @pyqtSlot()
    def open_standalone(self):
        try:
            port = int(self.port_input.text())
            save_path = self.path_input.text()
            self.webview_manager.launch_webview(
                f"http://{HOST}:{port}",
                save_path=save_path,
                on_launch_callback=print,
                on_error_callback=print
            )
        except: print(f"{ERROR} Invalid port")

    def open_in_browser(self):
        try:
            import webbrowser
            webbrowser.open(f"http://{HOST}:{int(self.port_input.text())}")
        except: print(f"{ERROR} Invalid port")

    def setup_downloads(self, webview_view):
        profile = webview_view.page().profile()
        
        profile.downloadRequested.connect(self.on_download_requested)

    def on_download_requested(self, download):
        from settings_manager import SettingsManager
        settings = SettingsManager().load()
        save_dir = settings.get("save_path", os.path.join(os.path.expanduser("~"), "Documents"))
        
        full_path = os.path.join(save_dir, download.suggestedFileName())
        try:
            download.setPath(full_path)
            download.accept()
            print(f"[SUCCESS] File saving to: {full_path}")
        except:
            print(f"[ERROR] Failed to save file to: {full_path}")

    def closeEvent(self, event):
        self.save_user_settings()
        self.server_manager.stop_server()
        self.webview_manager.close_webview()
        super().closeEvent(event)