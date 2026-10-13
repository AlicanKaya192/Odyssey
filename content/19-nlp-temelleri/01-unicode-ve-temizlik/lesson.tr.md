# Unicode ve Metin Temizleme

Bir önceki bölümde "Great", "great" ve "great!" kelimelerini aynı saymak için
`lower()` ve `strip()` kullandık. Gerçek metinde iş bundan çok daha karışık:
web sayfasından kopyalanan bir yorumda gözle görünmeyen boşluklar, kıvrık
tırnaklar, HTML artıkları, aynı görünen ama farklı kodlanmış harfler olabilir.
Bilgisayar bunların her birini ayrı bir şey sanır. Bu bölüm metnin bilgisayarda
nasıl saklandığını, **Unicode normalleştirmeyi**, Türkçenin büyük-küçük harf
tuzağını ve sonunda kirli yorumları temizleyen bir **temizleme hattını**
(cleaning pipeline) anlatıyor.

## Bilgisayar harfi nasıl saklar?

Bilgisayar yalnızca sayı saklayabilir. Her karaktere bir numara verilir; bu
numaralandırmanın dünya standardı **Unicode**. Her karakterin Unicode'daki
numarasına **kod noktası** (code point) denir. Dosyaya ya da ağa yazılırken bu
numaralar baytlara çevrilir; en yaygın yöntem **UTF-8**.

```python
for ch in ["A", "a", "ş", "é", "€"]:
    print(ch, ord(ch), len(ch.encode("utf-8")))
print(chr(351), "ş" == chr(351))
```

```text
A 65 1
a 97 1
ş 351 2
é 233 2
€ 8364 3
ş True
```

- `ord` karakterin kod noktasını verir, `chr` tersini yapar: 351 "ş".
- `encode("utf-8")` metni baytlara çevirir. İngilizce harfler 1 bayt, "ş" ve
  "é" 2 bayt, "€" 3 bayt tutuyor. UTF-8'in en büyük avantajı bu: İngilizce
  metin eski ASCII ile birebir aynı, öbür diller de sığıyor.
- Python'da `str` her zaman kod noktalarından oluşur; `len("ş")` 1'dir.
  Baytlarla yalnızca dosya okurken ve yazarken uğraşırsın:
  `open(..., encoding="utf-8")`.

## Aynı görünen, farklı dizeler

"é" iki şekilde yazılabilir: tek bir hazır karakter olarak ya da "e" harfinin
arkasına gelen bir **birleşen işaret** (combining mark) olarak. Ekranda ikisi
de aynı görünür.

```python
import unicodedata

a = "caf" + chr(0xE9)      # é: tek karakter
b = "cafe" + chr(0x301)    # e + birleşen vurgu işareti
print(a, b, a == b, len(a), len(b))
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))
print([unicodedata.name(c) for c in b[-2:]])
```

```text
café café False 4 5
True
['LATIN SMALL LETTER E', 'COMBINING ACUTE ACCENT']
```

- İki "café" ekranda aynı ama Python için farklı dizeler: biri 4, öbürü 5
  karakter. Biri arama kutusuna, öbürü veritabanına bu şekilde girmişse arama
  hiçbir şey bulamaz.
- `unicodedata.normalize("NFC", ...)` metni **standart biçime** getiriyor:
  harf ve işareti tek karaktere birleştiriyor. Normalleştirmeden sonra ikisi
  eşit.
- `unicodedata.name` karakterin resmî adını veriyor; görünmeyen karakteri
  avlarken çok işe yarar.

**NFC** (birleştir) ve **NFD** (ayır) iki standart biçim. Metin
karşılaştırmadan ya da saklamadan önce NFC'ye çevirmek iyi bir alışkanlık.

## Uyumluluk normalleştirmesi: NFKC

Bazı karakterler başka bir karakterin **görsel çeşidi**: "ﬁ" bağlı harfi
(ligature) aslında "f" ve "i", "ＡＢＣ" tam genişlikli harfler (Doğu Asya
klavyelerinden gelir), "…" tek karakterlik üç nokta. **NFKC** bunları da sade
hâllerine çeviriyor.

```python
import unicodedata

samples = [chr(0xFB01) + "ne", "ＡＢＣ１２３", "wow" + chr(0xFF01),
           "x" + chr(0xB2), "wait" + chr(0x2026)]
for s in samples:
    print(s, "->", unicodedata.normalize("NFKC", s))
```

```text
ﬁne -> fine
ＡＢＣ１２３ -> ABC123
wow！ -> wow!
x² -> x2
wait… -> wait...
```

Dikkat: "x²" NFKC'den sonra "x2" oldu, yani "x kare" "x iki"ye dönüştü.
Yorumlarda bunun bir önemi yok, ama matematik ya da kimya metninde NFKC
anlamı bozar. Normalleştirme her zaman **göreve göre** seçilir.

## Türkçe büyük-küçük harf tuzağı

Türkçede dört "i" var: I/ı ve İ/i. Python'un `lower()` ve `upper()`
fonksiyonları ise dili bilmez; İngilizce kuralını uygular.

```python
word = "İSTANBUL"
low = word.lower()
print(low, len(word), len(low))
print("ILIK".lower(), "ılık".upper())

TR_LOWER = str.maketrans({"I": "ı", "İ": "i"})


def turkish_lower(text):
    return text.translate(TR_LOWER).lower()


print(turkish_lower("İSTANBUL"), turkish_lower("ILIK"))
```

```text
i̇stanbul 8 9
ilik ILIK
istanbul ılık
```

- `"İSTANBUL".lower()` 8 harflik kelimeden **9 karakterlik** bir dize
  çıkarıyor. Python "İ"yi "i" + birleşen nokta (U+0307) yapıyor. Ekranda
  "istanbul" gibi görünüyor ama "istanbul" ile eşit değil.
- `"ILIK".lower()` "ilik" veriyor; Türkçede doğrusu "ılık". İki kelimenin
  anlamı bambaşka.
- Çözüm: küçültmeden önce Türkçeye özgü iki harfi elle çevirmek.
  `str.maketrans` bir harf eşleme tablosu kuruyor, `translate` onu
  uyguluyor.

`casefold()` de aynı sorunu taşıyor. Türkçe metinle çalışan her program bu
çeviriyi kendisi yapmak zorunda.

## Aksanları atmak

Aramada "cafe" yazan birinin "café"yi de bulmasını isteriz. Bunun için
aksanlar atılır: metin NFD ile harf + işaret olarak ayrılır, sonra işaretler
silinir.

```python
import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


for w in ["café", "naïve", "Ångström", "şeker", "ılık", "İzmir"]:
    print(w, "->", strip_accents(w))
```

```text
café -> cafe
naïve -> naive
Ångström -> Angstrom
şeker -> seker
ılık -> ılık
İzmir -> Izmir
```

- `unicodedata.combining(c)` birleşen işaretler için sıfırdan farklı bir
  sayı veriyor; onları atıyoruz.
- "ş" → "s", "İ" → "I" oldu, ama **"ı" olduğu gibi kaldı**: "ı" Unicode'da
  "i"nin aksanlı hâli değil, ayrı bir harf. Ayrıştırılacak bir şeyi yok.
- Türkçede aksan atmak tehlikeli: "aşk" ile "ask", "yaşa" ile "yasa" aynı
  kelimeye dönüşür. Arama için kabul edilebilir, sınıflandırma için çoğu
  zaman bilgi kaybıdır.

## Web'den gelen kirli metin

`text_data.py`'deki `messy_reviews` aynı yorumları bir web sayfasından
kopyalanmış gibi veriyor: bölünmez boşluk (no-break space), sıfır genişlikli
boşluk (zero-width space), kıvrık tırnak, `<br>` gibi HTML etiketleri ve
`&amp;` gibi HTML varlıkları (entity). `ascii()` görünmeyen karakterleri kod
olarak gösteriyor.

```python
from text_data import messy_reviews

reviews = messy_reviews(2000)
print(ascii(reviews[3]["text"][:44]))
```

```text
'It\xa0does the\xa0job.<br>Much better\xa0tahn my old '
```

`\xa0` bölünmez boşluk: ekranda boşluk gibi görünüyor ama `split(" ")` onu
boşluk saymıyor, "It\xa0does" tek kelime kalıyor. Kaç yorumda hangi iz var?

```python
from collections import Counter

SIGNS = {"no-break space": chr(0xA0), "zero-width space": chr(0x200B),
         "curly quote": chr(0x2019), "html tag": "<", "entity": "&amp;"}
found = Counter()
for r in reviews:
    for name, sign in SIGNS.items():
        found[name] += sign in r["text"]
for name, count in found.items():
    print(name, count)
```

```text
no-break space 1130
zero-width space 715
curly quote 43
html tag 585
entity 66
```

2000 yorumun 1130'unda bölünmez boşluk, 715'inde sıfır genişlikli boşluk var.
Bunlar gerçek veride de çok sık: kopyala-yapıştır, kelime işlemciler ve web
editörleri ekliyor.

## Temizleme hattı

Hepsini sırayla düzelten bir fonksiyon yazalım:

```python
import html
import re
import unicodedata

QUOTES = str.maketrans({chr(0x2018): "'", chr(0x2019): "'",
                        chr(0x201C): '"', chr(0x201D): '"'})


def clean(text):
    text = html.unescape(text)                  # &amp; -> &
    text = re.sub(r"<[^>]+>", " ", text)        # <br>, <p> -> boşluk
    text = unicodedata.normalize("NFKC", text)  # ！ -> !, … -> ...
    text = text.translate(QUOTES)               # kıvrık tırnak -> düz
    text = text.replace(chr(0x200B), "")        # görünmez boşluk
    return " ".join(text.split())               # bütün boşluklar tek boşluk


raw = [r["text"] for r in reviews]
print(ascii(clean(raw[3])[:44]))


def vocabulary(texts):
    return {w.strip(".,!?" + chr(34)).lower() for t in texts for w in t.split(" ")}


print(len(vocabulary(raw)), len(vocabulary(clean(t) for t in raw)))
```

```text
'It does the job. Much better tahn my old off'
2225 362
```

- `html.unescape` HTML varlıklarını gerçek karakterlere çeviriyor.
- `re.sub(r"<[^>]+>", " ", text)` `<` ile `>` arasındaki her şeyi siliyor;
  düzenli ifadeleri (regular expression) Temel Kütüphaneler patikasından
  biliyorsun.
- `text.split()` (argümansız) bölünmez boşluk, sekme ve satır sonu dahil her
  türlü boşluktan bölüyor; `" ".join(...)` hepsini tek boşlukla birleştiriyor.
- **Sonuç:** kirli metinde 2225 farklı "kelime" vardı; temizledikten sonra
  362 kaldı. Temiz veride bu sayı 360; aradaki fark yalnızca `&` işareti ve
  noktalamadan geriye kalan boş dize. Yani temizlik olmasa kelime
  dağarcığının altıda beşi çöp olurdu: "the\xa0job", "job.<br>Much"
  gibi uydurma kelimeler.

**Sıra önemli.** Bu hatta HTML varlıkları etiketlerden önce çözülüyor;
bunun bir bedeli var: metinde kaçışlı yazılmış `&lt;b&gt;` gibi bir ifade
önce `<b>`ye çevrilip sonra etiket diye siliniyor. Yorumlarda böyle bir ifade
yok; olsaydı etiketleri önce silmek gerekirdi. Bir temizleme hattında her
adımın neden o sırada olduğunu bil.

## Neyi temizlememeli?

Temizlik bilgi de götürebilir. Duygu analizinde "GREAT!!!" ile "great"
aynı şey değil: büyük harf ve ünlemler duygunun şiddetini taşıyor. "C++" ile
"C" bir programlama sorusunda farklı; noktalamayı silmek onları
birleştiriyor. Sayılar, tarihler ve sipariş numaraları bilgi çıkarmada
gerekli. Kural şu: **temizliği görev belirler.** Önce bu bölümdeki gibi
neyin kirli olduğunu ölç, sonra yalnızca gürültüyü sil.

## Özet

- Unicode her karaktere bir numara (kod noktası) verir; UTF-8 bu numaraları
  baytlara çevirir. Dosyaları her zaman `encoding="utf-8"` ile aç.
- Aynı görünen metinler farklı kodlanmış olabilir: karşılaştırmadan önce
  `unicodedata.normalize("NFC", ...)`; görsel çeşitleri de sadeleştirmek için
  NFKC (ama "x²" gibi anlam taşıyanlara dikkat).
- Python'un `lower()`'ı Türkçeyi bilmez: "İ" → "i̇", "I" → "i". Önce
  `translate` ile Türkçe harfleri çevir.
- Aksan atmak aramayı kolaylaştırır ama Türkçede kelimeleri birleştirebilir;
  "ı" zaten ayrıştırılamaz.
- Web metni görünmez karakterlerle doludur. Temizleme hattı kelime
  dağarcığını 2225'ten 362'ye indirdi. Temizlik görevine göre seçilir;
  büyük harf ve ünlem gibi duygu taşıyan izleri gereksiz yere silme.
