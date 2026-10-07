On the Docker track we checked a container's health at the `/health`
address. Now you write that address.

**What to do:** keep the existing `GET /`; add `GET /health` next to it:

```json
{"status": "ok"}
```
