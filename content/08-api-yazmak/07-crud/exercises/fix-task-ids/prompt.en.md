This task API looks like it works, but it has a bug: a task added after
another task is deleted is written over an existing task.

**What to do:** fix `create_task` so it uses the `next_id` counter (a
number must never repeat).

- `POST /tasks` `{"title": "A"}` → `201`, `{"title": "A", "done": false, "id": 1}`
- `POST /tasks` `{"title": "B"}` → `id` `2`
- `DELETE /tasks/1` → `204`
- `POST /tasks` `{"title": "C"}` → `id` **`3`**
- `GET /tasks` → B and C, both still there
