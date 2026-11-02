`endpoint_changes(old, new)` iki sürümün uç nokta listelerini
karşılaştırıp şu sözlüğü döndürsün:

- `"added"`: yalnızca `new`'de olanlar,
- `"removed"`: yalnızca `old`'da olanlar.

İki liste de abece sırasında ve tekrarsız olsun.

**Beklenen çıktı:**

```
added ['/debug', '/export']
removed ['/old']
```
