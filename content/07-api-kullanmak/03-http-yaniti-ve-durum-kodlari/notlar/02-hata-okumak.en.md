The order to look at things in when an error response arrives, with examples.

## The order

1. **Status code:** which class? `4xx` or `5xx`?
2. **Body:** did the API write the reason? (fields such as `error`,
   `detail`, `message`)
3. **Headers:** is there a `Retry-After`? A `Location`?
4. **Your own request:** do the address, method, headers and body match the
   documentation?

## Example 1

```text
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"error": "missing api key"}
```

No key was sent. Check the documentation for which header the key goes in
(Section 08).

## Example 2

```text
HTTP/1.1 404 Not Found
Content-Type: application/json

{"error": "book 9999 not found"}
```

The address is right, the record does not exist. Check where you got the
identifier (9999) from.

## Example 3

```text
HTTP/1.1 405 Method Not Allowed
Allow: GET, POST
```

The method you used is not valid at this address. The `Allow` header lists
the valid ones: perhaps `POST` was needed instead of `PUT`.

## Example 4

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

The request is fine, just too frequent. Wait 30 seconds and send the same
one.

## Example 5

```text
HTTP/1.1 503 Service Unavailable
Retry-After: 120

{"error": "maintenance"}
```

The server is under maintenance. There is nothing for you to fix; try again
in two minutes.

## Don't

- Do not treat the body of an error response as data and carry on. Code
  first.
- Do not resend a request that got a `4xx` unchanged in a loop; you will get
  the same error every time and the server may stop you with a `429`.
