Dekoratör, "her fonksiyona aynı ek iş" demektir: sayaç, süre ölçmek, kayıt
tutmak, yeniden denemek. İki kalıp çoğu işi görür.

## Sayaç ve yeniden deneme

```python
from functools import wraps


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls
def add(a, b):
    return a + b


add(1, 2)
add(3, 4)
print(add.calls, add.__name__)


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as error:
                    print(f"attempt {attempt} failed: {error}")
            raise RuntimeError("giving up")
        return wrapper
    return decorator


answers = iter(["x", "y", "42"])


@retry(times=3)
def read_number():
    return int(next(answers))


print(read_number())
```

```text
2 add
attempt 1 failed: invalid literal for int() with base 10: 'x'
attempt 2 failed: invalid literal for int() with base 10: 'y'
42
```

- **`count_calls`**: sarmalayıcı her çağrıda sayacı artırıp asıl fonksiyonu
  çağırıyor. Fonksiyonlar da nesnedir; `wrapper.calls` gibi bir özellik
  taşıyabilir.
- `@wraps(func)` sayesinde `add.__name__` hâlâ `add`.

## Argümanlı dekoratör nasıl çalışır?

`@retry(times=3)` yazınca önce `retry(times=3)` çağrılır ve **asıl
dekoratörü** döndürür; o da fonksiyonu sarar. Bu yüzden üç kat iç içe
fonksiyon var:

| Kat | Ne alır | Ne döndürür |
|---|---|---|
| `retry(times)` | ayar | dekoratör |
| `decorator(func)` | fonksiyon | sarmalayıcı |
| `wrapper(*args, **kwargs)` | çağrının argümanları | sonuç |

Örnekte ilk iki deneme `int("x")` ve `int("y")` yüzünden düştü, üçüncüde
`42` geldi. Bütün denemeler düşseydi `RuntimeError` yükselirdi.

## Ne zaman dekoratör?

- Aynı ek iş birçok fonksiyonda tekrarlanıyorsa (ölçmek, kaydetmek,
  denetlemek).
- Asıl fonksiyonun kodu o işi bilmek zorunda olmamalıysa.

Tek bir yerde kullanılacak bir şey için dekoratör yazma; düz bir fonksiyon
çağrısı daha açıktır. Hazır dekoratörlerin çoğu (`lru_cache`, `property`,
`staticmethod`, `dataclass`) zaten bu kalıbı kullanıyor.
