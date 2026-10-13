Dağarcık eğitim verisinden öğrenilir. Test verisindeki kelimelerin ne kadarı
o dağarcıkta yok? Aynı türden metinde ve başka türden metinde ölçelim:

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews, make_tickets

reviews = [r["text"] for r in make_reviews(2000)]
tickets = [t["text"] for t in make_tickets(500)]
vectorizer = CountVectorizer().fit(reviews[:1000])
analyze = vectorizer.build_analyzer()


def oov_share(texts):
    tokens = [w for t in texts for w in analyze(t)]
    unseen = sum(w not in vectorizer.vocabulary_ for w in tokens)
    return round(unseen / len(tokens), 3)


print(oov_share(reviews[1000:]), oov_share(tickets))
```

```text
0.005 0.633
```

- İlk 1000 yorumla kurulan dağarcık, sonraki 1000 yorumun kelimelerinin
  %99,5'ini tanıyor: aynı türden metin, aynı kelimeler.
- Aynı dağarcık destek taleplerinin kelimelerinin **%63'ünü tanımıyor**.
  "refund", "invoice", "password" yorumlarda hiç geçmedi; model bunları
  sessizce atacak.

## Ne anlama geliyor?

Bir model yalnızca eğitimde gördüğü kelimelerle karar verir. Ürün yorumlarıyla
eğitilmiş bir sınıflandırıcıyı destek taleplerine uygularsan, talebin
çoğunu hiç görmeden karar verir; doğruluğu ölçmeden "çalışıyor" sanabilirsin.
Bu duruma **alan kayması** (domain shift) denir.

Kontrol listesi:

- Modeli kullanacağın metne benzeyen veriyle eğit.
- Yeni veride dağarcık dışı payını ölç. Birdenbire artarsa (yeni ürün,
  yeni sezon, yeni argo) model eskimiş demektir.
- Dağarcık dışı kelimeye dayanıklı yöntemler: harf n-gram'ları (04), alt
  kelime parçalama (ikinci modül).
