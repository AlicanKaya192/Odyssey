`ablation(definitions, base, tickets)` `definitions`'ta olup `base`'te
olmayan her kelimeyi (kategorisiyle birlikte) tek tek çıkarıp hazır
`accuracy(render(...), tickets)` ile yeniden ölçsün. Değişim
`round(yeni - tam, 2)` sıfır değilse `[kelime, değişim]` listeye girsin
(sözlük ve kelime sırasıyla).

**Beklenen çıktı:**

```
tracking -0.05
deliver -0.05
back 0.05
seam -0.05
card -0.05
```
