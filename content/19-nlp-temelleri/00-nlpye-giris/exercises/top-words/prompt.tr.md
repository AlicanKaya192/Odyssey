`top_words(n, label, k)` ilk `n` yorumdan etiketi `label` olanlardaki en sık
`k` kelimeyi döndürsün. Her kelimeyi `lower()` ile küçült ve
`strip(".,!?")` ile noktalamadan temizle. Sonuç `Counter`'ın
`most_common(k)` çıktısının **kendisi** olsun: `(kelime, sayı)` demetlerinden
oluşan liste.

**Beklenen çıktı:**

```
the 281
is 138
not 117
i 99
after 71
```
