# Birleştirmek

Bir dalda çalıştın, iş bitti ve beğendin. Şimdi o işi ana dala (`main`)
taşımak istiyorsun. Bunun adı **birleştirmek** (*merge*): bir dalın
commit'lerini başka bir dala katmak.

## Nasıl yapılır?

İki adım; sıra önemli:

1. **Değişikliği alacak** dala geç: `git switch main`.
2. Getirilecek dalı ver: `git merge about`.

"main'e about'u birleştir" diye okunur. Komut bulunduğun dalı değiştirir,
verdiğin dala dokunmaz.

Git iki farklı biçimde birleştirir; hangisinin olacağına geçmişin şekli
karar verir.

## 1. İleri sarma (*fast-forward*)

`about` dalı açıldıktan sonra `main`'de hiç commit atılmadıysa iş kolay:
`main`'in etiketi `about`'un son commit'ine **kaydırılır**. Yeni commit
oluşmaz.

<figure class="fig">
  <div class="flow">
    <span class="node">Add home page<br><small>main (önce)</small></span><span class="arrow">→</span>
    <span class="node acc">Add about page<br><small>about, main (sonra)</small></span>
  </div>
  <figcaption>main ayrıldığı yerde duruyordu; birleştirme yalnızca main etiketini about'un commit'ine kaydırdı.</figcaption>
</figure>

```text
~/site (main) $ git log --oneline --graph --all
* 14643f4 (about) Add about page
* a0cf655 (HEAD -> main) Add home page
~/site (main) $ git merge about
Updating a0cf655..14643f4
Fast-forward
 about.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 about.html
~/site (main) $ git log --oneline --graph --all
* 14643f4 (HEAD -> main, about) Add about page
* a0cf655 Add home page
```

Çıktıdaki `Fast-forward` bunu söylüyor. Geçmiş düz bir çizgi olarak kaldı.

## 2. Üç yönlü birleştirme ve birleştirme commit'i

`contact` dalında çalışırken `main`'de de commit atıldıysa iki dal
**ayrışmıştır**; etiketi kaydırmak `main`'deki işi kaybettirir. Git bu
durumda üç şeye bakar: iki dalın son commit'leri ve ayrıldıkları **ortak
ata** (*merge base*). Sonra ikisinin değişikliklerini birleştiren yeni bir
commit oluşturur: **birleştirme commit'i** (*merge commit*).

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Ortak ata</span><span>Add home page — iki dal buradan ayrıldı.</span></div>
    <div class="anat-row"><span>main'in ucu</span><span>Add styles — main'de sonradan atılan commit.</span></div>
    <div class="anat-row"><span>contact'ın ucu</span><span>Add contact page — dalda atılan commit.</span></div>
    <div class="anat-row"><span>Birleştirme commit'i</span><span>Merge branch 'contact' — iki ebeveyni var, ikisinin değişikliklerini taşır.</span></div>
  </div>
  <figcaption>Üç yönlü birleştirme: Git ortak atadan bu yana iki dalda neyin değiştiğine bakıp ikisini birleştirir.</figcaption>
</figure>

```text
~/site (main) $ git log --oneline --graph --all
* 23a2dc6 (HEAD -> main) Add styles
| * de0737c (contact) Add contact page
|/  
* a0cf655 Add home page
~/site (main) $ git merge contact --no-edit
Merge made by the 'ort' strategy.
 contact.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (main) $ git log --oneline --graph
*   247f509 (HEAD -> main) Merge branch 'contact'
|\  
| * de0737c (contact) Add contact page
* | 23a2dc6 Add styles
|/  
* a0cf655 Add home page
```

Birleştirme commit'inin **iki ebeveyni** var: `main`'in önceki son commit'i
ve `contact`'ın son commit'i. Grafikteki `|\` ve `|/` dalın ayrılıp
birleştiği yerleri gösteriyor.

> **Gerçek terminalde** üç yönlü birleştirmede Git, commit mesajını
> düzenlemen için bir düzenleyici açar; hazır mesaj (`Merge branch
> 'contact'`) çoğu zaman yeterlidir, kaydedip kapatırsın. Düzenleyici
> açılmasın istersen `--no-edit` (hazır mesaj) ya da `-m "mesaj"` yaz.
> Odyssey'nin terminalinde düzenleyici yok; `--no-edit` ya da `-m`
> kullanacağız.

## Her zaman birleştirme commit'i: `--no-ff`

İleri sarma mümkün olsa bile birleştirme commit'i istiyorsan `--no-ff`
(*no fast-forward*). Bazı ekipler bunu sever: grafikte "bu commit'ler bir
dalda yapıldı ve şu anda birleştirildi" bilgisi kalır.

```text
~/site (main) $ git merge --no-ff about --no-edit
Merge made by the 'ort' strategy.
 about.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 about.html
~/site (main) $ git log --oneline --graph
*   8fbaac5 (HEAD -> main) Merge branch 'about'
|\  
| * 14643f4 (about) Add about page
|/  
* a0cf655 Add home page
```

## Zaten birleşmiş

Aynı dalı iki kez birleştirmeye çalışırsan Git yapacak bir şey bulamaz:

```text
~/site (main) $ git merge contact
Already up to date.
```

## Dalını güncel tutmak

Uzun süren bir dalda çalışırken `main` ilerler. Dalın çok geride kalırsa
sonunda birleştirmek zorlaşır. Çözüm, ara sıra **`main`'i kendi dalına
birleştirmek**: aynı komut, ters yönde.

```text
~/site (main) $ git switch feature
Switched to branch 'feature'
~/site (feature) $ git merge main --no-edit
Merge made by the 'ort' strategy.
 news.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 news.txt
~/site (feature) $ git log --oneline --graph
*   82518df (HEAD -> feature) Merge branch 'main'
|\  
| * 5df455c (main) Add news
* | c62bac9 Start feature
|/  
* a0cf655 Add home page
~/site (feature) $ ls
feature.txt  index.html  news.txt
```

Artık `feature` dalı `main`'deki yenilikleri de içeriyor; işine onların
üstünde devam ediyorsun.

## Birleştirdikten sonra

Birleştirme dalı silmez. İşi biten dalları temizlemek iyi bir alışkanlık:

```text
~/site (main) $ git branch --merged
  about
  contact
* main
~/site (main) $ git branch -d about contact
Deleted branch about (was 14643f4).
Deleted branch contact (was d1d3ccd).
~/site (main) $ git branch
* main
  wip
```

`git branch -d` birleştirilmiş dalları sorunsuz siler (`--merged` listesi
silmesi güvenli olanları gösteriyor). Dalın commit'leri kaybolmaz: artık
`main`'in geçmişinde duruyorlar.

## Ya iki dal aynı satırı değiştirdiyse?

Git çoğu durumda iki dalın değişikliklerini kendisi birleştirir: farklı
dosyalar, ya da aynı dosyanın farklı yerleri. Ama iki dal **aynı satırı
farklı biçimde** değiştirdiyse hangisinin doğru olduğunu bilemez ve sana
sorar: buna **çakışma** (*conflict*) denir. Bir sonraki bölümün konusu.

## Özet

- Birleştirmek: değişikliği alacak dala geç, `git merge <dal>`.
- Hedef dal ilerlememişse **ileri sarma**: etiket kayar, yeni commit yok.
- İki dal ayrışmışsa **üç yönlü birleştirme**: iki ebeveynli bir
  birleştirme commit'i oluşur.
- `--no-edit` hazır mesajı kullanır, `-m` kendi mesajını verir, `--no-ff`
  her zaman birleştirme commit'i oluşturur.
- Dalını güncellemek için `main`'i kendi dalına birleştir.
- Birleştirme dalı silmez; `git branch -d` ile temizle.
