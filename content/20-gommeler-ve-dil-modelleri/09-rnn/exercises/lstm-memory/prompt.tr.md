`lstm_memory(forgets, writes, news)` hücre durumunu `0`'dan başlatsın ve her
adımda `c = f · c + i · g` ile güncellesin (`f` unutma, `i` yazma kapısı,
`g` yeni bilgi). Her adımdan sonraki hücre değerini 3 basamakla listede
döndürsün.

**Beklenen çıktı:**

```
[0.8, 0.8, 0.8]
[1.0, 0.5, -0.3]
```
