`predict_all(weight, rows)` her satırın sınıfını tahmin etsin: logitler
`rows · Wᵀ`, tahmin en büyük logitin sırası. Başlangıçtaki satır satır döngüyü
kaldır; bütün satırları **tek çarpımla**, `torch.inference_mode()` içinde
hesapla ve listeyi döndür.

**Beklenen çıktı:**

```
[0, 1, 2]
```
