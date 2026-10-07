Combine the `ENTRYPOINT` + `CMD` setup from the previous section with the
port: `docker run site` should run on 8000, `docker run site 9000` on 9000.

**What to do:**

1. With `ENTRYPOINT`, `python -m http.server` should always run.
2. With `CMD`, the default argument should be `8000`.

Odyssey will run the container twice: with no argument (8000) and with the
argument `9000` (9000); the page must come in both.
