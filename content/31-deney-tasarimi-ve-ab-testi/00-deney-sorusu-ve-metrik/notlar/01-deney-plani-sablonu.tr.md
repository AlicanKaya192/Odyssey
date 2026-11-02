Test başlamadan doldurulur, sonra değiştirilmez. Değişmesi gerekirse
nedeniyle birlikte tarihli bir not düşülür.

| Başlık | Örnek |
|---|---|
| Değişiklik | Ödeme düğmesi sayfanın üstüne taşınıyor |
| Gerekçe | Mobilde düğme ilk ekranda görünmüyor |
| Birincil metrik | Kullanıcı başına satın alma oranı (`bought`) |
| Beklenen yön | Artış |
| En küçük anlamlı etki | +0,5 puan |
| Koruma metrikleri | İade oranı (alıcılar içinde), sayfa açılış süresi |
| Atama birimi | Kullanıcı |
| Atama oranı | %50 / %50 |
| Örneklem ve süre | Güç analizinden; en az bir tam hafta |
| Test ve α | İki oran z-testi, α = 0,05, iki yönlü |

## Metriğin yazılışı

Bir metrik dört şeyle tanımlanır:

1. **Pay:** ne sayılıyor? (satın alan kullanıcı)
2. **Payda:** neye bölünüyor? (deneye giren kullanıcı)
3. **Pencere:** hangi süre içinde? (atamadan sonraki 14 gün)
4. **Süzgeç:** kim dahil? (yalnızca ödeme sayfasına gelenler)

"Dönüşüm oranı" demek yetmez; bu dördü yazılmazsa iki kişi aynı adla iki
farklı sayı hesaplar.

## Sık hatalar

- Testten sonra "en iyi görünen" metriği birincil yapmak.
- Koruma metriği seçmemek: satın alma artarken iadeler patlayabilir.
- Süre gibi yönü belirsiz bir metriği hedef yapmak.
- Paydayı karıştırmak: "alıcı başına iade" ile "kullanıcı başına iade"
  farklı sayılardır.
