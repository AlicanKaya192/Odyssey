`hinge_losses(y, scores)` fonksiyonunu yaz: her örnek için
`max(0, 1 − y · puan)`; `.round(3).tolist()` döndürsün. Etiketler `−1/+1`.

**Beklenen çıktı:**

```
[0.0, 0.5, 0.7, 2.2]
```
