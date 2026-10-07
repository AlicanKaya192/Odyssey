# GitHub ile Çalışmak

Git bir araçtı; GitHub o aracın etrafına kurulmuş bir **çalışma yeri**:
depoların internette durduğu, ekiplerin kodu birlikte gözden geçirdiği,
hataların ve görevlerin takip edildiği yer. Bu bölümde GitHub'ın Git ile
birleştiği noktaları göreceğiz: depo açmak, **pull request**, **fork** ve
**issue**.

> GitHub'ın kendisi bir web sitesi; tıklanacak düğmeleri anlatacağız. Terminal
> tarafını (her zaman aynı kalan kısmı) alıştırmalarda yapacaksın.

## Bir depo sayfası

GitHub'da bir deponun sayfasında şu sekmeler bulunur:

| Sekme | Ne var |
|---|---|
| **Code** | Dosyalar, dallar, commit geçmişi; altta `README.md` çizilmiş hâlde. Yeşil **Code** düğmesi klonlama adresini verir. |
| **Issues** | Hata bildirimleri, istekler, yapılacaklar. |
| **Pull requests** | Birleştirilmeyi bekleyen dallar ve tartışmaları. |
| **Actions** | Otomatik işler (her push'ta testleri çalıştırmak gibi). |
| **Settings** | Depo adı, görünürlük, ortak çalışanlar, dal korumaları. |

## Depo oluşturmak

1. Sağ üstteki **+** → **New repository**.
2. **Repository name**: kısa, boşluksuz (`notes`). **Description** isteğe bağlı.
3. **Public** (herkes görür) ya da **Private** (yalnızca sen ve davet
   ettiklerin).
4. Bilgisayarında zaten bir depo varsa **README, .gitignore ve lisans
   ekleme**: GitHub'daki depo boş kalsın, yoksa ilk push reddedilir (iki
   tarafın geçmişi farklı başlar).
5. **Create repository**.

GitHub boş deponun sayfasında hazır komutlar gösterir. "Komut satırında yeni
bir depo oluştur" kısmı şudur:

```text
~/notes $ echo "# notes" >> README.md
~/notes $ git init
Initialized empty Git repository in /home/ada/notes/.git/
~/notes (main) $ git add README.md
~/notes (main) $ git commit -m "first commit"
[main (root-commit) 9a20964] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
~/notes (main) $ git branch -M main
~/notes (main) $ git remote add origin https://github.com/ada/notes.git
~/notes (main) $ git push -u origin main
To https://github.com/ada/notes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Tek yeni komut `git branch -M main`: bulunduğun dalın adını zorla `main`
yapar (eski ayarlarla `master` açılmış depolar için). Dal zaten `main`
olduğu için burada bir şey değişmedi.

## README.md

Deponun ana sayfasında çizilen dosya `README.md`. Projeyi ilk kez gören
birinin okuyacağı şey: ne işe yarar, nasıl kurulur, nasıl kullanılır.
Markdown ile yazılır:

```text
# Notlarım

Günlük işlerimi takip ettiğim küçük bir depo.

## Kullanım

- `todo.txt` yapılacaklar
- `done.txt` bitenler
```

`#` başlık, `-` madde, ters tırnak kod. GitHub bunları biçimlendirilmiş
gösterir.

## Pull request: "dalımı birleştirir misiniz?"

Ekiplerde `main`'e doğrudan push yapılmaz (07'deki özellik dalı akışı). Bunun
yerine dal GitHub'a gönderilir ve bir **pull request** (PR) açılır: "bu
dalı `main`'e birleştirmek istiyorum, bakar mısınız?"

<figure class="fig">
  <div class="flow">
    <span class="node">Dal + push</span><span class="arrow">→</span>
    <span class="node">PR aç</span><span class="arrow">→</span>
    <span class="node">İnceleme</span><span class="arrow">→</span>
    <span class="node ok">Merge</span><span class="arrow">→</span>
    <span class="node acc">git pull</span>
  </div>
  <figcaption>Pull request'in yaşamı. Gözden geçirmede istenen değişiklikler aynı dala push edilir; PR kendiliğinden güncellenir.</figcaption>
</figure>

### 1. Dalı gönder

```text
~/site (main) $ git switch -c contact-form
Switched to a new branch 'contact-form'
~/site (contact-form) $ echo "<form>" > contact.html
~/site (contact-form) $ git add .
~/site (contact-form) $ git commit -m "Add contact form"
[contact-form 94887a5] Add contact form
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (contact-form) $ git push -u origin contact-form
remote: 
remote: Create a pull request for 'contact-form' on GitHub by visiting:
remote:      https://github.com/ada/site/pull/new/contact-form
remote: 
To https://github.com/ada/site.git
 * [new branch]      contact-form -> contact-form
branch 'contact-form' set up to track 'origin/contact-form'.
```

GitHub yeni dalı görünce `remote:` satırlarında PR açma bağlantısını
veriyor. Depo sayfasında da sarı bir **Compare & pull request** şeridi
çıkar.

### 2. PR'ı aç

Bağlantıya tıklayınca açılan sayfada: hangi dal hangi dala (`base: main` ←
`compare: contact-form`), bir başlık ve açıklama (ne değişti, neden, nasıl
denenir). **Create pull request**.

### 3. Gözden geçirme

Ekip arkadaşların **Files changed** sekmesinde farkı satır satır görür, satıra
yorum yazar, **Approve** (onay) ya da **Request changes** (değişiklik iste)
der. Değişiklik istenirse aynı dalda yeni commit atıp push yaparsın; PR
kendiliğinden güncellenir. Yeni bir PR açılmaz.

### 4. Birleştirme

Onaydan sonra GitHub'da **Merge pull request**. Üç seçenek var:

| Seçenek | Ne yapar |
|---|---|
| **Create a merge commit** | `--no-ff` gibi: dalın commit'leri + birleştirme commit'i. |
| **Squash and merge** | Dalın bütün commit'leri tek bir commit'e sıkıştırılır. |
| **Rebase and merge** | Dalın commit'leri `main`'in ucuna tek tek dizilir (12). |

Ardından GitHub dalı silmeyi önerir (**Delete branch**).

### 5. Kendi bilgisayarını güncelle

Birleştirme GitHub'da oldu; senin bilgisayarın bilmiyor. Yerel tarafı
toplamak:

```text
~/site (contact-form) $ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
~/site (main) $ git pull
From https://github.com/ada/site
   05e1329..312cf67  main       -> origin/main
Updating 05e1329..312cf67
Fast-forward
 contact.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (main) $ git branch -d contact-form
Deleted branch contact-form (was 94887a5).
~/site (main) $ git fetch --prune
From https://github.com/ada/site
 - [deleted]         (none)     -> origin/contact-form
~/site (main) $ git log --format="%h %s" -3
312cf67 Merge pull request #1 from ada/contact-form
94887a5 Add contact form
05e1329 Add home page
~/site (main) $ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

- `git switch main` + `git pull`: birleştirilmiş `main`'i al.
- `git branch -d`: yerel dalı sil (işi artık `main`'de).
- `git fetch --prune`: GitHub'da silinen dalların `origin/...` izlerini
  temizle.

> **Squash and merge** yapıldıysa dalının commit'leri `main`'de **aynen**
> yer almaz (yerine tek bir yeni commit var). Bu yüzden `git branch -d`
> "not fully merged" der; iş gerçekten birleştiyse `-D` ile silersin.

## Fork: başkasının projesine katkı

Yazma iznin olmayan bir depoya (açık kaynak bir proje gibi) doğrudan push
yapamazsın. Bunun yerine **fork**: GitHub'da depo sayfasındaki **Fork**
düğmesi deponun bütün geçmişiyle **kendi hesabındaki** bir kopyasını açar.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>upstream</span><span>github.com/grace/site — orijinal depo. Okuyabilirsin, yazamazsın.</span></div>
    <div class="anat-row"><span>origin</span><span>github.com/ada/site — senin fork'un. Buraya push edersin.</span></div>
    <div class="anat-row"><span>Bilgisayarın</span><span>origin'in klonu. Güncellemeleri upstream'den alır, işini origin'e gönderirsin.</span></div>
  </div>
  <figcaption>Fork akışında iki uzak depo var. PR, fork'undaki daldan orijinal depoya açılır.</figcaption>
</figure>

Akış:

1. Orijinal depoyu fork'la → `github.com/ada/site`.
2. **Kendi fork'unu** klonla (o `origin` olur).
3. Orijinal depoyu `upstream` adıyla ekle: güncellemeleri oradan alacaksın.
4. Dal aç, çalış, kendi fork'una push et.
5. GitHub'da fork'undan orijinal depoya PR aç.

Fork'u güncel tutmak:

```text
~/site (main) $ git remote add upstream https://github.com/grace/site.git
~/site (main) $ git remote -v
origin  https://github.com/ada/site.git (fetch)
origin  https://github.com/ada/site.git (push)
upstream        https://github.com/grace/site.git (fetch)
upstream        https://github.com/grace/site.git (push)
~/site (main) $ git fetch upstream
From https://github.com/grace/site
 * [new branch]      main       -> upstream/main
~/site (main) $ git merge upstream/main
Updating 7446ff5..c1276e9
Fast-forward
 news.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 news.html
~/site (main) $ git push
To https://github.com/ada/site.git
   7446ff5..c1276e9  main -> main
```

## Issue'lar

**Issue** bir hata bildirimi, bir istek ya da bir yapılacak. Her issue'nun bir
numarası var (`#12`). Commit mesajında ya da PR açıklamasında `Fixes #12`
yazarsan PR birleşince issue kendiliğinden kapanır. PR'lar ve issue'lar aynı
numara sırasını paylaşır.

## Birkaç ayar ve araç

- **Collaborators** (Settings): depoya yazma izni verdiğin kişiler.
- **Branch protection**: `main`'e doğrudan push'u kapatır, PR ve onay ister.
- **GitHub Desktop** ve **VS Code**'un Git paneli bu bölümdeki her şeyi
  düğmelerle yapar; arkada aynı komutlar çalışır.
- **`gh`**: GitHub'ın komut satırı aracı (`gh pr create`, `gh repo clone`);
  ayrıca kurulur.

## Özet

- GitHub'da boş depo aç; mevcut bir depoyu göndereceksen README ekleme.
- Pull request: dalı gönder → PR aç → gözden geçir → birleştir → yerelde
  `pull`, `branch -d`, `fetch --prune`.
- Squash'lanmış dalı silmek için `-D`.
- Fork: kendi kopyan (`origin`) + orijinal (`upstream`); güncellemek için
  `fetch upstream`, `merge upstream/main`, `push`.
- `Fixes #12` PR birleşince issue'yu kapatır.
