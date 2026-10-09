## Formüller

| Ne | Formül |
|---|---|
| Sigmoid | `σ(z) = 1 / (1 + e⁻ᶻ)` |
| Olasılık | `p = σ(A w)` |
| Log kaybı | `−ort(y log p + (1 − y) log(1 − p))` |
| Gradyan | `Aᵀ (p − y) / n` |
| Karar | `p ≥ eşik` ise 1 |
| Softmax | `pₖ = e^(zₖ) / Σ e^(zⱼ)` |

## Ağırlığı yorumlamak

`wᵢ`, `xᵢ` bir birim artınca **log-odds**'un (`log(p / (1 − p))`) ne kadar
arttığıdır. `e^(wᵢ)` odds oranıdır: `wᵢ = 0,7` ise `e^0,7 ≈ 2`, yani odds iki
katına çıkar. Özellikler standartlaştırıldıysa ağırlıklar birbiriyle
karşılaştırılabilir.

## scikit-learn ile

- `LogisticRegression()` varsayılan olarak düzenlileştirir (`C=1`);
  düzenlileştirmesiz karşılaştırma için `C=np.inf`.
- `predict_proba(X)[:, 1]` sınıf 1'in olasılığı; `predict` eşiği 0,5 alır.
- Çok sınıfta softmax (multinomial) kullanılır.

## Sık hatalar

- `np.log(0)`: olasılık tam 0 ya da 1 olursa kayıp sonsuz; pratikte
  `np.clip(p, 1e-12, 1 - 1e-12)`.
- Büyük negatif `z`'de `np.exp(-z)` taşar; uyarı verir ama sigmoid yine 0'a
  gider. Softmax'ta en büyüğü çıkar.
- Sınıfları ayıran mükemmel bir doğru varsa düzenlileştirmesiz ağırlıklar
  sonsuza büyür; gradyan inişi hiç durmaz.
