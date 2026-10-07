`PUT` and `PATCH` both mean "change"; the difference is in what is sent.

| | `PUT` | `PATCH` |
|---|---|---|
| Body | The **whole** record | Only the changed fields |
| Model | With required fields (`BookIn`) | All optional (`BookPatch`) |
| Missing field | `422` | Left alone |
| In code | `books[id] = {...}` | `record.update(patch.model_dump(exclude_unset=True))` |

## Sending the same request twice

Even if `PUT /books/2 {"title": "Persuasion", "year": 1817}` is sent twice,
the result is the same: the record ends up in that state. This is called
**idempotent** (safe to repeat). `GET`, `PUT` and `DELETE` are like this: if
the network drops and the client sends the request again, no harm is done.
(`DELETE` returns `404` the second time, but the record is still deleted.)

`POST` isn't: a `POST /books` sent twice creates two books. That's where
the retry rule from API 1 comes from: don't blindly repeat a `POST`.

## `exclude_unset`, `exclude_none`, `exclude_defaults`

| Sent | `exclude_unset=True` | `exclude_none=True` |
|---|---|---|
| `{"year": 1966}` | `{"year": 1966}` | `{"year": 1966}` |
| `{"title": null}` | `{"title": None}` | `{}` |
| `{}` | `{}` | `{}` |

`exclude_unset` keeps a `null` the client sent on purpose; `exclude_none`
drops it. The right one for `PATCH` is `exclude_unset`. If a field can't be
`null` (like `title`), turn a sent `null` into a `422` with a validator (see
the lesson); a rule (`min_length=1`) isn't applied to `None` and doesn't
stop it.

## `PATCH` with an empty body

`PATCH /books/1 {}` → nothing changes, the record comes back as it is
(`200`). If you want an error: `if not changes: raise HTTPException(400, ...)`.
