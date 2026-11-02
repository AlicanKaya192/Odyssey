Her istisna `id`, `owner`, `expires` (`"YYYY-MM-DD"`) ve `compensating`
alanlı bir sözlük; bazı alanlar boş ya da hiç yok.

`policy_exceptions(exceptions, today)` sorunları `"<id>: <sorun>"`
biçiminde döndürsün. İstisnalar `id` sırasında, her istisnada sorunlar bu
sırada:

1. `owner` boş ya da yok → `"no owner"`
2. `expires` boş ya da yok → `"no end date"`; varsa ve `today`'den önceyse
   → `"expired"` (bugün biten hâlâ geçerli)
3. `compensating` boş ya da yok → `"no compensating control"`

Bu biçimdeki tarihler metin olarak karşılaştırılabilir.

**Beklenen çıktı:**

```
EX-1: no owner
EX-1: no compensating control
EX-3: expired
EX-4: no end date
```
