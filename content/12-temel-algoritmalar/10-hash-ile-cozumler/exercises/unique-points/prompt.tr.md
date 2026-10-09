Bir `Point` sınıfı yaz: `x` ve `y` tutsun; **içeriği aynı iki nokta eşit
sayılsın** ve kümede tek eleman olsun. Bunun için `__eq__` ve `__hash__`
yaz (hash için `(x, y)` demetini kullan).

Sonra `count_unique(pairs)` fonksiyonunu yaz: `[x, y]` çiftlerinden `Point`
nesneleri kurup bir kümeye koysun ve kümenin boyunu döndürsün.

**Beklenen çıktı:**

```
2
0
True
```

`__hash__` olmadan aynı noktalar kümede ayrı ayrı sayılırdı.
