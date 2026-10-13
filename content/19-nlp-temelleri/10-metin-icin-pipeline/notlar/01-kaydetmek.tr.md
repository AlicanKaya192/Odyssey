Bir metin modelini kullanmak için iki şey gerekir: vektörleştirici (dağarcık,
IDF) ve model (ağırlıklar). Pipeline ikisini tek nesnede tuttuğu için tek
dosyaya kaydedilir.

```python
import os

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LogisticRegression(max_iter=1000))]).fit(texts, labels)
joblib.dump(pipe, "review_model.joblib")
print(round(os.path.getsize("review_model.joblib") / 1024), "KB")
loaded = joblib.load("review_model.joblib")
new = ["The battery died after two days.", "Totally worth the money."]
print(loaded.predict(new).tolist())
print(bool((loaded.predict(texts) == pipe.predict(texts)).all()))
```

```text
131 KB
['negative', 'positive']
True
```

- Dosya 131 KB: dağarcık, IDF değerleri ve her sınıfın ağırlıkları.
- Yüklenen Pipeline ham metni doğrudan alıyor ve bütün tahminleri
  kaydedilenle aynı.

## Dikkat edilecekler (ML Kütüphaneleri'nden)

- **Sürüm:** dosyayı kaydeden ve yükleyen scikit-learn sürümü aynı olmalı;
  farklıysa uyarı verir, sonuçlar değişebilir.
- **Güvenlik:** `joblib.load` dosyanın içindeki kodu çalıştırabilir. Yalnızca
  kendi kaydettiğin ya da güvendiğin dosyaları yükle.
- **Son model:** son modeli bütün eğitim verisiyle (gerekirse
  test dahil, ölçüm bittikten sonra) yeniden eğitip kaydet; ölçümü daha önce
  ayrı bir test kümesinde yapmış olmalısın.
