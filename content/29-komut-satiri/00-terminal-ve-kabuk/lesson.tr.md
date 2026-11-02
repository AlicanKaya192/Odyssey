# Terminal, Kabuk ve İstem

Bilgisayarı çoğu zaman fareyle kullanıyorsun: klasöre çift tıklıyorsun, dosyayı
sürükleyip bırakıyorsun. Bu yöntemin adı **görsel arayüz**. Aynı işleri bir de
**yazarak** yapmanın yolu var: bir komut yazarsın, bilgisayar onu yapar. Buna
**komut satırı** deniyor.

Bu patikada komut satırını sıfırdan öğreneceğiz. Önce neden işine yarayacağını,
sonra terminalin parçalarını, en sonda da ilk komutlarını göreceksin.

## Neden komut satırı?

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Görsel arayüz</h4><p>Fareyle tıklarsın</p><p>Gördüğün düğmeler kadar</p><p>Aynı işi 100 kez elle yaparsın</p></div>
    <div class="ok"><h4>Komut satırı</h4><p>Komutu yazarsın</p><p>Her program, her seçenek</p><p>Bir kez yazar, istediğin kadar tekrarlarsın</p></div>
  </div>
  <figcaption>İkisi aynı işi yapar; komut satırı tekrar eden ve uzaktaki işlerde öne geçer.</figcaption>
</figure>

Görsel arayüz bir işi **bir kez** yapmak için rahattır. Ama şu durumları düşün:

- 300 fotoğrafın adını tek tek değiştirmen gerekiyor.
- Bir sunucuda (internetteki başka bir bilgisayarda) çalışıyorsun ve orada
  ekran, fare, pencere hiçbiri yok.
- Her sabah aynı beş adımı tekrarlıyorsun.

Komut satırında bu işler bir satır, ya da birkaç satırlık bir **betik**
(komutları sırayla yazdığın küçük dosya) olur. Git, Docker, Python
ortamları, sunucular, veri bilimi araçları: hepsi önce komut satırından
kullanılır. Görsel araçlar da çoğu zaman arkada bu komutları çalıştırır.

## Terminal ve kabuk: iki ayrı şey

İki kelimeyi birbirine karıştırmamak gerekiyor.

- **Terminal**, yazdığın metni ve gelen cevabı gösteren **penceredir**.
- **Kabuk** (İngilizcesi *shell*), yazdığın satırı okuyup anlayan ve
  çalıştıran **programdır**.

<figure class="fig">
  <div class="flow">
    <span class="node">Sen<br><small>klavyeden yazarsın</small></span><span class="arrow">→</span>
    <span class="node">Terminal<br><small>pencere</small></span><span class="arrow">→</span>
    <span class="node acc">Kabuk (bash)<br><small>komutu okur, çalıştırır</small></span><span class="arrow">→</span>
    <span class="node">İşletim sistemi<br><small>dosyalar, programlar</small></span>
  </div>
  <figcaption>Terminal yalnızca yazdığını gösteren pencere. Komutu anlayan ve çalıştıran program kabuk.</figcaption>
</figure>

Linux'ta en yaygın kabuğun adı **bash**. macOS'ta varsayılan kabuk *zsh*, ama
komutların neredeyse hepsi aynıdır. Windows'ta bash'i iki yoldan
kullanabilirsin: Git ile birlikte gelen **Git Bash** ya da Windows içinde
gerçek bir Linux çalıştıran **WSL**. Bu patikada öğrendiğin her şey üçünde de
geçerli.

> Odyssey'deki terminal gerçek bash gibi davranır ama bilgisayarındaki
> dosyalara dokunmaz: dosyalar, klasörler, hepsi Odyssey'nin içinde, sana ait
> küçük bir Linux bilgisayarında duruyor. Bir şeyi bozarsan **Baştan başla**
> düğmesi yeter.

## İstem (prompt)

Terminal açılınca bir satırın başında şunun gibi bir yazı görürsün:

```text
~ $
```

Buna **istem** (İngilizcesi *prompt*) deniyor. İstem iki şey söyler: şu an
hangi klasördesin ve kabuk senden komut bekliyor. `$` işaretinden sonrasını
sen yazarsın.

<figure class="fig">
  <pre><code class="language-text">~/notes $ ls -a docs</code></pre>
  <div class="anat">
    <div class="anat-row"><span>~/notes</span><span>Şu an bulunduğun klasör. <code>~</code> ev klasörün demek.</span></div>
    <div class="anat-row"><span>$</span><span>İstemin sonu: kabuk komut bekliyor.</span></div>
    <div class="anat-row"><span>ls</span><span>Komut: çalıştırılacak programın adı.</span></div>
    <div class="anat-row"><span>-a</span><span>Seçenek: komutun nasıl çalışacağını değiştirir. Tire ile başlar.</span></div>
    <div class="anat-row"><span>docs</span><span>Argüman: komutun üzerinde çalışacağı şey (burada bir klasör).</span></div>
  </div>
  <figcaption>Her komut satırı aynı düzende: komut, sonra seçenekler, sonra argümanlar; aralarında boşluk.</figcaption>
</figure>

`~` (tilde) işareti **ev klasörün** demek: sana ait dosyaların durduğu klasör.
Bu terminalde ev klasörünün tam adı `/home/ada`. Gerçek bir Linux'ta istem
genellikle biraz daha uzundur, kullanıcı adını ve bilgisayarın adını da
gösterir: `ada@laptop:~$`. Anlamı aynı.

> Ders örneklerinde satır `$` ile başlıyorsa o satır **senin yazdığın**
> komuttur; altındaki satırlar komutun cevabı. `$` işaretini yazmazsın.

## İlk komutlar

Üç komutla başlayalım:

- `pwd` (*print working directory*): bulunduğun klasörün tam yolunu yazar.
- `ls` (*list*): bulunduğun klasördekileri listeler.
- `echo`: arkasına yazdığın metni olduğu gibi geri yazar.

```text
~ $ pwd
/home/ada
~ $ ls
notes/  projects/  todo.txt
~ $ echo Hello
Hello
~ $ echo "Hello, terminal"
Hello, terminal
```

`ls` çıktısında adın sonunda `/` olanlar **klasör**, olmayanlar **dosya**.
(Bu terminal ve Git Bash klasörleri böyle gösterir; bazı sistemlerde bunun
yerine renk kullanılır.)

## Komutun yapısı: komut, seçenek, argüman

Bir komut satırı her zaman aynı düzendedir:

```text
komut  seçenekler  argümanlar
```

- **Komut**: çalıştırılacak programın adı (`ls`).
- **Seçenek** (option, flag): komutun nasıl çalışacağını değiştirir. Tire ile
  başlar: `-a`.
- **Argüman**: komutun üzerinde çalışacağı şey: bir dosya, bir klasör, bir
  metin.

Aralarında **boşluk** olmak zorunda. `ls -a` iki parçadır; `ls-a` yazarsan
kabuk `ls-a` adında bir komut arar ve bulamaz.

`ls -a` gizli dosyaları da gösterir. Linux'ta adı nokta ile başlayan dosya ya
da klasör **gizlidir**; normal `ls` onları göstermez.

```text
~ $ ls notes
plan.txt
~ $ ls -a notes
./  ../  .draft  plan.txt
~ $ ls -a
./  ../  .bashrc  notes/  projects/  todo.txt
```

`ls -a` iki tuhaf ad ekledi: `./` bulunduğun klasörün kendisi, `../` bir
üstteki klasör. İkisini bir sonraki bölümde ayrıntılı göreceğiz. Ev
klasöründe bir de `.bashrc` göründü: bash'in ayar dosyası. Adı noktayla
başladığı için normal `ls` onu göstermiyordu.

Seçenekler birleştirilebilir: `ls -a -l` yerine `ls -al` yazılabilir. Bunu
ilerideki bölümlerde sık kullanacağız.

## Hata mesajlarını okumak

Terminal yanlış yazdığında sana kızmaz, ne olduğunu söyler. Hata mesajını
okumak bu işin yarısıdır.

```text
~ $ Ls
bash: Ls: command not found
~ $ sl
bash: sl: command not found
~ $ ls nope
ls: cannot access 'nope': No such file or directory
```

- `command not found`: böyle bir komut yok. Çoğu zaman yazım hatasıdır.
- Linux'ta **büyük ve küçük harf farklıdır**: `Ls` ile `ls` aynı şey değil.
  Dosya adlarında da öyle: `Notes.txt` ile `notes.txt` iki ayrı dosya.
- `No such file or directory`: komut doğru, ama verdiğin dosya ya da klasör
  orada yok.

## Boşluklar ve tırnaklar

Kabuk satırı **boşluklardan** parçalara ayırır. Bu yüzden arka arkaya birkaç
boşluk, kabuğun gözünde tek bir ayraçtır:

```text
~ $ echo Hello     world
Hello world
~ $ echo "Hello     world"
Hello     world
```

İlk komutta `echo` iki ayrı argüman aldı (`Hello` ve `world`) ve onları tek
boşlukla birleştirdi. İkincisinde tırnaklar metni **tek bir argüman** yaptı;
içindeki boşluklar olduğu gibi kaldı. Tırnakları daha çok kullanacağız: adında
boşluk olan bir dosyayı da tırnakla yazarsın.

## Geçmiş ve kısayollar

Kabuk yazdığın komutları hatırlar. **Yukarı ok** tuşu bir önceki komutu
getirir; tekrar basınca daha öncekini. `history` komutu bu oturumda
yazdıklarının hepsini numaralarıyla listeler:

```text
~ $ pwd
/home/ada
~ $ echo hi
hi
~ $ history
    1  pwd
    2  echo hi
    3  history
```

Gerçek bir terminalde işini kolaylaştıran birkaç tuş daha var:

| Tuş | Ne yapar |
|---|---|
| Yukarı / aşağı ok | Önceki / sonraki komut |
| `Ctrl+L` ya da `clear` | Ekranı temizler |
| `Ctrl+C` | Çalışan komutu durdurur (kopyalamaz!) |
| `Tab` | Komutun ya da dosya adının devamını tamamlar |

Odyssey'nin terminalinde ok tuşları, `Ctrl+L` ve `clear` çalışır; `Tab` ile
tamamlama yok, adları kendin yazarsın.

## Özet

- **Terminal** pencere, **kabuk** (bash) komutu okuyup çalıştıran program.
- **İstem** nerede olduğunu gösterir; `~` ev klasörün, `$` "komut bekliyorum".
- Komut satırı: **komut, seçenek, argüman**, aralarında boşluk.
- `pwd` neredesin, `ls` neler var, `ls -a` gizlilerle birlikte, `echo` metni
  yazar.
- Büyük-küçük harf önemli; boşluklu metin tırnak içine.
- Hata mesajı ne olduğunu söyler: önce oku.
