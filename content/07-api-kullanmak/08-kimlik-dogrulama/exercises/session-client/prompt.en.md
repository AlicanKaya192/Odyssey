Instead of writing the same headers on every request, set up a session.

**What to do:**

1. Open a session with `session = requests.Session()` and add three headers
   to `session.headers`:
   - `Authorization: Bearer letmein`
   - `X-API-Key: demo-key-123`
   - `User-Agent: library-cli/1.0`
2. Send three requests with the session: `/me`, `/stats`, `/books/2`. Print
   the address and the status code of each.
3. On the last line print the `User-Agent` header the third request sent
   (`r.request.headers`).

**Expected output:**

```
/me 200
/stats 200
/books/2 200
user agent: library-cli/1.0
```
