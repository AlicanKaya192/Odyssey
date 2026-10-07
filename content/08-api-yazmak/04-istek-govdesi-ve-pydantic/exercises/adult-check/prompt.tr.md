**Yapman gereken:** `POST /users` bir kişi alsın ve reşit olup olmadığını
söylesin (18 ve üstü).

- `{"name": "Ada", "age": 36}` → `{"name": "Ada", "age": 36, "adult": true}`
- `{"name": "Tim", "age": "12"}` → `{"name": "Tim", "age": 12, "adult": false}`
- `{"name": "Bo"}` → `422`
- `{"name": "Bo", "age": "old"}` → `422`
