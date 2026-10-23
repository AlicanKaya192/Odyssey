Alıştırmanın klasöründe saydam zeminli bir tişört (`shirt.png`) ve üç fotoğraf var (`before1.jpg`, `before2.jpg`, `before3.jpg`; Odyssey için çizildi). Tişörtü fotoğraftaki kişinin üstüne giydirelim.

Komut satırından **iki** argüman alan bir program yaz: girdi resmi ve çıktı resmi (ikisi de JPEG ya da PNG). Girdiyi `Image.open` ile aç, `ImageOps.fit` ile (varsayılan ayarlarla) tişörtün boyuna getirip kırp, tişörtü `photo.paste(shirt, shirt)` ile üstüne koy (tişört hem resim hem maske) ve sonucu `Image.save` ile çıktıya yaz.

Şu durumlarda `sys.exit` ile çık: iki argüman yoksa (`Too few command-line arguments` / `Too many command-line arguments`), girdinin ya da çıktının uzantısı `.jpg`, `.jpeg`, `.png` değilse (büyük/küçük harf fark etmez; `Invalid input` / `Invalid output`), uzantıları farklıysa (`Input and output have different extensions`), girdi yoksa (`Input does not exist`). Programı çalıştırınca resmin **Çıktı** sekmesinde görünür. (CS50'de dosyanın adı `shirt.py`.)

İpucu: `os.path.splitext("before1.jpg")` `('before1', '.jpg')` verir.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı bir klasörde çalıştırıp çıktını ve yazdığın dosyayı karşılaştırıyor.

- Girdi yok → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py before1.jpg before2.jpg before3.jpg` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py before1.jpg invalid_format.bmp` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py before1.jpg after1.png` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py non_existent_image.jpg after1.jpg` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py before1.jpg after1.jpg` → yazılan dosya `after1.jpg`
- Komut `python cozum.py before2.jpg after2.jpg` → yazılan dosya `after2.jpg`
- Komut `python cozum.py before3.jpg after3.jpg` → yazılan dosya `after3.jpg`
