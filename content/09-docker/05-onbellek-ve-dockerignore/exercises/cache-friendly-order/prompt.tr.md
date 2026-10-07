Bu Dockerfile çalışıyor ama her kod değişikliğinde `pip install` baştan
çalışıyor.

**Yapman gereken:** sırayı önbellek dostu yap: önce yalnızca
`requirements.txt`'yi kopyala, paketleri kur, **sonra** kodun tamamını
kopyala.

Çalıştırdıktan sonra `app.py`'de değişiklik yapamazsın (salt okunur) ama
terminaldeki adımlara bak: ikinci çalıştırmada hepsi `CACHED`.

**Beklenen çıktı:**

```
built with a warm cache
```
