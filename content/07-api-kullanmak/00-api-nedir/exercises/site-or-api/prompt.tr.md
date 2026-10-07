Her yanıt ne tür veri taşıdığını bir etiketle söyler: **içerik türü**
(content type). `text/html` bir web sayfası, yani insan için; `application/json`
düzenli veri, yani program için.

**Yapman gerekenler:**

1. `responses` listesindeki yanıtlardan içerik türü `application/json`
   olanların adreslerini `api_urls` adlı bir listeye topla (sırayı koru).
2. `For programs:` yazdır, altına bu adresleri birer satırda yazdır.
3. Son satırda `text/html` olanların sayısını `For people: N` biçiminde
   yazdır.

**Beklenen çıktı:**

```
For programs:
/api/weather
/api/cities
/api/forecast
For people: 2
```

İçerik türünü Bölüm 02 ve 03'te başlıkların (headers) içinde yeniden
göreceksin; istemci yanıtı nasıl okuyacağına ona bakarak karar veriyor.
