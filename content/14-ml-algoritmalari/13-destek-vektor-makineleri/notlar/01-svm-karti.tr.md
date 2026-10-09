## Formüller

| Ne | Formül |
|---|---|
| Puan | `f(x) = w·x + b`, sınıf `sign(f(x))` |
| Menteşe kaybı | `max(0, 1 − y f(x))`, `y ∈ {−1, +1}` |
| Amaç | `λ/2 ‖w‖² + ort(menteşe)` ya da `½‖w‖² + C Σ menteşe` |
| Bağ | `C = 1 / (λ n)` |
| Marj genişliği | `2 / ‖w‖` |

## Çekirdekler

| Çekirdek | `K(a, b)` | Sınır |
|---|---|---|
| Doğrusal | `a·b` | düz |
| Polinom | `(a·b + 1)ᵈ` | `d`. dereceden eğri |
| RBF (Gauss) | `exp(−γ ‖a − b‖²)` | esnek, yerel |

`γ` büyükse her nokta yalnızca çok yakınını etkiler (karmaşık sınır, aşırı
uyum riski); küçükse sınır düzleşir.

## Ne zaman?

- Orta boyda veri, çok özellik (metin gibi), net bir sınır.
- Çok büyük veride çekirdekli SVM yavaş; doğrusal SVM (`LinearSVC`) ya da
  SGD tercih edilir.
- Olasılık doğal olarak çıkmaz; `SVC(probability=True)` ek bir kalibrasyonla
  üretir.

## Sık hatalar

- Ölçeklememek: uzaklık ve iç çarpım büyük birimli özelliğe kayar.
- Etiketleri 0/1 bırakmak: menteşe kaybı `−1/+1` ister.
- `C` ve `γ`'yı ayrı ayrı denemek: birlikte (ızgara) aranmalı.
