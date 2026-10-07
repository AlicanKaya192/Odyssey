Sunucular gelen her isteği bir **kayda** (log) yazar: kim, hangi uç noktaya
sordu. Bu kayıtlar "en çok hangi kapı kullanılıyor?", "olmayan bir kapıya
kim soruyor?" gibi soruların cevabı.

Kayıt `log` listesinde: her öğe `(istemci, uç nokta)` demeti. API'nin bildiği
uç noktalar `known` listesinde.

**Yapman gerekenler:**

1. Her uç noktanın kaç istek aldığını `counts` adlı bir sözlükte say.
2. Uç noktaları **abece sırasıyla** `uç_nokta sayı` biçiminde yazdır.
3. `known` içinde olmayan uç noktalara giden isteklerin (bunlar `404` alır)
   toplamını `404 responses: N` biçiminde yazdır.

**Beklenen çıktı:**

```
/cities 1
/forecast 2
/news 2
/weather 3
404 responses: 2
```
