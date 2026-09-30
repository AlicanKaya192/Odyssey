Temiz 2024 satışından 8–21 Temmuz arasındaki 14 günü sil ve iki yöntemle
geri doldur. Başlangıç kodunda `truth` (gerçek) ve `gap` (boşluklu) hazır.

**Yapman gerekenler:**

1. Doğrusal doldurma: `linear = gap.interpolate()`.
2. Haftalık zincir: `chain = gap.copy()`; eksik günleri **tarih sırasıyla**
   dolaş ve her birine 7 gün önceki değeri yaz
   (`chain.loc[day - pd.Timedelta(days=7)]`).
3. İki yöntemin boşluktaki ortalama mutlak hatasını bir ondalığa yuvarlayıp
   aynı satıra yazdır (önce doğrusal).
4. Boşluktaki iki cumartesi (13 ve 20 Temmuz) için gerçek, doğrusal ve zincir
   değerlerini tam sayıya yuvarlayıp iki satırda yazdır.
5. Boşluk içinde doğrusal doldurmanın ve zincirin standart sapmasını, gerçeğin
   standart sapmasıyla birlikte bir ondalığa yuvarlayıp aynı satıra yazdır
   (sıra: gerçek, doğrusal, zincir).
6. `gap.ffill(limit=3)` sonrasında kaç `NaN` kaldığını yazdır.

**Beklenen çıktı:**

```
47.5 9.6
344 278 346
343 242 346
45.2 21.2 52.9
11
```

Doğrusal doldurma iki cumartesi tepesini de kaçırıyor ve boşluğun içindeki
oynaklığı yarıdan fazla azaltıyor: düz, eğimli bir çizgi. Zincir deseni koruyor.
`limit=3` ise boşluğu kapatmıyor, yalnızca ilk üç gününü dolduruyor.
