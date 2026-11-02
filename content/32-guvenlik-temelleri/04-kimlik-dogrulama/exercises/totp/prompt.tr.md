`hotp` başlangıç kodunda hazır. TOTP, sayaç yerine saati kullanan HOTP'dir.

`totp(secret, unix_time, step=30, digits=6)` fonksiyonunu yaz: sayaç
`unix_time // step`, kod `hotp(secret, sayac, digits)`.

**Beklenen çıktı:**

```
59 287082
1111111109 081804
1234567890 005924
94287082
```
