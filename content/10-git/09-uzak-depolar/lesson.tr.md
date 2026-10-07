# Uzak Depolar

Şimdiye kadar her şey yalnızca senin bilgisayarındaydı. Bilgisayar bozulursa
geçmiş de gider; başkasıyla çalışmak da mümkün değil. **Uzak depo**
(*remote*) aynı deponun başka bir yerdeki kopyası: çoğu zaman GitHub'da.

Uzak depoyla üç şey yaparsın:

- **`clone`**: uzak depoyu geçmişiyle birlikte bilgisayarına indir.
- **`push`**: kendi commit'lerini uzak depoya gönder.
- **`fetch` / `pull`**: başkalarının gönderdiği commit'leri al.

<figure class="fig">
  <div class="flow">
    <span class="node">Sen<br><small>main</small></span><span class="arrow">→</span>
    <span class="node acc">git push</span><span class="arrow">→</span>
    <span class="node ok">GitHub<br><small>origin</small></span><span class="arrow">→</span>
    <span class="node acc">git pull</span><span class="arrow">→</span>
    <span class="node">Ekip arkadaşın<br><small>main</small></span>
  </div>
  <figcaption>GitHub ortak buluşma yeri: herkes kendi commit'ini oraya gönderir, başkalarınınkini oradan alır.</figcaption>
</figure>

> Bu bölümün terminalinde GitHub taklit ediliyor: `https://github.com/...`
> adresleri benzeticinin içinde, internete çıkılmıyor. Komutlar ve çıktılar
> gerçek GitHub'dakiyle aynı; yalnızca indirme ilerleme satırları
> (`Receiving objects: 100%` gibi) kısaltıldı.

## `git clone`: indirmek

Grace'in tarif deposunu indirelim:

```text
~ $ git clone https://github.com/grace/recipes.git
Cloning into 'recipes'...
~ $ cd recipes
~/recipes (main) $ ls
README.md  soup.txt
~/recipes (main) $ git log --oneline
b2024e6 (HEAD -> main, origin/main, origin/HEAD) Add soup
~/recipes (main) $ git remote -v
origin  https://github.com/grace/recipes.git (fetch)
origin  https://github.com/grace/recipes.git (push)
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`git clone` dört şey yaptı:

1. `recipes` klasörünü açtı ve bütün commit'leri indirdi.
2. Uzak depoyu **`origin`** adıyla kaydetti (`git remote -v`). `origin`
   yalnızca bir takma ad; "indirdiğim yer" demek.
3. Uzaktaki her dal için bir **uzak izleme dalı** oluşturdu: `origin/main`.
4. Senin `main` dalını `origin/main`'i **izleyecek** şekilde ayarladı;
   `git status` bu yüzden "up to date with 'origin/main'" diyor.

## Uzak izleme dalları

`origin/main`, "**son baktığımda** GitHub'daki `main` buradaydı" demek. Senin
bilgisayarında durur ve kendiliğinden güncellenmez; yalnızca `fetch`, `pull`
ve `push` onu günceller. Bu yüzden Git sana "geridesin" diyebilmek için önce
GitHub'a bakmalı (`fetch`).

| Ad | Ne |
|---|---|
| `main` | Senin dalın; commit atınca ilerler. |
| `origin/main` | GitHub'daki `main`'in son bilinen yeri. |
| `origin/HEAD` | Uzak deponun varsayılan dalı (`origin/main`'i gösterir). |

## `git push`: göndermek

Bir değişiklik yapıp gönderelim:

```text
~/recipes (main) $ echo "salt" >> soup.txt
~/recipes (main) $ git commit -am "Add salt"
[main d7bf1c2] Add salt
 1 file changed, 1 insertion(+)
~/recipes (main) $ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
   b2024e6..d7bf1c2  main -> main
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Commit'ten sonra `git status` "ahead of 'origin/main' by 1 commit" diyor:
sende var, GitHub'da yok. `git push` gönderdi; son satırdaki `eski..yeni  main
-> main` "GitHub'daki main'i şu commit'ten şu commit'e taşıdım" demek.

## Kendi deponu GitHub'a koymak

Bilgisayarında `git init` ile başladığın bir depoyu ilk kez göndermek için:

1. GitHub'da **boş** bir depo oluştur (README eklemeden; 10'da adım adım).
   GitHub sana deponun adresini verir.
2. Adresi `origin` adıyla kaydet: `git remote add origin <adres>`.
3. İlk gönderimi `-u` ile yap: `git push -u origin main`.

```text
~/notes (main) $ git remote add origin https://github.com/ada/notes.git
~/notes (main) $ git remote -v
origin  https://github.com/ada/notes.git (fetch)
origin  https://github.com/ada/notes.git (push)
~/notes (main) $ git push -u origin main
To https://github.com/ada/notes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
~/notes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`-u` (*set upstream*) "bundan sonra `main`, `origin/main`'i izlesin" der.
Bir kez yaptıktan sonra yalnızca `git push` ve `git pull` yazarsın.

> **Gerçek GitHub'a ilk gönderimde** kimliğini doğrulaman gerekir. Windows'ta
> Git ile gelen *Git Credential Manager* tarayıcıda GitHub giriş sayfasını
> açar; bir kez onaylarsın, sonrası hatırlanır. GitHub artık hesap şifresiyle
> push kabul etmiyor; tarayıcı girişi, kişisel erişim anahtarı (*token*) ya da
> SSH anahtarı gerekir.

Adres yanlışsa ya da depo GitHub'da açılmamışsa:

```text
~/notes (main) $ git remote add origin https://github.com/ada/notse.git
~/notes (main) $ git push -u origin main
remote: Repository not found.
fatal: repository 'https://github.com/ada/notse.git/' not found
```

## `git fetch`: bakmak

Grace depoya yeni bir commit göndermiş olsun. Senin bilgisayarın bunu
bilmez; önce sorman gerekir:

```text
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
~/recipes (main) $ git fetch
From https://github.com/grace/recipes
   b2024e6..37e19db  main       -> origin/main
~/recipes (main) $ git status
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
~/recipes (main) $ git log --oneline --all
37e19db (origin/main, origin/HEAD) Add bread recipe
b2024e6 (HEAD -> main) Add soup
~/recipes (main) $ ls
README.md  soup.txt
```

`git fetch` yeni commit'leri indirdi ve `origin/main`'i ilerletti; **senin
`main` dalına dokunmadı**, dosyaların değişmedi. Şimdi `git status` geride
olduğunu söyleyebiliyor. `fetch` güvenlidir: hiçbir şeyini değiştirmez,
yalnızca haber getirir.

## `git pull`: almak

`git pull` = `git fetch` + `git merge origin/main`. Sende yeni commit
yoksa birleştirme ileri sarma olur:

```text
~/recipes (main) $ git pull
From https://github.com/grace/recipes
   b2024e6..37e19db  main       -> origin/main
Updating b2024e6..37e19db
Fast-forward
 bread.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 bread.txt
~/recipes (main) $ ls
README.md  bread.txt  soup.txt
```

## İki taraf da ilerlediyse

Sen bir commit attın, bu arada Grace de gönderdi. Göndermeye çalışınca:

```text
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/grace/recipes.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

GitHub reddetti: kabul etseydi Grace'in commit'i kaybolurdu. Önce onun işini
almalısın. Ama `git pull` da bir karar ister:

```text
~/recipes (main) $ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
~/recipes (main) $ git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

İki dal ayrıştığı için Git birleştirme mi (*merge*) yoksa yeniden dizme mi
(*rebase*, 12) istediğini soruyor. Birleştirme seçelim; her seferinde yazmamak
için ayarı bir kez yapabilirsin: `git config --global pull.rebase false`.

```text
~/recipes (main) $ git pull --no-rebase --no-edit
From https://github.com/grace/recipes
   b2024e6..458d82a  main       -> origin/main
Merge made by the 'ort' strategy.
 bread.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 bread.txt
~/recipes (main) $ git log --oneline --graph
*   dd028b4 (HEAD -> main) Merge branch 'main' of https://github.com/grace/recipes
|\  
| * 458d82a (origin/main, origin/HEAD) Add bread recipe
* | d7bf1c2 Add salt
|/  
* b2024e6 Add soup
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
   458d82a..dd028b4  main -> main
```

Artık senin ve Grace'in commit'leri birleşti; gönderim kabul edildi.

## Dalları göndermek

Kendi dalını da gönderebilirsin; ekip arkadaşların görür, GitHub'da pull
request açarsın (10):

```text
~/recipes (main) $ git switch -c spicy
Switched to a new branch 'spicy'
~/recipes (spicy) $ echo "chili" >> soup.txt
~/recipes (spicy) $ git commit -am "Add chili"
[spicy cf97db7] Add chili
 1 file changed, 1 insertion(+)
~/recipes (spicy) $ git push
fatal: The current branch spicy has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin spicy

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

~/recipes (spicy) $ git push -u origin spicy
remote: 
remote: Create a pull request for 'spicy' on GitHub by visiting:
remote:      https://github.com/grace/recipes/pull/new/spicy
remote: 
To https://github.com/grace/recipes.git
 * [new branch]      spicy -> spicy
branch 'spicy' set up to track 'origin/spicy'.
~/recipes (spicy) $ git branch -a
  main
* spicy
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
  remotes/origin/spicy
```

`remote:` ile başlayan satırları GitHub yazıyor: yeni dal için bir "pull request"
bağlantısı veriyor. Pull request'i bir sonraki bölümde göreceğiz.

Bir dalı GitHub'dan silmek için `git push origin --delete dal`.

## Gönderilmiş geçmişi değiştirme

`--amend`, `reset`, `rebase` geçmişi yeniden yazar. Commit'ler henüz yalnızca
sendeyken sorun değil. **Gönderdikten sonra** yaparsan GitHub'daki geçmişle
seninki ayrışır ve `push` reddedilir. `git push --force` reddi ezip geçer
ama başkalarının o arada gönderdiği commit'leri **siler**. ⚠ Paylaşılmış bir
dalda zorla gönderme; gerekiyorsa en azından `--force-with-lease` kullan
(başkası bir şey gönderdiyse reddeder).

## Özet

- Uzak depo başka yerdeki kopya; varsayılan adı `origin`.
- `git clone` indirir, `origin`'i ve izlemeyi ayarlar.
- `origin/main` GitHub'daki dalın son bilinen yeri; `fetch` / `pull` /
  `push` günceller.
- `git push` gönderir; ilk kez `git remote add origin <adres>` +
  `git push -u origin main`.
- `git fetch` yalnızca haber getirir; `git pull` = fetch + merge.
- Reddedilen push: önce `git pull` (gerekirse `--no-rebase`), sonra
  `git push`.
- Paylaşılmış geçmişi yeniden yazma; zorla gönderme.
