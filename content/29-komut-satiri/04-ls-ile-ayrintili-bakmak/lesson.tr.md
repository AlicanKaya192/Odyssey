# ls ile Ayrıntılı Bakmak

Şimdiye kadar `ls`'i yalnızca adları görmek için kullandık. Oysa `ls` bir
dosya hakkında çok daha fazlasını söyleyebilir: ne kadar büyük olduğunu, en
son ne zaman değiştiğini, kime ait olduğunu, kimlerin okuyup yazabildiğini.
Bu bölümde `ls`'in en çok kullanılan seçeneklerini ve uzun listenin her
sütununu öğreneceğiz.

## Hatırlatma: düz `ls`

```text
~/project $ ls
data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -1
data.csv
docs/
notes.txt
report.txt
src/
```

Düz `ls` adları yan yana dizer. `-1` (bir rakamı) her adı ayrı satıra yazar;
uzun listelerde okumak daha kolaydır.

## Uzun liste: `ls -l`

`-l` (*long*) seçeneği her dosya için bir satır yazar:

```text
~/project $ ls -l
total 588
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada      0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 src/
```

Satır ilk bakışta karmaşık görünür ama hep aynı sütunlardan oluşur:

<figure class="fig">
  <pre><code class="language-text">-rw-r--r-- 1 ada ada  412 Oct  7 10:00 report.txt</code></pre>
  <div class="anat">
    <div class="anat-row"><span>-</span><span>Tür: <code>-</code> sıradan dosya, <code>d</code> klasör (directory).</span></div>
    <div class="anat-row"><span>rw-r--r--</span><span>İzinler: kim okuyabilir, yazabilir, çalıştırabilir. Ayrıntısı İzinler bölümünde.</span></div>
    <div class="anat-row"><span>1</span><span>Bağlantı sayısı. Dosyada çoğu zaman 1; şimdilik geç.</span></div>
    <div class="anat-row"><span>ada</span><span>Sahibi (kullanıcı).</span></div>
    <div class="anat-row"><span>ada</span><span>Grubu.</span></div>
    <div class="anat-row"><span>412</span><span>Boyut, bayt cinsinden. <code>-h</code> ile 4.0K gibi okunur.</span></div>
    <div class="anat-row"><span>Oct  7 10:00</span><span>Son değiştirilme zamanı.</span></div>
    <div class="anat-row"><span>report.txt</span><span>Adı.</span></div>
  </div>
  <figcaption><code>ls -l</code> (long) her dosya için bir satır yazar; sütunlar hep bu sırada.</figcaption>
</figure>

En çok bakacağın üç şey: **ilk harf** (dosya mı klasör mü), **boyut** ve
**ad**. İzin sütununu İzinler bölümünde harf harf okuyacağız; şimdilik
`rw-` "okunur ve yazılır" demek diye bil.

Birkaç ayrıntı:

- `notes.txt`'nin boyutu `0`: `touch` ile açılmış boş bir dosya.
- Klasörlerin boyutu `4096`. Bu, klasörün içindekilerin toplamı değil;
  klasörün kendi kaydının diskte kapladığı bir blok.
- En üstteki `total` satırı dosya sayısı değildir; dosyaların diskte
  kapladığı toplam alanı blok cinsinden verir. Çoğu zaman görmezden gelinir.

## Okunaklı boyutlar: `-h`

`588895` kaç megabayt? Hesaplamak zor. `-h` (*human-readable*) boyutları
`K`, `M`, `G` birimleriyle yazar:

```text
~/project $ ls -l data.csv report.txt
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
~/project $ ls -lh data.csv report.txt
-rw-r--r-- 1 ada ada 576K Oct  7 10:00 data.csv
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
~/project $ ls -lh
total 588K
-rw-r--r-- 1 ada ada 576K Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada 4.0K Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada    0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada 4.0K Oct  7 10:00 src/
```

`576K` yaklaşık yarım megabayt demek (1 K = 1024 bayt, 1 M = 1024 K).
1024 bayttan küçük dosyalar olduğu gibi kalır (`292`). Seçeneklerin harf
sırası önemli değil: `ls -lh`, `ls -hl` ve `ls -l -h` aynıdır.

## Gizli dosyalarla: `-a` ve `-A`

```text
~/project $ ls -a
./  ../  .env  data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -A
.env  data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -la
total 600
drwxr-xr-x 4 ada ada   4096 Oct  7 10:00 ./
drwxr-xr-x 3 ada ada   4096 Oct  7 10:00 ../
-rw-r--r-- 1 ada ada      6 Oct  7 10:00 .env
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada      0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 src/
```

- `-a` (*all*) gizlileri ve `./`, `../` girdilerini gösterir.
- `-A` (*almost all*) gizlileri gösterir ama `./` ve `../`'yu yazmaz.
- `-la` ikisini birleştirir: gizliler dahil, ayrıntılı. Bir klasörde "neler
  var, hepsi" diye bakmanın en yaygın yolu.

## Alt klasörlerle birlikte: `-R`

`-R` (*recursive*, büyük harf) klasörü ve içindeki bütün alt klasörleri
sırayla listeler. Her klasörden önce yolunu başlık olarak yazar:

```text
~ $ ls -R project
project:
data.csv  docs/  notes.txt  report.txt  src/

project/docs:
readme.md

project/src:
main.py
```

Büyük projelerde `-R` çok uzun bir çıktı verir; dosya aramak için ileride
çok daha iyi bir araç göreceğiz: `find`.

## Klasörün kendisi: `-d`

`ls`'e bir klasör verirsen **içine** bakar. Klasörün kendi satırını görmek
istersen `-d` (*directory*) eklersin:

```text
~ $ ls -l project/src
total 4
-rw-r--r-- 1 ada ada 9 Oct  7 10:00 main.py
~ $ ls -ld project/src
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 project/src/
~ $ ls -l project/src/main.py
-rw-r--r-- 1 ada ada 9 Oct  7 10:00 project/src/main.py
```

Dosya verirsen `ls` yalnızca o dosyanın satırını yazar.

## Özet

| Komut | Ne gösterir |
|---|---|
| `ls -1` | Her ad ayrı satırda |
| `ls -l` | Tür, izin, sahip, grup, boyut, tarih, ad |
| `ls -lh` | Boyutlar `K`, `M`, `G` ile |
| `ls -a` | Gizliler ve `./`, `../` |
| `ls -A` | Gizliler, `./` ve `../` olmadan |
| `ls -la` | Gizliler dahil, ayrıntılı |
| `ls -R` | Bütün alt klasörlerle |
| `ls -ld klasör` | Klasörün kendi satırı |

Seçenekler birleşir (`-lah`), sıraları önemli değil.
