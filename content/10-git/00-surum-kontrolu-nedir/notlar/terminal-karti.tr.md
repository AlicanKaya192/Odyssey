Git ile çalışırken en sık kullanacağın kabuk komutları. Hepsi Git Bash'te,
Mac'te ve Linux'ta aynı.

## Nerede olduğunu görmek

| Komut | Ne yapar |
|---|---|
| `pwd` | Bulunduğun klasörün tam yolu. |
| `ls` | Klasördekiler; klasörlerin sonunda `/`. |
| `ls -a` | Gizlilerle birlikte (`.git/` burada görünür). |

## Dolaşmak

| Komut | Ne yapar |
|---|---|
| `cd notes` | `notes` klasörüne gir. |
| `cd notes/site` | İki kat birden in. |
| `cd ..` | Bir üst klasöre çık. |
| `cd ../..` | İki üst klasöre çık. |
| `cd ~` ya da yalnızca `cd` | Ev klasörüne dön. |

Yollarda `~` ev klasörün, `.` bulunduğun klasör, `..` bir üstü demek.

## Oluşturmak ve silmek

| Komut | Ne yapar |
|---|---|
| `mkdir notes` | Klasör aç. |
| `mkdir -p a/b/c` | İç içe klasörleri tek seferde aç. |
| `touch a.txt` | Boş dosya oluştur (varsa dokunmaz). |
| `echo "metin" > a.txt` | Dosyayı **baştan** yaz. |
| `echo "metin" >> a.txt` | Dosyanın **sonuna** ekle. |
| `cat a.txt` | Dosyayı ekrana yaz. |
| `mv a.txt b.txt` | Adını değiştir ya da taşı. |
| `rm a.txt` | Dosyayı sil. |
| `rm -r eski` | Klasörü içindekilerle birlikte sil. |

## Birkaç kolaylık

- **↑ / ↓**: önceki komutlar arasında gezin.
- **Tab**: dosya ve klasör adını tamamlar (gerçek terminalde; Odyssey'nin
  alıştırma terminalinde yok).
- **`clear`** ya da **Ctrl+L**: ekranı temizler, hiçbir şeyi silmez.
- **`komut1 && komut2`**: birincisi başarılı olursa ikincisini çalıştırır.
  `mkdir notes && cd notes` sık görülen bir kalıp.

## Dikkat

- `rm` geri dönüşüm kutusuna göndermez; silinen dosya gider.
- `>` dosyanın eski içeriğini sorgusuz siler.
- Boşluk içeren adları tırnakla yaz: `cd "my notes"`. Daha iyisi: dosya ve
  klasör adlarında boşluk kullanma.
