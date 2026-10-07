**What to do:** write a middleware that adds two headers to **every**
answer:

- `X-Process-Time`: the time taken to process the request (seconds, 4
  decimals)
- `X-App-Version`: `2.0.0`

Don't touch the endpoints; even the `404` answer of a missing address must
have the headers.
