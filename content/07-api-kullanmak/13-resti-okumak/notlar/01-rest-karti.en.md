Keep this at hand when reading or designing a REST API.

## Address patterns

| Pattern | Example | Meaning |
|---|---|---|
| `/resources` | `/books` | A collection |
| `/resources/<id>` | `/books/42` | A single item |
| `/resources/<id>/sub-resources` | `/authors/6/books` | A related collection |
| `/resources?filter=...` | `/books?author=Austen` | A filtered collection |
| `/v2/resources` | `/v2/books` | A version |

## Method × address

| | Collection `/books` | Item `/books/42` |
|---|---|---|
| `GET` | List (200) | Fetch (200 / 404) |
| `POST` | Create (201) | Usually 405 |
| `PUT` | Usually 405 | Replace (200) |
| `PATCH` | Usually 405 | Change part (200) |
| `DELETE` | Rarely (delete all) | Delete (204) |

## Naming

- Plural nouns: `/books`, `/authors` (not the singular `/book`).
- Lower case, hyphens between words: `/reading-lists`.
- No verbs: not `/books/42/delete`, but `DELETE /books/42`.
- No file extensions: not `/books.json`; the `Accept` header gives the format.

## Questions to ask

When judging an endpoint, ask:

1. Is there a verb in the address?
2. Does the method describe the job correctly? (Does a `GET` change
   something?)
3. Are the success and error codes meaningful? (Does it return `200` for an
   error?)
4. Is filtering in the query or in a new address?
5. Does the request stand on its own? (Is the identity on every request?)
