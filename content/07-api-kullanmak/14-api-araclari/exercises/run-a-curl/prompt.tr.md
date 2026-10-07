Belgeden kopyaladığın curl komutunu Python'da çalıştır. `parse_curl` hazır
veriliyor (bir önceki alıştırmanın çözümü).

**Yapman gerekenler:**

1. `parse_curl(command)` ile komutu çöz.
2. `requests.request(method, url, headers=..., data=...)` ile isteği gönder.
   Gövde metin olduğu için `data=` kullan; `Content-Type` başlığı zaten
   komutta var.
3. Durum kodunu, `Location` başlığını ve yanıttaki başlığı (`title`)
   yazdır.

**Beklenen çıktı:**

```
status: 201
location: /books/24
title: Kindred
```
