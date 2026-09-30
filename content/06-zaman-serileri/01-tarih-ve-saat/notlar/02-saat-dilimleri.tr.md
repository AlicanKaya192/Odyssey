## İki tür zaman

| | Saat dilimsiz (naive) | Dilimli (aware) |
|---|---|---|
| Örnek | `datetime(2024, 3, 9, 14, 30)` | `datetime(2024, 3, 9, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))` |
| Bildiği | Duvar saati | Duvar saati + hangi dilim |
| `tzinfo` | `None` | Bir dilim |
| Ne zaman | Tek şehir, yaz saati yok | Farklı yerler, yaz saati, API'ler |

**İkisi birbiriyle karşılaştırılamıyor ve çıkarılamıyor:**
`TypeError: can't compare offset-naive and offset-aware datetimes`. Önce
ikisini aynı türe getir.

## `replace` ile `astimezone` farkı

En sık karıştırılan iki işlem:

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

t = datetime(2024, 3, 9, 14, 30)                 # naive

t.replace(tzinfo=timezone.utc)
# 2024-03-09 14:30+00:00   saat AYNI kaldi, yalnizca etiket eklendi

t.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("Europe/Istanbul"))
# 2024-03-09 17:30+03:00   AYNI AN, baska dilimin saatiyle
```

- **`replace(tzinfo=...)`**: "bu saat zaten bu dilimde" diyorsun. Saat
  değişmiyor. Naive bir zamana dilimini **tanıtmak** için.
- **`astimezone(...)`**: "bu anı başka bir dilimin saatiyle göster". Saat
  değişiyor, an aynı kalıyor. **Dönüştürmek** için.

Dilimli bir zamana `replace` ile başka dilim vermek anı değiştirir; neredeyse
her zaman hatadır.

## Sık kullanılan bölge adları

| Ad | Fark | Yaz saati |
|---|---|---|
| `UTC` | +00:00 | Yok |
| `Europe/Istanbul` | +03:00 | 2016'dan beri yok |
| `Europe/London` | +00:00 / +01:00 | Var |
| `Europe/Berlin` | +01:00 / +02:00 | Var |
| `America/New_York` | -05:00 / -04:00 | Var |
| `Asia/Tokyo` | +09:00 | Yok |

Fark yazmak (`+03:00`) yerine **bölge adı** kullan: fark yaz saatinde
değişiyor, bölge adı kuralları biliyor. Sabit fark gerekiyorsa
`timezone(timedelta(hours=3))`.

## Yaz saati geçişleri (Europe/Berlin, 2024)

| Tarih | Ne oldu | Sonuç |
|---|---|---|
| 31 Mart 02:00 | Saat 03:00'e atladı | 02:00–03:00 arası **hiç yaşanmadı**; o gün 23 saat |
| 27 Ekim 03:00 | Saat 02:00'ye döndü | 02:00–03:00 arası **iki kez** yaşandı; o gün 25 saat |

```python
berlin = ZoneInfo("Europe/Berlin")
datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=0).utcoffset()   # 2:00:00  ilki
datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=1).utcoffset()   # 1:00:00  ikincisi
```

Saatlik veride bunun görünen sonucu: bahar gününde **23 satır**, sonbahar
gününde **25 satır**. Günlük toplam alırken bir saat eksik ya da fazla
sayılıyor.

## Altın kural

1. Zamanı **UTC** olarak sakla.
2. Hesabı (fark, toplama, sıralama) **UTC'de** yap.
3. Yerel saate **yalnızca insana gösterirken** çevir.
4. Dışarıdan gelen naive zamanın hangi dilimde olduğunu **öğren**, tahmin
   etme; sonra `replace` ile tanıt.

## Unix zamanı

```python
datetime.fromtimestamp(1710000000, tz=timezone.utc)        # saniye
datetime.fromtimestamp(1710000000123 / 1000, tz=timezone.utc)   # milisaniye
```

| Hane sayısı | Birim |
|---|---|
| 10 | Saniye |
| 13 | Milisaniye |
| 16 | Mikrosaniye |
| 19 | Nanosaniye (pandas'ın iç birimi) |
