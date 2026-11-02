Bu bölümün komutları, bir bakışta.

| Komut | Ne yapar |
|---|---|
| `mkdir notes` | `notes` klasörünü açar. |
| `mkdir a b c` | Üç klasör birden. |
| `mkdir -p site/css/img` | Eksik üst klasörlerle birlikte; varsa sessiz. |
| `touch todo.txt` | Boş dosya; varsa yalnızca zamanını günceller. |
| `touch a.txt b.txt` | Birden çok boş dosya. |
| `echo "metin" > f.txt` | Dosyayı **baştan** yazar (eski içerik gider). |
| `echo "metin" >> f.txt` | Dosyanın **sonuna** ekler. |
| `cat f.txt` | Dosyanın içini yazar. |
| `cat a.txt b.txt` | İki dosyayı art arda. |
| `cat -n f.txt` | Satır numaralarıyla. |
| `rmdir boş` | Yalnızca **boş** klasörü siler. |
| `touch .secret` | Gizli dosya (adı nokta ile başlar). |

## Birkaç satırlık dosya yazmak

```bash
echo "eggs" > shopping.txt
echo "bread" >> shopping.txt
echo "tea" >> shopping.txt
cat shopping.txt
```

İlk satır `>`, sonrakiler `>>`. Bir yanlış yaparsan ilk satırı yeniden `>` ile
yazmak dosyayı sıfırlar.

## Sık hatalar

| Gördüğün | Sebebi | Ne yaparsın |
|---|---|---|
| `mkdir: cannot create directory 'a/b': No such file or directory` | `a` yok | `mkdir -p a/b` |
| `mkdir: cannot create directory 'a': File exists` | Zaten var | Bir şey yapma ya da `-p` |
| `rmdir: failed to remove 'x': Directory not empty` | Klasör boş değil | İçini boşalt (sonraki bölüm: `rm -r`) |
| `bash: notes/x.txt: No such file or directory` | `>` klasör açmaz | Önce `mkdir notes` |
| Dosyanın eski satırları kayboldu | `>>` yerine `>` | Bundan sonra `>>` |
