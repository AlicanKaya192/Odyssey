Bu Dockerfile `CMD`'yi shell biçiminde yazıyor: konteynerin 1 numaralı süreci
Python değil `sh` ve `docker stop`'un sinyali programa ulaşmıyor.

**Yapman gereken:** son satırı aynı komutu çalıştıran **exec biçimine**
çevir. Komutun üç parçası var: `python`, `report.py`, `--short`.

**Beklenen çıktı:**

```
report mode: short
```
