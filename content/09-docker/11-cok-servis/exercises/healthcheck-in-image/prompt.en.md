compose.yaml starts `web` once `api` is healthy, but `api` has no
healthcheck; Compose says: `container ... has no healthcheck configured`.

**What to do:** write the check not in compose.yaml but **in the API's
image** with the `HEALTHCHECK` instruction (`api/Dockerfile`): every 2
seconds, with a 3-second timeout, 15 tries; the command is the Python line in
the comment. You can split the long line with `\`.

Odyssey will bring the project up and look for `items: 3` in `web`'s log.
