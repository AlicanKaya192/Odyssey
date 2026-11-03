Kod incelemesinde ya da bir projeyi devralırken kriptografi kısmına
bakarken bu sorular sırayla sorulur.

## Kod

- [ ] Gizli değerler `secrets` ile mi üretiliyor? (`random` yok)
- [ ] Kaynakta tırnak içinde yazılmış anahtar, parola ya da jeton var mı?
- [ ] Etiket ve özet karşılaştırmaları `hmac.compare_digest` ile mi?
- [ ] Kendi yazılmış şifre, kip ya da dolgu kodu var mı? (Olmamalı.)
- [ ] Çözülen veri, etiket doğrulanmadan kullanılıyor mu?

## Ayarlar

| Ayar | Kabul | Red |
|---|---|---|
| Özet | SHA-256, SHA-384, SHA-512, SHA-3, BLAKE2 | MD5, SHA-1 |
| Simetrik | AES-GCM, ChaCha20-Poly1305 | ECB, doğrulamasız CBC/CTR, DES, RC4 |
| AES anahtarı | 128, 192, 256 bit | Daha kısa |
| RSA anahtarı | 2048+ bit, OAEP / PSS | 1024 ve altı, dolgusuz |
| Eğri | 256+ bit (X25519, P-256, Ed25519) | Daha kısa |
| Parola KDF | Argon2id, scrypt, PBKDF2 (yüz binlerce tekrar) | Tek özet, tuzsuz |
| Nonce / IV | Her mesajda benzersiz | Sabit, sayaç sıfırlanıyor |
| TLS | 1.3, güçlü 1.2; doğrulama açık | 1.0, 1.1, `verify=False` |

## Anahtar yönetimi

- [ ] Anahtarlar sır kasasında ya da ortam değişkeninde mi?
- [ ] Her amaç için ayrı anahtar var mı (şifreleme, MAC, imza)?
- [ ] Anahtar döndürme (değiştirme) planı var mı?
- [ ] Sızan anahtar için ne yapılacağı yazılı mı?
