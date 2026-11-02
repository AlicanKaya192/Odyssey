`otp_encrypt(message, key_hex)` metni (`encode()` ile bayta çevirip)
anahtarla XOR'lasın ve şifreli metni onaltılık olarak döndürsün. Anahtar
mesajdan **kısaysa** `"key too short"` döndürsün; uzunsa yalnızca baştaki
gerekli kısmı kullanılır.

**Beklenen çıktı:**

```
6ad09d5e491260d699234e
b7b6
key too short
```
