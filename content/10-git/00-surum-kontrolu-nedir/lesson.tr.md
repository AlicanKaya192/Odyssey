# Sürüm Kontrolü Nedir?

Bir proje üzerinde birkaç gün çalıştığını düşün. Klasöre bakınca şunu
görüyorsun:

```text
rapor.docx
rapor_son.docx
rapor_son_v2.docx
rapor_GERCEKTEN_son.docx
rapor_son_v2_hoca_duzeltmeleri.docx
```

Hangisi en yenisi? İkinci sürümle üçüncü arasında ne değişti? Dün sildiğin
paragrafı geri getirmek istersen hangi dosyaya bakacaksın? Bir arkadaşın da
aynı rapor üzerinde çalışıyorsa ikinizin değişikliği nasıl birleşecek?

Kodda bu sorun çok daha büyük. Bir program yüzlerce dosyadan oluşuyor; bir
satırı değiştirmek başka bir yeri bozabiliyor ve "dün çalışıyordu, bugün
neden çalışmıyor?" sorusu her gün soruluyor. **Sürüm kontrolü** bu soruların
hepsine cevap veren yöntemin adı.

## Sürüm kontrolü ne yapar?

Sürüm kontrol sistemi projenin klasörünü izler ve sen istediğinde o anki
hâlinin **fotoğrafını** çeker. Bu fotoğrafa Git'te **commit** deniyor
(Türkçe kaynaklarda "kayıt" ya da "işleme" de dendiğini görürsün; biz
programın kendi kelimesini kullanacağız, çünkü komutlar da öyle).

Her commit dört şeyi saklar:

- **Ne değişti:** hangi dosyada hangi satır eklendi ya da silindi.
- **Kim yaptı:** adın ve e-posta adresin.
- **Ne zaman:** tarih ve saat.
- **Neden:** senin yazdığın kısa bir açıklama, **commit mesajı**.

<figure class="fig">
  <div class="flow">
    <span class="node">commit 1<br><small>"Add readme"</small></span><span class="arrow">→</span>
    <span class="node">commit 2<br><small>"Add contact page"</small></span><span class="arrow">→</span>
    <span class="node">commit 3<br><small>"Fix typo in title"</small></span><span class="arrow">→</span>
    <span class="node acc">şimdi<br><small>klasördeki dosyalar</small></span>
  </div>
  <figcaption>Her commit projenin o anki fotoğrafı ve bir mesaj taşıyor. Herhangi birine geri dönebilirsin.</figcaption>
</figure>

Böylece dosyanın tek bir kopyası klasörde duruyor, geçmişin tamamı ise Git'in
içinde. Klasörü `rapor_son_v2` gibi kopyalarla doldurman gerekmiyor.

Bunun sana kazandırdıkları:

1. **Geri dönebilirsin.** Bir şey bozulursa çalışan son hâle tek komutla
   dönersin.
2. **Ne değiştiğini görürsün.** İki commit arasındaki fark satır satır
   gösterilir.
3. **Rahatça denersin.** Yeni bir fikri ayrı bir **dalda** (branch)
   denersin; beğenmezsen ana çalışmana hiç dokunmadan atarsın.
4. **Birlikte çalışırsın.** Birden fazla kişi aynı projede çalışır, Git
   değişiklikleri birleştirir.

## Git nedir, GitHub nedir?

Bu iki ad çok karıştırılıyor, çünkü ikisi de "Git" ile başlıyor.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Git</h4><p>Bilgisayarında çalışan program</p><p>İnternetsiz çalışır</p><p>commit, dal, geçmiş</p><p><b>Araç</b></p></div>
    <div class="dim"><h4>GitHub</h4><p>İnternetteki bir site</p><p>Depoları saklar ve paylaştırır</p><p>pull request, issue</p><p><b>Depoların durduğu yer</b></p></div>
  </div>
  <figcaption>Git olmadan GitHub'ın bir anlamı yok; GitHub olmadan da Git tek başına çalışır.</figcaption>
</figure>

**Git** senin bilgisayarında çalışan bir programdır. 2005'te Linus Torvalds
tarafından Linux çekirdeğinin geliştirilmesi için yazıldı ve bugün yazılım
dünyasının neredeyse tamamı onu kullanıyor. İnternet olmadan da çalışır:
commit atmak, geçmişe bakmak, dal açmak tamamen senin bilgisayarında olur.

**GitHub** ise Git depolarını internette saklayan bir sitedir. Projeni oraya
gönderirsin, başkaları görür, indirir, katkıda bulunur. GitLab ve Bitbucket
da aynı işi yapan başka sitelerdir. Kısaca: **Git araç, GitHub o aracın
ürettiği depoların durduğu yer.**

## Depo (repository)

Git'in izlediği klasöre **depo** (repository, kısaca *repo*) deniyor. Bir
klasörü depoya çevirdiğinde Git içine `.git` adında gizli bir klasör açar.
Bütün geçmiş, bütün commit'ler, dallar ve ayarlar oradadır.

> `.git` klasörünü elle düzenleme ve silme. Silersen klasördeki dosyalar
> yerinde kalır ama geçmişin tamamı gider: o klasör yeniden sıradan bir
> klasör olur.

## Neden terminal?

Git'in asıl yüzü **komut satırıdır** (terminal). VS Code'un içindeki Git
paneli, GitHub Desktop gibi görsel araçlar da arka planda aynı komutları
çalıştırır. Komutları bilen biri:

- her aracı ve her bilgisayarı kullanabilir,
- hata mesajlarını anlar (mesajlar komutların dilinde yazılır),
- internette bulduğu çözümleri uygulayabilir (hemen hepsi komut olarak
  yazılmıştır).

Bu yüzden bu patikada Git'i terminalden öğreneceğiz. Windows'ta Git ile
birlikte gelen **Git Bash** terminalini, Mac ve Linux'ta sistemin kendi
terminalini kullanırsın; komutlar üçünde de aynıdır.

## Terminali okumak

Terminal seni her satırda bir **istemle** (prompt) karşılar. İstem "yazmaya
hazırım" demektir ve sana nerede olduğunu söyler:

<figure class="fig">
  <pre><code class="language-text">~/notes (main) $ git status</code></pre>
  <div class="anat">
    <div class="anat-row"><span>~</span><span>Ev klasörün (Git Bash'te genellikle /c/Users/adın). Her yolun başı.</span></div>
    <div class="anat-row"><span>/notes</span><span>Şu an içinde bulunduğun klasör.</span></div>
    <div class="anat-row"><span>(main)</span><span>Bir Git deposunun içindeysen bulunduğun dal. Depo dışında görünmez.</span></div>
    <div class="anat-row"><span>$</span><span>Komut bekliyorum. Sen bundan sonrasını yazarsın.</span></div>
    <div class="anat-row"><span>git status</span><span>Senin yazdığın komut.</span></div>
  </div>
  <figcaption>İstem sana her satırda nerede olduğunu söylüyor. Ders örneklerinde $ ile başlayan satırlar yazdığın komutlar.</figcaption>
</figure>

`$` işaretinden sonra komutunu yazar ve **Enter**'a basarsın. Komutun
çıktısı alt satırlara yazılır, sonra yeni bir istem gelir.

## İlk komutlar

Git'e geçmeden önce terminalde dolaşmayı öğrenmen gerekiyor: nerede
olduğunu görmek, klasör açmak, dosya oluşturmak. Hepsi Git ile çalışırken
sürekli kullanacağın komutlar.

| Komut | Ne yapar |
|---|---|
| `pwd` | Şu an hangi klasörde olduğunu yazar (*print working directory*). |
| `ls` | Bulunduğun klasördeki dosyaları ve klasörleri listeler. |
| `ls -a` | Gizli olanlarla (`.` ile başlayanlar) birlikte listeler. |
| `mkdir notes` | `notes` adında yeni bir klasör açar (*make directory*). |
| `cd notes` | `notes` klasörüne girer (*change directory*). |
| `cd ..` | Bir üst klasöre çıkar. |
| `cd ~` | Ev klasörüne döner. |
| `echo "Hi" > a.txt` | `a.txt` dosyasını yazar (varsa içeriği silinip yeniden yazılır). |
| `echo "Hi" >> a.txt` | `a.txt` dosyasının sonuna satır ekler. |
| `cat a.txt` | Dosyanın içeriğini ekrana yazar. |
| `rm a.txt` | Dosyayı siler (geri dönüşüm kutusuna gitmez). |

Bir örnek oturum:

```text
~ $ pwd
/home/ada
~ $ mkdir notes
~ $ ls
notes/
~ $ cd notes
~/notes $ pwd
/home/ada/notes
~/notes $ echo "Buy milk" > todo.txt
~/notes $ echo "Call Ada" >> todo.txt
~/notes $ cat todo.txt
Buy milk
Call Ada
~/notes $ ls
todo.txt
```

Birkaç şeye dikkat et:

- `mkdir` ve `cd` başarılı olunca **hiçbir şey yazmaz**. Terminalde sessizlik
  çoğu zaman "tamam" demektir.
- `ls` klasörlerin sonuna `/` koyar; dosyaları klasörlerden böyle ayırırsın.
- `cd notes`'tan sonra istem `~/notes $` oldu: artık oradasın.
- `>` dosyayı baştan yazar, `>>` sonuna ekler. İkisini karıştırırsan
  dosyadaki her şey gider; `>` yazmadan önce bir kez düşün.

## Odyssey'deki terminal

Bu patikanın alıştırmalarında kod yazmayacaksın; **terminale komut
yazacaksın**. Alıştırmanın sağında bir terminal açılıyor:

- Üstte **hedefler** var. Her komuttan sonra kontrol ediliyor; tutan hedefin
  yanına ✓ geliyor. Hepsi tutunca alıştırma çözülüyor.
- Komutlar gerçek Git gibi davranıyor ve çıktılar gerçek Git'in çıktılarıyla
  aynı, ama **bilgisayarındaki dosyalara dokunmuyor**. Bilgisayarında Git
  kurulu olmasa da alıştırmalar çalışır.
- Terminal Ada Lovelace adlı hayalî bir kullanıcının bilgisayarında
  açılıyor: ev klasörü `/home/ada`. Kendi bilgisayarında bu yol farklı olur
  (Git Bash'te `/c/Users/adın`), komutlar aynı.
- Klavyede ↑ tuşu önceki komutu getirir; aynı komutu yeniden yazmana gerek
  kalmaz.
- Bir şeyi bozarsan **Baştan başla** düğmesi alıştırmayı ilk hâline
  döndürür.

## İlk tadım: `git init`

Bir klasörü depoya çevirmek tek komut: `git init` (*initialize*, başlat).
Önce Git'in kurulu olduğunu `git --version` ile görelim:

```text
~/notes $ git --version
git version 2.55.0
~/notes $ ls -a
.  ..
~/notes $ git init
Initialized empty Git repository in /home/ada/notes/.git/
~/notes (main) $ ls -a
.  ..  .git/
```

Üç şey değişti:

1. Git klasörde boş bir depo oluşturduğunu söyledi.
2. `ls -a` artık gizli `.git/` klasörünü gösteriyor; geçmiş orada duracak.
3. İstemin sonuna **`(main)`** geldi. Bu, şu an `main` adlı **dalda**
   olduğunu söylüyor. Dalları ileride ayrıntılı göreceğiz; şimdilik "depo
   içindeyim" işareti olarak bil.

Depo hâlâ boş: henüz hiçbir commit yok. İlk commit'i iki bölüm sonra
atacağız; önce gerçek bilgisayarına Git'i kurup ayarlarını yapacağız.

## Özet

- **Sürüm kontrolü** projenin geçmişini tutar: ne, kim, ne zaman, neden.
- Git'te geçmişin her adımına **commit** denir; her commit'in bir mesajı
  vardır.
- **Git** bilgisayarında çalışan programdır, **GitHub** depoların internette
  durduğu sitedir.
- Git'in izlediği klasör **depo**dur; geçmiş gizli `.git` klasöründedir.
- Terminalde `pwd`, `ls`, `cd`, `mkdir`, `echo`, `cat`, `rm` ile dolaşırsın.
- `git init` bir klasörü depoya çevirir.
