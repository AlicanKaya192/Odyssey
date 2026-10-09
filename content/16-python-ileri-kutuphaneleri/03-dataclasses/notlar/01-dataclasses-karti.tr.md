## Tanım

```python
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    stock: int = 0

    def total(self) -> float:
        return self.price * self.stock
```

## @dataclass seçenekleri

| Seçenek | Ne yapar |
|---|---|
| `frozen=True` | değişmez, hash'lenebilir (küme, sözlük anahtarı) |
| `order=True` | `<`, `>`, `sorted`, `max` (alan sırasıyla) |
| `slots=True` | yalnızca tanımlı alanlar, daha az bellek |
| `kw_only=True` | alanlar yalnızca adıyla |
| `eq=False` | `__eq__` üretme (kimliğe göre karşılaştır) |

## field

| Yazım | Ne yapar |
|---|---|
| `field(default_factory=list)` | her nesneye yeni liste |
| `field(init=False)` | `__init__`'te istenmez |
| `field(repr=False)` | yazdırırken gizle (parola gibi) |
| `field(compare=False)` | karşılaştırmaya katma |

## Yardımcılar

| Yazım | Ne verir |
|---|---|
| `asdict(obj)` | sözlük (iç içe de) |
| `astuple(obj)` | demet |
| `replace(obj, alan=değer)` | değişmiş yeni nesne |
| `fields(Sınıf)` | alan bilgileri |
| `Sınıf(**sözlük)` | sözlükten nesne |

## Hatırla

- Varsayılanlılar varsayılansızlardan sonra.
- `= []` olmaz; `field(default_factory=list)`.
- `__post_init__` doğrulama için.
- `dataclass` türleri denetlemez.
