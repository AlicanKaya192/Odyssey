Publish `index.html` with a web server running in a container.

**What to do:**

1. Start from `python:3.13-slim`; the working folder is `/srv`.
2. Copy `index.html`.
3. Document port 8000 with `EXPOSE`.
4. Run `python -m http.server 8000` (exec form; four parts).

Odyssey will publish the container to a port and send a request to `/`;
`Odyssey Docs` should appear on the page. To try it yourself:
`docker run -d -p 8080:8000 site` and `localhost:8080` in the browser.
