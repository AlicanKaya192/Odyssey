`escape_like(term)` metindeki `\`, `%` ve `_` karakterlerinin önüne
`\` koysun. Başlangıç kodu doğru karakterleri kaçıyor ama **sırası
yanlış**: `\`'yi en son kaçtığı için az önce eklediği kaçış işaretlerini
de ikiler. Önce `\`, sonra `%` ve `_`.

**Beklenen çıktı:**

```
0% ['50% discount']
_ ['plan_b']
n_b ['plan_b']
```
