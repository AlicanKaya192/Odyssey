The exercises of this path use small servers written with Python's own
library, without installing extra packages. Knowing how they work makes it
easier to understand what is listening in the container.

## A file server

```text
python -m http.server 8000
```

It serves the files in its folder. If there is an `index.html`, that is the
home page. By default it listens on all addresses (`0.0.0.0`);
`--bind 127.0.0.1` makes it reachable only from inside.

## A small API that returns JSON

```python
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


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

- `("0.0.0.0", 8000)`: which address and port. Always `0.0.0.0` in a
  container.
- `do_GET`: the method that runs on every GET request; `self.path` is the
  requested path.
- `send_response`, `send_header`, `end_headers`, `wfile.write`: the status
  code, the headers and the body (the parts of a response you saw in the API
  path).

## In real projects

These small servers are enough for learning, but real applications use
frameworks:

| Framework | Running | Watch out in a container |
|---|---|---|
| FastAPI + uvicorn | `uvicorn main:app --host 0.0.0.0 --port 8000` | `--host 0.0.0.0` is required |
| Flask | `flask run --host 0.0.0.0` | Default 127.0.0.1 |
| Django | `python manage.py runserver 0.0.0.0:8000` | Default 127.0.0.1 |
| Streamlit | `streamlit run app.py --server.address 0.0.0.0` | |

In the API 2 path you will write your own API with FastAPI and put it into a
container with the methods of this path.
