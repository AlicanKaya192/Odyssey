Tek bir hesap yerine **üç hesabı birden** yapıp rapor tablosu
üreteceksin.

**Yapman gerekenler:**

1. Şehre göre grupla ve üç sütunlu bir rapor üret, adı `report` olsun:
   - `people` — o şehirde kaç kişi var
   - `average` — not ortalaması
   - `highest` — en yüksek not
2. Sonucu **bir basamağa yuvarla** ve yazdır.
3. Izmir'de kaç kişi olduğunu tek başına yazdır.

**Beklenen çıktı:**

```
        people  average  highest
city
Ankara       3     87.0       91
Bursa        2     69.0       70
Izmir        3     71.3       76
3
```

**Kullanacağın yazım:**

```python
data.groupby("city").agg(
    yeni_ad=("hangi sutun", "hangi hesap"),
    ...
)
```

Bu biçim rapor üretirken en okunaklısı: sütun adını sen veriyorsun ve
hangi sütundan ne hesaplandığı tek bakışta görünüyor.

Sonuç bir tablo olduğu için tek hücreyi `loc[satır, sütun]` ile
alabiliyorsun.
