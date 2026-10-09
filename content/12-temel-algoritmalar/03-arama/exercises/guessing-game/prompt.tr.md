Biri 1 ile `n` arasında bir sayı tuttu. Her tahmininde sana "büyük",
"küçük" ya da "bildin" diyor. En iyi strateji her seferinde kalan aralığın
**ortasını** söylemek.

`count_guesses(n, secret)` fonksiyonunu yaz: bu stratejiyle `secret`'ı kaç
tahminde bulduğunu döndürsün. Tahmin `(lo + hi) // 2`; aralık başta
`lo = 1`, `hi = n`.

Sonra 100 ve 1 000 000 için en kötü durumu yazdır: aralıktaki **her**
`secret` için tahmin sayısının en büyüğü. (1 000 000 için bütün sayıları
denemek uzun sürer; onun yerine yalnızca `secret = 1` ve `secret = n`'yi
dene ve büyüğünü al.)

**Beklenen çıktı:**

```
100 7
1000000 20
```

100 sayıda en fazla 7, bir milyonda 20 tahmin: `O(log n)`.
