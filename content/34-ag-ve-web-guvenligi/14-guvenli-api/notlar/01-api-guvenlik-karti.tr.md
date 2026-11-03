## Her uç nokta için sorular

1. **Kim?** İstek kimlik doğrulamadan geçti mi (oturum, jeton, API
   anahtarı)? Kimliksiz açık kalması gereken uç noktalar bilerek mi açık?
2. **Bu nesne onun mu?** Adresteki ya da gövdedeki her kimlik için sahiplik
   denetimi. Yoksa `404`.
3. **Bu işi yapabilir mi?** Yönetici uç noktaları (`DELETE /users/7`)
   rolü denetliyor mu? Bir uç noktayı arayüzden gizlemek onu korumaz.
4. **Hangi alanlar girer?** Değiştirilebilir alanların izin listesi.
5. **Hangi alanlar çıkar?** Gösterilebilir alanların izin listesi.
6. **Ne kadar?** İstek sayısı, gövde boyutu, sayfa büyüklüğü sınırı.
7. **Hata ne söylüyor?** Kısa kod ve mesaj; ayrıntı günlükte.

## API Security Top 10 (2023) başlıkları

| Başlık | Bu bölümde |
|---|---|
| Nesne düzeyinde bozuk yetkilendirme | Sahiplik denetimi, `404` |
| Bozuk kimlik doğrulama | Kimlik Doğrulama Hataları bölümü |
| Nesne özelliği düzeyinde bozuk yetkilendirme | Girişte ve çıkışta izin listesi |
| Sınırsız kaynak tüketimi | Kova, boyut ve sayfa sınırı |
| İşlev düzeyinde bozuk yetkilendirme | Rol denetimi (soru 3) |
| Hassas iş akışlarına sınırsız erişim | Satın alma, kayıt gibi akışlara ek sınır |
| Sunucu tarafı istek sahteciliği | SSRF bölümü |
| Güvenlik yapılandırma hataları | Varsayılanlar, başlıklar, hata metinleri |
| Yanlış envanter yönetimi | Eski sürüm (`/v1`) ve test uç noktaları açık kalmasın |
| API'lerin güvensiz kullanımı | Başka bir API'den gelen veri de girdidir |

## Kısa kurallar

- Kimlik tahmin edilemese bile sahiplik denetlenir.
- Kayıt nesnesi olduğu gibi JSON'a çevrilmez.
- Sınırı aşan isteğe `429`, istersen `Retry-After`.
- Eski sürümler kapatılır ya da yenisiyle aynı denetimlerden geçer.
