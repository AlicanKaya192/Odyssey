# Alt Kelime Parçalama: BPE

Kelime düzeyindeki her yöntemin aynı sorunu var: **dağarcık dışı**
(out-of-vocabulary, OOV) kelime. Eğitimde görülmemiş bir kelimenin sayımı,
TF-IDF sütunu, vektörü yok. Harf düzeyine inmek bu sorunu çözer (her kelime
harflerden oluşur) ama dizileri çok uzatır. **BPE** (byte pair encoding,
bayt çifti kodlama) ikisinin arasında bir yol bulur: sık görülen kelimeler
tek parça kalır, nadir kelimeler anlamlı **alt kelime** (subword)
parçalarına bölünür. Bugünkü büyük dil modellerinin neredeyse hepsi BPE ya
da ona çok benzer bir yöntemle parçalanmış metinle çalışır. Bu bölümde BPE'yi
sıfırdan yazacağız.

## Dağarcık dışı kelimeler

5000 talepten bir kelime dağarcığı kuralım ve 2000 yeni talepte kaç kelimenin
dağarcıkta olmadığına bakalım:

```python
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z]+")
train = Counter(w for t in make_tickets(5000, seed=1)
                for w in TOKEN.findall(t["text"].lower()))
test = Counter(w for t in make_tickets(2000)
               for w in TOKEN.findall(t["text"].lower()))
unseen = {w: n for w, n in test.items() if w not in train}
print(len(train), len(unseen), sum(unseen.values()), sum(test.values()))
print(sorted(unseen, key=unseen.get, reverse=True)[:5])
```

```text
429 16 19 36716
['notificaitons', 'cusotmer', 'stopepd', 'ocotber', 'shippnig']
```

- 36 716 kelimenin yalnızca 19'u dağarcık dışında; ama bu 16 farklı kelime
  yazım hatalarından ibaret: "notificaitons", "cusotmer"... Yazım hatalarının
  sonu yok; her yeni metin yenilerini getirir.
- Gerçek dilde dağarcık dışı kelimeler bundan çok daha sık: özel adlar, yeni
  ürünler, yabancı kelimeler, Türkçe gibi dillerde ekli biçimler.

## BPE'yi öğrenmek

BPE'nin fikri bir sıkıştırma yönteminden geliyor (Gage, 1994) ve NLP'ye
Sennrich ve arkadaşları (2016) taşıdı:

1. Her kelimeyi harflerine ayır; sonuna bir kelime sonu işareti `</w>` ekle.
2. Bütün kelimelerde yan yana gelen sembol çiftlerini say (kelimenin
   sıklığıyla ağırlıklı).
3. En sık çifti birleştirip tek sembol yap; bu bir **birleştirme kuralı**.
4. İstenen sayıda kural çıkana kadar 2'ye dön.

```python
def pair_counts(words):
    pairs = Counter()
    for symbols, n in words.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[a, b] += n
    return pairs


def merge(symbols, pair):
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def learn_bpe(counts, n_merges):
    words = {tuple(w) + ("</w>",): n for w, n in counts.items()}
    merges = []
    for _ in range(n_merges):
        pairs = pair_counts(words)
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))
        merges.append(best)
        new_words = Counter()
        for symbols, n in words.items():
            new_words[merge(symbols, best)] += n
        words = new_words
    return merges


merges = learn_bpe(train, 300)
print(merges[:4])
print(merges[4:8])
```

```text
[('e', '</w>'), ('s', '</w>'), ('d', '</w>'), ('o', 'r')]
[('t', 'h'), ('t', '</w>'), ('e', 'r'), ('y', '</w>')]
```

- İlk kurallar kelime sonları: `e</w>`, `s</w>`, `d</w>`. İngilizcede en sık
  harf çiftleri kelimelerin sonunda.
- Sonra `or`, `th`, `er`. Sonraki kurallar bu parçaları birleştiriyor
  (`th` + `e</w>` = "the") ve adım adım daha uzun, anlamlı parçalar
  kuruluyor.
- Eşit sayılı çiftlerde `(sayı, çift)` anahtarı sonucu belirli kılıyor; her
  çalıştırmada aynı kurallar çıkıyor.

## Yeni kelimeyi parçalamak

Yeni bir kelime harflerine ayrılır ve öğrenilen kurallar **öğrenildikleri
sırayla** uygulanır:

```python
def encode(word, merges):
    symbols = tuple(word) + ("</w>",)
    for pair in merges:
        symbols = merge(symbols, pair)
    return list(symbols)


for word in ["refund", "refunded", "parcel", "pracel", "zebra"]:
    print(word, encode(word, merges))
```

```text
refund ['refund</w>']
refunded ['refun', 'd', 'ed</w>']
parcel ['parcel</w>']
pracel ['p', 'r', 'ac', 'e', 'l</w>']
zebra ['z', 'e', 'b', 'r', 'a</w>']
```

- "refund" ve "parcel" sık kelimeler: tek parça.
- "refunded" eğitimde az geçti: `refun + d + ed</w>`. Yine de anlamlı
  parçaları var; bir model "refun" parçası için öğrendiğini burada da
  kullanabilir. (`refund` + `ed` daha güzel olurdu; BPE dilbilgisi bilmez,
  yalnızca sayar.)
- Yazım hatalı "pracel" de parçalara bölündü: `p + r + ac + e + l</w>`.
- "zebra" taleplerde hiç geçmedi: harflerine kadar bölündü. Ama **hiçbir
  kelime dağarcık dışı kalmaz**: en kötü durumda harflerle yazılır.
- Kelime sonu işareti sayesinde parçalar yeniden birleştirilebilir: `</w>`
  gördüğün yerde boşluk koy.

## Kaç kural?

Kural sayısı bir ayar: az kural kısa dağarcık ama uzun diziler, çok kural
tersini verir.

```python
def symbols_used(counts, merges):
    return {s for w in counts for s in encode(w, merges)}


for n in [0, 50, 100, 300, 1000]:
    m = learn_bpe(train, n)
    tokens = sum(len(encode(w, m)) * c for w, c in test.items())
    print(n, len(symbols_used(train, m)), round(tokens / sum(test.values()), 2))
```

```text
0 26 5.08
50 75 2.95
100 121 2.38
300 277 1.34
1000 468 1.0
```

- 0 kural, yani harf düzeyi: 26 sembol ama kelime başına 5,08 parça.
- 300 kuralla kelime başına 1,34 parça; çoğu kelime tek parça, nadir
  olanlar bölünüyor.
- 1000 kuralda neredeyse her kelime tek parçaya inmiş (1,0); artık kelime
  düzeyine çok yakın. Gerçek modellerde dağarcık genellikle 30 000 ile
  100 000 parça arasında seçilir.

## Özet

- Kelime düzeyinde dağarcık dışı kelime kaçınılmaz; harf düzeyi dizileri
  uzatır.
- BPE en sık sembol çiftini tekrar tekrar birleştirerek bir parça dağarcığı
  öğrenir; sık kelimeler tek parça, nadirler alt kelimelere bölünür.
- Yeni kelime, kurallar öğrenildikleri sırayla uygulanarak parçalanır; hiçbir
  kelime dağarcık dışı kalmaz.
- Kural sayısı dağarcık boyu ile dizi uzunluğu arasında bir ödünleşim.
