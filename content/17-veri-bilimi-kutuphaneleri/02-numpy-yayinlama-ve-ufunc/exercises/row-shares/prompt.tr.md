`row_shares(matrix)` her satırı kendi toplamına bölsün; sonuç 3 basamağa
yuvarlı iç içe liste. Başlangıç kodu toplamı `(n,)` şeklinde bırakıyor:
bazı tablolarda hata veriyor, kare tablolarda sessizce yanlış eksene
bölüyor. `keepdims=True` kullan.

**Beklenen çıktı:**

```
[[0.25, 0.75], [0.5, 0.5]]
```
