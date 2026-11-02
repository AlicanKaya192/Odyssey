# Kopyalamak, Taşımak, Silmek

Görsel arayüzde bir dosyayı kopyalamak için sağ tıklarsın, taşımak için
sürüklersin, silmek için çöp kutusuna atarsın. Terminalde bu üç iş üç
komuttur: `cp`, `mv` ve `rm`. Üçü de kısa ve hızlıdır; `rm` ise **geri
alınamaz**, o yüzden bu bölümün bir kısmı dikkatli olmanın yollarını
anlatıyor.

## İki komut, bir fark

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>cp kaynak hedef</h4><p>Kaynak yerinde kalır</p><p>Hedefte bir kopyası olur</p><p>Klasör için <code>-r</code> gerekir</p></div>
    <div class="dim"><h4>mv kaynak hedef</h4><p>Kaynak yerinden kalkar</p><p>Hedefte o olur (taşıma ya da yeni ad)</p><p>Klasör için seçenek gerekmez</p></div>
  </div>
  <figcaption>İkisinde de hedef var olan bir klasörse dosya onun <b>içine</b> gider; değilse hedef yeni ad olur.</figcaption>
</figure>

İkisinin de yazılışı aynı: önce **kaynak**, en sonda **hedef**.

```text
cp  kaynak  hedef
mv  kaynak  hedef
```

## Kopyalamak: `cp`

`cp` (*copy*) kaynağın bir kopyasını hedefte oluşturur:

```text
~/notes $ cp todo.txt todo-copy.txt
~/notes $ ls
ideas.txt  todo-copy.txt  todo.txt
~/notes $ cat todo-copy.txt
Buy milk
~/notes $ mkdir backup
~/notes $ cp todo.txt backup/
~/notes $ cp todo.txt ideas.txt backup
~/notes $ ls backup
ideas.txt  todo.txt
~/notes $ cp nope.txt backup
cp: cannot stat 'nope.txt': No such file or directory
```

- `cp todo.txt todo-copy.txt` aynı klasörde ikinci bir dosya yarattı.
- `cp todo.txt backup/` dosyayı `backup` klasörünün **içine** kopyaladı; adı
  aynı kaldı.
- Birden çok kaynak verebilirsin; o zaman son argüman bir klasör olmak
  zorunda.
- Olmayan bir dosyayı kopyalamaya çalışınca `cannot stat` dedi: "o dosyanın
  bilgisine bakamadım, çünkü yok".

Hedefin ne anlama geldiğini her zaman şu soru belirler: **hedef var olan bir
klasör mü?**

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>cp a.txt b.txt</span><span><code>b.txt</code> yoksa: a.txt'nin kopyası b.txt adıyla. Varsa: <b>sorulmadan üstüne yazılır</b>.</span></div>
    <div class="anat-row"><span>cp a.txt backup/</span><span><code>backup</code> bir klasör: kopya <code>backup/a.txt</code> olur.</span></div>
    <div class="anat-row"><span>cp a.txt b.txt backup/</span><span>Birden çok kaynak: son argüman klasör olmak zorunda.</span></div>
    <div class="anat-row"><span>mv old.txt new.txt</span><span>Aynı klasörde yeni ad: yeniden adlandırma.</span></div>
    <div class="anat-row"><span>mv a.txt archive/</span><span>Klasörün içine taşıma; ad aynı kalır.</span></div>
  </div>
  <figcaption>Son argüman hep hedef. Ne olacağını hedefin var olan bir klasör olup olmadığı belirler.</figcaption>
</figure>

## Klasör kopyalamak: `cp -r`

`cp` bir klasörü tek başına kopyalamaz. İçindeki her şeyle birlikte
kopyalaması için `-r` (*recursive*: iç içe, en dibe kadar) seçeneği gerekir:

```text
~/notes $ cp site site-backup
cp: -r not specified; omitting directory 'site'
~/notes $ cp -r site site-backup
~/notes $ ls site-backup
index.html
~/notes $ cp -r site site-backup
~/notes $ ls site-backup
index.html  site/
```

Son iki komuta dikkat: `site-backup` artık var olduğu için ikinci
`cp -r site site-backup`, `site` klasörünü onun **içine** kopyaladı. Aynı
komutu iki kez çalıştırmak iki kez aynı sonucu vermiyor; hedefin o anki
durumu önemli.

## Üstüne yazmak sorulmaz

Hedefte aynı adda bir dosya varsa `cp` (ve `mv`) **sormadan** onun üstüne
yazar:

```text
~/notes $ cat ideas.txt
Ideas
~/notes $ cp todo.txt ideas.txt
~/notes $ cat ideas.txt
Buy milk
```

`ideas.txt`'nin eski içeriği gitti. Önemli bir dosyayı değiştirmeden önce
yedek almak bu yüzden iyi bir alışkanlık: `cp notes.txt notes.txt.bak`.

## Taşımak ve yeniden adlandırmak: `mv`

`mv` (*move*) bir dosyayı ya da klasörü başka bir yere taşır. Aynı klasörde
yeni bir ad verirsen **yeniden adlandırmış** olursun; Linux'ta ayrı bir
"yeniden adlandır" komutu yoktur:

```text
~/notes $ mv todo.txt shopping.txt
~/notes $ ls
ideas.txt  shopping.txt
~/notes $ mkdir archive
~/notes $ mv shopping.txt archive/
~/notes $ ls
archive/  ideas.txt
~/notes $ ls archive
shopping.txt
~/notes $ mv archive old-notes
~/notes $ ls
ideas.txt  old-notes/
~/notes $ mv nope.txt archive
mv: cannot stat 'nope.txt': No such file or directory
```

- `mv todo.txt shopping.txt` yalnızca adı değiştirdi.
- `mv shopping.txt archive/` dosyayı klasörün içine taşıdı.
- `mv archive old-notes` bir **klasörün** adını değiştirdi. `cp`'nin aksine
  `mv` klasörde de seçenek istemez; içindekiler olduğu gibi gelir.

## Silmek: `rm`

`rm` (*remove*) dosyaları siler. Klasörü içindekilerle birlikte silmek için
yine `-r` gerekir:

```text
~/notes $ ls
ideas.txt  old.txt  tmp/  todo.txt
~/notes $ rm old.txt
~/notes $ rm tmp
rm: cannot remove 'tmp': Is a directory
~/notes $ rm -r tmp
~/notes $ ls
ideas.txt  todo.txt
~/notes $ rm nope.txt
rm: cannot remove 'nope.txt': No such file or directory
~/notes $ rm -f nope.txt
```

- `rm tmp` klasörü silmeyi reddetti (`Is a directory`); `rm -r tmp` sildi.
- `rm -f` (*force*) olmayan dosya için şikâyet etmedi. `-f` hiçbir şey
  sormaz, hiçbir şeye itiraz etmez; bu yüzden tehlikelidir.

> **`rm` geri alınamaz.** Terminalde çöp kutusu yok; silinen dosya gitmiştir.
> Özellikle `rm -rf` (içindekilerle, sormadan) yazmadan önce yolu iki kez oku.

## Sormasını istersen: `rm -i`

`-i` (*interactive*) seçeneği her dosyayı silmeden önce sorar. Gerçek bir
terminalde şöyle görünür; `y` yazarsan siler, başka bir şey yazarsan
dokunmaz:

```text
$ rm -i todo.txt
rm: remove regular file 'todo.txt'? n
```

Odyssey'nin terminali klavyeden cevap alamadığı için `rm -i` burada hiçbir
şey silmez, yalnızca bunu söyleyen bir mesaj yazar. Yine de alışkanlık
olarak bil: emin olmadığın silmelerde `-i` iyi bir emniyet kemeri.

## Özet

- `cp kaynak hedef` kopyalar, kaynak kalır; klasör için `cp -r`.
- `mv kaynak hedef` taşır ya da yeniden adlandırır; klasörde de çalışır.
- Hedef var olan bir klasörse dosya onun içine gider; birden çok kaynakta son
  argüman klasör olmalı.
- `cp` ve `mv` var olan dosyanın üstüne sormadan yazar.
- `rm dosya` siler, `rm -r klasör` içindekilerle siler, `-f` hiç sormaz.
- `rm` geri alınamaz: önce `ls` ile bak, önemli dosyanın yedeğini al.
