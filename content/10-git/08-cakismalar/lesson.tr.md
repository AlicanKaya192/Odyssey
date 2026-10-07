# Çakışmalar

Git iki dalı birleştirirken çoğu zaman her şeyi kendisi halleder. Ama iki dal
**aynı dosyanın aynı satırını farklı biçimde** değiştirdiyse hangisinin doğru
olduğunu bilemez. Bu durumda birleştirmeyi yarıda durdurur ve kararı sana
bırakır: buna **çakışma** (*merge conflict*) denir.

Çakışma bir hata değildir; bir **soru**. Korkulacak bir şey de yok: ne
yaptığını bilmezsen birleştirmeyi tek komutla iptal edersin.

## Önce: Git neyi kendisi birleştirir?

Bir dükkânın tanıtım sayfası (`page.txt`) üç satır. `summer` dalında ilk
satır, `main`'de son satır değişmiş olsun: farklı satırlar, çakışma yok.

```text
~/shop (main) $ git merge summer --no-edit
Auto-merging page.txt
Merge made by the 'ort' strategy.
 page.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
~/shop (main) $ cat page.txt
Welcome to summer!
We sell books
Open 8-17
```

`Auto-merging page.txt` Git'in dosyanın içine bakıp iki değişikliği de
aldığını söylüyor.

## Çakışma nasıl görünür?

Şimdi iki dal **aynı satırı** (açılış saatini) farklı değiştirmiş olsun:
`summer`'da `Open 9-20`, `main`'de `Open 8-17`.

```text
~/shop (main) $ git merge summer
Auto-merging page.txt
CONFLICT (content): Merge conflict in page.txt
Automatic merge failed; fix conflicts and then commit the result.
~/shop (main|MERGING) $ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   page.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Üç şey oldu:

1. Git `CONFLICT` dedi ve hangi dosyada olduğunu yazdı.
2. Birleştirme **yarıda kaldı**: commit atılmadı. İstem `(main|MERGING)`
   oldu; "birleştirmenin ortasındasın" diyor.
3. `git status` çakışan dosyayı **Unmerged paths** altında, `both modified`
   (iki taraf da değiştirdi) olarak gösteriyor.

## Çakışma işaretleri

Git çakışan dosyanın içine iki hâli de yazdı:

```text
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
<<<<<<< HEAD
Open 8-17
=======
Open 9-20
>>>>>>> summer
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</span><span>Bizim tarafın başladığı yer: bulunduğun dal (main).</span></div>
    <div class="anat-row"><span>Open 8-17</span><span>main'deki hâl.</span></div>
    <div class="anat-row"><span>=======</span><span>İki tarafı ayıran çizgi.</span></div>
    <div class="anat-row"><span>Open 9-20</span><span>Getirdiğin daldaki hâl.</span></div>
    <div class="anat-row"><span>&gt;&gt;&gt;&gt;&gt;&gt;&gt; summer</span><span>Gelen tarafın bittiği yer ve dalın adı.</span></div>
  </div>
  <figcaption>Çözmek: bu beş satırın yerine doğru olan tek satırı (ya da satırları) bırak, işaretleri sil.</figcaption>
</figure>

`HEAD` bulunduğun dal (`main`), `summer` getirdiğin dal. Git'in kafası
yalnızca o satırda karıştı; dosyanın geri kalanı (`Welcome`, `We sell books`) normal.

## Çözmek: üç adım

1. **Dosyayı istediğin son hâline getir.** İşaret satırlarını (`<<<<<<<`,
   `=======`, `>>>>>>>`) sil, doğru içeriği bırak. Biri, öbürü ya da ikisinin
   karışımı olabilir; karar senin. Burada sabah 8'de açılıp akşam 8'de
   kapanmaya karar verelim: `Open 8-20`.
2. **`git add dosya`** ile "bu dosyayı çözdüm" de.
3. **Birleştirmeyi bitir:** `git commit --no-edit` (hazır birleştirme
   mesajıyla). `git merge --continue` de aynı işi yapar.

```text
~/shop (main|MERGING) $ echo "Welcome" > page.txt
~/shop (main|MERGING) $ echo "We sell books" >> page.txt
~/shop (main|MERGING) $ echo "Open 8-20" >> page.txt
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
Open 8-20
~/shop (main|MERGING) $ git add page.txt
~/shop (main|MERGING) $ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
        modified:   page.txt
~/shop (main|MERGING) $ git commit --no-edit
[main c02108b] Merge branch 'summer'
~/shop (main) $ git log --oneline --graph
*   c02108b (HEAD -> main) Merge branch 'summer'
|\  
| * 524d5b4 (summer) Summer hours
* | 41667c0 Open earlier
|/  
* 071cfb3 Add page
```

> Gerçek bir projede dosyayı düzenleyicide açıp düzeltirsin. VS Code
> çakışma işaretlerini tanır ve üstlerinde *Accept Current Change* (bizimki),
> *Accept Incoming Change* (gelen), *Accept Both Changes* (ikisi) bağlantıları
> gösterir. Odyssey'nin terminalinde düzenleyici olmadığı için dosyayı
> `echo` ile yeniden yazıyoruz: ilk satır `>`, sonrakiler `>>`.

## Bir tarafı olduğu gibi almak

Bazen çözüm basittir: "tamamen benimki" ya da "tamamen gelen". Satır satır
düzenlemek yerine:

| Komut | Dosya neye döner |
|---|---|
| `git checkout --ours dosya` | Bulunduğun dalın hâline (`HEAD`). |
| `git checkout --theirs dosya` | Birleştirdiğin dalın hâline. |

(`git restore --ours` / `--theirs` aynı işi yapar.) Ardından yine
`git add` ve commit:

```text
~/shop (main|MERGING) $ git checkout --theirs page.txt
Updated 1 path from the index
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
Open 9-20
~/shop (main|MERGING) $ git add page.txt
~/shop (main|MERGING) $ git commit -m "Merge summer hours"
[main 1f9b310] Merge summer hours
```

> Birleştirmede **ours** her zaman bulunduğun dal, **theirs** `git merge`'e
> verdiğin dal. (12'de göreceğimiz `rebase`'de ikisi yer değiştirir; o
> yüzden karıştırılır.)

## Vazgeçmek: `git merge --abort`

Çakışma beklemediğin kadar büyükse ya da yanlış dalı birleştirdiysen
birleştirmeyi iptal et. Her şey `git merge`'den önceki hâline döner:

```text
~/shop (main) $ git merge summer
Auto-merging page.txt
CONFLICT (content): Merge conflict in page.txt
Automatic merge failed; fix conflicts and then commit the result.
~/shop (main|MERGING) $ git merge --abort
~/shop (main) $ git status
On branch main
nothing to commit, working tree clean
~/shop (main) $ cat page.txt
Welcome
We sell books
Open 8-17
```

## Çözmeden commit atamazsın

Çakışan dosyayı `git add` ile işaretlemeden commit atmaya çalışırsan Git
reddeder ve hangi dosyaların beklediğini söyler:

```text
~/shop (main|MERGING) $ git commit -m "Merge"
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U       page.txt
```

## Çakışmayı azaltmak

- **Küçük ve sık commit, kısa ömürlü dal.** Dal ne kadar uzun yaşarsa `main`
  ile o kadar ayrışır.
- **`main`'i dalına sık birleştir** (07). Çakışmalar küçükken çözülür.
- **Aynı dosyada çalışacaksanız konuşun.** Git'in değil, ekibin işi.
- **Biçimlendirmeyi karıştırma.** Bir dosyanın bütün girintisini
  değiştirmek her satırı "değişti" yapar; başkasının işiyle mutlaka çakışır.

## Özet

- Çakışma: iki dal aynı satırı farklı değiştirdi; Git sorar.
- `git status` çakışan dosyaları `both modified` olarak gösterir; istem
  `MERGING` der.
- İşaretler: `<<<<<<< HEAD` (bizimki) … `=======` … `>>>>>>> dal` (gelen).
- Çözmek: dosyayı düzelt → `git add` → `git commit --no-edit`.
- `--ours` / `--theirs` bir tarafı olduğu gibi alır.
- `git merge --abort` her şeyi birleştirmeden önceki hâline döndürür.
