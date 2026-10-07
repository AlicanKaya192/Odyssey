JSON ile çalışırken gereken her şey tek sayfada.

## Dört fonksiyon

| Fonksiyon | Ne yapar |
|---|---|
| `json.loads(metin)` | JSON metnini Python yapısına çevirir |
| `json.dumps(yapı)` | Python yapısını JSON metnine çevirir |
| `json.load(dosya)` | açık dosyadaki JSON'u okur |
| `json.dump(yapı, dosya)` | yapıyı açık dosyaya JSON olarak yazar |

Hatırlama yolu: **`s` = string (metin).** `s` varsa metinle, yoksa dosyayla
çalışıyor.

## Kalıplar

```python
import json

# Dosyadan okumak
with open("data.json", encoding="utf-8") as file:
    data = json.load(file)

# Dosyaya yazmak (okunur biçimde, Türkçe harfler korunarak)
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

# Olmayabilecek alan
email = user.get("email", "no email")

# Dosya yoksa ya da bozuksa varsayılan
try:
    with open("settings.json", encoding="utf-8") as file:
        settings = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    settings = {"theme": "dark"}
```

## JSON ve Python türleri

| JSON | Python |
|---|---|
| `{ }` nesne | `dict` |
| `[ ]` dizi | `list` |
| `"metin"` | `str` |
| `36`, `3.5` | `int`, `float` |
| `true`, `false` | `True`, `False` |
| `null` | `None` |

## JSON yazım kuralları

- Metinler ve anahtarlar **çift tırnak** içinde: `"name"`, tek tırnak yok.
- Anahtar **her zaman metin**: `{1: "a"}` yazılınca `{"1": "a"}` olur.
- `true`, `false`, `null` küçük harfle.
- Son öğeden sonra **virgül yok**.
- Yorum satırı yok.

## Gidip gelince

| Python'da | JSON'dan geri gelince |
|---|---|
| demet `(1, 2)` | liste `[1, 2]` |
| sayı anahtar `{1: "a"}` | metin anahtar `{"1": "a"}` |
| küme `{"a", "b"}` | yazılamaz: önce `sorted(...)` ile listeye çevir |

## İç içe veriyi okumak

```python
data["students"][0]["scores"][1]
```

Soldan sağa: sözlükte **anahtarla**, listede **sırayla** bir adım içeri.
Takılırsan ara adımı `print` ile yazdır ve türüne bak (`type(...)`).
