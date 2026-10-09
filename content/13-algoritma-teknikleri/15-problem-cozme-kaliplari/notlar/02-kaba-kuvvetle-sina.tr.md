Hızlı bir algoritma yazınca doğru olduğundan nasıl emin olursun? Elle seçilmiş
birkaç örnek, ince bir hatayı kaçırabilir. Güvenilir yol **karşılaştırma testi
(stress testing)**: yavaş ama açıkça doğru bir kaba kuvvet çözümü yaz, sonra
iki çözümü yüzlerce **küçük, rastgele** girdide yarıştır. İlk farklılık,
hatayı gösteren en sade örnek olur.

```python
import random


def slow(temps):
    result = [0] * len(temps)
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            if temps[j] > temps[i]:
                result[i] = j - i
                break
    return result


def fast_buggy(temps):
    result, stack = [0] * len(temps), []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] <= t:   # hata: <= olmamalı
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def fast(temps):
    result, stack = [0] * len(temps), []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def stress(fn, trials=500):
    rng = random.Random(1)
    for _ in range(trials):
        temps = [rng.randint(15, 20) for _ in range(rng.randint(1, 8))]
        if fn(temps) != slow(temps):
            return temps, fn(temps), slow(temps)
    return "ok"


print(stress(fast_buggy))
print(stress(fast))
```

```text
([18, 18], [1, 0], [0, 0])
ok
```

Hatalı sürüm "eşit sıcaklık da daha sıcak sayılır" diyordu; karşılaştırma testi
bunu iki elemanlı bir örnekle yakaladı: `[18, 18]`. Doğru sürüm 500 denemenin
hepsinde kaba kuvvetle aynı.

İki ipucu: girdileri **küçük** tut (hata çıkınca elle izlenebilsin) ve
değerleri **dar** bir aralıktan seç (15–20 arası sıcaklık eşitlikleri sık
üretir; eşitlik hataların sık saklandığı yerdir). Rastgele üreteci tohumla,
hata her çalıştırmada aynı örnekle tekrarlansın.
