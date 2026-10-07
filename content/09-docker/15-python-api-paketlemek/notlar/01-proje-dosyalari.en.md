All the files of the notes API from the lesson. You can copy them into
a folder and run them with `docker compose up -d --build`; the address
is `localhost:8095`.

## app.py

The API itself. Standard library only.

```python
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
```

## healthcheck.py

The check `HEALTHCHECK` runs. Exit code 0 = healthy.

```python
import os
import sys
import urllib.request

PORT = os.environ.get("PORT", "8000")

try:
    urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=2)
except OSError:
    sys.exit(1)
```

## requirements.txt

Empty for now; when a package is needed, a `package==version` line goes here.

```text
# No third-party packages yet; add them here when you need them.
```

## Dockerfile

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/notes.db \
    PORT=8000

RUN useradd --create-home --uid 1000 app \
 && mkdir /data \
 && chown app:app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py healthcheck.py ./

USER app
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "healthcheck.py"]
CMD ["python", "app.py"]
```

## .dockerignore

```text
.git
.env
**/__pycache__
*.db
```

## compose.yaml

```yaml
services:
  web:
    build: .
    ports:
      - "8095:8000"
    env_file: .env
    volumes:
      - notes-data:/data
    restart: unless-stopped

volumes:
  notes-data:
```

## .env

Not added to the repository (`.gitignore`); a `.env.example` with fake values goes there instead.

```text
DB_PATH=/data/notes.db
PORT=8000
```

## Trying it

```text
docker compose up -d --build
docker compose ps                         # wait until it is (healthy)
curl localhost:8095/health
curl -X POST localhost:8095/notes -d @note.json
curl localhost:8095/notes
docker compose down                       # the data stays in the volume
docker compose down -v                    # also removes the volume
```

`note.json`: `{"text": "buy milk"}`. In PowerShell write `curl.exe`.
