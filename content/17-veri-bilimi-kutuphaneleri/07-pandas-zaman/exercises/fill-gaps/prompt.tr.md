`fill_gaps(dates, values, how)` tarih indeksli seriye `asfreq("D")` ile eksik
günleri eklesin ve `how`'a göre doldursun:

- `"zero"`: `fillna(0)`
- `"ffill"`: `ffill()`
- `"interpolate"`: `interpolate()`

Sonucu 1 basamağa yuvarlı liste olarak döndürsün.

**Beklenen çıktı:**

```
zero [40.0, 42.0, 0.0, 0.0, 51.0]
ffill [40.0, 42.0, 42.0, 42.0, 51.0]
interpolate [40.0, 42.0, 45.0, 48.0, 51.0]
```
