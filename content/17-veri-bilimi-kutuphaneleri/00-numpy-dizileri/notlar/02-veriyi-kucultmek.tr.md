Büyük bir ölçüm setinde her sütunun tipini **değerlerin aralığına göre**
seçmek belleği birkaç kat azaltır. Aşağıda yarım milyon satırlık bir hava
istasyonu verisi var: istasyon numarası, sıcaklık, nem.

```python
import numpy as np

rng = np.random.default_rng(7)
n = 500_000
station = rng.integers(0, 120, n)
temp = rng.normal(15, 8, n)
humidity = rng.integers(0, 101, n)
before = station.nbytes + temp.nbytes + humidity.nbytes


def smallest_int(values):
    for kind in (np.int8, np.int16, np.int32, np.int64):
        info = np.iinfo(kind)
        if values.min() >= info.min and values.max() <= info.max:
            return kind


small_station = station.astype(smallest_int(station))
small_humidity = humidity.astype(smallest_int(humidity))
small_temp = temp.astype(np.float32)
after = small_station.nbytes + small_temp.nbytes + small_humidity.nbytes
print(small_station.dtype, small_humidity.dtype, small_temp.dtype)
print(before // 1024, after // 1024, round(before / after, 1))
same_station = np.array_equal(station, small_station)
same_humidity = np.array_equal(humidity, small_humidity)
print(same_station, same_humidity)
print(float(np.abs(temp - small_temp).max()) < 1e-5)
```

```text
int8 int8 float32
11718 2929 4.0
True True
True
```

## Adımlar

1. **Aralığı ölç:** `values.min()` ve `values.max()`.
2. **Sığan en küçük tipi seç:** `np.iinfo` sınırlarıyla karşılaştır.
   İstasyon (0–119) ve nem (0–100) `int8`'e sığıyor.
3. **Ondalıkta duyarlığa karar ver:** sıcaklık için 7 basamak (`float32`)
   fazlasıyla yeter; fark 0,00001'in altında.
4. **Doğrula:** tam sayılar birebir aynı mı (`np.array_equal`)? Ondalık fark
   kabul edilebilir mi?

Sonuç: 11 718 KB'tan 2 929 KB'a, **4 kat** küçük.

## Dikkat

- Sonradan bu sütunlarla **hesap** yapılacaksa sonucun da sığması gerekir:
  `int8` nemleri toplamak taşar. Toplamadan önce `astype(np.int64)` ya da
  `sum(dtype=np.int64)`.
- Yeni veri geldikçe aralık değişebilir (121. istasyon). Tip seçimi bir
  kez değil, veri her yüklendiğinde denetlenir.
- pandas'ta aynı iş `pd.to_numeric(..., downcast="integer")` ile yapılır
  (pandas performansı bölümü).
