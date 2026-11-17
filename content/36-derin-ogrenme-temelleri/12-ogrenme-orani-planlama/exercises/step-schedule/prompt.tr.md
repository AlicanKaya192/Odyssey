`step_rates(lr, step_size, gamma, epochs)` bir parametreli SGD'yi `StepLR` ile
sarsın ve her turun başındaki öğrenme oranını (6 basamakla) bir listeye
eklesin. Her turda önce `optimizer.step()`, sonra `scheduler.step()`.

**Beklenen çıktı:**

```
[0.1, 0.1, 0.05, 0.05, 0.025]
```
