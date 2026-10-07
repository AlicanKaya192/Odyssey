`api.py` is an API; find which port it listens on in the last line of the
file.

**What to do:** write the Dockerfile that runs this API: `python:3.13-slim`,
working folder `/app`, copy `api.py`, **document the port it listens on with
`EXPOSE`**, and run `python api.py`.

Odyssey will send two requests: `/health` → `200` and `{"status": "ok"}`,
`/missing` → `404`.
