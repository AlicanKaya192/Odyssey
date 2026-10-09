A token shouldn't be valid forever. If it's stolen, the thief can use it as
long as they like.

## Logging out

If the server forgets the token, the token becomes invalid:

```python
@app.post("/logout", status_code=204)
def logout(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    tokens.pop(cred.credentials, None)
```

After this, `GET /me` with the same token → `401 Invalid token`.

## A token that expires

Store the time the token was created next to it, and check its age when it's
used:

```python
import time

TOKEN_SECONDS = 3600
tokens = {}          # token -> {"user": ..., "created": ...}


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    info = tokens.get(cred.credentials)
    if info is None or time.time() - info["created"] > TOKEN_SECONDS:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return info["user"]
```

When the client gets a `401`, it logs in again.

## Tokens in memory

The `tokens` dictionary in this section lives in the server's memory: if the
server restarts, everyone is logged out. A real application keeps tokens in
a database, or uses signed tokens the server doesn't store, like JWT.

## The client side (from the Using APIs module)

```python
r = requests.post(f"{BASE}/token", json={"username": "ada", "password": "..."})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
requests.get(f"{BASE}/me", headers=headers)
```

On the `/docs` page, pasting the token into the **Authorize** button makes
the page add this header to every request too.
