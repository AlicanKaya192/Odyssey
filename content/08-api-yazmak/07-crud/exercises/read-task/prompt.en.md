Adding tasks (`POST /tasks`) is ready.

**What to do:**

1. `find_task(task_id)`: a helper that gives `404` (`"Task not found"`) if
   the task is missing, otherwise returns it.
2. `GET /tasks`: filter with an optional `done` query.
3. `GET /tasks/{task_id}`: one task.

- Added: `{"title": "A"}`, `{"title": "B", "done": true}`
- `GET /tasks?done=true` → only B
- `GET /tasks` → both
- `GET /tasks/2` → B; `GET /tasks/9` → `404`
