Gövdeden gelen `422` cevaplarının türleri ve ne anlama geldikleri.
`loc` her zaman `body` ile başlar; sonraki öğe alanın adı (iç içe modelde
yol: `["body", "author", "name"]`, listede sıra: `["body", "items", 0,
"price"]`).

| `type` | Örnek gövde | Anlamı |
|---|---|---|
| `missing` | `{"title": "Dune"}` | Zorunlu alan yok (`year`) |
| `missing` (`loc: ["body"]`) | gövde yok | Hiç gövde gönderilmedi |
| `int_parsing` | `{"year": "nineteen"}` | Sayıya çevrilemedi |
| `int_from_float` | `{"year": 1965.5}` | Kesirli sayı tam sayı olamaz |
| `string_type` | `{"title": 5}` | Metin bekleniyordu |
| `list_type` | `{"tags": "sf"}` | Liste bekleniyordu |
| `model_attributes_type` | `{"author": "Austen"}` | Nesne bekleniyordu |
| `json_invalid` | `{bad json` | JSON hiç okunamadı |

## Hata ayıklarken

1. Önce `loc`: hangi alan?
2. Sonra `type` ve `msg`: ne bekleniyordu?
3. `input`: ne geldi? Çoğu zaman yazım ya da tırnak hatası.

İstemci tarafında (`requests`) en sık sebep: `json=` yerine `data=`
kullanmak. `data=` gövdeyi form olarak gönderiyor (`title=Dune&year=1965`);
FastAPI JSON nesnesi beklediği için `422` geliyor: `type:
model_attributes_type`, `loc: ["body"]` (ölçtük).

## Fazladan alanlar

Modelde olmayan alanlar hata vermeden atılır. İstemcinin yanlış alan adı
yazdığını yakalamak istiyorsan modele şu satır eklenir:

```python
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    year: int
```

Böylece `{"title": "Dune", "year": 1965, "yaer": 1}` → `422`
(`extra_forbidden`).
