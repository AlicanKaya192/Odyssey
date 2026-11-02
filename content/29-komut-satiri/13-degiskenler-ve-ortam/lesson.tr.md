# Değişkenler ve Ortam

Kabuk yalnızca komut çalıştırmaz, değer de saklar. Bir değeri bir **değişkene**
koyup tekrar tekrar kullanabilir, bir komutun çıktısını yakalayabilir,
çalıştırdığın programlara ayar verebilirsin. Python, git ve Docker gibi
programların davranışını değiştiren ayarların çoğu da **ortam değişkenleridir**.
Bu bölüm bir sonrakinin, betik yazmanın, temeli.

## Değişken tanımlamak ve kullanmak

<figure class="fig">
  <pre><code class="language-text">name=Ada          echo "Hello, &#36;name"</code></pre>
  <div class="anat">
    <div class="anat-row"><span>name</span><span>Değişkenin adı: harf, rakam, <code>_</code>; rakamla başlamaz.</span></div>
    <div class="anat-row"><span>=</span><span>Atama. İki yanında <b>boşluk olmaz</b>.</span></div>
    <div class="anat-row"><span>Ada</span><span>Değer: her zaman metin. Boşluk varsa tırnak: <code>name="Ada Lovelace"</code>.</span></div>
    <div class="anat-row"><span>&#36;name</span><span>Kullanırken başına <code>&#36;</code>; kabuk yerine değeri koyar.</span></div>
  </div>
  <figcaption>Atarken <code>&#36;</code> yok, kullanırken var. Çift tırnak içinde değer konur, tek tırnak içinde konmaz.</figcaption>
</figure>

```text
~ $ name=Ada
~ $ echo $name
Ada
~ $ echo "Hello, $name"
Hello, Ada
~ $ echo 'Hello, $name'
Hello, $name
~ $ name=Grace
~ $ echo "Hello, $name"
Hello, Grace
~ $ name = Ada
bash: name: command not found
```

- Atarken `$` yok: `name=Ada`. Kullanırken var: `$name`.
- Değişken yeniden atanabilir; son değer geçerli.
- **Eşittirin iki yanında boşluk olmaz.** `name = Ada` yazınca kabuk `name`'i
  bir komut sandı.
- Çift tırnak içinde değer konur, tek tırnak içinde konmaz. Tek tırnak her
  şeyi olduğu gibi bırakır: jokerleri de, `$`'ı da. Çift tırnak jokerleri
  kapatır ama `$`'ı açık bırakır.

## Adın nerede bittiği: süslü parantez

```text
~ $ file=report
~ $ echo "$file_2026.txt"
.txt
~ $ echo "${file}_2026.txt"
report_2026.txt
~ $ echo "[$nothing]"
[]
~ $ echo "${nothing:-none}"
none
```

Kabuk değişkenin adını harf, rakam ve `_` bitene kadar okur: `$file_2026`
yazınca `file_2026` adında bir değişken aradı. Böyle bir değişken yok ve
**tanımsız değişken hata vermez, boş metin olur**; geriye `.txt` kaldı. Adın
sınırını `${file}` ile çizersin.

`${nothing:-none}` "boşsa şu değeri kullan" demek; betiklerde varsayılan değer
vermenin kısa yolu.

## Değişkeni tırnakla kullan

```text
~ $ greeting="Hello   world"
~ $ echo $greeting
Hello world
~ $ echo "$greeting"
Hello   world
```

Tırnaksız `$greeting` yazınca kabuk değeri boşluklardan böldü ve `echo`'ya iki
ayrı kelime verdi; aradaki fazla boşluklar kayboldu. Çift tırnak değeri tek
parça tutar. İçinde boşluk olabilecek her değişkeni (özellikle dosya
adlarını) `"$ad"` diye kullan.

## Komutun çıktısını yakalamak

```text
~ $ count=$(ls docs | wc -l)
~ $ echo "docs has $count files"
docs has 5 files
~ $ echo $((count * 2))
10
~ $ lines=$(wc -l < names.txt)
~ $ echo "names.txt has $lines lines"
names.txt has 7 lines
```

- `$( komut )` komutu çalıştırır ve çıktısını yerine koyar (*command
  substitution*). Sonuç bir değişkene atanabilir ya da doğrudan bir metnin
  içinde kullanılabilir.
- `$(( ... ))` tam sayı aritmetiği yapar; içinde değişkenin başına `$`
  yazmak gerekmez.

## Kabuğun hazır değişkenleri

```text
~ $ echo $HOME
/home/ada
~ $ echo $USER
ada
~ $ echo $PWD
/home/ada
~ $ cd docs
~/docs $ echo $PWD
/home/ada/docs
~/docs $ cd
~ $ echo $SHELL
/bin/bash
```

Kabuk açılırken bazı değişkenleri kendisi doldurur. `HOME` ev klasörün (`~`
kısaltması bunu kullanır), `USER` kullanıcı adın, `PWD` bulunduğun klasör
(`cd` ile değişir), `SHELL` kullandığın kabuk. Bunlar **büyük harfle** yazılır;
kendi değişkenlerine küçük harfli adlar vermek karışmayı önler.

## Ortam değişkenleri: export

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Kabuk değişkeni</h4><p><code>city=London</code></p><p>Yalnızca bu kabukta</p><p>Başlatılan programlar görmez</p></div>
    <div class="ok"><h4>Ortam değişkeni</h4><p><code>export city=London</code></p><p>Bu kabukta ve başlattığı her programda</p><p><code>env</code> listesinde görünür</p></div>
  </div>
  <figcaption>Bir program (Python, git, bir betik) ayarını ortam değişkenlerinden okur. Ona bir değer vermek için <code>export</code>.</figcaption>
</figure>

```text
~ $ city=London
~ $ bash -c 'echo "[$city]"'
[]
~ $ export city
~ $ bash -c 'echo "[$city]"'
[London]
~ $ printenv city
London
~ $ unset city
~ $ printenv city
```

`bash -c '...'` yeni bir kabuk başlatıp tırnak içindeki komutu çalıştırır;
"başka bir program" yerine geçiyor. İlk denemede yeni kabuk `city`'yi
görmedi: sıradan bir değişken yalnızca tanımlandığı kabukta yaşar. `export`
değişkeni **ortama** çıkardı; kabuğun bundan sonra başlattığı her program onu
görür. `printenv` bir ortam değişkenini yazar, `unset` değişkeni kaldırır.

Bir değeri yalnızca **tek bir komuta** vermek de mümkün:

```text
~ $ GREETING=Hi bash -c 'echo $GREETING'
Hi
~ $ echo "[$GREETING]"
[]
```

Komutun önüne yazılan atama yalnızca o komut için geçerli; kabukta iz
bırakmadı.

## Ortamın tamamı: env

```text
~ $ env
HOME=/home/ada
USER=ada
LOGNAME=ada
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
PWD=/home/ada
LANG=en_US.UTF-8
TERM=xterm-256color
~ $ env | grep HOME
HOME=/home/ada
```

`env` ortam değişkenlerinin listesini yazar. Gerçek bir bilgisayarda bu liste
çok daha uzundur; içinden aradığını `grep` ile süzersin.

## PATH: komutlar nerede aranır

Bir komut yazdığında kabuk onu `PATH` değişkenindeki klasörlerde, soldan
sağa arar. Klasörler `:` ile ayrılır.

```text
~ $ echo $PATH
/usr/local/bin:/usr/bin:/bin
~ $ which ls
/usr/bin/ls
~ $ ls -l tools/greet
-rwxr-xr-x 1 ada ada 34 Oct  7 10:00 tools/greet*
~ $ greet
bash: greet: command not found
~ $ export PATH="$HOME/tools:$PATH"
~ $ echo $PATH
/home/ada/tools:/usr/local/bin:/usr/bin:/bin
~ $ greet
Hello from greet
~ $ which greet
/home/ada/tools/greet
```

- `which ls` komutun PATH'te nerede bulunduğunu söyler.
- `tools/greet` çalıştırılabilir olduğu hâlde `greet` bulunamadı: `tools`
  PATH'te değil.
- `export PATH="$HOME/tools:$PATH"` yeni klasörü başa ekledi ve **eski değeri
  korudu**. `$PATH`'i sona yazmayı unutsaydın PATH yalnızca `tools` olurdu ve
  `ls` bile bulunamazdı.

Bir program "kurduğun hâlde `command not found`" diyorsa sebep çoğu zaman
budur: kurulduğu klasör PATH'te değildir.

## Kalıcı yapmak: ~/.bashrc

Tanımladığın değişkenler, `export`'lar ve takma adlar (*alias*) terminal
kapanınca kaybolur. bash her yeni terminalde ev klasöründeki `.bashrc`
dosyasını okur; kalıcı olmasını istediğin satırlar oraya yazılır:

```text
~ $ cat .bashrc
# ~/.bashrc: bash reads this file when a new terminal opens.
# Aliases and settings written here last for every session.
~ $ echo "alias ll='ls -l'" >> .bashrc
~ $ ll names.txt
bash: ll: command not found
~ $ source .bashrc
~ $ ll names.txt
-rw-r--r-- 1 ada ada 47 Oct  7 10:00 names.txt
~ $ type ll
ll is aliased to `ls -l'
```

- `>>` ile satır dosyanın **sonuna** eklendi; `>` yazsaydın eski içerik
  silinirdi.
- Ekledikten hemen sonra `ll` çalışmadı: dosya yalnızca **yeni** bir terminal
  açılırken okunur. `source .bashrc` onu şu anki kabuğa okuttu.
- `type ll` bir adın ne olduğunu söyler: takma ad, kabuğun kendi komutu ya da
  bir program.

PATH eklemesi de genellikle `.bashrc`'ye yazılır:
`export PATH="$HOME/tools:$PATH"`.

## Özet

| Yazım | Ne yapar |
|---|---|
| `ad=değer` | Değişken tanımlar (boşluksuz) |
| `"$ad"`, `"${ad}"` | Değeri kullanır |
| `${ad:-varsayılan}` | Boşsa varsayılan |
| `$(komut)` | Komutun çıktısı |
| `$((a + b))` | Aritmetik |
| `export AD=değer` | Ortam değişkeni |
| `AD=değer komut` | Yalnızca o komut için |
| `env`, `printenv AD` | Ortamı gösterir |
| `unset ad` | Değişkeni kaldırır |
| `export PATH="$HOME/x:$PATH"` | PATH'e klasör ekler |
| `source ~/.bashrc` | Ayar dosyasını yeniden okur |
