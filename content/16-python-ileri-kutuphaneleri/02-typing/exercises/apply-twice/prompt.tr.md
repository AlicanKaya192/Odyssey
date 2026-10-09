`apply_twice(func, value)` fonksiyonunu yaz: `func`'ı `value`'ya iki kez
uygulasın (`func(func(value))`). Belirtimler: `func: Callable[[int], int]`,
`value: int`, dönüş `int`. `Callable`'ı `collections.abc`'den al.

**Beklenen çıktı:**

```
12
21
```
