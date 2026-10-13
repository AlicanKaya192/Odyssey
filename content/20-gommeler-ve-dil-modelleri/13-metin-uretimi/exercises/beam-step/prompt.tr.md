`beam_step(beams, table, width)` ışın aramasının bir adımını atsın. `beams`
`[puan, kelimeler]` listesi; `table` son kelime → {sonraki kelime:
olasılık}. Her yolu her olası kelimeyle uzat, puana `log(olasılık)` ekle (3
basamak), puana göre büyükten küçüğe sırala, en iyi `width` yolu döndür.

**Beklenen çıktı:**

```
-1.021 ['<s>', 'the', 'app']
-1.204 ['<s>', 'my', 'order']
```
