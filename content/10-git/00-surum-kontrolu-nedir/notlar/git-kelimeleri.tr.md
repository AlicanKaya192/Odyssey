Bu patikada sürekli geçecek kelimeler. Şimdi hepsini ezberlemen gerekmiyor;
her biri kendi bölümünde ayrıntılı anlatılıyor. Bir kelimeye takıldığında
buraya dön.

| Kelime | Anlamı | Bölüm |
|---|---|---|
| **depo** (repository, repo) | Git'in izlediği klasör; geçmiş `.git` içinde. | 00 |
| **commit** | Projenin bir anının fotoğrafı: değişiklik + yazar + tarih + mesaj. | 02 |
| **commit mesajı** | Commit'in neden atıldığını anlatan kısa cümle. | 02 |
| **çalışma alanı** (working tree) | Klasördeki dosyaların şu anki hâli. | 02 |
| **hazırlık alanı** (staging area, index) | Bir sonraki commit'e girecek değişikliklerin toplandığı yer. | 02 |
| **hash** | Her commit'in eşsiz kimliği: `6fb3238` gibi bir harf-rakam dizisi. | 03 |
| **diff** | İki hâl arasındaki satır satır fark. | 03 |
| **dal** (branch) | Geçmişin ayrı bir kolu; üzerinde denersin, sonra birleştirirsin. | 06 |
| **main** | Çoğu deponun ana dalının adı (eskiden `master`). | 06 |
| **HEAD** | "Şu an neredeyim" işareti; çoğu zaman bulunduğun dalın son commit'i. | 06 |
| **merge** | İki dalın değişikliklerini birleştirmek. | 07 |
| **çakışma** (conflict) | İki dal aynı satırı farklı değiştirmiş; seçimi sen yaparsın. | 08 |
| **uzak depo** (remote) | Deponun başka yerdeki kopyası, genellikle GitHub'da. | 09 |
| **origin** | Klonladığın uzak deponun varsayılan adı. | 09 |
| **clone** | Uzak depoyu geçmişiyle birlikte bilgisayarına indirmek. | 09 |
| **push / pull** | Commit'leri uzak depoya göndermek / oradan almak. | 09 |
| **pull request** (PR) | GitHub'da "dalımı birleştirir misiniz" isteği. | 10 |
| **fork** | Başkasının deposunun GitHub'daki kendi kopyan. | 10 |
| **stash** | Yarım işi commit'lemeden kenara koymak. | 11 |
| **rebase** | Commit'leri başka bir commit'in üstüne yeniden dizmek. | 12 |
| **etiket** (tag) | Bir commit'e verilen kalıcı ad, ör. `v1.0`. | 13 |
| **reflog** | HEAD'in gittiği her yerin kaydı; kaybolanı bulmanın yolu. | 14 |

## Komutların genel biçimi

Git komutlarının hepsi aynı kalıpla yazılır:

```text
git <alt komut> [seçenekler] [hedefler]
git commit -m "Add readme"
git log --oneline -n 3
```

- `git`'ten sonraki ilk kelime ne yapılacağını söyler (`commit`, `log`).
- `-m`, `-n` gibi tek tireli kısa seçenekler; `--oneline` gibi çift tireli
  uzun seçenekler vardır.
- Ne yazacağını unuttuysan `git <alt komut> -h` kısa bir yardım gösterir
  (gerçek terminalde).
