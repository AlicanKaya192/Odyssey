Zamanlayıcının `step()`'i optimizer'ınkinden **önce** çağrılırsa PyTorch
uyarı verir; oran plana göre bir tur erken değişir:

```python
import warnings

w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.StepLR(optimizer, step_size=3)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    scheduler.step()
print(str(caught[0].message).split(". ")[0])
```

```text
Detected call of `lr_scheduler.step()` before `optimizer.step()`
```

- Doğru kalıp: her kümede `zero_grad`, `backward`, (gerekirse kırpma),
  `optimizer.step()`; turun sonunda bir kez `scheduler.step()`.
- `T_max`, `step_size` gibi sayılar **`scheduler.step()` çağrısı** sayısıdır.
  Zamanlayıcıyı her kümede çağırıyorsan (bazı ısınma planlarında böyle
  yapılır) bu sayıları tur değil adım cinsinden vermelisin; yoksa plan ilk
  turda biter.
- Oranı kayıt için okumak: `scheduler.get_last_lr()` ya da
  `optimizer.param_groups[0]["lr"]`.
