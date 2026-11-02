# Yönlendirme: Çıktıyı Dosyaya Göndermek

Dosya Oluşturmak bölümünde `echo "metin" > dosya` yazdık ve metin ekran
yerine dosyaya gitti. Bu, kabuğun en güçlü özelliklerinden birinin ilk
örneğiydi: **yönlendirme** (redirection). Herhangi bir komutun çıktısını bir
dosyaya gönderebilir, hata mesajlarını ayırabilir, girdiyi bir dosyadan
verebilirsin. Bu bölümde hepsini sırayla göreceğiz.

## Üç akış

Her komutun üç **akışı** (stream) vardır. Akış, verinin aktığı bir kanal
gibi düşünülebilir:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>0 stdin</span><span><b>Standart girdi</b>: komutun okuduğu yer. Normalde klavye; <code>&lt;</code> ile bir dosya.</span></div>
    <div class="anat-row"><span>1 stdout</span><span><b>Standart çıktı</b>: komutun asıl sonucu. Normalde ekran; <code>&gt;</code> ile bir dosya.</span></div>
    <div class="anat-row"><span>2 stderr</span><span><b>Standart hata</b>: hata mesajları. O da normalde ekran; <code>2&gt;</code> ile bir dosya.</span></div>
  </div>
  <figcaption>Her komutun üç akışı vardır. Ekranda stdout ile stderr karışık görünür ama ayrı kanallardır; yönlendirme onları ayırır.</figcaption>
</figure>

Ekranda bir komutun çıktısı ile hata mesajı alt alta görünür, ama kabuğun
gözünde ikisi farklı kanallardan gelir. Yönlendirme bu kanalları ekran
yerine dosyalara bağlar.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>&gt; dosya</span><span>stdout dosyaya; dosya <b>baştan yazılır</b>.</span></div>
    <div class="anat-row"><span>&gt;&gt; dosya</span><span>stdout dosyanın <b>sonuna eklenir</b>.</span></div>
    <div class="anat-row"><span>2&gt; dosya</span><span>Yalnızca hata mesajları dosyaya.</span></div>
    <div class="anat-row"><span>&gt; dosya 2&gt;&amp;1</span><span>İkisi aynı dosyaya (önce <code>&gt;</code>, sonra <code>2&gt;&amp;1</code>).</span></div>
    <div class="anat-row"><span>&amp;&gt; dosya</span><span>bash'te aynısının kısa yazılışı.</span></div>
    <div class="anat-row"><span>&lt; dosya</span><span>Komut girdisini klavye yerine dosyadan okur.</span></div>
    <div class="anat-row"><span>/dev/null</span><span>"Hiçlik" dosyası: buraya gönderilen her şey kaybolur.</span></div>
  </div>
  <figcaption>Yönlendirme komutun sonuna yazılır ve komutun kendisi bundan habersizdir; işi kabuk yapar.</figcaption>
</figure>

## Çıktıyı dosyaya: `>`

```text
~ $ ls notes
ideas.txt  todo.txt
~ $ ls notes > list.txt
~ $ cat list.txt
ideas.txt
todo.txt
~ $ date > today.txt
~ $ cat today.txt
Wed Oct  7 10:00:00 +03 2026
```

`ls notes > list.txt` ekrana hiçbir şey yazmadı; liste dosyaya gitti. Dosyada
adlar ayrı satırlarda, çünkü `ls` çıktısı ekrana değil dosyaya giderken her
adı ayrı satıra yazar. `date` komutu o anın tarihini yazar; onu da dosyaya
gönderebildik. Yönlendirme **her** komutla çalışır, çünkü işi komut değil
kabuk yapar.

## Sona eklemek: `>>`

```text
~ $ echo "first run" > run.log
~ $ echo "second run" >> run.log
~ $ cat run.log
first run
second run
~ $ echo "oops" > run.log
~ $ cat run.log
oops
```

`>` dosyayı her seferinde baştan yazar; `>>` sonuna ekler. Bir betiğin her
çalışmasını bir kayıt dosyasına not etmek gibi işlerde hep `>>` kullanılır.

## Hataları ayırmak: `2>`

`>` yalnızca stdout'u yönlendirir. Hata mesajları stderr'den geldiği için
ekranda kalır:

```text
~ $ ls notes nope
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt  todo.txt
~ $ ls notes nope > out.txt
ls: cannot access 'nope': No such file or directory
~ $ cat out.txt
notes:
ideas.txt
todo.txt
~ $ ls notes nope 2> errors.txt
notes:
ideas.txt  todo.txt
~ $ cat errors.txt
ls: cannot access 'nope': No such file or directory
```

- `> out.txt` listeyi dosyaya yazdı, hata yine ekranda göründü.
- `2> errors.txt` yalnızca hatayı dosyaya yazdı; liste ekranda kaldı.

`2`, stderr'in numarası. `>` aslında `1>`'in kısa yazılışı.

## İkisi birden: `2>&1` ve `&>`

Çıktıyı ve hataları **aynı** dosyada toplamak için önce stdout'u dosyaya
gönderir, sonra stderr'i "stdout'un gittiği yere" bağlarsın:

```text
~ $ ls notes nope > all.txt 2>&1
~ $ cat all.txt
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt
todo.txt
~ $ ls notes nope &> all2.txt
~ $ cat all2.txt
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt
todo.txt
```

`2>&1` "2 numarayı 1 numaranın gittiği yere gönder" demek. Baştaki `&`,
`1`'in bir dosya adı değil akış numarası olduğunu söyler; `2>1` yazsaydın
adı `1` olan bir dosya oluşurdu. Sıra önemli: önce `> dosya`, sonra `2>&1`.
bash'te aynı işin kısa yolu `&> dosya`.

## Hiçliğe göndermek: `/dev/null`

`/dev/null` özel bir dosyadır: içine yazılan her şey kaybolur, okunduğunda
hiçbir şey vermez. Görmek istemediğin çıktıyı oraya gönderirsin:

```text
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ ls nope 2> /dev/null
~ $ ls notes > /dev/null
~ $ cat /dev/null
```

Komut yine çalıştı ve çıkış kodu değişmedi; yalnızca mesajı görmedik.
Betiklerde "hata çıkarsa ekrana basma" demenin yolu `2> /dev/null`.

## Girdiyi dosyadan: `<`

`<` ters yönde çalışır: komut girdisini klavye yerine dosyadan okur.

```text
~ $ sort names.txt
ada
alan
grace
linus
~ $ sort < names.txt
ada
alan
grace
linus
~ $ wc -l names.txt
4 names.txt
~ $ wc -l < names.txt
4
~ $ sort < names.txt > sorted.txt
~ $ cat sorted.txt
ada
alan
grace
linus
```

`sort names.txt` ile `sort < names.txt` aynı sonucu verdi: birinde dosyayı
`sort` açtı, ötekinde kabuk açıp içeriğini `sort`'a verdi. Fark `wc`'de
görünüyor: `<` ile `wc` dosyanın adını bilmediği için yalnızca sayıyı yazdı.
Sayıyı bir betikte kullanacaksan bu çok işe yarar. Aynı satırda hem `<` hem
`>` olabilir.

## Tuzaklar

```text
~ $ ls nope > empty.txt
ls: cannot access 'nope': No such file or directory
~ $ cat empty.txt
~ $ wc -c empty.txt
0 empty.txt
~ $ echo hi > nowhere/x.txt
bash: nowhere/x.txt: No such file or directory
~ $ echo hi > notes
bash: notes: Is a directory
```

- **Dosya komut çalışmadan önce açılır.** `ls nope > empty.txt` başarısız
  oldu, ama `empty.txt` yine de oluştu ve boş. Bu yüzden
  `sort names.txt > names.txt` asla yazılmaz: kabuk `names.txt`'yi `sort`
  okumadan önce boşaltır ve dosya kaybolur. Sonucu başka bir dosyaya yaz.
- `>` klasör açmaz: hedef klasör yoksa hatayı **kabuk** yazar (`bash: ...`).
- Bir klasörün üstüne yazılamaz: `Is a directory`.

## Özet

| Yazım | Ne yapar |
|---|---|
| `komut > dosya` | stdout dosyaya, dosya baştan yazılır |
| `komut >> dosya` | stdout dosyanın sonuna |
| `komut 2> dosya` | Yalnızca hatalar dosyaya |
| `komut > dosya 2>&1` | İkisi aynı dosyaya (`&> dosya`) |
| `komut 2> /dev/null` | Hataları yok et |
| `komut < dosya` | Girdiyi dosyadan oku |
| `komut < girdi > çıktı` | İkisi birden |

Yönlendirmeyi kabuk yapar, bu yüzden her komutla çalışır. Okuduğun dosyaya
aynı komutta `>` ile yazma.
