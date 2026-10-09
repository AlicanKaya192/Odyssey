Her özyinelemeli fonksiyon döngüyle de yazılabilir, her döngü de
özyinelemeyle. Hangisini seçeceğin problemin şekline bağlı.

| | Özyineleme | Döngü |
|---|---|---|
| Doğal olduğu yer | iç içe yapılar: ağaç, klasör, iç içe liste; böl ve fethet | düz diziler, sayaçlar, "n kez yap" |
| Ek bellek | her seviye için yığında bir çerçeve: `O(derinlik)` | genelde `O(1)` |
| Python'daki sınır | derinlik ~1000 (`RecursionError`) | yok |
| Okunabilirlik | tanım özyinelemeliyse çok kısa | düz işlerde daha açık |

## Özyinelemeyi döngüye çevirmek: kendi yığınını tut

Dersteki `deep_sum`, Python'un çağrı yığını yerine **kendi yığınımızla**
(bir liste) döngüyle de yazılabilir:

```python
def deep_sum_loop(items):
    total = 0
    stack = [items]                 # işlenecek listeler
    while stack:
        current = stack.pop()
        for item in current:
            if isinstance(item, list):
                stack.append(item)  # sonra işlenecek
            else:
                total += item
    return total

print(deep_sum_loop([1, [2, 3], [4, [5, [6]]]]))   # 21
```

Bu sürüm derinlik sınırına takılmaz: çok derin iç içe yapılarda (on binlerce
kat) güvenli yol budur.

## `sys.setrecursionlimit` hakkında

Sınırı büyütmek mümkün (`sys.setrecursionlimit(10_000)`), ama derinliği
gerçekten büyük olabilen bir iş için güvenilir bir çözüm değil: her seviye
bellek kullanır ve sınır yalnızca hatanın nerede çıkacağını değiştirir.
Derinlik büyük olabiliyorsa döngüye çevirmek daha sağlam.

## Kuyruk özyinelemesi (tail recursion)

Özyinelemeli çağrı fonksiyonun **son işi** ise (`return f(n - 1)` gibi,
sonucun üstünde başka işlem yok) buna kuyruk özyinelemesi denir. Bazı diller
(Scheme gibi) bunu kendiliğinden döngüye çevirir ve yığın büyümez.
**Python bunu yapmaz**: kuyruk özyinelemesi de yığında çerçeve biriktirir.
