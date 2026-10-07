**What to do:** `POST /users` takes a person and says whether they are an
adult (18 or over).

- `{"name": "Ada", "age": 36}` → `{"name": "Ada", "age": 36, "adult": true}`
- `{"name": "Tim", "age": "12"}` → `{"name": "Tim", "age": 12, "adult": false}`
- `{"name": "Bo"}` → `422`
- `{"name": "Bo", "age": "old"}` → `422`
