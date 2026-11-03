## CSRF bir bakışta

| Soru | Cevap |
|---|---|
| Neden olur? | Tarayıcı çerezi isteğin nereden başladığına bakmadan ekler |
| Saldırgan ne yapar? | Kullanıcı adına bir **işlem** yaptırır |
| Cevabı okuyabilir mi? | Hayır (aynı köken politikası) |
| Çerezi çalar mı? | Hayır; tarayıcı kendisi ekler |
| Hangi istekler? | Durum değiştirenler: `POST`, `PUT`, `PATCH`, `DELETE` |

## Savunmalar

| Savunma | Nasıl? | Not |
|---|---|---|
| CSRF jetonu | `secrets` ile üret, oturuma bağla, formda gönder, `compare_digest` | Asıl savunma |
| Çift gönderimli çerez | Jeton hem çerezde hem formda; ikisi karşılaştırılır | Sunucuda saklamadan |
| `SameSite=Lax` / `Strict` | Başka siteden gelen `POST`'a çerez gitmez | Açıkça yaz; ikinci katman |
| `GET` durum değiştirmez | Durum değiştiren iş `POST` ile | `Lax` üst düzey `GET`'e çerez ekler |
| Köken denetimi | `Origin` izin listesinde mi? | Başlık yoksa kural önceden belli |
| Yeniden doğrulama | Önemli işlemde parola ya da MFA | Başka site parolayı bilmez |

## SameSite kararı (başka siteden gelen istek)

| Öznitelik | Üst düzey `GET` | Gizli form `POST` |
|---|---|---|
| `Strict` | Çerez yok | Çerez yok |
| `Lax` | Çerez var | Çerez yok |
| `None` (+ `Secure`) | Çerez var | Çerez var |

## Kurallar

- Jeton yalnızca sayfanın içinde durur; adreste (`?csrf=...`) taşınmaz.
- Jeton her oturumda farklıdır; oturum yenilenince jeton da yenilenir.
- XSS açığı bütün CSRF savunmalarını boşa çıkarır.
- CORS bir CSRF savunması değildir (CORS ve Güvenlik Başlıkları bölümü).
