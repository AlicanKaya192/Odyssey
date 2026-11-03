Yeni bir site için başlangıç noktası olarak kullanılabilecek değerler.
Her site kendi ihtiyacına göre daraltır ya da genişletir; CSP özellikle
sitenin gerçekten yüklediği kaynaklara göre yazılır.

## Önerilen değerler

| Başlık | Değer |
|---|---|
| `Content-Security-Policy` | `default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `X-Frame-Options` | `DENY` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |

## Değerlerin anlamı

- **`max-age=31536000`:** bir yıl (saniye). `includeSubDomains` bütün alt
  alan adlarını da kapsar; önce her alt alan adının HTTPS'e hazır olduğu
  denetlenir.
- **`strict-origin-when-cross-origin`:** aynı sitede tam adres, başka
  siteye yalnızca köken (`https://shop.example`), HTTPS'ten HTTP'ye hiçbir
  şey gönderilir.
- **`frame-ancestors 'none'` ve `DENY`:** sayfa hiçbir çerçevede
  gösterilmez. Kendi sitenin çerçevesine izin vermek için `'self'` ve
  `SAMEORIGIN`.
- **`Permissions-Policy`:** sayfanın kullanmadığı tarayıcı özelliklerini
  kapatır; sayfaya bir betik sızsa bile kameraya erişemez.

## Denetim

- Başlık adları büyük/küçük harfe duyarsız karşılaştırılır.
- Başlıklar **her** cevapta gönderilir, hata sayfaları dahil.
- CSP önce `Content-Security-Policy-Report-Only` ile denenir: tarayıcı
  engellemez, yalnızca ihlali bildirir.
- Başlıklar ikinci katmandır: kaçışlama, parametreli sorgu ve CSRF jetonu
  yerinde kalır.
