**Yapman gereken:** sayaca bir `DELETE /counter` ekle: sayacı `0` yapsın ve
yeni hâli döndürsün.

Odyssey iki kez artırıp sonra siliyor:

```text
POST   /counter   {"count": 1}
POST   /counter   {"count": 2}
DELETE /counter   {"count": 0}
GET    /counter   {"count": 0}
```
