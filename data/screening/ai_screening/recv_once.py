"""Receive one PDF POSTed from the browser tab and save it; bound to 127.0.0.1, exits after one valid upload or 300 s.
Usage: python -P recv_once.py <out.pdf> [port]"""
import sys, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
OUT, PORT = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8765
class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*'); self.send_header('Access-Control-Allow-Private-Network', 'true')
    def do_OPTIONS(self): self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        ok = body[:5] == b'%PDF-'
        if ok: open(OUT, 'wb').write(body)
        self.send_response(200 if ok else 400); self.cors(); self.end_headers(); self.wfile.write(b'saved' if ok else b'not a pdf')
        print('received', len(body), 'bytes, pdf' if ok else 'bytes, NOT a pdf', flush=True)
        if ok: threading.Thread(target=self.server.shutdown).start()
    def log_message(self, *a): pass
srv = HTTPServer(('127.0.0.1', PORT), H)
threading.Timer(300, srv.shutdown).start()
srv.serve_forever(); print('stopped')
