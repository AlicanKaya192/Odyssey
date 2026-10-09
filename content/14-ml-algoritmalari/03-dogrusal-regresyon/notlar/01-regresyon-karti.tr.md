## Formüller

| Ne | Formül | NumPy / scikit-learn |
|---|---|---|
| Model | `ŷ = w₀ + Σ wᵢ xᵢ` = `A w` | `LinearRegression` |
| Kesişim sütunu | `A = [1, X]` | `np.column_stack([np.ones(n), X])` |
| Çözüm | `(Aᵀ A) w = Aᵀ y` | `np.linalg.solve`, `np.linalg.lstsq` |
| MSE | `Σ(y − ŷ)² / n` | `mean_squared_error` |
| RMSE | `√MSE` (hedefle aynı birim) | `root_mean_squared_error` |
| MAE | <code>Σ&#124;y − ŷ&#124; / n</code> (aykırıya daha az duyarlı) | `mean_absolute_error` |
| R² | `1 − Σ(y − ŷ)² / Σ(y − ȳ)²` | `r2_score` |

## Ne zaman dikkat?

- **Eş doğrusallık:** neredeyse aynı özellikler; `np.linalg.cond` büyükse
  ağırlıkları yorumlama, düzenlileştirme kullan.
- **Ölçek:** normal denklem ölçekten etkilenmez, ama ağırlıkları karşılaştırmak
  ve gradyan inişi (bölüm 4) için özellikler standartlaştırılır.
- **Aykırı değerler:** kare hata büyük hatayı çok cezalandırır; tek bir aykırı
  nokta doğruyu kendine çekebilir.
- **Doğrusal olmayan ilişki:** artıklarda desen varsa özellik ekle (`x²`,
  etkileşim `x₁·x₂`).

## Sık hatalar

- Kesişim sütununu unutmak: doğru orijinden geçmeye zorlanır.
- `np.linalg.inv(A.T @ A)` yazmak: `solve` ya da `lstsq` daha sağlam.
- R²'yi eğitim verisinde ölçüp yetinmek: aşırı uyumu göstermez.
