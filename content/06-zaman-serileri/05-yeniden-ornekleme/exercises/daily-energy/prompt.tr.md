`energy_hourly.csv` saatlik yükü (MW) içeriyor. Aynı seriden iki ayrı
günlük özet çıkar: tüketilen toplam enerji ve günün tepe yükü.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `load_mw` sütununu `load` serisine al.
2. Günlük toplamı (`sum`) ve günlük en yüksek değeri (`max`) hesapla.
3. Gün sayısını yazdır.
4. En çok enerji tüketilen günü (`"%Y-%m-%d"`) ve o günün toplamını (bir
   ondalık) aynı satıra yazdır.
5. Tepe yükün en yüksek olduğu günü ve o tepe değeri aynı satıra yazdır.
6. Hafta içi günlerin ve hafta sonu günlerin ortalama günlük toplamını tam
   sayıya yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
61
2024-03-04 22841.7
2024-03-07 1282.0
22383 19256
```

En çok tüketilen gün ile en yüksek tepenin görüldüğü gün aynı olmak zorunda
değil: biri bütün günün toplamına, öteki tek bir saate bakıyor.
