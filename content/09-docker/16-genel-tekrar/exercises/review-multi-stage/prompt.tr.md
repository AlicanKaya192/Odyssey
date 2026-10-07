`report.py` bir rapor üretiyor. Raporu göstermek için Python gerekmiyor;
son imajda yalnızca rapor dosyası olsun.

**Yapman gerekenler:**

1. `build` adlı ilk aşama (`python:3.13-slim`): çalışma klasörü `/src`,
   `report.py`'yi kopyala ve `RUN python report.py > report.txt` ile raporu
   üret.
2. İkinci aşama (`alpine:3.22`): ilk aşamadan `/src/report.txt`'yi
   `/report.txt` olarak kopyala; `CMD ["cat", "/report.txt"]`.

Son imaj 20 MB'tan küçük olmalı.

**Beklenen çıktı:**

```
apples    12
pears      7
plums     30
total     49
```
