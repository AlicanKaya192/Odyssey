`bigram_prob(sentences, a, b, k)` cümlelere `<s>` ve `</s>` ekleyip sayımları
kursun ve add-k olasılığını 3 basamakla döndürsün:

`(sayı(a, b) + k) / (sayı(a sonrasında bir şey) + k · V)`

`V` dağarcık boyu (`<s>` ve `</s>` dahil).

**Beklenen çıktı:**

```
0.667
0.2
0.024
```
