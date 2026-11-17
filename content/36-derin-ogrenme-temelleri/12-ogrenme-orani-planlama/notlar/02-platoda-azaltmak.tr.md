Öteki zamanlayıcılar takvime bakar; `ReduceLROnPlateau` **sonuca** bakar.
Doğrulama kaybı `patience` tur boyunca iyileşmezse oranı `factor` ile
çarpar. Bu yüzden `step()`'e o turun doğrulama kaybı verilir:

```python
w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=2)
val_losses = [1.0, 0.8, 0.7, 0.7, 0.71, 0.72, 0.69, 0.69, 0.7, 0.7]
rates = []
for val_loss in val_losses:
    optimizer.step()
    scheduler.step(val_loss)
    rates.append(optimizer.param_groups[0]["lr"])
print(rates)
```

```text
[0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.025]
```

- En iyi kayıp 0,7 3. turda geldi; sonraki üç tur onu geçemedi ve 6. turun
  sonunda oran yarıya indi.
- 0,69 yeni en iyi oldu, sayaç sıfırlandı; yine üç tur iyileşme olmayınca
  oran bir kez daha yarıya indi.
- Erken durdurmayla (Düzenlileştirme bölümü) iyi anlaşır: önce oranı
  düşür, o da işe yaramazsa dur.
