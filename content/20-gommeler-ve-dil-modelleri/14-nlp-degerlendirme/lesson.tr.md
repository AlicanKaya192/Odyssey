# NLP'de Değerlendirme

Sınıflandırmada değerlendirme kolaydır: tahmin ya doğru etikettir ya
değildir. Ama bir model **metin üretiyorsa** (çeviri, özet, cevap) "doğru"
tek bir metin değildir: aynı şey onlarca farklı cümleyle söylenebilir. Bu
bölümde metin üretimi için en yaygın iki otomatik ölçüyü, **BLEU** ve
**ROUGE**'u sıfırdan yazıp neyi ölçtüklerine ve neyi kaçırdıklarına
bakacağız. Sonra etiketlerin kendisine döneceğiz: iki insan aynı metne aynı
etiketi veriyor mu, ve bu değerlendirmeyi nasıl sınırlıyor?

## BLEU: kelime gruplarının kesinliği

**BLEU** (Papineni ve arkadaşları, 2002) makine çevirisi için geliştirildi.
Adayın 1, 2, 3 ve 4 kelimelik gruplarının ne kadarının referansta da
geçtiğine bakar (kesinlik). Bir grup referansta kaç kez geçiyorsa en fazla
o kadar sayılır (kırpma); "the the the" hilesi böyle önlenir. Dört
kesinliğin geometrik ortalaması alınır ve referanstan kısa adaylar
**kısalık cezası** (brevity penalty) ile cezalandırılır.

```python
import math
from collections import Counter


def ngrams(words, n):
    return Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))


def bleu(candidate, reference, max_n=4):
    c, r = candidate.split(), reference.split()
    logs = []
    for n in range(1, max_n + 1):
        cand, ref = ngrams(c, n), ngrams(r, n)
        clipped = sum(min(k, ref[g]) for g, k in cand.items())
        logs.append(math.log(max(clipped, 1e-9) / max(sum(cand.values()), 1)))
    brevity = min(1.0, math.exp(1 - len(r) / len(c)))
    return round(brevity * math.exp(sum(logs) / max_n), 3)


reference = ("your parcel will arrive on monday and we will send "
             "a tracking number")
candidates = [
    "your parcel will arrive on monday and we will send a tracking number",
    "your parcel will arrive on monday and we will email a tracking code",
    "the package is coming monday , you will get a tracking number by email",
    "your parcel will arrive",
    "the the the the the the the the the the the the",
]
for cand in candidates:
    print(bleu(cand, reference), cand)
```

```text
1.0 your parcel will arrive on monday and we will send a tracking number
0.702 your parcel will arrive on monday and we will email a tracking code
0.001 the package is coming monday , you will get a tracking number by email
0.105 your parcel will arrive
0.0 the the the the the the the the the the the the
```

- Referansın aynısı 1,0. İki kelimesi değişen aday 0,702.
- Üçüncü aday **aynı anlamı** taşıyor ("package is coming monday", takip
  numarası e-postayla) ama BLEU 0,001: kelimeler farklı, 3 ve 4 kelimelik
  ortak grup neredeyse yok. BLEU anlamı değil **yüzeyi** ölçer.
- Kısa aday "your parcel will arrive" kelimelerinin hepsi doğru olduğu
  hâlde kısalık cezasıyla 0,105'e iniyor. Tekrar hilesi 0.
- BLEU tek bir cümlede gürültülüdür; bütün bir sınav kümesi üzerinden
  toplanınca sistemleri karşılaştırmakta işe yarar. Birden çok referans
  kullanmak da yardım eder (birinci not).

## ROUGE: özetlerde geri çağırma

**ROUGE** (Lin, 2004) özetler için yaygın. BLEU'nun tersine **geri
çağırmaya** bakar: referans özetin kelime gruplarının ne kadarı adayda var?
ROUGE-1 tek kelimeler, ROUGE-2 ikililer; **ROUGE-L** ise en uzun ortak alt
diziye (longest common subsequence) bakar, yani kelimelerin sırasını da
hesaba katar.

```python
def rouge_n(candidate, reference, n):
    cand, ref = ngrams(candidate.split(), n), ngrams(reference.split(), n)
    overlap = sum(min(k, cand[g]) for g, k in ref.items())
    return round(overlap / max(sum(ref.values()), 1), 3)


def lcs(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                table[i + 1][j + 1] = table[i][j] + 1
            else:
                table[i + 1][j + 1] = max(table[i][j + 1], table[i + 1][j])
    return table[-1][-1]


summary = "the parcel arrived damaged and the customer wants a refund"
outputs = ["the customer wants a refund because the parcel arrived damaged",
           "customer parcel damaged refund",
           "the customer wants a new phone and the parcel is fine"]
for out in outputs:
    rouge_l = lcs(out.split(), summary.split()) / len(summary.split())
    print(rouge_n(out, summary, 1), rouge_n(out, summary, 2), round(rouge_l, 3))
```

```text
0.9 0.778 0.5
0.4 0.0 0.3
0.7 0.556 0.4
```

Sütunlar: ROUGE-1, ROUGE-2, ROUGE-L.

- Birinci aday doğru ve akıcı; cümleleri yer değiştirdiği için ROUGE-L 0,5'e
  iniyor ama ROUGE-1 0,9.
- İkinci aday dört anahtar kelime: anlamın özü doğru ama ROUGE-1 0,4.
- Üçüncü aday **yanlış**: müşteri yeni telefon istiyor, kargo sağlam. Yine
  de ROUGE-1 0,7 ve ROUGE-2 0,556 ile anahtar kelime listesinden **yüksek**
  puan alıyor. Ortak kelimeler ("the customer wants a", "the parcel") anlamı
  ters çevrilmiş bir özete puan kazandırıyor.
- Ders: kelime örtüşmesine dayalı ölçüler hızlı ve ucuzdur, ama doğruluğu
  ölçmez. Gömme benzerliğine dayalı ölçüler (04'teki gibi) eş anlamlıları
  yakalar; bugün çok kullanılan bir yol da güçlü bir dil modelini **hakem**
  olarak kullanmaktır. Hiçbiri insan değerlendirmesinin yerini tamamen
  tutmaz.

## Etiketler ne kadar güvenilir?

İnsan değerlendirmesi de kusursuz değildir. 1000 yorumu iki kişinin
etiketlediğini düşünelim; ikisi de yorumların %20'sinde dikkatsiz davranıp
rastgele bir etiket seçiyor. İki etiketleyici ne kadar anlaşıyor? Düz
uyuşma oranı yanıltıcıdır, çünkü iki kişi rastlantıyla da aynı etiketi
verebilir. **Cohen'in kappa'sı** rastlantıyla beklenen uyuşmayı çıkarır:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

`p_o` gözlenen uyuşma, `p_e` iki kişinin etiket oranlarından hesaplanan
rastlantı uyuşması.

```python
import random

from text_data import make_reviews

reviews = make_reviews(1000)
gold = [r["label"] for r in reviews]


def annotator(seed, error):
    rng = random.Random(seed)
    labels = ["positive", "neutral", "negative"]
    return [rng.choice(labels) if rng.random() < error else g for g in gold]


def cohen_kappa(a, b):
    observed = sum(x == y for x, y in zip(a, b)) / len(a)
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in ca) / len(a) ** 2
    kappa = (observed - expected) / (1 - expected)
    return round(observed, 3), round(expected, 3), round(kappa, 3)


ann_a, ann_b = annotator(1, 0.2), annotator(2, 0.2)
print(Counter(gold).most_common())
print(*cohen_kappa(ann_a, ann_b))
always = ["positive"] * len(gold)
print(*cohen_kappa(always, gold))
```

```text
[('positive', 671), ('negative', 186), ('neutral', 143)]
0.772 0.442 0.591
0.671 0.671 0.0
```

- İki etiketleyici %77,2 anlaşıyor; ama rastlantıyla %44,2 beklenirdi
  (yorumların çoğu olumlu). Kappa 0,591: "orta" uyuşma.
- Her yoruma "positive" diyen biri gerçek etiketlerle %67,1 uyuşuyor; kappa
  **0**. Bu kadar uyuşma tamamen sınıf dağılımından geliyor, hiçbir bilgi
  yok.
- Gerçek projelerde etiketleme yönergesi yazılır, birkaç kişi aynı örnekleri
  etiketler ve kappa ölçülür. Kappa düşükse sorun çoğu zaman modelde değil
  görevin tanımındadır: insanlar bile neyin "nötr" olduğunda anlaşamıyordur.

## Özet

- BLEU adayın kelime gruplarının referansta geçme oranına (kesinlik), ROUGE
  referansın kelime gruplarının adayda geçme oranına (geri çağırma) bakar.
- İkisi de yüzeyi ölçer: aynı anlamı farklı kelimelerle söyleyen aday
  düşük, ortak kelimeleri olan yanlış bir özet yüksek puan alabilir.
- Otomatik ölçüler sistemleri karşılaştırmak için ucuz bir başlangıç;
  önemli kararlar insan değerlendirmesiyle desteklenir.
- Cohen'in kappa'sı rastlantı uyuşmasını çıkarır; etiketlerin ne kadar
  güvenilir olduğunu ve modelden ne kadarını bekleyebileceğimizi gösterir
  (ikinci not).
