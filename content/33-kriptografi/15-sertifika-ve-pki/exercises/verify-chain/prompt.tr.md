`digest`, `tbs` ve `check_signature` hazır. `verify_chain(chain,
trusted)` siteden köke doğru her halkayı denetliyor ama zincirin
tepesindeki kökün **güven deposunda** olup olmadığına bakmıyor. Ekle:
`trusted` adı `[e, n]`'e eşleyen bir sözlük; tepedeki sertifikanın adı ve
anahtarı orada yoksa `"untrusted root"` döndür.

**Beklenen çıktı:**

```
ok
untrusted root
```
