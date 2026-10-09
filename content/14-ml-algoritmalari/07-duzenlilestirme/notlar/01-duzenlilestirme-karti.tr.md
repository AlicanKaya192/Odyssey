## Üç ceza

| Yöntem | Ceza | Etkisi | scikit-learn |
|---|---|---|---|
| Ridge (L2) | `α Σ w²` | ağırlıkları küçültür, sıfır yapmaz | `Ridge` |
| Lasso (L1) | <code>α Σ &#124;w&#124;</code> | bazı ağırlıkları tam sıfır yapar | `Lasso` |
| Elastic Net | ikisinin karışımı | seçim + eş doğrusallıkta kararlılık | `ElasticNet` |

## scikit-learn'de `α`'nın ölçeği

Aynı adlı ayar her modelde aynı ölçekte değil:

- `Ridge`: `‖y − Xw‖² + α ‖w‖²` (hata **toplamı**).
- `Lasso`: `‖y − Xw‖² / (2n) + α ‖w‖₁` (hata **ortalaması**, yarısı).
- `LogisticRegression`: `C = 1 / α`; büyük `C` az düzenlileştirme,
  `C=np.inf` hiç.

Sıfırdan yazıp karşılaştırırken bu ölçekler tutturulmalı; derste tutturuldu.

## Neden önce standartlaştırma?

Ceza bütün ağırlıklara aynı katsayıyla uygulanır. Bir özellik metre yerine
milimetreyle ölçülürse ağırlığı bin kat küçülür ve ceza onu neredeyse hiç
etkilemez. Standartlaştırma her özelliği aynı ölçeğe getirir.

## Sık hatalar

- Kesişimi cezalandırmak: model ortalamayı tutturamaz. Önce merkezle.
- `α`'yı eğitim hatasıyla seçmek: hep `α = 0` çıkar.
- Lasso'nun seçtiği özellikleri kesin gerçek sanmak: eş doğrusal iki
  özellikten birini neredeyse rastgele seçebilir.
