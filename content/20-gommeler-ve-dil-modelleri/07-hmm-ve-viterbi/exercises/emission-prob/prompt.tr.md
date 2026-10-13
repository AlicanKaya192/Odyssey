`emission_prob(train, tag, word, k)` add-k yayım olasılığını 3 basamakla
döndürsün: `(sayı(word, tag) + k) / (sayı(tag) + k · V)`; `V` eğitimdeki
farklı kelime sayısı + 1 (bilinmeyen için).

**Beklenen çıktı:**

```
1.0
0.333
0.111
```
