Bu bölümün komutları, bir bakışta.

| Komut | Ne yapar |
|---|---|
| `cat dosya` | Bütün dosya |
| `cat -n dosya` | Satır numaralarıyla |
| `head dosya` | İlk 10 satır |
| `head -n 5 dosya` / `head -5 dosya` | İlk 5 satır |
| `tail dosya` | Son 10 satır |
| `tail -n 5 dosya` / `tail -5 dosya` | Son 5 satır |
| `tail -n +5 dosya` | 5. satırdan sona |
| `tail -f dosya` | Sonu izler, yeni satırları yazar (gerçek terminalde) |
| `wc dosya` | Satır, kelime, bayt |
| `wc -l dosya` | Satır sayısı |
| `wc -w dosya` | Kelime sayısı |
| `wc -c dosya` | Bayt sayısı |

## Hangisini ne zaman?

| Soru | Komut |
|---|---|
| Dosya neyle başlıyor? (başlık satırı, sütunlar) | `head -n 3` |
| Az önce ne oldu? (kayıt dosyası) | `tail` |
| Kaç kayıt / kaç satır? | `wc -l` |
| 40. satırda ne var? | `cat -n` ya da `head -n 40` ve son satırına bak |
| Uzun bir belgeyi rahat okumak | `less` (gerçek terminalde) |

## Sık hatalar

| Gördüğün | Sebebi |
|---|---|
| `head: invalid number of lines: 'ten'` | Sayı rakamla yazılır |
| `tail: cannot open 'x' for reading: No such file or directory` | Dosya yok ya da yanlış yerdesin |
| `wc: logs: Is a directory` | Klasörün kendisi sayılmaz; içindeki bir dosyayı ver |
