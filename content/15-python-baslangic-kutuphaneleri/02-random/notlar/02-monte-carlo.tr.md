Rastgele sayılarla bir değeri **tahmin etmeye** Monte Carlo yöntemi denir.
Klasik örnek π: kenarı 1 olan karenin içine rastgele noktalar at ve çeyrek
dairenin (yarıçap 1) içine düşenleri say. Çeyrek dairenin alanı π/4, karenin
alanı 1; içeri düşenlerin oranı π/4'e yaklaşır.

```python
import math
import random


def estimate_pi(n, seed=0):
    r = random.Random(seed)
    inside = 0
    for _ in range(n):
        x, y = r.random(), r.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / n


for n in (100, 1000, 10000, 100000, 1000000):
    estimate = estimate_pi(n)
    print(n, estimate, round(abs(estimate - math.pi), 4))
```

```text
100 3.04 0.1016
1000 3.128 0.0136
10000 3.1352 0.0064
100000 3.14844 0.0068
1000000 3.14244 0.0008
```

100 noktayla tahmin 3,04 (hata 0,10); bir milyon noktayla 3,14244 (hata
0,0008). Hata genelde nokta sayısının karekökü kadar yavaş küçülür: 100 kat
nokta, yaklaşık 10 kat daha az hata. Tablo bunun dalgalı olduğunu da
gösteriyor: 10 000 noktadan 100 000'e geçince hata biraz büyüdü, çünkü her
tahmin şansa bağlı.

Monte Carlo, formülü bilinmeyen ya da çözülmesi zor sorularda işe yarar: bir
oyunda kazanma olasılığı, bir sıranın ne kadar uzayacağı, bir yatırımın
olası sonuçları. Algoritma Teknikleri modülünün Rastgele Algoritmalar
bölümünde daha fazlası var.
