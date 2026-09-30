## Periyot

```python
p = pd.Period("2024-03", freq="M")
```

| İşlem | Sonuç |
|---|---|
| `p.start_time`, `p.end_time` | Aralığın ilk ve son anı |
| `p + 1`, `p - 1` | Sonraki / önceki periyot |
| `p.days_in_month` | 31 |
| `p.year`, `p.month`, `p.quarter` | 2024, 3, 1 |
| `str(p)`, `p.strftime("%b %Y")` | `2024-03`, `Mar 2024` |
| `(p - pd.Period("2023-12", "M")).n` | 3 (kaç ay fark) |
| `p.asfreq("Q")` | `2024Q1` (ait olduğu çeyrek) |
| `pd.Period("2024Q1").asfreq("M", how="end")` | `2024-03` |

## Tarihten periyoda, periyottan tarihe

```python
s.index.to_period("M")             # DatetimeIndex -> PeriodIndex
df["date"].dt.to_period("M")       # sutunda
ps.to_timestamp()                  # periyot -> ay basi
ps.to_timestamp(how="end")         # periyot -> ay sonu (son an)
ps.index.start_time                # yalnizca baslangiclar
pd.period_range("2024-01", periods=12, freq="M")
```

## Periyot kısaltmaları

| Kısaltma | Aralık | Etiket örneği |
|---|---|---|
| `D` | Gün | `2024-03-09` |
| `W` | Hafta, pazartesi–pazar | `2024-03-04/2024-03-10` |
| `M` | Ay | `2024-03` |
| `Q` | Çeyrek | `2024Q1` |
| `Q-MAR` | Mart'ta biten mali yılın çeyreği | `2024Q4` |
| `Y` | Yıl | `2024` |
| `h` | Saat | `2024-03-09 14:00` |

**Nokta ve aralık kısaltmaları farklı:**

| İstenen | `date_range` / `resample` | `Period` / `to_period` |
|---|---|---|
| Ay | `ME` (son), `MS` (baş) | `M` |
| Çeyrek | `QE`, `QS` | `Q` |
| Yıl | `YE`, `YS` | `Y` |

## Dönemlere toplamak

```python
s.groupby(s.index.to_period("M")).sum()       # aylik toplam
s.groupby(s.index.to_period("M")).mean()      # aylik gunluk ortalama
s.groupby(s.index.to_period("Q")).sum()       # ceyreklik
s.groupby(s.index.to_period("W")).sum()       # haftalik
s.groupby([s.index.year, s.index.month]).sum()    # yil ve ay ayri seviyede
```

## `Timedelta` ile `DateOffset`

| | `Timedelta` | `DateOffset` |
|---|---|---|
| Bildiği | Sabit süre: gün, saat, dakika | Takvim: ay, yıl, hafta, gün |
| `2024-01-31` + "bir ay" | `days=30` → `2024-03-01` | `months=1` → `2024-02-29` |
| `2024-02-29` + "bir yıl" | `days=365` → `2025-02-28` | `years=1` → `2025-02-28` |
| Ne zaman | Süre ölçerken | Takvimde ilerlerken |

```python
t + pd.DateOffset(months=1)
t + pd.DateOffset(years=1)
t + pd.DateOffset(months=3, days=5)
t - pd.DateOffset(years=1)          # gecen yil ayni gun
t + pd.DateOffset(day=1)            # ayin 1'i (tekil "day": o gune AYARLA)
```

Çoğul (`days=1`) **ekliyor**, tekil (`day=1`) o değere **ayarlıyor.** İkisi
karıştırılırsa hata çıkmıyor, sonuç yanlış oluyor.

## Hazır ofsetler

```python
from pandas.tseries.offsets import (BDay, CustomBusinessDay, MonthBegin,
                                    MonthEnd, QuarterEnd, Week, YearEnd)
```

| Ofset | `2024-03-09` (cumartesi) için |
|---|---|
| `+ MonthEnd(0)` | `2024-03-31` |
| `+ MonthEnd(1)` | `2024-03-31` (ay sonundaysan bir sonraki) |
| `- MonthBegin(1)` | `2024-03-01` |
| `+ MonthBegin(1)` | `2024-04-01` |
| `+ QuarterEnd(0)` | `2024-03-31` |
| `+ YearEnd(0)` | `2024-12-31` |
| `+ BDay(1)` | `2024-03-11` (pazartesi) |
| `+ BDay(0)` | `2024-03-11` (iş günü değilse sonrakine) |
| `- BDay(1)` | `2024-03-08` (cuma) |

**`(0)` ile `(1)` farkı:** `(0)` "zaten oradaysan kal", `(1)` "her durumda bir
sonrakine git". Tarih tam sınırda olmadıkça ikisi aynı sonucu veriyor.

## İş günü sayıları

```python
len(pd.bdate_range("2024-03-01", "2024-03-31"))     # 21
np.busday_count("2024-03-01", "2024-04-01")         # 21  (bitis haric)
np.busday_count("2024-04-01", "2024-05-01", holidays=list_of_dates)   # 18
pd.date_range(start, end, freq=CustomBusinessDay(holidays=...))
```

`np.busday_count` bitiş gününü **saymıyor**; `bdate_range` sayıyor.
