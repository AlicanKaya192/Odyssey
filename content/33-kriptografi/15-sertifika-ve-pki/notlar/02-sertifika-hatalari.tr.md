Sertifika hataları çoğu zaman "can sıkıcı bir uyarı" gibi görülür ve
kapatılır. Oysa her biri doğrulamanın bir adımının düştüğünü söyler.

| Hata | Hangi adım düştü | Ne yapılır |
|---|---|---|
| Süresi dolmuş | Tarih | Sertifika yenilenir (otomatik yenileme kurulur) |
| Ad eşleşmiyor | Ad | Doğru ad için sertifika alınır; bağlanılan adres denetlenir |
| Güvenilmeyen kök | Güven deposu | Kök gerçekten güvenilir mi diye bakılır; rastgele kök eklenmez |
| Zincir eksik | Zincir | Sunucu ara sertifikayı da göndermelidir |
| İptal edilmiş | İptal | Yeni anahtar, yeni sertifika |

## Yapılmayacaklar

- **Doğrulamayı kapatmak.** Koddaki `verify=False` gibi bir ayar, TLS'i
  şifreleyen ama kiminle konuştuğunu bilmeyen bir bağlantıya çevirir;
  arada biri kendi sertifikasını sunabilir. Test ortamı için bile kendi
  kökünü güven deposuna eklemek doğru yoldur, doğrulamayı kapatmak değil.
- **Hata mesajını kullanıcıya "geç" düğmesiyle bırakmak.** Kullanıcılar
  uyarıyı okumadan geçer (Sosyal Mühendislik bölümü).
- **Özel anahtarı sertifikayla aynı yere, herkesin okuyabileceği biçimde
  koymak.** Sertifika açıktır, özel anahtar değildir.

## Kendi imzalı sertifika

Geliştirme ortamında kendini imzalamış (self-signed) bir sertifika
kullanılabilir. Doğru kullanımı: o sertifikanın kökünü yalnızca
geliştirme makinesinin güven deposuna eklemek. Yanlış kullanımı: üretimde
kendi imzalı sertifika ile doğrulamayı kapatmak.
