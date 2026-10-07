Bu görev API'si çalışıyor gibi duruyor ama bir hatası var: bir görev
silindikten sonra eklenen görev, var olan bir görevin üstüne yazılıyor.

**Yapman gereken:** `create_task`'ı `next_id` sayacını kullanacak şekilde
düzelt (numara hiç tekrar etmesin).

- `POST /tasks` `{"title": "A"}` → `201`, `{"title": "A", "done": false, "id": 1}`
- `POST /tasks` `{"title": "B"}` → `id` `2`
- `DELETE /tasks/1` → `204`
- `POST /tasks` `{"title": "C"}` → `id` **`3`**
- `GET /tasks` → B ve C, ikisi de duruyor
