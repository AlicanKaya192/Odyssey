Docker ve Python'un en sık hata mesajları, sebepleri ve çözümleri. Mesajın
bir parçasını bu sayfada ara.

## Derleme

| Mesaj | Sebep | Çözüm |
|---|---|---|
| `unknown instruction: FORM` | Talimatta yazım hatası | Önerilen adı yaz (`FROM`) |
| `"/x": not found` | Dosya bağlamda yok ya da `.dockerignore`'da | Adı, klasörü, `.dockerignore`'u denetle |
| `did not complete successfully: exit code: 1` | Bir `RUN` düştü | Üstündeki satırlarda komutun kendi hatası |
| `No matching distribution found` | pip paketi bulamadı (ad, sürüm ya da internet) | Paket adını ve sürümünü denetle |
| `pull access denied` / `not found` (FROM'da) | Taban imajın adı ya da etiketi yanlış | `python:3.13-slim` gibi doğru ad |
| `failed to connect to the docker API` | Docker Desktop kapalı | Docker Desktop'ı aç |

## Çalışma

| Mesaj | Sebep | Çözüm |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | Dosya kopyalanmamış ya da paket kurulmamış | `COPY`, requirements.txt |
| `can't open file '/app/app.py'` | Dosya başka klasörde | `WORKDIR` ve `COPY` hedefi |
| `exec: "x": executable file not found in $PATH` | Komut yok ya da yazım hatası | `CMD` / `ENTRYPOINT` |
| `Permission denied` | Kullanıcı o klasöre yazamıyor | `chown` |
| `Address already in use` | Program aynı portu iki kez açmaya çalışıyor | Tek sunucu; port ayarı |
| `port is already allocated` | Ana makine portu dolu | Başka bir `-p` |
| `Connection refused` | Hedef dinlemiyor (localhost, kapalı servis) | Adres, `0.0.0.0`, servis adı |
| `No address associated with hostname` | Servis adı yanlış ya da aynı ağda değil | Ad, ağ |
| `Read-only file system` | `--read-only` ile yazılmaya çalışılıyor | Yazılacak yere volume |
| `Killed` / çıkış kodu 137 | Bellek sınırı ya da zorla durdurma | `--memory`, `docker stats` |

## Compose

| Mesaj | Sebep | Çözüm |
|---|---|---|
| `did not find expected key` | YAML girintisi bozuk | Sekme yerine boşluk, hizalama |
| `refers to undefined volume` | Adlı volume en alttaki `volumes:`'ta yok | Tanımla |
| `has no healthcheck configured` | `service_healthy` beklenen serviste denetim yok | `healthcheck` ekle |
| `dependency failed to start` | Bağlı servis başlayamadı ya da sağlıksız | O servisin günlüğü |
