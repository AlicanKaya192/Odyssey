# Stash: İşi Kenara Koymak

Bir dalda yarım bir iş üzerindesin. Tam o sırada acil bir istek geliyor:
`main`'de bir yazım hatası hemen düzeltilmeli. Dal değiştirmen gerekiyor ama:

- Yarım işi commit'lemek istemiyorsun (henüz çalışmıyor, geçmişi kirletir).
- Commit'lemeden dal değiştirmeye çalışınca Git ya değişikliği yanında
  taşıyor ya da reddediyor (06).

**Stash** (zula, kenara koyma) tam bunun için: commit'lenmemiş
değişikliklerini bir kenara kaldırır, çalışma alanını temizler. İşin bitince
geri getirirsin.

<figure class="fig">
  <div class="flow">
    <span class="node no">Yarım iş<br><small>commit'lenmemiş</small></span><span class="arrow">→</span>
    <span class="node acc">git stash</span><span class="arrow">→</span>
    <span class="node ok">Temiz alan<br><small>başka iş</small></span><span class="arrow">→</span>
    <span class="node acc">git stash pop</span><span class="arrow">→</span>
    <span class="node no">Geri geldi</span>
  </div>
  <figcaption>Stash commit'lenmemiş değişiklikleri bir kenara kaldırır; geri getirince kaldığın yerden devam edersin.</figcaption>
</figure>

## Kenara koymak ve geri getirmek

```text
~/site (main) $ echo "h1 {color: red}" >> style.css
~/site (main) $ git status -s
 M style.css
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (5e414f930ae1a4280290b7040f79f5b9c495f800)
```

- `git stash` değişiklikleri kaldırdı; `git status` temiz. Artık rahatça dal
  değiştirebilirsin.
- `Saved working directory and index state WIP on main: …` "main'in şu
  commit'inin üstündeki yarım iş (*work in progress*) kaydedildi" demek.
- `git stash pop` en son kaldırılanı geri getirip listeden siler.

## Acil iş senaryosu

```text
~/site (redesign) $ echo "h1 {font-size: 3em}" >> style.css
~/site (redesign) $ git stash
Saved working directory and index state WIP on redesign: e20491f Add home page
~/site (redesign) $ git switch main
Switched to branch 'main'
~/site (main) $ echo "<h1>Welcome</h1>" > index.html
~/site (main) $ git commit -am "Fix typo"
[main baff07e] Fix typo
 1 file changed, 1 insertion(+), 1 deletion(-)
~/site (main) $ git switch redesign
Switched to branch 'redesign'
~/site (redesign) $ git stash pop
On branch redesign
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (ee4d503a89591f06c196b2b1fc1bccbc64a59df2)
```

Yarım iş hiç commit'lenmedi, acil düzeltme kendi dalında yapıldı ve gönderime
hazır, sonra kaldığın yerden devam ettin.

## Birden çok stash

Stash bir **yığın**: her `git stash` en üste yeni bir kayıt koyar. `git
stash list` hepsini gösterir; en yenisi `stash@{0}`, bir öncekisi
`stash@{1}`. Mesaj vermek bulmayı kolaylaştırır:

```text
~/site (main) $ echo "h1 {color: red}" >> style.css
~/site (main) $ git stash push -m "try red"
Saved working directory and index state On main: try red
~/site (main) $ echo "h1 {color: blue}" >> style.css
~/site (main) $ git stash push -m "try blue"
Saved working directory and index state On main: try blue
~/site (main) $ git stash list
stash@{0}: On main: try blue
stash@{1}: On main: try red
~/site (main) $ git stash show stash@{1}
 style.css | 1 +
 1 file changed, 1 insertion(+)
~/site (main) $ git stash apply stash@{1}
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
~/site (main) $ git stash list
stash@{0}: On main: try blue
stash@{1}: On main: try red
```

| Komut | Ne yapar |
|---|---|
| `git stash` | Değişiklikleri kaldırır (mesaj: `WIP on dal: …`). |
| `git stash push -m "mesaj"` | Kendi mesajınla kaldırır. |
| `git stash list` | Kayıtları listeler. |
| `git stash show` | En sondakinin hangi dosyaları değiştirdiğini gösterir; `-p` farkı. |
| `git stash pop` | En sondakini uygular ve **siler**. |
| `git stash apply stash@{1}` | Belirli bir kaydı uygular, **silmez**. |
| `git stash drop stash@{1}` | Bir kaydı uygulamadan siler. |
| `git stash clear` | ⚠ Bütün kayıtları siler. |

`pop` ile `apply` farkı: `apply` kaydı listede bırakır; aynı değişikliği
başka bir dala da uygulamak istersen işe yarar.

## İzlenmeyen dosyalar: `-u`

`git stash` varsayılan olarak yalnızca **izlenen** dosyalardaki
değişiklikleri alır. Yeni (izlenmeyen) bir dosya klasörde kalır:

```text
~/site (main) $ echo "h1 {}" >> style.css
~/site (main) $ echo "draft" > notes.txt
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
?? notes.txt
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (cb05b8cf2da6315c557d413607b2148bcd53da62)
~/site (main) $ git stash -u
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (be19b371c1deda113dd29deeefbaf38b9d5cf94b)
```

`-u` (*include untracked*) yeni dosyaları da kaldırır.

## Başka bir dalda geri getirmek

Stash bir dala bağlı değildir. Yanlış dalda çalışmaya başladığını fark
edersen: kaldır, doğru dala geç, orada geri getir.

```text
~/site (main) $ echo "<input>" >> index.html
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git switch -c search
Switched to a new branch 'search'
~/site (search) $ git stash pop
On branch search
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   index.html

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (42a7a3946d54809cbde91659c0d836f0e285e9c7)
~/site (search) $ git commit -am "Add search box"
[search 623d81e] Add search box
 1 file changed, 1 insertion(+)
~/site (search) $ git log --oneline --all
623d81e (HEAD -> search) Add search box
e20491f (main) Add home page
```

## Çakışma

Stash'i geri getirirken aynı satırlar bu arada değiştiyse birleştirmedeki
gibi çakışma olabilir. Çözümü aynı: dosyayı düzelt, `git add`. Çakışma olursa
`pop` kaydı **silmez** (iş kaybolmasın); çözünce `git stash drop` ile
sen silersin.

## Ne zaman stash, ne zaman commit?

Stash kısa süreli bir cep: birkaç dakika ya da saat. Günlerce duran iş
stash'te unutulur; liste uzar ve neyin ne olduğu karışır. Uzun beklemesi
gereken iş için bir dal aç ve commit'le (mesajı `WIP` olabilir; sonra
`--amend` ya da squash ile düzeltirsin).

## Özet

- `git stash` commit'lenmemiş değişiklikleri kaldırır, çalışma alanını
  temizler; `git stash pop` geri getirir.
- Stash bir yığın: `stash@{0}` en yeni; `list`, `show`, `apply`, `drop`.
- `-m` mesaj, `-u` izlenmeyen dosyalar.
- Stash dala bağlı değil; başka dalda geri getirilebilir.
- Kısa süre için stash, uzun süre için dal + commit.
