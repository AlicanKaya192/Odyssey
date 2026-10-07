İlk commit'lerde en sık görülen mesajlar, sebepleri ve çözümleri.

| Mesaj | Sebep | Çözüm |
|---|---|---|
| `fatal: not a git repository` | Depo olmayan bir klasördesin. | `pwd` ile yerine bak; doğru klasöre `cd` ile gir ya da `git init`. |
| `nothing to commit, working tree clean` | Commit'lenecek değişiklik yok. | Önce bir dosyayı değiştir. |
| `nothing added to commit but untracked files present` | Yeni dosyalar var ama hiçbiri eklenmedi. | `git add <dosya>` sonra commit. |
| `no changes added to commit` | Değişiklikler hazırlık alanında değil. | `git add` ya da `git commit -am`. |
| `fatal: pathspec 'x' did not match any files` | `git add`'e verdiğin ad yok. | `ls` ile adı kontrol et (büyük-küçük harf, uzantı). |
| `Author identity unknown` | Ad ve e-posta ayarsız. | Bölüm 01: `git config --global user.name …` |
| `error: pathspec 'Home' did not match any file(s) known to git` | `-m "Add Home"` yerine `-m Add Home` yazdın; Git `Home`'u dosya adı sandı. | Mesajı tırnakla yaz. |

## Adım adım ilk commit

```text
git init                          bir kez, depo yoksa
git status                        ne var?
git add index.html                commit'e girecekleri seç
git status                        doğru mu?
git commit -m "Add home page"     fotoğrafı çek
git log --oneline                 geçmişte gör
```

## Yazmadan önce sor

- **Bu commit tek bir iş mi anlatıyor?** İki ayrı iş varsa iki commit.
- **Hazırlık alanında olmaması gereken bir şey var mı?** Şifre, büyük veri,
  geçici dosya.
- **Mesaj bir yabancıya ne olduğunu söylüyor mu?** `Fix bug` değil,
  `Fix crash when the list is empty`.
