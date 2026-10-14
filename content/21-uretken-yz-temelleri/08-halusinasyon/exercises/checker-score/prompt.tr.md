Başlangıç kodunda dersteki `unsupported` fonksiyonu hazır. `score(examples,
source)` her `[cevap, sadık_mı]` örneğinde cevabı, desteksiz ayrıntısı varsa
"uydurma" diye işaretlesin ve `[tp, fp, fn, tn, kesinlik, duyarlılık]`
döndürsün. `tp`: işaretlenen uydurma, `fp`: işaretlenen sadık cevap, `fn`:
kaçan uydurma, `tn`: işaretlenmeyen sadık cevap. Kesinlik
`tp / (tp + fp)`, duyarlılık `tp / (tp + fn)`; 2 basamağa yuvarlanmış
`float`, payda 0 ise `0.0`.

**Beklenen çıktı:**

```
[3, 0, 1, 2, 1.0, 0.75]
```
