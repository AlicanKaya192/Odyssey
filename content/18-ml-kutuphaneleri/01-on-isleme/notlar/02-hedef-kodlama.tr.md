Çok fazla farklı değeri olan bir kategori (400 mağaza, binlerce ürün) için
one-hot yüzlerce sütun açar. Yaygın bir kısa yol: her kategoriyi **hedefin o
kategorideki ortalamasıyla** değiştirmek (hedef kodlama). Ama bu elle
yapılınca hedefi özelliğin içine sızdırır.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import TargetEncoder

rng = np.random.default_rng(4)
df = pd.DataFrame({"shop": rng.integers(0, 400, 2000).astype(str),
                   "bought": rng.integers(0, 2, 2000)})
train, test = train_test_split(df, test_size=0.5, random_state=4)
means = train.groupby("shop")["bought"].mean()
naive_train = train["shop"].map(means).to_frame()
naive_test = test["shop"].map(means).fillna(train["bought"].mean()).to_frame()
model = LogisticRegression().fit(naive_train, train["bought"])
print(round(model.score(naive_train, train["bought"]), 3),
      round(model.score(naive_test, test["bought"]), 3))
enc = TargetEncoder(random_state=4)
safe_train = enc.fit_transform(train[["shop"]], train["bought"])
safe_test = enc.transform(test[["shop"]])
model = LogisticRegression().fit(safe_train, train["bought"])
print(round(model.score(safe_train, train["bought"]), 3),
      round(model.score(safe_test, test["bought"]), 3))
```

```text
0.734 0.484
0.492 0.497
```

## Ne oldu?

- Veride **hiçbir ilişki yok**: mağaza ve satın alma birbirinden bağımsız
  rastgele üretildi. Gerçek başarı %50 civarında olmalı.
- Elle kodlama eğitimde **%73,4** doğruluk verdi, testte %48,4. Her mağazanın
  ortalaması, o mağazanın kendi satırlarının hedefinden hesaplandı; mağaza
  başına 2–3 satır olunca ortalama satırın kendi cevabını taşıyor. Model
  hedefi özelliğin içinden okudu.
- `TargetEncoder` eğitim verisinde **çapraz uydurma** (cross fitting) yapar:
  her satırın kodu, o satırın bulunmadığı katlardan hesaplanır. Eğitim
  skoru %49,2, yani dürüst: öğrenilecek bir şey yok ve model de bunu
  gösteriyor.
- Az kaydı olan kategorinin ortalaması güvenilmezdir; `TargetEncoder` onu
  genel ortalamaya doğru çeker (düzleştirme, `smooth`).

## Kural

Hedeften türetilen her özellik (hedef ortalaması, hedefe göre sıralama)
eğitim satırının **kendi** cevabını görmeden hesaplanmalı. Elle yapmak
yerine `TargetEncoder`; eğitimde `fit_transform`, testte `transform`.
