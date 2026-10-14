`kept_share(k)` eğitim verisinin (ortalaması çıkarılmış) tekil değerlerinden
(`S`) ilk `k` yönün verinin yayılımının ne kadarını tuttuğunu döndürsün:
`(S[:k] ** 2).sum() / (S ** 2).sum()`, 3 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
2 0.287
8 0.674
16 0.85
32 0.966
```
