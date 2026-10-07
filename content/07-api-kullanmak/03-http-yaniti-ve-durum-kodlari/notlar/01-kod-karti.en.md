To recall status codes quickly.

## Classes

| Class | Meaning | Whose job |
|---|---|---|
| `1xx` | Information: "carry on" | You rarely see these |
| `2xx` | Success | Use the body |
| `3xx` | Redirect: look elsewhere | The library follows it for you |
| `4xx` | Client error | **Yours**: fix the request |
| `5xx` | Server error | **Theirs**: wait and try again |

## Ten everyday codes

- `200` OK · `201` created · `204` OK but no body
- `400` broken request · `401` not recognised · `403` not allowed · `404` not there
- `429` slow down · `500` server error · `503` not available right now

## A one-sentence rule

> If it starts with 4, look at your request; if it starts with 5, wait.

The exception is `429`: it starts with four, but the request is fine; it is
just sent too often. You wait for `Retry-After` and send the same request.

## Python

```python
from http import HTTPStatus

HTTPStatus(404).phrase     # 'Not Found'
404 // 100                 # 4 -> the class
200 <= code < 300          # did it succeed?
```
