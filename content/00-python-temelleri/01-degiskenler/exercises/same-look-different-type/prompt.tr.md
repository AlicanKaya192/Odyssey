Elinde iki değişken var:

```python
x = "5"
y = 5
```

Biri metin, biri sayı. Yalnızca `x` ve `y`'yi (ve gerekirse `int()` /
`str()`) kullanarak beş değişken oluştur:

| Değişken | Değeri | Tipi | Nasıl |
|---|---|---|---|
| `r1` | `"55"` | metin | yalnızca `x` ile |
| `r2` | `10` | sayı | yalnızca `y` ile |
| `r3` | `"555"` | metin | yalnızca `x` ile |
| `r4` | `10` | sayı | `x` ve `y` birlikte |
| `r5` | `"55"` | metin | `y` ve `x` birlikte |

Sonra her birini tipiyle birlikte yazdır (`print(r1, type(r1))`):

```
55 <class 'str'>
10 <class 'int'>
555 <class 'str'>
10 <class 'int'>
55 <class 'str'>
```

`r1` ile `r5` ekranda aynı görünüyor, `r2` ile `r4` de. Ama nasıl
üretildikleri farklı. İşin özü bu: `+` işareti sayılarda toplar, metinlerde
uç uca ekler; metinle sayıyı ise hiç toplamaz.

> Dikkat: Sonuçları kendin yazma (`r1 = "55"` gibi). Her birini `x` ve `y`
> ile işlem yaparak üret.
