Komut satırından bir CSV dosyasının adını alan bir program yaz: `python cozum.py students.csv`. Dosyanın başlık satırında `name` ve `house` sütunları var (sırası değişebilir). Program her binayı abece sırasıyla ve o binadaki öğrenci sayısıyla yazsın: `Gryffindor: 3`.

Sorunlu durumlarda `sys.exit` ile çıksın: argüman yoksa `Too few command-line arguments`, birden fazlaysa `Too many command-line arguments`, adı `.csv` ile bitmiyorsa `Not a CSV file`, dosya yoksa `File does not exist`. Klasörde `students.csv` ve sütunları ters sırada olan `club.csv` var.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py students.csv
Gryffindor: 3
Hufflepuff: 1
Ravenclaw: 2
Slytherin: 1
```
