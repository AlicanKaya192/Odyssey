Docker'la çalıştıkça imajlar, durmuş konteynerler ve derleme önbelleği
birikiyor. Önce ne kadar yer kapladığına bak, sonra yalnızca gerekeni sil.

## Ne kadar yer kaplıyor?

```text
docker system df
```

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          2         0         191.2MB   191.2MB (99%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     20        0         60.85MB   14MB
```

- **ACTIVE**: şu anda bir konteynerin kullandıkları.
- **RECLAIMABLE**: silinirse boşalacak yer.

## Temizlik komutları, küçükten büyüğe

| Komut | Neyi siler? |
|---|---|
| `docker rm ad` | Tek bir konteyneri |
| `docker rmi imaj:etiket` | Tek bir imajı (ya da yalnızca bir adını) |
| `docker container prune` | Bütün **durmuş** konteynerleri |
| `docker image prune` | **Adsız** (`<none>`) imajları |
| `docker image prune -a` | Hiçbir konteynerin kullanmadığı **bütün** imajları |
| `docker builder prune` | Derleme önbelleğini |
| `docker volume prune` | Kullanılmayan volume'ları (**veri gider**) |
| `docker system prune` | Durmuş konteynerler + adsız imajlar + boştaki ağlar + önbellek |

Hepsi silmeden önce ne yapacağını söyleyip `y/N` onayı istiyor. `-f`
eklenirse sormuyor; betiklerde kullanılır, elle yazarken gerek yok.

## Dikkat edilecekler

- **`volume prune` veriyi siliyor.** Bir veritabanının verisi volume'daysa
  geri gelmez. Volume bölümüne kadar buna dokunma.
- **`image prune -a`** kullanılmayan bütün imajları siliyor; `python:3.13-slim`
  da gidebilir ve bir dahaki derlemede yeniden indirilir (internet gerekir).
- **Odyssey'nin imajları** `odyssey-ex-...` adlı. Onları Ayarlar › Docker'dan
  silmek daha güvenli: yalnızca Odyssey'nin işaretlediklerine dokunuyor.

## Bir alışkanlık

Haftada bir `docker system df`'e bakmak yetiyor. Denemeler için
konteynerleri `--rm` ile çalıştırırsan durmuş konteyner zaten birikmiyor.
