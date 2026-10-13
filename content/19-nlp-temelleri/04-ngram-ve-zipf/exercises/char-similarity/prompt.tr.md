`similarity(a, b, n)` iki kelimenin harf n-gram kümelerinin Jaccard
benzerliğini (ortak / birleşim) 2 basamağa yuvarlayıp döndürsün.
`char_ngrams` hazır. Çıktıda aynı kelime çiftleri için `n=3` ve `n=2`
yan yana.

**Beklenen çıktı:**

```
cable 1.0 1.0
cables 0.57 0.62
cabel 0.25 0.33
able 0.5 0.57
```
