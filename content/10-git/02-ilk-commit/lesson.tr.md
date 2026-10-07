# İlk Commit: Üç Alan

Git kuruldu, adını biliyor. Artık ilk commit'i atabiliriz. Ama önce Git'in
dosyalarına nasıl baktığını anlamamız gerekiyor; bu bölümün asıl konusu bu.
Git'teki komutların yarısı, burada anlatacağımız **üç alan** arasında dosya
taşımaktan ibaret.

## Üç alan

<figure class="fig">
  <div class="flow">
    <span class="node">Çalışma alanı<br><small>klasördeki dosyalar</small></span><span class="arrow">→</span>
    <span class="node acc">git add</span><span class="arrow">→</span>
    <span class="node">Hazırlık alanı<br><small>bir sonraki commit</small></span><span class="arrow">→</span>
    <span class="node acc">git commit</span><span class="arrow">→</span>
    <span class="node ok">Depo<br><small>kalıcı geçmiş (.git)</small></span>
  </div>
  <figcaption>Değişiklik önce çalışma alanında olur, git add ile hazırlık alanına, git commit ile depoya geçer.</figcaption>
</figure>

1. **Çalışma alanı** (*working tree*): klasördeki dosyaların şu anki hâli.
   Düzenlediğin, sildiğin, oluşturduğun her şey önce burada olur. Git burada
   hiçbir şeyi kendiliğinden kaydetmez.
2. **Hazırlık alanı** (*staging area*, *index*): bir sonraki commit'e
   **girecek** değişikliklerin toplandığı yer. `git add` bir değişikliği
   buraya koyar.
3. **Depo** (*repository*): commit'lerin, yani kalıcı geçmişin durduğu yer
   (`.git` klasörü). `git commit` hazırlık alanındakileri tek bir commit
   olarak buraya yazar.

### Neden arada bir hazırlık alanı var?

Bir öğleden sonra üç şey yaptığını düşün: ana sayfaya bir başlık ekledin,
iletişim sayfasındaki yazım hatasını düzelttin, bir de kendine not dosyası
açtın. Bunları tek commit'e koyarsan geçmişte "neler oldu?" sorusunun cevabı
karışık olur; not dosyası ise hiç commit'lenmemeli.

Hazırlık alanı **neyin commit'e gireceğini seçmeni** sağlar: önce başlığı
ekleyip commit'lersin, sonra yazım düzeltmesini; not dosyası dışarıda kalır.
Her commit tek bir anlamlı iş anlatır.

## Boş bir depo

Yeni bir depoda `git status` (durum) şunu söyler:

```text
~/site $ git init
Initialized empty Git repository in /home/ada/site/.git/
~/site (main) $ git status
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`git status` Git'teki en önemli komut. Ne yapacağını bilmediğinde, bir
komuttan önce ve sonra: `git status`. Çıktısı hem durumu hem de **bir sonraki
adımda ne yazabileceğini** söyler (parantez içindeki `use "git add"…`
satırları).

## Dosya ekleyince: izlenmeyen dosyalar

İki dosya oluşturalım:

```text
~/site (main) $ echo "<h1>Hello</h1>" > index.html
~/site (main) $ echo "body {}" > style.css
~/site (main) $ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html
        style.css

nothing added to commit but untracked files present (use "git add" to track)
```

Git dosyaları gördü ama **izlemiyor** (*untracked*): bunlar Git'in
geçmişinde hiç olmamış dosyalar. Git onları sen istemeden commit'lere
koymaz.

## `git add`: hazırlık alanına koymak

```text
~/site (main) $ git add index.html
~/site (main) $ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   index.html

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        style.css
```

`index.html` artık **Changes to be committed** (commit'e girecek
değişiklikler) altında, yeşil ve `new file` olarak. `style.css` hâlâ
izlenmiyor, çünkü onu eklemedik.

`git add` başarılı olunca hiçbir şey yazmaz. Ne olduğunu görmek için
`git status`.

| Komut | Hazırlık alanına koyar |
|---|---|
| `git add index.html` | Yalnızca o dosyayı. |
| `git add index.html style.css` | Saydığın dosyaları. |
| `git add .` | Bulunduğun klasördeki (ve altındaki) bütün değişiklikleri. |
| `git add -A` | Deponun tamamındaki bütün değişiklikleri, hangi klasörde olursan ol. |

`git add .` çok kullanışlı ama dikkatli ol: istemediğin dosyaları da
(şifreli bir ayar dosyası, büyük bir veri dosyası) ekleyebilir. Önce
`git status` ile neler eklenecek bak. İstemediğin dosyaları kalıcı olarak
dışarıda tutmayı 05'te göreceğiz.

## `git commit`: fotoğrafı çekmek

```text
~/site (main) $ git commit -m "Add home page"
[main (root-commit) 5ab7f19] Add home page
 1 file changed, 1 insertion(+)
 create mode 100644 index.html
~/site (main) $ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        style.css

nothing added to commit but untracked files present (use "git add" to track)
```

Çıktıyı okuyalım:

<figure class="fig">
  <pre><code class="language-text">[main (root-commit) 5ab7f19] Add home page
 1 file changed, 1 insertion(+)
 create mode 100644 index.html</code></pre>
  <div class="anat">
    <div class="anat-row"><span>main</span><span>Commit'in atıldığı dal.</span></div>
    <div class="anat-row"><span>(root-commit)</span><span>Deponun ilk commit'i; öncesi yok. Sonraki commit'lerde yazmaz.</span></div>
    <div class="anat-row"><span>5ab7f19</span><span>Commit'in kimliğinin (hash) kısa hâli. Her commit'te farklı.</span></div>
    <div class="anat-row"><span>Add home page</span><span>Senin mesajın.</span></div>
    <div class="anat-row"><span>1 file changed…</span><span>Kaç dosya değişti, kaç satır eklendi (+) ya da silindi (-).</span></div>
    <div class="anat-row"><span>create mode 100644</span><span>Yeni bir dosya geldi; 100644 sıradan (çalıştırılamayan) dosya demek.</span></div>
  </div>
  <figcaption>İlk commit'in çıktısı. Kimlik senin terminalinde başka olur: içine tarih ve yazar da giriyor.</figcaption>
</figure>

Commit'ten sonra `git status` artık `index.html`'den bahsetmiyor: dosya
commit'te ve o zamandan beri değişmedi. Yalnızca `style.css` kaldı.

> `-m` olmadan `git commit` yazarsan Git mesajı yazman için bir düzenleyici
> açar. Odyssey'nin terminalinde düzenleyici yok; mesajı hep `-m` ile
> yazacağız.

### İyi bir commit mesajı

Mesaj, geçmişe bakan birine (birkaç ay sonraki sana) **neden** sorusunun
cevabını verir. Şimdilik üç kural yeter:

- Kısa tut (50 karakter civarı): `Add home page`.
- Emir kipiyle başla: `Add`, `Fix`, `Remove`, `Update`. "Bu commit uygulanırsa
  ne yapar?" sorusunun cevabı gibi.
- `update`, `fix`, `asdf` gibi bir şey anlatmayan mesajlardan kaçın.

İngilizce yazmak yaygın bir alışkanlık (projeler uluslararası), ama zorunlu
değil. Bu patikada İngilizce yazacağız. Ayrıntısı 15'te.

## Değiştirilmiş dosyalar

Commit'lenmiş bir dosyayı değiştirince Git onu **modified** (değiştirilmiş)
olarak gösterir:

```text
~/site (main) $ echo "<p>Hi</p>" >> index.html
~/site (main) $ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   index.html

no changes added to commit (use "git add" and/or "git commit -a")
```

Kırmızı satır, değişikliğin henüz hazırlık alanında olmadığını söylüyor
(**Changes not staged for commit**). Commit'e girmesi için yine `git add`
gerekiyor. Yani `git add` "yeni dosya ekle" değil, "**bu değişikliği bir
sonraki commit'e koy**" demek; yeni dosya da bir değişiklik.

## Bir dosyanın yaşam döngüsü

<figure class="fig">
  <div class="flow">
    <span class="node no">İzlenmeyen<br><small>untracked</small></span><span class="arrow">→</span>
    <span class="node acc">Hazırlanmış<br><small>git add</small></span><span class="arrow">→</span>
    <span class="node ok">Değişmemiş<br><small>git commit</small></span><span class="arrow">→</span>
    <span class="node no">Değiştirilmiş<br><small>dosyayı düzenle</small></span><span class="arrow">→</span>
    <span class="node acc">Hazırlanmış<br><small>git add</small></span>
  </div>
  <figcaption>Bir dosya bu dört hâl arasında döner. Her düzenlemeden sonra commit'e girmesi için yeniden git add gerekir.</figcaption>
</figure>

## Kısa durum: `git status -s`

Uzun çıktı yerine iki harflik bir özet:

```text
~/site (main) $ git status -s
M  about.html
 M index.html
MM style.css
?? notes.txt
```

| Kod | Anlamı |
|---|---|
| `??` | İzlenmeyen dosya. |
| `A ` | Yeni dosya, hazırlık alanında. |
| `M ` | Değiştirilmiş, hazırlık alanında (sol sütun yeşil). |
| ` M` | Değiştirilmiş, hazırlık alanında **değil** (sağ sütun kırmızı). |
| `MM` | Bir kısmı hazırlık alanında, sonra yeniden değiştirilmiş. |

Sol sütun **hazırlık alanı**, sağ sütun **çalışma alanı**. `MM` ilginç:
`git add` değişikliğin o anki hâlini hazırlık alanına kopyalar. Ondan sonra
dosyayı yine değiştirirsen yeni değişiklik dışarıda kalır; commit'e girmesi
için yeniden `git add` gerekir.

## Kısayol: `git commit -a`

`-a` (*all*), **izlenen** dosyalardaki bütün değişiklikleri önce hazırlık
alanına koyar, sonra commit'ler. `-a` ile `-m` birleşip `-am` olur:

```text
~/site (main) $ git commit -am "Add greeting"
[main d00097d] Add greeting
 1 file changed, 1 insertion(+)
~/site (main) $ git status -s
?? todo.txt
```

Dikkat: `-a` **yeni (izlenmeyen) dosyaları eklemez**. `todo.txt` dışarıda
kaldı. Yeni dosyalar için her zaman `git add` gerekir.

## Yanlışlıkla ekledim: geri çıkarmak

Yeni bir dosyayı yanlışlıkla hazırlık alanına koyduysan `git status` ne
yapacağını söylüyor: `git rm --cached <dosya>`. Dosya klasörde kalır, yalnızca
hazırlık alanından çıkar ve yeniden izlenmeyen olur.

```text
~/site (main) $ git status -s
M  index.html
A  passwords.txt
~/site (main) $ git rm --cached passwords.txt
rm 'passwords.txt'
~/site (main) $ git status -s
M  index.html
?? passwords.txt
```

> `--cached` çok önemli. Onsuz `git rm` dosyayı **klasörden de siler**.
> Daha önce commit'lenmiş bir dosyadaki değişikliği hazırlık alanından
> çıkarmanın yolu farklı (`git restore --staged`); onu 04'te göreceğiz.

## Git boş klasörleri izlemez

Git dosyaları izler, klasörleri değil. İçinde dosya olmayan bir klasör
`git status`'ta görünmez ve commit'e girmez. Boş bir klasörü depoda tutmak
isteyenler içine `.gitkeep` adında boş bir dosya koyar (bir gelenek; Git
için özel bir anlamı yok).

## Özet

- Üç alan: **çalışma alanı** → `git add` → **hazırlık alanı** →
  `git commit` → **depo**.
- `git status` her şeyi söyler; her adımdan önce ve sonra bak.
- `git add` bir değişikliği bir sonraki commit'e koyar (yeni dosya da bir
  değişiklik).
- `git commit -m "Mesaj"` hazırlık alanındakileri commit'ler.
- `git status -s`: sol sütun hazırlık alanı, sağ sütun çalışma alanı.
- `git commit -am` izlenen dosyalar için kısayol; yeni dosyaları almaz.
- `git rm --cached` yeni bir dosyayı hazırlık alanından çıkarır, silmez.
