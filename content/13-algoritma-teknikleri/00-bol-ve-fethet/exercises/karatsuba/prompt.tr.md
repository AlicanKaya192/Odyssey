`karatsuba(x, y)` fonksiyonunu tamamla: iki negatif olmayan tam sayıyı
**üç** yarım boy çarpımla çarpsın.

- `half = max(len(str(x)), len(str(y))) // 2`
- `a, b = divmod(x, 10 ** half)`, `c, d = divmod(y, 10 ** half)`
- `ac`, `bd` ve `(a + b)(c + d)` özyinelemeyle; orta terim
  `(a + b)(c + d) - ac - bd`
- sonuç `ac * 10 ** (2 * half) + orta * 10 ** half + bd`

Temel durum ve sayaç hazır: `MULTS` tek basamak çarpımlarını sayıyor.
`count_mults` dört çarpımlı bir çözümü yakalar.

**Beklenen çıktı:**

```
7006652
True
33
```
