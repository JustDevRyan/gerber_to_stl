import os
import sys
import signal
import threading
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QLineEdit, QTextEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from gts_service.wsgi import application


class EmittingStream:
    # Redirect stdout/stderr to a QTextEdit.
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        if text.strip():
            self.text_edit.append(text)
            self.text_edit.moveCursor(self.text_edit.textCursor().End)

    def flush(self):
        pass

class WebServerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()

        self.setWindowTitle("Gerber To STL")

        layout = QVBoxLayout()


        # Label colors
        global INFO
        INFO = '<span style="color:#00b5de;">[INFO]</span>'
        global ERROR
        ERROR = '<span style="color:red;">[ERROR]</span>'
        global WARNING
        WARNING = '<span style="color:orange;">[WARNING]</span>'
        global SUCCESS
        SUCCESS = '<span style="color:green;">[SUCCESS]</span>'



        # --- Title ---
        title = QLabel(
            'Ported to Windows by <a href="https://github.com/JustDevRyan" style="text-decoration:none; color:#3399ff; cursor:pointer;">JustDevRyan</a>'
        )
        title.setAlignment(Qt.AlignCenter)
        title.setOpenExternalLinks(True)  # Make link clickable
        title.setStyleSheet("""
            font-size: 20px;
            margin: 12px;
        """)
        layout.addWidget(title)

        # --- Port Section ---
        layout.addWidget(QLabel("Port:"))
        port_row = QHBoxLayout()
        self.port_input = QLineEdit("8000")
        self.port_input.setEnabled(False)
        self.port_input.setFixedWidth(150)
        self.port_checkbox = QCheckBox("Customize")
        self.port_checkbox.stateChanged.connect(self.toggle_port)
        port_row.addWidget(self.port_input)
        port_row.addWidget(self.port_checkbox)
        layout.addLayout(port_row)

        # --- Console ---
        layout.addWidget(QLabel("Console Output:"))
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console, stretch=1)

        # --- Start/Stop button ---
        self.start_button = QPushButton("Start Webserver")
        self.start_button.clicked.connect(self.toggle_webserver)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Redirect stdout/stderr
        sys.stdout = EmittingStream(self.console)
        sys.stderr = EmittingStream(self.console)

        # Server thread + instance
        self.server_thread = None
        self.server_instance = None

    def toggle_port(self, state):
        if state == Qt.Checked:
            self.port_input.setEnabled(True)
        else:
            self.port_input.setText("8000")
            self.port_input.setEnabled(False)

    def toggle_webserver(self):
        if self.server_thread and self.server_thread.is_alive():
            self.stop_webserver()
        else:
            self.start_webserver()

    def start_webserver(self):
        host = "127.0.0.1"
        port = int(self.port_input.text())
        self.console.clear()
        print(f"{INFO} Starting webserver on {host}:{port}...")

        if self.server_thread and self.server_thread.is_alive():
            print(f"{WARNING} Webserver is already running!")
            return

        self.stop_event.clear()
        self.start_button.setText("Stop Webserver")
        self.server_thread = threading.Thread(target=self.runserver, args=(host, port), daemon=True)
        self.server_thread.start()

    def stop_webserver(self):        
        if self.server_instance:
            print(f"{WARNING} Requesting server stop...")
            self.stop_event.set()
            if self.server_thread:
                self.server_thread.join(timeout=3)
            self.server_instance = None
            self.server_thread = None
            self.start_button.setText("Start Webserver")
            print(f"{SUCCESS} Server stopped.")
        else:
            print(f"{ERROR} No running webserver to stop.")

    def runserver(self, host, port):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gts_service.settings")
        try:
            with make_server(host, port, application, server_class=WSGIServer, handler_class=WSGIRequestHandler) as httpd:
                self.server_instance = httpd
                print(f"{SUCCESS} Serving on http://{host}:{port} (Press Stop Webserver or close app to quit)")

                while not self.stop_event.is_set():
                    httpd.handle_request()
        except OSError as e:
            print(f"{ERROR} Could not start server: {e}")
        finally:
            self.server_instance = None
            self.server_thread = None
            self.start_button.setText("Start Webserver")
            print(f"{INFO} Webserver thread exited.")


if __name__ == "__main__":

    def handle_exit(sig, frame):
        print(f"\n{WARNING} Shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    app = QApplication(sys.argv)
    window = WebServerUI()
    window.resize(390, 450)
    window.setWindowIcon(QIcon(".\icon.ico"))
    window.setFixedSize(window.size()) 
    window.show()
    sys.exit(app.exec_())
