İç içe bir JSON'da aradığın değere nasıl ulaşılır: adım adım.

## Örnek yanıt

```json
{
  "city": "Izmir",
  "updated": "2024-03-01T09:00",
  "forecast": [
    {"day": "mon", "temp": 24, "wind": {"speed": 12, "dir": "N"}},
    {"day": "tue", "temp": 21}
  ]
}
```

## Yolu kurmak

"Pazartesi rüzgâr hızı kaç?" sorusunun yolu:

| Adım | İfade | Elindeki |
|---|---|---|
| 1 | `data` | sözlük |
| 2 | `data["forecast"]` | liste (günler) |
| 3 | `data["forecast"][0]` | sözlük (pazartesi) |
| 4 | `data["forecast"][0]["wind"]` | sözlük (rüzgâr) |
| 5 | `data["forecast"][0]["wind"]["speed"]` | `12` |

Her adımda kendine sor: **sözlük mü (ad ile), liste mi (sıra numarasıyla)?**
Emin değilsen `print(type(...))`.

## Eksik alan

Salı kaydında `wind` yok. `data["forecast"][1]["wind"]` `KeyError` verir.
Güvenli yol:

```python
day = data["forecast"][1]
wind = day.get("wind", {})
print(wind.get("speed", "unknown"))   # unknown
```

`get("wind", {})` alan yoksa boş bir sözlük veriyor; ikinci `get` de o boş
sözlükten varsayılanı alıyor. Böylece zincir kopmuyor.

## Bütün günleri dolaşmak

```python
for day in data["forecast"]:
    print(day["day"], day["temp"])
```

Liste içindeki sözlükleri dolaşmak, API yanıtlarıyla yapacağın en sık iş.
Bir sonraki bölüm tam olarak bunu tabloya dökmeyi anlatıyor.
