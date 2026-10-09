`kmp_count(text, pattern)` fonksiyonunu **KMP** ile yaz: kalıbın metinde kaç
kez geçtiğini döndürsün; üst üste binenler de sayılır. `prefix_table` hazır.

Eşleşme bulunca `k`'yı sıfırlama: `k = table[k - 1]`. `find`, `index`,
`count`, `startswith` yok.

**Beklenen çıktı:**

```
3
18
0
```
