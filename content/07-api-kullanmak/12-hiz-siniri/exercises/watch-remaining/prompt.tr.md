429 almadan, kalan hakkı izleyerek 7 istek gönder: hak sıfıra inince pencerenin
yenilenmesi için bekle.

**Yapman gerekenler:**

1. `/limited`'e 7 istek gönder.
2. Her yanıttan sonra `X-RateLimit-Remaining`'i sayıya çevir; `0` ise
   `pause` yazdır ve 1 saniye bekle.
3. Kodları `codes` listesine topla; sonda listeyi yazdır.

**Beklenen çıktı:**

```
pause
pause
[200, 200, 200, 200, 200, 200, 200]
```
