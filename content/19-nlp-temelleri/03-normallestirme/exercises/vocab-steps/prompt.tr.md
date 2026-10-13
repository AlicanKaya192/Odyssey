`vocab_steps(n)` ilk `n` yorumdaki kelime dağarcığını üç adımda ölçsün ve
`[ham, durak_sonrası, kök_sonrası]` döndürsün:

1. ham: bütün kelimelerin kümesi
2. durak sonrası: `STOP`'ta olmayanlar
3. kök sonrası: kalanların `stem` ile kökleri (küme)

**Beklenen çıktı:**

```
[332, 303, 297]
```
