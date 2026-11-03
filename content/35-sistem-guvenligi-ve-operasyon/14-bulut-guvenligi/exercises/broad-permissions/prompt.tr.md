`broad_permissions(policy)` `allow` etkili olup işlemi tam `"*"` olan ya
da `":*"` ile biten ifadelerin işlemlerini **bir kez** ve abece sırasıyla
döndürsün. `deny` ifadeleri sayılmaz: geniş bir yasak sorun değildir.

**Beklenen çıktı:**

```
['*', 'compute:*']
```
