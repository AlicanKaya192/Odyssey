Erken durdurmayı her projede yeniden yazmamak için küçük bir sınıf işe
yarar. `min_delta` "iyileşme sayılması için en az ne kadar düşmeli"
demek:

```python
class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.0):
        self.patience, self.min_delta = patience, min_delta
        self.best, self.waited = float("inf"), 0

    def step(self, val_loss):
        if val_loss < self.best - self.min_delta:
            self.best, self.waited = val_loss, 0
            return False
        self.waited += 1
        return self.waited >= self.patience


stopper = EarlyStopping(patience=3)
losses = [0.9, 0.7, 0.6, 0.62, 0.61, 0.65, 0.5]
for epoch, loss in enumerate(losses, start=1):
    if stopper.step(loss):
        print("stop at", epoch, "best", stopper.best)
        break
```

```text
stop at 6 best 0.6
```

- 3. turdaki 0,6'dan sonra üç tur iyileşme yok; 6. turda durdu.
- 7. turda kayıp 0,5'e inecekti, ama o turu hiç görmedik. Sabır bir
  pazarlık: küçük sabır erken (bazen fazla erken) durdurur, büyük sabır
  boşuna tur harcar. Tipik değerler 5–20 tur.
- `min_delta`, gürültü düzeyindeki küçük düşüşlerin (0,6 → 0,5999) sayacı
  sıfırlamasını önler.
