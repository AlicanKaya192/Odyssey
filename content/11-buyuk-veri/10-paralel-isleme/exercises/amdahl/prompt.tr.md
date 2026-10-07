Amdahl yasasıyla hızlanmayı hesaplayan bir fonksiyon yaz.

**Yapman gerekenler:**

`speedup(p, n)` fonksiyonunu yaz:

- `p`: işin paralel yapılabilen oranı (0 ile 1 arası),
- `n`: çekirdek sayısı,
- dönüş: `1 / ((1 - p) + p / n)`, **iki ondalığa** yuvarlanmış.

Örnekler:

- `speedup(0.9, 4)` → `3.08`
- `speedup(0.9, 24)` → `7.27`
- `speedup(0.5, 4)` → `1.6`
