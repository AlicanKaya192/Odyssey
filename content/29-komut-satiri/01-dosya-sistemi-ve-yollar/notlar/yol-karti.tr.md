Yolları yazarken ve `cd` ile dolaşırken bakacağın kart.

## İşaretler

| İşaret | Anlamı | Örnek |
|---|---|---|
| `/` (başta) | Kökten başla | `/etc/hostname` |
| `/` (arada) | Klasörleri ayırır | `projects/site/css` |
| `~` | Ev klasörü (`/home/ada`) | `~/notes` |
| `.` | Bulunduğun klasör | `./notes` = `notes` |
| `..` | Bir üst klasör | `../api` |

## cd

| Komut | Nereye gider |
|---|---|
| `cd notes` | Buradaki `notes` klasörüne |
| `cd projects/site` | İki kat aşağı |
| `cd ..` | Bir kat yukarı |
| `cd ../..` | İki kat yukarı |
| `cd ../api` | Yukarı çık, yandaki `api`'ye gir |
| `cd /etc` | Mutlak yol: her yerden `/etc` |
| `cd`, `cd ~` | Ev klasörü |
| `cd ~/notes` | Ev klasöründeki `notes`, her yerden |
| `cd -` | Bir önceki klasör (vardığı yeri yazar) |
| `cd "my notes"` | Adında boşluk olan klasör |

## Mutlak mı, göreli mi?

- Başında `/` ya da `~` varsa **mutlak**: nerede olduğun fark etmez.
- Yoksa **göreli**: bulunduğun klasörden başlar. Çalışmıyorsa önce `pwd`.

## Hatalar

| Gördüğün | Anlamı |
|---|---|
| `No such file or directory` | O adda klasör yok ya da yanlış yerdesin |
| `Not a directory` | Verdiğin şey dosya |
| `too many arguments` | İki yol verdin; boşluklu adı tırnakla yaz |
