Dallarla ilgili bütün komutlar tek yerde.

## Görmek

| Komut | Ne gösterir |
|---|---|
| `git branch` | Yerel dallar; `*` bulunduğun. |
| `git branch -v` | Her dalın son commit'iyle. |
| `git branch -a` | Uzak depo dallarıyla birlikte (09). |
| `git branch --merged` | Bulunduğun dala birleştirilmiş olanlar. |
| `git branch --no-merged` | Henüz birleştirilmemiş olanlar. |
| `git log --oneline --graph --all` | Bütün dalların geçmişi, çizgilerle. |

## Açmak ve geçmek

| Komut | Ne yapar |
|---|---|
| `git branch ad` | Bulunduğun commit'te dal açar, geçmez. |
| `git branch ad <commit>` | Belirli bir commit'te dal açar. |
| `git switch ad` | Dala geçer. |
| `git switch -c ad` | Açar ve geçer. |
| `git switch -c ad <commit>` | Belirli bir commit'ten açar ve geçer. |
| `git switch -` | Bir önceki dala döner. |
| `git checkout ad` / `git checkout -b ad` | Eski yazımlar. |

## Düzenlemek

| Komut | Ne yapar |
|---|---|
| `git branch -m yeni` | Bulunduğun dalın adını değiştirir. |
| `git branch -m eski yeni` | Başka bir dalın adını değiştirir. |
| `git branch -d ad` | Birleştirilmişse siler. |
| `git branch -D ad` | ⚠ Zorla siler. |

## Sık hatalar

| Mesaj | Anlamı | Çözüm |
|---|---|---|
| `fatal: invalid reference: x` | Böyle bir dal yok. | `git branch` ile adına bak; açmak için `-c`. |
| `fatal: a branch named 'x' already exists` | Aynı adla dal var. | Başka ad ya da `git switch x`. |
| `Your local changes ... would be overwritten` | Commit'lenmemiş değişiklik gideceğin dalda farklı. | Önce commit ya da `git stash`. |
| `the branch 'x' is not fully merged` | Dalda başka yerde olmayan commit'ler var. | Önce birleştir; gerçekten istiyorsan `-D`. |
| `cannot delete branch 'x' used by worktree` | Bulunduğun dalı siliyorsun. | Başka dala geç. |
| `cannot lock ref ... exists` | `feature` varken `feature/x` açmaya çalıştın. | Farklı bir ad seç. |
