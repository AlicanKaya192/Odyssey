Her yeni API yanıtında aynı tarif. Kod parçalarını kopyalayıp uyarlayabilirsin.

## Tarif

```python
import csv

# 1) Zarfı aç
items = response["data"]

# 2-5) Her kayıttan düz bir satır
rows = []
for item in items:
    author = item.get("author", {})
    rows.append({
        "id": item["id"],                                  # 2) seçilen sütun
        "title": item.get("title", ""),
        "author_name": author.get("name", ""),             # 3) iç içe alan
        "author_country": author.get("country", "unknown"),
        "tags": "|".join(item.get("tags", [])),            # 4) liste → tek hücre
        "price": float(item["price"]),                     # 5) tür düzeltme
    })

# Dosyaya yaz
with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
```

`writer.writerows(rows)` bütün satırları tek seferde yazar; döngüyle
`writerow` yazmanın kısası.

## Liste → ayrı satırlar

```python
pairs = []
for item in items:
    for tag in item.get("tags", []):
        pairs.append({"book_id": item["id"], "tag": tag})
```

İki iç içe döngü: dıştaki kitapları, içteki o kitabın etiketlerini dolaşıyor.

## Kontrol listesi

- Kayıt listesi hangi anahtarda? (`data`, `items`, `results`)
- `meta` / `total` elimdekinin hepsi olmadığını söylüyor mu?
- Her alan her kayıtta var mı? Yoksa `get` ve varsayılan.
- Listeler: birleştir mi, ayrı satır mı?
- Sayılar metin olarak mı geliyor?
- Sütun adları tutarlı mı? (`author_name`, `author_country`)
