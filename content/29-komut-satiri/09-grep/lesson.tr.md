# grep ile Metin Aramak

Bir kayıt dosyası binlerce satır olabilir; içinden yalnızca hata satırlarını
görmek istersin. Bir projede bir fonksiyonun adının hangi dosyalarda geçtiğini
bulmak istersin. İkisinin de cevabı `grep`. Adı eski bir düzenleyici
komutundan gelir (*global regular expression print*); bugün komut satırında en
çok kullanılan araçlardan biri.

## Satırları süzmek

<figure class="fig">
  <pre><code class="language-text">grep -i -n error logs/app.log</code></pre>
  <div class="anat">
    <div class="anat-row"><span>grep</span><span>Komut: satır satır okur, deseni taşıyan satırları yazar.</span></div>
    <div class="anat-row"><span>-i -n</span><span>Seçenekler: büyük/küçük harf fark etmesin, satır numarasını yaz.</span></div>
    <div class="anat-row"><span>error</span><span><b>Desen</b>: aranan metin. Her zaman ilk argüman.</span></div>
    <div class="anat-row"><span>logs/app.log</span><span>Aranacak dosya(lar). Verilmezse grep girdisini okur (boru).</span></div>
  </div>
  <figcaption>Önce desen, sonra dosyalar. İkinci kelimeden sonrası hep dosya adı sayılır.</figcaption>
</figure>

```text
~ $ grep ERROR logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
~ $ grep database logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 info database ok
~ $ grep nothing logs/app.log
~ $ echo $?
1
```

`grep` dosyayı satır satır okur ve deseni taşıyan satırları **olduğu gibi**
yazar. Hiçbir satır bulamazsa hiçbir şey yazmaz; ama çıkış kodu söyler:

- `0`: en az bir satır buldu,
- `1`: hiç bulamadı,
- `2`: bir hata oldu (dosya yok gibi).

Betiklerde "bu dosyada hata var mı" sorusu bu kodla sorulur.

## Büyük ve küçük harf: `-i`

```text
~ $ grep error logs/app.log
~ $ grep -i error logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:13 Error timeout while sending mail
```

`grep` harf büyüklüğüne **duyarlıdır**: `error` aramak `ERROR`'u bulmaz. `-i`
(*ignore case*) farkı kapatır; üç biçim de (`ERROR`, `Error`) bulundu. Gerçek
kayıt dosyalarında yazım çoğu zaman tutarsızdır, bu yüzden `-i` çok sık
kullanılır.

## Numara, sayı, tersi: `-n`, `-c`, `-v`

```text
~ $ grep -n WARN logs/app.log
3:2026-10-07 10:03 WARN slow request /books
7:2026-10-07 10:08 WARN disk 85% full
11:2026-10-07 10:14 WARN disk 90% full
~ $ grep -c INFO logs/app.log
5
~ $ grep -v INFO logs/app.log
2026-10-07 10:03 WARN slow request /books
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:07 info database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:13 Error timeout while sending mail
2026-10-07 10:14 WARN disk 90% full
```

- `-n` her satırın başına numarasını koyar (`3:`). Dosyayı bir düzenleyicide
  açıp o satıra gitmek için işe yarar.
- `-c` satırları yazmaz, **sayar**. `grep INFO dosya | wc -l` ile aynı sonuç.
- `-v` tersini yapar: deseni **taşımayan** satırları yazar. Burada `INFO`
  dışındaki her şey çıktı; dikkat et, küçük harfli `info` satırı da geldi.

## Kelimenin parçası, kelimenin tamamı: `-w`, `-x`

```text
~ $ grep -c in logs/app.log
5
~ $ grep -w in logs/app.log
2026-10-07 10:01 INFO user ada logged in
2026-10-07 10:11 INFO user alan logged in
~ $ grep -x ada names.txt
ada
```

`grep -c in` beş satır saydı: `logged in`'in yanında `info`, `retrying` ve
`sending` de `in` harflerini taşıyor. Desen bir **metin parçası** olarak
aranır. `-w` (*word*) yalnızca tek başına duran kelimeyi bulur. `-x` daha da
sıkıdır: satırın **tamamı** desene eşit olmalı.

## Desenler: düzenli ifadeler

grep'in deseni düz metin değil, bir **düzenli ifadedir** (regular
expression). Bazı karakterler özel anlam taşır:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>^a</code></span><span><code>a</code> ile <b>başlayan</b> satırlar.</span></div>
    <div class="anat-row"><span><code>e$</code></span><span><code>e</code> ile <b>biten</b> satırlar.</span></div>
    <div class="anat-row"><span><code>.</code></span><span>Herhangi <b>tek</b> bir karakter.</span></div>
    <div class="anat-row"><span><code>[0-9]</code></span><span>Köşeli parantezdekilerden biri: burada bir rakam.</span></div>
    <div class="anat-row"><span><code>x*</code></span><span>Öndeki karakterden sıfır ya da daha fazla.</span></div>
    <div class="anat-row"><span><code>-E 'A|B'</code></span><span>A <b>ya da</b> B (genişletilmiş ifade; <code>+</code> "bir ya da daha fazla").</span></div>
  </div>
  <figcaption>Desen bir <b>düzenli ifade</b>dir (regular expression). Joker karakterlere benzer ama aynı değildir: burada <code>.</code> tek karakter, <code>*</code> "öncekinden tekrar".</figcaption>
</figure>

```text
~ $ grep '^a' names.txt
ada
alan
~ $ grep 'e$' names.txt
grace
katherine
~ $ grep 'disk ..% full' logs/app.log
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:14 WARN disk 90% full
~ $ grep -E 'ERROR|WARN' logs/app.log
2026-10-07 10:03 WARN slow request /books
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:14 WARN disk 90% full
~ $ grep -oE '[0-9]+%' logs/app.log
85%
90%
```

- `'^a'`: `a` ile başlayan adlar. `'e$'`: `e` ile bitenler.
- `'disk ..% full'`: iki nokta, herhangi iki karakter demek; 85 de 90 da
  uydu.
- `-E 'ERROR|WARN'`: `-E` genişletilmiş ifadeyi açar ve `|` "ya da" olur.
- `-o` satırın tamamını değil, yalnızca **eşleşen parçayı** yazar.
  `[0-9]+` "bir ya da daha fazla rakam" demek.

Joker karakterlerle karıştırma: Joker Karakterler bölümünde `*` "herhangi bir
metin"di ve işi kabuk yapıyordu. Düzenli ifadede `*` "öndeki karakterden sıfır
ya da daha fazla" demek; "herhangi bir metin" `.*` diye yazılır.

## Birden çok dosya ve klasör: `-r`, `-l`

```text
~ $ grep -c ERROR logs/app.log logs/old/2025.log
logs/app.log:2
logs/old/2025.log:1
~ $ grep -r ERROR logs
logs/app.log:2026-10-07 10:05 ERROR database timeout
logs/app.log:2026-10-07 10:10 ERROR payment failed
logs/old/2025.log:2025-12-31 23:55 ERROR disk full
~ $ grep -rl ERROR logs
logs/app.log
logs/old/2025.log
```

- Birden çok dosya verilince grep her satırın başına **dosya adını** yazar.
- `-r` (*recursive*) klasörün içine ve alt klasörlerine iner.
- `-l` satırları değil, yalnızca eşleşmenin olduğu **dosyaların adlarını**
  yazar. "Bu kelime hangi dosyalarda geçiyor?" sorusunun cevabı.

## Boruda grep

Dosya adı verilmezse grep girdisini okur; bu yüzden boruların en sık
kullanılan parçasıdır:

```text
~ $ ls docs | grep txt
d.txt
e.txt
~ $ grep -i error logs/app.log | wc -l
3
~ $ grep -ic error logs/app.log
3
```

Kısa seçenekler birleştirilebilir: `-i -c` yerine `-ic`. Son iki komut aynı
sayıyı verdi.

## Tırnak kullan

```text
~ $ grep user ada logs/app.log
grep: ada: No such file or directory
logs/app.log:2026-10-07 10:01 INFO user ada logged in
logs/app.log:2026-10-07 10:11 INFO user alan logged in
~ $ echo $?
2
~ $ grep 'user ada' logs/app.log
2026-10-07 10:01 INFO user ada logged in
```

Tırnaksız yazınca kabuk boşlukta böldü: desen yalnızca `user` oldu, `ada` bir
**dosya adı** sayıldı. grep `ada` dosyasını bulamadı (çıkış kodu 2) ve `user`
geçen bütün satırları yazdı. Deseni her zaman tek tırnak içine yaz; `$`, `*`,
`|` gibi işaretler de böylece kabuğa değil grep'e ulaşır.

## Özet

| Seçenek | Ne yapar |
|---|---|
| `-i` | Büyük/küçük harf farkı yok |
| `-n` | Satır numarası |
| `-c` | Sayı |
| `-v` | Eşleşmeyenler |
| `-w` / `-x` | Tam kelime / tam satır |
| `-o` | Yalnızca eşleşen parça |
| `-E` | Genişletilmiş ifade (`+`, "ya da") |
| `-r` / `-l` | Alt klasörler / yalnızca dosya adları |

Önce desen, sonra dosyalar; desen tek tırnak içinde. Çıkış kodu 0 buldu, 1
bulamadı, 2 hata.
