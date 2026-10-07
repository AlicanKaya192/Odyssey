Volume ve bind mount kullanırken en sık karşılaşılan şaşırtıcı durumlar.

## Bağlanan klasör içindekini gizler

İmajda `/app` klasöründe dosyalar varken `-v ${PWD}:/app` ile bilgisayarındaki
bir klasörü oraya bağlarsan, konteyner artık **yalnızca bağladığın klasörü**
görüyor; imajın `/app` içindekiler örtülüyor (silinmiyor, görünmüyor).

"Dosyam imajda vardı, konteynerde yok" sorununun sık sebebi bu.

**Boş bir volume** ilk kez bir klasöre bağlandığında ise Docker imajın o
klasördeki dosyalarını volume'a **kopyalıyor**. Volume doluysa kopyalamıyor.

## Klasör yolu hangi terminalde nasıl yazılır?

| Terminal | Şu anki klasör |
|---|---|
| PowerShell | `-v ${PWD}:/app` |
| Komut İstemi (cmd) | `-v %cd%:/app` |
| Git Bash | `-v "$(pwd)":/app` (yol çevrimi sorun çıkarabilir) |
| Linux / Mac | `-v "$(pwd)":/app` |

Tam yol da yazılabilir: `-v C:\Users\ada\project:/app`. Yolda boşluk varsa
tırnak içine al.

## `-v` mi, `--mount` mu?

İkisi aynı işi yapıyor. `--mount` daha uzun ama daha açık:

```text
--mount type=volume,source=notes,target=/data
--mount type=bind,source=${PWD},target=/app,readonly
```

`-v` ile bilgisayarındaki bir yolu yazarken yazım hatası yaparsan (yol yoksa)
Docker sessizce **boş bir klasör oluşturuyor**; `--mount` ise hata veriyor.

## İzinler

Konteynerin içindeki program kök olmayan bir kullanıcıyla çalışıyorsa
(Güvenlik bölümü) bağlanan klasöre yazamayabilir:
`PermissionError: [Errno 13] Permission denied: '/data/notes.txt'`. Çözüm
klasörün sahibini Dockerfile'da ayarlamak (`chown`); Güvenlik bölümünde.

## Windows'ta hız

Bind mount'ta dosyalar Windows ile WSL 2'deki Linux arasında gidip geliyor;
çok sayıda küçük dosyada (ör. `node_modules`, büyük veri) yavaşlayabiliyor.
Volume Linux'un içinde durduğu için hızlı. Büyük veri volume'a.

## Hangi volume'lar kullanılıyor?

```text
docker ps --format "{{.Names}}: {{.Mounts}}"
docker volume ls --filter dangling=true    # hiçbir konteynere bağlı olmayanlar
```
