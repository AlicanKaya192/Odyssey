## Kopyalamak

| Yazım | Dış kap | İçteki nesneler |
|---|---|---|
| `b = a` | aynı | aynı |
| `copy.copy(a)`, `a.copy()`, `list(a)`, `a[:]` | yeni | **paylaşılır** |
| `copy.deepcopy(a)` | yeni | yeni |

- `x is y`: aynı nesne mi? `x == y`: değerleri eşit mi?
- `[[0] * 3] * 3` aynı listeyi üç kez gösterir; `[[0] * 3 for _ in range(3)]`.
- Demet ve metin gibi değişmez nesnelerde kopya sorunu yoktur.

## pprint

| Yazım | Ne yapar |
|---|---|
| `pprint(veri)` | satırlara bölüp yazdırır |
| `pprint(veri, width=60)` | satır genişliği |
| `pprint(veri, depth=1)` | yalnızca ilk düzey, gerisi `...` |
| `pprint(veri, sort_dicts=False)` | anahtarları sıralama |
| `pformat(veri)` | aynı metni döndürür |

## enum

| Yazım | Ne verir |
|---|---|
| `class Status(Enum): PAID = "paid"` | tanım |
| `Status.PAID.name` / `.value` | `"PAID"` / `"paid"` |
| `Status("paid")` | değerden üye |
| `Status["PAID"]` | addan üye |
| `list(Status)` | bütün üyeler |
| `IntEnum` | tam sayı gibi, sıralanır |
| `Flag` + `auto()` | <code>&#124;</code> ile birleşen seçenekler |

- Üye düz metne eşit değil; JSON'a `value` yazılır.
- Geçersiz değer `ValueError`, yanlış ad `AttributeError`.
