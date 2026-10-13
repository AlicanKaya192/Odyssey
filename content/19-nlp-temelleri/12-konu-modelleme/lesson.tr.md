# Konu Modelleme

Elinde etiketsiz binlerce destek talebi var ve "insanlar en çok ne hakkında
yazıyor?" diye soruyorsun. **Konu modelleme** (topic modelling) belgelerde
birlikte geçen kelime gruplarını bulur: her grup bir **konu**, her belge bu
konuların bir karışımı. Etiket gerekmez; bu bir denetimsiz öğrenme
yöntemi. Bu bölümde iki yaygın yöntemi, NMF ve LDA'yı, talepler üzerinde
deneyeceğiz. Taleplerin gerçek kategorilerini biliyoruz ama modele
vermeyeceğiz; yalnızca sonunda bulunan konuların kategorilerle ne kadar
örtüştüğüne bakacağız.

## NMF ile konular

**NMF** (non-negative matrix factorization, negatif olmayan matris
ayrıştırması) belge-kelime matrisini iki küçük matrisin çarpımına ayırır:
belge-konu (`W`) ve konu-kelime (`H`). İkisi de negatif değil, o yüzden bir
belge konuların **toplamı** olarak okunabilir.

```python
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
categories = np.array([t["category"] for t in tickets])
EXTRA_STOP = {"ord", "com", "example", "hi", "hello", "thanks", "thank",
              "dear", "support", "regards", "help"}
tfidf = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS | EXTRA_STOP),
                        token_pattern=r"[a-z]{2,}", min_df=5)
X = tfidf.fit_transform(texts)
words = tfidf.get_feature_names_out()


def show_topics(components, k=6):
    for i, row in enumerate(components):
        print(i, " ".join(words[row.argsort()[::-1][:k]]))


nmf = NMF(n_components=5, random_state=0, max_iter=500)
W = nmf.fit_transform(X)
print(X.shape, W.shape, nmf.components_.shape)
show_topics(nmf.components_)
```

```text
(2000, 142) (2000, 5) (5, 142)
0 does number card order work long
1 account email address change access locked
2 app page error time crashes screen
3 arrived box parcel damaged open order
4 delivered got says order address wrong
```

- Ön işleme konu modellemede kritik. İngilizce durak kelimelerin yanına bu
  veriye özgü olanları ekledik: "ord" (sipariş numaraları `ORD-12345`),
  "com" ve "example" (e-posta adresleri), selamlaşmalar. `token_pattern`
  yalnızca harfleri alıyor, sayılar dışarıda. Durak kelimeler olmadan ne
  olduğunu ilk notta görüyoruz.
- `W` 2000 × 5: her talebin her konudaki ağırlığı. `H` (`components_`)
  5 × 142: her konunun her kelimedeki ağırlığı. Bir konuyu en ağır
  kelimelerine bakarak **sen** adlandırırsın; model ad vermez.
- Konular okunuyor: 1 hesap, 2 uygulama hataları, 3 hasarlı paket, 4 yanlış
  yere teslim. 0 ise karışık: "number card order work long".

## Konular kategorilerle örtüşüyor mu?

Her talebe en ağır konusunu verip gerçek kategorilerle çapraz tablo
kuralım. **Saflık** (purity): her konunun en kalabalık kategorisini doğru
sayınca doğru düşen talep oranı.

```python
topic = W.argmax(axis=1)


def purity(topic):
    table = pd.crosstab(pd.Series(topic, name="topic"),
                        pd.Series(categories, name="category"))
    print(table)
    return round(table.max(axis=1).sum() / len(categories), 3)


print(purity(topic))
```

```text
category  account  billing  refund  shipping  technical
topic                                                  
0              16       53     113       143         40
1             376      150      22        14         11
2              13       43      18         9        438
3               3        2      23       165          0
4               2       70       8       262          6
0.692
```

- Hesap (1) ve uygulama (2) konuları kategorilerle iyi örtüşüyor.
- Kargo iki konuya bölündü: hasarlı paketler (3) ve yanlış teslimat (4).
- **Fatura ve iade kendi konularını bulamadı.** İkisi aynı kelimeleri
  kullanıyor ("card", "charged", "money", "order"); fatura talepleri hesap
  konusuna (150), iade talepleri karışık konuya (113) dağıldı.
- Ders: konu modeli **senin kategorilerini** değil, **birlikte geçen
  kelimeleri** bulur. Kategoriler bir iş kararıdır (fatura ekibi, iade
  ekibi); kelimeler bunu bilmez.

## Konu sayısı

Konu sayısını sen seçersin. 8 konu deneyelim:

```python
nmf8 = NMF(n_components=8, random_state=0, max_iter=500)
W8 = nmf8.fit_transform(X)
show_topics(nmf8.components_)
print(purity(W8.argmax(axis=1)))
```

```text
0 change address delivery order email account
1 account access locked attempts data delete
2 app page error time crashes order
3 arrived box parcel damaged open order
4 delivered got says order wrong package
5 card paid credit refund charged did
6 update working push notifications stopped phone
7 does number work tracking long shipping
category  account  billing  refund  shipping  technical
topic                                                  
0              16        1       3        54          1
1             334      101      13         6         14
2               9       28       3         2        253
3               3        2       6       164          0
4               2       17       3       171          6
5              32      144     150        28         27
6               5       22       1         3        152
7               9        3       5       165         42
0.722
```

- Daha çok konu daha ince ayrım: kargo dört konuya bölündü (adres
  değişikliği, hasar, yanlış teslimat, takip numarası), uygulama hataları
  ikiye (çökme, bildirimler).
- Fatura ve iade yine **tek bir para konusunda** (5) birleşti: 144 fatura,
  150 iade. Konu sayısını artırmak onları ayırmadı.
- Saflık biraz arttı, ama saflık konu sayısıyla zaten artar: her belgeye ayrı
  konu verilse saflık 1 olur. Konu sayısını saflığa bakarak seçme; konuların
  okunur ve işe yarar olup olmadığına bak.

## LDA

**LDA** (latent Dirichlet allocation) olasılık modeli: her belgenin bir konu
dağılımı, her konunun bir kelime dağılımı olduğunu varsayar ve belgeyi
yazan bir süreç kurar. TF-IDF değil, ham **sayımlar** ister.

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

counter = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS | EXTRA_STOP),
                          token_pattern=r"[a-z]{2,}", min_df=5)
C = counter.fit_transform(texts)
words = counter.get_feature_names_out()
lda = LatentDirichletAllocation(n_components=5, random_state=0)
D = lda.fit_transform(C)
show_topics(lda.components_)
print(purity(D.argmax(axis=1)))
print(D[1].round(2).tolist(), categories[1])
```

```text
0 account log error login shows screen
1 address account change email order number
2 arrived long does shipping damaged box
3 app time order happens second page
4 order card paid refund credit got
category  account  billing  refund  shipping  technical
topic                                                  
0             155       91      14        11        174
1             178       47       5       210         80
2               5        1      18       230          2
3              54       11       8        16        221
4              18      168     139       126         18
0.501
[0.34, 0.02, 0.02, 0.59, 0.02] account
```

- LDA'nın konuları bu veride daha bulanık ve saflık daha düşük (0,501'e
  0,692). LDA kelime sayımlarından olasılık tahmin eder; kısa metinlerde
  (bir iki cümlelik talepler) sayımlar azdır ve tahmin zayıflar. NMF kısa
  metinlerde çoğu zaman daha okunur konular verir.
- `D`'nin her satırı toplamı 1 olan bir dağılım: bir talebin hangi
  konulardan ne kadar oluştuğu. LDA'nın asıl gücü bu: uzun belgelerde
  (makaleler, kitaplar) "bu belge %60 ekonomi, %40 siyaset" diyebilmek.
- Son satır kısa metnin sorununu gösteriyor: "I cannot log in to my
  acconut... reset the password" talebinin yalnızca %34'ü hesap konusunda
  (0), %59'u konu 3'te. "account" yazım hatalı ve birkaç kelime bütün
  dağılımı belirliyor.

## Yeni bir belge

Eğitilmiş bir konu modeli yeni belgeye konu ağırlıkları verir:

```python
new = ["My parcel arrived damaged and the box was open.",
       "I was charged twice, please refund the extra money."]
for weights in nmf.transform(tfidf.transform(new)):
    print(weights.round(2).tolist())
```

```text
[0.0, 0.0, 0.0, 0.36, 0.0]
[0.03, 0.03, 0.0, 0.0, 0.0]
```

İlk talep neredeyse yalnızca hasar konusunda (3). İkincinin ağırlığı
konulara dağılmış ve küçük: "charged", "refund", "money" beş konunun
hiçbirine tam oturmuyor, çünkü model para konusunu ayrı bulamamıştı. Konu
modeli görmediği bir ayrımı yeni belgede de yapamaz.

## Özet

- Konu modelleme etiketsiz belgelerde birlikte geçen kelime gruplarını
  bulur. Konuları en ağır kelimelerine bakarak sen adlandırırsın.
- NMF TF-IDF matrisini belge-konu ve konu-kelime matrislerine ayırır; kısa
  metinlerde çoğu zaman LDA'dan okunur.
- LDA ham sayımlarla çalışan bir olasılık modelidir; her belgeye bir konu
  dağılımı verir, uzun belgelerde güçlüdür.
- Konular senin kategorilerin değildir: aynı kelimeleri kullanan fatura ve
  iade ayrılmadı. Konu sayısını okunurluğa ve işe yararlığa bakarak seç.
- Ön işleme (durak kelimeler, sayılar) konuların kalitesini belirler.
