`bce_loss(y, p)` fonksiyonunu yaz: `−ort(y log p + (1 − y) log(1 − p))`;
`p`'yi önce `[1e-12, 1 − 1e-12]` aralığına kırp (`np.clip`), `round(..., 4)`
döndürsün.

**Beklenen çıktı:**

```
0.2798
0.0
```
