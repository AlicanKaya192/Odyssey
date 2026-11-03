## İsteğin parçaları

| Parça | Örnek |
|---|---|
| İstek satırı | `POST /login HTTP/1.1` |
| Başlıklar | `Host: shop.example.com`, `Cookie: session=...` |
| Boş satır | `\r\n` |
| Gövde | `user=ada&password=...` |

## Yöntemler

| Yöntem | İşi | Durum değiştirir mi? |
|---|---|---|
| `GET` | Okumak | Hayır (değiştirmemeli) |
| `POST` | Göndermek, oluşturmak | Evet |
| `PUT` / `PATCH` | Değiştirmek | Evet |
| `DELETE` | Silmek | Evet |

## Durum kodları

| Kod | Anlamı |
|---|---|
| 1xx | Bilgi |
| 2xx | Başarılı (200 OK, 201 Created) |
| 3xx | Yönlendirme (301 kalıcı, 302 geçici) |
| 4xx | İstemci hatası (400, 401, 403, 404, 429 çok istek) |
| 5xx | Sunucu hatası (500, 503) |

401 kimlik yok, 403 yetki yok, 404 yok. Varlığı gizlemek için 404.

## Güvenlikle ilgili başlıklar

| Başlık | İşi |
|---|---|
| `Strict-Transport-Security` | HSTS: düz HTTP'yi hiç deneme |
| `Set-Cookie` | Çerez koy (Oturum ve Çerez bölümü) |
| `Content-Security-Policy` | Hangi betiklerin çalışacağı (CORS ve Güvenlik Başlıkları) |
| `Location` | Yönlendirmenin hedefi |
| `Server` | Sunucu yazılımı; sürüm yazılmaz |

## HTTPS

- HTTPS = HTTP + TLS: **gizlilik, bütünlük, sunucu kimliği**.
- Sitenin güvenilir olduğunu **söylemez**; alan adı yine görünür.
- HSTS: `max-age=31536000; includeSubDomains` (bir yıl = 31536000 saniye).
- Sayfadaki her kaynak `https://` (karışık içerik yok).
