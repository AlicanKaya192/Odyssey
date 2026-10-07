Bu Dockerfile'da üç güvenlik sorunu var:

1. Taban imajın sürümü sabit değil (`latest`).
2. Bir şifre `ENV` ile imaja gömülmüş.
3. Program açıkça root olarak çalışıyor.

**Yapman gereken:** üçünü de düzelt: `python:3.13-slim`, şifre satırını
kaldır (şifre çalıştırırken verilecek), `useradd` ile `app` kullanıcısı
oluşturup ona geç.

**Beklenen çıktı** (Odyssey şifreyi vermeden çalıştırıyor):

```
user: app
password set: False
```
