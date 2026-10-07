An endpoint can return not only a dictionary but also a list; FastAPI turns
it into a JSON array.

**What to do:** `GET /colors` returns this array:

```json
["red", "green", "blue"]
```
