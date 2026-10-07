# Kurtarma: reflog ve Kopuk HEAD

`git reset --hard` ile üç commit'i attın, birleştirilmemiş bir dalı `-D` ile
sildin, ya da bir yerde "detached HEAD" yazdı ve commit'lerin kayboldu...
İyi haber: **commit'lenmiş iş Git'te neredeyse hiç kaybolmaz.** Daldan
düşen commit'ler bir süre deponun içinde durmaya devam eder. Onları bulmanın
yolu **reflog**.

## Kopuk HEAD (*detached HEAD*)

Normalde HEAD bir **dalı** gösterir, dal da bir commit'i. Commit atınca dal
ilerler. Ama bir dala değil doğrudan bir **commit'e** (ya da bir etikete)
geçersen HEAD kopar:

```text
~/app (main) $ git checkout HEAD~1
Note: switching to 'HEAD~1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 1c20e46 Two
~/app (1c20e46...) $ git status
HEAD detached at 1c20e46
nothing to commit, working tree clean
~/app (1c20e46...) $ cat f.txt
1
2
```

Git uzun bir açıklama yazıyor; özeti şu: "Etrafa bakabilirsin, deneme
yapabilirsin; ama burada attığın commit'ler hiçbir dala ait değil." İstem de
dal yerine kısa bir hash ve üç nokta gösteriyor.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Normal</h4><p>HEAD → main → commit</p><p>Commit atınca main ilerler</p><p>İstem: (main)</p></div>
    <div class="no"><h4>Kopuk HEAD</h4><p>HEAD → commit</p><p>Commit atınca hiçbir dal ilerlemez</p><p>İstem: (c1a230e...)</p></div>
  </div>
  <figcaption>Kopuk HEAD'de bakmak güvenli; iş yapacaksan önce git switch -c ile dal aç.</figcaption>
</figure>

Kopuk HEAD **eski bir hâle bakmak** için güvenli ve kullanışlı. Sorun, orada
commit atıp sonra bir dala dönersen çıkar:

```text
~/app (1c20e46...) $ echo "e" > e.txt
~/app (1c20e46...) $ git add .
~/app (1c20e46...) $ git commit -m "Experiment"
[detached HEAD 95e02d2] Experiment
 1 file changed, 1 insertion(+)
 create mode 100644 e.txt
~/app (95e02d2...) $ git switch main
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  95e02d2 Experiment

If you want to keep it by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> 95e02d2

Switched to branch 'main'
~/app (main) $ git branch experiment HEAD@{1}
~/app (main) $ git log --oneline experiment -2
95e02d2 (experiment) Experiment
1c20e46 Two
```

Git uyardı: `Experiment` commit'i hiçbir dala bağlı değil. Uyarının söylediğini
yaparsan (`git branch <ad> <hash>`) commit kurtulur. Daha iyisi: kopuk
HEAD'de iş yapacaksan **önce dal aç**: `git switch -c deneme`.

## reflog: HEAD'in günlüğü

Git, HEAD'in gittiği **her yeri** kaydeder: commit, checkout, reset, merge,
rebase... Bu kayda **reflog** (*reference log*) denir. `git log` dalın
geçmişini gösterir; `git reflog` senin **yaptıklarını**:

```text
~/app (main) $ git reflog
be3b130 (HEAD -> main, test) HEAD@{0}: checkout: moving from test to main
be3b130 (HEAD -> main, test) HEAD@{1}: checkout: moving from main to test
be3b130 (HEAD -> main, test) HEAD@{2}: commit: Three
1c20e46 HEAD@{3}: commit: Two
8ba380a HEAD@{4}: commit (initial): One
```

Her satır: o andaki commit, `HEAD@{n}` (n adım önce HEAD neredeydi) ve ne
olduğu. `HEAD@{0}` şu an, `HEAD@{1}` bir önceki hareket. Bu adlar bir commit
yerine her komutta kullanılabilir.

## Kurtarma 1: `reset --hard` geri alma

Üç commit'i `reset --hard` ile attın:

```text
~/app (main) $ git reset --hard HEAD~2
HEAD is now at 8ba380a One
~/app (main) $ git log --oneline
8ba380a (HEAD -> main) One
~/app (main) $ git reflog -3
8ba380a (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
be3b130 HEAD@{1}: commit: Three
1c20e46 HEAD@{2}: commit: Two
~/app (main) $ git reset --hard HEAD@{1}
HEAD is now at be3b130 Three
~/app (main) $ git log --oneline
be3b130 (HEAD -> main) Three
1c20e46 Two
8ba380a One
```

`git log` artık yalnızca `One`'ı gösteriyor ama reflog her şeyi hatırlıyor:
`HEAD@{1}` reset'ten hemen önceki hâl. `git reset --hard HEAD@{1}` dalı oraya
geri götürdü.

## Kurtarma 2: silinen dal

Birleştirilmemiş `temp` dalını `-D` ile sildin. Dal yalnızca bir etiketti;
commit'leri hâlâ duruyor. Reflog'da dalın son commit'ini bul ve oraya yeni
bir dal aç:

```text
~/app (main) $ git reflog -3
be3b130 (HEAD -> main) HEAD@{0}: checkout: moving from temp to main
f46d820 HEAD@{1}: commit: Temp work
be3b130 (HEAD -> main) HEAD@{2}: checkout: moving from main to temp
~/app (main) $ git branch temp HEAD@{1}
~/app (main) $ git log --oneline temp -2
f46d820 (temp) Temp work
be3b130 (HEAD -> main) Three
```

## Neyi kurtaramazsın?

Reflog yalnızca **commit'lenmiş** hâlleri bilir:

| Durum | Kurtarılır mı? |
|---|---|
| `reset --hard` ile atılan commit'ler | Evet, reflog. |
| `-D` ile silinen dal | Evet, reflog + `git branch`. |
| Kopuk HEAD'de atılıp unutulan commit'ler | Evet, reflog. |
| Yanlış `rebase` ya da `--amend` | Evet: eski hâl reflog'da (`HEAD@{n}`). |
| Commit'lenmemiş değişiklik (`restore`, `reset --hard`, `clean -f`) | ⚠ Hayır. |
| `git stash drop` / `clear` | Çok zor (özel araçlarla). |

Ders: emin olmadığın bir işe girmeden önce **commit'le** (gerekirse sonra
`--amend` ya da `reset --soft` ile düzeltirsin).

> Reflog **yalnızca senin bilgisayarında** durur, GitHub'a gitmez ve kalıcı
> değildir: Git eski kayıtları bir süre sonra (varsayılan 90 gün, daldan
> düşmüşler için 30 gün) temizler. Kurtarmayı geciktirme.

## Panik anında

1. **Dur.** Başka komut yazma; özellikle `reset --hard`, `clean` yazma.
2. `git status`: yarım bir işlem var mı (MERGING, REBASE)? Varsa
   `--abort` çoğu zaman en güvenli çıkış.
3. `git reflog`: kaybettiğini düşündüğün hâli bul (mesajından tanırsın).
4. O commit'e **dal aç** (`git branch kurtar HEAD@{3}`) ya da dalını oraya
   taşı (`git reset --hard HEAD@{3}`).
5. `git log --oneline kurtar` ile doğru yerde olduğuna bak.

## Özet

- Kopuk HEAD: bir dala değil bir commit'e geçtin; bakmak güvenli, iş
  yapacaksan önce `git switch -c`.
- Kopuk HEAD'den ayrılırken Git sahipsiz commit'leri ve kurtarma komutunu
  yazar.
- `git reflog` HEAD'in her hareketini tutar; `HEAD@{n}` n hareket öncesi.
- Atılan commit'ler: `git reset --hard HEAD@{n}`; silinen dal: `git branch
  ad HEAD@{n}`.
- Commit'lenmemiş iş reflog'da yoktur.
