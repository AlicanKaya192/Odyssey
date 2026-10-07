Bir API'nin bir saatlik yanıt kodları `codes` listesinde. Sunucunun sağlığını
özetleyeceksin.

**Yapman gerekenler:**

1. `counts` adlı bir sözlükte her sınıftan kaç yanıt olduğunu say. Anahtarlar
   `"2xx"`, `"3xx"`, `"4xx"`, `"5xx"`; hiç olmayan sınıf da `0` ile yer
   alsın.
2. Sınıfları bu sırayla `2xx: 11` biçiminde yazdır.
3. Hata oranını (4xx + 5xx, toplamın yüzdesi) bir ondalıkla
   `error rate: 40.0%` biçiminde yazdır.
4. En sık görülen **hata** kodunu ve `HTTPStatus` ile adını yazdır.

**Beklenen çıktı:**

```
2xx: 11
3xx: 1
4xx: 6
5xx: 2
error rate: 40.0%
most common error: 404 Not Found
```

Yüzdeyi bir ondalıkla yazmak için `f"{rate:.1f}%"`.
