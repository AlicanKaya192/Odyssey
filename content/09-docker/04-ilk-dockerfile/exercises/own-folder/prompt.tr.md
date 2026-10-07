Bu Dockerfile çalışıyor ama `app.py` imajın kök klasörüne (`/`) gidiyor ve
Linux'un kendi klasörlerinin arasına karışıyor.

**Yapman gereken:** `COPY` satırından önce `/srv` klasörünü çalışma klasörü
yapan talimatı ekle. `app.py` bulunduğu klasörü yazdırıyor.

**Beklenen çıktı:**

```
working in /srv
```
