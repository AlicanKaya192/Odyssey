`render_rules(rules)` sözlükte **bulunan** kurallar için satır yazsın,
bulunmayanı atlasın. Sıra ve biçim dersteki gibi:

- `max_words` → `Words: at most N.`
- `max_sentences` → `Sentences: at most N.`
- `must_include` → `Mention: a, b.`
- `must_not_include` → `Do not use: x y`

Satırları `"\n"` ile birleştirip döndür.

**Beklenen çıktı:**

```
Words: at most 15.
Mention: tent, zip.
---
Sentences: at most 2.
```
