İşler bir sözlükte: anahtar işin adı, değer beklediği işlerin listesi.

`unknown_needs(needs)` fonksiyonunu yaz. Var olmayan bir işi bekleyen her durum için `"iş -> beklenen"` metnini, sırayla bir listede döndür. Sorun yoksa boş liste.

- `"build": ["lint", "tests"]` ve `tests` diye bir iş yoksa: `"build -> tests"`

**Beklenen çıktı:**

```
['build -> tests', 'deploy -> approve']
[]
```
