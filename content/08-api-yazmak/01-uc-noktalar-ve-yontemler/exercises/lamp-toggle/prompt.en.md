A small API that controls a lamp.

**What to do:**

1. `GET /lamp` reads the state: `{"on": false}`.
2. `POST /lamp/toggle` flips the lamp (off if on, on if off) and returns the
   new state.

Python's `False` becomes `false` in JSON.

```text
GET  /lamp          {"on": false}
POST /lamp/toggle   {"on": true}
POST /lamp/toggle   {"on": false}
```
