`linear_search(items, target)` fonksiyonunu yaz: listeyi baştan sona gezsin
ve **iki değerli bir demet** döndürsün: `(indeks, adım)`.

- `indeks`: değerin ilk geçtiği yer; yoksa `-1`.
- `adım`: yapılan karşılaştırma sayısı (`items[i] == target` kaç kez
  soruldu).

Boş listede `(-1, 0)` dönmeli.

**Beklenen çıktı:**

```
(0, 1)
(1, 2)
(4, 5)
(-1, 5)
```

En iyi durum 1 adım, en kötü durum (yok ya da sonda) `n` adım.
