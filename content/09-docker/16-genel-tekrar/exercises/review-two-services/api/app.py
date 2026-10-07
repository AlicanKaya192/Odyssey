import json
import os
import signal
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_PATH = os.environ.get("DB_PATH", "notes.db")
PORT = int(os.environ.get("PORT", "8000"))


def query(sql, params=()):
    db = sqlite3.connect(DB_PATH)
    try:
        with db:
            cursor = db.execute(sql, params)
            return cursor.fetchall(), cursor.lastrowid
    finally:
        db.close()


def setup():
    query(
        "CREATE TABLE IF NOT EXISTS notes "
        "(id INTEGER PRIMARY KEY, text TEXT NOT NULL)"
    )
    query("CREATE TABLE IF NOT EXISTS starts (id INTEGER PRIMARY KEY)")
    query("INSERT INTO starts DEFAULT VALUES")


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
        elif self.path == "/notes":
            rows, _ = query("SELECT id, text FROM notes ORDER BY id")
            self.send_json(200, [{"id": i, "text": t} for i, t in rows])
        elif self.path == "/stats":
            notes, _ = query("SELECT COUNT(*) FROM notes")
            starts, _ = query("SELECT COUNT(*) FROM starts")
            self.send_json(200, {"notes": notes[0][0], "starts": starts[0][0]})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/notes":
            self.send_json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or b"{}")
        text = str(data.get("text", "")).strip()
        if not text:
            self.send_json(400, {"error": "text is required"})
            return
        _, new_id = query("INSERT INTO notes (text) VALUES (?)", (text,))
        self.send_json(201, {"id": new_id, "text": text})

    def log_message(self, fmt, *args):
        if self.path != "/health":
            print(self.command, self.path, args[1], flush=True)


def stop(signum, frame):
    print("shutting down", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop)
    setup()
    print(f"listening on port {PORT}, database {DB_PATH}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
