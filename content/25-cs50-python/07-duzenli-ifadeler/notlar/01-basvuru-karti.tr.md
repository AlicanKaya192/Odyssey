Hafta 7'de geçen her şey tek sayfada. Kalıplar hep ham dize: `r"..."`.

## Fonksiyonlar

`import re` ile:

| Yazım | Ne yapar |
|---|---|
| `re.search(kalıp, dize)` | dizenin herhangi bir yerinde arar; eşleşme ya da `None` |
| `re.match(kalıp, dize)` | yalnızca dizenin başından eşleşir |
| `re.fullmatch(kalıp, dize)` | dizenin tamamı kalıba uymalı |
| `re.sub(kalıp, yerine, dize)` | bulduklarını değiştirir; tutmazsa dize aynen döner |
| `re.findall(kalıp, dize)` | bütün eşleşmelerin listesi (grup varsa grupların) |
| `re.split(kalıp, dize)` | kalıba göre böler |

Üçüncü argüman bayrak: `re.IGNORECASE` (büyük/küçük harf fark etmez),
`re.MULTILINE`, `re.DOTALL`.

## Tekrar

| İşaret | Anlamı |
|---|---|
| `*` | sıfır ya da daha fazla |
| `+` | bir ya da daha fazla |
| `?` | sıfır ya da bir (isteğe bağlı) |
| `{m}` | tam `m` tane |
| `{m,n}` | `m` ile `n` arası |

Hepsi **soldaki tek şeye** uygulanır: `ab+` `abbb`'yi tutar, `abab`'ı değil;
`(ab)+` ikisini de.

## Karakterler ve kümeler

| İşaret | Anlamı |
|---|---|
| `.` | satır sonu dışında herhangi bir karakter |
| `\.` | harfiyen nokta (kaçış) |
| `[abc]` | `a`, `b` ya da `c` |
| `[a-z]` | aralık |
| `[^@]` | `@` dışındaki herhangi bir karakter |
| `\d` / `\D` | rakam / rakam olmayan |
| `\s` / `\S` | boşluk karakteri / boşluk olmayan |
| `\w` / `\W` | harf, rakam, `_` / bunların dışı |
| `\b` | kelime sınırı (karakter değil, bir yer) |

## Yer ve gruplar

| Yazım | Anlamı |
|---|---|
| `^` | dizenin başı (köşeli parantezin dışında) |
| `$` | dizenin sonu |
| <code>A&#124;B</code> | A ya da B |
| `(...)` | grup; içindekini yakalar |
| `(?:...)` | grup, yakalamaz |

## Eşleşme nesnesi

| Yazım | Ne verir |
|---|---|
| `matches.group(0)` | eşleşmenin tamamı |
| `matches.group(1)` | birinci grup (gruplar 1'den sayılır) |
| `matches.groups()` | bütün gruplar, demet olarak |
| `if matches := re.search(...):` | ata ve sor (mors işleci) |

## Dersin kalıpları

| Kalıp | İş |
|---|---|
| `r"^\w+@(\w+\.)?\w+\.edu$"` | `.edu` e-posta adresi, isteğe bağlı alt alan |
| `r"^(.+), *(.+)$"` | `Soyad, Ad` → iki grup |
| `r"^(https?://)?(www\.)?twitter\.com/"` | adresin başı (`re.sub` ile atmak için) |
| `r"(?:www\.)?twitter\.com/([a-z0-9_]+)"` | kullanıcı adını yakalamak |

Gerçek bir programda e-posta adresini kendi kalıbınla değil, yaygın bir
kütüphaneyle doğrula (`validators`).
