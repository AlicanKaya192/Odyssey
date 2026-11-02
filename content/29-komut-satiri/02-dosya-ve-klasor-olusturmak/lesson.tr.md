# Dosya ve Klasör Oluşturmak

Artık dosya sisteminde dolaşabiliyorsun. Sırada kendi klasörlerini ve
dosyalarını oluşturmak var: bir proje için klasör iskeleti kurmak, boş
dosyalar açmak, bir dosyaya birkaç satır yazmak ve yazdığını okumak. Bu
bölümün komutları `mkdir`, `touch`, `echo` ile `>`, `cat` ve `rmdir`.

## Klasör açmak: `mkdir`

`mkdir` (*make directory*) yeni bir klasör açar. Birden çok ad verirsen
hepsini açar:

```text
~ $ mkdir blog
~ $ ls
blog/
~ $ mkdir blog/posts blog/images
~ $ ls blog
images/  posts/
~ $ mkdir blog
mkdir: cannot create directory 'blog': File exists
~ $ mkdir site/css
mkdir: cannot create directory 'site/css': No such file or directory
~ $ mkdir -p site/css
~ $ ls site
css/
~ $ mkdir -p site/css
```

Üç şeye dikkat:

1. Başarılı olunca **hiçbir şey yazmadı**. Terminalde sessizlik çoğu zaman
   "tamam" demektir; emin olmak için `ls` ile bakarsın.
2. Var olan bir klasörü yeniden açmaya çalışınca `File exists` dedi. Eski
   klasöre dokunmadı.
3. `mkdir site/css` hata verdi, çünkü `site` henüz yoktu: `mkdir` yolun
   **son** klasörünü açar, üsttekileri kendiliğinden açmaz.

İç içe klasörler için `-p` (*parents*) seçeneği var:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>mkdir site/css</h4><p><code>site</code> yoksa hata verir</p><p>Yalnızca son klasörü açar</p><p>Klasör zaten varsa: <code>File exists</code></p></div>
    <div class="ok"><h4>mkdir -p site/css</h4><p>Eksik olan bütün klasörleri açar</p><p><code>site</code>, sonra <code>css</code></p><p>Zaten varsa sessizce geçer</p></div>
  </div>
  <figcaption><code>-p</code> (parents): yolun üstündeki klasörler de yoksa onları da aç.</figcaption>
</figure>

`-p` ile aynı komutu ikinci kez çalıştırınca da hata gelmedi. Bu yüzden
betiklerde çoğu zaman `mkdir -p` yazılır: klasör varsa da yoksa da sonuç
aynıdır.

## Boş dosya oluşturmak: `touch`

`touch` verdiğin adda **boş** bir dosya oluşturur:

```text
~/notes $ touch todo.txt
~/notes $ ls
todo.txt
~/notes $ cat todo.txt
~/notes $ touch a.txt b.txt c.txt
~/notes $ ls
a.txt  b.txt  c.txt  todo.txt
```

`cat todo.txt` hiçbir şey yazmadı, çünkü dosya boş. Dosya zaten varsa
`touch` içeriğine dokunmaz; yalnızca "son değiştirilme zamanını" günceller.
Adı da buradan geliyor: dosyaya dokunur geçer.

## Dosyaya yazmak: `echo` ve `>`

İçinde yazı olan bir dosyayı en kolay `echo` ile oluşturursun. `echo` normalde
metni ekrana yazar; sonuna `> dosya` eklersen yazdığı şey ekran yerine
**dosyaya** gider:

<figure class="fig">
  <pre><code class="language-text">echo "Buy milk" &gt; list.txt</code></pre>
  <div class="anat">
    <div class="anat-row"><span>echo</span><span>Metni yazan komut.</span></div>
    <div class="anat-row"><span>"Buy milk"</span><span>Yazılacak metin.</span></div>
    <div class="anat-row"><span>&gt;</span><span>Çıktıyı ekrana değil dosyaya gönder. Dosya yoksa açılır, varsa <b>içi silinip</b> baştan yazılır.</span></div>
    <div class="anat-row"><span>&gt;&gt;</span><span>(&gt; yerine) Dosyanın <b>sonuna ekle</b>; eski içerik kalır.</span></div>
    <div class="anat-row"><span>list.txt</span><span>Çıktının gideceği dosya.</span></div>
  </div>
  <figcaption>Komutun ekrana yazacağı şey <code>&gt;</code> ile bir dosyaya akar. Yönlendirmenin bütün ayrıntıları ileride kendi bölümünde.</figcaption>
</figure>

```text
~/notes $ echo "Buy milk" > list.txt
~/notes $ cat list.txt
Buy milk
~/notes $ echo "Call Ada" >> list.txt
~/notes $ cat list.txt
Buy milk
Call Ada
~/notes $ echo "Oops" > list.txt
~/notes $ cat list.txt
Oops
```

Son iki komuta iyi bak: `>` dosyanın içini **sormadan siler** ve baştan
yazar. "Buy milk" ve "Call Ada" gitti, yalnızca "Oops" kaldı. Bir dosyanın
sonuna ekleyeceksen her zaman `>>`.

Bu terminalde metin düzenleyici (nano, vim) yok; dosyaları `echo` ile satır
satır yazacaksın. Gerçek bir Linux'ta da bu yöntem kısa dosyalar ve betikler
için sık kullanılır.

## Dosyayı okumak: `cat`

`cat` dosyanın içini ekrana yazar. Birden çok dosya verirsen hepsini art arda
yazar; adı da İngilizce *concatenate* (art arda eklemek) kelimesinden geliyor:

```text
~/notes $ cat shop.txt calls.txt
Buy milk
Call Ada
~/notes $ cat shop.txt nope.txt
Buy milk
cat: nope.txt: No such file or directory
~/notes $ cat -n shop.txt calls.txt
     1  Buy milk
     2  Call Ada
```

Bulamadığı dosya için hata yazdı ama ötekini yine yazdı. `-n` seçeneği
satırların başına numara koyar; numaralar iki dosya boyunca devam etti.

## Boş klasörü silmek: `rmdir`

`rmdir` (*remove directory*) bir klasörü siler, ama **yalnızca boşsa**:

```text
~ $ mkdir empty
~ $ rmdir empty
~ $ ls
~ $ mkdir full
~ $ touch full/a.txt
~ $ rmdir full
rmdir: failed to remove 'full': Directory not empty
~ $ rmdir nope
rmdir: failed to remove 'nope': No such file or directory
```

İçi dolu bir klasörü `rmdir` silmez; bu bir güvenlik. İçindekilerle birlikte
silmenin yolu bir sonraki bölümde (`rm -r`), dikkat gerektiren bir komut
olduğu için ayrıca anlatılıyor.

## Gizli dosyalar

Linux'ta bir dosyayı ya da klasörü gizli yapmak için adını **nokta** ile
başlatman yeter. Gizli olmanın tek anlamı, normal `ls`'in onu göstermemesi:

```text
~/notes $ touch .secret
~/notes $ ls
~/notes $ ls -a
./  ../  .secret
```

Programlar ayarlarını çoğu zaman böyle dosyalarda tutar: ev klasöründeki
`.bashrc` bash'in ayarları, bir projedeki `.gitignore` Git'in.

## Dosya adları

```text
~/notes $ touch "my file.txt"
~/notes $ touch my-file.txt
~/notes $ touch Report.txt report.txt
~/notes $ ls
Report.txt  my file.txt  my-file.txt  report.txt
~/notes $ cat my file.txt
cat: my: No such file or directory
cat: file.txt: No such file or directory
```

Bu örnek üç kuralı birden gösteriyor:

- **Boşluk** argümanları ayırır. `cat my file.txt` iki ayrı dosya aradı. Adında
  boşluk olan dosyayı tırnakla yazarsın; ama en iyisi baştan `-` ya da `_`
  kullanmak.
- **Büyük ve küçük harf** farklıdır: `Report.txt` ile `report.txt` iki ayrı
  dosya. (`ls` büyük harfle başlayanları önce dizdi.)
- **Uzantı** (`.txt`, `.md`) adın bir parçasıdır. Linux dosyanın ne olduğuna
  uzantıya bakarak karar vermez; uzantı insanlar ve programlar için bir
  ipucudur.

## Özet

- `mkdir a b` klasör açar; iç içe için `mkdir -p a/b/c`.
- `touch dosya` boş dosya oluşturur, var olana dokunmaz.
- `echo "metin" > dosya` dosyayı baştan yazar; `>>` sonuna ekler.
- `cat dosya` içini yazar; `cat -n` satır numarasıyla.
- `rmdir klasör` yalnızca boş klasörü siler.
- Adı noktayla başlayan dosya gizlidir; `ls -a` gösterir.
- Adlarda boşluk yerine `-` ya da `_`; büyük-küçük harf önemli.
