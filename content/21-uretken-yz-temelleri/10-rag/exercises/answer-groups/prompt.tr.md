`groups(results)` her `[key, cevap]` çiftini dersteki dört gruptan birine
koysun ve `[doğru, doğru çekimser, yanlış, kaçırılan]` sayılarını döndürsün.
`key` `None` ise soru cevapsız: cevap `NOT_FOUND` ise doğru çekimser, değilse
yanlış. `key` varsa: cevap `NOT_FOUND` ise kaçırılan, `key` cevapta geçiyorsa
doğru, değilse yanlış.

**Beklenen çıktı:**

```
[1, 1, 1, 1]
```
