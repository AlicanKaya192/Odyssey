Konteynerin çıkış kodu içindeki programın çıkış kodu. Python'da
`sys.exit(3)` programı 3 koduyla bitiriyor.

**Yapman gereken:** `python -c` ile çalışan bir `CMD` yaz: önce `failing`
yazsın, sonra programı **3** koduyla bitirsin. Kod tek satırda, komutlar
noktalı virgülle ayrılmış:

```python
import sys; print('failing'); sys.exit(3)
```

Köşeli parantezin içi zaten çift tırnak kullandığı için Python kodunda tek
tırnak (`'failing'`) kullan.

**Beklenen:** çıktı `failing`, konteynerin çıkış kodu `3`.
