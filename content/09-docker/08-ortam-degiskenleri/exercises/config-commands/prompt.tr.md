**Yapman gerekenler:** `commands.sh` dosyasına sırayla üç komut yaz:

1. `app` imajını `APP_ENV=production` ortam değişkeniyle çalıştır; bitince
   silinsin.
2. `app` imajını `app.env` dosyasındaki değişkenlerle çalıştır; bitince
   silinsin.
3. Bu klasördeki Dockerfile'dan `app` imajını `VERSION=2.1` derleme
   argümanıyla kur.
