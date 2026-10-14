# Halüsinasyon ve Güvenilirlik

06. bölümde oyuncak model, hiç görmediği bir ülkenin başkenti sorulunca
"the capital of canada is ottawa" dedi: kendinden emin, dilbilgisi
kusursuz ve yanlış. Bir dil modelinin dayanağı olmayan bir içeriği akıcı
biçimde üretmesine **halüsinasyon** (hallucination) denir. Bu bölüm iki
soruyu ele alıyor: neden olur ve bir program bunu nasıl **yakalar**.

## Neden olur?

- **Hedef doğruluk değil, akıcılık.** Model eğitimde sıradaki token'ı
  tahmin etmeyi öğrenir. "Metne benzeyen bir devam" ile "doğru bir devam"
  çoğu zaman aynıdır ama her zaman değil.
- **Bilgi boşlukları.** Verisinde olmayan ya da az geçen bir konuda model
  yine bir şey üretir; "bilmiyorum" demek de öğrenilmesi gereken bir
  davranıştır.
- **Verilen metne sadakatsizlik.** Model önüne konan belgeyi özetlerken ya
  da ondan cevap verirken belgede olmayan bir ayrıntı ekleyebilir. Buna
  **kaynağa sadakatsizlik** (unfaithfulness) da denir.

Halüsinasyonu tamamen önleyen bir ayar yok; ama programın tarafında üç
şey yapılabilir: modelin emin olmadığını **ölçmek**, cevabı bir **kaynağa
karşı denetlemek** ve emin olunamayan yerde **cevap vermemek**.

## Tutarlılıkla ölçmek

06'daki oyuncak model alıştırmalarda kullanılmak üzere `tiny_chat.py`
dosyasında duruyor. Aynı soruyu sıcaklık 1 ile 20 kez soralım ve en sık
cevabın payına bakalım:

```python
from collections import Counter
from tiny_chat import ask, CAPITALS


def consistency(country, n=20):
    answers = Counter(ask(country, temperature=1.0, seed=s)[0]
                      for s in range(n))
    answer, count = answers.most_common(1)[0]
    return answer, count / n


for c in ["france", "peru", "turkey", "chile"]:
    answer, share = consistency(c)
    print(c, share, answer)
```

```text
france 1.0 the capital of france is paris .
peru 1.0 the capital of peru is lima .
turkey 0.35 the capital of canada is ottawa .
chile 0.35 the capital of canada is ottawa .
```

Bildiği ülkelerde 20 cevabın 20'si aynı. Bilmediği ülkelerde en sık cevap
bile denemelerin yalnızca %35'i: model her seferinde başka
bir şey söylüyor. Buna **öz tutarlılık** (self-consistency) denetimi
denir: bir modelin bildiği konuda cevapları birbirini tutar, bilmediği
konuda dağılır.

## Emin değilsen cevap verme

Tutarlılığı bir kapıya çevirelim: en sık cevabın payı 0,6'nın altındaysa
"emin değilim" de. Sözlükteki on iki ülkenin hepsinde deneyelim ve
cevapları gerçek başkentle karşılaştıralım:

```python
def gated(country, threshold=0.6):
    answer, share = consistency(country)
    return answer if share >= threshold else None


correct = wrong = abstained = 0
for country, capital in CAPITALS.items():
    answer = gated(country)
    if answer is None:
        abstained += 1
    elif answer.split()[5] == capital:
        correct += 1
    else:
        wrong += 1
print("correct", correct, "wrong", wrong, "abstained", abstained)
print("without the gate, wrong:",
      sum(ask(c)[0].split()[5] != cap for c, cap in CAPITALS.items()))
```

```text
correct 10 wrong 0 abstained 2
without the gate, wrong: 2
```

Kapı olmadan model on iki sorunun ikisinde yanlış cevap veriyordu; kapıyla
yanlış cevap kalmıyor ve bu iki soruda "emin değilim" deniyor. Bedeli
çağrı sayısı: her soru için 20 çağrı. Oyuncak modelde ayrım bu kadar
keskin çünkü bildiği her şeyi tek bir biçimde biliyor; gerçek modellerde
cevaplar bildiği konularda da biraz değişir, eşik verilerle ayarlanır ve
tutarlı ama yanlış cevaplar da olabilir. Tutarlılık bir **işarettir**,
kanıt değildir.

## Cevabı kaynağa karşı denetlemek

Modele bir belge verip ondan cevap istendiğinde daha güçlü bir denetim
mümkün: cevaptaki ayrıntılar belgede geçiyor mu? Bir mağazanın iade
politikasını kaynak olarak alalım. Aşağıdaki on iki cevap **örnek**: elle
yazdık ve hangilerinin politikaya sadık olduğunu biliyoruz (`True` sadık,
`False` uydurma ayrıntı içeriyor).

```python
import re

POLICY = ("Orders over 50 euros ship for free. Standard delivery takes "
          "3 to 5 working days. Returns are accepted within 30 days of "
          "delivery. Refunds are paid to the original card within 7 days. "
          "Customer service is open Monday to Friday, 9:00 to 17:00.")

EXAMPLES = [
    ("Shipping is free for orders over 50 euros.", True),
    ("Standard delivery takes 3 to 5 working days.", True),
    ("Standard delivery takes 1 to 2 working days.", False),
    ("Yes, within 30 days of delivery.", True),
    ("Yes, within 60 days of delivery.", False),
    ("The refund is paid to your original card within 7 days.", True),
    ("The refund is paid as store credit within 7 days.", False),
    ("Monday to Friday, from 9:00 to 17:00.", True),
    ("Every day from 9:00 to 17:00, including Sunday.", False),
    ("Yes, we ship to Canada in 10 days.", False),
    ("Yes, if your order is over 50 euros.", True),
    ("The policy does not say; please ask customer service.", True),
]
DETAIL = re.compile(r"\d+(?::\d+)?|[A-Z][a-z]+")


def details(text):
    found = DETAIL.findall(text)
    first = text.split()[0].strip(",.")
    return [d for d in found if d != first]


def unsupported(answer, source):
    known = set(DETAIL.findall(source))
    return [d for d in details(answer) if d not in known]


for answer, faithful in EXAMPLES[:3] + EXAMPLES[8:10]:
    print(faithful, unsupported(answer, POLICY))
```

```text
True []
True []
False ['1', '2']
False ['Sunday']
False ['Canada', '10']
```

`details` cevaptaki sayıları, saatleri ve büyük harfle başlayan adları
topluyor (cümlenin ilk kelimesi hariç, o her zaman büyük harfle başlar).
`unsupported` bunlardan kaynakta geçmeyenleri listeliyor. Uydurma bir
süre ("1 to 2"), bir gün ("Sunday") ya da bir ülke ("Canada") yakalanıyor.

## Denetçi ne kadar iyi?

Denetçiyi, cevabında desteksiz ayrıntı bulduğu her örneği "uydurma" diye
işaretleyen bir sınıflandırıcı gibi ölçelim:

```python
tp = fp = fn = tn = 0
for answer, faithful in EXAMPLES:
    flagged = bool(unsupported(answer, POLICY))
    if flagged and not faithful:
        tp += 1
    elif flagged:
        fp += 1
    elif not faithful:
        fn += 1
        print("missed:", answer)
    else:
        tn += 1
print("tp", tp, "fp", fp, "fn", fn, "tn", tn)
```

```text
missed: The refund is paid as store credit within 7 days.
tp 4 fp 0 fn 1 tn 7
```

Beş uydurmanın dördü yakalandı ve sadık cevapların hiçbiri yanlışlıkla
işaretlenmedi. Kaçan cevap öğretici: "store credit" (mağaza puanı)
politikada yok ama ne sayı ne de büyük harfli bir ad; denetçinin
baktığı yerin dışında. Basit kurallar en sık uydurmaları (sayılar,
tarihler, adlar) ucuza yakalar ama anlamı denetlemez. Bu örnekler bizim
yazdığımız on iki cümle; gerçek bir uygulamada denetçi, gerçek cevaplar
üzerinde etiketlenmiş bir örneklemle ölçülür.

## Pratikte

- **Kaynak ver:** modele cevabı dayandıracağı belgeyi vermek (RAG, sonraki
  bölümler) bilgi boşluğunu kapatır ve denetimi mümkün kılar.
- **Kaynak göster:** cevabın her iddiasının hangi parçadan geldiğini
  yazdırmak (kaynak numarası) denetimi kolaylaştırır; numaranın gerçekten
  o parçayı gösterdiği ayrıca denetlenir.
- **Çekimser kalabilmek:** sistem mesajında "kaynakta yoksa bilmediğini
  söyle" demek ve programda emin olunamayan cevabı göstermemek.
- **Ölç:** halüsinasyon oranı, etiketlenmiş örnekler üzerinde ölçülen bir
  sayıdır; bir ayar değişince yeniden ölçülür.

## Özet

- Halüsinasyon: dayanağı olmayan içeriği akıcı biçimde üretmek. Hedefin
  doğruluk değil akıcılık olması ve bilgi boşlukları başlıca nedenler.
- Öz tutarlılık: aynı soruyu birkaç kez sorup cevapların ne kadar
  örtüştüğüne bakmak. Oyuncak modelde bildiği konularda pay 1,0, bilmediği
  konularda %35.
- Eşikle çekimser kalmak, oyuncak modelde yanlış cevapları sıfırladı;
  bedeli soru başına 20 çağrı.
- Kaynak denetimi: cevaptaki sayı ve adlar kaynakta geçiyor mu? On iki
  örnekte beş uydurmanın dördü yakalandı; anlamı değişen ama ayrıntısı
  olmayan cevap kaçtı.
- Hiçbir denetim tek başına yeterli değil; denetçiler de ölçülür.
