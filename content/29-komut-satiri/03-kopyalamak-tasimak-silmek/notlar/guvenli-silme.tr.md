`rm` geri alınamaz. Deneyimli kullanıcılar da yanlış dosyayı siler; fark,
bunu önleyen birkaç alışkanlıkta.

## Silmeden önce

1. **Neredesin?** `pwd`. Göreli yol bulunduğun klasöre göre çalışır; yanlış
   klasörde `rm -r tmp` başka bir `tmp`'yi siler.
2. **Ne sileceksin?** Önce aynı yolla `ls`: `ls project/cache`. Gördüğün
   listeyi silmek istiyorsan `ls` yerine `rm -r` yaz.
3. **Önemli mi?** Yedeğini al: `cp -r project project-backup`.

## Seçenekler

| Seçenek | Ne zaman |
|---|---|
| `-i` | Emin değilsen: her dosya için sorar |
| `-r` | Yalnızca klasör silerken |
| `-f` | Yalnızca betiklerde, ne yaptığını bildiğinde |

`-rf` birlikte "içindekilerle, sormadan, itiraz etmeden" demektir. En sık
felaketler bu iki harfle olur.

## Tehlikeli yazımlar

| Yazım | Neden tehlikeli |
|---|---|
| `rm -rf /` | Kök klasör; bu terminal ve modern Linux reddeder |
| `rm -rf ~` | Ev klasörünün tamamı |
| `rm -rf project /` | Araya kaçan bir boşluk: önce `project`, sonra `/` |
| `rm -r *` | Bulunduğun klasördeki her şey (joker karakterler bölümünde) |

## Çöp kutusu yok

Terminalde silinen dosya çöp kutusuna gitmez. Masaüstü ortamlarında çöp
kutusuna gönderen ayrı araçlar vardır (`gio trash` gibi), ama `rm` onlardan
biri değildir.
