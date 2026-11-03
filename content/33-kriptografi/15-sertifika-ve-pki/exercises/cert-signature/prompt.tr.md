`digest` hazır. `check_signature(cert, e, n)` sertifikanın imzasını CA'nın
açık anahtarıyla doğrulasın. İmzalanan baytlar, **`signature` dışındaki**
alanların `json.dumps(..., sort_keys=True).encode()` hâlidir. Başlangıç
kodu imzanın kendisini de imzalanan veriye katıyor ve doğru sertifikayı
reddediyor.

**Beklenen çıktı:**

```
True
False
```
