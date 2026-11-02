# Joker Karakterler

Bir klasörde 200 fotoğraf olduğunu düşün ve hepsini başka bir klasöre
taşımak istiyorsun. Adları tek tek yazmak saatler sürer. **Joker
karakterler** (wildcards) bir **kalıp** yazmanı sağlar: "adı `.jpg` ile biten
her dosya". Kabuk kalıbı eşleşen adların listesine çevirir, komut o listeyle
çalışır.

## Üç joker ve bir kısaltma

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>*</span><span>Herhangi sayıda herhangi karakter (hiç karakter de olur). <code>*.txt</code>: .txt ile biten her ad.</span></div>
    <div class="anat-row"><span>?</span><span>Tam olarak <b>bir</b> karakter. <code>photo?.jpg</code>: photo1.jpg evet, photo10.jpg hayır.</span></div>
    <div class="anat-row"><span>[abc]</span><span>Köşeli parantezdekilerden <b>biri</b>. <code>[0-9]</code> bir rakam, <code>[a-z]</code> bir küçük harf.</span></div>
    <div class="anat-row"><span>{a,b}</span><span>Joker değil, kısaltma: listedeki her biri yazılır, dosya var mı diye bakılmaz.</span></div>
  </div>
  <figcaption>İlk üçü var olan dosya adlarıyla eşleşir; süslü parantez her zaman açılır.</figcaption>
</figure>

## Yıldız: `*`

`*` herhangi sayıda herhangi karakterle eşleşir; hiç karakter de olabilir:

```text
~/work $ ls
data.csv  notes.txt  photo1.jpg  photo10.jpg  photo2.jpg  report.txt
~/work $ ls *.txt
notes.txt  report.txt
~/work $ ls photo*
photo1.jpg  photo10.jpg  photo2.jpg
~/work $ echo *.txt
notes.txt report.txt
~/work $ echo *
data.csv notes.txt photo1.jpg photo10.jpg photo2.jpg report.txt
```

- `*.txt`: `.txt` ile biten her ad.
- `photo*`: `photo` ile başlayan her ad.
- `*`: klasördeki her ad (gizliler hariç; birazdan).

`echo *.txt` sonucu adları tek satırda yazdı. Bu, jokerin nasıl
açıldığını görmenin en kolay yolu.

## Jokeri kabuk açar

Bu bölümün en önemli fikri şu: jokeri `ls` ya da `rm` açmaz, **kabuk**
açar. Komut yıldızı hiç görmez; kabuğun bulduğu adların listesini görür.

<figure class="fig">
  <div class="flow">
    <span class="node">Sen yazarsın<br><small><code>ls *.txt</code></small></span><span class="arrow">→</span>
    <span class="node acc">Kabuk açar<br><small>eşleşen adları bulur</small></span><span class="arrow">→</span>
    <span class="node">Program görür<br><small><code>ls notes.txt report.txt</code></small></span>
  </div>
  <figcaption>Jokerleri programlar değil kabuk açar. <code>ls</code> yıldızı hiç görmez, adların listesini görür.</figcaption>
</figure>

Bu yüzden jokerler **her** komutla çalışır: `ls`, `cp`, `mv`, `rm`, `cat`,
hatta `echo`. Ve bu yüzden `echo` ile önceden bakmak güvenlidir: `echo`
hiçbir dosyaya dokunmaz, yalnızca kabuğun ürettiği listeyi yazar.

## Soru işareti: `?`

`?` **tam olarak bir** karakterle eşleşir:

```text
~/work $ ls photo?.jpg
photo1.jpg  photo2.jpg
~/work $ ls photo??.jpg
photo10.jpg
```

`photo?.jpg` iki haneli `photo10.jpg`'yi almadı; iki soru işareti ise
yalnızca onu aldı. Numaralı dosyalarda tek ve çift haneliyi ayırmanın kolay
yolu.

## Köşeli parantez: `[...]`

`[...]` içindeki karakterlerden **bir tanesiyle** eşleşir. Tire ile aralık
yazılır: `[0-9]` bir rakam, `[a-z]` bir küçük harf.

```text
~/work $ ls photo[12].jpg
photo1.jpg  photo2.jpg
~/work $ ls [dn]*
data.csv  notes.txt
~/work $ ls photo[0-9].jpg
photo1.jpg  photo2.jpg
```

## Hiçbir şey eşleşmezse

```text
~/work $ ls *.pdf
ls: cannot access '*.pdf': No such file or directory
~/work $ echo *.pdf
*.pdf
```

bash eşleşen bir ad bulamazsa kalıbı **olduğu gibi** bırakır. `ls` bu yüzden
gerçekten `*.pdf` adında bir dosya aradı ve bulamadı. "Kalıbım bir şeyle
eşleşti mi?" sorusunun cevabını `echo` hemen verir.

## Jokeri kapatmak

Bazen yıldızı düz yazmak istersin (örneğin bir metinde). Tırnak içine alır
ya da önüne ters bölü koyarsın:

```text
~/work $ echo "*.txt"
*.txt
~/work $ echo '*.txt'
*.txt
~/work $ echo \*.txt
*.txt
~/work $ echo *.txt
notes.txt report.txt
```

Tırnak içinde joker açılmaz. Bunu ileride `find` ve `grep` ile çok
kullanacağız: kalıbı kabuk değil, o program yorumlasın diye tırnaklarız.

## Gizli dosyalar eşleşmez

`*` ve `?` adın başındaki **noktayla** eşleşmez. `echo *` çıktısında
`.hidden.txt` yoktu. Bu bir güvenlik: `rm *` ayar dosyalarına dokunmaz.
Gizli dosyaları istiyorsan noktayı açıkça yazarsın: `.h*`.

## Süslü parantez: `{a,b}` ve `{1..5}`

Süslü parantez bir joker değil, bir **kısaltmadır**: listedeki her öğe için
bir kelime üretir. Dosyaların var olup olmadığına bakmaz; bu yüzden
**yeni** şeyler oluştururken işe yarar:

```text
~ $ echo file{1,2,3}.txt
file1.txt file2.txt file3.txt
~ $ echo {a..e}
a b c d e
~ $ mkdir -p site/{css,js,img}
~ $ ls site
css/  img/  js/
~ $ touch site/js/app{1..3}.js
~ $ ls site/js
app1.js  app2.js  app3.js
```

- `{1,2,3}` virgüllü liste; virgülden sonra **boşluk olmaz**.
- `{1..3}` ve `{a..e}` aralık.
- `mkdir -p site/{css,js,img}` tek komutla üç klasör açtı.

## Joker ve `rm`: önce bak

Joker birkaç harfle çok sayıda dosyayı kapsar; `rm` ile birleşince bir yanlış
harf çok şey götürür. Alışkanlık şu: aynı kalıbı önce zararsız bir komutla
dene, sonra asıl komutu yaz.

```text
~/work $ ls
a.tmp  data.csv   photo1.jpg   photo2.jpg
b.tmp  notes.txt  photo10.jpg  report.txt
~/work $ echo rm *.tmp
rm a.tmp b.tmp
~/work $ rm *.tmp
~/work $ ls
data.csv  notes.txt  photo1.jpg  photo10.jpg  photo2.jpg  report.txt
```

`echo rm *.tmp` hiçbir şey silmedi, yalnızca çalışacak komutu gösterdi. Bir
başka sık felaket boşluk: `rm * .tmp` (yıldızdan sonra boşluk) "her şeyi ve
`.tmp` adlı dosyayı sil" demektir.

## Özet

- `*` herhangi sayıda karakter, `?` tam bir karakter, `[abc]` listeden biri,
  `[0-9]` aralıktan biri.
- Jokeri **kabuk** açar; komut adların listesini görür. `echo kalıp` ile
  sonucu önceden gör.
- Eşleşme yoksa kalıp olduğu gibi kalır.
- Tırnak ya da `\` jokeri kapatır.
- Gizli dosyalar `*` ile eşleşmez.
- `{a,b}` ve `{1..5}` dosyaya bakmadan liste üretir; yeni klasör ve dosya
  açarken kullanışlı.
- `rm` ile joker kullanmadan önce aynı kalıba `echo` ya da `ls` ile bak.
