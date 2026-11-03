`entropy_bits(alphabet, length)` alfabeden rastgele seçilmiş `length`
karakterlik bir jetonun kaç bit taşıdığını `round(..., 1)` ile döndürsün:
`length × log2(a)`.

- `a` alfabedeki **farklı** karakter sayısıdır: `"aabb"` iki karakterdir,
  aynı harfi iki kez yazmak olasılık eklemez.
- Alfabe boşsa `0.0` döndür (`log2(0)` tanımsız).

Başlangıç kodu `len(alphabet)` kullanıyor ve boş alfabede hata veriyor.

**Beklenen çıktı:**

```
19.9
8.0
0.0
```
