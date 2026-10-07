Adding, reading and `find_task` are ready.

**What to do:** `PUT /tasks/{task_id}`: replace the whole task with the
incoming `TaskIn` and return the current task. `404` if missing.

- `POST /tasks` `{"title": "Read Dune"}` → id `1`
- `PUT /tasks/1` `{"title": "Read Emma", "done": true}` → `{"title": "Read Emma", "done": true, "id": 1}`
- `PUT /tasks/1` `{"done": true}` → `422`
- `PUT /tasks/5` `{"title": "X"}` → `404`
