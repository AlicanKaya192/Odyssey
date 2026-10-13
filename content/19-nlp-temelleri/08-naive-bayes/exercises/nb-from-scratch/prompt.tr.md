`train` hazır: sınıf sayıları, sınıf başına kelime sayıları ve dağarcık.
`predict(text)` her sınıf için (alfabetik sırayla):

1. `log(önsel)`: `priors[label] / toplam`
2. metindeki her **dağarcıkta olan** kelime için
   `log((counts[label][w] + 1) / (sınıf_kelime_toplamı + len(vocab)))`

toplamını hesaplasın ve en büyük puanlı sınıfı döndürsün.

**Beklenen çıktı:**

```
great sound -> pos
battery died -> neg
terrible -> neg
unknown words -> pos
```
