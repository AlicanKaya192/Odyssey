Dersteki adımları bir fonksiyona dök: `hotp(secret, counter, digits=6)`.

- `secret` bir metin; HMAC'e vermeden önce `encode()` ile bayta çevir.
- Sayaç 8 baytlık büyük uçlu (`"big"`) sayı olarak mesaj olur.
- HMAC-SHA1, dinamik kesme, `& 0x7FFFFFFF`, `% 10**digits`.
- Sonucu `digits` uzunluğunda **metin** olarak döndür (`zfill`).

Denemek için standardın sırrı: `"12345678901234567890"`.

**Beklenen çıktı:**

```
0 755224
1 287082
2 359152
3 969429
94287082
```
