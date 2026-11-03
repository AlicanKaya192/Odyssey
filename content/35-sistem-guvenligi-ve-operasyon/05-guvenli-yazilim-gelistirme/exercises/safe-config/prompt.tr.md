`load_config(user_config)` güvenli varsayılanlardan (`DEFAULTS`) başlasın;
kullanıcının verdiği ayarlardan yalnızca `DEFAULTS`'ta olan anahtarları
uygulasın. Ayrıca `session_minutes` hiçbir zaman 60'ı geçmesin (daha büyük
verilirse 60 olsun). Başlangıç kodu her anahtarı olduğu gibi kabul
ediyor.

**Beklenen çıktı:**

```
debug True
session_minutes 60
tls True
```
