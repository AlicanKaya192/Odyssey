Taban adres bazen `/` ile bitiyor, bazen bitmiyor; uç nokta bazen `/` ile
başlıyor, bazen başlamıyor. Dört durumun dördünde de sonuç **tek bir**
`/` ile birleşmeli.

**Yapman gerekenler:**

1. `endpoint_url(base, path)` fonksiyonunu yaz: tabanın sağındaki ve yolun
   solundaki eğik çizgileri temizleyip araya tek `/` koysun.
2. Aşağıdaki dört birleşimi yazdır.

**Beklenen çıktı:**

```
https://api.example.com/v1/weather
https://api.example.com/v1/weather
https://api.example.com/v1/weather
https://api.example.com/v1/books/42
```
