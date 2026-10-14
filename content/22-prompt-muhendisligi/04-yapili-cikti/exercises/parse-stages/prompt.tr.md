`parse_json(text)` dersteki gibi üç yolu sırayla denesin: metnin kendisi,
kod bloğu işaretleri atılmış hâli
(`` re.sub(r"^`{3}(?:json)?\s*|\s*`{3}$", "", text.strip()) ``) ve ilk `{`
ile son `}` arasındaki parça. İlk başaranı `[veri, yolun adı]` olarak
döndürsün (adlar `"as is"`, `"fence"`, `"braces"`); hiçbiri başarmazsa
`[None, "failed"]`.

**Beklenen çıktı:**

```
[{'a': 1}, 'as is']
[{'a': 2}, 'fence']
[{'a': 3}, 'braces']
[None, 'failed']
```
