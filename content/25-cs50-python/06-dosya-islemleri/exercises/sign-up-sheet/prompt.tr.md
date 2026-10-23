Kullanıcıdan adını ve evini iste, `students.csv`'nin sonuna `csv.DictWriter` ile bir satır ekle (sütunlar `name`, `home`). Adreste virgül olabilir (`Number Four, Privet Drive`); `csv` onu tırnağa alır. Dosyada başlık hazır, sen yazma. Windows'ta boş satır çıkmasın diye dosyayı `newline=""` ile aç.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın ve dosyan denetlenir):

```text
$ python cozum.py
Name: Harry
Home: Number Four, Privet Drive
```
