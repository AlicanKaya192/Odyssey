Çekirdek hilesinin özü bir eşitlik: bazı fonksiyonlar, noktaları daha büyük
bir uzaya taşıyıp orada iç çarpım almakla **aynı sonucu** verir. İki boyutlu
noktalar için ikinci dereceden çekirdek `(a·b + 1)²`, altı boyutlu bir
genişletmedeki iç çarpıma eşittir:

```python
import numpy as np


def phi(v):
    x1, x2 = v
    r = np.sqrt(2)
    return np.array([1, r * x1, r * x2, x1 * x1, x2 * x2, r * x1 * x2])


def poly_kernel(a, b):
    return (a @ b + 1) ** 2


a = np.array([1.0, 2.0])
b = np.array([3.0, -1.0])
print(round(phi(a) @ phi(b), 6), round(poly_kernel(a, b), 6))
print(len(phi(a)))
```

```text
0.641 0.976
0.939
```

İki yol aynı sayıyı veriyor: altı boyutlu vektörleri kurmadan, iki boyutlu iç
çarpımın üzerinden. Boyut büyüdükçe fark devleşir: 100 özellikli veride
ikinci dereceden genişletme 5 000'den fazla boyut ister, çekirdek ise yine tek
bir iç çarpım ve kare. RBF çekirdeği `exp(−γ ‖a − b‖²)` sonsuz boyutlu bir
genişletmeye karşılık gelir; açıkça kurmak imkânsız, çekirdekle hesaplamak
kolay.

Bedeli: çekirdekli SVM bütün nokta çiftleri arasındaki çekirdek değerine
bakar; eğitim süresi örnek sayısıyla kabaca karesel büyür. On binlerce
satırdan sonra doğrusal SVM ya da başka yöntemler tercih edilir.
