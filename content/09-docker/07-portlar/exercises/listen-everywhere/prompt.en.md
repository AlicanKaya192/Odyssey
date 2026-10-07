This small API runs in a container and the port is published; but a request
from outside gets `Empty reply from server`.

**What to do:** fix the address the server listens on in `server.py`: inside
the container the program must listen on **all addresses**. (Update the
printed line with the same address too.)

Odyssey will send a request to `/health`; the reply must be
`{"status": "ok"}`.
