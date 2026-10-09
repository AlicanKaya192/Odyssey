`word_counts(words)` fonksiyonunu yaz: bir kelime listesi alsın, her
kelimenin kaç kez geçtiğini bir **sözlükte** döndürsün.

- `["to", "be", "or", "not", "to", "be"]` →
  `{"to": 2, "be": 2, "or": 1, "not": 1}`

`.count()` kullanma: her kelime için listeyi baştan taramak `O(n²)` olur.
Sözlükte tek geçişte say.

**Beklenen çıktı:**

```
{'to': 2, 'be': 2, 'or': 1, 'not': 1}
{}
```
