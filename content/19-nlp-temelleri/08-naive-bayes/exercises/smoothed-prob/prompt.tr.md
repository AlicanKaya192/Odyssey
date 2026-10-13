`word_prob(count, class_total, vocab_size, alpha)` bir kelimenin sınıf içindeki
yumuşatılmış olasılığını 5 basamakla döndürsün:

`(count + alpha) / (class_total + alpha * vocab_size)`

İlk örnekte kelime sınıfta hiç görülmemiş ama olasılığı sıfır değil.

**Beklenen çıktı:**

```
0.00077
0.02
0.02437
```
