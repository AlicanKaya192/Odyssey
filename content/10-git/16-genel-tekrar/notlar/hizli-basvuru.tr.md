Patikadaki bütün komutlar tek sayfada.

## Başlamak

| Komut | Ne yapar |
|---|---|
| `git init` | Klasörü depo yapar. |
| `git clone <url>` | Uzak depoyu indirir. |
| `git config --global user.name "Ad"` | Kimlik (bir kez). |

## Her gün

| Komut | Ne yapar |
|---|---|
| `git status` / `-s` | Durum. |
| `git add dosya` / `.` | Hazırlık alanına koy. |
| `git commit -m "Mesaj"` | Commit. |
| `git diff` / `--staged` | Fark. |
| `git log --oneline --graph --all` | Geçmiş. |
| `git pull` / `git push` | Al / gönder. |

## Dallar

| Komut | Ne yapar |
|---|---|
| `git switch -c dal` | Aç ve geç. |
| `git switch dal` / `-` | Geç / öncekine dön. |
| `git merge dal` | Bulunduğun dala birleştir. |
| `git branch -d dal` / `-D` | Sil / zorla sil. |
| `git rebase main` | Yeni tabana taşı (yalnızca sende olan dal). |
| `git cherry-pick X` | Tek commit'i kopyala. |

## Geri almak

| Komut | Ne yapar |
|---|---|
| `git restore dosya` | ⚠ Dosyadaki değişikliği at. |
| `git restore --staged dosya` | Hazırlıktan çıkar. |
| `git commit --amend` | Son commit'i düzelt. |
| `git reset --soft / --mixed / --hard HEAD~1` | Commit'i geri al. |
| `git revert X` | Paylaşılmış commit'i geri al. |
| `git stash` / `pop` | Kenara koy / geri getir. |
| `git reflog` | Kaybolanı bul. |

## Uzak depo ve sürüm

| Komut | Ne yapar |
|---|---|
| `git remote add origin <url>` | Uzak depoyu kaydet. |
| `git push -u origin dal` | Dalı ilk kez gönder. |
| `git fetch --prune` | Haber al, silinmiş dalları temizle. |
| `git tag -a v1.0 -m "..."` | Sürüm etiketi. |
| `git push --tags` | Etiketleri gönder. |

## Durum işaretleri

| Görürsen | Anlamı | Çıkış |
|---|---|---|
| <code>(main&#124;MERGING)</code> | Birleştirme yarım | çöz + commit ya da `git merge --abort` |
| <code>(main&#124;REBASE)</code> | Rebase yarım | çöz + `git rebase --continue` ya da `--abort` |
| `(1a2b3c4...)` | Kopuk HEAD | `git switch -c yeni` ya da `git switch -` |
