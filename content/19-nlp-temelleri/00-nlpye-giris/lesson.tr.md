# NLP'ye Giriş

Şimdiye kadar çalıştığın verilerin çoğu tabloydu: her satır bir örnek, her
sütun bir sayı ya da kategori. Oysa dünyadaki verinin büyük kısmı **metin**:
ürün yorumları, destek talepleri, e-postalar, haberler, sözleşmeler, sohbet
kayıtları. **Doğal Dil İşleme** (Natural Language Processing, kısaca **NLP**)
bilgisayarın bu metinlerle çalışmasını sağlayan yöntemlerin adı. Bu bölüm
metnin neden zor bir veri olduğunu, NLP'nin hangi soruları cevapladığını ve
patika boyunca kullanacağımız veriyi tanıtıyor; sonunda kendi yazdığımız
basit bir kuralın ne kadar kötü çalıştığını ölçüp bu patikanın neden var
olduğunu göreceğiz.

## Metin neden zor bir veri?

Bir tabloda "fiyat" sütunu sayıdır; 49,99'u 59,99 ile karşılaştırmak kolaydır.
Metinde böyle hazır sütunlar yok. Bir yorumun olumlu mu olumsuz mu olduğu
hiçbir sütunda yazmıyor; kelimelerin içine gömülü. Üstelik:

- **Aynı anlam, farklı yazım.** "Harika", "çok iyi", "bayıldım" aynı şeyi
  söylüyor ama ortak tek harfleri yok.
- **Aynı yazım, farklı anlam.** İngilizcede *bank* hem banka hem nehir kıyısı;
  Türkçede "yüz" hem sayı hem surat. Anlamı **bağlam** (çevresindeki kelimeler)
  belirliyor.
- **Olumsuzlama.** "Kötü değil" olumlu bir cümle, ama içinde "kötü" geçiyor.
- **Alay.** "Harika, ikinci gün bozuldu." Olumlu bir kelimeyle olumsuz bir
  şey söyleniyor.
- **Yazım hataları ve biçim.** "güzle", "GÜZEL!!!", "güzel." üçü de aynı
  kelime olmalı ama bilgisayar için üç ayrı dize (string).
- **Dilin kendisi.** Türkçe **sondan eklemeli** bir dil: "evlerimizden" tek
  kelime ama içinde "ev", çoğul, iyelik ve ayrılma eki var. İngilizcede bu
  dört kelimeyle söylenir ("from our houses").

Bilgisayar ise yalnızca sayılarla hesap yapabiliyor. NLP'nin temel işi bu
yüzden şu: **metni, anlamını olabildiğince koruyarak sayılara çevirmek** ve o
sayılarla karar vermek.

<figure class="fig">
  <div class="flow">
    <span class="node acc">Metin<br><code>"Not bad!"</code></span>
    <span class="arrow">→</span>
    <span class="node">Temizle</span>
    <span class="arrow">→</span>
    <span class="node">Parçala</span>
    <span class="arrow">→</span>
    <span class="node">Sayıya çevir</span>
    <span class="arrow">→</span>
    <span class="node ok">Model<br><b>olumlu</b></span>
  </div>
  <figcaption>Hemen her NLP sistemi bu adımlardan geçer; patika her birini sırayla anlatıyor.</figcaption>
</figure>

## NLP hangi soruları cevaplar?

| Görev | Soru | Örnek | Patikada |
|---|---|---|---|
| Sınıflandırma | Bu metin hangi gruba ait? | Yorum olumlu mu, talep hangi birime gitmeli? | NLP Temelleri 08–11 |
| Arama | Bu soruya en yakın belge hangisi? | Yardım makaleleri içinde arama | NLP Temelleri 07 |
| Bilgi çıkarma | Metnin içinde hangi tarih, tutar, sipariş var? | "ORD-48213" numarasını bulmak | NLP Temelleri 14 |
| Konu bulma | Bu binlerce metin hangi konulardan bahsediyor? | Taleplerin ana başlıkları | NLP Temelleri 12–13 |
| Etiketleme | Her kelimenin görevi ne? | İsim mi, fiil mi? | Gömmeler ve Dil Modelleri 07 |
| Dil modelleme | Sıradaki kelime ne olabilir? | Otomatik tamamlama | Gömmeler ve Dil Modelleri 06, 13 |

Çeviri, özetleme ve soru cevaplama gibi görevler de bu temellerin üstüne
kurulur; ikinci modülün sonunda büyük dil modellerinin bunları nasıl
yaptığını kavramsal olarak göreceğiz.

## İki yaklaşım: kurallar ve öğrenme

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>KURAL TABANLI</h5>
<pre><code>if "refund" in text:
    team = "refunds"</code></pre>
      <p>Uzman yazar. Okunur, ama her yeni ifade için yeni kural gerekir.</p>
    </div>
    <div class="ok">
      <h5>ÖĞRENEN</h5>
<pre><code>model.fit(texts, labels)
model.predict(new_texts)</code></pre>
      <p>Etiketli örneklerden öğrenir. Veri ister, benzer ifadeleri kendisi yakalar.</p>
    </div>
  </div>
  <figcaption>İki yaklaşım rakip değil: biçimi kesin bilgide kural, anlam ve tonda öğrenen model.</figcaption>
</figure>

İlk NLP sistemleri **kural tabanlıydı** (rule-based): bir uzman "içinde
*iade* geçen talep iade birimine gider" gibi kuralları elle yazıyordu.
Kurallar anlaşılır ve hızlıdır, ama dil o kadar çeşitli ki kural listesi
hiçbir zaman bitmez. Bugünkü sistemlerin çoğu **öğrenen** sistemler:
kuralları elle yazmak yerine **etiketli örneklerden** (metin + doğru cevap)
bir model eğitiyoruz. Bu patikada ikisini de yazacağız; bu bölümün sonunda
kuralların neden yetmediğini sayılarla göreceğiz.

## Veri setimiz

Patika boyunca kullanacağımız metinler `text_data.py` dosyasında. Bu dosya
internetten veri indirmiyor; ürün yorumlarını ve destek taleplerini **sabit
bir tohumla** (seed) üretiyor. Yani senin bilgisayarında da benimkinde de
aynı metinler çıkıyor ve dersteki sayılar seninkilerle birebir tutuyor.
Metinler İngilizce: gerçek projelerde de verinin çoğu İngilizce, ve alıştırma
kodunda Türkçe harf gerekmiyor. Türkçeye özgü sorunları ayrı başlıklarda
göreceğiz.

```python
from collections import Counter
from text_data import make_reviews

reviews = make_reviews(2000)
print(len(reviews))
for key, value in reviews[0].items():
    print(key, "=", value)
print(Counter(r["label"] for r in reviews))
```

```text
2000
id = 1
product = sports watch
text = Not bad for the price. The weight is not fragile at all.
rating = 5
label = positive
Counter({'positive': 1318, 'negative': 393, 'neutral': 289})
```

- `make_reviews(2000)` 2000 yorum veriyor; her biri bir sözlük (dictionary):
  `id`, `product` (ürün), `text` (yorumun kendisi), `rating` (1–5 yıldız) ve
  `label` (etiket).
- Etiket yıldızdan geliyor: 4–5 yıldız `positive` (olumlu), 3 yıldız
  `neutral` (nötr), 1–2 yıldız `negative` (olumsuz).
- Dağılım **dengesiz** (imbalanced): yorumların 1318'i olumlu, yalnızca
  289'u nötr. Gerçek mağazalarda da insanlar çoğunlukla memnun olduklarında
  yorum yazar.
- İlk yoruma dikkat et: "Not bad for the price" (fiyatına göre fena değil).
  İçinde *bad* geçiyor ama etiketi olumlu. Bu cümleye birazdan döneceğiz.

`make_tickets` da aynı şekilde destek talepleri üretiyor; onları ilerideki
bölümlerde kullanacağız.

## İlk keşif: uzunluklar ve kelimeler

Bir modele geçmeden önce veriye bakmak her zaman ilk iştir. İki basit soru:
yorumlar ne kadar uzun ve en sık hangi kelimeler geçiyor?

```python
from collections import Counter
from text_data import make_reviews

reviews = make_reviews(2000)
for label in ["positive", "neutral", "negative"]:
    lengths = [len(r["text"].split()) for r in reviews if r["label"] == label]
    print(label, round(sum(lengths) / len(lengths), 1), min(lengths), max(lengths))

words = Counter()
for r in reviews:
    for w in r["text"].lower().split():
        words[w.strip(".,!?")] += 1
print(len(words))
print(" ".join(f"{w}:{c}" for w, c in words.most_common(8)))
```

```text
positive 15.4 4 40
neutral 15.9 4 34
negative 16.1 3 38
360
the:3613 is:1717 i:902 for:663 it:602 not:601 my:592 but:492
```

- `text.split()` metni boşluklardan bölüyor; her parça kabaca bir kelime.
  Bu işin adı **tokenizasyon** (tokenisation, parçalara ayırma); 02. bölümde
  `split`'in neden yetmediğini göreceğiz.
- Yorumlar ortalama 15–16 kelime; uzunluk etiketi ele vermiyor.
- `lower()` büyük harfleri küçültüyor, `strip(".,!?")` kelimenin başındaki
  ve sonundaki noktalama işaretlerini atıyor. Böyle olmasa "Great", "great"
  ve "great!" üç ayrı kelime sayılırdı.
- En sık kelimeler "the", "is", "i", "for": anlam taşımayan, her metinde
  geçen kelimeler. Bunlara **durak kelimeleri** (stop words) deniyor;
  03. bölümün konusu.
- "not" 601 kez geçiyor. Olumsuzlama bu veride çok sık; kelime saymaya dayanan
  her yöntem bununla uğraşmak zorunda kalacak.

## İlk sınıflandırıcı: elle yazılmış kurallar

Şimdi yorumun etiketini tahmin eden en basit programı yazalım: olumlu
kelimeleri ve olumsuz kelimeleri say, hangisi fazlaysa o.

```python
from text_data import make_reviews

GOOD = {"good", "great", "excellent", "perfect",
        "love", "worth", "fantastic", "comfortable"}
BAD = {"bad", "terrible", "awful", "broke",
       "hate", "waste", "poor", "useless"}


def predict(text):
    words = [w.strip(".,!?") for w in text.lower().split()]
    score = sum(w in GOOD for w in words) - sum(w in BAD for w in words)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


reviews = make_reviews(2000)
hits = sum(predict(r["text"]) == r["label"] for r in reviews)
print(hits, len(reviews), round(hits / len(reviews), 3))
print(round(sum(r["label"] == "positive" for r in reviews) / len(reviews), 3))
```

```text
898 2000 0.449
0.659
```

- `sum(w in GOOD for w in words)` her kelime için `True`/`False` üretiyor;
  `sum` `True`'ları 1 sayıyor. Böylece kaç olumlu kelime geçtiğini buluyoruz.
- Kural 2000 yorumun 898'inde doğru: **doğruluk** (accuracy) %44,9.
- İkinci satır daha çarpıcı: hiçbir şeye bakmadan **her yoruma "olumlu"
  demek** %65,9 doğruluk veriyor. Elle yazdığımız kural, hiçbir şey yapmayan
  bu tahminden daha kötü.

Her zaman en sık sınıfı söyleyen bu tembel tahmine **taban çizgisi**
(baseline) deniyor. Bir modelin işe yarayıp yaramadığını anlamanın ilk yolu
onu taban çizgisiyle karşılaştırmak. Dengesiz veride taban çizgisi şaşırtıcı
derecede yüksek olabilir; %65,9'u geçmeyen bir model hiçbir şey öğrenmemiştir.

## Kurallar nerede yanılıyor?

```python
import textwrap

wrong = [r for r in reviews if predict(r["text"]) != r["label"]]
print(len(wrong))
for r in wrong[:5]:
    print(r["label"], "->", predict(r["text"]))
    print(textwrap.fill(r["text"], 60, initial_indent="  ", subsequent_indent="  "))
```

```text
1102
positive -> negative
  Not bad for the price. The weight is not fragile at all.
positive -> neutral
  It does the job. Much better tahn my old office chair.
negative -> neutral
  i would not buy this sports watch again.
positive -> neutral
  I lvoe the armrests. Much better than my old office chair.
  Exactly what I needed. My daughter loves it too. Exactly
  what I needed.
positive -> neutral
  Not flimsy for the price.
```

`textwrap.fill` uzun metni 60 karakterlik satırlara bölüp başına iki boşluk
koyuyor; yalnızca okunsun diye. Beş hatanın her biri farklı bir sorunu
gösteriyor:

1. **Olumsuzlama:** "Not bad" ve "not fragile" olumlu, ama kural *bad*
   kelimesini görüp olumsuz dedi.
2. **Listede olmayan kelime:** "It does the job", "Much better" olumlu
   ifadeler ama listemizde yok; skor 0 kaldı, kural nötr dedi.
3. **Fiil olarak olumsuzluk:** "would not buy" olumsuz, ama listedeki hiçbir
   kelimeyi içermiyor.
4. **Yazım hatası ve çekim:** "lvoe" ve "loves" listedeki "love" ile eşleşmedi.
5. **Liste eksik:** "Not flimsy" (çürük değil) olumlu, ama "flimsy" listede
   bile yok.

Listeye kelime ekleyerek bunların bir kısmını düzeltebilirsin, ama her
eklenen kelime yeni bir istisna doğurur ("not" eklersen "not worth"ü yakalarsın,
"not bad"i kaçırırsın). Bu patikanın geri kalanı bu soruna verilen
cevaplardan oluşuyor: metni düzgün temizlemek ve parçalamak, kelimeleri
sistemli biçimde sayılara çevirmek ve kuralları elle yazmak yerine **veriden
öğrenmek**. 09. bölümde aynı yorumlarda öğrenen bir modelin %90 dolaylarına
çıktığını göreceksin.

## Patikanın haritası

- **NLP Temelleri** (bu modül): metni temizleme, parçalama, sayıya çevirme
  (kelime torbası, TF-IDF), arama, sınıflandırma, duygu analizi, konu
  modelleme, bilgi çıkarma ve sonunda baştan sona bir destek talebi
  sınıflandırıcısı. Araçlar: Python, NumPy, scikit-learn.
- **Gömmeler ve Dil Modelleri**: kelimelerin anlamını yakalayan vektörler,
  alt kelime parçalama, sıradaki kelimeyi tahmin eden dil modelleri, dikkat
  mekanizması ve transformer. Hepsini NumPy ile sıfırdan, küçük örneklerle
  yazacağız.

## Özet

- NLP, metni anlamını koruyarak sayılara çevirip onlarla karar vermektir.
- Metin zordur: aynı anlam farklı yazılır, aynı yazım farklı anlama gelir,
  olumsuzlama ve alay kelime saymayı yanıltır.
- Her modeli önce **taban çizgisiyle** karşılaştır. Dengesiz veride hep
  çoğunluğu söylemek bile yüksek doğruluk verir.
- Elle yazılmış kurallar anlaşılırdır ama dilin çeşitliliğine yetişemez;
  bu veride %44,9 ile taban çizgisinin (%65,9) altında kaldı.
