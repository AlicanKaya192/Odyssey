Yeni bir bilgisayarda bir kez yapılacak ayarların tamamı. 01'dekilere
(ad, e-posta, dal adı, düzenleyici) bu patikada öğrendiklerin eklendi.

```text
git config --global user.name "Adın Soyadın"
git config --global user.email "github-epostan@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

git config --global pull.rebase true
git config --global fetch.prune true
git config --global push.autoSetupRemote true

git config --global alias.lg "log --oneline --graph --all"
git config --global alias.st "status -s"
git config --global alias.last "log -1 --stat"
```

| Ayar | Kazancı |
|---|---|
| `pull.rebase true` | `pull` ayrışmada soru sormaz, yerel commit'leri üste dizer (12). |
| `fetch.prune true` | GitHub'da silinen dalların izleri kendiliğinden temizlenir (10). |
| `push.autoSetupRemote true` | Yeni dalda ilk push için `-u origin dal` gerekmez. |
| `alias.lg` | `git lg`: bütün dallar tek bakışta. |
| `alias.st` | `git st`: kısa durum. |
| `alias.last` | `git last`: son commit ve dosyaları. |

## Ayarları görmek

```text
git config --global --list
```

Ayarların hepsi `~/.gitconfig` dosyasında durur; yeni bir bilgisayara
geçerken bu dosyayı kopyalamak da olur (kişisel e-posta gibi şeylere dikkat).
