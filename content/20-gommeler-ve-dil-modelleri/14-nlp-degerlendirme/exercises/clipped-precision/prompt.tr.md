`clipped_precision(candidate, reference, n)` BLEU'nun bir basamağını
hesaplasın: adayın `n`'li kelime gruplarından referansta da geçenlerin oranı;
her grup referansta kaç kez geçiyorsa en fazla o kadar sayılır. 3 basamak;
adayda grup yoksa `0.0`.

**Beklenen çıktı:**

```
0.75
0.25
0.667
```
