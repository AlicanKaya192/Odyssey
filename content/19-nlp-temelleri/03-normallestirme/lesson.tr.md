# Normalleştirme ve Kök Bulma

Parçalamadan sonra elimizde bir token listesi var, ama aynı anlamı taşıyan
pek çok farklı token: "love", "loves", "loved", "loving". Model için bunların
her biri ayrı bir sütun olacak ve her birini ayrı ayrı öğrenmek zorunda
kalacak. **Normalleştirme** (normalisation) bu farklı biçimleri bir araya
getirme işi. Bu bölüm dört aracı anlatıyor: durak kelimelerini atmak, kök
bulmak (stemming), sözlük biçimine indirmek (lemmatisation) ve değişken
bilgileri yer tutucuya çevirmek. Her birinin bir bedeli var; bölümün yarısı
o bedelleri ölçmek.

## Durak kelimeleri

"the", "is", "at" gibi kelimeler her metinde geçer ve tek başına konu ya da
duygu taşımaz. Bunlara **durak kelimeleri** (stop words) deniyor.
scikit-learn hazır bir İngilizce liste veriyor:

```python
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

print(len(ENGLISH_STOP_WORDS))
print(sorted(ENGLISH_STOP_WORDS)[:8])
print([w for w in ["not", "no", "never", "nor", "very", "too"] if w in ENGLISH_STOP_WORDS])
tokens = "the fit is not good at all".split()
print([t for t in tokens if t not in ENGLISH_STOP_WORDS])
```

```text
318
['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against']
['not', 'no', 'never', 'nor', 'very', 'too']
['fit', 'good']
```

- Liste 318 kelime: "a", "about", "above"... hepsi sık ve tek başına anlamsız
  görünen kelimeler.
- Ama **"not", "no", "never", "nor"** de listede, "very" ve "too" da.
  "the fit is not good at all" (oturuşu hiç iyi değil) cümlesinden geriye
  **"fit good"** kalıyor: olumsuz bir yorum olumlu görünüyor.

Durak kelimelerini atmanın kazancını yorumlarda ölçelim:

```python
import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_reviews

reviews = make_reviews(2000)
docs = [re.findall(r"[a-z]+", r["text"].lower()) for r in reviews]
words = Counter(w for d in docs for w in d)
kept = Counter(w for d in docs for w in d if w not in ENGLISH_STOP_WORDS)
print(len(words), sum(words.values()))
print(len(kept), sum(kept.values()))
```

```text
332 30798
298 16176
```

İlk sayı farklı kelime, ikinci sayı toplam kelime. Durak kelimeleri atınca
dağarcık 332'den 298'e indi, ama **toplam kelimenin yarısı** gitti (30 798 →
16 176). Durak kelimeleri az sayıda ama çok sık kelimelerdir. Metni kısaltmak
ve hızlandırmak için iyi; ancak duygu analizinde olumsuzluk ve şiddet
kelimelerini listeden çıkarmadan kullanma. Bir sonraki bölümlerde göreceğimiz
TF-IDF ise sık kelimelerin ağırlığını zaten kendisi düşürüyor; çoğu zaman
durak listesine hiç gerek kalmıyor.

## Kök bulma (stemming)

**Kök bulma** kelimenin sonundaki ekleri kurallarla kesip atmak: "loves" →
"love", "batteries" → "battery". Sözlük kullanmaz, yalnızca harflere bakar.
Kendi basit kök bulucumuzu yazalım:

```python
SUFFIX_RULES = [("ies", "y"), ("ing", ""), ("ed", ""), ("ly", ""), ("s", "")]


def stem(word):
    for suffix, replacement in SUFFIX_RULES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            if suffix == "s" and word.endswith("ss"):
                return word
            return word[: len(word) - len(suffix)] + replacement
    return word


for w in ["loves", "loved", "loving", "batteries", "quickly", "glass",
          "stopped", "news", "university", "universe", "running", "ran"]:
    print(w, "->", stem(w))
```

```text
loves -> love
loved -> lov
loving -> lov
batteries -> battery
quickly -> quick
glass -> glass
stopped -> stopp
news -> new
university -> university
universe -> universe
running -> runn
ran -> ran
```

- Kurallar sırayla deneniyor; ilk uyan ek kesiliyor. Kökün en az üç harf
  kalması şartı "is", "as" gibi kelimeleri koruyor; "ss" kuralı "glass"ı.
- **Tutarsız kökler:** "loves" → "love" ama "loved" ve "loving" → "lov".
  Aynı kelimenin biçimleri iki farklı köke düştü. "stopped" → "stopp",
  "running" → "runn": çift ünsüzü kural bilmiyor.
- **Fazla kesmek** (over-stemming): "news" → "new". Haber ile yeni aynı token
  oldu.
- **Az kesmek** (under-stemming): "ran" "run" ile birleşmedi; düzensiz
  fiilleri hiçbir ek kuralı yakalayamaz.

Gerçek kök bulucular (en bilineni **Porter** algoritması, nltk'de hazır) onlarca
kural ve istisna kullanır, ama aynı sınırlara sahiptir: harflere bakarlar,
anlama değil. Kök bulucunun çıktısı her zaman gerçek bir kelime değildir
("lov", "univers"); bu sorun değil, çünkü model için önemli olan aynı
kelimenin biçimlerinin aynı token'a düşmesi.

Bu verideki etkisi:

```python
stems = Counter(stem(w) for d in docs for w in d if w not in ENGLISH_STOP_WORDS)
print(len(stems))
groups = {}
for w in kept:
    groups.setdefault(stem(w), []).append(w)
for s, ws in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:4]:
    print(s, sorted(ws))
```

```text
292
day ['day', 'days']
lvoe ['lvoe', 'lvoes']
love ['love', 'loves']
work ['working', 'works']
```

Dağarcık yalnızca 298'den 292'ye indi: üretilmiş yorumlarda çekimli biçim az.
Gerçek yorumlarda kök bulma dağarcığı genellikle belirgin biçimde küçültür.
Gruplar kök bulmanın neyi birleştirdiğini gösteriyor; "lvoe" ile "lvoes"
yazım hatalı biçimler olarak kendi aralarında birleşti, doğru "love" ile
değil. Kök bulma yazım hatasını düzeltmez.

## Sözlük biçimi (lemmatisation)

**Lemmatisation** kelimeyi sözlükteki temel biçimine indirir: "was" → "be",
"better" → "good", "mice" → "mouse". Bunu kurallar değil bir **sözlük** ve
dil bilgisi yapar:

```python
LEMMAS = {"was": "be", "were": "be", "is": "be", "better": "good", "best": "good",
          "ran": "run", "running": "run", "batteries": "battery", "mice": "mouse"}

for w in ["was", "better", "ran", "mice", "loves"]:
    print(w, "->", LEMMAS.get(w, w))
```

```text
was -> be
better -> good
ran -> run
mice -> mouse
loves -> loves
```

Bu küçük sözlük fikri gösteriyor; sözlükte olmayan "loves" olduğu gibi kaldı.
Gerçek araçlar (spaCy, nltk'nin WordNet'i) yüz binlerce kelimelik sözlükler
ve kelimenin cümledeki görevini (isim mi fiil mi) kullanır: "saw" fiilse
"see", isimse "saw" (testere). Lemmatisation kök bulmadan daha doğru ama
daha yavaş ve dile özgü bir kaynak ister.

## Türkçe: sondan eklemeli bir dil

Türkçede bir kelimeye art arda pek çok ek gelir. İngilizce kök bulucu
Türkçede işe yaramaz; ekleri tekrar tekrar kesmek gerekir:

```python
SUFFIXES = ["imizden", "lerden", "lardan", "ler", "lar", "den", "dan", "de", "da"]


def turkish_root(word):
    changed = True
    while changed:
        changed = False
        for suffix in SUFFIXES:
            if word.endswith(suffix) and len(word) > len(suffix) + 1:
                word = word[: -len(suffix)]
                changed = True
                break
    return word


for w in ["evlerimizden", "kitaplardan", "okulda", "kalemler", "dede", "adalar"]:
    print(w, "->", turkish_root(w))
```

```text
evlerimizden -> ev
kitaplardan -> kitap
okulda -> okul
kalemler -> kalem
dede -> de
adalar -> ada
```

- "evlerimizden" önce "imizden" kesilerek "evler", sonra "ler" kesilerek
  "ev" oldu: döngü ek kalmayana kadar sürüyor.
- **"dede" → "de"**: "de" bulunma eki sanıldı. Kelimenin kendisi ekle
  bitiyor gibi görünüyorsa kural yanılıyor. "adalar" ise doğru: "ada".
- Türkçe için gerçek araçlar kelimenin bütün olası çözümlemelerini çıkaran
  **biçimbilim çözümleyicileri** (morphological analyser) kullanır; en
  bilineni Zemberek. Snowball kök bulucularının da Türkçe bir sürümü var.

## Değişken bilgiyi yer tutucuya çevirmek

Destek taleplerinde her sipariş numarası, tutar ve e-posta ayrı bir token'dı
(02. bölüm). Model için önemli olan "burada bir sipariş numarası var" bilgisi,
numaranın kendisi değil. Değişken bilgiyi bir **yer tutucuyla**
(placeholder) değiştirelim:

```python
import re
from text_data import make_tickets

RULES = [
    (r"[\w.+-]+@\w+\.\w+", "<email>"),
    (r"\$\d+(?:\.\d+)?", "<money>"),
    (r"[A-Z]+-\d+", "<order>"),
    (r"\d+", "<num>"),
]


def mask(text):
    for pattern, placeholder in RULES:
        text = re.sub(pattern, placeholder, text)
    return text


tickets = [t["text"] for t in make_tickets(2000)]
print(mask("Refund $12.50 for ORD-48213, mail ana12@example.com by 2026-03-14."))
before_ = {w for t in tickets for w in t.lower().split()}
after = {w for t in tickets for w in mask(t).lower().split()}
print(len(before_), len(after))
```

```text
Refund <money> for <order>, mail <email> by <num>-<num>-<num>.
1718 384
```

- Kurallar **sırayla** uygulanıyor: rakam kuralı en sonda, yoksa tutarın ve
  sipariş numarasının içindeki rakamlar önce `<num>` olurdu ve kalıp bir daha
  eşleşmezdi.
- Tarih üç `<num>`'a dönüştü; tarih ayrıca önemliyse ona da bir kural (ve
  `<date>`) yazılır.
- Dağarcık **1718'den 384'e** indi. Talep metinlerinin dörtte üçünden fazlası
  her biri tek bir talepte geçen numaralardan, tutarlardan ve adreslerden
  oluşan "kelimeler"di.

## Ne zaman normalleştirmemeli?

Normalleştirme bilgi atar. Kural şu: **görevin hangi farkı önemsediğini sor.**

- Duygu analizinde "not", "never", "very" önemli; durak listesinden çıkar.
- Konu bulmada "running" ile "run" aynı konu; kök bulma yardım eder.
- Bilgi çıkarmada sipariş numarasının kendisi gerekir; yer tutucu kullanma.
- İkinci modülde göreceğimiz alt kelime parçalama (BPE) ve dil modelleri kök
  bulmaya ihtiyaç duymaz; ekleri ve biçimleri kendisi öğrenir.

## Özet

- Normalleştirme aynı anlamın farklı biçimlerini birleştirip dağarcığı
  küçültür.
- Hazır durak listeleri "not", "no", "never" kelimelerini de siler; duygu
  analizinde olumsuzluğu yok eder.
- Kök bulma kurallarla ek keser: hızlıdır ama tutarsız kökler, fazla ve az
  kesme hataları yapar.
- Lemmatisation sözlük ve dil bilgisiyle temel biçimi bulur: daha doğru,
  daha pahalı.
- Türkçede ekler art arda gelir; basit kesici "dede"yi "de" yapar, gerçek
  çözüm biçimbilim çözümleyicisidir.
- Yer tutucular değişken bilgiyi tek token'a indirir: talep dağarcığı
  1718'den 384'e indi.
