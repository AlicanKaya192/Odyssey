`average_miss(values, n, repeats)` örneklem ortalamasının gerçek ortalamayı
ortalama ne kadar ıskaladığını ölçsün: `seed` 0'dan `repeats - 1`'e kadar her
seferinde `np.random.default_rng(seed)` ile tekrarsız `n` değer seç,
`abs(örneklem ortalaması - gerçek ortalama)` farkını topla ve bu farkların
ortalamasını 3 basamakla döndür. Başlangıç kodu tek bir örnekleme bakıyor.

**Beklenen çıktı:**

```text
11.873
5.34
1.678
```
