# Dosyanın İçine Bakmak

Bir dosyanın içini görmek için şimdiye kadar `cat` kullandık. Kısa dosyalarda
yeterli; ama bir sunucunun kayıt dosyası binlerce satır olabilir ve hepsini
ekrana dökmek hiçbir şey göstermez. Bu bölümde dosyanın **bir kısmına**
bakmayı ve dosyayı **saymayı** öğreneceğiz: `head`, `tail`, `wc` ve gerçek
terminallerdeki `less`.

Örneklerde iki dosya var: kısa bir şiir (`poem.txt`) ve bir sunucunun kayıt
dosyası (`logs/server.log`). Kayıt dosyası (log), bir programın ne yaptığını
satır satır, zamanıyla yazdığı dosyadır.

## Hepsi birden: `cat`

```text
~ $ cat poem.txt
Roses are red
Violets are blue
The shell is fast
And so are you
~ $ cat -n poem.txt
     1  Roses are red
     2  Violets are blue
     3  The shell is fast
     4  And so are you
```

`cat -n` satırların başına numara koyar. "Hata 3. satırda" gibi bir bilgiyle
dosyaya bakarken işe yarar.

On beş satırlık kayıt dosyası bile ekranda epey yer tutuyor:

```text
~ $ cat logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
2026-10-07 10:03 WARN slow request /api/books
2026-10-07 10:04 INFO user alan logged in
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 INFO database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:09 INFO user grace logged in
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:11 INFO backup done
2026-10-07 10:12 INFO user ada logged out
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
```

Bin satırlık bir dosyada ilk satırlar çoktan ekranın yukarısından kayıp
gitmiş olurdu. Çoğu zaman dosyanın tamamına değil, başına ya da sonuna
bakmak istersin.

## Baş ve son: `head` ve `tail`

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>head</h4><p>Baştan 10 satır</p><p><code>head -n 3</code>: ilk 3</p><p>Dosya neyle başlıyor?</p></div>
    <div class="ok"><h4>tail</h4><p>Sondan 10 satır</p><p><code>tail -n 3</code>: son 3</p><p><code>tail -n +5</code>: 5. satırdan sona</p></div>
  </div>
  <figcaption>Büyük bir dosyanın tamamını ekrana dökmek yerine başına ya da sonuna bakarsın. Kayıt dosyalarında en yeni satırlar sondadır.</figcaption>
</figure>

`head` dosyanın başını yazar; seçeneksiz **10** satır. `-n` ile kaç satır
istediğini söylersin (`-n 3` yerine kısaca `-3` de yazılır):

```text
~ $ head logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
2026-10-07 10:03 WARN slow request /api/books
2026-10-07 10:04 INFO user alan logged in
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 INFO database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:09 INFO user grace logged in
~ $ head -n 3 logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
~ $ head -3 poem.txt
Roses are red
Violets are blue
The shell is fast
```

`tail` aynı işi sondan yapar. Sayının önüne `+` koyarsan anlamı değişir:
"son N satır" değil, "N. satırdan sonuna kadar":

```text
~ $ tail -n 3 logs/server.log
2026-10-07 10:12 INFO user ada logged out
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
~ $ tail -n +14 logs/server.log
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
~ $ tail -n 1 poem.txt logs/server.log
==> poem.txt <==
And so are you

==> logs/server.log <==
2026-10-07 10:14 INFO server stopped
```

Birden çok dosya verince `head` ve `tail` her dosyanın önüne
`==> ad <==` başlığını koyar; hangi satırın hangi dosyadan geldiğini
anlarsın.

Kayıt dosyalarında en yeni satırlar **sondadır**, çünkü programlar dosyanın
sonuna ekler. "Az önce ne oldu?" sorusunun ilk cevabı `tail`'dir. Gerçek bir
terminalde `tail -f server.log` (*follow*) dosyayı izlemeye devam eder ve yeni
satırlar geldikçe yazar; `Ctrl+C` ile durur. Bu terminalde dosyalar kendi
kendine büyümediği için `-f` yok.

## Saymak: `wc`

`wc` (*word count*) bir dosyanın satırlarını, kelimelerini ve baytlarını
sayar:

<figure class="fig">
  <pre><code class="language-text"> 15  88 591 logs/server.log</code></pre>
  <div class="anat">
    <div class="anat-row"><span>15</span><span>Satır sayısı (<code>-l</code>, lines).</span></div>
    <div class="anat-row"><span>88</span><span>Kelime sayısı (<code>-w</code>, words): boşluklarla ayrılmış parçalar.</span></div>
    <div class="anat-row"><span>591</span><span>Bayt sayısı (<code>-c</code>): dosyanın boyutu, satır sonları dahil.</span></div>
    <div class="anat-row"><span>logs/server.log</span><span>Sayılan dosya.</span></div>
  </div>
  <figcaption><code>wc</code> (word count) seçeneksiz üçünü de yazar; seçenekle yalnızca istediğini.</figcaption>
</figure>

```text
~ $ wc logs/server.log
 15  88 591 logs/server.log
~ $ wc -l logs/server.log
15 logs/server.log
~ $ wc -w poem.txt
14 poem.txt
~ $ wc -c poem.txt
64 poem.txt
~ $ wc -l poem.txt logs/server.log
  4 poem.txt
 15 logs/server.log
 19 total
```

- `wc -l` yalnızca satır sayısı. En çok kullanılanı bu: "kayıtta kaç satır
  var", "listede kaç kişi var".
- `wc -w` kelime, `wc -c` bayt sayısı. Bayt sayısı `ls -l`'deki boyutla aynı.
- Birden çok dosyada en sona `total` satırı eklenir.

`wc` sonucu verir, dosyanın içini göstermez. Bir dosyayı ekrana dökmeden "ne
kadar büyük" sorusunu cevaplamanın yolu.

## Hatalar

```text
~ $ head -n ten poem.txt
head: invalid number of lines: 'ten'
~ $ tail nope.txt
tail: cannot open 'nope.txt' for reading: No such file or directory
~ $ wc logs
wc: logs: Is a directory
      0       0       0 logs
```

- Satır sayısı rakamla yazılır: `-n 10`, `-n ten` değil.
- `head` ve `tail` dosyayı bulamayınca `cannot open ... for reading` der.
- Klasörün içi okunmaz; `wc` hatayı yazdıktan sonra yine de sıfırlı bir
  satır basar.

## Sayfa sayfa okumak: `less`

Gerçek bir terminalde uzun bir dosyayı okumanın en rahat yolu `less`:

```text
$ less logs/server.log
```

`less` dosyayı ekranı kaplayan bir görünümde açar; ok tuşlarıyla ya da
boşlukla ilerlersin, `/hata` yazıp arama yaparsın, `q` ile çıkarsın. Dosyayı
değiştirmez, yalnızca gösterir. (Adı bir şakadan gelir: daha eski bir
programın adı *more*'du, `less` ondan daha fazlasını yapıyor.)

Odyssey'nin terminali tam ekran program açamadığı için burada `less` yok;
yerine `head`, `tail` ve `cat -n` kullanacaksın. Tuşları ders notunda.

## Özet

| Komut | Ne yapar |
|---|---|
| `cat -n dosya` | Bütün dosya, satır numarasıyla |
| `head dosya` | İlk 10 satır |
| `head -n 3 dosya` | İlk 3 satır |
| `tail -n 3 dosya` | Son 3 satır |
| `tail -n +5 dosya` | 5. satırdan sona |
| `wc dosya` | Satır, kelime, bayt |
| `wc -l dosya` | Yalnızca satır sayısı |
| `less dosya` | Sayfa sayfa okumak (gerçek terminalde) |
