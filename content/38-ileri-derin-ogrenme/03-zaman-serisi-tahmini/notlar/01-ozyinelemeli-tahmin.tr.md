Dersteki model hep **bir gün** ilerisini tahmin etti ve her gün gerçek
değerleri gördü. İki hafta sonrası istenirse gerçek değerler henüz yok:
modelin kendi tahminini pencerenin sonuna ekleyip bir sonraki günü
tahmin etmek gerekir (özyinelemeli tahmin, recursive forecast). Aşağıdaki
kod dersteki modeli ve değişkenleri kullanıyor; test döneminde her 7 günde
bir yeni bir başlangıç noktasından 14 gün tahmin edip aynı günlerin bir
günlük tahminleriyle karşılaştırıyor.

```python
def recursive(start, days=14):
    window = torch.tensor(scaled[start - 28:start]).reshape(1, 28, 1)
    preds = []
    with torch.no_grad():
        for _ in range(days):
            p = model(window)
            preds.append(p.item())
            window = torch.cat([window[:, 1:], p.reshape(1, 1, 1)], dim=1)
    return np.array(preds) * std + mean


starts = range(split, len(series) - 14, 7)
errors_multi, errors_one = [], []
for s in starts:
    days = series[s:s + 14]
    errors_multi.append(np.abs(recursive(s) - days).mean())
    errors_one.append(np.abs(pred[s - split:s - split + 14] - days).mean())
print(len(starts), np.mean(errors_multi) > np.mean(errors_one))
```

```text
13 True
```

- `torch.cat([window[:, 1:], ...], dim=1)`: pencerenin en eski gününü atıp
  tahmini sona ekler; pencere hep 28 gün kalır.
- 13 başlangıç noktasının ortalamasında özyinelemeli tahminin hatası bir
  günlük tahmininkinden büyük: her tahminin hatası bir sonraki tahminin
  **girdisi** oluyor ve hatalar birikiyor.
- Tek tek bakınca birkaç pencerede tersi de oluyor. Tek bir 14 günlük
  pencereye bakıp karar vermek bu yüzden yanıltır; Zaman Serileri
  patikasındaki gibi birden çok kesimin ortalamasına bakılır.

## Birkaç gün ilerisi için üç yol

| Yol | Nasıl | Artısı / eksisi |
|---|---|---|
| Özyinelemeli | Tek adımlık modelin tahminini girdi yap | Tek model; hata birikir |
| Doğrudan | Her ufuk için ayrı model (1 gün, 2 gün, ...) | Birikme yok; çok model |
| Çok çıkışlı | Son katman `nn.Linear(hidden, 14)`: 14 günü birden ver | Tek model, birikme yok; en yaygın derin öğrenme yolu |
