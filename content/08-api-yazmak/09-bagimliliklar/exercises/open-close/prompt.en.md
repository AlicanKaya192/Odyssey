A rehearsal for a real database connection: the connection opens and closes
on every request, and the `events` list records what happened.

**What to do:**

1. `get_conn`: a `yield` dependency. First append `"open"` to `events`, give
   `"conn"`; when the endpoint is done, append `"close"` **even on an
   error**.
2. `GET /items` and `GET /items/{item_id}` (`404`, `"Item not found"`) use
   `get_conn`.
3. `GET /events` → `events` (uses no connection).

- `GET /items`, `GET /items/9` (`404`), `GET /events` → `["open", "close", "open", "close"]`
