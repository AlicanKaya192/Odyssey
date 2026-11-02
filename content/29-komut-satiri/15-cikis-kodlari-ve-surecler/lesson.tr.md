# Çıkış Kodları, Süreçler ve Ötesi

Her komut bittiğinde ekrana yazdıklarının yanında görünmeyen bir şey daha
bırakır: başarılı olup olmadığını söyleyen bir sayı. Betikler, `&&` ile
kurulan zincirler ve GitHub Actions gibi otomatik sistemler bu sayıya bakarak
karar verir. Bölümün ikinci yarısında, bu terminalin benzetemediği ama gerçek
bir terminalde her gün kullanacağın şeylere bakacağız: süreçler, paket
yöneticileri, yardım sayfaları ve uzak sunucular.

## Çıkış kodu: `$?`

```text
~ $ ls docs
a.md  b.md
~ $ echo $?
0
~ $ grep zzz names.txt
~ $ echo $?
1
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ echo $?
2
~ $ ./names.txt
bash: ./names.txt: Permission denied
~ $ echo $?
126
~ $ nosuchcmd
bash: nosuchcmd: command not found
~ $ echo $?
127
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>0</span><span><b>Başarılı.</b> Tek "iyi" kod budur.</span></div>
    <div class="anat-row"><span>1</span><span>Genel hata; grep'te "bulunamadı".</span></div>
    <div class="anat-row"><span>2</span><span>Yanlış kullanım: dosya yok (ls, grep), geçersiz seçenek.</span></div>
    <div class="anat-row"><span>126</span><span>Komut bulundu ama çalıştırılamadı (x izni yok).</span></div>
    <div class="anat-row"><span>127</span><span>Komut bulunamadı.</span></div>
    <div class="anat-row"><span>130</span><span>Ctrl+C ile durduruldu.</span></div>
  </div>
  <figcaption>Her komut bitince 0–255 arası bir sayı bırakır. Hangi hatanın hangi sayıyla geleceğine her program kendisi karar verir; 0 dışındaki her şey "bir sorun var" demektir.</figcaption>
</figure>

`$?` son komutun çıkış kodunu tutar. Hangi hatanın hangi sayıyla geleceğine
her program kendisi karar verir; ortak olan yalnızca **0 = başarılı**. grep'te
"bulamadım" 1, ls'te "dosya yok" 2. Komut bulunamazsa kabuk 127, bulup
çalıştıramazsa 126 verir.

## `$?` yalnızca son komutundur

```text
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ echo $?
2
~ $ echo $?
0
~ $ grep zzz names.txt | wc -l
0
~ $ echo $?
0
```

- İkinci `echo $?` 0 verdi: artık ilk `echo`'nun kodunu gösteriyor. Kodu
  kullanacaksan hemen oku ya da bir değişkene al: `code=$?`.
- Borunun çıkış kodu **en sondaki** komutundur. grep hiçbir şey bulamadı ama
  `wc` başarılı olduğu için zincir 0 verdi. (Gerçek betiklerde
  `set -o pipefail` bunu değiştirir.)

## Koda göre zincirlemek: `&&`, `||`, `;`

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>a ; b</span><span>Önce a, sonra <b>her durumda</b> b.</span></div>
    <div class="anat-row"><span>a &amp;&amp; b</span><span>b yalnızca a <b>başarılıysa</b> (0) çalışır.</span></div>
    <div class="anat-row"><span>a &#124;&#124; b</span><span>b yalnızca a <b>başarısızsa</b> çalışır.</span></div>
    <div class="anat-row"><span>! a</span><span>a'nın sonucunu ters çevirir.</span></div>
  </div>
  <figcaption>"Bu olduysa şunu yap" demenin en kısa yolu. Betikte aynı işi <code>if</code> yapar.</figcaption>
</figure>

```text
~ $ mkdir reports && echo created
created
~ $ mkdir reports && echo created
mkdir: cannot create directory 'reports': File exists
~ $ mkdir reports || echo already there
mkdir: cannot create directory 'reports': File exists
already there
~ $ ls nope; echo still runs
ls: cannot access 'nope': No such file or directory
still runs
~ $ grep -q ada names.txt && echo found
found
~ $ grep -q ERROR app.log || echo no errors
no errors
```

- `&&`: önceki başarılıysa devam et. Klasör ikinci kez açılamadı, `created`
  yazılmadı.
- `||`: önceki başarısızsa bunu yap; "olmazsa şu" demek.
- `;` yalnızca sıradır, sonuca bakmaz.
- `grep -q` hiçbir şey yazmaz; yalnızca kodla cevap verir. `&&` ve `||` ile en
  sık kullanılan komutlardan biri.

`!` bir komutun sonucunu ters çevirir: `! grep -q ERROR app.log && echo ok`,
"ERROR yoksa ok yaz" demek.

## if de koda bakar

```text
~ $ if grep -q WARN app.log; then echo warnings; else echo clean; fi
warnings
~ $ if [ -d docs ]; then echo folder; fi
folder
```

`if` aslında bir komutun çıkış koduna bakar. `[ -d docs ]` de bir komut
olduğu için Betik Yazmak bölümündeki `if [ ... ]` yazımı aynı kuralın özel bir
hâliydi. `grep -q` gibi bir komutu doğrudan koşul olarak yazabilirsin.

## Betiğin kendi kodu: exit

```text
~ $ cat check_file.sh
#!/bin/bash
if [ ! -f "$1" ]; then
  echo "missing: $1"
  exit 3
fi
echo "found: $1"
~ $ bash check_file.sh names.txt
found: names.txt
~ $ echo $?
0
~ $ bash check_file.sh nope.txt
missing: nope.txt
~ $ echo $?
3
~ $ bash check_file.sh nope.txt || echo the check failed
missing: nope.txt
the check failed
```

Betik `exit 3` ile bittiği için çağıran tarafta `$?` 3 oldu ve `||` devreye
girdi. `exit` yazılmazsa betiğin kodu, çalıştırdığı son komutun kodudur.
Kendi betiklerinde başarıda `exit 0`, her hata türü için ayrı bir sayı vermek
çağıranın işini kolaylaştırır. CI sistemleri (GitHub Actions) bir adımın
geçip geçmediğine tam olarak bu sayıyla karar verir.

## Süreçler

Bu terminal gerçek programlar çalıştırmaz, her şeyi kendi içinde benzetir; bu
yüzden aşağıdakiler burada yok. Gerçek bir terminalde sık kullanacaksın:

| Komut | Ne yapar |
|---|---|
| `ps` / `ps aux` | Çalışan süreçleri listeler (her birinin bir PID numarası var) |
| `top` / `htop` | Süreçleri canlı izler: işlemci ve bellek kullanımı |
| Ctrl+C | Öndeki komutu durdurur (çıkış kodu 130) |
| `kill PID` | Bir sürece durma isteği gönderir; `kill -9 PID` zorla durdurur |
| `komut &` | Komutu arka planda başlatır, istem hemen geri gelir |
| `jobs`, `fg`, `bg` | Arka plandaki işleri listeler, öne ya da arkaya alır |
| Ctrl+Z | Öndeki komutu durdurmaz, askıya alır (`fg` ile devam) |

**Süreç** (*process*) çalışmakta olan bir programdır. Terminali kapatınca
oradan başlatılan süreçler de genellikle kapanır.

## Ötesi: gerçek terminalde

| Konu | Örnek | Ne işe yarar |
|---|---|---|
| Yardım | `man ls`, `ls --help` | Her komutun bütün seçenekleri |
| Paket yöneticisi | `sudo apt install tree`, `brew install tree` | Program kurmak |
| Uzak sunucu | `ssh ada@sunucu` | Başka bir bilgisayarda komut satırı |
| Dosya göndermek | `scp dosya ada@sunucu:` | Sunucuya kopyalamak |
| İndirmek | `curl -O adres` | İnternetten dosya |
| Sayfalı okumak | `less dosya` | Uzun dosyada gezinmek (`q` çıkar) |

Windows'ta gerçek bir Linux terminali için WSL (Windows Subsystem for Linux)
kurulabilir; Git Bash da bu patikadaki komutların çoğunu çalıştırır.

## Özet

- `$?` son komutun kodu; 0 başarılı, başka her şey sorun.
- `a && b` başarılıysa, `a || b` başarısızsa, `a ; b` her durumda.
- Borunun kodu sondaki komutundur.
- `if` bir komutun koduna bakar; `grep -q` ve `[ ]` iki örnek.
- Betik `exit N` ile kendi kodunu seçer.
- Süreçler: `ps`, `kill`, Ctrl+C, `&`; yardım: `man`.
