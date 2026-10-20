Kapı tuzağına düşmeyen `fresh_gate(sets, now, max_age, min_gain)` fonksiyonunu yaz. `sets` her biri `"month"`, `"old"` ve `"new"` anahtarlı sözlükler (iki modelin o kümedeki doğruluğu):

- Yalnızca güncel kümeleri kullan: `now - month <= max_age`.
- Güncel küme yoksa `["no fresh set", 0]` döndür.
- Kazanç = güncel kümelerde `new - old` ortalaması, üç basamağa yuvarlanmış.
- Kazanç en az `min_gain` ise `["promote", kazanç]`, değilse `["keep", kazanç]`.

**Beklenen çıktı:**

```
['promote', 0.156]
['keep', -0.095]
['no fresh set', 0]
```
