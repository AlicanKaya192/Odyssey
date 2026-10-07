This time the client in `web` sends **a single request** and ends: if the API
is not ready, it fails. The API prepares for two seconds when it starts.

**What to do:** write compose.yaml:

1. `api`: image from `./api`; a healthcheck:
   `test` = `["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000')"]`,
   `interval: 2s`, `timeout: 3s`, `retries: 15`.
2. `web`: image from `./web`; it starts once `api` is **healthy**
   (`depends_on` + `condition: service_healthy`).

Odyssey will bring the project up and look for `items: 3` in `web`'s log.
