Üç sayının **ortancasını**, yani ne en büyük ne en küçük olanı bul ve
`middle` değişkenine koy:

```python
a = 17
b = 42
c = 29
```

```
29
```

Kural: `sorted`, `min` ve `max` kullanmak yasak. Yalnızca `if`,
karşılaştırma ve `and` / `or`.

Bir sayının ortanca olması ne demek? Ötekilerden birinden büyük ya da eşit,
ötekinden küçük ya da eşit olması. `a` için bunun iki yolu var: `b <= a <=
c` ya da `c <= a <= b`. Aynı düşünceyi `b` ve `c` için de kur.

> Dikkat: Kodun yalnızca bu üç sayı için değil, her sıralamada çalışmalı.
> Bitince değerleri değiştirip dene (örneğin `a = 42`, `b = 29`,
> `c = 17`; yine `29` çıkmalı), sonra geri al.
