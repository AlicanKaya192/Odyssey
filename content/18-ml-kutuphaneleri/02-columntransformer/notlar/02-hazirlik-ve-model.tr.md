`ColumnTransformer` asıl gücünü bir modelle **tek nesnede** birleşince
gösterir: ham DataFrame girer, tahmin çıkar. Doldurma, kodlama ve model aynı
`fit` ile öğrenilir; yeni veride eksik değer ya da bilinmeyen şehir olsa da
çalışır.

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

rng = np.random.default_rng(5)
n = 200
homes = pd.DataFrame({"size": rng.uniform(50, 200, n).round(),
                      "city": rng.choice(["Izmir", "Ankara", "Bursa"], n)})
bonus = homes["city"].map({"Izmir": 300, "Ankara": 200, "Bursa": 100})
price = homes["size"] * 20 + bonus + rng.normal(0, 50, n)
homes.loc[homes.sample(10, random_state=5).index, "size"] = np.nan
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["size"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
model = make_pipeline(prep, LinearRegression()).fit(homes, price)
new = pd.DataFrame({"size": [100.0, np.nan], "city": ["Izmir", "Van"]})
print(model.predict(new).round(0).tolist())
print(round(model.score(homes, price), 3))
print(model[0].named_transformers_["num"].statistics_.tolist())
```

```text
[2327.0, 2679.0]
0.953
[122.5]
```

## Ne oldu?

- `make_pipeline(prep, LinearRegression())` önce hazırlığı, sonra modeli
  uygular. Model ham `homes` tablosuyla eğitildi, ham `new` tablosuyla tahmin
  yaptı; arada elle hiçbir adım yok.
- İkinci yeni ev hem boyutu bilinmeyen hem görülmemiş bir şehirde (Van). Boyut
  eğitimdeki medyanla (122,5) dolduruldu; şehir sütunlarının hepsi 0 oldu.
  Hata yok, ama bu tahmin **varsayımlarla** yapıldı: Van için model hiçbir
  şehrin etkisini kullanmadı. Üretimde bu tür satırları saymak ve izlemek
  gerekir.
- `model[0]` ilk adımı (hazırlığı), `named_transformers_["num"]` onun
  parçasını verir; öğrenilen medyan oradan okunur.

## Neden tek nesne?

- Test ve üretim verisine **aynı** adımlar, aynı öğrenilmiş değerlerle
  uygulanır; birini unutmak mümkün değil.
- Çapraz doğrulamada hazırlık her katta yalnızca o katın eğitim verisiyle
  öğrenilir: sızıntı kendiliğinden önlenir (Pipeline bölümü).
- Kaydedilen tek dosya her şeyi taşır (Model Kaydetme bölümü).
