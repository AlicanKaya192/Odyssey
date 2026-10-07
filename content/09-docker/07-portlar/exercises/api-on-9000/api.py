import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({"status": "ok"}).encode()
            self.send_response(200)
        else:
            body = json.dumps({"error": "not found"}).encode()
            self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print("listening on 0.0.0.0:9000", flush=True)
HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()
