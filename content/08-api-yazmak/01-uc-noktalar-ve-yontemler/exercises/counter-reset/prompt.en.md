**What to do:** add a `DELETE /counter` to the counter: it sets the counter
to `0` and returns the new state.

Odyssey increases twice, then deletes:

```text
POST   /counter   {"count": 1}
POST   /counter   {"count": 2}
DELETE /counter   {"count": 0}
GET    /counter   {"count": 0}
```
