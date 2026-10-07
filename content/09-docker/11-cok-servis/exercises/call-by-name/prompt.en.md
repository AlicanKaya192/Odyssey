The client in the `web` service cannot reach the API; its log keeps saying
`waiting for the API: ... Connection refused`.

**What to do:** fix `API_URL` in `web/client.py`. `localhost` is `web`
itself; the API is the service called `api`, listening on 8000.

Odyssey will bring the project up and wait for the line `items: 3` in
`web`'s log.
