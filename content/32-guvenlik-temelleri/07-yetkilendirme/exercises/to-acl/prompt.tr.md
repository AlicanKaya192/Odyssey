`to_acl(matrix)` matrisi nesne nesne bir erişim listesine çevirsin:
anahtar nesne, değer `"ozne:eylem"` metinlerinin **abece sırasında**
listesi. Hiç izni olmayan nesne sözlüğe girmesin.

Örnek: `{"ada": {"grades": ["read", "write"]}}` →
`{"grades": ["ada:read", "ada:write"]}`.

**Beklenen çıktı:**

```
grades ada:read, ada:write, alan:read
payroll alan:read
```
