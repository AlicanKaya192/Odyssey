Sıralı kutu sınırları (`edges`) veriliyor; `n` sınır `n + 1` kutu yapar. `bin_shares(values, edges)` fonksiyonunu yaz:

- Her değerin kutusu `bisect.bisect_left(edges, value)`: değerden küçük kaç sınır varsa o numara. Sınıra eşit değer o sınırın **solundaki** kutuya düşer.
- Her kutuya düşen değerlerin payını üç basamağa yuvarlayıp kutu sırasıyla döndür.

**Beklenen çıktı:**

```
[0.2, 0.4, 0.2, 0.2]
[0.25, 0.25, 0.25, 0.25]
```
