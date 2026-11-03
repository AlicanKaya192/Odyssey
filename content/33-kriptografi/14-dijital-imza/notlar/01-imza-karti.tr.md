## İmzalama ve doğrulama

| Adım | Kim | İşlem |
|---|---|---|
| Özet | İmzalayan | `h = sha256(mesaj)` |
| İmza | İmzalayan (özel anahtar) | `s = imzala(h, özel)` |
| Gönder | | `mesaj`, `s` |
| Doğrula | Herkes (açık anahtar) | `doğrula(s, özet(mesaj), açık)` |

Oyuncak RSA'da: `s = pow(h, d, n)`, doğrulama `pow(s, e, n) == h`.

## Ne söyler

- **Bütünlük:** mesaj imzalandıktan sonra değişmedi.
- **Kaynak:** bu özel anahtarın sahibi imzaladı.
- **İnkâr edilemezlik:** imzalayan sonradan "ben değildim" diyemez.

Gizlilik **sağlamaz**: imzalı mesaj açıkta durur. Gizlilik de gerekiyorsa
mesaj ayrıca şifrelenir.

## Algoritmalar

| | RSA-PSS | ECDSA | Ed25519 |
|---|---|---|---|
| Anahtar | 2048+ bit | 256 bit | 256 bit |
| İmza başına rastgele sayı | Dolguda | **Gerekir, asla tekrar etmez** | Gerekmez (belirleyici) |
| Not | Ders kitabı RSA imzası kullanılmaz | Sayı tekrarı özel anahtarı açar | Yeni sistemlerde sık seçilir |

## Doğrulayanın kuralları

1. Önce imza, sonra içerik: imza tutmazsa mesajın hiçbir alanı kullanılmaz.
2. Doğru açık anahtarla doğrula: anahtar sertifikadan ya da önceden
   güvenilir bir yoldan gelir, mesajın içinden değil.
3. İmzalı içerikte sürüm ya da tarih varsa onu da denetle: eski ama geçerli
   imzalı bir sürümün yeniden kurulmasını engellemek için.
