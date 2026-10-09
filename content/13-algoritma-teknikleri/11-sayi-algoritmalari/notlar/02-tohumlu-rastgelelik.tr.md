Bilgisayarın "rastgele" sayıları aslında bir formülden gelir. En eski
yöntemlerden biri **doğrusal eşlik üreteci (linear congruential generator,
LCG)**: bir sonraki sayı `(a × x + c) % m`. Başlangıç değeri `x` **tohumdur
(seed)**.

```python
def lcg(seed, count, a=1103515245, c=12345, m=2**31):
    out, x = [], seed
    for _ in range(count):
        x = (a * x + c) % m
        out.append(x)
    return out


print([x % 100 for x in lcg(42, 6)])
print([x % 100 for x in lcg(42, 6)])
print([x % 100 for x in lcg(7, 6)])


def distinct_before_repeat(a, c, m, seed=1):
    seen, x = set(), seed
    while x not in seen:
        seen.add(x)
        x = (a * x + c) % m
    return len(seen)


print(distinct_before_repeat(5, 3, 16), distinct_before_repeat(4, 3, 16))
```

```text
[27, 64, 53, 6, 35, 32]
[27, 64, 53, 6, 35, 32]
[16, 33, 38, 71, 40, 21]
16 3
```

Aynı tohum aynı diziyi verir: makine öğrenmesinde `random_state=42` yazmanın
anlamı bu, deney tekrarlanabilir olur. `m` sınırlı olduğu için dizi bir gün
tekrara düşer; `a` ve `c` iyi seçilirse (`5, 3, 16`) bütün 16 değeri dolaşır,
kötü seçilirse (`4, 3, 16`) üç değerde takılır.

Python'un `random` modülü ve NumPy'nin `default_rng`'si LCG değil, çok daha uzun döngülü
üreteçler kullanır (Mersenne Twister, PCG64). Ama fikir aynı: tohum + mod
aritmetiği. Şifreleme için tahmin edilebilir olmayan `secrets` modülü gerekir.
