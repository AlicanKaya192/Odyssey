Matriste bir öznenin satırında `"*"` anahtarı **bütün nesneler** demek.
Örneğin `{"*": ["read"], "grades": ["write"]}` her şeyi okuyabilir, ayrıca
`grades`'e yazabilir.

`effective_actions(matrix, subject, obj)` öznenin o nesnede yapabileceği
eylemleri, `obj` satırındakilerle `"*"` satırındakilerin birleşimi olarak,
**tekrarsız ve abece sırasında** bir liste olarak döndürsün. Bilinmeyen
özne ya da nesne için boş liste.

**Beklenen çıktı:**

```
['read', 'write']
['read']
[]
[]
```
