İnternette bulacağın çözümlerin çoğu Git 2.23'ten (2019) önce yazıldı ve
`restore` / `switch` yerine eski komutları kullanır. Hepsi hâlâ çalışır;
karşılıklarını bilmek yeter.

| Eski yazım | Yeni yazım | Ne yapar |
|---|---|---|
| `git checkout -- dosya` | `git restore dosya` | Dosyadaki değişikliği at. |
| `git reset HEAD dosya` | `git restore --staged dosya` | Hazırlık alanından çıkar. |
| `git checkout HEAD~2 -- dosya` | `git restore --source=HEAD~2 dosya` | Dosyanın eski hâlini getir. |
| `git checkout dal` | `git switch dal` | Dala geç (06). |
| `git checkout -b yeni` | `git switch -c yeni` | Yeni dal açıp geç (06). |

## Neden ikiye ayrıldı?

`git checkout` çok farklı iki iş yapıyordu: dal değiştirmek ve dosyaları geri
yüklemek. Bir karakterlik fark (`--`) hangisinin yapılacağını belirliyordu
ve yanlış yazan biri değişikliğini kaybedebiliyordu. `switch` yalnızca dal
değiştirir, `restore` yalnızca dosyalara dokunur.

## `reset` ile dosya

`git reset dosya` (commit vermeden, dosya adıyla) da hazırlık alanından
çıkarır, `git restore --staged dosya` ile aynı. `--hard` dosya adıyla
kullanılamaz:

```text
fatal: Cannot do hard reset with paths.
```
