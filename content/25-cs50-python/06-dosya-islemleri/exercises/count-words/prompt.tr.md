Komut satırından bir dosya adı al (`python cozum.py notes.txt`) ve dosyadaki satır ve kelime sayısını `4 lines, 10 words` biçiminde yaz. Boş satır da satırdır; kelimeler boşlukla ayrılır (`split()`). Argüman sayısı yanlışsa `sys.exit("Usage: python cozum.py FILE")`, dosya yoksa `sys.exit("File does not exist")`.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın ve dosyan denetlenir):

```text
$ python cozum.py notes.txt
4 lines, 10 words
```
