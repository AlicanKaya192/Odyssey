`app.py` ayarlarını sabit yazıyor. Ortam değişkenlerinden okusun.

**Yapman gerekenler:**

1. `env`'i `APP_ENV` değişkeninden oku; yoksa `"development"`.
2. `port`'u `PORT` değişkeninden oku; yoksa `8000`. Sayı olarak kullanılıyor
   (`port + 0`), yani `int(...)` gerekli.

Odyssey konteyneri iki kez çalıştıracak: değişkensiz ve
`-e APP_ENV=production -e PORT=9000` ile.

**Beklenen çıktılar:**

```
env: development port: 8000
env: production port: 9000
```
