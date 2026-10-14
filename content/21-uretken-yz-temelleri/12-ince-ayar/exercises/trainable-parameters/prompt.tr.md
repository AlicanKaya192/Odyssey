`count_trainable(sizes, layers)` katman boyutları `sizes` olan bir ağda
(`[64, 32, 10]` → iki katman) yalnızca `layers` listesindeki katmanlar
eğitilirse kaç parametrenin güncellendiğini döndürsün. `i`. katmanın
parametre sayısı `sizes[i] * sizes[i + 1] + sizes[i + 1]` (ağırlıklar ve
sapmalar).

**Beklenen çıktı:**

```
2410
330
```
