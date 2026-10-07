A review of Sections 03, 06 and 11: a function that sends a request to an
address and says in a word what happened.

**What to do:** write the function `diagnose(path)`. It sends a request with
`timeout=1` and returns one of:

| Situation | Return |
|---|---|
| `requests.Timeout` | `"too slow"` |
| `2xx` | `"ok"` |
| `401` or `403` | `"need permission"` |
| `404` | `"not found"` |
| `5xx` | `"server error"` |
| anything else | `"other"` |

Then print each address in the `paths` list with its diagnosis.

**Expected output:**

```
/books/1 -> ok
/books/0 -> not found
/stats -> need permission
/broken -> server error
/slow -> too slow
/me -> need permission
```
