Rastgele bir parolanın entropisi `uzunluk × log2(alfabe)` bittir.
`entropy_bits(length, alphabet_size)` bunu hesaplayıp `round(..., 1)` ile
döndürmeli. Başlangıç kodu yanlış logaritmayı kullanıyor: `math.log` doğal
logaritmadır; iki tabanlısı `math.log2`.

**Beklenen çıktı:**

```
8 10 26.6
12 26 56.4
16 62 95.3
20 94 131.1
```
