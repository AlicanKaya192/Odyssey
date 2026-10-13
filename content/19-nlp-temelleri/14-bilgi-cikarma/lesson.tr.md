# Kural Tabanlı Bilgi Çıkarma

Şimdiye kadar bütün bir metne tek bir karar verdik: olumlu mu, hangi
kategori, hangi konu. **Bilgi çıkarma** (information extraction) metnin
içinden belirli parçaları çeker ve tabloya döker: sipariş numarası, tutar,
e-posta, tarih, hata kodu, şehir. Destek talebi "ORD-27246 numaralı sipariş
teslim edildi görünüyor" diyorsa, sistem o numarayı bulup sipariş
kaydını kendiliğinden açabilir. Bu bölümde kuralla, yani düzenli ifadeler
(regex) ve sözlüklerle bilgi çıkaracağız, kurallarımızı küçük bir el
etiketli veride ölçeceğiz ve çıkan bilgiyi tabloya dökeceğiz.

## Düzenli ifadelerle alan çıkarmak

Biçimi belli olan bilgiler için düzenli ifade en kısa yol. 02'de
parçalayıcıyı regex ile kurmuştuk; aynı aracı bu kez alan bulmak için
kullanıyoruz.

```python
import re

from text_data import make_tickets

PATTERNS = {
    "order": r"\bORD-\d{5}\b",
    "amount": r"\$\d+\.\d{2}",
    "email": r"\b[\w.]+@[\w.]+\.\w+\b",
    "date": r"\b\d{4}-\d{2}-\d{2}\b",
    "error": r"\bE\d{3,4}\b",
}


def extract(text):
    return {field: re.findall(p, text) for field, p in PATTERNS.items()}


tickets = make_tickets(2000)
print(tickets[4]["text"][:60])
print(extract(tickets[4]["text"]))
found = [extract(t["text"]) for t in tickets]
for field in PATTERNS:
    print(field, sum(bool(f[field]) for f in found))
```

```text
The app crashes every time I open the order page. Order ORD-
{'order': ['ORD-27246'], 'amount': [], 'email': [], 'date': [], 'error': []}
order 780
amount 261
email 173
date 46
error 191
```

- `\b` kelime sınırı: `ORD-123456` gibi daha uzun bir numaranın içinden
  `ORD-12345` kopartılmasın.
- `\d{5}` tam beş rakam, `\d{3,4}` üç ya da dört. Hata kodları `E401` gibi
  üç, `E1007` gibi dört rakamlı.
- 2000 talebin 780'inde sipariş numarası var. Bu sayılar **bulunanlar**;
  kaç tanesini kaçırdığımızı bilmiyoruz. Bunun için el ile etiketlenmiş
  örnek gerekiyor.

## Kuralı ölçmek

Kuralların asıl sorunu, yazanın aklına gelen biçimleri yakalamaları. Tutar
kuralımız `$12.49` biçimini biliyor; `$5` ya da `$1,200.00` gelirse ne olur?
Küçük bir **altın standart** (gold standard) kuralım: her cümle için doğru
cevabı elle yazıyoruz.

```python
from collections import Counter

GOLD = [
    ("I paid $12.49 for it.", ["$12.49"]),
    ("Refund $5 please.", ["$5"]),
    ("The total was $1,200.00 in March.", ["$1,200.00"]),
    ("I was charged $8.90 and $8.90 again.", ["$8.90", "$8.90"]),
    ("It costs 30 dollars.", ["30 dollars"]),
    ("Version 2.49 of the app crashes.", []),
    ("Order ORD-12345 never came.", []),
]


def score(pattern):
    tp = fp = fn = 0
    for text, gold in GOLD:
        got, want = Counter(re.findall(pattern, text)), Counter(gold)
        tp += sum((got & want).values())
        fp += sum((got - want).values())
        fn += sum((want - got).values())
    return round(tp / (tp + fp), 3), round(tp / (tp + fn), 3)


print(score(r"\$\d+\.\d{2}"))
print(score(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"))
```

```text
(1.0, 0.5)
(1.0, 0.833)
```

- İlk kural bulduğunda hep haklı (kesinlik 1,0), ama tutarların yalnızca
  yarısını buluyor (duyarlılık 0,5): `$5` ve `$1,200.00` kaçıyor.
- İkinci kural binlik ayracı (`(?:,\d{3})*`) ve isteğe bağlı kuruşu
  (`(?:\.\d{2})?`) biliyor: duyarlılık 0,833. "30 dollars" hâlâ kaçıyor;
  dolar işareti olmayan tutar için ayrı bir kural gerekir.
- `Counter` ile sayıyoruz, küme ile değil: aynı tutar iki kez geçiyorsa iki
  kez bulunmalı.
- Kural yazmak bir döngü: altın standarda yeni zor örnekler ekle, kuralı
  genişlet, kesinliğin düşmediğini ölç. Gerçek metinden alınmış birkaç yüz
  etiketli örnek, kuralın yanında en değerli şeydir.

## Bilgiyi tabloya dökmek

Çıkan bilgi bir tabloya girince sıradan veri analizi başlar:

```python
import pandas as pd

table = pd.DataFrame(found)
table["category"] = [t["category"] for t in tickets]
has_order = table["order"].str.len() > 0
print(has_order.groupby(table["category"]).mean().round(3))
errors = Counter(e for codes in table.loc[table["category"] == "technical", "error"]
                 for e in codes)
print(errors.most_common(3))
```

```text
category
account      0.120
billing      0.475
refund       0.641
shipping     0.669
technical    0.131
Name: order, dtype: float64
[('E500', 52), ('E401', 44), ('E403', 31)]
```

- Kargo ve iade taleplerinin üçte ikisinde sipariş numarası var, hesap ve
  teknik taleplerin yalnızca sekizde birinde. Bir sipariş numarası yoksa,
  sistem talebi otomatik olarak siparişe bağlayamaz; formda numara istemek
  gerekir.
- Teknik taleplerde en sık hata kodu `E500`: sunucu tarafı hatası. Bu
  bilgi talep metinlerinin içinde gömülüydü; çıkarınca bir sayıya dönüştü.

## Bağlamla anlam

Aynı biçimdeki iki tutar farklı şeyler anlatabilir: ödenen para mı, iade
edilen mi? Tutarın **solundaki** birkaç kelimeye bakalım:

```python
def amount_roles(text):
    roles = []
    for match in re.finditer(r"\$\d+\.\d{2}", text):
        left = text[max(0, match.start() - 30):match.start()].lower()
        roles.append("refund" if "refund" in left else "other")
    return roles


print(amount_roles("The refund of $20.00 has not reached my card."))
print(amount_roles("You refunded $10.00 but I paid more than that."))
print(Counter(r for t in tickets for r in amount_roles(t["text"])))
```

```text
['refund']
['refund']
Counter({'other': 193, 'refund': 80})
```

- 30 karakterlik sol pencere "refund" ya da "refunded" içeriyorsa tutar
  iade tutarı. 273 tutarın 80'i iade olarak işaretlendi.
- Bu da bir kural, ve sınırları var: "I did not ask for a refund, I paid
  $20.00 twice" cümlesinde pencere "refund"u görür ve yanılır. Bağlam
  kuralları kolayca karmaşıklaşır; bu noktada bir sıra etiketleme modeli
  (ikinci not ve sonraki modülde HMM) daha iyi bir yol olur.

## Sözlükle varlık bulmak

Bazı bilgilerin biçimi yok, yalnızca adı var: şehirler, ürünler, kişiler.
Bunları bir **sözlükle** (gazetteer, yer adları listesi) ararız. Talep
verisindeki şehirleri arayalım, sonra aynı sözlüğe "Nice" (Fransa'da bir
şehir) ekleyip yorumlarda deneyelim:

```python
from text_data import CITIES, make_reviews

city_pattern = r"\b(" + "|".join(CITIES) + r")\b"
cities = Counter(m for t in tickets for m in re.findall(city_pattern, t["text"]))
print(cities.most_common(3))
reviews = [r["text"] for r in make_reviews(2000)]
print(sum(bool(re.search(r"\bNice\b", r, re.I)) for r in reviews))
print(sum(bool(re.search(r"\bNice\b", r)) for r in reviews))
```

```text
[('Berlin', 20), ('Madrid', 20), ('Dublin', 18)]
70
0
```

- Sözlüğü `|` ile tek bir düzenli ifadeye çevirdik; `\b` "Oslo"nun
  "Oslonian" içinde bulunmasını önlüyor.
- Büyük/küçük harf duyarsız aramada "Nice" 70 yorumda "bulundu": hepsi
  "the strap is very nice" gibi sıfatlar. Duyarlı aramada 0; ama bu yalnızca
  bu veride "nice" hiç cümle başında olmadığı için. Cümle başındaki "Nice
  fit." yine şehir sayılırdı.
- Sözlük yöntemi **belirsizlik** (ambiguity) karşısında zayıf: "Paris" bir
  şehir ve bir isim, "Apple" bir şirket ve bir meyve. Ayırmak için bağlama
  bakmak gerekir.

## Özet

- Biçimi belli bilgiler (numara, tutar, e-posta, tarih, kod) düzenli
  ifadelerle çıkarılır; `\b` ve tekrar sayıları (`{5}`, `{3,4}`) kuralı
  sıkılaştırır.
- Kuralı küçük bir el etiketli altın standartta kesinlik ve duyarlılıkla
  ölç; kural yalnızca aklına gelen biçimleri yakalar.
- Çıkan bilgi tabloya girince sıradan analizle soruya dönüşür.
- Bağlam kuralları ve sözlükler hızlı başlangıç verir, ama belirsizlik ve
  bağlam karmaşıklaştıkça öğrenen modellere ihtiyaç doğar.
