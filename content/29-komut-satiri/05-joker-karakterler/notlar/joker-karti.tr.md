Kalıplar ve eşleştikleri, bir bakışta.

| Kalıp | Eşleşir | Eşleşmez |
|---|---|---|
| `*.txt` | `a.txt`, `notes.txt` | `a.txt.bak`, `.hidden.txt` |
| `photo*` | `photo1.jpg`, `photo` | `my-photo.jpg` |
| `*report*` | `report.txt`, `old-report.md` | `rep.txt` |
| `photo?.jpg` | `photo1.jpg`, `photoA.jpg` | `photo10.jpg` |
| `photo??.jpg` | `photo10.jpg` | `photo1.jpg` |
| `[ab]*` | `a.txt`, `b.csv` | `c.txt` |
| `log[0-9].txt` | `log1.txt` | `log10.txt` |
| `.h*` | `.hidden.txt` | `hidden.txt` |
| `*/` | Bütün (gizli olmayan) klasörler | Dosyalar |
| `logs/*.log` | `logs` içindeki `.log` dosyaları | Alt klasörlerdekiler |

## Süslü parantez (her zaman açılır)

| Yazdığın | Kabuğun ürettiği |
|---|---|
| `file{1,2,3}.txt` | `file1.txt file2.txt file3.txt` |
| `{a..d}` | `a b c d` |
| `site/{css,js}` | `site/css site/js` |
| `report.{txt,bak}` | `report.txt report.bak` |

## Kapatmak

| Yazdığın | Sonuç |
|---|---|
| `"*.txt"` | Düz `*.txt` |
| `'*.txt'` | Düz `*.txt` |
| `\*.txt` | Düz `*.txt` |

## Hatırla

- Jokeri kabuk açar; eşleşme yoksa kalıp olduğu gibi kalır.
- Sonucu önceden gör: `echo kalıp`.
