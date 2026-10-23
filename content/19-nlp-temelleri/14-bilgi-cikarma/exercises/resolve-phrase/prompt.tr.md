`resolve(phrase, reference)` `"today at 9am"`, `"tomorrow at 7pm"` ya da
`"in 3 days at 10am"` gibi bir ifadeyi, referans an `reference`'a (ISO
biçimli metin, ör. `"2026-03-14T01:30:00+03:00"`) göre çözsün:

- Büyük/küçük harf önemli değil; ifadenin **tamamı** bu biçimde olmalı,
  değilse `"rejected"`.
- `am`/`pm` yoksa `"needs_clarification"`.
- Saat 1–12 arasında değilse `"rejected"`. `12am` gece yarısı, `12pm` öğlen.
- Sonuç, referansın saat dilimiyle `isoformat()`:
  `"2026-03-15T19:00:00+03:00"`.

**Beklenen çıktı:**

```
2026-03-16T09:00:00+03:00
2026-03-15T00:00:00+03:00
needs_clarification
rejected
```
