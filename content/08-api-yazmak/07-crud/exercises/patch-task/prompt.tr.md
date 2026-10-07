Ekleme ve `find_task` hazır.

**Yapman gerekenler:**

1. `TaskPatch`: `title` ve `done` isteğe bağlı (varsayılan `None`);
   `title` en az 1 karakter; **gönderilen** `null` `422` olsun.
2. `PATCH /tasks/{task_id}`: yalnızca gönderilen alanları değiştir, güncel
   görevi döndür; görev yoksa `404`.

- `POST /tasks` `{"title": "Read Dune"}` → id `1`
- `PATCH /tasks/1` `{"done": true}` → `{"title": "Read Dune", "done": true, "id": 1}`
- `PATCH /tasks/1` `{"title": "Read Emma"}` → `done` hâlâ `true`
- `PATCH /tasks/1` `{"title": null}` → `422`
- `PATCH /tasks/1` `{}` → görev değişmeden
