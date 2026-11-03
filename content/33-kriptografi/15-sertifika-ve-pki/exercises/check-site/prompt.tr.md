`verify_chain`, `date_status` ve `host_matches` hazır. `check_site(chain,
trusted, host, today)` sırasıyla zinciri, site sertifikasının (`chain[0]`)
tarihini ve adını (`subject`) denetlesin; ilk düşen adımın sonucunu
(`verify_chain`'in mesajı, `date_status`'un mesajı ya da `"name
mismatch"`) döndürsün, hepsi geçerse `"ok"`. Başlangıç kodu yalnızca
zincire bakıyor.

**Beklenen çıktı:**

```
ok
expired
name mismatch
```
