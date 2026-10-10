İki fonksiyon yaz:

- `sign(key, message)`: `hmac.new` ile SHA-256 imzasını onaltılık metin
  olarak döndür (`key` ve `message` metin; ikisini de `encode()` et).
- `verify(key, message, tag)`: imzayı yeniden hesaplayıp
  `hmac.compare_digest` ile karşılaştır.

Başlangıç kodu anahtarı kullanmıyor: herkes aynı "imzayı" üretebilir.

**Beklenen çıktı:**

```
e3b44dc2cb859682
True False
```
