## string

| Ad | İçerik |
|---|---|
| `ascii_lowercase` / `ascii_uppercase` | a–z / A–Z |
| `ascii_letters` | ikisi birden |
| `digits` | 0–9 |
| `punctuation` | `!"#$%&'()*+,-./:;<=>?@[\]^_` ve diğerleri |
| `whitespace` | boşluk, sekme, satır sonu |
| `Template("...$ad...")` | `substitute`, `safe_substitute` |

Silmek: `metin.translate(str.maketrans("", "", string.punctuation))`.

## textwrap

| Fonksiyon | Ne yapar |
|---|---|
| `wrap(m, width=40)` | satır listesi |
| `fill(m, width=40)` | satırları birleştirilmiş tek metin |
| `shorten(m, width=40, placeholder="...")` | kelime sınırında kısalt |
| `indent(m, "> ")` | her satıra önek |
| `dedent(m)` | ortak baş boşluğu sil |

## difflib

| Fonksiyon | Ne verir |
|---|---|
| `SequenceMatcher(None, a, b).ratio()` | benzerlik 0–1 |
| `get_close_matches(k, seçenekler, n=3, cutoff=0.6)` | en benzerler |
| `unified_diff(eski, yeni, lineterm="")` | `git diff` biçiminde fark |

## unicodedata

| Fonksiyon | Ne yapar |
|---|---|
| `normalize("NFC", m)` | birleşik biçim (karşılaştırmadan önce) |
| `normalize("NFD", m)` | ayrıştırılmış biçim (aksan atmadan önce) |
| `category(ch)` | `Mn` aksan, `Lu` büyük harf, `Nd` rakam... |
| `name(ch)` | karakterin Unicode adı |

## Türkçe

- `"İ".lower()` iki karakter; `"I".lower()` `i` (Türkçede `ı`).
- Önce `I`/`İ` çevir, sonra `lower()`; ya da tersi `upper()` için.
- `sorted` Türkçe abeceyi bilmez: kendi `key` fonksiyonun.
