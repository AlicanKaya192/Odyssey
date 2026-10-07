Bir lambayı yöneten küçük bir API.

**Yapman gerekenler:**

1. `GET /lamp` durumu okusun: `{"on": false}`.
2. `POST /lamp/toggle` lambayı tersine çevirsin (açıksa kapat, kapalıysa
   aç) ve yeni durumu döndürsün.

Python'daki `False` JSON'da `false` olur.

```text
GET  /lamp          {"on": false}
POST /lamp/toggle   {"on": true}
POST /lamp/toggle   {"on": false}
```
