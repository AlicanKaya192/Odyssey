Model eğitilmiş ve bir kez kurulmuş. `predict(values)` fonksiyonunu yaz:

- 6 değer değilse `ValueError("expected 6 values, got N")`.
- `torch.inference_mode()` içinde logitler ve `softmax`.
- `{"label": sınıf adı, "probability": olasılığı (2 basamak)}` döndür.

**Beklenen çıktı:**

```
high True
expected 6 values, got 1
```
