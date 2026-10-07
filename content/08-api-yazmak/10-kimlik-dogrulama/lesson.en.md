# Authentication

Until now anyone who knew the address could call every endpoint you wrote.
In a real API some jobs must be open only to **certain people**: reading
your own notes, deleting a record, an admin page. In this section you
answer two questions:

- **Authentication**: *Who are you?* If I don't know, `401`.
- **Authorization**: *Are you allowed to do this?* If not, `403`.

In API 1 you sent keys and tokens as a client; now you write the side that
**checks** them.

## 1. An API key

The simplest way: you give each client a secret key, and the client sends
it in a header with every request.

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
KEYS = {"k-123": "ada"}


def require_api_key(key: Annotated[str | None, Depends(api_key_header)]):
    if key not in KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return KEYS[key]


@app.get("/reports")
def reports(owner: Annotated[str, Depends(require_api_key)]):
    return {"owner": owner}
```

- `APIKeyHeader(name="X-API-Key")`: a ready-made dependency that reads the
  header. It does the same job as `Header()` from the previous section; the
  difference is that it tells `/docs` "this API needs a key" (an
  **Authorize** button appears on the page).
- `auto_error=False`: give `None` if the header is missing, so we write the
  error message ourselves.

```text
GET /reports                      401 {"detail": "Invalid API key"}
GET /reports  (X-API-Key: k-123)  200 {"owner": "ada"}
```

Don't put the key in the **query** (`?key=k-123`): addresses get written to
server logs and browser history. A header is safer.

## 2. Passwords: never stored as they are

If people log in with a username and password, the server has to keep the
password somewhere. **Not as plain text**: if the database leaks one day,
every password goes with it (people reuse passwords elsewhere).

Instead you store the password's **hash**: a transformation that can't be
reversed. At login, the incoming password is hashed and compared with the
stored hash.

```python
import hashlib
import hmac


def hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000).hex()


SALT = b"fixed-salt-for-demo"
users = {"ada": {"hash": hash_password("lovelace", SALT)}}


def check_password(username: str, password: str) -> bool:
    user = users.get(username)
    if user is None:
        return False
    return hmac.compare_digest(user["hash"], hash_password(password, SALT))
```

- `pbkdf2_hmac(..., 100_000)`: computes the hash **slowly on purpose**
  (100,000 rounds). Unnoticeable for someone who knows the password; very
  slow for an attacker trying millions. The result is a 64-character string.
- **Salt**: random bytes added to the password before hashing. Two users
  with the same password get different hashes. In reality every user gets
  their own salt (`secrets.token_bytes(16)`), stored next to the hash; here
  one salt keeps things short.
- `hmac.compare_digest`: when comparing two strings, its time doesn't depend
  on where they differ; an attacker can't measure the time to get hints.

Real projects use libraries like `bcrypt` or `argon2` for this; the idea is
the same.

## 3. A token: log in once, then the token

Sending the password with every request isn't good. Instead, the client
logs in **once** and gets a **token** in return; it sends the token in later
requests.

```python
import secrets
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

bearer = HTTPBearer()
tokens = {}


class Login(BaseModel):
    username: str
    password: str


@app.post("/token")
def login(form: Login):
    if not check_password(form.username, form.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = secrets.token_hex(16)
    tokens[token] = form.username
    return {"access_token": token, "token_type": "bearer"}


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    if cred.credentials not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[cred.credentials]


@app.get("/me")
def me(user: Annotated[str, Depends(current_user)]):
    return {"user": user}
```

- `secrets.token_hex(16)`: an unpredictable random 32-character string. The
  `random` module is **not** used for this; it's predictable.
- `HTTPBearer()`: a ready-made dependency that reads the
  `Authorization: Bearer <token>` header. `cred.credentials` is the token
  itself.
- The `tokens` dictionary keeps which token belongs to whom.

<figure class="fig">
  <div class="flow">
    <span class="node">POST /token<br><small>username + password</small></span><span class="arrow">→</span>
    <span class="node acc">token<br><small>301f1864…</small></span><span class="arrow">→</span>
    <span class="node">GET /me<br><small>Authorization: Bearer 301f…</small></span><span class="arrow">→</span>
    <span class="node ok">{"user": "ada"}</span>
  </div>
  <figcaption>The password travels only once; every later request uses the token. The server finds whose token it is in the <code>tokens</code> dictionary.</figcaption>
</figure>

The flow we measured:

```text
POST /token {"username": "ada", "password": "nope"}      401
POST /token {"username": "ada", "password": "lovelace"}  200
            {"access_token": "301f1864...", "token_type": "bearer"}
GET /me  (no header)                   401 {"detail": "Not authenticated"}
GET /me  (Authorization: Bearer zzz)   401 {"detail": "Invalid token"}
GET /me  (Authorization: Bearer 301f…) 200 {"user": "ada"}
```

If the header is missing entirely, `HTTPBearer` gives the `401` itself and
adds a `WWW-Authenticate: Bearer` header to the answer (we measured).

## 4. Permission: 403, not 401

Once you know who it is, checking permission is a separate dependency:

```python
roles = {"ada": "admin", "alan": "member"}


def require_admin(user: Annotated[str, Depends(current_user)]):
    if roles.get(user) != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
```

The chain `current_user` → `require_admin`: first who (`401`), then
permission (`403`). Now you see that the dependency chain from the previous
section is made exactly for this.

## Two more things you need to know

- **HTTPS.** The key, password and token travel in headers **as plain
  text**. On a real server the address must be `https://`; otherwise anyone
  in between can read them. The practice server on your computer
  (`127.0.0.1`) doesn't go out, so it's fine.
- **JWT.** Here the tokens live in the server's memory (`tokens`). Another
  common way is JWT: a token containing the username and an expiry time,
  **signed** by the server; the server checks the signature without storing
  anything. It needs a separate package (`PyJWT`); the logic is the same as
  in this section.

## Summary

- `401` I don't know who you are, `403` I know but you're not allowed.
- An API key in a header: `APIKeyHeader(name="X-API-Key")`.
- A password is never plain: a salted, slow hash (`pbkdf2_hmac`), compared
  with `hmac.compare_digest`.
- Login → a token with `secrets.token_hex` → `Authorization: Bearer` →
  `HTTPBearer` + a `current_user` dependency.
- Permission is a separate dependency, attached to `current_user`.
