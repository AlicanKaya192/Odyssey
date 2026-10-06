Biri 1 ile 1000 arasında bir sayı tuttu: `secret = 371`. Her tahminde sana
yalnızca "büyük" ya da "küçük" diyor. En akıllı yol, her seferinde kalan
aralığın **tam ortasını** söylemek: her tahmin, olasılıkların yarısını
eliyor. Buna **ikili arama** denir.

Aralığı `low = 1`, `high = 1000` ile başlat ve şunu tekrarla:

1. `guess = (low + high) // 2`
2. Tahmini yazdır.
3. Tahmin `secret`'tan büyükse aralığın üst sınırını tahminin bir altına
   çek; küçükse alt sınırını tahminin bir üstüne çek; eşitse dur.

Tahmin sayısını `guesses` değişkeninde say. Çıktı şöyle olmalı:

```
Guess 1: 500 -> too high
Guess 2: 250 -> too low
Guess 3: 375 -> too high
Guess 4: 312 -> too low
Guess 5: 343 -> too low
Guess 6: 359 -> too low
Guess 7: 367 -> too low
Guess 8: 371 -> correct
Found 371 in 8 guesses
```

1000 sayının içinden 8 tahminde buldun; hangi sayı tutulursa tutulsun en
fazla 10 tahmin yeter. Bu yöntemin gücü bu: her tahmin kalan aralığı
yarıya indiriyor.

> Dikkat: Sınırı güncellerken `high = guess` değil `high = guess - 1`
> yaz: `guess` zaten denendi. Aksi hâlde bazı sayılarda döngü hiç bitmez.
