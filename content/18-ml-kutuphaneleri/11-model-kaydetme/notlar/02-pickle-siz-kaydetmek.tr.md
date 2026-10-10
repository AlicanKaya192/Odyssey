Doğrusal bir model yalnızca birkaç sayıdan ibarettir: ölçekleyicinin
ortalamaları ve sapmaları, katsayılar ve sabit terim. Bunları düz bir JSON
dosyasına yazmak `pickle`'ın iki sorununu birden ortadan kaldırır: dosya kod
çalıştıramaz ve scikit-learn sürümüne bağlı değildir.

```python
import json
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=4, n_informative=3,
                           n_redundant=0, random_state=2)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
scaler, clf = model[0], model[-1]
params = {"mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist(),
          "coef": clf.coef_[0].tolist(), "intercept": float(clf.intercept_[0])}
text = json.dumps(params)
print(len(text))
p = json.loads(text)
z = (X - np.array(p["mean"])) / np.array(p["scale"])
proba = 1 / (1 + np.exp(-(z @ np.array(p["coef"]) + p["intercept"])))
print(bool(np.allclose(proba, model.predict_proba(X)[:, 1])))
```

```text
313
True
```

## Ne görüyoruz

- Modelin tamamı birkaç yüz karakterlik bir metin.
- Tahmini NumPy ile kendimiz hesapladık: ölçekle, katsayılarla çarp, sabiti
  ekle, sigmoid. Sonuç scikit-learn'ün `predict_proba`'sıyla aynı.
- Bu dosya her dilde okunabilir; scikit-learn'ü kurmadan da tahmin
  yapılabilir.

## Sınırı

- Yalnızca formülü basit modellerde pratik (doğrusal, lojistik). Bir ormanı
  elle yazmak binlerce düğüm demek.
- Karmaşık modeller için dile bağımsız biçimler var (ONNX gibi); ek paket
  gerektirdikleri için burada anlatılmadı.
