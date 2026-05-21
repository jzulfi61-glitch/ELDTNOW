#!/usr/bin/env python3
"""
Static file server with Cache-Control: no-store headers.
Prevents browsers from caching stale module HTML/JS between updates.
"""
import http.server
import socketserver

PORT = 5000
BIND = "0.0.0.0"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}", flush=True)


with socketserver.TCPServer((BIND, PORT), NoCacheHandler) as httpd:
    httpd.allow_reuse_address = True
    print(f"Serving on http://{BIND}:{PORT} (Cache-Control: no-store)", flush=True)
    httpd.serve_forever()
