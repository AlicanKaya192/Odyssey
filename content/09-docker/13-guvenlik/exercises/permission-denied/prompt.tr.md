`writer.py` `/app/output.txt` dosyasına yazıyor; imaj `app` kullanıcısıyla
çalışıyor ve program şu hatayla düşüyor:

```text
PermissionError: [Errno 13] Permission denied: '/app/output.txt'
```

`/app` klasörünü `WORKDIR` root olarak oluşturdu.

**Yapman gereken:** `USER app` satırından önce `/app`'in sahibini `app`
yap (`chown`). Root'a dönme, `777` verme.

**Beklenen çıktı:**

```
saved 3 lines as app
```
