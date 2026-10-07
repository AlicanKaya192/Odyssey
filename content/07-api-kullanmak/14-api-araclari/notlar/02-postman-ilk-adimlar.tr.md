Postman'e (ya da Bruno'ya) ilk kez başlarken izleyebileceğin sıra.

## İlk istek

1. Uygulamayı aç; yeni bir istek (**New → HTTP Request**) oluştur.
2. Yöntemi seç (`GET`), adresi yaz: açık bir API'nin örnek adresi.
3. **Send**'e bas. Alttaki panelde durum kodu, süre, boyut ve gövde görünür.
4. **Headers** sekmesinde yanıt başlıklarına bak: `Content-Type`, hız sınırı
   başlıkları...

## Parametre, başlık, gövde

- **Params** sekmesi: sorgu parametrelerini tablo olarak yazarsın; adres
  kendiliğinden güncellenir.
- **Headers** sekmesi: `Accept`, `X-API-Key` gibi başlıklar.
- **Authorization** sekmesi: türü seç (Bearer Token, Basic Auth, API Key);
  Postman doğru başlığı kendisi kurar.
- **Body → raw → JSON**: `POST` / `PATCH` gövdesi.

## Ortam değişkenleri

1. **Environments** altında yeni bir ortam aç: `base_url`, `token`.
2. İsteklerde `{{base_url}}/books` ve `Bearer {{token}}` yaz.
3. Test ve canlı sunucu için iki ortam tut; sağ üstten seçerek geç.

Böylece anahtar isteklerin içinde değil, ortamda durur; koleksiyonu
paylaşırken anahtarı paylaşmazsın.

## Koleksiyon

- İlgili istekleri bir koleksiyonda topla ("Kütüphane API'si").
- Klasörlerle düzenle: Kitaplar, Yazarlar.
- **Export** ile JSON olarak dışa aktar; ekiple paylaş ya da sürüm kontrolüne
  koy (anahtarlar ortamda kalsın).

## İstekten koda

Çalışan bir isteğin sağ tarafındaki **Code** (`</>`) düğmesi, onu curl ya da
Python requests koduna çevirir. Önce araçta dene, çalışınca kodu oradan al:
API ile çalışmanın en verimli düzeni.
