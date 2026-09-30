Yolcu serisinde fark almanın neden yetmediğini ve logaritmanın neyi
düzelttiğini ölç.

**Yapman gerekenler:**

1. `d = p.diff()` hesapla. Üç dönem için (2013–2016, 2017–2020, 2021–2024)
   standart sapmasını bir ondalığa yuvarlayıp liste olarak yazdır.
2. Aynısını `np.log(p).diff()` için üç ondalıkla yazdır.
3. Her iki listede son dönemin ilk döneme oranını iki ondalığa yuvarlayıp aynı
   satıra yazdır.
4. Yıllık büyüme oranı: `growth = np.log(p).diff(12)`. Ortalamasını yüzde
   olarak bir ondalığa yuvarlayıp yazdır (`growth.mean() * 100`).
5. `growth` serisinin ilk dolu değerinin tarihini ve `NaN` sayısını aynı
   satıra yazdır.

**Beklenen çıktı:**

```
[14.2, 23.0, 34.7]
[0.093, 0.097, 0.1]
2.44 1.08
10.2
2014-01-01 12
```

Düz farkta dalga boyu dönemden döneme 2.4 katına çıkıyor; logaritmadan sonra
oran 1'e çok yakın. Yıllık büyüme ortalama %10 dolayında: düzey üç katına
çıkarken büyüme **oranı** sabit kalmış.
