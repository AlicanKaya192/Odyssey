`required` istenen kontroller, `status` kontrol → `"yes"`, `"partial"`
ya da `"no"`. Listede olmayan kontrol `"no"` sayılır.

`gap_report(required, status)` bir sözlük döndürsün:

- `"coverage"`: `"yes"` olanların yüzdesi, `round(..., 1)` ile; `required`
  boşsa `100.0`,
- `"missing"`: `"no"` olanlar, abece sırasında,
- `"partial"`: `"partial"` olanlar, abece sırasında.

**Beklenen çıktı:**

```
coverage: 40.0
missing: ['logging', 'patching']
partial: ['mfa']
```
