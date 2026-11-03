`release_blockers(checklist, required)` `required` listesindeki her madde
için kontrol listesine baksın: madde listede **yoksa** ya da değeri
`False` ise yayını engeller. Engelleyen maddeleri abece sırasıyla
döndürsün. Başlangıç kodu olmayan maddede `KeyError` veriyor.

**Beklenen çıktı:**

```
dependencies_scanned
security_tests_pass
```
