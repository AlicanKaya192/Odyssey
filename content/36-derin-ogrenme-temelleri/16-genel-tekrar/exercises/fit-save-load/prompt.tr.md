`fit_save_load` `y = 2x + 1` doğrusunu öğreniyor ve başka tohumla yeni bir
`fresh` modeli kuruyor. Eğitilen modelin state_dict'ini `line.pt`'ye kaydet ve
`fresh`'e `weights_only=True` ile yükle; sonuç `[2.0, 1.0, True]` olmalı.

**Beklenen çıktı:**

```
[2.0, 1.0, True]
```
