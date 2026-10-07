# Dallar

Şimdiye kadar bütün commit'ler tek bir çizgi üzerindeydi. Gerçek projelerde
aynı anda birden çok iş yürür: bir yandan yeni bir özellik yazarsın, bir
yandan acil bir hata çıkar. Yeni özellik yarımken hatayı düzeltip yayınlaman
gerekir; yarım iş de ortalıkta olmamalı.

Git'in cevabı **dal** (*branch*): geçmişin ayrı bir kolu. Her dal kendi
commit'lerini biriktirir, diğerine dokunmaz. Denemeni bir dalda yaparsın;
beğenirsen ana dalla birleştirirsin (07), beğenmezsen dalı silersin.

## Dal aslında bir etiket

Git'te dal, **bir commit'i gösteren bir addır**, o kadar. Bir dal açmak
klasörü kopyalamaz; yalnızca küçük bir işaret oluşturur. Bu yüzden dal
açmak anlıktır ve hiç yer kaplamaz.

<figure class="fig">
  <div class="flow">
    <span class="node">Add home page</span><span class="arrow">→</span>
    <span class="node">Add styles</span><span class="arrow">→</span>
    <span class="node acc">Add login form<br><small>login ← HEAD</small></span>
  </div>
  <figcaption>Dallar commit'leri gösteren etiketler. login dalında commit atınca yalnızca login etiketi ilerledi; main yerinde kaldı.</figcaption>
</figure>

Commit attığında **bulunduğun dalın etiketi** yeni commit'e kayar.
**HEAD** "şu an hangi daldayım" sorusunun cevabıdır; istemdeki `(main)`
da bunu gösterir.

## Dalları görmek ve dal açmak

```text
~/site (main) $ git branch
* main
~/site (main) $ git branch login
~/site (main) $ git branch
  login
* main
~/site (main) $ git branch -v
  login 7085b6f Add styles
* main  7085b6f Add styles
```

- `git branch` dalları listeler; `*` bulunduğun dal.
- `git branch login` yeni dal **açar ama geçmez**: hâlâ `main`'desin.
- `git branch -v` her dalın gösterdiği commit'i de yazar. İki dal da aynı
  commit'i gösteriyor: yeni dal, açıldığı yerden başlar.

## Dala geçmek: `git switch`

```text
~/site (main) $ git switch login
Switched to branch 'login'
~/site (login) $ echo "<form>" > login.html
~/site (login) $ git add login.html
~/site (login) $ git commit -m "Add login form"
[login 8072547] Add login form
 1 file changed, 1 insertion(+)
 create mode 100644 login.html
~/site (login) $ git branch -v
* login 8072547 Add login form
  main  7085b6f Add styles
```

Artık `login` dalındayız (istem `(login)` diyor). Burada atılan commit
yalnızca bu dalı ilerletti; `main` eski yerinde kaldı. `git log --oneline
--all --graph` bütün dalları birlikte çizer:

```text
~/site (main) $ git log --oneline --graph --all
* 0bb20c6 (HEAD -> main) Fix typo
| * 8072547 (login) Add login form
|/  
* 7085b6f Add styles
* a0cf655 Add home page
```

Açıp geçmek en sık yapılan iş olduğu için kısayolu var:

```bash
git switch -c contact     # -c: create, aç ve geç
```

> Eski yazım: `git checkout -b contact`. İnternetteki çoğu örnek bunu
> kullanır; aynı işi yapar.

## Dal değiştirince dosyalar değişir

Bir dala geçmek, klasördeki dosyaları **o dalın son commit'indeki hâline**
getirir. `login` dalında eklenen dosya `main`'de yoktur:

```text
~/site (main) $ ls
index.html  style.css
~/site (main) $ git switch login
Switched to branch 'login'
~/site (login) $ ls
index.html  login.html  style.css
~/site (login) $ git switch -
Switched to branch 'main'
~/site (main) $ ls
index.html  style.css
```

Dosya kaybolmadı: `login` dalının commit'inde duruyor. Dala geri dönünce
yerine gelir. `git switch -` bir önceki dala döner (iki dal arasında gidip
gelirken kullanışlı).

## Commit'lenmemiş değişiklikler ne olur?

Commit'lemediğin değişiklikler bir dala ait değildir; seninle birlikte
taşınırlar. Git dal değiştirirken bunları sana hatırlatır (`M` satırları):

```text
~/site (main) $ echo "h1 {}" >> style.css
~/site (main) $ git switch -c contact
M       style.css
Switched to a new branch 'contact'
~/site (contact) $ git status -s
 M style.css
```

Ama gideceğin dalda aynı dosya **farklıysa**, Git değişikliğini ezmemek için
dal değiştirmeyi reddeder:

```text
~/site (main) $ echo "<h1>Welcome</h1>" > index.html
~/site (main) $ git switch login
error: Your local changes to the following files would be overwritten by checkout:
        index.html
Please commit your changes or stash them before you switch branches.
Aborting
```

İki çıkış var: değişikliği önce commit'le, ya da kenara koy (`git stash`,
bölüm 11).

## Dalları düzenlemek

| Komut | Ne yapar |
|---|---|
| `git branch -m eski yeni` | Dalın adını değiştirir (`-m yeni` bulunduğun dalı). |
| `git branch -d ad` | Dalı siler; işi başka bir dala birleştirilmiş olmalı. |
| `git branch -D ad` | Dalı **zorla** siler; birleştirilmemiş commit'ler daldan düşer. ⚠ |
| `git branch --merged` | Bulunduğun dala birleştirilmiş dallar (silmesi güvenli). |
| `git branch --no-merged` | Henüz birleştirilmemiş dallar. |

```text
~/site (main) $ git branch --merged
* main
  old-idea
~/site (main) $ git branch --no-merged
  experiment
  login
~/site (main) $ git branch -d old-idea
Deleted branch old-idea (was 7085b6f).
~/site (main) $ git branch -d experiment
error: the branch 'experiment' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D experiment'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
~/site (main) $ git branch -D experiment
Deleted branch experiment (was 5d34b75).
~/site (main) $ git branch
  login
* main
```

`-d` birleştirilmemiş bir dalı silmeyi reddeder; içinde başka hiçbir yerde
olmayan commit'ler var. Gerçekten atmak istiyorsan `-D`.

> Bulunduğun dalı silemezsin; önce başka bir dala geç.

## Dal adları

- Kısa ve ne için olduğunu söyleyen: `login`, `fix-typo`, `contact-page`.
- Boşluk kullanılmaz; kelimeler `-` ile ayrılır.
- Ekipler sık sık önek kullanır: `feature/login`, `fix/header`. Eğik çizgi
  dalı bir klasördeymiş gibi saklar; bu yüzden `feature` adlı bir dal
  varken `feature/login` açılamaz.
- Ana dal çoğu projede `main`. Ona doğrudan deneme commit'i atmak yerine
  dal aç: `main` her zaman çalışan hâli göstersin.

## Özet

- Dal bir commit'i gösteren hareketli bir addır; açmak anlık ve ucuz.
- `git branch` listeler / açar, `git switch` geçer, `git switch -c` açıp
  geçer.
- Commit yalnızca bulunduğun dalı ilerletir; HEAD bulunduğun dalı gösterir.
- Dal değiştirmek klasördeki dosyaları o dalın hâline getirir;
  commit'lenmemiş değişiklikler taşınır ya da Git dal değiştirmeyi reddeder.
- `git log --oneline --graph --all` dalları birlikte çizer.
- `-m` yeniden adlandırır, `-d` güvenle siler, `-D` zorla siler.
