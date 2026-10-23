Veri çoğu zaman temizlenmeye muhtaçtır. Alıştırmanın klasöründeki `before.csv`'de öğrencilerin adı tek sütunda, `Soyad, Ad` biçiminde duruyor (`"Abbott, Hannah"`), yanında binası (`house`).

Komut satırından **iki** argüman alan bir program yaz: okunacak CSV'nin adı (sütunlar `name`, `house`) ve yazılacak yeni CSV'nin adı. Program her adı ayrı ad ve soyada bölüp yeni dosyaya `first`, `last`, `house` sütunlarıyla (bu sırayla, başlık satırıyla) yazsın. Her öğrencinin adı ve soyadı olduğunu varsay.

İki argüman yoksa (`Too few command-line arguments` / `Too many command-line arguments`) ya da ilk dosya okunamıyorsa (`Could not read invalid_file.csv`, dosyanın adıyla) `sys.exit` ile çık. (CS50'de dosyanın adı `scourgify.py`.)

İpucu: `csv.DictReader` ve `csv.DictWriter`; başlığı `writer.writeheader()` yazar. Windows'ta boş satır çıkmasın diye yazacağın dosyayı `newline=""` ile aç.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı bir klasörde çalıştırıp çıktını ve yazdığın dosyayı karşılaştırıyor.

- Girdi yok → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py 1.csv 2.csv 3.csv` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py invalid_file.csv output.csv` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py before.csv after.csv` → yazılan dosya `after.csv`
- Komut `python cozum.py class.csv clean.csv` → yazılan dosya `clean.csv`
