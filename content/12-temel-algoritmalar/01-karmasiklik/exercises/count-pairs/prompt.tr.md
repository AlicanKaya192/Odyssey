`count_pairs(n)` fonksiyonunu **iç içe iki döngüyle** yaz: `0`'dan `n-1`'e
kadar sayılardan oluşan her **ikiliyi** (`i < j`) bir kez saysın ve sayıyı
döndürsün.

Sonra `n` değeri 10, 100 ve 1000 için `n`'yi, sayılan ikili sayısını ve
`n * (n - 1) // 2` formülünün sonucunu aynı satıra yazdır.

**Beklenen çıktı:**

```
10 45 45
100 4950 4950
1000 499500 499500
```

Sayım formülle aynı; `n` 10 kat büyüyünce iş yaklaşık 100 kat büyüyor:
`O(n²)`.
