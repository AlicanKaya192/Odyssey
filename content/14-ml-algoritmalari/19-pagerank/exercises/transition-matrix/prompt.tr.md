`transition_matrix(links)` fonksiyonunu yaz: `links[j]`, `j` sayfasının
bağlantı verdiği sayfaların listesi; `n = len(links)`. `M[i, j] = 1 / çıkış(j)`
(`j → i` varsa). Bağlantısı olmayan (boş liste) sayfanın sütunu `1 / n`.
`.round(3).tolist()` döndürsün.

**Beklenen çıktı:**

```
[0.0, 0.0, 1.0]
[0.5, 0.0, 0.0]
[0.5, 1.0, 0.0]
```
