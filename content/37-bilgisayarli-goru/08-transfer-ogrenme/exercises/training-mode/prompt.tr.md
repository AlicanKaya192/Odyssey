`training_mode(model)` iki parçalı bir modeli (gövde `model[0]`, baş
`model[1]`) dondurulmuş gövdeyle eğitime hazırlasın: model eğitim kipinde,
ama gövde (içindeki BatchNorm dahil) değerlendirme kipinde.

**Beklenen çıktı:**

```
True False True
False
```
