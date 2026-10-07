## Komutlar

| Komut | Ne yapar |
|---|---|
| `git stash` | İzlenen dosyalardaki değişiklikleri kaldırır. |
| `git stash -u` | İzlenmeyen dosyaları da kaldırır. |
| `git stash push -m "mesaj"` | Mesajla kaldırır. |
| `git stash list` | Kayıtlar (`stash@{0}` en yeni). |
| `git stash show` / `show -p` | Dosya özeti / farkın tamamı. |
| `git stash pop` | En yeniyi uygular ve siler. |
| `git stash apply stash@{n}` | Uygular, silmez. |
| `git stash drop stash@{n}` | Uygulamadan siler. |
| ⚠ `git stash clear` | Hepsini siler. |

## Kalıplar

**Acil iş:**

```text
git stash
git switch main
git switch -c fix-typo
... düzelt, commit ...
git switch -
git stash pop
```

**Yanlış dalda başladım:**

```text
git stash
git switch dogru-dal
git stash pop
```

**Pull engellendi** ("Your local changes ... would be overwritten"):

```text
git stash
git pull
git stash pop
```

## Dikkat

- `git stash` boş çalışma alanında `No local changes to save` der; bir şey
  kaldırmaz.
- `pop` çakışmada kaydı silmez; çözdükten sonra `git stash drop`.
- `clear` ve `drop` ile silinen stash'ler geri gelmez (çok zor kurtarılır).
- Stash'te iş unutma: `git stash list` boş değilse içinde ne olduğuna bak.
