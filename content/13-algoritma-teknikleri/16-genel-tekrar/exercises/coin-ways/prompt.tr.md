`coin_ways(amount, coins)` fonksiyonunu **dinamik programlama** ile yaz:
paraları istediğin kadar kullanarak `amount`'u kaç farklı şekilde
oluşturabileceğini döndürsün; sıra önemli değil (`1 + 2` ile `2 + 1` aynı).

`ways[0] = 1`; her para için `ways[t] += ways[t - c]`, `t` küçükten büyüğe.
Paralar dış döngüde olmalı, yoksa sıralar ayrı sayılır.

**Beklenen çıktı:**

```
4
0
234896541
```
