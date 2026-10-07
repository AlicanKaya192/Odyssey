**Yapman gereken:** aynı adla birden çok kez gönderilen `tag` değerlerini
liste olarak al; abece sırasıyla ve sayısıyla döndür.

- `GET /tags?tag=python&tag=api&tag=docker` → `{"tags": ["api", "docker", "python"], "count": 3}`
- `GET /tags` → `{"tags": [], "count": 0}`
