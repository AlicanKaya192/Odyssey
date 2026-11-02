`pbkdf2_hex` hazır. `make_record(password, salt_hex, iterations)` şu biçimde
tek bir metin döndürsün; parçalar `$` işaretiyle ayrılır:

`pbkdf2_sha256` · yineleme sayısı · tuz (hex) · özet (hex)

Örneğin `pbkdf2_sha256$1000$8f2a...$1c0e...`.

**Beklenen çıktı:**

```
pbkdf2_sha256
1000
8f2a1c9e5b7d3f60a4c2e8b1d6f09a37
67af6c9fbd0e983a5d9de90813f30d2fd211
```
