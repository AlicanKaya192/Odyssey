Adding and `find_task` are ready.

**What to do:**

1. `TaskPatch`: `title` and `done` optional (default `None`); `title` at
   least 1 character; a `null` that is **sent** must be `422`.
2. `PATCH /tasks/{task_id}`: change only the sent fields, return the
   current task; `404` if missing.

- `POST /tasks` `{"title": "Read Dune"}` → id `1`
- `PATCH /tasks/1` `{"done": true}` → `{"title": "Read Dune", "done": true, "id": 1}`
- `PATCH /tasks/1` `{"title": "Read Emma"}` → `done` still `true`
- `PATCH /tasks/1` `{"title": null}` → `422`
- `PATCH /tasks/1` `{}` → the task unchanged
