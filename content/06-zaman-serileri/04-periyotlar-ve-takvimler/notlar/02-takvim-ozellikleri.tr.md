Takvimden türetilen sütunlara **takvim özellikleri** deniyor. Analizde
gruplama anahtarı, ileride (Bölüm 19) makine öğrenmesi modelinin girdisi
oluyorlar. Hepsi **tahmin yapılacak gün için önceden bilinir**; bu yüzden
sızıntı riski taşımıyorlar.

## Temel özellikler

```python
idx = s.index

features = pd.DataFrame({
    "year": idx.year,
    "quarter": idx.quarter,
    "month": idx.month,
    "day": idx.day,
    "dayofweek": idx.dayofweek,
    "dayofyear": idx.dayofyear,
    "week": idx.isocalendar().week.to_numpy(),
    "is_weekend": idx.dayofweek >= 5,
    "is_month_start": idx.is_month_start,
    "is_month_end": idx.is_month_end,
}, index=idx)
```

## Ay içindeki konum

| Özellik | Kod | Ne işe yarar |
|---|---|---|
| Ayın kaçıncı günü | `idx.day` | Maaş günü, fatura günü etkisi |
| Ay sonuna kalan gün | `((idx + MonthEnd(0)) - idx).days` | Ay sonu kapanışı |
| Ayın kaçıncı haftası | `(idx.day - 1) // 7 + 1` | "Ayın ilk haftası" etkisi |
| Ayın gün sayısı | `idx.days_in_month` | Aylık toplamı düzeltmek için |

## Tatil ve iş günü

```python
holidays = pd.read_csv("holidays_2024.csv", parse_dates=["date"])["date"]

is_holiday = idx.isin(holidays)
is_workday = (idx.dayofweek < 5) & ~is_holiday
day_before_holiday = (idx + pd.Timedelta(days=1)).isin(holidays)
day_after_holiday = (idx - pd.Timedelta(days=1)).isin(holidays)
```

Tatilin kendisi kadar **öncesi ve sonrası** da önemli: bayramdan önceki gün
alışveriş artar, bayram günü mağaza kapalıdır, ertesi gün yavaş başlar. Üç ayrı
özellik, üç ayrı etki.

## Tatil listesi hazırlamak

pandas'ta hazır olarak yalnızca ABD federal tatilleri var
(`USFederalHolidayCalendar`). Başka bir ülke için listeyi kendin tutuyorsun.
Dikkat edilecekler:

- **Dini bayramlar her yıl başka güne düşüyor.** Tek bir yılın listesi bir
  sonraki yıl için geçersiz; her yılın tarihlerini ayrı yaz.
- **Hafta sonuna düşen tatil.** İş günü sayısını değiştirmiyor ama satış
  desenini değiştirebiliyor.
- **Yarım günler** (arife). Tam gün gibi davranmıyorlar; ayrı bir sütunla
  işaretle.
- **Köprü günleri.** Tatil perşembeye düşünce cuma resmî olarak iş günü ama
  fiilen boş.
- **Geleceği de yaz.** Tahmin yapacağın dönemin tatillerini bilmiyorsan model
  onları kullanamıyor.

## Ayları adil karşılaştırmak

| Durum | Bölünecek sayı |
|---|---|
| Her gün gerçekleşen şey (mağaza satışı, tüketim) | Ayın gün sayısı: `idx.days_in_month` |
| Yalnızca iş günü gerçekleşen şey (fatura, üretim) | Ayın iş günü sayısı |
| Hafta içi–hafta sonu çok farklıysa | Ayda kaç cumartesi olduğuna da bak |

```python
monthly = s.groupby(s.index.to_period("M")).sum()
per_day = monthly / monthly.index.days_in_month

workdays = pd.Series(1, index=pd.bdate_range("2024-01-01", "2024-12-31"))
workdays_per_month = workdays.groupby(workdays.index.to_period("M")).sum()
```

**Beş cumartesili ay.** Bir ayda 4 ya da 5 cumartesi olabiliyor. Cumartesi
satışı pazartesinin 1.5 katıysa, beş cumartesili ay hiçbir şey değişmeden
daha yüksek toplam veriyor. Bu etkiye **işlem günü etkisi** (trading day
effect) deniyor.

## Aynı günü geçen yılla karşılaştırmak

```python
last_year = s.copy()
last_year.index = last_year.index + pd.DateOffset(years=1)
change = s / last_year - 1
```

Dikkat: "geçen yılın aynı tarihi" haftanın **başka bir gününe** düşüyor
(9 Mart 2024 cumartesi, 9 Mart 2023 perşembe). Haftalık deseni güçlü olan
seride 364 gün (tam 52 hafta) geri gitmek daha adil:
`s.shift(364)` (Bölüm 06).
