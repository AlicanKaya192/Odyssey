## Bağlantı

| Komut | Ne yapar |
|---|---|
| `git clone <adres>` | Depoyu geçmişiyle indirir, `origin`'i ayarlar. |
| `git clone <adres> klasor` | Başka bir klasör adıyla indirir. |
| `git remote -v` | Kayıtlı uzak depolar ve adresleri. |
| `git remote add origin <adres>` | Uzak depoyu kaydeder. |
| `git remote set-url origin <yeni>` | Adresi değiştirir. |
| `git remote remove origin` | Kaydı siler (GitHub'daki depoya dokunmaz). |

## Göndermek

| Komut | Ne yapar |
|---|---|
| `git push -u origin main` | İlk gönderim; izlemeyi ayarlar. |
| `git push` | İzlenen dala gönderir. |
| `git push -u origin dal` | Yeni bir dalı ilk kez gönderir. |
| `git push origin --delete dal` | GitHub'daki dalı siler. |
| `git push --tags` | Etiketleri gönderir (13). |
| ⚠ `git push --force-with-lease` | Yeniden yazılmış geçmişi gönderir; başkası göndermişse reddeder. |

## Almak

| Komut | Ne yapar |
|---|---|
| `git fetch` | Yenilikleri indirir, `origin/...` dallarını günceller; senin dalına dokunmaz. |
| `git pull` | fetch + merge. |
| `git pull --no-rebase` | Ayrışmış dallarda birleştirmeyle al. |
| `git pull --rebase` | Ayrışmış dallarda yeniden dizerek al (12). |
| `git config --global pull.rebase false` | `pull`'un hep birleştirmesini seç (bir kez). |

## Durumu görmek

| Komut | Ne gösterir |
|---|---|
| `git status` | `ahead` / `behind` / `diverged` (son fetch'e göre). |
| `git branch -vv` | Her dalın izlediği uzak dal ve ileri / geri sayısı. |
| `git branch -a` | Uzak izleme dallarıyla birlikte bütün dallar. |
| `git log --oneline --all --graph` | Senin ve uzak dalların geçmişi birlikte. |

## Sık mesajlar

| Mesaj | Anlamı | Ne yapmalı |
|---|---|---|
| `Your branch is ahead of 'origin/main' by N commits` | Göndermediğin commit var. | `git push` |
| `Your branch is behind 'origin/main' by N commits` | Almadığın commit var. | `git pull` |
| `have diverged` | İki taraf da ilerlemiş. | `git pull --no-rebase`, sonra `git push` |
| `! [rejected] ... (fetch first)` | GitHub'da senin bilmediğin commit var. | `git pull`, sonra `git push` |
| `has no upstream branch` | Dal ilk kez gönderiliyor. | `git push -u origin dal` |
| `Repository not found` | Adres yanlış ya da depo yok / erişimin yok. | Adresi ve GitHub'ı kontrol et. |
