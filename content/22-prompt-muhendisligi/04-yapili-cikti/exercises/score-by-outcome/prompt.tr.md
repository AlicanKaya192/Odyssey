`score_outcomes(pairs)` `[beklenen, gelen]` çiftlerinin listesini alsın ve
bir sözlük döndürsün:

- `LABELS`'taki her sonuç için `[doğru, toplam]`: beklenen o sonuç olan
  çiftlerin kaçında gelen de aynı.
- `"false_accept"`: gelen `"accepted"` iken beklenen başka bir şey olan
  çiftlerin sayısı. En pahalı hata bu: sorulması ya da reddedilmesi
  gereken bir cevap kabul edildi.

**Beklenen çıktı:**

```
accepted [1, 2]
rejected [1, 2]
needs_clarification [0, 1]
false_accept 2
```
