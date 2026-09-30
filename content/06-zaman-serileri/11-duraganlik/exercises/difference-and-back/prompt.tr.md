Günlük satışta düz farkı ve mevsimsel farkı karşılaştır, sonra farkın
hiçbir bilgi kaybettirmediğini göster.

**Yapman gerekenler:**

1. Serinin, `s.diff()`'in ve `s.diff(7)`'nin standart sapmasını bir ondalığa
   yuvarlayıp aynı satıra yazdır.
2. Aynı üç serideki `NaN` sayılarını aynı satıra yazdır.
3. Haftalık desen gitti mi? `s.diff()` ve `s.diff(7)` için haftanın gününe
   göre ortalamayı al ve her birinde en yüksek ile en düşük gün arasındaki
   farkı bir ondalığa yuvarlayıp aynı satıra yazdır.
4. Düz farkı geri çevir: `back = s.diff().cumsum() + s.iloc[0]`. İlk satır
   dışında seriyle aynı mı? `(back.iloc[1:] - s.iloc[1:]).abs().max() < 1e-9`
   sonucunu yazdır.
5. Mevsimsel farkı bir adım geri çevir: serinin son gününün değerini,
   `s.diff(7)`'nin son değeri ile 7 gün önceki satışın toplamı olarak hesapla
   ve gerçek son değerle birlikte aynı satıra yazdır.

**Beklenen çıktı:**

```
58.9 46.1 17.1
0 1 7
136.7 0.4
True
347 347
```

Düz farkta haftanın günleri arasında hâlâ büyük bir fark var: desen yerinde.
`diff(7)`'de neredeyse sıfır. Ve iki fark da geri alınabiliyor: model farkı
tahmin eder, düzeye sen çevirirsin.
