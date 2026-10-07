An order you can follow when starting Postman (or Bruno) for the first time.

## The first request

1. Open the application; create a new request (**New → HTTP Request**).
2. Choose the method (`GET`) and write the address: a sample address of a
   public API.
3. Press **Send**. The status code, time, size and body appear in the panel
   below.
4. Look at the response headers in the **Headers** tab: `Content-Type`, rate
   limit headers...

## Parameters, headers, body

- **Params** tab: you write the query parameters as a table; the address
  updates itself.
- **Headers** tab: headers such as `Accept` and `X-API-Key`.
- **Authorization** tab: choose the type (Bearer Token, Basic Auth, API Key);
  Postman builds the right header itself.
- **Body → raw → JSON**: the body of a `POST` / `PATCH`.

## Environment variables

1. Under **Environments** create a new environment: `base_url`, `token`.
2. In the requests write `{{base_url}}/books` and `Bearer {{token}}`.
3. Keep two environments for the test and live servers; switch by choosing
   one at the top right.

That way the key lives in the environment, not inside the requests; when you
share the collection you do not share the key.

## Collections

- Gather related requests in a collection ("Library API").
- Organise them in folders: Books, Authors.
- **Export** it as JSON; share it with the team or put it under version
  control (keep the keys in the environment).

## From a request to code

The **Code** (`</>`) button on the right of a working request turns it into
curl or Python requests code. Try it in the tool first, then take the code
from there once it works: the most efficient way of working with an API.
