## Ne kayboldu, nasıl gelir?

| Ne oldu? | Kurtarma |
|---|---|
| `git reset --hard HEAD~n` ile commit'ler gitti | `git reflog` → `git reset --hard HEAD@{1}` |
| `git branch -D dal` ile dal silindi | `git reflog` → dalın son commit'i → `git branch dal <hash>` |
| Kopuk HEAD'de commit atıp dala döndüm | Uyarıdaki hash ile `git branch kurtar <hash>` ya da `git reflog` |
| `--amend` ile son commit'i bozdum | `git reset --hard HEAD@{1}` (amend öncesi) |
| Rebase her şeyi karıştırdı (bitti) | `git reflog` → `rebase (start)`'tan önceki satır → `git reset --hard HEAD@{n}` |
| Rebase sürüyor, karıştı | `git rebase --abort` |
| Birleştirme sürüyor, karıştı | `git merge --abort` |
| Dosyadaki commit'lenmemiş değişikliği attım | ⚠ Kurtarılamaz |

## Reflog satırını okumak

```text
63074be HEAD@{3}: reset: moving to HEAD~2
```

`63074be` o anki commit, `HEAD@{3}` üç hareket önce, `reset: moving to
HEAD~2` ne yapıldığı. Aradığın hâli **hareketten önceki** satırda bulursun:
reset'ten önceki durum, reset satırının bir altındadır.

## Komutlar

| Komut | Ne yapar |
|---|---|
| `git reflog` | HEAD'in bütün hareketleri. |
| `git reflog -10` | Son 10 hareket. |
| `git log --oneline HEAD@{2}` | O andaki geçmiş. |
| `git show HEAD@{2}` | O andaki commit. |
| `git branch kurtar HEAD@{2}` | O ana dal aç (en güvenlisi). |
| `git reset --hard HEAD@{2}` | Dalını oraya taşı (commit'lenmemiş işi siler). |
| `git switch -c ad` | Kopuk HEAD'deyken buradan dal aç. |
| `git switch -` | Kopuk HEAD'den önceki dala dön. |

## Altın kural

Kurtarırken önce **dal aç**, sonra bak. Dal açmak hiçbir şeyi silmez;
yanlış yerdeyse dalı silersin, başka hiçbir şey değişmez.
