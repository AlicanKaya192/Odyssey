`pick_suite(client_suites, server_suites)` sunucunun seçimini yapsın:
sunucunun **kendi tercih sırasıyla** baktığı listeden istemcinin de
desteklediği ilk takımı döndürsün; ortak takım yoksa
`"handshake_failure"`. Başlangıç kodu her zaman istemcinin ilk takımını
alıyor; sunucu onu desteklemiyor olabilir.

**Beklenen çıktı:**

```
TLS_AES_128_GCM_SHA256
handshake_failure
```
