# Borular: Komutları Birbirine Bağlamak

Yönlendirme bölümünde bir komutun çıktısını bir **dosyaya** gönderdik. Bu
bölümde çıktıyı başka bir **komuta** göndereceğiz. Bunu yapan işaret `|`;
adı **boru** (pipe). Komut satırını gerçekten güçlü yapan şey budur: her biri
tek bir işi iyi yapan küçük komutları uç uca ekleyip büyük işler kurarsın.

## İlk boru

```text
~ $ ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ ls docs | wc -l
5
~ $ cat names.txt
grace
ada
linus
alan
margaret
katherine
dennis
~ $ cat names.txt | sort
ada
alan
dennis
grace
katherine
linus
margaret
```

`ls docs | wc -l` iki komut çalıştırdı. `ls docs` ekrana yazacağı listeyi
ekran yerine boruya verdi; `wc -l` o listeyi girdi olarak okudu ve satırlarını
saydı. Sonuç: `docs` klasöründe 5 dosya var. `cat names.txt | sort` da aynı
şekilde: `cat` adları borudan `sort`'a verdi, `sort` sıraladı.

<figure class="fig">
  <div class="flow">
    <span class="node">cat names.txt<br><small>7 adı yazar</small></span><span class="arrow">→</span>
    <span class="node acc">sort<br><small>sıralar</small></span><span class="arrow">→</span>
    <span class="node acc">head -n 3<br><small>ilk 3'ü bırakır</small></span><span class="arrow">→</span>
    <span class="node">Ekran<br><small>ada, alan, dennis</small></span>
  </div>
  <figcaption>Boru (<code>|</code>) soldaki komutun stdout'unu sağdakinin stdin'ine bağlar. Aradaki sonuçlar hiçbir dosyaya yazılmaz.</figcaption>
</figure>

Boru, soldaki komutun **stdout**'unu sağdaki komutun **stdin**'ine bağlar.
Yönlendirme bölümündeki akışları hatırla: 1 numara (stdout) bir sonraki
komutun 0 numarasına (stdin) akar. Aradaki sonuçlar hiçbir dosyaya yazılmaz.

## Zincir kurmak

Bir boruya istediğin kadar komut ekleyebilirsin:

```text
~ $ cat names.txt | sort | head -n 3
ada
alan
dennis
~ $ sort names.txt | tail -n 2
linus
margaret
~ $ head -n 6 logs/app.log | tail -n 3
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 info database ok
```

- `cat names.txt | sort | head -n 3`: oku, sırala, ilk üçü bırak.
- `sort names.txt | tail -n 2`: `sort` dosyayı kendisi de açabilir; o zaman
  baştaki `cat`'e gerek yok.
- `head -n 6 logs/app.log | tail -n 3`: ilk altı satırın son üçü, yani
  dosyanın 4., 5. ve 6. satırları. Ne `head` ne `tail` bunu tek başına yapar;
  ikisi birlikte yapar.

Bir zincir kurarken her `|`'den sonra çalıştırıp çıktıya bak. Bir adım yanlış
gittiyse hangisi olduğunu hemen görürsün.

## Borudaki `ls` tek sütun yazar

```text
~ $ ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ ls docs | cat
a.md
b.md
c.md
d.txt
e.txt
~ $ ls docs | head -n 2
a.md
b.md
```

Ekranda `ls` adları yan yana dizer. Çıktısı boruya (ya da dosyaya) gidince her
adı **ayrı bir satıra** yazar; çünkü bir sonraki komut satır satır okur.
`ls docs | wc -l`'nin dosya sayısını vermesi bu yüzden.

## Süzmek: borunun içinde `grep`

`grep kelime` girdisinde o kelimenin geçtiği satırları bırakır, ötekileri
atar. Ayrıntısı bir sonraki bölümde; burada boruda nasıl kullanıldığına
bakalım:

```text
~ $ ls docs | grep md
a.md
b.md
c.md
~ $ grep ERROR logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
~ $ grep ERROR logs/app.log | wc -l
2
```

`ls docs | grep md` yalnızca adında `md` geçenleri bıraktı. Son satır çok
sık kullanılan bir kalıp: önce **süz**, sonra **say**. Kayıt dosyasında kaç
hata olduğunu böyle bulursun.

## Boru yalnızca stdout'u taşır

```text
~ $ ls docs nope | wc -l
ls: cannot access 'nope': No such file or directory
6
~ $ ls docs nope 2>&1 | wc -l
7
~ $ ls docs nope 2> /dev/null | wc -l
6
```

- `ls docs nope | wc -l`: hata mesajı yine ekranda göründü ve sayılmadı.
  `wc` `6` dedi: iki ad verildiği için `ls` önce `docs:` başlığını, sonra beş
  adı yazdı.
- `2>&1 |`: önce stderr'i stdout'a bağla, sonra boruya ver. Hata satırı da
  sayıldı: `7`.
- `2> /dev/null |`: hatayı yok et, yalnızca listeyi işle.

## Boru ve yönlendirme birlikte

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Boru <code>|</code></h4><p>Sağında bir <b>komut</b> durur</p><p><code>sort names.txt | head -n 3</code></p><p>Çıktı başka bir programa gider</p></div>
    <div class="ok"><h4>Yönlendirme <code>&gt;</code></h4><p>Sağında bir <b>dosya</b> durur</p><p><code>sort names.txt &gt; sorted.txt</code></p><p>Çıktı bir dosyaya yazılır</p></div>
  </div>
  <figcaption>İkisi birlikte de kullanılır: önce borularla işlenir, en sonda <code>&gt;</code> ile kaydedilir.</figcaption>
</figure>

```text
~ $ sort names.txt | head -n 3 > top.txt
~ $ cat top.txt
ada
alan
dennis
~ $ cat -n poem.txt | tail -n 2
     3  The shell is fast
     4  And so are you
```

`>` her zaman satırın **sonundaki** komutun çıktısını yakalar. Son komutta
sıra önemli: önce `cat -n` numaraladı, sonra `tail` kesti; bu yüzden
numaralar şiirdeki gerçek yerleri (3 ve 4) gösteriyor.

Gerçek bir terminalde çıktıyı hem görmek hem kaydetmek için `tee` kullanılır:
`sort names.txt | tee sorted.txt` sonucu ekrana yazar **ve** dosyaya kaydeder.
Bu terminalde `tee` yok; aynı işi `> dosya` ve ardından `cat dosya` ile yaparsın.

## Tuzaklar

```text
~ $ echo names.txt | cat
names.txt
~ $ echo names.txt | ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ wc -l names.txt
7 names.txt
~ $ cat names.txt | wc -l
7
```

- **Boru metni taşır, dosya adını değil.** `echo names.txt | cat`, dosyanın
  içini değil `names.txt` yazısını basar.
- **Her komut girdisini okumaz.** `ls`, `cd`, `mkdir` borudan gelen metne
  bakmaz; `echo names.txt | ls docs` yalnızca `docs`'u listeler ve gelen metin
  kaybolur.
- Borudan gelen metnin adı yoktur: `cat names.txt | wc -l` yalnızca sayıyı
  yazar.
- Borunun sağına dosya yazılmaz: `sort names.txt | top.txt` kabuğun `top.txt`
  adında bir **program** aramasına yol açar. Dosya için `>`.

## Özet

- `komut1 | komut2`: komut1'in çıktısı komut2'nin girdisi olur.
- Ekranda yalnızca son komutun çıktısı (ve hatalar) görünür.
- Boruda `ls` her adı ayrı satıra yazar.
- Boru stderr'i taşımaz; taşıması için `2>&1 |`.
- Kaydetmek için satırın sonuna `> dosya`.
- Zinciri adım adım kur, her adımda çıktıya bak.
