`load_kind(path)` dosyayı güvenli olmayan kipte yüklüyor. Onu güvenli kipe al:
`weights_only=True` ile yükle; dosya reddedilirse (`pickle.UnpicklingError`)
`"refused"`, yüklenirse `"ok"` döndür. Program `ok refused` basmalı.

**Beklenen çıktı:**

```
ok refused
```
