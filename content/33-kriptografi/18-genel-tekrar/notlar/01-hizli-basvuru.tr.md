## Python standart kütüphanesi

| İş | Kod |
|---|---|
| Rastgele anahtar / jeton | `secrets.token_bytes(32)`, `secrets.token_hex(16)` |
| Özet | `hashlib.sha256(veri).hexdigest()` |
| HMAC | `hmac.new(anahtar, mesaj, hashlib.sha256).digest()` |
| Güvenli karşılaştırma | `hmac.compare_digest(a, b)` |
| Paroladan anahtar | `hashlib.pbkdf2_hmac("sha256", parola, tuz, tekrar, dklen=32)` |
| Bellek isteyen KDF | `hashlib.scrypt(parola, salt=tuz, n=2**14, r=8, p=1, dklen=32)` |
| Büyük üs, ters | `pow(a, e, n)`, `pow(a, -1, n)` |
| Bayt ↔ sayı | `int.from_bytes(b, "big")`, `n.to_bytes(uzunluk, "big")` |
| Bayt ↔ onaltılık | `b.hex()`, `bytes.fromhex(metin)` |

Standart kütüphanede **yok**: AES, ChaCha20, RSA, ECDH, Ed25519. Bunlar
denenmiş bir kriptografi kütüphanesinden kullanılır.

## Doğru seçimler

| İhtiyaç | Seçim |
|---|---|
| Veriyi şifrele | AES-256-GCM ya da ChaCha20-Poly1305 (AEAD) |
| Mesaj bütünlüğü (paylaşılan anahtar) | HMAC-SHA256 |
| Dosya özeti | SHA-256 |
| Parola saklama / paroladan anahtar | Argon2id; yoksa scrypt ya da PBKDF2 (600 000+) |
| Tek sırdan çok anahtar | HKDF, amaç başına `info` |
| Anahtar değişimi | X25519 (geçici, ileri gizlilik) |
| İmza | Ed25519; ya da ECDSA, RSA-PSS (2048+) |
| Bağlantı | TLS 1.3, sertifika doğrulaması açık |

## Asla

- Gizli değer için `random`.
- ECB; aynı anahtarla nonce tekrarı; doğrulamasız şifreleme.
- MD5 / SHA-1 ile bütünlük; tuzsuz, hızlı parola özeti.
- Dolgusuz RSA; 2048 bitten kısa RSA.
- Koda gömülü sır; `verify=False`.
- Kendi şifre algoritmanı yazmak.
