## Kurmak

```python
s = pd.read_csv("f.csv", index_col="date", parse_dates=True)["value"]
s = s.sort_index()

df = df.set_index("date").sort_index()   # sutundan indekse
df = df.reset_index()                    # indeksten sutuna geri
```

## Seçmek

| Yazılan | Seçilen |
|---|---|
| `s.loc["2024-03-09"]` | Tek gün (tek değer) |
| `s.loc["2024-03"]` | Mart 2024'ün tamamı |
| `s.loc["2024"]` | 2024'ün tamamı |
| `s.loc["2024-03-04":"2024-03-10"]` | İki uç **dahil** |
| `s.loc["2024-01":"2024-03"]` | Ocak başından Mart sonuna |
| `s.loc[:"2024-06-30"]` | Baştan o güne kadar |
| `s.loc["2024-12-25":]` | O günden sona |
| `s.loc["2024-03-15 08:00":"2024-03-15 12:00"]` | Saat aralığı (saatlik veri) |
| `s.iloc[-7:]` | Son 7 **satır** (tarihten bağımsız) |
| `s.truncate(before="2024-12-01")` | O tarihten öncesini at |
| `s[s.index.dayofweek >= 5]` | Hafta sonları |
| `s[s.index.month == 12]` | Bütün Aralık ayları |
| `s.between_time("08:00", "18:00")` | Her günün o saatleri |
| `s.at_time("18:00")` | Her günün tam o saati |

**Tek gün ile aralık farkı:** günlük veride `s.loc["2024-03-09"]` tek bir sayı
veriyor; saatlik veride aynı yazım o günün 24 satırını veriyor.

## İndeksin özellikleri

```python
s.index.min(), s.index.max()
s.index[-1] - s.index[0]              # toplam sure
s.index.year, s.index.month, s.index.day
s.index.dayofweek, s.index.day_name()
s.index.hour                          # saatlik veride
s.index.normalize()                   # saatleri sifirla
s.index.is_monotonic_increasing       # sirali mi
s.index.is_unique                     # tekrar yok mu
s.index.freq                          # frekans (None olabilir)
pd.infer_freq(s.index)                # frekans tahmini
```

## Temizlik reçetesi

```python
s = pd.read_csv("f.csv", index_col="date", parse_dates=True)["value"]

# 1. Sirala
s = s.sort_index()

# 2. Tekrarlar
print(s.index.duplicated().sum())
s = s.groupby(level=0).sum()          # ya da .last() / .mean() / ~duplicated()

# 3. Eksikler
full = pd.date_range(s.index.min(), s.index.max(), freq="D")
print(full.difference(s.index))

# 4. Takvime oturt
s = s.asfreq("D")
print(s.isna().sum())
```

Adımların sırası önemli: tekrar varken `asfreq` hata veriyor, sıralı değilken
dilimleme çalışmıyor.

## Tekrarları çözmek

| Yöntem | Ne zaman |
|---|---|
| `s.groupby(level=0).sum()` | Değer bir toplamın parçaları (satış, adet) |
| `s.groupby(level=0).mean()` | Aynı anın birden çok ölçümü (sıcaklık) |
| `s.groupby(level=0).last()` | Sonradan gelen düzeltme geçerli |
| `s.groupby(level=0).first()` | İlk kayıt geçerli |
| `s[~s.index.duplicated(keep="first")]` | Birebir aynı satır iki kez gelmiş |

## Eksikliği ölçmek

```python
gaps = s.index.to_series().diff()
print(gaps.value_counts())     # 1 gun: 352, 2 gun: 3, 3 gun: 1, 4 gun: 1
print(gaps.max())              # en uzun bosluk
```

İki satır arasındaki fark 1 günden büyükse arada eksik gün var. 4 günlük fark,
arada 3 eksik gün demek.

## `asfreq`, `reindex`, `resample`

| Araç | Ne yapıyor |
|---|---|
| `s.asfreq("D")` | Tam takvime oturtur, eksikler `NaN` |
| `s.asfreq("D", fill_value=0)` | Eksikleri sabit değerle doldurur |
| `s.reindex(full)` | Verdiğin herhangi bir indekse oturtur |
| `s.resample("D").sum()` | Frekansı **değiştirir** ve toplar (Bölüm 05) |

`asfreq` değerleri değiştirmiyor, yalnızca satır açıyor. `resample` ise
gruplayıp bir işlem uyguluyor; ikisi karıştırılmamalı.
