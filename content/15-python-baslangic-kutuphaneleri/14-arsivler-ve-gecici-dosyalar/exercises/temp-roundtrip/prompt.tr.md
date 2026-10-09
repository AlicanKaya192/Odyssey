`temp_roundtrip(files)` fonksiyonunu yaz: `files` bir `{ad: metin}`
sözlüğü. `tempfile.TemporaryDirectory()` ile geçici bir klasör açsın, her
dosyayı içine yazsın ve blok içinde klasördeki adları sıralı liste olarak
alsın. Bloktan çıkınca klasörün hâlâ var olup olmadığına baksın ve
`(adlar, var_mı)` döndürsün. Sonuç `([...], False)` olmalı.

**Beklenen çıktı:**

```
(['a.txt', 'b.txt'], False)
```
