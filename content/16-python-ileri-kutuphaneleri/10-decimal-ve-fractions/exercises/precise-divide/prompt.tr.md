`precise_divide(a, b, digits)` iki metni `Decimal`'a çevirip böler ve
sonucu metin olarak döndürür; bölme `digits` **anlamlı basamakla** yapılmalı.
Başlangıç kodu `getcontext().prec`'i değiştirdiği için bütün programın
duyarlığı bozuluyor (son satır 28 yazmalı). `localcontext()` kullan.

**Beklenen çıktı:**

```
0.14286
0.667
28
```
