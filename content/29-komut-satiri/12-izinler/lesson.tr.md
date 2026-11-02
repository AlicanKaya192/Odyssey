# İzinler ve chmod

Linux çok kullanıcılı bir sistemdir: aynı bilgisayarda birden fazla kişi, bir
web sunucusu, bir veritabanı çalışır. Kimin hangi dosyayı okuyabileceğine,
değiştirebileceğine ve çalıştırabileceğine **izinler** karar verir. Kendi
bilgisayarında da her gün karşına çıkarlar: yazdığın betiği ilk kez
çalıştırdığında büyük ihtimalle `Permission denied` göreceksin.

## İzinleri okumak

ls ile Ayrıntılı Bakmak bölümünde izin sütununu bu bölüme bırakmıştık. Şimdi
sırası geldi:

```text
~ $ ls -l notes.txt scripts/hello.sh
-rw-r--r-- 1 ada ada  9 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada 37 Oct  7 10:00 scripts/hello.sh
~ $ ls -ld private
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 private/
~ $ whoami
ada
~ $ id
uid=1000(ada) gid=1000(ada) groups=1000(ada)
```

<figure class="fig">
  <pre><code class="language-text">-rwxr-xr-- 1 ada ada 37 Oct  7 10:00 hello.sh</code></pre>
  <div class="anat">
    <div class="anat-row"><span>-</span><span>Tür: <code>-</code> dosya, <code>d</code> klasör.</span></div>
    <div class="anat-row"><span>rwx</span><span><b>Sahip</b> (user, <code>u</code>): okur, yazar, çalıştırır.</span></div>
    <div class="anat-row"><span>r-x</span><span><b>Grup</b> (group, <code>g</code>): okur, çalıştırır; yazamaz.</span></div>
    <div class="anat-row"><span>r--</span><span><b>Diğerleri</b> (others, <code>o</code>): yalnızca okur.</span></div>
    <div class="anat-row"><span>ada ada</span><span>Sahip kullanıcı ve grup.</span></div>
  </div>
  <figcaption>Dokuz harf üçerli üç gruptur. Harf yerine <code>-</code> varsa o izin yok.</figcaption>
</figure>

- Üç izin var: **r** okuma (*read*), **w** yazma (*write*), **x** çalıştırma
  (*execute*).
- Üç kişi grubu var: **sahip** (`u`, *user*), **grup** (`g`), **diğerleri**
  (`o`, *others*).
- `whoami` kim olduğunu, `id` hangi gruplarda olduğunu söyler. Bu terminalde
  sen `ada`'sın ve dosyaların sahibi de `ada`; bu yüzden ilk üçlü seni
  ilgilendirir.

`notes.txt` için `rw-r--r--`: sen okuyup yazarsın, başkaları yalnızca okur. Yeni
bir dosya hep böyle başlar; yeni bir klasör `rwxr-xr-x` ile.

## Çalıştırma izni: `+x`

```text
~ $ ./scripts/hello.sh
bash: ./scripts/hello.sh: Permission denied
~ $ echo $?
126
~ $ bash scripts/hello.sh
Hello from a script
~ $ chmod +x scripts/hello.sh
~ $ ls -l scripts/hello.sh
-rwxr-xr-x 1 ada ada 37 Oct  7 10:00 scripts/hello.sh*
~ $ ./scripts/hello.sh
Hello from a script
~ $ ls scripts
hello.sh*
```

- `./scripts/hello.sh` bir betiği **program gibi** çalıştırmaktır ve `x` ister.
  Kabuk çıkış kodu olarak `126` verdi: "buldum ama çalıştıramıyorum".
- `bash scripts/hello.sh` ise çalışır: burada çalışan program `bash`, betiği
  yalnızca **okur**; `r` yeter.
- `chmod +x` çalıştırma iznini ekledi; `ls` artık adın sonuna `*` koyuyor.

Betik yazmak sonraki bölümün konusu; orada her betik bu adımla başlayacak.

## Harflerle değiştirmek

`chmod` (*change mode*) şöyle okunur: **kim**, **ne yapılsın**, **hangi izin**.

| Kim | İşlem | İzin |
|---|---|---|
| `u` sahip | `+` ekle | `r` |
| `g` grup | `-` kaldır | `w` |
| `o` diğerleri | `=` tam olarak bu | `x` |
| `a` hepsi | | |

```text
~ $ chmod u-w notes.txt
~ $ ls -l notes.txt
-r--r--r-- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ echo Call Ada >> notes.txt
bash: notes.txt: Permission denied
~ $ chmod u+w notes.txt
~ $ chmod go-r notes.txt
~ $ ls -l notes.txt
-rw------- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ chmod g+w,o+r shared.txt
~ $ ls -l shared.txt
-rw-rw-r-- 1 ada ada 10 Oct  7 10:00 shared.txt
~ $ chmod a-w shared.txt
~ $ ls -l shared.txt
-r--r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
```

- `u-w` sahibinden yazmayı kaldırdı; `>>` artık dosyaya ekleyemiyor. Hatayı
  kabuk yazdı, çünkü dosyayı açmaya çalışan kabuktu.
- `go-r` grup ve diğerlerinden okumayı kaldırdı: dosya yalnızca senin.
- Virgülle birden çok değişiklik: `g+w,o+r`.
- `a-w` herkesten yazmayı kaldırır. Kim yazılmazsa (`+x` gibi) herkes sayılır.

## Sayılarla değiştirmek

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>r = 4</span><span>Okuma</span></div>
    <div class="anat-row"><span>w = 2</span><span>Yazma</span></div>
    <div class="anat-row"><span>x = 1</span><span>Çalıştırma</span></div>
    <div class="anat-row"><span>7 = 4+2+1</span><span><code>rwx</code></span></div>
    <div class="anat-row"><span>6 = 4+2</span><span><code>rw-</code></span></div>
    <div class="anat-row"><span>5 = 4+1</span><span><code>r-x</code></span></div>
    <div class="anat-row"><span>4</span><span><code>r--</code></span></div>
    <div class="anat-row"><span>0</span><span><code>---</code></span></div>
  </div>
  <figcaption>Her grup bir rakam: sahip, grup, diğerleri. <code>755</code> = <code>rwxr-xr-x</code>, <code>644</code> = <code>rw-r--r--</code>, <code>600</code> = <code>rw-------</code>.</figcaption>
</figure>

```text
~ $ chmod 600 notes.txt
~ $ ls -l notes.txt
-rw------- 1 ada ada 9 Oct  7 10:00 notes.txt
~ $ chmod 755 scripts/hello.sh
~ $ ls -l scripts/hello.sh
-rwxr-xr-x 1 ada ada 37 Oct  7 10:00 scripts/hello.sh*
~ $ chmod 444 shared.txt
~ $ ls -l shared.txt
-r--r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
~ $ chmod 644 notes.txt shared.txt
~ $ ls -l notes.txt shared.txt
-rw-r--r-- 1 ada ada  9 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada 10 Oct  7 10:00 shared.txt
```

Sayı her üçlüyü **baştan** yazar; harf yalnızca söylediğin izni değiştirir.
"Bir dosyaya çalıştırma ekle" için `+x`, "bu dosyanın izni tam olarak şu
olsun" için sayı kullanışlıdır. Ezberlemeye değer üç sayı: `644` sıradan dosya,
`755` program ve klasör, `600` yalnızca senin olan dosya.

`chmod 777` (herkes her şeyi yapar) hızlı bir çözüm gibi görünür ama herkesin
dosyanı değiştirip çalıştırmasına izin verir. Her zaman işin gerektirdiği **en
az** izni ver.

## Klasörlerde izinler

Klasörde harflerin anlamı biraz farklıdır:

- `r`: içindekileri listelemek (`ls`).
- `w`: içinde dosya oluşturmak, silmek, adını değiştirmek.
- `x`: içine girmek (`cd`) ve içindeki dosyalara **ulaşmak**.

```text
~ $ chmod 700 private
~ $ ls -ld private
drwx------ 2 ada ada 4096 Oct  7 10:00 private/
~ $ chmod u-x private
~ $ cd private
bash: cd: private: Permission denied
~ $ cat private/secret.txt
cat: private/secret.txt: Permission denied
~ $ chmod u+x private
~ $ cat private/secret.txt
the plan
```

`x` kalkınca yalnızca `cd` değil, içindeki dosyayı okumak da yasaklandı;
dosyanın kendi izni `rw-r--r--` olduğu hâlde. Dosyaya giden yoldaki her
klasörde `x` gerekir.

## Sistem dosyaları ve root

```text
~ $ ls -l /etc/passwd
-rw-r--r-- 1 root root 129 Oct  7 10:00 /etc/passwd
~ $ ls -ld /root /tmp
drwx------ 2 root root 4096 Oct  7 10:00 /root/
drwxrwxrwt 2 root root 4096 Oct  7 10:00 /tmp/
~ $ cd /root
bash: cd: /root: Permission denied
~ $ touch /etc/test.txt
touch: cannot touch '/etc/test.txt': Permission denied
~ $ touch /tmp/test.txt
~ $ ls -l /tmp/test.txt
-rw-r--r-- 1 ada ada 0 Oct  7 10:00 /tmp/test.txt
```

Sistemin kendi dosyaları **root** adlı yöneticiye aittir. `/etc/passwd`'yi
herkes okuyabilir ama yalnızca root değiştirebilir; `/root` root'un ev klasörü
ve başkasına tamamen kapalı. `/tmp` herkese açık bir geçici klasördür (sondaki
`t`, herkesin yalnızca kendi dosyasını silebileceği anlamına gelir).

Gerçek bir Linux'ta yönetici izni isteyen bir komutun başına `sudo` yazılır:
`sudo touch /etc/test.txt`. sudo şifreni sorar ve komutu root olarak
çalıştırır. Bu terminalde `sudo` yok; ayrıntısı ders notunda.

## Tuzaklar

```text
~ $ chmod abc notes.txt
chmod: invalid mode: 'abc'
Try 'chmod --help' for more information.
~ $ chmod 999 notes.txt
chmod: invalid mode: '999'
Try 'chmod --help' for more information.
~ $ chmod +x
chmod: missing operand after '+x'
Try 'chmod --help' for more information.
~ $ chmod 000 notes.txt
~ $ cat notes.txt
cat: notes.txt: Permission denied
~ $ chmod 644 notes.txt
```

- Geçersiz bir izin `invalid mode` verir; sayılar 0–7 arasıdır.
- Dosya adını unutursan `missing operand`.
- `chmod 000` dosyayı sahibine bile kapatır; ama sahibi izni geri verebilir.

## Özet

| Komut | Ne yapar |
|---|---|
| `ls -l`, `ls -ld klasör` | İzinleri gösterir |
| `chmod +x f` | Çalıştırma izni ekler |
| `chmod u-w f` | Sahibinden yazmayı kaldırır |
| `chmod go-r f` | Grup ve diğerlerinden okumayı kaldırır |
| `chmod 644 f` | `rw-r--r--` |
| `chmod 755 f` | `rwxr-xr-x` |
| `chmod 600 f` | `rw-------` |
| `chmod 700 klasör` | Yalnızca sahibi girer |

r = 4, w = 2, x = 1; rakamlar sahip, grup, diğerleri sırasıyla.
