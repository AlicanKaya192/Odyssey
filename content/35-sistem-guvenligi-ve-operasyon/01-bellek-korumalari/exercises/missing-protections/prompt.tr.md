Her program bir sözlük: `name` ve koruma adları → `True` / `False`.
Zorunlu korumalar `canary`, `nx`, `pie`. `missing_protections(binary)`
eksik olanları abece sırasıyla bir liste olarak döndürsün. Bir koruma
sözlükte **hiç yoksa** da eksik sayılır (varsayılmaz, denetlenir).

**Beklenen çıktı:**

```
app: ok
tool: canary, pie
old: canary, nx, pie
```
