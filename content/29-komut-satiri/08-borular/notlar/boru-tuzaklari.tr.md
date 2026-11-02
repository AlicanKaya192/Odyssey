Boruyla ilk çalışırken en sık yapılan yanlışlar.

## Borunun sağına dosya yazmak

`sort names.txt | top.txt` çalışmaz: kabuk `top.txt` adında bir program arar.
Borunun sağında her zaman bir **komut** durur. Dosyaya yazmak için `>`:
`sort names.txt > top.txt`.

## Dosya adını boruyla vermek

`echo names.txt | cat` dosyanın içini göstermez; `names.txt` yazısını basar.
Boru metni taşır. Dosyayı açtırmak istiyorsan adı argüman olarak ver:
`cat names.txt`.

## Girdi okumayan komuta boru

`ls`, `cd`, `mkdir`, `rm` borudan gelen metne bakmaz. `echo docs | ls`
`docs`'u değil bulunduğun klasörü listeler.

## Hataların sayılmaması

`ls a nope | wc -l` hata satırını saymaz, çünkü hata stderr'den gider ve
boruya girmez. Saymak istiyorsan `ls a nope 2>&1 | wc -l`.

## Sırayı karıştırmak

`tail -n 2 poem.txt | cat -n` son iki satırı **1 ve 2** diye numaralar; `cat -n`
yalnızca kendisine gelen iki satırı görür. Gerçek numaralar için önce
numarala, sonra kes: `cat -n poem.txt | tail -n 2`.

## Hepsini bir kerede yazmak

Uzun bir zinciri tek seferde yazıp çalıştırırsan yanlış adımı bulmak zorlaşır.
Her `|`'den sonra çalıştır, çıktıya bak, sonra bir sonraki adımı ekle.
