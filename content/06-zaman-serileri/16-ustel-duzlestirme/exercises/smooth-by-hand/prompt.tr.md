Basit üstel düzleştirmeyi bir döngüyle kendin yaz ve pandas'ın sonucuyla
karşılaştır. Başlangıç kodunda `y` hazır: 1–14 Eylül 2024 satışları.

**Yapman gerekenler:**

1. `smooth(values, alpha)` fonksiyonunu yaz: düzeyi ilk değerle başlat; her
   değer için `level = alpha * value + (1 - alpha) * level` uygula ve
   düzeyleri liste olarak döndür.
2. `α = 0.5` ile ilk 5 düzeyi bir ondalığa yuvarlayıp liste olarak yazdır.
3. Aynısını pandas ile hesapla (`y.ewm(alpha=0.5, adjust=False).mean()`) ve
   ilk 5 değeri yazdır.
4. İki sonuç 14 günün hepsinde aynı mı? En büyük mutlak farkın `1e-9`'dan
   küçük olup olmadığını yazdır.
5. 15 Eylül tahmini son düzeydir. `α = 0.1`, `0.5` ve `0.9` için bu tahmini
   bir ondalığa yuvarlayıp liste olarak yazdır.
6. 15 Eylül'ün gerçek değerini yazdır.

**Beklenen çıktı:**

```
[351.0, 287.0, 255.0, 259.5, 261.8]
[351.0, 287.0, 255.0, 259.5, 261.8]
True
[312.4, 337.4, 373.9]
353
```

Aynı 14 gün, üç farklı tahmin. Son gün (cumartesi) yüksek olduğu için büyük
`α` tahmini yukarı çekiyor; küçük `α` iki haftanın ortalamasına yakın
kalıyor. Ortadaki tahmin pazar gününe (353) tesadüfen yakın düştü, ama model
bütün ufuk için aynı sayıyı söylüyor: pazartesi için de 337. Oysa bu iki
haftanın pazartesileri 223 ve 270. Basit üstel düzleştirme haftalık deseni
bilmiyor; mevsimli seride tek başına kullanılmaz.
