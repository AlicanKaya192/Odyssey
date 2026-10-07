`visits.py` her çalıştığında bir SQLite veritabanına bir ziyaret ekleyip
toplamı yazıyor. Veritabanının yerini `DB_PATH` ortam değişkeninden okuyor;
yoksa çalışma klasörüne (`app.db`) yazıyor ve veri her konteynerde
sıfırlanıyor.

**Yapman gerekenler:**

1. `ENV` ile `DB_PATH=/data/visits.db` varsayılanını yaz.
2. `/data`'yı `VOLUME` ile belgele.

Odyssey iki ayrı konteyneri aynı volume'la (`-v visits:/data`) çalıştıracak.

**Beklenen çıktılar:**

```
db: /data/visits.db visits: 1
db: /data/visits.db visits: 2
```
