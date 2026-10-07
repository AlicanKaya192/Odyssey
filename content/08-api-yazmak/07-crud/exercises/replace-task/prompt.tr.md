Ekleme, okuma ve `find_task` hazır.

**Yapman gereken:** `PUT /tasks/{task_id}`: görevin tamamını gelen
`TaskIn` ile değiştir ve güncel görevi döndür. Görev yoksa `404`.

- `POST /tasks` `{"title": "Read Dune"}` → id `1`
- `PUT /tasks/1` `{"title": "Read Emma", "done": true}` → `{"title": "Read Emma", "done": true, "id": 1}`
- `PUT /tasks/1` `{"done": true}` → `422`
- `PUT /tasks/5` `{"title": "X"}` → `404`
