Add the image's own health check. The check is ready in `healthcheck.py`.

**What to do:**

1. Copy `healthcheck.py` into the image too (right now only `app.py` is copied).
2. After `USER`, add a `HEALTHCHECK`: every 5 seconds, a 3-second timeout,
   3 retries; the command `python healthcheck.py` in exec form.

Odyssey will start the service with `compose.yaml` and wait for the state to
become `healthy`.
