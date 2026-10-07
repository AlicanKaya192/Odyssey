The library's website (`https://library.example.com`) will call the API from
the browser.

**What to do:** with `CORSMiddleware`, allow only this site, only for `GET`
(all headers allowed).

- `GET /books`, `Origin: https://library.example.com` → `access-control-allow-origin: https://library.example.com` in the answer
- an `OPTIONS /books` preflight from another site → `400`
