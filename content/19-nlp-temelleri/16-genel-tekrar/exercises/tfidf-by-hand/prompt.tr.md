`tfidf_weights(docs, word)` her belge (token listesi) için `word`'ün TF-IDF
ağırlığını döndürsün (3 basamak, normalleştirme yok):

- TF: kelimenin belgede kaç kez geçtiği
- IDF: `ln((1 + n) / (1 + df)) + 1`; `n` belge sayısı, `df` kelimeyi
  içeren belge sayısı (scikit-learn'ün varsayılanı)

**Beklenen çıktı:**

```
[2.575, 0.0, 1.288]
[1.288, 1.288, 0.0]
```
