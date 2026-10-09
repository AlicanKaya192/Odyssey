## Sınıflandırma ölçüleri

| Ölçü | Formül | Soru | scikit-learn |
|---|---|---|---|
| Doğruluk | `(TP + TN) / n` | kaçta kaçı doğru? | `accuracy_score` |
| Kesinlik | `TP / (TP + FP)` | "pozitif" dediklerimin kaçı doğru? | `precision_score` |
| Duyarlılık | `TP / (TP + FN)` | pozitiflerin kaçını buldum? | `recall_score` |
| Özgüllük | `TN / (TN + FP)` | negatiflerin kaçını doğru bıraktım? | — |
| F1 | `2PR / (P + R)` | kesinlik ve duyarlılık birlikte | `f1_score` |
| ROC AUC | eğri altı alan | pozitif negatiften yüksek puan alır mı? | `roc_auc_score` |
| Ortalama kesinlik | kesinliklerin ağırlıklı toplamı | dengesizde pozitifleri bulmak | `average_precision_score` |

## Regresyon ölçüleri (bölüm 3)

MSE, RMSE (hedefin biriminde), MAE (aykırıya dayanıklı), R² (taban çizgisine
göre).

## Hangisi ne zaman?

- Sınıflar dengeliyse ve hataların bedeli eşitse doğruluk yeter.
- Yanlış alarm pahalıysa (spam filtresi gerçek postayı silerse) kesinlik.
- Kaçırmak pahalıysa (hastalık, dolandırıcılık) duyarlılık.
- Eşikten bağımsız sıralama kalitesi için ROC AUC; pozitifler çok azsa
  ortalama kesinlik.

## Sık hatalar

- Dengesiz veride doğruluğu raporlamak; taban çizgisini (en sık sınıf)
  yanına yazmamak.
- Puan yerine 0/1 tahminle AUC hesaplamak: eğri tek noktaya iner.
- Kesinlik ve duyarlılığı eşik söylemeden vermek: ikisi de eşiğe bağlı.
