# Metin Araçları: sort, uniq, cut, tr

grep satırları seçiyordu. Bu bölümdeki dört araç satırları **işler**:
sıralar, tekrarları sayar, parçalara böler, karakterleri değiştirir. Tek
başlarına küçük işler yaparlar; borunun içinde birleşince bir tabloyu ya da
kayıt dosyasını birkaç saniyede özetlersin.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>sort</span><span>Satırları <b>sıralar</b>. <code>-r</code> ters, <code>-n</code> sayı gibi, <code>-u</code> tekrarsız, <code>-t , -k 3</code> 3. alana göre.</span></div>
    <div class="anat-row"><span>uniq</span><span><b>Art arda</b> gelen aynı satırları teke indirir. <code>-c</code> sayar, <code>-d</code> tekrar edenler, <code>-u</code> bir kez geçenler.</span></div>
    <div class="anat-row"><span>cut</span><span>Her satırdan bir <b>parça keser</b>: <code>-d , -f 2</code> virgülle ayrılmış 2. alan, <code>-c 1-10</code> ilk 10 karakter.</span></div>
    <div class="anat-row"><span>tr</span><span>Karakterleri <b>çevirir</b> ya da siler: <code>tr a-z A-Z</code>, <code>-d</code> sil, <code>-s</code> tekrarı sıkıştır. Yalnızca girdiden okur.</span></div>
  </div>
  <figcaption>Dört araç da satır satır çalışır ve borunun içinde birbirine eklenir.</figcaption>
</figure>

## sort: sıralamak

```text
~ $ sort names.txt
ada
alan
dennis
grace
katherine
linus
margaret
~ $ sort -r names.txt
margaret
linus
katherine
grace
dennis
alan
ada
```

`sort` satırları abece sırasıyla yazar, `-r` (*reverse*) tersine çevirir.
Dosyanın kendisine dokunmaz; sonucu saklamak istiyorsan `> başka.txt`.

### Sayıları sıralamak: `-n`

```text
~ $ cut -d , -f 3 data/sales.csv | tail -n +2 | sort
120
175
250
30
40
60
80
95
~ $ cut -d , -f 3 data/sales.csv | tail -n +2 | sort -n
30
40
60
80
95
120
175
250
```

İlk sıralama yanlış görünüyor: `120`, `30`'dan önce geldi. `sort` normalde
**metin** gibi karşılaştırır: önce ilk karakterlere bakar ve `1`, `3`'ten
küçüktür. `-n` (*numeric*) satırın başındaki sayının **değerine** bakar.
(Ortadaki `tail -n +2` başlık satırını attı; Dosyanın İçine Bakmak
bölümünden hatırla: "2. satırdan sona".)

### Bir alana göre sıralamak: `-t` ve `-k`

```text
~ $ cat data/sales.csv
name,city,amount
ada,London,120
alan,Manchester,80
grace,New York,250
linus,Helsinki,40
margaret,Boston,175
dennis,New York,60
katherine,Boston,95
ada,London,30
~ $ sort -t , -k 3 -n data/sales.csv
name,city,amount
ada,London,30
linus,Helsinki,40
dennis,New York,60
alan,Manchester,80
katherine,Boston,95
ada,London,120
margaret,Boston,175
grace,New York,250
~ $ sort -t , -k 3 -rn data/sales.csv | head -n 3
grace,New York,250
margaret,Boston,175
ada,London,120
```

- `-t ,` alanları ayıran karakteri söyler (virgül).
- `-k 3` 3. alandan itibaren sırala demek.
- `-rn` ters ve sayı gibi; ardından `head -n 3` en büyük üç satışı verdi.

Başlık satırı `amount` sayı olmadığı için `-n` onu 0 saydı ve en üste koydu.
Dikkat: bu terminal büyük harfleri küçüklerden önce sıralar. Gerçek bir
bilgisayarda sıra dil ayarına (*locale*) göre değişebilir; aynı sırayı her
yerde almak için `LC_ALL=C sort` yazılır.

## cut: sütun kesmek

```text
~ $ cut -d , -f 1 data/sales.csv | head -n 3
name
ada
alan
~ $ cut -d , -f 1,3 data/sales.csv | head -n 3
name,amount
ada,120
alan,80
~ $ cut -c 1-10 logs/app.log | head -n 2
2026-10-07
2026-10-07
~ $ cut -d ' ' -f 3- logs/app.log | head -n 3
INFO server started
INFO user ada logged in
WARN slow request /books
```

- `-d ,` ayırıcı (*delimiter*), `-f 1` 1. alan (*field*).
- `-f 1,3` iki alan; araya yine ayırıcı konur. `-f 2-4` bir aralık olurdu.
- `-c 1-10` alan değil **karakter** keser: kayıttaki tarih her satırda ilk
  10 karakter.
- `-f 3-` 3. alandan satırın sonuna kadar.

`cut`'un ayırıcısı tek bir karakter olmalı. Kayıt dosyasında ayırıcı boşluk;
boşluğu tırnak içinde yazarız: `-d ' '`.

## uniq: tekrarlar

```text
~ $ head -n 4 data/visits.log
10.0.0.1 /home
10.0.0.2 /books
10.0.0.1 /books
10.0.0.3 /home
~ $ cut -d ' ' -f 2 data/visits.log | uniq | wc -l
11
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq
/about
/books
/contact
/home
~ $ cut -d , -f 2 data/sales.csv | tail -n +2 | sort -u
Boston
Helsinki
London
Manchester
New York
```

`uniq` yalnızca **art arda gelen** aynı satırları birleştirir. Ziyaret
kaydında `/home` dağınık satırlarda geçtiği için `uniq` 12 satırı ancak 11'e
indirdi. Önce `sort` aynıları yan yana getirir, sonra `uniq` dört sayfa
bırakır. `sort -u` ikisini birden yapar.

### Saymak: `-c`, `-d`, `-u`

<figure class="fig">
  <div class="flow">
    <span class="node">cut -d ' ' -f 2<br><small>sayfayı kes</small></span><span class="arrow">→</span>
    <span class="node acc">sort<br><small>aynıları yan yana</small></span><span class="arrow">→</span>
    <span class="node acc">uniq -c<br><small>say</small></span><span class="arrow">→</span>
    <span class="node">sort -rn<br><small>en çok üstte</small></span>
  </div>
  <figcaption>"Hangisi kaç kez?" sorusunun kalıbı. <code>uniq</code> yalnızca komşu satırları birleştirdiği için önce <code>sort</code> gerekir.</figcaption>
</figure>

```text
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq -c
      2 /about
      4 /books
      1 /contact
      5 /home
~ $ cut -d ' ' -f 2 data/visits.log | sort | uniq -c | sort -rn
      5 /home
      4 /books
      2 /about
      1 /contact
~ $ cut -d ' ' -f 1 data/visits.log | sort | uniq -d
10.0.0.1
10.0.0.2
10.0.0.3
~ $ cut -d ' ' -f 1 data/visits.log | sort | uniq -u
10.0.0.4
10.0.0.5
10.0.0.6
10.0.0.7
```

- `uniq -c` her satırın önüne kaç kez geçtiğini yazar.
- Arkasına `sort -rn` eklenince en çok ziyaret edilen sayfa üste çıktı. Bu
  zincir "hangisi kaç kez?" sorusunun kalıbıdır; kelime, adres, hata türü,
  her şey için aynı.
- `uniq -d` birden çok kez geçenleri (birer kez), `uniq -u` yalnızca bir kez
  geçenleri yazar: üç adres tekrar gelmiş, dördü bir kez.

## tr: karakter çevirmek

```text
~ $ echo hello | tr a-z A-Z
HELLO
~ $ tr '[:lower:]' '[:upper:]' < poem.txt
ROSES ARE RED
VIOLETS ARE BLUE
THE SHELL IS FAST
AND SO ARE YOU
~ $ cat notes/messy.txt
Buy   milk  and   bread
Call    Ada
~ $ tr -s ' ' < notes/messy.txt
Buy milk and bread
Call Ada
~ $ echo 2026-10-07 | tr -d -
20261007
~ $ echo a,b,c | tr , '\n'
a
b
c
```

- `tr a-z A-Z` birinci kümedeki her harfi ikincideki karşılığına çevirir.
  `'[:lower:]' '[:upper:]'` aynı şeyin sınıf adlarıyla yazılışı.
- `-s` (*squeeze*) art arda gelen aynı karakteri teke indirir: dağınık
  boşluklar düzeldi.
- `-d` (*delete*) siler: tarihteki tireler gitti.
- `'\n'` satır sonudur: virgülleri satır sonuna çevirince her parça ayrı
  satıra düştü.

`tr` dosya adı almaz; girdisini her zaman `<` ile ya da bir borudan okur.

## Hepsi bir arada: en sık geçen kelimeler

```text
~ $ tr ' ' '\n' < poem.txt | sort | uniq -c | sort -rn | head -n 3
      3 are
      1 you
      1 so
```

Boşlukları satır sonuna çevir (her kelime bir satır), sırala, say, sayıya göre
sırala, ilk üçü al. Beş küçük komut, tek satır: şiirde en çok `are` geçiyor.

## Tuzaklar

```text
~ $ tr a-z A-Z poem.txt
tr: extra operand 'poem.txt'
Try 'tr --help' for more information.
~ $ sort -t , -k 2 data/sales.csv | head -n 2
margaret,Boston,175
katherine,Boston,95
~ $ sort -t , -k 2,2 data/sales.csv | head -n 2
katherine,Boston,95
margaret,Boston,175
```

- `tr a-z A-Z poem.txt`: `tr` dosya adını fazladan argüman sayar.
- `-k 2` 2. alandan **satırın sonuna** kadar bakar; iki Boston satırının
  sırasını tutarlar belirledi: metin gibi `175`, `95`'ten önce gelir.
  `-k 2,2` yalnızca 2. alana bakar; eşitlikte bütün satır karşılaştırılır ve
  `katherine` öne geçer.
- `uniq`'i `sort`'suz kullanmak tekrarları kaçırır.
- Dosyayı kendisine sıralama: `sort f > f` dosyayı boşaltır (Yönlendirme
  bölümünden hatırla).

## Özet

| Komut | Ne yapar |
|---|---|
| `sort` / `-r` / `-n` / `-u` | Sırala / ters / sayı gibi / tekrarsız |
| `sort -t , -k 3` | 3. alana göre |
| `uniq` / `-c` / `-d` / `-u` | Komşu tekrarları teke indir / say / tekrarlananlar / bir kez geçenler |
| `cut -d , -f 2` | 2. alan |
| `cut -c 1-10` | İlk 10 karakter |
| `tr a-z A-Z` | Harf çevir |
| `tr -d x` / `tr -s ' '` | Sil / sıkıştır |

"Hangisi kaç kez?" kalıbını ezberle: kes, `sort`, `uniq -c`, `sort -rn`.
