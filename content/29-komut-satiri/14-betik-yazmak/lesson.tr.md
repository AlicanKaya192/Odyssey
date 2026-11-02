# Betik Yazmak

Aynı komutları her gün yeniden yazıyorsan onları bir dosyaya koyma zamanı
gelmiştir. Bir **betik** (script), komutların bir dosyaya yazılmış hâlidir;
dosyayı çalıştırınca komutlar yukarıdan aşağı sırayla çalışır. Bu bölümde
şimdiye kadar öğrendiğin her şey (değişkenler, yönlendirme, borular, izinler)
bir araya geliyor.

## İlk betik

<figure class="fig">
  <pre><code class="language-text">#!/bin/bash
# Greets the person given as the first argument.
echo "Hello, &#36;1!"</code></pre>
  <div class="anat">
    <div class="anat-row"><span>#!/bin/bash</span><span><b>Shebang</b>: ilk satır. "Bu dosyayı bash ile çalıştır" der.</span></div>
    <div class="anat-row"><span># ...</span><span>Yorum: <code>#</code> ile başlayan satırı kabuk atlar.</span></div>
    <div class="anat-row"><span>echo ...</span><span>Komutlar: terminale yazacağın komutların aynısı, yukarıdan aşağı sırayla.</span></div>
    <div class="anat-row"><span>&#36;1</span><span>Betiğe verilen ilk argüman.</span></div>
  </div>
  <figcaption>Betik, komutların bir dosyaya yazılmış hâlidir. Yeni bir şey öğrenmiyorsun; bildiklerini kaydediyorsun.</figcaption>
</figure>

```text
~ $ cat hello.sh
#!/bin/bash
# My first script
echo "Hello from a script"
echo "I am running in $PWD"
~ $ bash hello.sh
Hello from a script
I am running in /home/ada
~ $ ./hello.sh
bash: ./hello.sh: Permission denied
~ $ chmod +x hello.sh
~ $ ./hello.sh
Hello from a script
I am running in /home/ada
```

- `bash hello.sh`: bash dosyayı okuyup içindeki komutları çalıştırdı. Bunun
  için dosyayı okuyabilmek yeter.
- `./hello.sh`: dosyayı **program gibi** çalıştırmak. İzinler bölümünden
  hatırla: bunun için `x` izni gerekir; `chmod +x` sonrası çalıştı.
- `./hello.sh` ile çalışınca hangi programın kullanılacağını ilk satır,
  **shebang** (`#!/bin/bash`) söyler.

Gerçek bir bilgisayarda betiği bir düzenleyicide yazarsın (VS Code, nano).
Bu terminalde düzenleyici yok; betikler hazır geliyor, kendi betiğini ise
`echo` ve `>>` ile satır satır yazacaksın.

## Argümanlar

<figure class="fig">
  <pre><code class="language-text">./greet.sh Ada Grace Linus</code></pre>
  <div class="anat">
    <div class="anat-row"><span>&#36;0</span><span>Betiğin kendi adı: <code>./greet.sh</code></span></div>
    <div class="anat-row"><span>&#36;1 &#36;2 &#36;3</span><span>Sırayla argümanlar: <code>Ada</code>, <code>Grace</code>, <code>Linus</code></span></div>
    <div class="anat-row"><span>&#36;#</span><span>Argüman sayısı: <code>3</code></span></div>
    <div class="anat-row"><span>&#36;@</span><span>Argümanların hepsi; <code>"&#36;@"</code> diye tırnakla kullanılır</span></div>
  </div>
  <figcaption>Argüman, betiği her çalıştırışta farklı bir değerle kullanmanı sağlar.</figcaption>
</figure>

```text
~ $ bash greet.sh Ada
Hello, Ada!
You gave 1 arguments: Ada
This script is greet.sh
~ $ bash greet.sh Ada Grace Linus
Hello, Ada!
You gave 3 arguments: Ada Grace Linus
This script is greet.sh
~ $ bash greet.sh "Ada Lovelace"
Hello, Ada Lovelace!
You gave 1 arguments: Ada Lovelace
This script is greet.sh
~ $ bash greet.sh
Hello, !
You gave 0 arguments: 
This script is greet.sh
```

- `"Ada Lovelace"` tırnak içinde olduğu için **tek** argüman sayıldı.
- Argüman verilmeyince `$1` boş kaldı ve betik yine çalıştı: `Hello, !`. Bunu
  önlemek bir sonraki konunun işi.

## Karar vermek: if

```text
~ $ cat check.sh
#!/bin/bash
if [ -z "$1" ]; then
  echo "usage: check.sh FILE"
  exit 1
fi
if [ -f "$1" ]; then
  lines=$(wc -l < "$1")
  echo "$1 has $lines lines"
else
  echo "$1: no such file"
  exit 2
fi
~ $ bash check.sh
usage: check.sh FILE
~ $ bash check.sh notes.txt
notes.txt has 3 lines
~ $ bash check.sh nope.txt
nope.txt: no such file
```

```text
if [ koşul ]; then
  komutlar
else
  başka komutlar
fi
```

- `[ -z "$1" ]`: ilk argüman boş mu? Boşsa kullanım bilgisini yazıp `exit 1`
  ile çık. Betiğin geri kalanı hiç çalışmadı.
- `[ -f "$1" ]`: böyle bir dosya var mı?
- `exit` betiği bitirir; arkasındaki sayı **çıkış kodudur**. 0 "başarılı",
  başka her sayı "bir sorun var" demek. Çıkış kodları sonraki bölümün konusu.

`[ ... ]` aslında bir komuttur (`test`) ve köşeli parantezlerin **içinde
boşluk** olmak zorundadır. Komut satırında da çalışır:

```text
~ $ [ -f notes.txt ] && echo file
file
~ $ [ -d notes.txt ] || echo not a folder
not a folder
~ $ [ 3 -gt 2 ] && echo bigger
bigger
~ $ name=Ada
~ $ if [ "$name" = "Ada" ]; then echo hi Ada; else echo who; fi
hi Ada
```

| Sınama | Doğru olur, eğer |
|---|---|
| `-f yol` / `-d yol` / `-e yol` | Dosya / klasör / herhangi biri var |
| `-z "$a"` / `-n "$a"` | Metin boş / boş değil |
| `"$a" = "$b"` / `"$a" != "$b"` | Metinler eşit / farklı |
| `$a -eq $b`, `-ne`, `-lt`, `-le`, `-gt`, `-ge` | Sayı karşılaştırması |
| `! ...` | Tersi |

Sayılar için `-gt` gibi kısaltmalar kullanılır; `>` köşeli parantezin içinde
yönlendirme olur ve adı `0` olan bir dosya açar.

## Tekrarlamak: for ve while

```text
~ $ for name in Ada Grace Linus; do echo "Hi, $name"; done
Hi, Ada
Hi, Grace
Hi, Linus
~ $ for f in *.txt; do echo "file: $f"; done
file: notes.txt
file: todo.txt
~ $ cat backup.sh
#!/bin/bash
for f in "$@"; do
  cp "$f" "$f.bak"
  echo "saved $f.bak"
done
~ $ bash backup.sh notes.txt todo.txt
saved notes.txt.bak
saved todo.txt.bak
~ $ ls *.bak
notes.txt.bak  todo.txt.bak
```

```text
for değişken in liste; do
  komutlar
done
```

Liste düz kelimeler, bir joker (`*.txt`), `"$@"` (bütün argümanlar) ya da bir
komutun çıktısı (`$(seq 1 5)`) olabilir. `backup.sh` kendisine verilen her
dosyanın kopyasını aldı.

```text
~ $ cat countdown.sh
#!/bin/bash
n=$1
while [ $n -gt 0 ]; do
  echo $n
  n=$((n - 1))
done
echo "Go!"
~ $ bash countdown.sh 3
3
2
1
Go!
~ $ for i in $(seq 1 3); do touch "day$i.txt"; done
~ $ ls day*
day1.txt  day2.txt  day3.txt
```

`while` koşul doğru olduğu sürece döner. `n=$((n - 1))` her turda sayıyı
azaltıyor; azaltmayı unutursan döngü hiç bitmez. Kısa döngüler betik
gerektirmez, komut satırında tek satırda da yazılır.

## Fonksiyonlar

```text
~ $ cat report.sh
#!/bin/bash
count_lines() {
  local file=$1
  wc -l < "$file"
}
for f in *.txt; do
  echo "$f: $(count_lines "$f") lines"
done
~ $ bash report.sh
notes.txt: 3 lines
todo.txt: 1 lines
```

Fonksiyon bir komut grubuna ad verir: `count_lines() { ... }`. Çağırırken
diğer komutlar gibi argüman alır ve içeride onlar `$1`, `$2` olur.
`local` değişkeni fonksiyona ait yapar; dışarıdaki aynı adlı değişkene
dokunmaz.

## Kendi betiğini yazmak

```text
~ $ echo '#!/bin/bash' > hi.sh
~ $ echo 'echo "Hi there"' >> hi.sh
~ $ cat hi.sh
#!/bin/bash
echo "Hi there"
~ $ chmod +x hi.sh
~ $ ./hi.sh
Hi there
```

Satırları tek tırnak içinde yazdık: tek tırnak `!`'ı ve içteki çift tırnakları
olduğu gibi dosyaya geçirir. İlk satır `>` ile dosyayı açtı, sonrakiler `>>` ile
eklendi.

## Tuzaklar

```text
~ $ hello.sh
bash: hello.sh: command not found
~ $ bash countdown.sh
countdown.sh: line 3: [: -gt: unary operator expected
Go!
~ $ bash nope.sh
bash: nope.sh: No such file or directory
```

- `hello.sh` tek başına bulunamaz: kabuk komutları PATH'te arar ve bulunduğun
  klasör PATH'te değil. `./hello.sh` "buradaki dosya" demek.
- Argüman verilmeyince `$n` boş kaldı; `[ -gt 0 ]` eksik bir sınama oldu. Betik
  hata verdi ama **durmadı**; `Go!` yine yazıldı. Argümanları denetle ya da
  varsayılan ver: `n=${1:-3}`.
- Değişkenleri hep çift tırnakla kullan: `"$1"`, `"$f"`. Boşluklu bir dosya
  adı tırnaksız iki ayrı kelimeye bölünür.

Gerçek bir terminalde `bash -x betik.sh` her komutu çalışmadan önce `+` ile
yazar; betiğin nerede yanlış gittiğini görmenin en kolay yolu. `case`
(çok seçenekli karar) ve `read` (klavyeden girdi okumak) da betiklerde sık
kullanılır; bu terminalde yoklar.

## Özet

| Parça | Yazım |
|---|---|
| İlk satır | `#!/bin/bash` |
| Çalıştırmak | `bash betik.sh` ya da `chmod +x` + `./betik.sh` |
| Argümanlar | `$1`, `$2`, `$#`, `"$@"`, `$0` |
| Karar | `if [ ... ]; then ... else ... fi` |
| Döngü | `for x in ...; do ... done`, `while [ ... ]; do ... done` |
| Fonksiyon | `ad() { ...; }`, içinde `local` |
| Bitirmek | `exit 0` başarılı, `exit 1` sorun |
