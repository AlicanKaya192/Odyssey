Yanında aksanlı adlar içeren `names.txt` var; hazır `ascii_lines`
fonksiyonu dosyayı okuyup her satırı `strip_accents`'ten geçiriyor.

`strip_accents(text)` fonksiyonunu yaz: metni
`unicodedata.normalize("NFD", ...)` ile ayrıştırsın ve kategorisi `"Mn"`
olan karakterleri (aksan işaretleri) atıp kalanları birleştirsin.

**Beklenen çıktı:**

```
Cafe Creme
Unlu Seker
Zoe Saldana
plain
```
