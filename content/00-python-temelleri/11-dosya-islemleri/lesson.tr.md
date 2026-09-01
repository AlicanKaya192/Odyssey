# Dosya İşlemleri

Buraya kadar yazdığın her program aynı sonla bitti: program kapandı, her şey
kayboldu. Değişkenler bellekte duruyor ve bellek program bitince temizleniyor.

Bir şeyin kalıcı olması için **diske** yazılması gerekiyor. Bu bölüm onu
anlatıyor: dosya açmak, okumak, yazmak ve bunu yaparken veri kaybetmemek.

Veri biliminde bunun ayrı bir önemi var. Çalışacağın veri bir dosyadan
geliyor; pandas'ın yaptığı ilk iş de aslında bu.

## Bir dosya açmak

Dosya açmanın doğru yolu `with` ile:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("first line\n")
```

Üç parça var:

<figure class="fig anat">
  <div class="sig">open(<u class="m1">"notes.txt"</u>, <u class="m2">"w"</u>, <u class="m3">encoding="utf-8"</u>)</div>
  <ul class="legend">
    <li class="m1"><b>Dosya adı</b> — hangi dosya. Yol verilmezse programın çalıştığı klasörde aranır.</li>
    <li class="m2"><b>Kip</b> — ne yapacaksın. <code>"w"</code> yaz, <code>"r"</code> oku, <code>"a"</code> sona ekle.</li>
    <li class="m3"><b>Kodlama</b> — harflerin diske nasıl yazılacağı. Her zaman <code>utf-8</code> yaz.</li>
  </ul>
</figure>

## Neden `with`?

Açtığın dosyayı kapatman gerekiyor. `with` bunu senin yerine yapıyor:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>with</b> bloğu<br>başlar</span>
    <span class="arrow">→</span>
    <span class="node">dosya açılır</span>
    <span class="arrow">→</span>
    <span class="node">işini yaparsın</span>
    <span class="arrow">→</span>
    <span class="node ok">blok bitince<br><b>kendiliğinden</b> kapanır</span>
  </div>
  <figcaption>Blok içinde hata çıksa bile dosya kapanıyor. Elle açıp kapatmak bu güvenceyi vermiyor.</figcaption>
</figure>

Elle de yapılabilir ama yapılmıyor:

```python
file = open("notes.txt", "w")
file.write("hello")
file.close()          # unutulursa veri diske yazilmayabilir
```

Arada bir hata çıkarsa `close()` satırına hiç gelinmiyor ve yazdığın şey
diske geçmemiş olabiliyor. `with` bu sorunu tamamen ortadan kaldırıyor.

## Yazmak

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("first line\n")
    file.write("second line\n")
```

Dikkat edilecek iki şey var:

**`write` satır sonu koymuyor.** `print` kendiliğinden alt satıra geçiyor,
`write` geçmiyor. `\n` yazmazsan her şey tek satıra biner.

**`"w"` kipi dosyayı siliyor.** Dosya varsa içeriği tamamen gidiyor ve
sıfırdan yazılıyor.

## `"w"` ile `"a"` farkı

Bu farkı bilmemek gerçek veri kaybına yol açıyor:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>"w" — SIFIRDAN YAZ</h5>
<pre><code>with open("log.txt", "w") as f:
    f.write("new\n")</code></pre>
    </div>
    <div class="ok">
      <h5>"a" — SONA EKLE</h5>
<pre><code>with open("log.txt", "a") as f:
    f.write("new\n")</code></pre>
    </div>
  </div>
  <figcaption>Soldaki dosyanın eski içeriğini siliyor. Sağdaki koruyup sonuna ekliyor. Bir kayıt dosyası tutuyorsan istediğin sağdaki.</figcaption>
</figure>

## Okumak

Üç yolu var, üçü farklı işe yarıyor.

**Tamamını tek metin olarak:**

```python
with open("notes.txt", encoding="utf-8") as file:
    content = file.read()

print(content)
```

Kip yazmadığında varsayılan `"r"`, yani okuma. Bu yüzden `"r"` genelde
yazılmıyor.

**Satır listesi olarak:**

```python
with open("notes.txt", encoding="utf-8") as file:
    lines = file.read().splitlines()

print(lines)
```

```
['first line', 'second line']
```

`splitlines()` satır sonlarını temizleyerek böldüğü için tercih edilen yol bu.

**Satır satır dolaşarak:**

```python
with open("notes.txt", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

Bu üçüncüsünün önemli bir avantajı var: dosyanın tamamını belleğe almıyor,
satır satır okuyor. Küçük dosyalarda fark etmez, ama iki gigabaytlık bir
veri dosyasında tek fark edilebilir yol bu.

## Satır sonlarına dikkat

Dosyadan okunan her satırın sonunda `\n` duruyor:

```python
with open("notes.txt", encoding="utf-8") as file:
    for line in file:
        print(repr(line))
```

```
'first line\n'
'second line\n'
```

`strip()` baştaki ve sondaki boşlukları — satır sonu dahil — temizliyor:

```python
clean = line.strip()
```

Bunu unutmak sinsi bir hataya yol açıyor: `line == "first line"` karşılaştırması
`False` çıkıyor, çünkü sağ tarafta `\n` yok.

## Kipler

| Kip | Ne yapar | Dosya yoksa |
|---|---|---|
| `"r"` | Okur (varsayılan) | `FileNotFoundError` |
| `"w"` | Sıfırdan yazar, eskisini siler | Oluşturur |
| `"a"` | Sonuna ekler | Oluşturur |
| `"x"` | Yazar ama dosya varsa hata verir | Oluşturur |

`"x"` kipi az bilinir ama işe yarar: yanlışlıkla üstüne yazmayı imkânsız
kılıyor.

## `encoding` neden önemli?

Harfler diske sayı olarak yazılıyor. Hangi harfin hangi sayı olacağını
**kodlama** belirliyor.

`utf-8` yazmazsan Python işletim sisteminin varsayılanını kullanıyor ve o
Windows'ta Türkçe için farklı olabiliyor. Sonuç: bir bilgisayarda yazdığın
dosya başka bir bilgisayarda bozuk görünüyor, ya da `UnicodeDecodeError`
alıyorsun.

**Kural: her `open` çağrısına `encoding="utf-8"` yaz.** İstisnasız.

## Dosya yoksa

Olmayan bir dosyayı okumaya çalışmak hata veriyor:

```python
with open("missing.txt", encoding="utf-8") as file:
    content = file.read()
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

Önceki bölümdeki `try` / `except` tam buraya oturuyor:

```python
try:
    with open("settings.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    content = ""
    print("no settings file, using defaults")
```

Burada yakalamanın anlamlı bir karşılığı var: varsayılana düşüyorsun.

## Basit bir veri dosyası okumak

Veri biliminde en sık karşına çıkacak biçim, her satırda virgülle ayrılmış
alanlar olması:

```
Ada,90
Alan,70
Grace,85
```

Bunu okumak öğrendiğin her şeyi bir araya getiriyor:

```python
scores = {}

with open("scores.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        name, value = line.split(",")
        scores[name] = int(value)

print(scores)
```

```
{'Ada': 90, 'Alan': 70, 'Grace': 85}
```

Satır satır oku, temizle, boş satırı atla, böl, çevir, sözlüğe koy. pandas'ın
`read_csv` fonksiyonu da özünde bunu yapıyor — yalnızca çok daha fazla
ayrıntıyla.

## Özet

- Değişkenler program bitince kaybolur; kalıcı olması gereken şey dosyaya
  yazılır.
- Dosya **her zaman** `with` ile açılır; blok bitince kendiliğinden kapanır.
- `open(ad, kip, encoding="utf-8")` — kodlamayı her seferinde yaz.
- `"r"` okur, `"w"` **eskisini silerek** yazar, `"a"` sonuna ekler,
  `"x"` dosya varsa yazmayı reddeder.
- `write` satır sonu koymaz; `\n` yazman gerekir.
- Okunan satırların sonunda `\n` durur; `strip()` ile temizlenir.
- Bütün dosyayı `read()`, satır listesini `read().splitlines()`, büyük
  dosyaları `for line in file:` ile okursun.
- Olmayan dosya `FileNotFoundError` verir; anlamlı bir karşılığın varsa
  `try` / `except` ile yakalarsın.
