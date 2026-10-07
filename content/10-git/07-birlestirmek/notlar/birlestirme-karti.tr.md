## Komutlar

| Komut | Ne yapar |
|---|---|
| `git merge dal` | `dal`'ı bulunduğun dala birleştirir. |
| `git merge dal --no-edit` | Hazır mesajla, düzenleyici açmadan. |
| `git merge dal -m "mesaj"` | Kendi mesajınla. |
| `git merge --no-ff dal` | İleri sarma mümkün olsa da birleştirme commit'i. |
| `git merge --abort` | Yarım kalan (çakışmalı) birleştirmeyi iptal eder (08). |
| `git branch --merged` | Birleştirilmiş, silmesi güvenli dallar. |
| `git log --oneline --graph` | Birleştirmeyi çizgiyle görmek. |

## Yön

Komut **bulunduğun dalı** değiştirir:

| Ne istiyorsun? | Önce | Sonra |
|---|---|---|
| Dalımdaki işi main'e almak | `git switch main` | `git merge dalim` |
| main'deki yenilikleri dalıma almak | `git switch dalim` | `git merge main` |

## İki biçim

| | İleri sarma | Üç yönlü |
|---|---|---|
| Ne zaman | Hedef dal ayrıldıktan sonra ilerlememiş | İki dal da ilerlemiş |
| Yeni commit | Yok; etiket kayar | Birleştirme commit'i (iki ebeveyn) |
| Çıktıda | `Fast-forward` | `Merge made by the 'ort' strategy.` |
| Grafik | Düz çizgi | <code>&#124;\</code> ve <code>&#124;/</code> ile çatal |
| Çakışma olabilir mi? | Hayır | Evet, aynı satır iki dalda değiştiyse |

`ort`, Git'in bugünkü birleştirme yönteminin adı (*Ostensibly Recursive's
Twin*). Eski çıktılarda `recursive` görürsün; aynı iş.

## Sık mesajlar

| Mesaj | Anlamı |
|---|---|
| `Already up to date.` | Dalın her şeyi zaten burada. |
| `merge: x - not something we can merge` | Böyle bir dal ya da commit yok; adı kontrol et. |
| `CONFLICT (content): Merge conflict in a.txt` | Çakışma; 08. bölüm. |
| `error: Your local changes ... would be overwritten by merge` | Commit'lenmemiş değişiklik birleştirmeye engel; önce commit ya da stash. |
