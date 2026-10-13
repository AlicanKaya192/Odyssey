`dedupe(n, threshold)` ilk `n` yorumu sırayla dolaşsın. Bir yorum, **daha
önce tutulan** yorumlardan herhangi biriyle Jaccard benzerliği `threshold`
ya da üstündeyse atılsın, değilse tutulsun. Tutulan yorum sayısını
döndürsün. `shingles` ve `jaccard` hazır.

**Beklenen çıktı:**

```
591
589
```
