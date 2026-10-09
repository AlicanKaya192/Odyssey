## Kurmak

| Yazım | Sonuç |
|---|---|
| `date(2026, 3, 15)` | 15 Mart 2026 |
| `datetime(2026, 3, 15, 14, 30)` | 15 Mart 2026 14:30 |
| `date.today()`, `datetime.now()` | şimdi (her çalıştırmada farklı) |
| `date.fromisoformat("2026-03-15")` | ISO metinden |
| `datetime.strptime(metin, biçim)` | herhangi bir biçimden |
| `datetime.combine(gün, saat)` | gün + saat |

## Okumak ve değiştirmek

| Yazım | Ne verir |
|---|---|
| `d.year`, `d.month`, `d.day` | parçalar |
| `d.weekday()` / `d.isoweekday()` | Pazartesi 0 / Pazartesi 1 |
| `d.replace(day=1)` | yalnızca bir parçası değişmiş **yeni** tarih |
| `dt.date()`, `dt.time()` | gün ya da saat kısmı |
| `d.isoformat()` | `"2026-03-15"` |
| `d.strftime("%d.%m.%Y")` | `"15.03.2026"` |

Tarih nesneleri değişmez (immutable): `replace` yeni nesne döndürür, eskisi
aynı kalır.

## Süre

| Yazım | Sonuç |
|---|---|
| `b - a` | `timedelta` |
| `a + timedelta(days=7)` | bir hafta sonrası |
| `delta.days` | tam gün sayısı |
| `delta.total_seconds()` | bütün süre saniye olarak |
| `delta / timedelta(hours=1)` | süre kaç saat (ondalık) |

## Saat dilimi

| Yazım | Ne yapar |
|---|---|
| `ZoneInfo("Europe/Istanbul")` | saat dilimi |
| `datetime(..., tzinfo=ZoneInfo(...))` | farkında nesne |
| `dt.astimezone(ZoneInfo(...))` | aynı anı başka saatte göster |
| `timezone.utc` | UTC |
| `dt.utcoffset()` | o tarihteki UTC farkı |

## Kontrol listesi

- Metinden okurken biçimi kontrol et: `%m` ay, `%M` dakika.
- Saklarken ISO biçimi ve mümkünse UTC.
- Saf ve farkında nesneleri karıştırma.
- "Bir ay sonra" için `timedelta(days=30)` yazma; ikinci nota bak.
