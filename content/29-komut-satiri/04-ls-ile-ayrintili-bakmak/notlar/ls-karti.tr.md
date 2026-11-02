`ls`'in en sık kullanılan seçenekleri.

| Seçenek | Adı | Ne yapar |
|---|---|---|
| `-l` | long | Her dosya bir satır: tür, izin, sahip, grup, boyut, tarih, ad |
| `-a` | all | Gizliler ve `./`, `../` |
| `-A` | almost all | Gizliler, `./` ve `../` olmadan |
| `-h` | human-readable | Boyutlar `K`, `M`, `G` ile (`-l` ile birlikte) |
| `-1` | one | Her ad ayrı satırda |
| `-R` | recursive | Alt klasörlerle birlikte |
| `-d` | directory | Klasörün içini değil kendisini |

## En çok kullanılan birleşimler

| Komut | Ne zaman |
|---|---|
| `ls -la` | Bir klasörde her şeye ayrıntılı bakmak |
| `ls -lh` | Hangi dosya büyük? |
| `ls -lah` | İkisi birden |
| `ls -ld klasör` | Klasörün izinlerine bakmak |

Birçok Linux'ta `ll` kısayolu `ls -l` (ya da `ls -alF`) için tanımlıdır.

## Gerçek ls'te olup bu terminalde olmayanlar

| Seçenek | Ne yapar |
|---|---|
| `-t` | Tarihe göre sıralar (en yeni üstte) |
| `-S` | Boyuta göre sıralar |
| `-r` | Sıralamayı tersine çevirir |

`ls -lt` "en son ne değişti" sorusunun hızlı cevabıdır.
