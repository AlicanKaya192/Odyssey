In a big measurement set, choosing each column's type **by the range of its
values** cuts memory several times. Below is half a million rows of weather
station data: station number, temperature, humidity.

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

## The steps

1. **Measure the range:** `values.min()` and `values.max()`.
2. **Pick the smallest type that fits:** compare with the `np.iinfo` limits.
   Station (0–119) and humidity (0–100) fit in `int8`.
3. **Decide the precision for decimals:** 7 digits (`float32`) are more than
   enough for temperature; the difference is below 0.00001.
4. **Check:** are the integers exactly the same (`np.array_equal`)? Is the
   decimal difference acceptable?

The result: from 11,718 KB to 2,929 KB, **4 times** smaller.

## Watch out

- If these columns will be used in **calculations** later, the results must
  fit too: summing `int8` humidity values overflows. Before summing,
  `astype(np.int64)` or `sum(dtype=np.int64)`.
- As new data arrives the range can change (a 121st station). The choice of
  type is checked every time the data is loaded, not once.
- In pandas the same job is done with `pd.to_numeric(..., downcast="integer")`
  (the pandas performance section).
