Bir API isteğinin adresi elinde. `urlparse` ile parçalarına ayır.

**Yapman gerekenler:**

1. `urllib.parse` modülünden `urlparse`'ı içe aktar.
2. `url`'yi ayır.
3. Şemayı, ana makineyi, portu, yolu, sorgu dizesini ve parçayı aşağıdaki
   biçimde yazdır.

**Beklenen çıktı:**

```
scheme: https
host: api.weather.test
port: 9000
path: /v2/forecast
query: city=Izmir&days=3
fragment: top
```

Ana makine için `.hostname` kullan: `.netloc` portu da içerir
(`api.weather.test:9000`).
