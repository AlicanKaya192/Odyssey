01'deki temizleme fonksiyonunu vektörleştiricinin içine koyabilirsin:
`TfidfVectorizer(preprocessor=clean)`. Böylece temizlik de Pipeline'ın
parçası olur ve modeli kullanırken unutulmaz. Kirli yorumlarda deneyelim:

```python
import html
import re
import unicodedata

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from text_data import messy_reviews

QUOTES = str.maketrans({chr(0x2018): "'", chr(0x2019): "'",
                        chr(0x201C): '"', chr(0x201D): '"'})


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(QUOTES).replace(chr(0x200B), "")
    return " ".join(text.split()).lower()


reviews = messy_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
for preprocessor in [None, clean]:
    pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=preprocessor)),
                     ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
    size = len(pipe.named_steps["tfidf"].vocabulary_)
    print(preprocessor is not None, round(pipe.score(X_test, y_test), 3), size)
print(TfidfVectorizer().build_analyzer()(texts[3])[:6])
```

```text
False 0.88 328
True 0.878 326
['it', 'does', 'the', 'job', 'br', 'much']
```

- Temizlik doğruluğu değiştirmedi (%88,0'a %87,8). scikit-learn'ün
  parçalayıcısı `\w\w+` aradığı için bölünmez boşluk, sıfır genişlikli boşluk
  ve tırnaklar zaten kelimeleri bölüyor. 01'deki temizlik `split(" ")` ile
  parçalarken kritikti; bu parçalayıcıda değil.
- Ama son satıra bak: temizlik olmadan `<br>` etiketi "br" diye bir kelime
  oldu. Dağarcık kirli; başka bir veride (çok HTML'li sayfalar) bu kelimeler
  modeli yanıltabilir. Temizliği doğrulukla değil, **dağarcığa bakarak** da
  değerlendir.

## preprocessor, tokenizer, analyzer

| Parametre | Ne zaman çalışır | Not |
|---|---|---|
| `preprocessor` | Parçalamadan önce, bütün metne | Verince varsayılan küçük harf **yapılmaz**; fonksiyonun kendisi yapmalı |
| `tokenizer` | Metni token listesine çevirir | 02'deki `TOKEN.findall` gibi; `token_pattern=None` ver ki uyarı çıkmasın |
| `analyzer` | Bütün işi tek fonksiyonla | Ön işleme, parçalama ve n-gram'ların hepsini sen yaparsın |

Kendi fonksiyonlarını kullanan bir Pipeline'ı kaydedersen, yüklerken o
fonksiyonların aynı adla içe aktarılabilir olması gerekir; fonksiyonu bir
modülde tut.
