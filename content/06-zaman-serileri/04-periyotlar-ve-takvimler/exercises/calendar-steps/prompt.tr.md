Dört abonelik, ayın farklı günlerinde başlamış. Her biri için "bir ay
sonraki yenileme günü" hesaplanacak. Bu alıştırmada dosya yok.

```python
starts = ["2024-01-31", "2024-02-29", "2024-03-31", "2024-08-30"]
```

**Yapman gerekenler:**

1. Her başlangıç için iki tarih hesapla: **30 gün sonrası**
   (`pd.Timedelta(days=30)`) ve **bir ay sonrası** (`pd.DateOffset(months=1)`).
   Üçünü `başlangıç 30gün biray` biçiminde (`"%Y-%m-%d"`) aynı satıra yazdır.
2. 9 Mart 2024 için bulunduğu ayın son gününü yazdır (`MonthEnd(0)`).
3. 9 Mart 2024'ten ay sonuna kaç gün kaldığını yazdır.

**Beklenen çıktı:**

```
2024-01-31 2024-03-01 2024-02-29
2024-02-29 2024-03-30 2024-03-29
2024-03-31 2024-04-30 2024-04-30
2024-08-30 2024-09-29 2024-09-30
2024-03-31
22
```

İlk satırda iki yöntem bir gün ayrışıyor: 30 gün sonrası Mart'a taşıyor, bir
ay sonrası Şubat'ın son gününe iniyor. Üçüncü satırda ikisi aynı güne denk
geliyor; tam da bu yüzden hata uzun süre fark edilmiyor.
