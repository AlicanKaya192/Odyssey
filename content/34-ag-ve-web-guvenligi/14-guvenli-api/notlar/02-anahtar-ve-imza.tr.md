API anahtarı ve istek imzası iki ayrı soruyu cevaplar: anahtar "kim",
imza "değişmedi ve yeni mi".

## API anahtarı

- **Üretme:** `secrets.token_urlsafe(32)`; tahmin edilebilir değer
  (kullanıcı adı, tarih, sıra numarası) kullanılmaz.
- **Önek:** `shop_live_...` gibi bir önek anahtarın neye ait olduğunu
  gösterir ve sızan anahtarı aramayı (kod deposunda, günlükte) kolaylaştırır.
- **Saklama:** sunucuda yalnızca özeti (`sha256`); anahtar kullanıcıya bir
  kez gösterilir.
- **Gönderme:** başlıkta (`Authorization`), adreste değil.
- **Karşılaştırma:** `hmac.compare_digest`.
- **Kapsam:** her anahtar yalnızca gereken işlere izin verir (yalnızca okuma
  gibi); en az yetki ilkesi.
- **Yenileme:** anahtarın süresi vardır; yenisi verilip eskisi bir süre
  sonra kapatılır. Sızan anahtar hemen iptal edilir.

## İstek imzası

İmzalanan metin isteğin bütün önemli parçalarını içerir:

| Parça | Neden |
|---|---|
| Zaman (`ts`) | Eski isteği reddetmek için |
| Yöntem (`POST`) | `GET` imzası `DELETE` için kullanılmasın |
| Yol (`/transfer`) | Başka uç noktaya taşınmasın |
| Gövde | Tutar, alıcı değişmesin |
| Nonce | Pencere içinde ikinci kez kullanılmasın |

- Sunucu imzayı **kendisi yeniden hesaplar** ve `hmac.compare_digest` ile
  karşılaştırır.
- Önce zaman, sonra imza denetlenir; ikisi birlikte gerekir.
- Saat farkı için küçük bir pencere (birkaç dakika) bırakılır; nonce'lar
  o pencere kadar hatırlanır.
- Sır iki tarafta da kod deposuna değil, sır yönetimine konur.
