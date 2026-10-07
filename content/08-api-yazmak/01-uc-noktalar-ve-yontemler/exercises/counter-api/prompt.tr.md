**Yapman gerekenler:** `state` sözlüğünü kullanan iki uç nokta:

1. `GET /counter` sayacı okusun: `{"count": 0}`.
2. `POST /counter` sayacı 1 artırıp yeni hâli döndürsün.

Odyssey sırayla `GET`, `POST`, `POST`, `GET` gönderecek:

```text
GET  /counter   {"count": 0}
POST /counter   {"count": 1}
POST /counter   {"count": 2}
GET  /counter   {"count": 2}
```
