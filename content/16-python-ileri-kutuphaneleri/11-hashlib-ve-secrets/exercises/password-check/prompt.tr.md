İki fonksiyon yaz:

- `hash_password(password, salt_hex)`: `salt_hex`'i `bytes.fromhex` ile
  baytlara çevir, `hashlib.pbkdf2_hmac("sha256", ...)` ile **100 000** tekrarla
  özet al ve onaltılık metin döndür.
- `check_password(password, salt_hex, key_hex)`: aynı tuzla yeniden hesapla ve
  `hmac.compare_digest` ile karşılaştır.

**Beklenen çıktı:**

```
ed2bacebbe4b33a2 64
True False
```
