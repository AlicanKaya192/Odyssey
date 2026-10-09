## Fonksiyonlar

| Yazım | Döndürür |
|---|---|
| `re.search(k, metin)` | ilk eşleşme (her yerde) ya da `None` |
| `re.match(k, metin)` | baştaki eşleşme ya da `None` |
| `re.fullmatch(k, metin)` | metnin tamamı uyarsa eşleşme, yoksa `None` |
| `re.findall(k, metin)` | bütün eşleşmelerin listesi |
| `m.group()`, `m.start()`, `m.end()` | bulunan metin, başı, sonu |

## Karakterler

| Yazım | Anlamı |
|---|---|
| `\d` / `\D` | rakam / rakam olmayan |
| `\w` / `\W` | kelime karakteri / olmayan |
| `\s` / `\S` | boşluk / boşluk olmayan |
| `.` | satır sonu dışında herhangi biri |
| `[abc]`, `[a-z0-9]` | listedekilerden biri |
| `[^abc]` | listede olmayan biri |
| `\.`, `\(`, `\?` | özel karakterin kendisi |

## Nicelik ve konum

| Yazım | Anlamı |
|---|---|
| `?` | 0 ya da 1 |
| `*` | 0 ya da daha fazla |
| `+` | 1 ya da daha fazla |
| `{n}`, `{n,}`, `{n,m}` | tam n, en az n, n ile m arası |
| `^`, `$` | metnin başı, sonu |
| `\b` | kelime sınırı |

## Sık kullanılan kalıplar

| Kalıp | Ne bulur |
|---|---|
| `\d+` | tam sayılar |
| `-?\d+` | işaretli tam sayılar |
| `\d+\.\d+` | ondalık sayılar |
| `\d{4}-\d{2}-\d{2}` | ISO tarih biçimi |
| `#\w+` | etiketler (hashtag) |
| `\bkelime\b` | yalnızca bütün kelime |

## Kurallar

- Kalıp her zaman `r"..."`.
- Doğrulamak için `fullmatch`; `search` metnin bir parçası uysa da bulur.
- Kullanıcıdan gelen metni kalıba koymadan önce `re.escape`.
- `flags=re.IGNORECASE`: büyük/küçük harf fark etmez.
