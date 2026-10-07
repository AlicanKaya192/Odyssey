`build_report.py` bir HTML raporu üretiyor; raporu göstermek için Python
gerekmiyor.

**Yapman gerekenler:** iki aşamalı bir Dockerfile:

1. `build` adında, `python:3.13-slim`'den bir aşama: çalışma klasörü `/src`,
   `build_report.py`'yi kopyala ve `RUN` ile çalıştır (rapor
   `/out/index.html`'e yazılıyor).
2. `alpine:3.22`'den son aşama: `build` aşamasından `/out`'u `/report`'a
   kopyala; konteyner çalışınca `cat /report/index.html`.

Odyssey son imajın **20 MB'tan küçük** olduğuna ve içinde Python
olmadığına bakacak.
