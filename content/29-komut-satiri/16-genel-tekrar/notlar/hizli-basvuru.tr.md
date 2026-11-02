Patikanın bütün komutları, tek sayfada.

## Dolaşmak

| Komut | Ne yapar |
|---|---|
| `pwd` | Bulunduğun klasör |
| `ls`, `ls -la`, `ls -lh` | Listele; ayrıntı, gizliler, okunur boyut |
| `cd yol`, `cd ..`, `cd ~`, `cd -` | Git; üst, ev, önceki |
| `clear` (Ctrl+L) | Ekranı temizle |

## Dosya ve klasör

| Komut | Ne yapar |
|---|---|
| `mkdir -p a/b` | Klasör (üstleriyle) |
| `touch f` | Boş dosya |
| `cp f g`, `cp -r d e` | Kopyala; klasörle |
| `mv f g` | Taşı ya da adını değiştir |
| `rm f`, `rm -r d`, `rmdir d` | Sil (geri alınmaz) |

## İçine bakmak

| Komut | Ne yapar |
|---|---|
| `cat f`, `cat -n f` | Hepsi; numaralı |
| `head -n 5 f`, `tail -n 5 f` | Baş, son |
| `tail -n +2 f` | 2. satırdan sona |
| `wc -l f` | Satır sayısı |

## Joker

`*` herhangi bir metin, `?` tek karakter, `[abc]` biri, `{a,b}` ikisi de.
Kabuk genişletir; tırnak içinde açılmaz.

## Yönlendirme ve boru

| Yazım | Ne yapar |
|---|---|
| `k > f`, `k >> f` | Çıktı dosyaya; sona ekle |
| `k 2> f`, `k > f 2>&1` | Hatalar; ikisi birden |
| `k 2> /dev/null` | Hataları at |
| `k < f` | Girdi dosyadan |
| <code>a &#124; b</code> | a'nın çıktısı b'nin girdisi |

## Metin

| Komut | Ne yapar |
|---|---|
| `grep -i -n -c -v -w -o 'desen' f` | Satır ara |
| <code>grep -E 'A&#124;B'</code>, `grep -rl 'k' .` | Ya da; dosya adları |
| `sort -r -n -u`, `sort -t , -k 3` | Sırala |
| `uniq -c -d -u` | Komşu tekrarlar |
| `cut -d , -f 2`, `cut -c 1-10` | Alan, karakter |
| `tr a-z A-Z`, `tr -d x`, `tr -s ' '` | Çevir, sil, sıkıştır |

## Bulmak

`find yol -name '*.py' -type f -maxdepth 2`, `-iname`, `-not`,
`-exec k {} \;`, `-delete` (önce listele).

## İzinler

`ls -l` → `-rwxr-xr--` (sahip, grup, diğerleri). `chmod +x f`, `chmod u-w f`,
`chmod 644 f` (r=4 w=2 x=1). Klasörde `x` = içine girmek.

## Değişkenler

| Yazım | Ne yapar |
|---|---|
| `ad=değer`, `"$ad"`, `"${ad}"` | Tanımla, kullan |
| `$(komut)`, `$((a + 1))` | Çıktı, aritmetik |
| `export AD=değer`, `env` | Ortam |
| `export PATH="$HOME/bin:$PATH"` | PATH'e ekle |
| `source ~/.bashrc` | Ayarları yeniden oku |

## Betik ve çıkış kodu

| Yazım | Ne yapar |
|---|---|
| `#!/bin/bash`, `chmod +x`, `./b.sh` | Betik |
| `$1 $# "$@" $0` | Argümanlar |
| `if [ -f "$1" ]; then ...; fi` | Karar |
| `for x in ...; do ...; done` | Döngü |
| `exit 1`, `echo $?` | Çıkış kodu |
| `a && b`, <code>a &#124;&#124; b</code>, `a ; b` | Başarılıysa, başarısızsa, her durumda |
