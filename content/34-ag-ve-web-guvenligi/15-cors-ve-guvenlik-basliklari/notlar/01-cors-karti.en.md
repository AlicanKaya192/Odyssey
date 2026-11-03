## CORS headers

| Header | Who sends it | What it says |
|---|---|---|
| `Origin` | Browser | The origin the request comes from |
| `Access-Control-Allow-Origin` | Server | The origin allowed to read (one origin or `*`) |
| `Access-Control-Allow-Credentials` | Server | `true`: a request with cookies may be read (not with `*`) |
| `Access-Control-Allow-Methods` | Server (preflight) | Allowed methods |
| `Access-Control-Allow-Headers` | Server (preflight) | Allowed request headers |
| `Access-Control-Max-Age` | Server (preflight) | How many seconds the preflight response is kept |
| `Vary: Origin` | Server | The response changes per origin; caches must not mix them up |

## Common mistakes

- Writing the incoming `Origin` back as it is (especially with
  `Allow-Credentials: true`).
- Checking the origin with `endswith`, `startswith` or `in`: names such
  as `notshop.example` or `shop.example.other.example` get through.
- Allowing the `null` origin.
- Allowing an `http://` origin: someone on the path can change that
  origin's page.
- Not sending `Vary: Origin`.
- Taking CORS for access control: CORS only governs reading by **a script
  in the browser**. A program that sends requests to the server directly
  is never stopped by CORS; authorization is still done on the server.

## The right order

```text
1. Is Origin on the allow list?  (exact equality, a set)
2. Yes: Allow-Origin = that origin, Allow-Credentials: true if needed
3. In every case: Vary: Origin
4. In a preflight: only the methods and headers needed
```
