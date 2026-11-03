Bir web uygulamasına CSRF savunması eklerken izlenecek adımlar ve sık
yapılan hatalar.

## Adımlar

1. **Durum değiştiren uç noktaları listele.** Para, ayar, parola, e-posta,
   silme, ekleme: hepsi. `GET` ile durum değiştiren varsa önce onu
   `POST`'a çevir.
2. **Jeton üret ve oturuma bağla.** Oturum açılınca ya da form üretilirken
   `secrets.token_urlsafe(32)`.
3. **Her formda gizli alan olarak gönder.** Betikle yapılan isteklerde
   jeton özel bir başlıkta gönderilir.
4. **Sunucuda her durum değiştiren istekte denetle.** Jeton yoksa ya da
   tutmazsa istek reddedilir; ayrıntılı hata mesajı verilmez.
5. **Oturum çerezine `SameSite=Lax` (ya da `Strict`) yaz.**
6. **`Origin` başlığını izin listesiyle denetle.**
7. **Önemli işlemlerde yeniden doğrula** (parola ya da MFA).

## Sık hatalar

- **Jetonu yalnızca bazı formlara koymak:** saldırgan korumasız olanı
  bulur. Denetim tek bir yerde, bütün durum değiştiren isteklere uygulanır.
- **Jetonun yokluğunu kabul etmek:** "jeton varsa denetle" yazılırsa,
  jetonsuz istek denetimsiz geçer.
- **Jetonu `==` ile karşılaştırmak:** zamanlama yan kanalı;
  `compare_digest`.
- **Herkes için aynı jeton:** jeton oturuma bağlı olmalı; sabit bir jeton
  bir kez görülünce her yerde çalışır.
- **Jetonu adreste taşımak:** kayıtlara ve `Referer` başlığına yazılır.
- **"Biz JSON API'yiz, CSRF bizi ilgilendirmez":** API çerezle kimlik
  doğruluyorsa ilgilendirir. Kimlik doğrulama çerezle değil, başlıkta
  açıkça gönderilen bir jetonla yapılıyorsa tarayıcı onu kendiliğinden
  eklemez ve CSRF riski düşer (Güvenli API bölümü).

## Test

- Jetonsuz istek reddediliyor mu?
- Başka bir oturumun jetonuyla gelen istek reddediliyor mu?
- `GET` ile durum değiştirilebiliyor mu? (Değiştirilememeli.)
- Oturum çerezinde `SameSite` var mı?
