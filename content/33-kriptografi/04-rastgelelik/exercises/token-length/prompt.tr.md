`token_length(bits, alphabet_size)` istenen bit sayısına ulaşmak için
gereken **en kısa** jeton uzunluğunu döndürsün: `bits / log2(a)`, yukarı
yuvarlanmış (`math.ceil`). Aşağı yuvarlamak jetonu hedefin altında bırakır.

Alfabe 2 karakterden küçükse hiçbir uzunluk bit taşımaz; `None` döndür.

**Beklenen çıktı:**

```
62 22
16 32
10 39
1 None
```
