Write your first compose.yaml.

**What to do:** a single service called `web`:

1. It builds its image from the Dockerfile in this folder (`build`).
2. The computer's 8090 goes to the container's 8000 (`ports`; in quotes).
3. The `APP_ENV` environment variable is `production` (`environment`).

Odyssey will read the file, then really bring it up with `docker compose up`
and send a request to the page. To try it yourself, `docker compose up -d
--build` and `localhost:8090` in the browser.
