`prepare(pixels)` `uint8` piksel değerlerini (0–255) bir `v2.Compose`
zinciriyle ağa hazırlasın: `v2.ToDtype(torch.float32, scale=True)`, sonra
`v2.Normalize([0.5], [0.25])`. Pikselleri `(1, 1, n)` şekilli bir `uint8`
tensör yap; sonucu 3 basamaklı düz liste olarak döndür.

**Beklenen çıktı:**

```
[-2.0, -0.996, 0.008, 2.0]
```
