## Adımlar ve sorular

| Adım | Sorulacak soru |
|---|---|
| Hazırlık | Plan, roller ve iletişim listesi hazır mı? Kayıt ve yedek var mı? |
| Tespit ve analiz | Uyarı gerçek mi? Ne zaman başladı, neyi etkiliyor? |
| Sınırlama | Yayılmayı nasıl durdururuz, iz kaybetmeden? |
| Temizleme | Kök neden ne, nasıl giderilir? |
| Kurtarma | Sistem temiz mi, geri açınca nasıl izleriz? |
| Olay sonrası | Ne öğrendik, hangi eylem kimde, ne zamana kadar? |

## Öncelik

| Puan (etki × aciliyet) | Öncelik |
|---|---|
| 6–9 | P1: hemen, herkes |
| 4–5 | P2: bugün |
| 1–3 | P3: sıraya girer |

## Sık yapılan hatalar

| Hata | Neden kötü? |
|---|---|
| Makineyi hemen kapatmak ya da silmek | Bellekteki ve diskteki iz kaybolur |
| Saldırganın gördüğü kanaldan (aynı e-posta) konuşmak | Plan saldırgana gider |
| Yalnızca belirtiyi gidermek | Kök neden kalır, olay tekrarlar |
| Zaman çizelgesini yerel saatlerle kurmak | Olay sırası yanlış okunur |
| Olay sonrası değerlendirmeyi atlamak | Ders alınmaz |

## Python kalıpları

- Öncelik: `"P1" if s >= 6 else "P2" if s >= 4 else "P3"`.
- UTC'ye çevirmek: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- Gösterge teması: `INDICATORS & set(gorulenler)` boş değilse temas var.
- Saat farkı: `(b - a).total_seconds() / 3600`.

## Akılda tutulacak

- Müdahale olay anında değil, önceden planlanır.
- Sınırlamada makine ağdan ayrılır ama kapatılmaz.
- Örnek alan adları için `.example`, `example.org`, `example.net`
  ayrılmıştır; örnek veride gerçek bir alan adı kullanılmaz.
- Olay sonrası değerlendirme suçlu değil eylem maddesi üretir.
