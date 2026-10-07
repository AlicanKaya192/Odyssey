The program should listen on port **9000** instead of 8000 inside the
container. Do not touch `app.py` or the Dockerfile; the program reads the port
from the `PORT` environment variable.

**What to do:**

1. Set `PORT` to 9000 in `.env`.
2. In `compose.yaml`, send the computer's 8095 to the container's **9000**.

The health check also reads the port from `PORT`, so you do not need to touch
it. Odyssey will wait for the service to become `healthy` and look at
`/health` on 9000:

```
{"status": "ok"}
```
