Kimlik doğrulama tek bir sayfa değil, birkaç akıştır. Her biri ayrı
denetlenir; saldırgan en zayıf olanı seçer.

## Giriş

- [ ] Başarısız girişte tek mesaj; bilinmeyen kullanıcıda da aynı süre.
- [ ] Hesap ve kaynak başına deneme sınırı, artan bekleme.
- [ ] Başarılı girişte oturum kimliği yenileniyor (Oturum ve Çerez).
- [ ] Başarılı ve başarısız girişler kaydediliyor (parola değil).

## Kayıt

- [ ] "Bu kullanıcı adı alınmış" mesajı numaralandırmaya yol açar; kayıt
  e-postayla doğrulanıyorsa mesaj "doğrulama bağlantısı gönderdik" olur.
- [ ] Parola kuralı: uzunluk ve bilinen kötü parolalar.
- [ ] Otomatik toplu kayda karşı hız sınırı.

## Parola sıfırlama

- [ ] Adres kayıtlı olsun olmasın aynı mesaj.
- [ ] Jeton rastgele, kısa ömürlü, tek kullanımlık, sunucuda özetli.
- [ ] Jeton adreste taşınıyorsa sayfa açılınca hemen kullanılır ve
  `Referer` ile başka siteye gitmez.
- [ ] Sıfırlamadan sonra öteki oturumlar kapanıyor, kullanıcıya bildirim
  gidiyor.

## MFA

- [ ] İkinci adım tamamlanmadan oturum tam yetkili sayılmıyor.
- [ ] Kod denemelerinde de hız sınırı var (6 haneli kodda 1000000
  olasılık var; sınırsız denemede bu az).
- [ ] Yedek kodlar tek kullanımlık ve özetli saklanıyor.

## Parola değişimi

- [ ] Eski parola ya da MFA isteniyor (oturumu ele geçiren biri tek başına
  değiştiremesin).
- [ ] Değişimden sonra öteki oturumlar kapanıyor.
