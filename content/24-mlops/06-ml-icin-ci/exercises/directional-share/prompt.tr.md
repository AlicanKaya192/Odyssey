Bir yön testinde her müşterinin değişiklikten **önceki** (`before`) ve **sonraki** (`after`) olasılıkları aynı sırayla veriliyor. Olasılığın düşmemesi bekleniyor. `directional_share(before, after, tolerance)` fonksiyonunu yaz:

- Sonraki olasılık, önceki eksi `tolerance`'tan küçük değilse test o müşteride tuttu sayılır (çok küçük düşüşler hoş görülür).
- Tutan müşterilerin payını üç basamağa yuvarlayıp döndür.
- Liste boşsa `None`.

**Beklenen çıktı:**

```
0.75
1.0
None
```
