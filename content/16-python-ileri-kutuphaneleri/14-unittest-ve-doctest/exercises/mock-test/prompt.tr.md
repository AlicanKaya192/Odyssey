`weather.py` içindeki `advice(city)` sıcaklığı `fetch_temp`'ten alıyor;
`fetch_temp` ağa çıkıyor ve testte hata veriyor. `patch("weather.fetch_temp",
return_value=...)` ile sıcaklığı sahtele ve en az **üç** test yaz: 5 derece →
`"coat"`, 20 derece → `"t-shirt"` ve sınır: **10 derece → `"t-shirt"`**.

**Beklenen çıktı:**

```

```
