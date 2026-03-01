# server.py
import threading
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler
from django.contrib.staticfiles.handlers import StaticFilesHandler
from core.gts_service.wsgi import application

class ServerManager:
    def __init__(self):
        self.server_instance = None
        self.server_thread = None
        self.stop_event = threading.Event()
        self.application = StaticFilesHandler(application)
    
    def start_server(self, host, port, on_start_callback=None, on_error_callback=None):
        def run_server():
            try:
                with make_server(host, port, self.application, 
                               server_class=WSGIServer, 
                               handler_class=WSGIRequestHandler) as httpd:
                    self.server_instance = httpd
                    if on_start_callback:
                        on_start_callback(host, port)
                    
                    while not self.stop_event.is_set():
                        try:
                            httpd.handle_request()
                        except Exception as e:
                            if on_error_callback:
                                on_error_callback(e)
            except Exception as e:
                if on_error_callback:
                    on_error_callback(e)
            finally:
                self.server_instance = None
        
        self.stop_event.clear()
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def stop_server(self):
        if self.server_instance:
            self.stop_event.set()
            self.server_instance = None
    
    def is_running(self):
        return self.server_thread and self.server_thread.is_alive()