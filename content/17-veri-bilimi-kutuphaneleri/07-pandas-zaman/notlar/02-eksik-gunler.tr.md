Gerçek kayıtlarda günler eksik olur: dükkân kapalıydı, sensör çalışmadı,
kimse gelmedi. Satır satır çalışan bir hesap bu boşluğu **görmez**: 3 Mart ile
6 Mart arka arkaya iki satırsa, "iki günlük ortalama" aslında dört güne
yayılır.

```python
import pandas as pd

days = pd.to_datetime(["2026-03-02", "2026-03-03", "2026-03-06", "2026-03-07"])
visits = pd.Series([40, 42, 50, 47], index=days)
print(visits.rolling(2).mean().tolist())
full = visits.asfreq("D")
print(len(visits), len(full), full.isna().sum())
print(full.fillna(0).tolist())
print(full.ffill().tolist())
print(full.interpolate().round(1).tolist())
print(visits.asfreq("D", fill_value=0).rolling(2).mean().tolist())
```

```text
[nan, 41.0, 46.0, 48.5]
4 6 2
[40.0, 42.0, 0.0, 0.0, 50.0, 47.0]
[40.0, 42.0, 42.0, 42.0, 50.0, 47.0]
[40.0, 42.0, 44.7, 47.3, 50.0, 47.0]
[nan, 41.0, 21.0, 0.0, 25.0, 48.5]
```

## Önce boşluğu görünür yap

`asfreq("D")` indeksi her günü içerecek şekilde doldurur; olmayan günler
`NaN` olur. 4 satır 6'ya çıktı, 2 gün eksikmiş. Boşluk artık görünüyor; nasıl
doldurulacağı ise verinin **anlamına** bağlı:

| Yöntem | Ne zaman doğru | Burada |
|---|---|---|
| `fillna(0)` | eksik gün gerçekten sıfırsa (kapalı dükkân) | 0, 0 |
| `ffill()` | değer bir sonraki ölçüme kadar geçerliyse (fiyat, stok) | 42, 42 |
| `interpolate()` | arada düzgün bir geçiş varsa (sıcaklık) | 44,7, 47,3 |
| bırak (`NaN`) | bilinmiyorsa; hesap eksikleri atlasın | — |

## Fark ediyor mu?

İlk satırda iki günlük ortalama 6 Mart için 46 diyor (42 ile 50'nin
ortalaması); oysa 4 ve 5 Mart'ta ziyaretçi yoktu. Eksik günler 0 olarak
eklenince aynı ortalama **25**. Hangisinin doğru olduğu "eksik gün sıfır mı,
bilinmiyor mu?" sorusunun cevabına bağlı; ama bu soruyu sormak ancak boşluğu
görünce mümkün.

`asfreq` ile `resample` farkı: `asfreq` yalnızca **yeniden dizer** (her gün
bir satır, değer olduğu gibi); `resample` **toplar** (birden fazla değer bir
kovaya düşerse birleştirir).
