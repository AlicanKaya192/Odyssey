Bir uç nokta yazarken "hangi kodu döndürmeliyim?" sorusunun kısa yolu.

## Başarılı

| Durum | Kod | Gövde |
|---|---|---|
| Okudum, işte sonuç | `200` | Var |
| Yeni kayıt oluşturdum | `201` | Yeni kayıt (+ `Location` başlığı) |
| İsteği aldım, sonra işleyeceğim | `202` | Kısa bilgi (`{"queued": true}`) |
| Yaptım, söyleyecek bir şey yok | `204` | **Yok** |

## İstemcinin hatası (4xx)

| Durum | Kod |
|---|---|
| Gövde/parametre kalıba uymuyor | `422` (FastAPI kendisi verir) |
| Kalıba uyuyor ama mantıksız (stokta olmayanı satmak) | `400` |
| Kim olduğunu söylemedin (anahtar yok) | `401` |
| Kim olduğunu biliyorum ama iznin yok | `403` |
| Böyle bir kayıt yok | `404` |
| Bu yöntem bu adreste yok | `405` (FastAPI kendisi verir) |
| Çakışma: bu ad zaten alınmış | `409` |
| Çok sık istek | `429` |

## Sunucunun hatası (5xx)

`500`'ü sen seçmezsin; kodundaki yakalanmamış bir hatadan ya da yanıt
modeline uymayan bir dönüşten çıkar. İstemciye "sende değil bende sorun
var" der.

## Karar sırası

1. Kalıp tutmadı mı? → FastAPI `422`.
2. Kimlik/izin sorunu mu? → `401` / `403`.
3. Kayıt yok mu? → `404`.
4. Var olanla çakışıyor mu? → `409`.
5. Başka bir iş kuralı mı bozuldu? → `400`.
6. Yeni bir şey mi oluştu? → `201`; silindi mi? → `204`; yoksa `200`.

## Adlarıyla

`from fastapi import status` sonrası: `status.HTTP_200_OK`,
`status.HTTP_201_CREATED`, `status.HTTP_204_NO_CONTENT`,
`status.HTTP_404_NOT_FOUND`, `status.HTTP_409_CONFLICT`. Sayı yazmakla aynı
sonuç; okuyan için daha açık.
