A short path to the question "which code should I return?" while writing an
endpoint.

## Success

| Situation | Code | Body |
|---|---|---|
| I read it, here is the result | `200` | Yes |
| I created a new record | `201` | The new record (+ a `Location` header) |
| I got the request and will process it later | `202` | Brief info (`{"queued": true}`) |
| Done, nothing to say | `204` | **None** |

## The client's mistake (4xx)

| Situation | Code |
|---|---|
| The body/parameters don't fit the template | `422` (FastAPI gives it) |
| It fits but makes no sense (selling what's out of stock) | `400` |
| You didn't say who you are (no key) | `401` |
| I know who you are, but you're not allowed | `403` |
| No such record | `404` |
| This method doesn't exist at this address | `405` (FastAPI gives it) |
| A clash: this name is already taken | `409` |
| Too many requests | `429` |

## The server's mistake (5xx)

You don't choose `500`; it comes from an uncaught error in your code or a
return value that doesn't fit the response model. It tells the client "the
problem is with me, not you".

## The order of decisions

1. Didn't the template fit? → FastAPI `422`.
2. An identity/permission problem? → `401` / `403`.
3. No such record? → `404`.
4. Does it clash with an existing one? → `409`.
5. Was some other business rule broken? → `400`.
6. Was something new created? → `201`; deleted? → `204`; otherwise `200`.

## By name

After `from fastapi import status`: `status.HTTP_200_OK`,
`status.HTTP_201_CREATED`, `status.HTTP_204_NO_CONTENT`,
`status.HTTP_404_NOT_FOUND`, `status.HTTP_409_CONFLICT`. The same result as
writing the number; clearer for the reader.
