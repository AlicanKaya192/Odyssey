# Promptları Değerlendirmek

Bu modülde bir sürü prompt ilkesi gördük: net talimat, örnekler, yapılı
çıktı, sistem mesajı. Her birinde aynı uyarıyı yaptık: bir ilkenin **senin
modelinde** işe yarayıp yaramadığını ancak ölçerek öğrenirsin. Bu bölüm o
ölçmenin nasıl yapıldığını anlatıyor: bir **değerlendirme kümesi**
kurmak, iki prompt sürümünün cevaplarını aynı kümede puanlamak, hataları
türlerine ayırmak ve iki sürüm arasındaki farkın gerçek mi rastlantı mı
olduğuna bakmak.

## Değerlendirme kümesi ve kayıtlı cevaplar

Değerlendirme kümesi, doğru cevabı bilinen girdilerdir: burada
`shop_data.py`'deki 40 destek mesajı ve bir çalışanın verdiği
kategoriler. Gerçek bir projede her prompt sürümünü bu mesajların hepsinde
modele sorar, cevapları kaydeder ve kayıtları puanlarsın.

Bu ders gerçek bir modele bağlanamadığı için `shop_data.py`'de iki prompt
sürümünün (`v1`: yalnızca talimat, `v2`: örnekli ve biçimi net) 40 mesaja
verdiği cevaplar **ders için yazılmış örnek yanıtlar** olarak duruyor.
Aşağıdaki sayılar bu örnek yanıtların puanı; bir modelin ölçümü değil.
Öğrenilen şey puanlama yöntemi; kendi modelinde aynı kodu kendi kayıtlarına
uygularsın.

## Üç ayrı ölçü

Bir cevabı puanlarken üç soru ayrı ayrı sorulur: cevap birebir istenen
biçimde mi, program onu ayrıştırabiliyor mu ve ayrıştırılan değer doğru
mu?

```python
from collections import Counter

from shop_data import TICKETS, LABELS, RECORDED


def normalize(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


gold = [t["label"] for t in TICKETS]
for version, replies in RECORDED.items():
    exact = sum(r == g for r, g in zip(replies, gold))
    parsed = [normalize(r) for r in replies]
    valid = sum(p != "needs_review" for p in parsed)
    right = sum(p == g for p, g in zip(parsed, gold))
    print(f"{version}: exact {exact}/40  valid {valid}/40  right {right}/40")
```

```text
v1: exact 26/40  valid 36/40  right 31/40
v2: exact 35/40  valid 39/40  right 36/40
```

`v1`'in 40 cevabından yalnızca 26'sı birebir istenen biçimde. Zararsız
farkları temizleyen katı ayrıştırıcıdan sonra 36'sı ayrıştırılabiliyor,
31'i doğru. `v2`'de 35 birebir, 39 ayrıştırılabilir, 36 doğru. Biçimi ve
doğruluğu ayrı saymak önemli: `v1`'in eksiklerinin bir kısmı yanlış
kategori değil, "It is about payment." gibi ayrıştırılamayan cümleler.
Biçim sorununu biçim talimatı ve örnekler çözer; yanlış kategoriyi
kategorilerin tanımları.

## Hataların türü

Toplam puan neyin düzeltileceğini söylemez. Hangi kategorinin hangisiyle
karıştığını sayalım:

```python
for version, replies in RECORDED.items():
    parsed = [normalize(r) for r in replies]
    misses = Counter((g, p) for g, p in zip(gold, parsed) if g != p)
    print(version)
    for (truth, answer), count in misses.most_common():
        print(f"   {truth:8} -> {answer:12} {count}")
```

```text
v1
   refunds  -> payment      2
   payment  -> needs_review 1
   returns  -> needs_review 1
   refunds  -> shipping     1
   payment  -> refunds      1
   shipping -> needs_review 1
   shipping -> payment      1
   refunds  -> needs_review 1
v2
   refunds  -> payment      1
   refunds  -> needs_review 1
   payment  -> refunds      1
   warranty -> returns      1
```

İki sürümde de en çok karışan çift para iadesi ile ödeme
(`refunds` ↔ `payment`): "iki kez para çekildi" ya da "hediye kartıyla
ödedim" gibi mesajlar iki kategoriye de benziyor. Bu, prompt'a neyin
ekleneceğini söylüyor: iki kategorinin farkını anlatan bir cümle ve bu
tür mesajlardan bir örnek. `v1`'in dört `needs_review`'u ise tek bir
sorundan geliyor: cevabın biçimi.

## Fark gerçek mi?

Kırk mesaj küçük bir küme. İki sürüm arasındaki fark birkaç mesajın şansına
bağlı olabilir. İki şeye bakıyoruz: sürümlerin **farklı** cevap verdiği
mesajlar (aynı cevap verilenler farkı açıklamaz) ve önceki modülde
gördüğümüz **yeniden örnekleme** (bootstrap) ile farkın aralığı.

```python
import random

ok1 = [normalize(r) == g for r, g in zip(RECORDED["v1"], gold)]
ok2 = [normalize(r) == g for r, g in zip(RECORDED["v2"], gold)]
print("only v2 right:", sum(b and not a for a, b in zip(ok1, ok2)))
print("only v1 right:", sum(a and not b for a, b in zip(ok1, ok2)))
rng = random.Random(0)
diffs = []
for _ in range(2000):
    picks = [rng.randrange(40) for _ in range(40)]
    diffs.append(sum(ok2[i] - ok1[i] for i in picks) / 40)
diffs.sort()
print("difference", (sum(ok2) - sum(ok1)) / 40,
      "90% interval", diffs[100], diffs[1899])
```

```text
only v2 right: 7
only v1 right: 2
difference 0.125 90% interval 0.0 0.25
```

Sürümler 40 mesajın 9'unda farklı sonuç veriyor: 7'sinde yalnızca `v2`,
2'sinde yalnızca `v1` doğru. Fark 0,125 (beş mesaj), ama yeniden
örneklemenin %90 aralığı 0 ile 0,25 arasında ve alt ucu sıfır. `v2` önde
görünüyor, ama bu kümeyle fark kesinleşmiyor; daha çok mesajla ölçmek
gerekir. Kırk mesajlık bir kümede beş mesajlık fark bile bu kadar oynak.

## Model başka bir modeli puanlarsa

Kategori gibi tek doğru cevabı olan işlerde puanlama kodla yapılır. Bir
özetin iyi olup olmadığı gibi açık uçlu işlerde ise sık kullanılan bir
yol, başka bir model çağrısına bir **puanlama ölçütü** (rubric) verip
cevabı puanlatmaktır ("model as a judge"). Bu yol hızlıdır ama puanlayan
da bir modeldir:

- Puanlayanın kendi önyargıları olabilir: uzun cevabı ya da kendi
  üslubuna benzeyen cevabı kayırabilir.
- Puanlayanın kararlarını **insan etiketleriyle** karşılaştırmadan ona
  güvenme; önceki modülde iki etiketleyicinin uyuşmasını ölçtüğümüz gibi
  puanlayanla insanların uyuşmasını ölç.
- Ölçütü net yaz: "iyi mi?" değil, "ürün adı geçiyor mu, vaat var mı,
  soruya cevap veriyor mu?" gibi ayrı sorular.

## Değerlendirme kümesi kurarken

- **Gerçek girdilerden kur** ve zor durumları ekle: iki kategori arasında
  kalan mesajlar, cevabı olmayan sorular, kötü niyetli mesajlar.
- **Kümeyi değiştirme, büyüt.** Eski sürümlerle karşılaştırabilmek için
  aynı kümeye yeni örnek eklenir, eskiler silinmez.
- **Geliştirme ve test kümesini ayır.** Prompt'u bir kümede
  iyileştirirsen o kümedeki puan iyimser olur; son kararı hiç bakmadığın
  bir test kümesiyle ver (Sistemli İyileştirme bölümünde).
- **Her prompt değişikliğinde yeniden çalıştır.** Bir yerdeki düzeltme
  başka bir yeri bozabilir (gerileme, regression).

## Özet

- Değerlendirme kümesi doğru cevabı bilinen girdilerdir; her prompt
  sürümü aynı kümede puanlanır.
- Biçim, ayrıştırılabilirlik ve doğruluk ayrı ölçülür.
- Hataları türlerine ayır; neyin düzeltileceğini toplam puan değil hata
  türleri söyler.
- Küçük kümede fark rastlantı olabilir: sürümlerin farklı cevap verdiği
  mesajlara ve yeniden örneklemeyle aralığa bak.
- Bir modelin başka modeli puanlaması hızlıdır ama önce insan
  etiketleriyle karşılaştırılır.
- Kümeyi büyüt, geliştirme ve test kümesini ayır, her değişiklikte
  yeniden çalıştır.
