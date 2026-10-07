The ways to send an identity, in one table.

| Method | How it is sent | requests | Note |
|---|---|---|---|
| API key (header) | `X-API-Key: abc123` | `headers={"X-API-Key": key}` | The header name depends on the API |
| API key (query) | `?api_key=abc123` | `params={"api_key": key}` | The address ends up in logs; only if you must |
| Bearer token | `Authorization: Bearer abc123` | `headers={"Authorization": "Bearer " + token}` | Do not forget the `Bearer ` prefix |
| Basic | `Authorization: Basic <base64>` | `auth=(user, password)` | Only with `https` |

## What to do for each code

| Code | Meaning | What to do |
|---|---|---|
| `401` | Not recognised | Was the key/token sent? In the right header? Has it expired? |
| `403` | Not allowed | Another permission or key is needed; retrying does not help |

## The session pattern

```python
import os
import requests

BASE = "http://api.odyssey.test"
token = os.environ.get("LIBRARY_TOKEN", "letmein")

session = requests.Session()
session.headers.update({"Authorization": "Bearer " + token})

me = session.get(BASE + "/me")
me.raise_for_status()
print(me.json())
```

## Security checklist

- Keys and tokens are not written into the code; they are read from an
  environment variable or a `.env` file.
- The `.env` file is added to `.gitignore`.
- A leaked key is revoked at once in the API's dashboard and replaced;
  deleting it from the history is not enough.
- Hide the headers when you share screenshots or error logs.
- Give a key only the permissions it needs (read-only, for example).
