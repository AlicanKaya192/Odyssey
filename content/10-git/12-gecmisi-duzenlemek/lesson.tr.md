# Geçmişi Düzenlemek

07'de dalları birleştirmeyi gördük: iki dalın işi bir birleştirme commit'iyle
bir araya geliyordu. Git'in ikinci bir yolu daha var: **rebase** (yeniden
temellendirmek). Bu bölümde rebase'i, bir commit'i başka bir dala kopyalayan
**cherry-pick**'i ve commit'leri düzenleyen **etkileşimli rebase**'i
göreceğiz.

Hepsinin ortak noktası: **yeni commit'ler oluşturup eskilerinin yerine
koyarlar**. Hash'ler değişir. Bu yüzden bölümün en önemli cümlesi en sonda:
paylaşılmış geçmişi yeniden yazma.

## Rebase: dalını yeni bir tabana taşımak

`feature` dalını açtıktan sonra `main` ilerledi. Birleştirme (07) iki çizgiyi
bir birleştirme commit'iyle bağlardı. Rebase ise `feature`'ın commit'lerini
alıp `main`'in **ucuna yeniden dizer**: sanki dalı bugün açmışsın gibi.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Önce</span><span>Base → Add m (main) · Base → Add x → Add y (feature): iki dal ayrışmış.</span></div>
    <div class="anat-row"><span>git rebase main</span><span>feature'ın commit'leri tek tek main'in ucuna yeniden uygulanır.</span></div>
    <div class="anat-row"><span>Sonra</span><span>Base → Add m → Add x' → Add y' (feature): düz çizgi; x' ve y' yeni commit'ler.</span></div>
  </div>
  <figcaption>Rebase dalın başladığı yeri (tabanını) değiştirir. İçerik aynı, commit'ler yeni.</figcaption>
</figure>

```text
~/app (main) $ git log --oneline --graph --all
* 151c3bc (HEAD -> main) Add m
| * bf2c324 (feature) Add y
| * 3326390 Add x
|/  
* e3511dd Base
~/app (main) $ git switch feature
Switched to branch 'feature'
~/app (feature) $ git rebase main
Successfully rebased and updated refs/heads/feature.
~/app (feature) $ git log --oneline --graph --all
* 501f79f (HEAD -> feature) Add y
* 79c4ca6 Add x
* 151c3bc (main) Add m
* e3511dd Base
```

Önce iki dal ayrışmıştı; rebase'ten sonra `feature`, `main`'in üstünde düz
bir çizgi. `Add x` ve `Add y` yeni hash'ler aldı (içerikleri aynı ama
ebeveynleri değişti, 03'teki hash notunu hatırla).

Artık `main`'e birleştirmek ileri sarma olur; geçmiş tek, düz bir çizgi
kalır:

```text
~/app (feature) $ git switch main
Switched to branch 'main'
~/app (main) $ git merge feature
Updating 151c3bc..501f79f
Fast-forward
 x.txt | 1 +
 y.txt | 1 +
 2 files changed, 2 insertions(+)
 create mode 100644 x.txt
 create mode 100644 y.txt
~/app (main) $ git log --oneline --graph
* 501f79f (HEAD -> main, feature) Add y
* 79c4ca6 Add x
* 151c3bc Add m
* e3511dd Base
```

## Birleştirme mi, rebase mi?

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Birleştirme (merge)</h4><p>Geçmiş olduğu gibi kalır</p><p>Bir birleştirme commit'i eklenir</p><p>Grafikte çatal ve birleşme</p><p><b>Paylaşılmış dallarda güvenli</b></p></div>
    <div class="dim"><h4>Rebase</h4><p>Commit'ler yeniden yazılır</p><p>Birleştirme commit'i yok</p><p>Grafikte düz çizgi</p><p><b>Yalnızca sende olan commit'ler için</b></p></div>
  </div>
  <figcaption>İkisi de iki dalın işini bir araya getirir; fark geçmişin şeklinde.</figcaption>
</figure>

İkisi de aynı dosyaları üretir; fark geçmişin **şeklinde**. Birçok ekip şunu
yapar: kendi dalını güncel tutmak için rebase (`git pull --rebase` gibi),
dalı `main`'e almak için PR ile birleştirme.

## Rebase'te çakışma

Rebase commit'leri tek tek uygular; biri çakışırsa durur:

```text
~/app (feature) $ git rebase main
Auto-merging f.txt
CONFLICT (content): Merge conflict in f.txt
error: could not apply d6fe9d2... Double a
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
Could not apply d6fe9d2... # Double a
~/app (feature|REBASE) $ git status
interactive rebase in progress; onto 6b9e1d8
Last command done (1 command done):
   pick d6fe9d2 # Double a
No commands remaining.
You are currently rebasing branch 'feature' on '6b9e1d8'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
        both modified:   f.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

İstem `(feature|REBASE)` oldu; HEAD kopuk (*detached*) çünkü Git commit'leri
dizerken hiçbir dalda değil. Çözüm birleştirmeye benzer, ama bitirmek için
commit yerine `--continue`:

1. Dosyayı düzelt, işaretleri sil.
2. `git add dosya`
3. `git rebase --continue` (sıradaki commit'lere devam eder)

```text
~/app (feature|REBASE) $ cat f.txt
<<<<<<< HEAD
A
=======
aa
>>>>>>> d6fe9d2 (Double a)
~/app (feature|REBASE) $ echo "AA" > f.txt
~/app (feature|REBASE) $ git add f.txt
~/app (feature|REBASE) $ git rebase --continue
[detached HEAD 3c1e0ed] Double a
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/feature.
~/app (feature) $ git log --oneline --graph
* 3c1e0ed (HEAD -> feature) Double a
* 6b9e1d8 (main) Upper a
* e3511dd Base
```

| Komut | Ne yapar |
|---|---|
| `git rebase --continue` | Çözülen commit'i uygulayıp devam eder. |
| `git rebase --skip` | Bu commit'i atlayıp devam eder (değişikliği kaybolur). |
| `git rebase --abort` | Her şeyi rebase'ten önceki hâline döndürür. |

> Rebase'te `ours` / `theirs` **yer değiştirir**: `ours` dizilmekte olan taban
> (`main`), `theirs` uygulanan senin commit'in. Karışıklık buradan çıkar; elle
> düzenlemek daha güvenli.

## `git pull --rebase`

09'da ayrışan dallarda `git pull --no-rebase` birleştirme commit'i
oluşturuyordu. `--rebase` ise senin yerel commit'lerini GitHub'dan gelenlerin
**üstüne** dizer; birleştirme commit'i olmaz:

```text
~/app (main) $ git pull --rebase
From https://github.com/ada/app
   e3511dd..bb21734  main       -> origin/main
Successfully rebased and updated refs/heads/main.
~/app (main) $ git log --oneline --graph
* ec2ffa2 (HEAD -> main) Add x
* bb21734 (origin/main, origin/HEAD) Add g
* e3511dd Base
~/app (main) $ git push
To https://github.com/ada/app.git
   bb21734..ec2ffa2  main -> main
```

Her seferinde yazmamak için: `git config --global pull.rebase true`.

## Cherry-pick: tek bir commit'i almak

Bazen bir dalın tamamı değil, yalnızca **bir commit'i** gerekir: başka dalda
düzeltilmiş bir hata, `main`'e de lazım. `git cherry-pick <commit>` o
commit'in değişikliğini bulunduğun dala **yeni bir commit** olarak uygular.

```text
~/app (main) $ git log --oneline experiment
d9f2c85 (experiment) Try flex layout
57015e0 Fix footer typo
5a6c6f0 Try grid layout
c9193f2 (HEAD -> main) Add footer
e3511dd Base
~/app (main) $ git cherry-pick experiment~1
[main 79b28fa] Fix footer typo
 Date: Wed Oct 7 10:03:00 2026 +0300
 1 file changed, 1 insertion(+), 1 deletion(-)
~/app (main) $ git log --oneline -3
79b28fa (HEAD -> main) Fix footer typo
c9193f2 Add footer
e3511dd Base
~/app (main) $ cat footer.html
<footer>Copyright</footer>
~/app (main) $ ls
f.txt  footer.html
```

Mesaj ve değişiklik aynı, hash farklı (ebeveyni farklı). Çakışma olursa
çözüm aynı: düzelt, `git add`, `git cherry-pick --continue` (ya da
`--abort`).

## Etkileşimli rebase: commit'leri düzenlemek

`git rebase -i HEAD~3` son üç commit'i bir düzenleyicide liste olarak açar.
Her satırın başındaki kelimeyi değiştirerek ne yapılacağını söylersin:

```text
pick 1a2b3c4 Add search box
squash 5d6e7f8 wip
reword 9a8b7c6 Fix serch
```

| Kelime | Ne yapar |
|---|---|
| `pick` | Commit'i olduğu gibi bırak. |
| `reword` | Mesajını değiştir. |
| `squash` | Bir öncekiyle birleştir (mesajları da). |
| `fixup` | Bir öncekiyle birleştir, kendi mesajını at. |
| `drop` | Commit'i sil. |
| satırların sırası | Commit'lerin sırasını değiştirir. |

Kaydedip kapatınca Git listeyi uygular. Bu, PR açmadan önce `wip`, `fix`,
`typo` commit'lerini temizlemenin en yaygın yolu.

> Odyssey'nin terminalinde düzenleyici olmadığı için etkileşimli rebase
> çalışmıyor; aynı sonuçların bir kısmına başka yollarla ulaşırsın: son
> commit'lerden birini birleştirmek `git reset --soft` + commit (04), son
> mesajı değiştirmek `--amend`.

## Altın kural

**Başkalarının da aldığı commit'leri rebase etme** (ve `--amend`, `reset`
ile değiştirme). Rebase yeni commit'ler oluşturur; eskileri başkalarının
bilgisayarında durmaya devam eder. Sen yeni geçmişi zorla gönderirsen (09)
onların geçmişiyle seninki ayrışır, iş kaybolabilir.

Güvenli kullanım: **yalnızca sende olan** commit'ler (henüz push etmediğin ya
da yalnızca senin çalıştığın bir dal).

## Özet

- `git rebase main`: dalının commit'lerini `main`'in ucuna yeniden dizer;
  geçmiş düz kalır, hash'ler değişir.
- Çakışmada: düzelt → `git add` → `git rebase --continue` (ya da `--abort`,
  `--skip`).
- `git pull --rebase` yerel commit'leri gelenlerin üstüne dizer.
- `git cherry-pick <commit>` tek bir commit'i bulunduğun dala kopyalar.
- `git rebase -i` commit'leri birleştirir, yeniden adlandırır, siler (gerçek
  terminalde).
- Paylaşılmış geçmişi yeniden yazma.
