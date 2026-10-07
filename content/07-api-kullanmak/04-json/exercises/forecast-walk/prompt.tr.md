`forecast.json` dosyasında dört günlük bir tahmin var. Her gün bir sözlük ve
**her günde rüzgâr bilgisi yok.**

**Yapman gerekenler:**

1. Dosyayı `json.load` ile `data` adlı değişkene oku.
2. Her gün için gün adını, sıcaklığı ve rüzgâr hızını yazdır. Rüzgâr yoksa
   hız yerine `?` yazdır (`get` kullan).
3. En sıcak günün adını `hottest` değişkenine koy ve yazdır.

**Beklenen çıktı:**

```
mon 24 wind 12
tue 21 wind ?
wed 26 wind 7
thu 19 wind 20
hottest: wed
```
