Bazı tablolar aynı anahtarı değil **en yakın zamanı** paylaşır. Bir işlem
saat 09:00:07'de yapıldı; fiyat tablosunda o saniye yok, 09:00:05'te
güncellenmiş fiyat var. Doğru eşleşme "o andan önceki son fiyat". `merge`
birebir eşitlik ister ve hiçbirini eşleştirmez; `merge_asof` tam bunun için.

```python
import pandas as pd


def at(*times):
    return pd.to_datetime(list(times), format="%H:%M:%S")


trades = pd.DataFrame({"time": at("09:00:03", "09:00:07", "09:01:30"),
                       "qty": [5, 2, 8]})
quotes = pd.DataFrame({"time": at("09:00:00", "09:00:05", "09:01:00"),
                       "price": [10.0, 10.2, 10.1]})
both = pd.merge_asof(trades, quotes, on="time")
print(both["price"].tolist())
near = pd.merge_asof(trades, quotes, on="time", tolerance=pd.Timedelta("20s"))
print(near["price"].tolist())
fwd = pd.merge_asof(trades, quotes, on="time", direction="forward")
print(fwd["price"].tolist())
print(both.assign(time=both["time"].dt.strftime("%H:%M:%S")))
```

```text
[10.0, 10.2, 10.1]
[10.0, 10.2, nan]
[10.2, 10.1, nan]
       time  qty  price
0  09:00:03    5   10.0
1  09:00:07    2   10.2
2  09:01:30    8   10.1
```

## Nasıl çalışır?

- Soldaki her satır için sağda zamanı **kendisinden küçük ya da eşit** olan
  son satırı alır (`direction="backward"`, varsayılan). 09:00:07'deki işlem
  09:00:05'teki 10,2 fiyatını aldı.
- `tolerance=pd.Timedelta("20s")`: en yakın fiyat 20 saniyeden eskiyse
  eşleştirme; `NaN` bırak. 09:01:30'daki işlemin son fiyatı 30 saniye önceydi,
  bu yüzden boş kaldı. Bayat veriyle hesap yapmamak için önemli.
- `direction="forward"` bir sonraki değeri alır; `"nearest"` hangisi
  yakınsa onu.

## Şartlar

- İki tablo da `on` sütununa göre **sıralı** olmalı; değilse pandas hata
  verir (`left keys must be sorted`). Önce `sort_values("time")`.
- Birden fazla nesnenin zaman serisi aynı tablodaysa (birçok hisse) `by="symbol"`
  her nesneyi kendi içinde eşleştirir.
- Sensör ölçümünü en yakın hava durumu kaydıyla, siparişi o anki kurla,
  olayı o anki ayarla eşleştirmek hep aynı kalıp.
