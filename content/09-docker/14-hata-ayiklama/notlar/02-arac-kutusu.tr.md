Hata ayıklarken en çok işe yarayan komutlar, ne zaman kullanılacaklarıyla.

## Konteyner hiç başlamıyor ya da hemen bitiyor

```text
docker ps -a                             # durum ve çıkış kodu
docker logs web                          # son yazdıkları
docker run --rm -it --entrypoint sh app  # aynı imajın içine bak
```

## Konteyner çalışıyor ama yanlış davranıyor

```text
docker logs -f --tail 50 web             # canlı günlük
docker exec -it web sh                   # içinde gezin
docker exec web env                      # ortam değişkenleri doğru mu?
docker top web                           # içinde hangi süreçler var?
docker stats                             # bellek ve işlemci kullanımı (canlı)
```

## Ayarlar doğru mu?

```text
docker inspect web --format "{{.Config.Cmd}}"          # komut
docker inspect web --format "{{.Config.Env}}"          # ortam
docker inspect web --format "{{json .Mounts}}"         # bağlamalar
docker inspect web --format "{{.State.ExitCode}}"      # çıkış kodu
docker port web                                         # portlar
```

## Dosyalar

```text
docker cp web:/app/output.txt .          # konteynerden bilgisayara
docker cp ./config.json web:/app/        # bilgisayardan konteynere
docker diff web                          # imaja göre ne değişti
```

`docker cp` durmuş konteynerde de çalışıyor: çöken bir programın bıraktığı
günlük dosyasını almak için kullanışlı.

## Derleme

```text
docker build --progress=plain --no-cache -t app .   # bütün çıktı
docker build --target build -t app:debug .          # bir aşamada dur
docker history app                                  # hangi katman ne
```

## Odyssey'de

Odyssey'nin terminali derleme adımlarını (`CACHED` / `DONE`), derleme
hatasının son satırlarını ve konteynerin çıktısını gösteriyor. Ayrıntı
gerekirse aynı Dockerfile'ı PowerShell'de kendin kurup bu komutlarla
incele.
