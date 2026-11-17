`used_rates(epochs)` her turda optimizer'ın kullandığı oranı kaydediyor; ama
zamanlayıcı yanlış yerde çağrılıyor ve oran plana göre bir tur erken
düşüyor. Sırayı düzelt: oranı kaydet, `optimizer.step()`, sonra
`scheduler.step()`.

**Beklenen çıktı:**

```
[0.1, 0.1, 0.05, 0.05, 0.025, 0.025]
```
