## El sıkışmanın parçaları

| Mesaj | İçinde | Hangi bölüm |
|---|---|---|
| ClientHello | Sürümler, şifre takımları, anahtar payı | Diffie-Hellman ve Eliptik Eğriler |
| ServerHello | Seçilen sürüm ve takım, anahtar payı | Diffie-Hellman ve Eliptik Eğriler |
| (anahtarlar) | HKDF; etikette döküm özeti; yön başına ayrı | Anahtar Türetme |
| Certificate | Sunucunun sertifika zinciri | Sertifikalar ve PKI |
| CertificateVerify | Döküm özetine sunucunun imzası | Dijital İmza |
| Finished | Bütün el sıkışmanın özetine HMAC | Mesaj Doğrulama: HMAC |
| Uygulama verisi | AEAD ile şifreli kayıtlar | Doğrulanmış Şifreleme |

## Döküm özeti

- Gidip gelen her mesaj **sırasıyla** tek bir özete eklenir.
- Anahtar türetmede, imzada ve Finished'da kullanılır.
- Yolda değişen bir mesaj iki tarafın özetini ayırır; Finished tutmaz.

## Ayarlar

| Konu | Doğrusu |
|---|---|
| Sürüm | TLS 1.3; gerekiyorsa TLS 1.2 |
| Kapalı | SSL 3.0, TLS 1.0, TLS 1.1 |
| TLS 1.3 takımları | `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256` |
| TLS 1.2 takımları | Yalnızca ECDHE + AEAD (GCM ya da ChaCha20-Poly1305) |
| Sertifika doğrulama | Her zaman açık |
| HSTS | `https` kalıcı olsun diye açık |

## Sürüm ve takım seçimi

İstemci desteklediklerini sıralar, sunucu **kendi tercih listesinden**
istemcinin de desteklediği ilkini seçer. Ortak bir seçenek yoksa el
sıkışma bir hatayla biter; zayıf bir seçeneğe "düşmek" yoktur.
