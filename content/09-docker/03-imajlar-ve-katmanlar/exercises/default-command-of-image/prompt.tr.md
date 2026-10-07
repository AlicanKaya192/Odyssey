`docker image inspect python:3.13-slim --format "{{.Config.Cmd}}"`
`[python3]` gösteriyor: bu imajın varsayılan komutu etkileşimli Python.
Kendi `CMD` satırın onun yerine geçiyor.

**Yapman gereken:** `python -c` ile şu kodu çalıştıran bir `CMD` yaz:

```python
import sys; print(sys.version_info[:2])
```

`sys.version_info[:2]` Python'un büyük ve küçük sürümünü bir demet olarak
veriyor.

**Beklenen çıktı:**

```
(3, 13)
```
