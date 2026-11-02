Dosya ve klasör adı seçerken uyulacak kurallar. Bunlara uyan adlar terminalde
tırnak, kaçış ya da sürpriz istemez.

## Güvenli adlar

- Küçük harf, rakam, `-`, `_` ve `.` kullan: `monthly-report.txt`,
  `data_2026.csv`.
- **Boşluk kullanma.** Kullanırsan her seferinde tırnak gerekir:
  `cat "my notes.txt"`.
- Türkçe harf (`ş`, `ğ`, `ı`) teknik olarak olur, ama her klavyede yazılamaz
  ve bazı araçlar sorun çıkarır. Dosya adlarında İngilizce harfler daha
  rahat.

## Büyük ve küçük harf

Linux için `Report.txt`, `report.txt` ve `REPORT.TXT` üç ayrı dosyadır.
Windows ve macOS bunları çoğu zaman aynı sayar; bir projeyi iki sistem
arasında taşırken sorun buradan çıkar. En kolayı hep küçük harf kullanmak.

## Uzantılar

| Uzantı | Genelde ne |
|---|---|
| `.txt` | Düz metin |
| `.md` | Markdown metni |
| `.csv` | Virgülle ayrılmış tablo |
| `.sh` | Bash betiği |
| `.py` | Python kodu |
| `.log` | Kayıt dosyası |

Uzantı zorunlu değildir; Linux'ta `notes` adında uzantısız bir metin dosyası
da olur. Uzantı, dosyayı açacak insana ve programa ipucudur.

## Gizli adlar

Nokta ile başlayan ad gizlidir: `.bashrc`, `.gitignore`, `.env`. Gizli
dosyalar genellikle ayar taşır; `ls -a` ile görünür.

## Kaçınılacak karakterler

`* ? [ ] $ & ; | < > ( ) ' " \` ve `!` kabuk için anlam taşır. Bir adda
bunlardan biri varsa komutlar beklemediğin şeyi yapabilir. Bunları adlarda
kullanma.
