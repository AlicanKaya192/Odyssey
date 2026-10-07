# Genel Tekrar

Patikanın sonuna geldin. Bu bölümde öğrendiklerini tek bir projenin
yaşamı üzerinden bir kez daha görüyoruz; sonra 40 soruluk karışık bir sınav
ve bütün konuları birleştiren beş alıştırma var.

## Büyük resim

<figure class="fig">
  <div class="flow">
    <span class="node acc">dal</span><span class="arrow">→</span>
    <span class="node">commit</span><span class="arrow">→</span>
    <span class="node acc">PR</span><span class="arrow">→</span>
    <span class="node">merge</span><span class="arrow">→</span>
    <span class="node ok">tag</span>
  </div>
  <figcaption>Bir işin yolu: depoyu al (ya da init), dal aç, commit'le, gönderip PR aç, birleştir, sürüm etiketi koy. Her adımda git status; ters giden bir şeyde 04 (geri almak), 08 (çakışma) ve 14 (kurtarma).</figcaption>
</figure>

| Konu | Bölüm | Ana komutlar |
|---|---|---|
| Depo ve ayarlar | 00–01 | `git init`, `git config --global` |
| Üç alan, commit | 02 | `git status`, `git add`, `git commit -m` |
| Bakmak | 03 | `git diff`, `git log`, `git show`, `git blame` |
| Geri almak | 04 | `git restore`, `--amend`, `git reset`, `git revert` |
| Görmezden gelmek | 05 | `.gitignore`, `git check-ignore` |
| Dallar, birleştirme, çakışma | 06–08 | `git switch -c`, `git merge`, `--abort` |
| Uzak depolar, GitHub | 09–10 | `git clone`, `git push -u`, `git pull`, PR, fork |
| Kenara koymak | 11 | `git stash`, `git stash pop` |
| Geçmişi düzenlemek | 12 | `git rebase`, `git cherry-pick` |
| Sürümler | 13 | `git tag -a`, `git push --tags` |
| Kurtarma | 14 | `git reflog`, `HEAD@{n}` |
| Alışkanlıklar | 15 | küçük commit, iyi mesaj, GitHub Flow |

## Bir projenin yaşamı

Bir tarif sitesinin ilk gününden ilk sürümüne kadar her şey, tek oturumda:

```text
~ $ mkdir recipes
~ $ cd recipes
~/recipes $ git init
Initialized empty Git repository in /home/ada/recipes/.git/
~/recipes (main) $ echo "__pycache__/" > .gitignore
~/recipes (main) $ echo "# Recipes" > README.md
~/recipes (main) $ git add .
~/recipes (main) $ git commit -m "Start recipe site"
[main (root-commit) 3c8e414] Start recipe site
 2 files changed, 2 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
~/recipes (main) $ git remote add origin https://github.com/ada/recipes.git
~/recipes (main) $ git push -u origin main
To https://github.com/ada/recipes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
~/recipes (main) $ git switch -c soup
Switched to a new branch 'soup'
~/recipes (soup) $ echo "water" > soup.txt
~/recipes (soup) $ git add .
~/recipes (soup) $ git commit -m "Add soup recipe"
[soup 3123685] Add soup recipe
 1 file changed, 1 insertion(+)
 create mode 100644 soup.txt
~/recipes (soup) $ git push -u origin soup
remote: 
remote: Create a pull request for 'soup' on GitHub by visiting:
remote:      https://github.com/ada/recipes/pull/new/soup
remote: 
To https://github.com/ada/recipes.git
 * [new branch]      soup -> soup
branch 'soup' set up to track 'origin/soup'.
~/recipes (soup) $ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
~/recipes (main) $ git merge --no-ff soup --no-edit
Merge made by the 'ort' strategy.
 soup.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 soup.txt
~/recipes (main) $ git branch -d soup
Deleted branch soup (was 3123685).
~/recipes (main) $ git push
To https://github.com/ada/recipes.git
   3c8e414..3c8d14a  main -> main
~/recipes (main) $ git tag -a v1.0 -m "First version"
~/recipes (main) $ git push origin v1.0
To https://github.com/ada/recipes.git
 * [new tag]         v1.0 -> v1.0
~/recipes (main) $ git log --oneline --graph
*   3c8d14a (HEAD -> main, tag: v1.0, origin/main) Merge branch 'soup'
|\  
| * 3123685 (origin/soup) Add soup recipe
|/  
* 3c8e414 Start recipe site
```

Bu oturumda neler oldu:

1. Depo açıldı, `.gitignore` ilk commit'ten önce yazıldı.
2. GitHub'daki boş depoya `-u` ile ilk gönderim.
3. Yeni iş bir dalda; dal gönderildi (PR açılacak).
4. Birleştirme `--no-ff` ile, dal silindi.
5. Sürüm açıklamalı etiketle işaretlendi ve etiket ayrıca gönderildi.

## Hangi durumda ne yaparım?

| Durum | Bölüm | Çıkış |
|---|---|---|
| Ne olduğunu anlamadım | hepsi | `git status` |
| Dosyadaki değişikliği atmak istiyorum | 04 | `git restore dosya` |
| Son commit'i düzeltmek istiyorum (push etmedim) | 04 | `git commit --amend` |
| Paylaşılmış bir commit'i geri almak istiyorum | 04 | `git revert` |
| İstemediğim dosyalar `git status`'ta | 05 | `.gitignore` |
| Çakışma çıktı | 08 | düzelt → `git add` → `git commit --no-edit` / `--abort` |
| Push reddedildi | 09 | `git pull`, sonra `git push` |
| Yarım işle dal değiştirmem gerek | 11 | `git stash` |
| Dalım geride kaldı | 07 / 12 | `git merge main` ya da `git rebase main` |
| Bir şeyi kaybettim | 14 | `git reflog` |

## Buradan sonra

Git'in en çok kullanılan kısmını öğrendin; günlük işin büyük çoğunluğu bu
komutlarla yürür. Sıradaki adım **gerçek bir proje**: GitHub'da bir depo aç,
bu patikadaki akışı kendi kodunla uygula. Bilmediğin bir şeyle
karşılaşırsan "Buradan Sonrası" notunda nereye bakacağın var.
