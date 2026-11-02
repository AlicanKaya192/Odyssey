# Dosya Sistemi ve Yollar

Terminalde bir dosyayla çalışmak için önce onun **nerede** olduğunu
söyleyebilmen gerekiyor. Görsel arayüzde klasörlere tıklayarak inersin;
komut satırında aynı şeyi **yol** yazarak yaparsın. Bu bölümde dosyaların
nasıl dizildiğini, yolların nasıl yazıldığını ve `cd` ile nasıl
dolaşıldığını göreceğiz.

## Tek bir ağaç

Linux'ta bütün dosyalar ve klasörler tek bir **ağacın** içinde durur. Ağacın
en tepesindeki klasöre **kök** (root) deniyor ve adı yalnızca `/` işareti.
Diğer her şey onun altında.

<figure class="fig">
  <pre><code class="language-text">/                     kök: her şeyin başladığı yer
├── bin/              temel programlar
├── etc/              sistemin ayar dosyaları
├── home/             kullanıcıların klasörleri
│   └── ada/          senin ev klasörün (~)
│       ├── notes/
│       └── projects/
│           ├── api/
│           └── site/
│               └── css/
├── root/             yöneticinin (root) ev klasörü
├── tmp/              geçici dosyalar
├── usr/              programlar ve kütüphaneler
└── var/              değişen veriler (kayıtlar)</code></pre>
  <figcaption>Linux'ta tek bir ağaç var; en tepesi kök klasör <code>/</code>. Her dosyanın bu ağaçta tek bir yeri vardır.</figcaption>
</figure>

Windows'ta her diskin kendi başı vardır (`C:`, `D:`); Linux'ta sürücü harfi
yoktur, her şey `/` altındaki tek ağaçtadır. Kök klasöre gidip bakalım:

```text
~ $ cd /
/ $ pwd
/
/ $ ls
bin/  etc/  home/  root/  tmp/  usr/  var/
/ $ cd ~
~ $ pwd
/home/ada
~ $ ls
notes/  projects/
```

Kökteki klasörlerin hepsini bilmen gerekmiyor; en sık karşılaşacakların:

- `/home`: kullanıcıların klasörleri. Senin ev klasörün `/home/ada`.
- `/etc`: sistemin ayar dosyaları.
- `/tmp`: geçici dosyalar (bilgisayar yeniden açılınca çoğu zaman silinir).
- `/usr` ve `/bin`: programlar. `ls` ve `cat` gibi komutlar aslında
  buralarda duran küçük programlardır.

Bu klasörler sistemin; çoğuna yalnızca bakabilirsin. Kendi işlerini ev
klasöründe yaparsın.

## Yol nedir?

**Yol** (path), bir dosyaya ya da klasöre giden tarif. Klasör adları `/` ile
birbirine eklenir: `/home/ada/projects/site` "kökten başla, `home`'a gir,
sonra `ada`'ya, sonra `projects`'e, sonra `site`'a" demek.

İki çeşit yol var:

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Mutlak yol</h4><p><code>/home/ada/projects/site</code></p><p><code>/</code> ile başlar</p><p>Kökten başlayıp tarif eder</p><p>Nerede olursan ol aynı yeri gösterir</p></div>
    <div class="dim"><h4>Göreli yol</h4><p><code>projects/site</code></p><p><code>/</code> ile başlamaz</p><p>Bulunduğun klasörden başlar</p><p>Nerede olduğuna göre başka yeri gösterir</p></div>
  </div>
  <figcaption>Ev klasöründeyken ikisi de aynı yere gider. <code>/tmp</code> klasöründeyken göreli yol <code>/tmp/projects/site</code> diye aranır.</figcaption>
</figure>

- **Mutlak yol** (absolute path) `/` ile başlar ve tarifi kökten verir.
  Nerede olursan ol, hep aynı yeri gösterir.
- **Göreli yol** (relative path) `/` ile başlamaz; tarif **bulunduğun
  klasörden** başlar. Daha kısadır ama nerede olduğuna bağlıdır.

## Kısaltmalar: `~`, `.` ve `..`

Yolların içinde birkaç özel işaret var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>/</span><span>Kök klasör. Yolun başındaysa "kökten başla" demek; yolun içinde klasörleri ayırır.</span></div>
    <div class="anat-row"><span>~</span><span>Ev klasörün: <code>/home/ada</code>.</span></div>
    <div class="anat-row"><span>.</span><span>Bulunduğun klasörün kendisi.</span></div>
    <div class="anat-row"><span>..</span><span>Bir üstteki klasör. <code>../..</code> iki üstteki.</span></div>
    <div class="anat-row"><span>-</span><span>Yalnızca <code>cd -</code> içinde: bir önceki bulunduğun klasör.</span></div>
  </div>
  <figcaption>Yolların içinde en çok kullanılan beş işaret.</figcaption>
</figure>

`..` ile yukarı çıkılır, `.` "burası" demektir. `~` ev klasörünün mutlak
yolunu kısaltır; `~/projects` her yerden ev klasöründeki `projects`
klasörünü gösterir.

## `cd` ile dolaşmak

`cd` (*change directory*) bulunduğun klasörü değiştirir. Arkasına bir yol
yazarsın, göreli ya da mutlak:

```text
~ $ pwd
/home/ada
~ $ cd projects/site
~/projects/site $ pwd
/home/ada/projects/site
~/projects/site $ cd css
~/projects/site/css $ pwd
/home/ada/projects/site/css
~/projects/site/css $ cd ..
~/projects/site $ pwd
/home/ada/projects/site
~/projects/site $ cd ../..
~ $ pwd
/home/ada
~ $ cd /home/ada/projects/api
~/projects/api $ pwd
/home/ada/projects/api
~/projects/api $ cd
~ $ pwd
/home/ada
```

Dikkat et:

- `cd projects/site` iki kat birden indi; yolun içinde istediğin kadar klasör
  olabilir.
- `cd ..` bir kat, `cd ../..` iki kat yukarı çıktı.
- `cd /home/ada/projects/api` mutlak yoldu; nerede olsaydık oraya giderdi.
- Arkasına hiçbir şey yazmadan `cd` seni ev klasörüne götürdü. `cd ~` de aynı
  şeyi yapar.

İstem her adımda değişti: kabuk sana hep nerede olduğunu gösteriyor.
Emin olamazsan `pwd` yaz.

## İki klasör arasında gidip gelmek: `cd -`

`cd -` seni **bir önceki** bulunduğun klasöre götürür ve vardığın yeri
ekrana yazar. İki klasör arasında çalışırken çok işe yarar:

```text
~ $ cd projects/site/css
~/projects/site/css $ cd -
/home/ada
~ $ cd -
/home/ada/projects/site/css
~/projects/site/css $ pwd
/home/ada/projects/site/css
```

## Bakmak için gitmek gerekmez

`ls` komutuna da yol verebilirsin. Bir klasörün içine bakmak için oraya
gitmen gerekmez:

```text
~ $ ls projects
api/  site/
~ $ ls projects/site
css/  index.html
~ $ ls ~/projects/api/docs
routes.txt
~ $ ls /etc
hostname  passwd  shells
~ $ ls .
notes/  projects/
~ $ ls ..
ada/
```

`ls ..` ev klasörünün bir üstüne, `/home` klasörüne baktı: orada yalnızca
`ada` var.

## Göreli yol nerede olduğuna bağlıdır

Aynı göreli yol başka bir klasörde başka bir yeri gösterir. `/tmp`
klasöründeyken `projects` diye bir şey yok:

```text
~ $ cd /tmp
/tmp $ ls projects
ls: cannot access 'projects': No such file or directory
/tmp $ ls ~/projects
api/  site/
/tmp $ cd projects
bash: cd: projects: No such file or directory
/tmp $ cd /home/ada/projects
~/projects $ pwd
/home/ada/projects
```

`~/projects` ise her yerden çalıştı, çünkü `~` mutlak bir yolun kısaltması.
"Burada yok" diyen bir hata gördüğünde ilk soracağın şey: **şu an
neredeyim?**

## Hatalar

```text
~ $ cd nowhere
bash: cd: nowhere: No such file or directory
~ $ cd notes/todo.txt
bash: cd: notes/todo.txt: Not a directory
~ $ cd projects site
bash: cd: too many arguments
```

- `No such file or directory`: o adda bir klasör yok (ya da yanlış yerdesin).
- `Not a directory`: verdiğin şey bir dosya; `cd` yalnızca klasöre girer.
- `too many arguments`: `cd` tek bir yol ister, sen iki tane verdin.

## Adında boşluk olan klasörler

Kabuk satırı boşluklardan böldüğü için `cd my notes`, `cd`'ye iki ayrı
argüman verir. Adında boşluk olan bir şeyi **tırnak** içinde yazarsın:

```text
~ $ mkdir "my notes"
~ $ ls
my notes/  notes/  projects/
~ $ cd my notes
bash: cd: too many arguments
~ $ cd "my notes"
~/my notes $ pwd
/home/ada/my notes
```

Gerçek bir Linux terminali bu adı `ls` çıktısında `'my notes'` diye
tırnaklı gösterir; boşluklu olduğunu hatırlatmak için. Bu yüzden çoğu kişi
dosya ve klasör adlarında boşluk yerine `-` ya da `_` kullanır:
`my-notes`, `my_notes`.

## Windows yolları ve Git Bash

Windows'ta yol `C:\Users\ada\Documents` gibi yazılır: başta sürücü harfi var,
klasörler **ters bölü** (`\`) ile ayrılır. Git Bash aynı klasörü Linux
biçiminde gösterir:

| Windows | Git Bash |
|---|---|
| `C:\Users\ada` | `/c/Users/ada` |
| `C:\Users\ada\Documents\notes.txt` | `/c/Users/ada/Documents/notes.txt` |
| `D:\photos` | `/d/photos` |

Sürücü harfi kökün altında bir klasör gibi görünür. Linux'ta ve Git Bash'te
klasörler **eğik çizgi** (`/`) ile ayrılır. Bir fark daha: Windows büyük ve
küçük harfi aynı sayar, Linux saymaz; `Notes` ile `notes` Linux'ta iki ayrı
klasördür.

## Özet

- Linux'ta tek bir ağaç var; tepesi kök `/`, senin yerin `~` (`/home/ada`).
- **Mutlak yol** `/` ile başlar ve her yerden aynı yeri gösterir; **göreli
  yol** bulunduğun klasörden başlar.
- `.` burası, `..` bir üstü, `~` ev klasörü.
- `cd yol` git, `cd ..` yukarı, `cd` ya da `cd ~` eve, `cd -` öncekine.
- `ls yol` oraya gitmeden içine bakar.
- Boşluklu adlar tırnak içinde yazılır.
