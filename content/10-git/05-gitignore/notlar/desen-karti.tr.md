`.gitignore` desenleri ve neye uydukları. Emin değilsen
`git check-ignore -v <dosya>` ile sor.

| Desen | Uyar | Uymaz |
|---|---|---|
| `*.log` | `a.log`, `logs/b.log` | `a.log.txt` |
| `debug.log` | `debug.log`, `src/debug.log` | `debug.logs` |
| `/debug.log` | `debug.log` (yalnızca kökte) | `src/debug.log` |
| `build/` | `build/` klasörü ve içi, `src/build/` | `build` adlı **dosya** |
| `build` | `build` dosyası **ve** klasörü | — |
| `docs/*.pdf` | `docs/a.pdf` | `docs/x/a.pdf`, `a.pdf` |
| `**/cache/` | `cache/`, `src/cache/`, `a/b/cache/` | `cache` adlı dosya |
| `data/raw/` | `data/raw/` ve içi | `raw/`, `src/data/raw/` |
| `!keep.log` | — (istisna: `keep.log` görmezden gelinmez) | — |
| `*.csv` + `!sample.csv` | `big.csv` | `sample.csv` (istisna) |

## Kurallar

1. Boş satırlar ve `#` ile başlayanlar okunmaz.
2. Desende `/` yoksa her klasördeki dosya adına bakılır.
3. Başta ya da ortada `/` varsa yol `.gitignore`'un durduğu yere göre okunur.
4. Sonda `/` varsa yalnızca klasörler.
5. Son eşleşen kural kazanır; `!` istisnası genel kuralın altına yazılır.
6. Klasörün tamamı görmezden gelinirse içinden `!` ile dosya kurtarılamaz.
7. Yalnızca izlenmeyen dosyalar etkilenir; izlenen dosya için `git rm --cached`.

## Bir şey ters gidince

| Belirti | Sebep | Çözüm |
|---|---|---|
| Dosya `.gitignore`'da ama `git status`'ta değişmiş görünüyor | Zaten izleniyor. | `git rm --cached dosya` + commit |
| `!` istisnası çalışmıyor | Klasörün tamamı yok sayılmış ya da istisna kuralın **üstünde**. | `klasör/*` yaz; sırayı düzelt. |
| Hiçbir kural çalışmıyor | Dosyanın adı `.gitignore.txt` olmuş (Windows uzantıyı gizliyor). | `ls -a` ile adına bak. |
| Klasörü görmezden gelmek istedim, dosya da gitti | Sonda `/` yoktu. | `build/` yaz. |
