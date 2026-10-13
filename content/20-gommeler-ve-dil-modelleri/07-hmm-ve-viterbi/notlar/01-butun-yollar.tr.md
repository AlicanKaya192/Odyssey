Viterbi'nin bulduğu yol gerçekten en iyisi mi? Kısa bir cümlede bütün
etiket dizilerini tek tek deneyip karşılaştıralım. Dersteki `transition`,
`log_emit`, `tags` ve `viterbi` ile:

```python
from itertools import product


def path_score(sentence, path):
    score, prev = 0.0, START
    for w, t in zip(sentence, path):
        score += transition[prev, index[t]] + log_emit(t, w)
        prev = index[t]
    return score


sentence = "they book the light train".split()
paths = list(product(tags, repeat=len(sentence)))
best = max(paths, key=lambda p: path_score(sentence, p))
print(len(paths), list(best) == viterbi(sentence))
print(list(best))
print(len(sentence) * len(tags) ** 2)
```

```text
16807 True
['PRON', 'VERB', 'DET', 'ADJ', 'NOUN']
245
```

- Beş kelimede 16 807 dizi var; en iyisi Viterbi'nin bulduğuyla aynı.
- Viterbi aynı sonuca `n · T² = 245` karşılaştırmayla ulaşıyor. Kelime
  sayısı iki katına çıkınca bütün dizilerin sayısı `7^10 ≈ 282 milyon` olur;
  Viterbi'nin işi yalnızca iki katına çıkar.
- Bunu mümkün kılan, HMM'in **Markov varsayımı**: bir etiketin puanı
  yalnızca bir önceki etikete bağlı. Bu yüzden bir adımdaki en iyi yolu
  bilmek, sonraki adım için yeterli.
