**What to do:** two endpoints that use the `state` dictionary:

1. `GET /counter` reads the counter: `{"count": 0}`.
2. `POST /counter` increases it by 1 and returns the new state.

Odyssey will send `GET`, `POST`, `POST`, `GET` in order:

```text
GET  /counter   {"count": 0}
POST /counter   {"count": 1}
POST /counter   {"count": 2}
GET  /counter   {"count": 2}
```
