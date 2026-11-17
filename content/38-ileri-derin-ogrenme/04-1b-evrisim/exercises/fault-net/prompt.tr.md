`FaultNet`'in `features` kısmını yaz: `nn.Conv1d(1, 8, 5, padding=2)`, ReLU,
`nn.Conv1d(8, 8, 5, padding=2)`, ReLU ve `nn.AdaptiveMaxPool1d(1)`. Gerisi
hazır: kod önce özelliklerin şeklini yazdırıyor, sonra ağı eğitip test
doğruluğunun %90'ı geçip geçmediğini.

**Beklenen çıktı:**

```
(2, 8, 1)
True
```
