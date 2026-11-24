"""Buybox-ab localhost preview server: /off|on/<lang>/products/<handle> serves the built page (Loop needs
the product handle as the last path part), /cart.js an empty cart, the rest from the serve dir.
Usage: python3 -I server.py <serve-dir> <port>"""
import json
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

SERVE, PORT = sys.argv[1], int(sys.argv[2])
EMPTY_CART = json.dumps({'token': 'preview', 'items': [], 'attributes': {}, 'item_count': 0, 'total_price': 0}).encode()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path.endswith('/cart.js') or path.endswith('/cart.json'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(EMPTY_CART)
            return
        parts = path.strip('/').split('/')
        if len(parts) == 4 and parts[0] in ('on', 'off', 'live', 'copy') and parts[2] == 'products' and '.' not in parts[3]:
            self.path = '/' + '/'.join(parts) + '.html'
        return super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *args):
        pass


ThreadingHTTPServer(('127.0.0.1', PORT), partial(Handler, directory=SERVE)).serve_forever()
