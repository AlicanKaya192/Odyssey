HTTP methods and their properties in one table.

| Method | Job | Body | Safe | Idempotent |
|---|---|---|---|---|
| `GET` | Get it | No | Yes | Yes |
| `HEAD` | Get only the headers | No | Yes | Yes |
| `OPTIONS` | Which methods can be used? | No | Yes | Yes |
| `POST` | Create something new | Yes | No | **No** |
| `PUT` | Replace completely | Yes | No | Yes |
| `PATCH` | Change part of it | Yes | No | Usually no |
| `DELETE` | Delete | Usually no | No | Yes |

## Do not mix up the two words

- **Safe:** changes nothing on the server. Reading is safe.
- **Idempotent:** the result is the same whether it is sent once or ten
  times. `DELETE` is not safe (it deletes) but it is idempotent (deleting a
  second time changes nothing).

## What this means in practice

The connection dropped and no response came. You do not know whether the
request reached the server.

- `GET`, `PUT`, `DELETE` → send it again; at worst the same thing happens
  once more.
- `POST` → stop before sending it again. The order may be created twice. If
  the API offers a solution for this (for example, a single-use identifier on
  every request), its documentation says so.

## PUT or PATCH?

Record: `{"title": "Emma", "author": "Austen", "price": 12}`

- `PATCH /books/42` with body `{"price": 10}` → only the price changes.
- `PUT /books/42` with body `{"price": 10}` → the record is replaced by a
  record **made only of the price**; the title and author may be lost.

Use `PATCH` for a partial change; use `PUT` when you send the whole record.
