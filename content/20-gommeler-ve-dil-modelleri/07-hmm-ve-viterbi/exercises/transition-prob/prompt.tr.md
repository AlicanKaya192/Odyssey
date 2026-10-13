`transition_prob(train, a, b)` her cümlenin etiketlerinin başına `"<s>"`
ekleyip `P(b | a) = sayı(a, b) / sayı(a'dan sonra bir etiket)` olasılığını
3 basamakla döndürsün (`a` hiç görülmediyse `0.0`).

**Beklenen çıktı:**

```
0.5
1.0
0.0
```
