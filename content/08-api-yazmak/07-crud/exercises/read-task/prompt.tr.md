Görev ekleme (`POST /tasks`) hazır.

**Yapman gerekenler:**

1. `find_task(task_id)`: görev yoksa `404` (`"Task not found"`), varsa
   görevi döndüren yardımcı.
2. `GET /tasks`: isteğe bağlı `done` sorgusuyla süz.
3. `GET /tasks/{task_id}`: tek görev.

- Eklenenler: `{"title": "A"}`, `{"title": "B", "done": true}`
- `GET /tasks?done=true` → yalnızca B
- `GET /tasks` → ikisi
- `GET /tasks/2` → B; `GET /tasks/9` → `404`
