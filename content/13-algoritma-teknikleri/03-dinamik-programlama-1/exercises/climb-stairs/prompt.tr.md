`ways_to_climb(n)` fonksiyonunu yaz: `n` basamaklı bir merdiveni her
adımda **1 ya da 2** basamak çıkarak kaç farklı şekilde çıkabileceğini
döndürsün. `n = 0` için 1 (hiç adım atmamak).

Son basamağa ya bir alttan ya iki alttan gelinir:
`ways[i] = ways[i − 1] + ways[i − 2]`.

Son satır `n = 90`; düz özyineleme hiç bitmez, tablo ya da `@cache` gerekir.

**Beklenen çıktı:**

```
1 1
2 2
3 3
4 5
5 8
90 4660046610375530309
```
