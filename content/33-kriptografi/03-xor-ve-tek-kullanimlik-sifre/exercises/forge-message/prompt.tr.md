Şifreli metnin düz hâli `old` olarak biliniyor. `forge(cipher_hex, old,
new)` anahtarı kullanmadan, çözüldüğünde `new` veren yeni şifreli metni
onaltılık döndürsün: yama = `old ^ new`, yeni şifreli metin = `cipher ^
yama`. `old` ve `new` aynı uzunlukta değilse `None`.

**Beklenen çıktı:**

```
6ad09d5e491260d691234e
PAY BOB 900
None
```
