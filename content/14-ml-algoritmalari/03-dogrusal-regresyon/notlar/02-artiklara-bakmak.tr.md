Yüksek R² modelin doğru biçimde olduğunu göstermez. **Artıklar** (residuals,
`y − ŷ`) rastgele dağılmalı; bir desen varsa model bir şeyi kaçırıyor demektir.
Eğri bir ilişkiye doğru uyduralım:

```python
import numpy as np

rng = np.random.default_rng(4)
x = np.sort(rng.uniform(0, 10, 90))
y = 2 + 0.5 * x ** 2 + rng.normal(0, 2, 90)       # gerçekte eğri
A = np.column_stack([np.ones(90), x])
w = np.linalg.lstsq(A, y, rcond=None)[0]
resid = y - A @ w
r2 = 1 - (resid ** 2).sum() / ((y - y.mean()) ** 2).sum()
print(round(r2, 3))
for part in np.array_split(resid, 3):              # sol, orta, sağ
    print(round(part.mean(), 2))
```

```text
0.941
1.62
-3.27
1.65
```

R² yüksek görünüyor, ama artıklar düzenli: solda ve sağda artı, ortada eksi.
Doğru, eğrinin uçlarında altta, ortasında üstte kalıyor. Çözüm modele `x²`
özelliğini eklemek. Artıkları `x`'e ya da tahmine karşı çizmek (ya da bu gibi
parçaların ortalamasına bakmak) her regresyondan sonra yapılacak ilk iştir.
