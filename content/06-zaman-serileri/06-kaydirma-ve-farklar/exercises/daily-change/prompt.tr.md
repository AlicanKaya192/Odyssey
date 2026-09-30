Satış bir günden ötekine ne kadar oynuyor, ve bunun ne kadarı haftalık
desenden geliyor?

**Yapman gerekenler:**

1. Dosyayı oku ve günlük farkı hesapla: `s.diff()`.
2. Farkların mutlak değerinin ortalamasını bir ondalığa yuvarlayıp yazdır.
3. En büyük artışın tarihini (`"%Y-%m-%d"`) ve miktarını aynı satıra yazdır.
4. En büyük düşüşün tarihini ve miktarını aynı satıra yazdır.
5. 9 Mart 2024 için geçen haftanın aynı gününe göre farkı yazdır
   (`s.diff(7)`).
6. `s.diff()` ve `s.diff(7)` standart sapmalarını bir ondalığa yuvarlayıp aynı
   satıra yazdır.

**Beklenen çıktı:**

```
36.8
2023-12-30 106.0
2024-01-01 -139.0
12.0
46.1 17.1
```

Günden güne farkın yayılımı, haftadan haftaya farkın neredeyse üç katı.
Aradaki fark haftanın deseni: cumartesiyi cumayla karşılaştırmak o deseni
ölçüyor, cumartesiyi cumartesiyle karşılaştırmak gerçek değişimi.
