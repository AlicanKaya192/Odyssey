You have the address of an API request. Take it apart with `urlparse`.

**What to do:**

1. Import `urlparse` from the `urllib.parse` module.
2. Take `url` apart.
3. Print the scheme, host, port, path, query string and fragment in the
   format below.

**Expected output:**

```
scheme: https
host: api.weather.test
port: 9000
path: /v2/forecast
query: city=Izmir&days=3
fragment: top
```

Use `.hostname` for the host: `.netloc` includes the port too
(`api.weather.test:9000`).
