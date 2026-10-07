Kimlik doğrulamada yapılacaklar ve yapılmayacaklar, tek listede.

## Yap

- Şifreyi **tuzlu ve yavaş** bir özetle sakla (`pbkdf2_hmac`, `bcrypt`,
  `argon2`). Her kullanıcıya ayrı tuz.
- Özetleri `hmac.compare_digest` ile karşılaştır.
- Jetonu ve anahtarı `secrets` modülüyle üret (`token_hex`, `token_urlsafe`).
- Anahtarı ve jetonu **başlıkta** gönder/oku.
- Girişte "kullanıcı yok" ile "şifre yanlış"ı **aynı** mesajla cevapla
  (`"Wrong username or password"`): ayrı mesaj, hangi kullanıcı adlarının
  var olduğunu ele verir.
- Gerçek sunucuda HTTPS.

## Yapma

| Yapma | Neden? |
|---|---|
| Şifreyi düz metin saklamak | Veritabanı sızarsa hepsi gider |
| `hashlib.sha256(password)` tek tur, tuzsuz | Hızlı: milyonlarca deneme saniyeler sürer |
| `random.randint` ile jeton | `random` tahmin edilebilir |
| Anahtarı sorguda göndermek | Günlüklere ve geçmişe yazılır |
| Şifreyi ya da jetonu cevaba/günlüğe yazmak | Sızar |
| `==` ile özet karşılaştırmak | Süre farkı ipucu verir |

## 401 mi 403 mü?

| Durum | Kod |
|---|---|
| Başlık yok | `401` |
| Anahtar/jeton tanınmıyor | `401` |
| Şifre yanlış | `401` |
| Kullanıcı tanındı, bu işe izni yok | `403` |

`401` cevabına `WWW-Authenticate` başlığı eklemek HTTP'nin kuralı;
`HTTPBearer` bunu kendisi yapıyor.
