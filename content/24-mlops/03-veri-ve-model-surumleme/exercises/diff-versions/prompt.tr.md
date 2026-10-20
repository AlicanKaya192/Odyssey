Bir verinin iki sürümü satır listesi olarak veriliyor; her satırda bir `"id"` var. `diff_versions(old, new)` fonksiyonunu yaz ve bir sözlük döndür:

- `"added"`: `new`'de olup `old`'da olmayan kimlikler.
- `"removed"`: `old`'da olup `new`'de olmayan kimlikler.
- `"changed"`: ikisinde de olan ama satırı farklı olan kimlikler.

Her liste **sıralı** olsun. Satırların listedeki sırası önemli değil: satırları kimlikle eşleştir.

**Beklenen çıktı:**

```
added ['C4']
removed ['C1']
changed ['C2']
```
