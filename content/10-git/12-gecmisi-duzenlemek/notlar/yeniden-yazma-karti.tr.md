Geçmişi yeniden yazan komutlar ve güvenli kullanım.

| Komut | Ne yapar | Paylaşılmışta? |
|---|---|---|
| `git commit --amend` | Son commit'i yenisiyle değiştirir. | ⚠ Hayır |
| `git reset HEAD~n` | Son n commit'i daldan çıkarır. | ⚠ Hayır |
| `git rebase main` | Dalın commit'lerini main'in ucuna dizer. | ⚠ Hayır |
| `git rebase -i HEAD~n` | Son n commit'i düzenler (squash, reword, drop). | ⚠ Hayır |
| `git pull --rebase` | Yerel commit'leri gelenlerin üstüne dizer. | Evet (yalnızca senin gönderilmemiş commit'lerin değişir) |
| `git cherry-pick X` | X'in kopyasını bulunduğun dala ekler. | Evet (yeni commit ekler) |
| `git revert X` | X'in tersini yapan commit ekler. | Evet |

## Rebase sırasında

| Durum | Komut |
|---|---|
| Çakışmayı çözdüm | `git add dosya` → `git rebase --continue` |
| Bu commit'i atla | `git rebase --skip` |
| Vazgeçtim | `git rebase --abort` |
| Neredeyim? | `git status` (yapılan ve kalan commit'leri listeler) |

## Cherry-pick sırasında

| Durum | Komut |
|---|---|
| Çakışmayı çözdüm | `git add dosya` → `git cherry-pick --continue` |
| Vazgeçtim | `git cherry-pick --abort` |
| Birden çok commit | `git cherry-pick A B C` ya da aralık `A^..C` |

## Zorla göndermek gerekirse

Kendi dalını (yalnızca senin çalıştığın) rebase ettikten sonra GitHub'daki
eski hâlinin üstüne yazmak için:

```text
git push --force-with-lease
```

`--force` değil `--force-with-lease`: son `fetch`'ten bu yana başkası o dala
bir şey gönderdiyse reddeder, işini ezmezsin.
