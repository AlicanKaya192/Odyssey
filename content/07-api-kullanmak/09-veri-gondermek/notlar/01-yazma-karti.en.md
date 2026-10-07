Every request that writes, with its expected codes.

| Job | Request | Body | Success code | Response body |
|---|---|---|---|---|
| Create | `POST /books` | The new record | `201` | The final record + `Location` |
| Change part | `PATCH /books/<id>` | Only the changed fields | `200` | The final record |
| Replace | `PUT /books/<id>` | The whole record | `200` | The final record |
| Delete | `DELETE /books/<id>` | None | `204` | Empty |

## requests

```python
r = requests.post(url, json=data, headers=AUTH)
r = requests.patch(url, json={"price": 8.99}, headers=AUTH)
r = requests.put(url, json=whole_record, headers=AUTH)
r = requests.delete(url, headers=AUTH)
```

## `json=` or `data=`?

| | `json=` | `data=` |
|---|---|---|
| Body | JSON text | `name=value&...` |
| `Content-Type` | `application/json` | `application/x-www-form-urlencoded` |
| When | The API wants JSON (most do) | Older APIs that expect a web form |

## Error codes

| Code | Meaning | Look at |
|---|---|---|
| `400` | The body cannot be read | Is the JSON broken; did you use `json=`? |
| `401` | No / invalid token | The `Authorization` header |
| `403` | No permission for this operation | The token's permissions |
| `404` | No such record | The identifier in the address |
| `405` | This method does not exist here | The `Allow` header; list or single record? |
| `409` | A conflict (the record already exists) | Check whether it exists first |
| `422` | The values break the rules | The `detail` in the body |

## Watch out

- Do not call `r.json()` on a `204` response; the body is empty.
- Do not repeat a `POST` automatically: duplicate records appear.
- Do not send only one field with `PUT`: the other fields may be lost.
