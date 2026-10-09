## Önbellek

| Yazım | Ne yapar |
|---|---|
| `@lru_cache(maxsize=128)` | son kullanılan 128 sonucu sakla |
| `@lru_cache(maxsize=None)` / `@cache` | sınırsız sakla |
| `f.cache_info()` | isabet, kaçırma, boyut |
| `f.cache_clear()` | önbelleği boşalt |
| `@cached_property` | özelliği bir kez hesapla, nesnede sakla |

Yalnızca aynı girdiye hep aynı sonucu veren fonksiyonlarda; argümanlar
değiştirilemez (hashable) olmalı.

## Fonksiyon üretmek

| Yazım | Ne verir |
|---|---|
| `partial(f, a, b=2)` | argümanları sabitlenmiş yeni fonksiyon |
| `reduce(f, dizi, başlangıç)` | soldan sağa tek değere indirmek |
| `operator.add`, `mul`, `itemgetter("ad")` | işleçlerin fonksiyon hâli |

## Dekoratörler

| Yazım | Ne yapar |
|---|---|
| `@wraps(func)` | sarmalayıcıya asıl adı ve açıklamayı kopyalar |
| `@total_ordering` | `__eq__` + `__lt__`'ten bütün karşılaştırmalar |
| `@singledispatch` + `.register` | ilk argümanın türüne göre sürüm |

## Dekoratör iskeleti

```python
from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # önce
        result = func(*args, **kwargs)
        # sonra
        return result
    return wrapper
```
