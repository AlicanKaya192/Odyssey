Bu Dockerfile çalışıyor, ama `main.py`'de tek harf değişse bile paketler
baştan kuruluyor.

**Yapman gereken:** sırayı düzelt: önce yalnızca `requirements.txt`'i
kopyala ve paketleri kur, sonra kodun geri kalanını kopyala.

**Beklenen çıktı:**

```
ready on Python 3.13
```
