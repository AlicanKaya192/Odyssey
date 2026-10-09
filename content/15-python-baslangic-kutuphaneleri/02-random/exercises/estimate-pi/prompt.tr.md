`estimate_pi(n, seed)` fonksiyonunu yaz: `r = random.Random(seed)` kursun;
`n` kez `x, y = r.random(), r.random()` ile bir nokta alsın ve
`x * x + y * y <= 1` olanları saysın. `4 * içeridekiler / n` değerini
`round(..., 3)` ile döndürsün. Çağrı sırası önemli: önce `x`, sonra `y`.

**Beklenen çıktı:**

```
3.128
3.142
```
