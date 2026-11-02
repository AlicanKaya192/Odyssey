`t_multiplier(level, n)` `n` kişilik örneklemde ortalamanın `level` güven
düzeyli aralığı için t çarpanını 3 basamakla döndürsün:
`stats.t.ppf((1 + level) / 2, df=n - 1)`. Başlangıç kodu normal dağılımın
çarpanını veriyor ve `n`'i hiç kullanmıyor.

**Beklenen çıktı:**

```text
2.776
1.984
2.861
```
