Dockerfile ve `.env` hazır. `compose.yaml`'ı yaz.

**Yapman gerekenler:** `web` adlı bir servis:

1. İmajı bu klasörden kursun (`build: .`).
2. Bilgisayarın 8095'i konteynerin 8000'ine gitsin (tırnak içinde).
3. Ortam değişkenlerini `.env` dosyasından alsın.
4. `notes-data` adlı volume `/data`'ya bağlansın; volume'u en altta da
   tanımla.
5. `restart: unless-stopped`.

Odyssey servisi açacak, `healthy` olmasını bekleyecek ve `/stats`'a
bakacak:

```
{"notes": 0, "starts": 1}
```
