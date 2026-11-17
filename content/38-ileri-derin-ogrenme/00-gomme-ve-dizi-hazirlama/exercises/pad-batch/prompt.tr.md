`pad_batch(seqs)` farklı uzunluktaki kimlik listelerini `pad_sequence` ile
`0` ile dolgulayıp `(B, T)` şeklinde bir tensöre çevirsin. İki öğeli bir
liste döndürsün: dolgulu tensörün `.tolist()` hâli ve her dizinin gerçek
uzunluğu.

**Beklenen çıktı:**

```
[[4, 2, 3], [5, 0, 0], [7, 7, 0]]
[3, 1, 2]
```
