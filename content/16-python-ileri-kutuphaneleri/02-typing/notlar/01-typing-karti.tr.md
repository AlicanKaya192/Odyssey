## Temeller (Python patikası)

| Yazım | Anlamı |
|---|---|
| `x: int`, `def f(a: str) -> bool:` | değişken, parametre, dönüş |
| `list[int]`, `dict[str, float]`, `tuple[int, str]` | kaplar |
| <code>str &#124; None</code> | metin ya da hiçbir şey |
| `-> None` | bir şey döndürmüyor |

## İleri biçimler

| Yazım | Anlamı | Nereden |
|---|---|---|
| `Literal["r", "w"]` | yalnızca bu değerler | `typing` |
| `Final` | yeniden atanmaz | `typing` |
| `type Ad = ...` | tür takma adı (3.12+) | dil |
| `Callable[[int, str], bool]` | fonksiyon türü | `collections.abc` |
| `Iterable[int]`, `Sequence[str]` | "dolaşılabilir", "sıralı" | `collections.abc` |
| `TypedDict` + `NotRequired` | anahtarları belli sözlük | `typing` |
| `NamedTuple` | türlü, adlı demet | `typing` |
| `def f[T](x: T) -> T` | genel fonksiyon (3.12+) | dil |
| `class Box[T]:` | genel sınıf (3.12+) | dil |
| `Any` | denetleme | `typing` |
| `object` | her şey olabilir, önce bak | yerleşik |

## Çalışma anında

| Yazım | Ne verir |
|---|---|
| `f.__annotations__` | belirtimler sözlüğü |
| `typing.get_type_hints(f)` | çözülmüş belirtimler |
| `typing.get_args(Literal["a", "b"])` | `("a", "b")` |
| `isinstance(x, int)` | gerçek denetim |

`isinstance(x, list[int])` çalışmaz: köşeli parantezli tür çalışma anında
denetlenemez.

## Parametre için geniş, dönüş için dar

Parametrede `Iterable[int]` yaz (liste, demet, küme, üreteç hepsi uyar);
dönüşte `list[int]` yaz (çağıran ne aldığını tam bilsin).
