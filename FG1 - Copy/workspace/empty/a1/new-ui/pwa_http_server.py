# Improved HTTP Server for PWA
import http.server
import socketserver
import os
import sys

PORT = 8080
# Serve from the new React-based html/ folder at the project root
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'html')

class PWAHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()    
    def do_GET(self):
        # Print for debugging
        print(f"Request path: {self.path}")
        # Always serve service worker and manifest from root
        if self.path == '/sw.js':
            self.path = '/sw.js'
            print(f"Serving service worker from: {os.path.join(DIRECTORY, 'sw.js')}")
        elif self.path == '/manifest.json':
            self.path = '/manifest.json'
            print(f"Serving manifest from: {os.path.join(DIRECTORY, 'manifest.json')}")
        elif self.path == '/offline.html':
            self.path = '/offline.html'
        elif self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

with socketserver.TCPServer(("", PORT), PWAHTTPRequestHandler) as httpd:
    print(f"Serving PWA at port {PORT} from directory: {DIRECTORY}")
    httpd.serve_forever()
