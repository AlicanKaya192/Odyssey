Python'da "birkaç alanı olan bir kayıt" için en az beş yol var. Aynı noktayı
dördüyle kuralım:

```python
from collections import namedtuple
from dataclasses import dataclass
from typing import TypedDict

PointT = namedtuple("PointT", "x y")


@dataclass
class PointD:
    x: int
    y: int


class PointTD(TypedDict):
    x: int
    y: int


for p in [{"x": 1, "y": 2}, PointT(1, 2), PointD(1, 2), PointTD(x=1, y=2)]:
    print(type(p).__name__, p)
```

```text
dict {'x': 1, 'y': 2}
PointT PointT(x=1, y=2)
PointD PointD(x=1, y=2)
dict {'x': 1, 'y': 2}
```

`TypedDict` çalışma anında düz bir sözlük; fark yalnızca editörün ve tip
denetleyicisinin gözünde.

## Hangisi ne zaman?

| Yapı | Değişebilir mi | Alan erişimi | En iyi olduğu yer |
|---|---|---|---|
| `dict` | evet | `p["x"]` | kısa ömürlü, şekli belirsiz veri |
| `TypedDict` | evet | `p["x"]` | JSON gibi dışarıdan gelen sözlüğe şema |
| `namedtuple` / `NamedTuple` | hayır | `p.x`, `p[0]` | küçük, değişmeyen kayıt; demet yerine |
| `@dataclass` | evet (`frozen` ile hayır) | `p.x` | metotlu, varsayılanlı, doğrulamalı kayıt |
| Pydantic `BaseModel` | evet | `p.x` | dışarıdan gelen veriyi **doğrulamak** (API) |

Kısa kural:

- Bir fonksiyon iki üç değer döndürüyorsa `NamedTuple`.
- Programın kendi nesneleri (ürün, sipariş, ayar) için `@dataclass`.
- JSON'u olduğu gibi taşıyorsan `TypedDict`.
- Gelen verinin türleri gerçekten denetlenmeliyse Pydantic (API Yazmak
  modülünde gördün); `dataclass` türleri denetlemez.
