2024'ün günlük satışını silik bir çizgiyle, üstüne iki hareketli
ortalamayı kalın çizgiyle çiz.

**Yapman gerekenler:**

1. Dosyayı oku. Hareketli ortalamaları **bütün seride** hesapla
   (`s.rolling(7).mean()`, `s.rolling(28).mean()`), sonra 2024'ü seç. Böylece
   yılın ilk günleri boş kalmıyor.
2. `figsize=(10, 4)` tuvalde üç çizgi çiz: günlük (`color="lightgray"`,
   etiket `daily`), 7 günlük (etiket `7-day mean`), 28 günlük (etiket
   `28-day mean`).
3. Lejantı ekle (`ax.legend()`) ve `chart.png` olarak kaydet.
4. Çizgi sayısını yazdır.
5. Lejanttaki etiketleri liste olarak yazdır:
   `[t.get_text() for t in ax.get_legend().get_texts()]`.
6. 2024 içindeki 7 günlük ve 28 günlük ortalamalardaki `NaN` sayılarını aynı
   satıra yazdır.

**Beklenen çıktı:**

```
3
['daily', '7-day mean', '28-day mean']
0 0
```

Ortalamaları önce bütün seride hesapladığın için 2024'ün 1 Ocak'ında da
değer var: pencere 2023'ün son günlerinden besleniyor. Önce 2024'ü seçip
sonra `rolling` yapsaydın ilk 27 gün boş kalırdı.
