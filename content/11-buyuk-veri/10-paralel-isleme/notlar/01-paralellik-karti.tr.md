Paralel kod yazmak için kalıplar ve karar tablosu.

## Süreç havuzu (saf Python hesabı)

```python
from concurrent.futures import ProcessPoolExecutor

def work(item):            # dosyanın en dış düzeyinde
    ...

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(work, items))
```

Çok sayıda küçük öğe varsa: `ex.map(work, items, chunksize=1_000)`.

## İş parçacığı havuzu (bekleme, NumPy)

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch, urls))
```

## Bitenin sırasıyla almak

```python
from concurrent.futures import as_completed

futures = [ex.submit(work, item) for item in items]
for f in as_completed(futures):
    print(f.result())          # hangisi önce biterse
```

`map` sonuçları verdiğin sırayla, `as_completed` bitme sırasıyla veriyor.

## `multiprocessing.Pool`

```python
from multiprocessing import Pool

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(work, items)
```

## Karar tablosu

| İş | Seçim |
|---|---|
| Saf Python döngüsü, ağır | Süreç havuzu |
| Ağdan / diskten bekleme | İş parçacığı havuzu |
| NumPy ağırlıklı hesap | İş parçacığı havuzu |
| pandas gruplama, küçük-orta veri | Paralel yapma; zaten hızlı |
| Dosyalarda SQL | DuckDB (bütün çekirdekleri kendisi kullanıyor) |
| pandas işini parçalara bölmek | dask (Bölüm 11) |

## Bu bilgisayarın ölçümleri

| İş | Sıralı | Paralel |
|---|---|---|
| Asal sayma, 4 süreç | 1,09 sn | 0,50 sn |
| Asal sayma, 4 iş parçacığı | 1,09 sn | 1,12 sn |
| 10 × 0,2 sn bekleme, 10 iş parçacığı | 2,01 sn | 0,21 sn |
| 10 000 küçük iş, 4 süreç | 0,0009 sn | 1,78 sn |
| pandas parçaları süreçlere | 0,09 sn | 1,14 sn |

## Amdahl yasası

```text
hızlanma = 1 / ((1 − p) + p / n)
```

| Paralel oran (p) | 4 çekirdek | 24 çekirdek | Sonsuz |
|---|---|---|---|
| %50 | 1,6 | 1,92 | 2 |
| %90 | 3,08 | 7,27 | 10 |
| %99 | 3,88 | 19,51 | 100 |
