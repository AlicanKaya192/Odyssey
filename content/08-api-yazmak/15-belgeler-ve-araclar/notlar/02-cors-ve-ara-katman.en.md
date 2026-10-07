## `CORSMiddleware` settings

| Setting | Meaning |
|---|---|
| `allow_origins=["https://site.com"]` | Which sites' pages may call it |
| `allow_methods=["GET", "POST"]` | Which methods are allowed |
| `allow_headers=["*"]` | Which headers may be sent (like `Authorization`) |
| `allow_credentials=True` | Requests with cookies/credentials; then `allow_origins` can't be `*` |

An **origin** = scheme + name + port: `https://library.example.com` and
`http://library.example.com` are different origins; so are
`http://127.0.0.1:8000` and `http://127.0.0.1:5173`.

## The preflight

Before "non-simple" requests like `POST` + JSON, the browser sends an
`OPTIONS` to the same address: "may I come with this method and these
headers?" We measured: `200` and `access-control-allow-methods: GET, POST`
for an allowed origin, `400 Disallowed CORS origin` for a disallowed one. If
the preflight fails, the browser never sends the real request.

## When you see a CORS error

If the browser's developer console says "blocked by CORS policy":

1. Is the page's origin in `allow_origins` (including the port)?
2. Is the method in `allow_methods`?
3. Is the header being sent (`Authorization`) in `allow_headers`?

## The order of middleware

```python
@app.middleware("http")
async def mw(request, call_next):
    # 1) before the request goes to the endpoint
    response = await call_next(request)
    # 2) before the answer goes to the client
    return response
```

With several middlewares, the one added last runs outermost: it sees the
request first and the answer last. Exception handlers and dependencies run
**inside** the middleware.

## Middleware or a dependency?

| Job | The right one |
|---|---|
| Adding a header to every answer, timing | Middleware |
| A key check on some endpoints | A dependency |
| Finding the user and handing it to the endpoint | A dependency |
