import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

time.sleep(2)  # preparing


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"items": 3}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print("api ready", flush=True)
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
