Yarım işi bekletmenin üç yolu var. Hangisinin uygun olduğu ne kadar
bekleyeceğine bağlı.

| Yol | Nasıl | Ne zaman |
|---|---|---|
| **Stash** | `git stash` … `git stash pop` | Dakikalar, birkaç saat. |
| **WIP commit** | `git commit -am "WIP"` … sonra `git reset --soft HEAD~1` ya da `--amend` | Gün sonu, bilgisayar değiştirirken (push edilebilir). |
| **Ayrı dal** | `git switch -c deneme` + commit | Günler; belki hiç birleşmeyecek deneme. |

## WIP commit'i düzeltmek

Gün sonunda yarım işi `WIP` mesajıyla commit'lediysen ertesi gün:

```text
git reset --soft HEAD~1     commit'i geri al, değişiklik hazırlıkta kalsın
... işi bitir ...
git commit -m "Add contact form"
```

Ya da işi bitirince `git commit --amend -m "Add contact form"`. İkisi de
yalnızca commit henüz paylaşılmamışsa (09).

## Aynı anda iki dalda çalışmak

Sık sık iki dal arasında gidip geliyorsan Git'in `worktree` özelliği aynı
deponun ikinci bir dalını **ayrı bir klasörde** açar:

```text
git worktree add ../site-fix fix-typo
```

Artık `../site-fix` klasörü `fix-typo` dalında; asıl klasör kendi dalında
kalıyor, stash'e gerek yok. İleri seviye bir araç; bilmen yeter.
