# Birliktelik Kuralları

"Ekmek alan tereyağı da alıyor" gibi cümleler **birliktelik kurallarıdır**
(association rules). Market sepeti analizi (market basket analysis) bunları
binlerce alışverişten çıkarır: hangi ürünler birlikte sık görülüyor ve biri
varken diğerinin olma olasılığı ne kadar artıyor? Bu bölümde üç ölçüyü
(destek, güven, kaldıraç), sık öğe kümelerini bulan **Apriori** algoritmasını
ve güvenin neden yanıltabildiğini görüyoruz.

## Sepetler ve destek

Elimizde 2000 sepet olsun. Veriyi kuralları bildiğimiz bir üreteçle
yapıyoruz: tereyağı ekmek varken daha olası, şeker kahve varken, cips bira
varken; çay ise kahve varken **daha az** olası (biri ötekinin yerine geçiyor).
Süt herkesin sepetinde sık, ama hiçbir şeye bağlı değil.

Bir öğe kümesinin **desteği** (support), onu içeren sepetlerin oranıdır.

```python
import numpy as np
from itertools import combinations

# (ürün, olasılık) ya da (ürün, bağlı olduğu ürün, varken, yokken)
RULES = [("milk", 0.6), ("bread", 0.4), ("butter", "bread", 0.6, 0.1),
         ("coffee", 0.35), ("sugar", "coffee", 0.55, 0.1),
         ("tea", "coffee", 0.15, 0.4), ("beer", 0.2),
         ("chips", "beer", 0.5, 0.08), ("eggs", 0.3), ("apples", 0.25)]


def make_basket(r):
    b = set()
    for u, rule in zip(r, RULES):
        p = rule[1] if len(rule) == 2 else (rule[2] if rule[1] in b else rule[3])
        if u < p:
            b.add(rule[0])
    return frozenset(b)


rng = np.random.default_rng(18)
baskets = [make_basket(rng.random(10)) for _ in range(2000)]


def support(items):
    items = frozenset(items)
    return sum(1 for b in baskets if items <= b) / len(baskets)


print(sum(len(b) for b in baskets) / len(baskets))
for s in (["milk"], ["bread"], ["bread", "butter"], ["beer", "chips"]):
    print(s, round(support(s), 3))
```

```text
3.1575
['milk'] 0.585
['bread'] 0.404
['bread', 'butter'] 0.236
['beer', 'chips'] 0.112
```

Bir sepette ortalama 3,16 ürün var. Sütün desteği 0,585: sepetlerin
yarısından fazlasında. Ekmek ile tereyağı birlikte sepetlerin %23,6'sında.

## Apriori: sık öğe kümeleri

10 ürünün `2^10 − 1 = 1023` boş olmayan alt kümesi var; 100 ürünle bu sayı
astronomik. **Apriori** bir gözleme dayanır: bir küme sıksa bütün alt
kümeleri de sıktır. Tersinden: bir küme seyrekse, onu içeren hiçbir küme
sık olamaz. Bu yüzden kümeler **katman katman** büyütülür:

1. Tek ürünlerin desteğini say, eşiğin altındakileri at.
2. Kalan `k` elemanlı kümelerden `k + 1` elemanlı adaylar kur; **bütün** `k`
   elemanlı alt kümeleri sık olmayan adayı saymadan at (budama).
3. Adayların desteğini say, eşiğin altındakileri at; aday kalmayana kadar.

<figure class="fig">
<svg viewBox="0 0 520 270" width="520" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="13.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="13.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="72.5" y="34" font-size="11" text-anchor="middle">milk 0.58</text><rect class="box" x="138.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="138.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="197.5" y="34" font-size="11" text-anchor="middle">bread 0.40</text><rect class="box" x="263.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="263.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="322.5" y="34" font-size="11" text-anchor="middle">butter 0.30</text><rect class="box" x="388.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="388.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="447.5" y="34" font-size="11" text-anchor="middle">chips 0.18</text><rect class="box" x="11.7" y="111" width="80" height="28" rx="6"/><rect class="curve" x="11.7" y="111" width="80" height="28" rx="6"/><text class="ink" x="51.7" y="129" font-size="11" text-anchor="middle">mi br 0.23</text><rect class="box" x="95.0" y="111" width="80" height="28" rx="6"/><rect class="curve" x="95.0" y="111" width="80" height="28" rx="6"/><text class="ink" x="135.0" y="129" font-size="11" text-anchor="middle">mi bu 0.17</text><rect class="box" x="178.3" y="111" width="80" height="28" rx="6"/><text class="dim" x="218.3" y="129" font-size="11" text-anchor="middle">mi ch 0.11</text><rect class="box" x="261.7" y="111" width="80" height="28" rx="6"/><rect class="curve" x="261.7" y="111" width="80" height="28" rx="6"/><text class="ink" x="301.7" y="129" font-size="11" text-anchor="middle">br bu 0.24</text><rect class="box" x="345.0" y="111" width="80" height="28" rx="6"/><text class="dim" x="385.0" y="129" font-size="11" text-anchor="middle">br ch 0.07</text><rect class="box" x="428.3" y="111" width="80" height="28" rx="6"/><text class="dim" x="468.3" y="129" font-size="11" text-anchor="middle">bu ch 0.05</text><rect class="box" x="14.5" y="206" width="116" height="28" rx="6"/><text class="dim" x="72.5" y="224" font-size="11" text-anchor="middle">mi br bu 0.13</text><rect class="box" x="139.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="197.5" y="224" font-size="11" text-anchor="middle">mi br ch ✕</text><rect class="box" x="264.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="322.5" y="224" font-size="11" text-anchor="middle">mi bu ch ✕</text><rect class="box" x="389.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="447.5" y="224" font-size="11" text-anchor="middle">br bu ch ✕</text></svg>
<figcaption>Dört ürünle Apriori (eşik 0,15; adlar ilk iki harfle: mi süt, br ekmek, bu tereyağı, ch cips). Mor çerçeve sık küme, gri seyrek; kesikli ve ✕ olanlar budandı: bir alt kümesi seyrek olduğu için desteği hiç sayılmadı.</figcaption>
</figure>

```python
def apriori(baskets, min_support):
    n = len(baskets)
    level = [frozenset([i]) for i in sorted({i for b in baskets for i in b})]
    frequent, counted, k = {}, 0, 1
    while level:
        counted += len(level)                      # desteği sayılan aday
        counts = {c: sum(1 for b in baskets if c <= b) for c in level}
        kept = {c: v / n for c, v in counts.items() if v / n >= min_support}
        frequent.update(kept)
        k += 1
        cands = set()
        for a, b in combinations(list(kept), 2):
            u = a | b
            if len(u) == k and all(frozenset(s) in kept
                                   for s in combinations(u, k - 1)):
                cands.add(u)
        level = sorted(cands, key=sorted)
    return frequent, counted


freq, counted = apriori(baskets, 0.05)
sizes = {}
for f in freq:
    sizes[len(f)] = sizes.get(len(f), 0) + 1
print(sizes, counted)
items = sorted({i for b in baskets for i in b})
brute = {frozenset(c) for k in range(1, len(items) + 1)
         for c in combinations(items, k) if support(c) >= 0.05}
print(brute == set(freq))
```

```text
{1: 10, 2: 44, 3: 22, 4: 1} 171
True
```

Destek eşiği 0,05 ile 77 sık küme var: 10 tek ürün, 44 ikili, 22 üçlü, 1
dörtlü. Apriori bunları bulmak için yalnızca 171 adayın desteğini saydı; bütün
1023 alt kümeyi tek tek sayan kaba kuvvet aynı kümeleri buldu. Ürün sayısı
arttıkça fark katlanarak büyür.

## Kurallar: güven ve kaldıraç

Sık bir kümeden `A → B` kuralı çıkar (`A` ve `B` kümeyi ikiye ayırır):

- **Güven** (confidence): `destek(A ∪ B) / destek(A)`, yani `A` varken `B`'nin
  de olma oranı.
- **Kaldıraç** (lift): `güven / destek(B)`. 1'den büyükse `A`, `B`'yi
  **artırıyor**; 1 civarındaysa ilişki yok; 1'den küçükse azaltıyor.

```python
def make_rules(freq, min_conf):
    rules = []
    for f, s in freq.items():
        for r in range(1, len(f)):
            for a in combinations(sorted(f), r):
                A, B = frozenset(a), f - frozenset(a)
                conf = s / freq[A]
                if conf >= min_conf:
                    lift = conf / freq[B]
                    rules.append((sorted(A), sorted(B),
                                  round(conf, 3), round(lift, 2)))
    return sorted(rules, key=lambda x: -x[3])


rules = make_rules(freq, 0.5)
print(len(rules))
for A, B, conf, lift in rules[:4]:
    print(A, "->", B, conf, lift)
for A, B, conf, lift in rules:
    if (A, B) in ((["bread"], ["butter"]), (["tea"], ["milk"])):
        print(A, "->", B, conf, lift)
```

```text
55
['beer'] -> ['chips'] 0.527 2.86
['chips'] -> ['beer'] 0.607 2.86
['beer', 'milk'] -> ['chips'] 0.525 2.85
['chips', 'milk'] -> ['beer'] 0.578 2.72
['bread'] -> ['butter'] 0.585 1.93
['tea'] -> ['milk'] 0.615 1.05
```

Kaldıraca göre en güçlü kural bira ile cips arasında (2,86): cips alanların
%60,7'si bira da almış, oysa bütün sepetlerin yalnızca %21'inde bira var. Ekmek → tereyağı da güçlü (kaldıraç 1,93).

Asıl ders son satırda: **çay → süt** kuralının güveni 0,615, yani ekmek →
tereyağı kuralınınkinden (0,585) yüksek. Ama kaldıracı 1,05: süt zaten
sepetlerin %58,5'inde var, çay bunu neredeyse hiç değiştirmiyor. Yalnızca
güvene bakan biri "çay alana süt öner" diye anlamsız bir kural çıkarırdı.
Popüler ürün her kuralın sağ tarafında yüksek güvenle görünür; kaldıraç bunu
düzeltir.

## Destek eşiği

```python
for ms in (0.2, 0.1, 0.05, 0.02, 0.01):
    f, c = apriori(baskets, ms)
    print(ms, len(f), c, max(len(x) for x in f))
```

```text
0.2 13 46 2
0.1 30 67 3
0.05 77 171 4
0.02 177 264 5
0.01 318 434 5
```

Eşik 0,2'den 0,01'e inerken sık küme sayısı 13'ten 318'e çıkıyor, en büyük
küme 2 üründen 5 ürüne büyüyor. Düşük eşik nadir ama ilginç birliktelikleri
yakalar, karşılığında çok daha fazla aday sayılır ve kural listesi
okunmayacak kadar uzar. Gerçek bir markette binlerce ürün olduğu için eşik
çok dikkatli seçilir.

## Özet

- Destek: kümeyi içeren sepetlerin oranı. Güven: `A` varken `B`'nin oranı.
  Kaldıraç: güvenin `B`'nin genel oranına bölümü.
- Apriori: sık kümenin bütün alt kümeleri sıktır; adaylar katman katman
  kurulur ve budanır.
- Kuralları güvene göre değil kaldıraca göre (ya da ikisine birlikte) sırala:
  popüler ürünler yüksek güvenle yanıltır.
- Destek eşiği küçüldükçe küme ve kural sayısı hızla büyür.
