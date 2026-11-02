Bu bölümün komutları, bir bakışta.

## cp

| Komut | Ne yapar |
|---|---|
| `cp a.txt b.txt` | a.txt'nin kopyası b.txt (varsa üstüne yazar) |
| `cp a.txt backup/` | `backup/a.txt` olarak kopyalar |
| `cp a.txt b.txt backup/` | İkisini de klasöre |
| `cp -r site site-backup` | Klasörü içindekilerle kopyalar |

## mv

| Komut | Ne yapar |
|---|---|
| `mv old.txt new.txt` | Yeniden adlandırır |
| `mv a.txt archive/` | Klasörün içine taşır |
| `mv a.txt b.txt archive/` | İkisini de taşır |
| `mv draft final` | Klasörün adını değiştirir (seçenek gerekmez) |

## rm

| Komut | Ne yapar |
|---|---|
| `rm a.txt` | Dosyayı siler |
| `rm a.txt b.txt` | Birden çok dosya |
| `rm -r tmp` | Klasörü içindekilerle siler |
| `rm -f a.txt` | Sormaz, yoksa şikâyet etmez |
| `rm -i a.txt` | Her dosya için sorar (gerçek terminalde) |
| `rmdir boş` | Yalnızca boş klasör |

## Hatalar

| Gördüğün | Anlamı |
|---|---|
| `cp: cannot stat 'x': No such file or directory` | Kaynak yok |
| `cp: -r not specified; omitting directory 'd'` | Klasör için `-r` unutuldu |
| `cp: target 'x' is not a directory` | Birden çok kaynak var, hedef klasör değil |
| `rm: cannot remove 'd': Is a directory` | Klasör için `rm -r` |
| `mv: cannot move 'a' to 'x/a': No such file or directory` | Hedef klasör yok |
