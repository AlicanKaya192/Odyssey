Değişkenlerin bütün yazımları, bir bakışta.

## Tanımlamak ve kullanmak

| Yazım | Ne yapar |
|---|---|
| `ad=Ada` | Tanımlar; `=` çevresinde boşluk yok |
| `ad="Ada Lovelace"` | Boşluklu değer tırnakla |
| `echo "$ad"` | Değeri kullanır |
| `echo "${ad}_2026"` | Adın sınırı belli |
| `echo '$ad'` | Tek tırnakta açılmaz: `$ad` yazar |
| `unset ad` | Kaldırır |

## Genişletmeler

| Yazım | Sonuç |
|---|---|
| `$(komut)` | Komutun çıktısı |
| `$((3 * 4))` | `12` (tam sayı) |
| `${ad:-yedek}` | `ad` boşsa `yedek` |
| `${#ad}` | Değerin uzunluğu |

## Ortam

| Yazım | Ne yapar |
|---|---|
| `export AD=değer` | Ortam değişkeni (alt programlar görür) |
| `export ad` | Var olan değişkeni ortama çıkarır |
| `AD=değer komut` | Yalnızca o komut için |
| `env` | Bütün ortam değişkenleri |
| `printenv AD` | Tek bir ortam değişkeni |

## Hazır değişkenler

| Ad | Değer |
|---|---|
| `HOME` | Ev klasörü |
| `USER` | Kullanıcı adı |
| `PWD` | Bulunduğun klasör |
| `SHELL` | Kullanılan kabuk |
| `PATH` | Komutların arandığı klasörler (`:` ile) |

## Hatırla

- Kendi değişkenlerine küçük harfli ad ver; büyük harfliler sistemin.
- İçinde boşluk olabilecek değişkeni hep `"$ad"` diye kullan.
- Tanımsız değişken hata vermez, boş olur: adını doğru yazdığından emin ol.
