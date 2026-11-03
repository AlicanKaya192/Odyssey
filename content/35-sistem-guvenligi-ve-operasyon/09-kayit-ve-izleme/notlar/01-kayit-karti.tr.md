## Neyi kaydet, neyi kaydetme

| Kaydet | Kaydetme |
|---|---|
| Giriş denemeleri (başarılı ve başarısız) | Parola, oturum jetonu |
| Yetki değişiklikleri, yeni hesaplar | Kart numarası, kimlik numarası |
| Reddedilen istekler, yetki hataları | Gereğinden fazla kişisel veri |
| Yönetici işlemleri, yapılandırma değişiklikleri | İsteğin bütün gövdesi |
| Uygulama hataları | Sır içeren yapılandırma |

## Kayıt düzeyleri

| Düzey | Ne zaman? |
|---|---|
| `DEBUG` | Geliştirme ayrıntısı; yayında genellikle kapalı |
| `INFO` | Olağan olay: giriş, işlem tamam |
| `WARNING` | Dikkat: başarısız giriş, beklenmeyen ama zararsız durum |
| `ERROR` | Bir işlem başarısız oldu |
| `CRITICAL` | Sistem ya da güvenlik için ciddi durum |

## Python kalıpları

- JSON satırını okumak: `json.loads(line)`; bozuk satırda `json.JSONDecodeError`.
- Sayım: `Counter(r["level"] for r in records)`.
- UTC'ye çevirmek: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- Kayan pencere: `deque`; eskiyi at: `while window[0] <= t - WINDOW: window.popleft()`.
- Özet zinciri: `prev = sha256((prev + entry).encode()).hexdigest()`.

## Akılda tutulacak

- Kayıt yoksa olay ne fark edilir ne de anlaşılır.
- Saat dilimi yazılmayan zaman damgası olay sırasını yanıltır.
- Kayıtlar saldırganın ulaştığı makinede kalmaz; ayrı bir sisteme gider.
- Özet zinciri değişikliği engellemez, fark ettirir.
- Saklama süresi yazılı bir karardır.
