**Beş alan**

```text
┌ dakika (0-59)
│ ┌ saat (0-23, UTC)
│ │ ┌ ayın günü (1-31)
│ │ │ ┌ ay (1-12)
│ │ │ │ ┌ haftanın günü (0-6, 0 = Pazar)
│ │ │ │ │
30 2 * * 1
```

**İşaretler**

| İşaret | Anlamı | Örnek |
|---|---|---|
| `*` | Her değer | `* * * * *` her dakika (GitHub'da en sık 5 dakikada bir) |
| `,` | Liste | `0 9 * * 1,3,5` Pzt, Çar, Cum 09:00 |
| `-` | Aralık | `0 9 * * 1-5` hafta içi 09:00 |
| `/` | Adım | `*/15 * * * *` 15 dakikada bir |

**Örnekler** (Türkiye = UTC + 3)

| cron | UTC | Türkiye |
|---|---|---|
| `0 3 * * *` | Her gün 03:00 | 06:00 |
| `17 3 * * *` | Her gün 03:17 | 06:17 |
| `30 2 * * 1` | Pazartesi 02:30 | Pazartesi 05:30 |
| `0 21 * * 0` | Pazar 21:00 | Pazar 24:00 = Pazartesi 00:00 |
| `0 6 1 * *` | Her ayın 1'i 06:00 | 09:00 |

**Türkiye saatinden cron'a**

1. İstenen Türkiye saatinden 3 çıkar.
2. Sonuç 0'dan küçükse 24 ekle ve **günü bir geri al** (Pazartesi 01:00
   Türkiye = Pazar 22:00 UTC → `0 22 * * 0`).

**Dikkat**

- Haftanın günü 0 = Pazar. Python'un `weekday()`'inde 0 = Pazartesi.
- Saat başları en yoğun an; `0` yerine `17` gibi bir dakika seç.
- cron'u tırnakla yaz: `- cron: "17 3 * * *"`. `*` ile başlayan değer
  tırnaksız YAML'da başka anlama gelir.
