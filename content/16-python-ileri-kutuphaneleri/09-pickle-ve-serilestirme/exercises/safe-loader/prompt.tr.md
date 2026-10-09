`load_safely(blob)` fonksiyonunu yaz: `pickle.Unpickler`'dan türeyen bir
sınıfta `find_class`'ı ezsin; `(modül, ad)` `ALLOWED` içindeyse üst sınıfın
`find_class`'ını çağırsın, değilse `pickle.UnpicklingError` fırlatsın.
`load_safely` yüklenen nesneyi döndürsün; engellenirse
`"blocked: <modül>.<ad>"` metnini döndürsün. Baytları dosyaya benzetmek
için `io.BytesIO(blob)`.

**Beklenen çıktı:**

```
Counter({'a': 2, 'b': 1, 'c': 1})
blocked: builtins.print
[1, 'x', None]
```
