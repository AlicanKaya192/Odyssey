`most_frequent(items)` fonksiyonunu yaz: en sık geçen değeri ve kaç kez
geçtiğini `(değer, sayı)` demeti olarak döndürsün. Eşitlikte **listede önce
görülen** değer kazansın. Boş listede `None`.

- `["b", "a", "b", "c", "a"]` → `("b", 2)` (a da 2 kez ama b önce görüldü)

Bir sayaç sözlüğü kur. `.count()`, `Counter` ve `most_common` kullanma.
Sözlük ekleme sırasını koruduğu için sayaçları gezerken **kesin büyük** (`>`)
olanı seçmek eşitlikte ilkini bırakır.

**Beklenen çıktı:**

```
('b', 2)
(3, 3)
None
```
