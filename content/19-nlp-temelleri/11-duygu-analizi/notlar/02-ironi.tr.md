Derste model ironi içeren 17 yorumun hepsini bildi. Ama o yorumlar üç sabit
kalıptan geliyordu ("Great, the ... broke on day ..."). Modeli bütün
yorumlarla eğitip **yeni** ironi cümleleri verelim:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_reviews

reviews = make_reviews(2000)
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())])
pipe.fit([r["text"] for r in reviews], [r["label"] for r in reviews])
new = ["Oh great, another broken zipper.", "Perfect, it died in a week.",
       "Lovely, the strap snapped on the first run.",
       "Thanks a lot, the lid leaks."]
for text, label in zip(new, pipe.predict(new)):
    print(label, "|", text)
```

```text
positive | Oh great, another broken zipper.
positive | Perfect, it died in a week.
positive | Lovely, the strap snapped on the first run.
positive | Thanks a lot, the lid leaks.
```

- Dördünü de olumlu buldu. Model ironiyi değil, eğitimdeki kalıpları
  öğrenmişti. Bu cümlelerdeki olumsuz kelimeleri ("broken", "died",
  "snapped", "leaks") eğitimde hiç görmedi; geriye "great", "perfect" gibi
  olumlu kelimeler kaldı.
- Dersteki sözlük de başaramıyor: dört cümleye `[1, 1, 0, 0]` puan
  veriyor. "great" ve "perfect" sözlükte olumlu, olumsuz olaylar ise sözlükte
  yok.

## İroni neden zor?

- **Kelimeler tersini söylüyor.** "Perfect" kelimesi olumlu; olumsuzluk
  cümlenin anlattığı olayda ("died in a week").
- **Dünya bilgisi gerekiyor.** Bir fermuarın bozulmaması gerektiğini, bir
  saatin bir haftada ölmemesi gerektiğini bilmek gerekiyor.
- **İpuçları zayıf ve kalıba bağlı.** "Oh great," ile başlamak, olumlu bir
  kelimenin arkasından olumsuz bir olay gelmesi, çok sayıda ünlem. Bunlar
  her zaman ironi değildir.

İroni ve alay tespiti hâlâ açık bir araştırma konusu; çok büyük dil
modelleri bile bağlam olmadan yanılır. Pratikte yapılan: ironinin sık olduğu
alanlarda (sosyal medya) daha çok ve daha çeşitli etiketli örnek toplamak, ve
bir duygu sisteminin sonucunu tek tek kararlar için değil **toplam
eğilimler** için kullanmak.
