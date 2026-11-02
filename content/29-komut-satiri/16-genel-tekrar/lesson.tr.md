# Genel Tekrar

Bu patikada terminali açmaktan kendi betiğini yazmaya kadar geldin. Bu bölüm
hepsini bir arada kullanıyor: önce küçük bir sunucu kaydını ve dağınık bir
klasörü baştan sona inceleyeceğiz, sonra bölümleri tek bir tabloda
toparlayacağız. Sınavda 40 soru ve beş karma alıştırma var; her alıştırma
birkaç bölümün aracını birlikte istiyor.

## Bir klasöre ilk bakış

```text
~ $ ls
inbox/  server.log  tools/
~ $ ls inbox
a.log  b.log  cache/  data.csv  draft.tmp  notes.txt  old.tmp
~ $ find . -type f | wc -l
10
~ $ find . -name '*.tmp'
./inbox/cache/page.tmp
./inbox/draft.tmp
./inbox/old.tmp
```

`ls` neyin nerede olduğunu, `find` kaç dosya olduğunu söyledi. Sayıya ev
klasöründeki gizli `.bashrc` da girdi. `.tmp` dosyaları geçici: alıştırmalardan
birinde onları temizleyeceksin.

## Kayıttan özet çıkarmak

```text
~ $ wc -l server.log
16 server.log
~ $ grep -c ERROR server.log
6
~ $ grep ERROR server.log | cut -d ' ' -f 4- | sort | uniq -c | sort -rn
      3 db timeout
      2 disk full
      1 login failed
```

Üç komutta kaydın büyüklüğünü, kaç hata olduğunu ve hangi hatanın kaç kez
geldiğini öğrendik. Son satır patikanın en çok işe yarayan kalıbı: süz (`grep`),
kes (`cut`), sırala (`sort`), say (`uniq -c`), sayıya göre sırala (`sort -rn`).

## İşi betiğe vermek

```text
~ $ cat tools/report.sh
#!/bin/bash
if [ ! -f "$1" ]; then
  echo "report: $1 not found"
  exit 2
fi
echo "$1: $(wc -l < "$1") lines, $(grep -c ERROR "$1") errors"
~ $ bash tools/report.sh server.log
server.log: 16 lines, 6 errors
~ $ bash tools/report.sh nope.log || echo "code: $?"
report: nope.log not found
code: 2
```

Aynı soruyu her gün soracaksan betik yaz. `report.sh` argümanını denetliyor,
yoksa kendi çıkış koduyla (2) bitiyor; `||` bunu yakaladı.

## Patikanın haritası

| Bölüm | Akılda kalması gereken |
|---|---|
| Terminal, Kabuk ve İstem | Terminal pencere, kabuk (bash) komutu çalıştıran program |
| Dosya Sistemi ve Yollar | `pwd`, `cd`, `ls`; mutlak (`/`) ve göreli yol, `~`, `..` |
| Dosya ve Klasör Oluşturmak | `mkdir -p`, `touch`, `rmdir`, `echo "..." > dosya` |
| Kopyalamak, Taşımak, Silmek | `cp -r`, `mv`, `rm`, `rm -r`; çöp kutusu yok |
| ls ile Ayrıntılı Bakmak | `ls -l`, `-a`, `-h`, `-R` |
| Joker Karakterler | `*`, `?`, `[ ]`, `{a,b}`; kabuk genişletir |
| Dosyanın İçine Bakmak | `cat`, `head`, `tail`, `wc` |
| Yönlendirme | `>`, `>>`, `2>`, `2>&1`, `<`, `/dev/null` |
| Borular | <code>a &#124; b</code>; boruda `ls` tek sütun |
| grep | `-i -n -c -v -w -o -E -r -l`, düzenli ifadeler |
| Metin Araçları | `sort`, `uniq`, `cut`, `tr` |
| find | `-name`, `-type`, `-maxdepth`, `-exec`, `-delete` |
| İzinler | `rwx`, `chmod +x`, `chmod 644/755/600` |
| Değişkenler ve Ortam | `ad=değer`, `"$ad"`, `$( )`, `export`, PATH, `.bashrc` |
| Betik Yazmak | shebang, `$1 $# "$@"`, `if`, `for`, `while`, fonksiyon |
| Çıkış Kodları | `$?`, `&&`, <code>&#124;&#124;</code>, `exit`, süreçler |

## Tekrar eden üç ders

1. **Tırnak.** Boşluk, `*`, `$` ya da `|` içeren her şeyi tırnakla. Tek tırnak
   hiçbir şeyi açmaz; çift tırnak değişkenleri açar.
2. **Önce bak, sonra değiştir.** `rm`, `find -delete` ve `>` geri alınmaz.
   Önce `ls`, `find` ya da `cat` ile ne olacağını gör.
3. **Küçük parçalar.** Bir boruyu ya da betiği adım adım kur; her adımdan
   sonra çıktıya bak.

Ders notlarında patikanın bütün komutlarını tek sayfada toplayan bir "Hızlı
Başvuru" ve buradan sonra neler öğrenebileceğini anlatan "Buradan Sonrası"
var.
