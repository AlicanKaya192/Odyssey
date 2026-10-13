`learn_bpe(counts, n_merges)` `{kelime: sıklık}` sözlüğünden en fazla
`n_merges` birleştirme kuralı öğrensin ve `[a, b]` listesi olarak döndürsün.
Her adımda en sık çifti seç; eşitlikte `(sayı, çift)` anahtarının en büyüğü.
Çift kalmazsa dur.

**Beklenen çıktı:**

```
['t', '</w>']
['s', 't</w>']
['e', 'st</w>']
['o', 'w']
['l', 'ow']
```
