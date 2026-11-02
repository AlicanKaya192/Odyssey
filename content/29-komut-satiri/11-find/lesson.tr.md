# find ile Dosya Bulmak

Bir projede yüzlerce dosya ve iç içe klasörler olur. "O ayar dosyası nerede
kalmıştı?", "Bu projede kaç Python dosyası var?", "Bütün yedek dosyalarını
silmek istiyorum" gibi soruların cevabı `find`. `ls` yalnızca tek bir klasörün
içine bakar; `find` başladığı yerden **bütün alt klasörlere** iner.

Bu bölümde çalışacağımız proje şöyle: `project` klasöründe kaynak kodu
(`src`), testler (`tests`), belgeler (`docs`), eski yedekler (`build`) ve kayıt
dosyaları (`logs`) var.

<figure class="fig">
  <pre><code class="language-text">find project -type f -name '*.py'</code></pre>
  <div class="anat">
    <div class="anat-row"><span>find</span><span>Komut: klasörün içine ve bütün alt klasörlerine iner.</span></div>
    <div class="anat-row"><span>project</span><span><b>Nereden</b> başlanacak. Önce yollar gelir; <code>.</code> bulunduğun klasör.</span></div>
    <div class="anat-row"><span>-type f</span><span><b>Koşul</b>: yalnızca dosyalar (<code>d</code> klasörler).</span></div>
    <div class="anat-row"><span>-name '*.py'</span><span><b>Koşul</b>: adı bu kalıba uyanlar. Kalıp tırnak içinde.</span></div>
  </div>
  <figcaption>Koşulların hepsi tutmalı ("ve"). Koşul yoksa find her şeyi yazar.</figcaption>
</figure>

## Her şeyi listelemek

```text
~ $ find project
project
project/build
project/build/main.bak
project/build/numbers.bak
project/docs
project/docs/guide.md
project/docs/notes.MD
project/empty
project/logs
project/logs/run1.log
project/logs/run2.log
project/readme.md
project/src
project/src/main.py
project/src/utils
project/src/utils/numbers.py
project/src/utils/text.py
project/tests
project/tests/test_main.py
~ $ find project -type d
project
project/build
project/docs
project/empty
project/logs
project/src
project/src/utils
project/tests
```

Koşulsuz `find project` klasörün kendisini ve altındaki her şeyi, her biri ayrı
satırda, **tam yoluyla** yazar. `-type d` yalnızca klasörleri bırakır; içi
boş `empty` klasörü de listede.

Bu terminal sonuçları abece sırasıyla yazar. Gerçek bir Linux'ta `find`
dosyaları diskteki sırasıyla yazar; sıra farklı çıkabilir, sonuç aynıdır.
Sıralı istiyorsan arkasına `| sort` eklersin.

## Ada göre: `-name` ve `-iname`

```text
~ $ find project -name '*.py'
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
~ $ find project -name 'main*'
project/build/main.bak
project/src/main.py
~ $ find project -name '*.md'
project/docs/guide.md
project/readme.md
~ $ find project -iname '*.md'
project/docs/guide.md
project/docs/notes.MD
project/readme.md
```

- `-name '*.py'` adı `.py` ile biten her şeyi buldu, hangi derinlikte olursa
  olsun.
- `'main*'` hem `main.py`'yi hem yedeği `main.bak`'ı buldu.
- `-name` harf büyüklüğüne bakar: `'*.md'` kalıbı `notes.MD`'yi bulmadı.
  `-iname` (*insensitive*) farkı kapatır.

Kalıp, Joker Karakterler bölümündeki joker kalıbının aynısı (`*`, `?`, `[ ]`);
farkı onu kabuğun değil `find`'ın uygulaması.

## Türe ve derinliğe göre

```text
~ $ find project -type f -name '*.log'
project/logs/run1.log
project/logs/run2.log
~ $ find project/src -type f
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
~ $ find project -maxdepth 1
project
project/build
project/docs
project/empty
project/logs
project/readme.md
project/src
project/tests
~ $ find project/docs -type f -not -name '*.md'
project/docs/notes.MD
```

- `-type f` dosya, `-type d` klasör. Birden çok koşul yazınca **hepsi**
  tutmalı: "hem dosya olsun hem adı `.log` ile bitsin".
- Başlangıç yolu daraltılabilir: `find project/src` yalnızca `src`'nin altına
  bakar.
- `-maxdepth 1` alt klasörlere inmez; `ls` gibi, ama klasörün kendisi de
  listede ve yollar tam.
- `-not` (ya da `!`) koşulu ters çevirir: `docs`'ta `.md` ile bitmeyen tek
  dosya `notes.MD`.

## Kalıbı tırnak içine yaz

```text
~ $ find project -name *.py
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
~ $ touch setup.py
~ $ find project -name *.py
~ $ find project -name '*.py'
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
```

İlk komut tırnaksız yazıldığı hâlde çalıştı, çünkü bulunduğun klasörde `.py`
ile biten bir dosya yoktu ve kabuk `*.py`'ye dokunmadı. `setup.py` oluşunca
kabuk `*.py`'yi **find çalışmadan önce** `setup.py`'ye çevirdi; find yalnızca
adı tam olarak `setup.py` olan dosyayı aradı ve hiçbir şey bulamadı. Hata da
vermedi: bu en sinsi hata türüdür. Kalıbı her zaman tırnak içine yaz.

## Boruda ve dosyada

```text
~ $ find project -name '*.py' | wc -l
4
~ $ find project -type f | grep test
project/tests/test_main.py
~ $ find . -name '*.log' > logs.txt
~ $ cat logs.txt
./project/logs/run1.log
./project/logs/run2.log
```

find her yolu ayrı satıra yazdığı için önceki bölümlerdeki her araçla
birleşir: `wc -l` sayar, `grep` süzer, `>` kaydeder. `find .` bulunduğun
klasörden başlar; yollar `./` ile başlar.

## Bulunan her dosyada komut çalıştırmak: `-exec`

```text
~ $ find project -name '*.log' -exec wc -l {} \;
2 project/logs/run1.log
2 project/logs/run2.log
~ $ find project -name '*.py' -exec grep -l TODO {} \;
project/src/main.py
project/src/utils/numbers.py
```

`-exec` bulunan **her** yol için bir komut çalıştırır. `{}` o anki yolun yerine
geçer, `\;` komutun bittiğini söyler (ters bölü, `;`'nin kabuğa değil find'a
gitmesi için). İkinci komut iki aracı birleştiriyor: find adı `.py` olan
dosyaları seçti, `grep -l` içinde `TODO` geçenlerin adını yazdı.

## Silmek: `-delete`

```text
~ $ find project -name '*.bak'
project/build/main.bak
project/build/numbers.bak
~ $ find project -name '*.bak' -delete
~ $ find project -name '*.bak'
~ $ ls project/build
```

`-delete` bulduğu her şeyi **sorusuz ve geri dönüşsüz** siler. Bu yüzden düzen
hep aynıdır:

1. Komutu `-delete` olmadan çalıştır, listeye bak.
2. Liste tam istediğin gibiyse aynı komutun **sonuna** `-delete` ekle.
3. Bir kez daha `-delete`'siz çalıştırıp boş geldiğini gör.

`build` klasörü yerinde kaldı; yalnızca içindeki iki yedek gitti.

## Hata mesajları

```text
~ $ find nope
find: 'nope': No such file or directory
~ $ find project -type x
find: Unknown argument to -type: x
~ $ find -name '*.py' project
find: paths must precede expression: `project'
find: possible unquoted pattern after predicate `-name'?
```

- Başlangıç yolu var olmalı.
- `-type` yalnızca belirli harfleri tanır (`f`, `d`...).
- Yol koşullardan **önce** yazılır. find burada bir de ipucu veriyor:
  kalıbın tırnaksız kalmış olabileceğini düşünüyor.

Gerçek bir terminalde find boyuta (`-size +1M`), tarihe (`-mtime -7`: son 7
günde değişmiş) ve boşluğa (`-empty`) göre de arar; koşulları "ya da" ile
birleştirmek için `-o` vardır. Bu terminalde bunlar yok.

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>ls</h4><p>Tek klasörün içi</p><p>Ad ve ayrıntı</p></div>
    <div class="ok"><h4>find</h4><p>Bütün alt klasörler</p><p><b>Dosyanın adına</b>, türüne göre arar</p></div>
    <div class="ok"><h4>grep -r</h4><p>Bütün alt klasörler</p><p><b>Dosyanın içine</b> göre arar</p></div>
  </div>
  <figcaption>"Adı neydi?" sorusu find'ın, "içinde ne yazıyordu?" sorusu grep'in.</figcaption>
</figure>

## Özet

| Yazım | Ne bulur |
|---|---|
| `find yol` | Yolun altındaki her şey |
| `find yol -name 'k'` | Adı k kalıbına uyanlar |
| `find yol -iname 'k'` | Aynısı, harf büyüklüğüne bakmadan |
| `find yol -type f` / `-type d` | Dosyalar / klasörler |
| `find yol -maxdepth 1` | Alt klasörlere inmeden |
| `find yol -not -name 'k'` | Uymayanlar |
| `find yol ... -exec komut {} \;` | Her bulunanda komut |
| `find yol ... -delete` | Bulunanları siler (önce listele!) |

Önce yol, sonra koşullar; kalıp tırnak içinde.
