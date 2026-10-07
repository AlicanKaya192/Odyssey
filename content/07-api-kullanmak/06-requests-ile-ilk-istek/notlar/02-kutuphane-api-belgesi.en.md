The documentation of this path's practice server. As with any API, you can
look here before starting an exercise. The base address:

```text
http://api.odyssey.test
```

## Books

| Request | What it does |
|---|---|
| `GET /books` | The list of books (paged, 5 at a time) |
| `GET /books/<id>` | One book; `404` if missing |
| `POST /books` | A new book (token required) → `201` |
| `PUT /books/<id>` | Replace the book completely (token) |
| `PATCH /books/<id>` | Change some of the book's fields (token) |
| `DELETE /books/<id>` | Delete the book (token) → `204` |

`GET /books` query parameters: `author`, `tag`, `year_min`, `year_max`, `q`
(a word in the title), `sort` (`title`, `year`, `price`; with a leading `-`
for largest first), `page`, `per_page` (at most 20).

A list response:

```json
{"data": [...], "meta": {"page": 1, "per_page": 5, "total": 23, "pages": 5},
 "links": {"next": "/books?page=2", "prev": null}}
```

A book:

```json
{"id": 1, "title": "Emma", "author_id": 1, "year": 1815, "price": 12.5,
 "tags": ["classic", "novel"], "updated": "2024-01-10",
 "author": {"id": 1, "name": "Austen", "country": "UK"}}
```

## Authors

| Request | What it does |
|---|---|
| `GET /authors` | All authors |
| `GET /authors/<id>` | One author |
| `GET /authors/<id>/books` | That author's books |

## Identity

| Where | Value | Needed for |
|---|---|---|
| `Authorization: Bearer letmein` | A token | Adding, changing, deleting books; `/me` |
| `X-API-Key: demo-key-123` | A reader key | `/stats` |
| `X-API-Key: admin-key-999` | An admin key | `/admin/report` |
| Basic: `reader` / `pass123` | User name and password | `/basic` |

These values are only for the practice server; in Section 08 you will see
why the key of a real API is never written into the code.

## Other endpoints

| Request | What it does |
|---|---|
| `GET /status` | The plain text `ok` |
| `GET /offset/books` | Paging with `offset` + `limit` |
| `GET /cursor/books` | Paging with a cursor |
| `GET /flaky` | `503` for the first two requests, then `200` |
| `GET /broken` | Always `500` |
| `GET /slow` | Answers after 3 seconds |
| `GET /limited` | 3 requests per second; `429` for more |
| `GET /changes?since=2024-03-01` | Books changed on or after that date |
| `GET /openapi.json` | A machine-readable description of this API |

The server starts from scratch on every run: books you add or delete are back
to how they were on the next run.
