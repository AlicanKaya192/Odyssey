`count_ways(amount, coins)` fonksiyonunu yaz: tutarı verilen paralarla
**kaç farklı şekilde** verebileceğini döndürsün. Sıra önemli değil: `2 + 5` ile
`5 + 2` aynı.

`ways = [1] + [0] * amount`; **dış döngü paralar**, iç döngü tutarlar:
`ways[a] += ways[a − c]`.

**Beklenen çıktı:**

```
10
292
321335886
```
