Trend var mı? En basit yol, her yılın ortalamasına bakmak: yıllık
ortalama haftalık ve aylık inip çıkmaları sönümlüyor, geriye uzun vadeli
yön kalıyor.

Tarihler henüz metin. Tarih türüne çevirmeyi Bölüm 02'de öğreneceksin; şimdilik
ISO 8601'in bir faydasını daha kullan: **yıl her zaman ilk dört karakter.**

```python
table["date"].str[:4]    # "2022-01-01" -> "2022"
```

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını oku.
2. `year` adında yeni bir sütun oluştur: tarihin ilk dört karakteri.
3. Yıla göre grupla, satışın ortalamasını bir ondalığa yuvarla. Her yılı
   `yıl ortalama` biçiminde bir satıra yazdır.
4. Son yılın ortalamasının ilk yıla göre yüzde kaç arttığını bir ondalığa
   yuvarlayıp yazdır: `(son / ilk - 1) * 100`.

**Beklenen çıktı:**

```
2022 225.5
2023 260.4
2024 294.0
30.4
```

İki yılda yaklaşık üçte bir büyüme: açık bir yukarı trend.
