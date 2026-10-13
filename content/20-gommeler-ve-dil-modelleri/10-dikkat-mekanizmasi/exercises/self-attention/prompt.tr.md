Bir cümlenin her kelimesi (satır) bütün kelimelere dikkat etsin.
`self_attention(X)` ağırlık tablosunu döndürsün: puanlar `X @ X.T / √d` (`d`
sütun sayısı), her satıra ayrı softmax, 3 basamak, liste listesi.

**Beklenen çıktı:**

```
[0.401, 0.198, 0.401]
[0.198, 0.401, 0.401]
[0.248, 0.248, 0.503]
```
