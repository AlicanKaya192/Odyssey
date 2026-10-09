# Sezgisel Optimizasyon

Bazı problemlerde en iyi cevabı bulmanın bilinen tek yolu bütün olasılıkları
denemektir ve olasılık sayısı patlar. **Gezgin satıcı problemi (traveling
salesman problem, TSP)** bunların en ünlüsü: `n` şehrin hepsine bir kez uğrayıp
başa dönen en kısa tur hangisi? **Sezgisel (heuristic)** yöntemler en iyiyi
garanti etmez ama makul sürede **iyi** bir cevap bulur. Burada önce küçük bir
örnekte gerçek en iyiyi bulup sezgisellerin ne kadar yaklaştığını ölçüyoruz.

## Kaba kuvvet: dokuz şehir

Başlangıç şehrini sabitleyince kalan 8 şehrin her sıralaması bir tur:
`8! = 40 320` tur.

```python
import itertools
import math
import random

random.seed(3)
cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(9)]


def tour_length(tour, pts):
    # tour[-1]'den tour[0]'a dönüş de dahil
    return sum(math.dist(pts[tour[i]], pts[tour[i - 1]])
               for i in range(len(tour)))


def brute_force(pts):
    best, count = None, 0
    for rest in itertools.permutations(range(1, len(pts))):
        count += 1
        tour = (0,) + rest
        if best is None or tour_length(tour, pts) < tour_length(best, pts):
            best = tour
    return list(best), count


best, count = brute_force(cities)
print(count, round(tour_length(best, cities), 1))
```

```text
40320 226.1
```

Dokuz şehirde en kısa tur 226.1. Ama şehir sayısı 60 olsa tur sayısı 80
basamaklı bir sayı olurdu (aşağıda ölçüyoruz): evrenin ömrü yetmez.

## En yakın komşu: açgözlü bir tur

İlk akla gelen sezgisel: bulunduğun şehirden **henüz gidilmemiş en yakın**
şehre git. `O(n²)`, çok hızlı.

```python
def nearest_neighbour(pts, start=0):
    tour = [start]
    left = set(range(len(pts))) - {start}
    while left:
        here = pts[tour[-1]]
        nxt = min(left, key=lambda c: math.dist(here, pts[c]))
        tour.append(nxt)
        left.remove(nxt)
    return tour


nn = nearest_neighbour(cities)
print(nn, round(tour_length(nn, cities), 1))
```

```text
[0, 8, 2, 3, 6, 7, 1, 4, 5] 232.9
```

232.9: en iyiden yaklaşık %3 uzun. Açgözlü seçim başta iyi gidiyor, ama sonda
geride bıraktığı uzak şehirlere dönmek zorunda kalıyor.

## Yerel arama: 2-opt

**Yerel arama (local search)** elindeki çözümü küçük değişikliklerle
iyileştirir ve iyileşme kalmayınca durur. TSP'de en bilinen değişiklik
**2-opt**: turdan iki kenarı çıkar, aradaki parçayı ters çevirip yeniden bağla.
Kesişen iki yol varsa bu hamle kesişmeyi açar ve tur kısalır.

<figure class="fig">
<svg viewBox="0 0 540 280" width="540" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="130" y="18" font-size="13" text-anchor="middle">en yakın komşu: 766</text><polyline class="curve" points="64.4,39.0 56.5,42.9 52.7,37.2 72.0,32.0 95.6,59.3 100.5,69.8 96.4,76.2 107.8,53.5 131.2,100.0 131.8,101.7 129.4,114.1 149.0,95.1 100.5,111.4 91.2,104.1 102.7,132.3 118.8,151.2 136.9,147.7 117.1,169.7 74.0,168.4 65.6,171.6 50.8,165.5 35.6,145.0 25.1,121.2 33.4,104.4 40.3,100.8 42.4,86.6 58.4,86.0 56.1,70.7 27.1,53.2 12.9,187.6 14.8,206.0 30.4,210.6 31.5,213.8 14.1,236.3 32.8,249.5 44.1,254.6 57.4,234.0 62.8,211.5 105.1,230.1 101.0,242.7 116.0,250.0 82.0,266.8 151.2,200.7 188.5,185.7 193.4,188.0 221.4,201.4 210.6,219.6 224.0,227.9 249.8,219.7 245.2,254.9 241.6,269.3 220.0,262.1 237.1,152.7 247.7,130.8 226.3,130.4 212.4,149.1 164.0,159.8 241.6,87.7 178.5,42.0 169.2,36.0 64.4,39.0" fill="none"/><circle class="dot" cx="64.4" cy="39.0" r="3"/><circle class="dot" cx="40.3" cy="100.8" r="3"/><circle class="dot" cx="30.4" cy="210.6" r="3"/><circle class="dot" cx="249.8" cy="219.7" r="3"/><circle class="dot" cx="164.0" cy="159.8" r="3"/><circle class="dot" cx="118.8" cy="151.2" r="3"/><circle class="dot" cx="56.1" cy="70.7" r="3"/><circle class="dot" cx="31.5" cy="213.8" r="3"/><circle class="dot" cx="14.8" cy="206.0" r="3"/><circle class="dot" cx="107.8" cy="53.5" r="3"/><circle class="dot" cx="101.0" cy="242.7" r="3"/><circle class="dot" cx="72.0" cy="32.0" r="3"/><circle class="dot" cx="25.1" cy="121.2" r="3"/><circle class="dot" cx="100.5" cy="111.4" r="3"/><circle class="dot" cx="91.2" cy="104.1" r="3"/><circle class="dot" cx="129.4" cy="114.1" r="3"/><circle class="dot" cx="226.3" cy="130.4" r="3"/><circle class="dot" cx="44.1" cy="254.6" r="3"/><circle class="dot" cx="237.1" cy="152.7" r="3"/><circle class="dot" cx="56.5" cy="42.9" r="3"/><circle class="dot" cx="149.0" cy="95.1" r="3"/><circle class="dot" cx="221.4" cy="201.4" r="3"/><circle class="dot" cx="95.6" cy="59.3" r="3"/><circle class="dot" cx="42.4" cy="86.6" r="3"/><circle class="dot" cx="33.4" cy="104.4" r="3"/><circle class="dot" cx="178.5" cy="42.0" r="3"/><circle class="dot" cx="212.4" cy="149.1" r="3"/><circle class="dot" cx="57.4" cy="234.0" r="3"/><circle class="dot" cx="136.9" cy="147.7" r="3"/><circle class="dot" cx="27.1" cy="53.2" r="3"/><circle class="dot" cx="131.8" cy="101.7" r="3"/><circle class="dot" cx="62.8" cy="211.5" r="3"/><circle class="dot" cx="12.9" cy="187.6" r="3"/><circle class="dot" cx="74.0" cy="168.4" r="3"/><circle class="dot" cx="100.5" cy="69.8" r="3"/><circle class="dot" cx="224.0" cy="227.9" r="3"/><circle class="dot" cx="105.1" cy="230.1" r="3"/><circle class="dot" cx="169.2" cy="36.0" r="3"/><circle class="dot" cx="58.4" cy="86.0" r="3"/><circle class="dot" cx="82.0" cy="266.8" r="3"/><circle class="dot" cx="193.4" cy="188.0" r="3"/><circle class="dot" cx="50.8" cy="165.5" r="3"/><circle class="dot" cx="65.6" cy="171.6" r="3"/><circle class="dot" cx="117.1" cy="169.7" r="3"/><circle class="dot" cx="151.2" cy="200.7" r="3"/><circle class="dot" cx="32.8" cy="249.5" r="3"/><circle class="dot" cx="35.6" cy="145.0" r="3"/><circle class="dot" cx="96.4" cy="76.2" r="3"/><circle class="dot" cx="131.2" cy="100.0" r="3"/><circle class="dot" cx="245.2" cy="254.9" r="3"/><circle class="dot" cx="14.1" cy="236.3" r="3"/><circle class="dot" cx="102.7" cy="132.3" r="3"/><circle class="dot" cx="188.5" cy="185.7" r="3"/><circle class="dot" cx="241.6" cy="269.3" r="3"/><circle class="dot" cx="210.6" cy="219.6" r="3"/><circle class="dot" cx="220.0" cy="262.1" r="3"/><circle class="dot" cx="241.6" cy="87.7" r="3"/><circle class="dot" cx="247.7" cy="130.8" r="3"/><circle class="dot" cx="52.7" cy="37.2" r="3"/><circle class="dot" cx="116.0" cy="250.0" r="3"/><text class="dim" x="400" y="18" font-size="13" text-anchor="middle">2-opt: 690</text><polyline class="curve" points="334.4,39.0 326.5,42.9 322.7,37.2 342.0,32.0 377.8,53.5 439.2,36.0 448.5,42.0 511.6,87.7 517.7,130.8 496.3,130.4 507.1,152.7 482.4,149.1 434.0,159.8 458.5,185.7 463.4,188.0 491.4,201.4 519.8,219.7 515.2,254.9 511.6,269.3 490.0,262.1 494.0,227.9 480.6,219.6 421.2,200.7 375.1,230.1 371.0,242.7 386.0,250.0 352.0,266.8 332.8,211.5 327.4,234.0 314.1,254.6 302.8,249.5 284.1,236.3 301.5,213.8 300.4,210.6 284.8,206.0 282.9,187.6 295.1,121.2 303.4,104.4 310.3,100.8 312.4,86.6 297.1,53.2 326.1,70.7 328.4,86.0 305.6,145.0 320.8,165.5 335.6,171.6 344.0,168.4 387.1,169.7 406.9,147.7 388.8,151.2 372.7,132.3 361.2,104.1 370.5,111.4 399.4,114.1 401.8,101.7 401.2,100.0 419.0,95.1 366.4,76.2 370.5,69.8 365.6,59.3 334.4,39.0" fill="none"/><circle class="dot" cx="334.4" cy="39.0" r="3"/><circle class="dot" cx="310.3" cy="100.8" r="3"/><circle class="dot" cx="300.4" cy="210.6" r="3"/><circle class="dot" cx="519.8" cy="219.7" r="3"/><circle class="dot" cx="434.0" cy="159.8" r="3"/><circle class="dot" cx="388.8" cy="151.2" r="3"/><circle class="dot" cx="326.1" cy="70.7" r="3"/><circle class="dot" cx="301.5" cy="213.8" r="3"/><circle class="dot" cx="284.8" cy="206.0" r="3"/><circle class="dot" cx="377.8" cy="53.5" r="3"/><circle class="dot" cx="371.0" cy="242.7" r="3"/><circle class="dot" cx="342.0" cy="32.0" r="3"/><circle class="dot" cx="295.1" cy="121.2" r="3"/><circle class="dot" cx="370.5" cy="111.4" r="3"/><circle class="dot" cx="361.2" cy="104.1" r="3"/><circle class="dot" cx="399.4" cy="114.1" r="3"/><circle class="dot" cx="496.3" cy="130.4" r="3"/><circle class="dot" cx="314.1" cy="254.6" r="3"/><circle class="dot" cx="507.1" cy="152.7" r="3"/><circle class="dot" cx="326.5" cy="42.9" r="3"/><circle class="dot" cx="419.0" cy="95.1" r="3"/><circle class="dot" cx="491.4" cy="201.4" r="3"/><circle class="dot" cx="365.6" cy="59.3" r="3"/><circle class="dot" cx="312.4" cy="86.6" r="3"/><circle class="dot" cx="303.4" cy="104.4" r="3"/><circle class="dot" cx="448.5" cy="42.0" r="3"/><circle class="dot" cx="482.4" cy="149.1" r="3"/><circle class="dot" cx="327.4" cy="234.0" r="3"/><circle class="dot" cx="406.9" cy="147.7" r="3"/><circle class="dot" cx="297.1" cy="53.2" r="3"/><circle class="dot" cx="401.8" cy="101.7" r="3"/><circle class="dot" cx="332.8" cy="211.5" r="3"/><circle class="dot" cx="282.9" cy="187.6" r="3"/><circle class="dot" cx="344.0" cy="168.4" r="3"/><circle class="dot" cx="370.5" cy="69.8" r="3"/><circle class="dot" cx="494.0" cy="227.9" r="3"/><circle class="dot" cx="375.1" cy="230.1" r="3"/><circle class="dot" cx="439.2" cy="36.0" r="3"/><circle class="dot" cx="328.4" cy="86.0" r="3"/><circle class="dot" cx="352.0" cy="266.8" r="3"/><circle class="dot" cx="463.4" cy="188.0" r="3"/><circle class="dot" cx="320.8" cy="165.5" r="3"/><circle class="dot" cx="335.6" cy="171.6" r="3"/><circle class="dot" cx="387.1" cy="169.7" r="3"/><circle class="dot" cx="421.2" cy="200.7" r="3"/><circle class="dot" cx="302.8" cy="249.5" r="3"/><circle class="dot" cx="305.6" cy="145.0" r="3"/><circle class="dot" cx="366.4" cy="76.2" r="3"/><circle class="dot" cx="401.2" cy="100.0" r="3"/><circle class="dot" cx="515.2" cy="254.9" r="3"/><circle class="dot" cx="284.1" cy="236.3" r="3"/><circle class="dot" cx="372.7" cy="132.3" r="3"/><circle class="dot" cx="458.5" cy="185.7" r="3"/><circle class="dot" cx="511.6" cy="269.3" r="3"/><circle class="dot" cx="480.6" cy="219.6" r="3"/><circle class="dot" cx="490.0" cy="262.1" r="3"/><circle class="dot" cx="511.6" cy="87.7" r="3"/><circle class="dot" cx="517.7" cy="130.8" r="3"/><circle class="dot" cx="322.7" cy="37.2" r="3"/><circle class="dot" cx="386.0" cy="250.0" r="3"/></svg>
<figcaption>Altmış şehir. Solda en yakın komşunun turu: sonda uzun dönüşler ve kesişmeler var. Sağda 2-opt sonrası: kesişmeler açılmış.</figcaption>
</figure>

```python
def two_opt(tour, pts):
    tour = tour[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                if tour_length(new, pts) < tour_length(tour, pts) - 1e-9:
                    tour, improved = new, True
    return tour


opt = two_opt(nn, cities)
print(opt, round(tour_length(opt, cities), 1))
```

```text
[0, 8, 2, 3, 7, 5, 4, 1, 6] 226.1
```

2-opt en yakın komşunun turunu 226.1'e indirdi: bu örnekte kaba kuvvetin
bulduğu en iyiyle aynı. Bunun garantisi yok, ama 40 320 tur denemek yerine
birkaç tur iyileştirme yetti.

## Altmış şehir

Kaba kuvvetin imkânsız olduğu büyüklükte üç yolu karşılaştıralım: rastgele bir
tur, en yakın komşu ve onun üstüne 2-opt.

```python
random.seed(8)
big = [(random.random() * 100, random.random() * 100) for _ in range(60)]
rand_tour = list(range(60))
random.shuffle(rand_tour)
nn_big = nearest_neighbour(big)
print(round(tour_length(rand_tour, big)), round(tour_length(nn_big, big)),
      round(tour_length(two_opt(nn_big, big), big)))
print(len(str(math.factorial(59) // 2)))
```

```text
3155 766 690
80
```

Rastgele tur 3155, en yakın komşu 766, 2-opt 690. En iyi turun ne olduğunu
bilmiyoruz; ama denenecek tur sayısı (yön farkı sayılmadan `59!/2`) 80 basamaklı
olduğu için bilmenin yolu da yok. Sezgisellerin gücü burada.

## Yerel en iyi tuzağı ve tavlama benzetimi

Yerel arama, komşularının hepsinden iyi ama genel olarak en iyi olmayan bir
**yerel en iyide (local optimum)** takılabilir. Çok çukurlu bir fonksiyonda
görmek kolay: `f(x) = x²/10 + 10·sin(x)`.

<figure class="fig">
<svg viewBox="0 0 560 396" width="560" xmlns="http://www.w3.org/2000/svg"><polyline class="curve" points="10.0,50.4 12.2,54.6 14.5,60.7 16.8,68.5 19.0,77.8 21.2,88.3 23.5,99.6 25.8,111.3 28.0,122.9 30.2,134.0 32.5,144.1 34.8,152.9 37.0,160.0 39.2,165.3 41.5,168.7 43.8,170.2 46.0,170.1 48.2,168.4 50.5,165.7 52.8,162.2 55.0,158.5 57.2,155.0 59.5,152.2 61.8,150.4 64.0,150.0 66.2,151.3 68.5,154.4 70.8,159.3 73.0,165.9 75.2,174.1 77.5,183.5 79.8,193.8 82.0,204.5 84.2,215.2 86.5,225.5 88.8,234.8 91.0,242.8 93.2,249.2 95.5,253.8 97.8,256.5 100.0,257.4 102.2,256.5 104.5,254.1 106.8,250.5 109.0,246.2 111.2,241.5 113.5,237.1 115.8,233.2 118.0,230.3 120.2,228.8 122.5,228.9 124.8,230.7 127.0,234.5 129.2,239.9 131.5,247.0 133.8,255.3 136.0,264.6 138.2,274.3 140.5,284.1 142.8,293.5 145.0,302.0 147.2,309.3 149.5,315.0 151.8,318.9 154.0,320.9 156.2,321.1 158.5,319.4 160.8,316.3 163.0,311.9 165.2,306.7 167.5,301.1 169.8,295.6 172.0,290.7 174.2,286.7 176.5,284.1 178.8,283.0 181.0,283.7 183.2,286.2 185.5,290.5 187.8,296.4 190.0,303.7 192.2,311.9 194.5,320.7 196.8,329.5 199.0,338.1 201.2,345.8 203.5,352.3 205.8,357.3 208.0,360.5 210.2,361.8 212.5,361.3 214.8,358.9 217.0,355.0 219.2,349.8 221.5,343.8 223.8,337.3 226.0,330.8 228.2,324.8 230.5,319.8 232.8,316.0 235.0,313.7 237.2,313.3 239.5,314.6 241.8,317.7 244.0,322.5 246.2,328.6 248.5,335.8 250.8,343.6 253.0,351.5 255.2,359.2 257.5,366.1 259.8,371.8 262.0,376.1 264.2,378.6 266.5,379.2 268.8,378.0 271.0,374.9 273.2,370.3 275.5,364.3 277.8,357.4 280.0,350.0 282.2,342.6 284.5,335.5 286.8,329.4 289.0,324.5 291.2,321.1 293.5,319.4 295.8,319.6 298.0,321.5 300.2,325.1 302.5,330.2 304.8,336.3 307.0,343.1 309.2,350.1 311.5,356.8 313.8,362.9 316.0,367.9 318.2,371.4 320.5,373.3 322.8,373.2 325.0,371.3 327.2,367.5 329.5,362.1 331.8,355.3 334.0,347.6 336.2,339.3 338.5,330.9 340.8,322.8 343.0,315.6 345.2,309.5 347.5,305.0 349.8,302.1 352.0,301.1 354.2,301.9 356.5,304.4 358.8,308.3 361.0,313.3 363.2,319.1 365.5,325.2 367.8,331.1 370.0,336.3 372.2,340.5 374.5,343.3 376.8,344.4 379.0,343.7 381.2,341.1 383.5,336.6 385.8,330.4 388.0,322.9 390.2,314.3 392.5,305.1 394.8,295.8 397.0,286.7 399.2,278.4 401.5,271.2 403.8,265.5 406.0,261.5 408.2,259.3 410.5,258.9 412.8,260.2 415.0,263.0 417.2,267.0 419.5,271.7 421.8,276.8 424.0,281.8 426.2,286.3 428.5,289.7 430.8,291.7 433.0,292.1 435.2,290.7 437.5,287.4 439.8,282.2 442.0,275.3 444.2,267.0 446.5,257.6 448.8,247.5 451.0,237.2 453.2,227.1 455.5,217.8 457.8,209.5 460.0,202.6 462.2,197.4 464.5,194.0 466.8,192.4 469.0,192.6 471.2,194.3 473.5,197.2 475.8,200.9 478.0,205.1 480.2,209.2 482.5,212.7 484.8,215.4 487.0,216.7 489.2,216.4 491.5,214.3 493.8,210.3 496.0,204.4 498.2,196.8 500.5,187.7 502.8,177.4 505.0,166.5 507.2,155.2 509.5,144.2 511.8,133.7 514.0,124.3 516.2,116.3 518.5,109.9 520.8,105.4 523.0,102.6 525.2,101.6 527.5,102.1 529.8,104.0 532.0,106.7 534.2,109.9 536.5,113.0 538.8,115.8 541.0,117.6 543.2,118.2 545.5,117.2 547.8,114.3 550.0,109.6" fill="none"/><circle class="dot2" cx="44.7" cy="170.4" r="5"/><circle class="dot2" cx="99.9" cy="257.4" r="5"/><circle class="dot2" cx="155.3" cy="321.2" r="5"/><circle class="dot2" cx="210.7" cy="361.9" r="5"/><circle class="dot3" cx="266.1" cy="379.3" r="5"/><circle class="dot2" cx="321.6" cy="373.5" r="5"/><circle class="dot2" cx="377.0" cy="344.4" r="5"/><circle class="dot2" cx="432.4" cy="292.2" r="5"/><circle class="dot2" cx="487.7" cy="216.8" r="5"/><circle class="dot2" cx="543.0" cy="118.2" r="5"/></svg>
<figcaption><code>x</code> −30 ile 30 arasında 10 çukur (yerel en iyi, turuncu). Yalnızca biri genel en iyi (yeşil, x ≈ -1.54).</figcaption>
</figure>

**Tepe tırmanma (hill climbing)** yalnızca iyileşen adımı atar. **Tavlama
benzetimi (simulated annealing)** ise kötüleşen adımı da bazen kabul eder:
olasılığı `exp(−fark / sıcaklık)`. Başta sıcaklık yüksek, çukurlar arasında
gezilebilir; sıcaklık düştükçe yalnızca iyileşmeler kalır. Ad, metali yavaş
soğutarak kusursuz kristal elde eden tavlamadan geliyor.

```python
def f(x):
    return x * x / 10 + 10 * math.sin(x)


def hill_climb(x, step=0.1):
    while True:
        best = min((x - step, x + step), key=f)
        if f(best) >= f(x):
            return x                           # iki yan da kötü: dur
        x = best


def anneal(x, rng, temp=20.0, cooling=0.998, steps=3000):
    best = x
    for _ in range(steps):
        cand = x + rng.uniform(-3, 3)
        delta = f(cand) - f(x)
        if delta < 0 or rng.random() < math.exp(-delta / temp):
            x = cand                           # kötüyü de bazen kabul et
        if f(x) < f(best):
            best = x
        temp *= cooling
    return best


xs = [i / 100 for i in range(-3000, 3001)]
glob = min(xs, key=f)                          # ızgarada gerçek en iyi
print(round(glob, 2), round(f(glob), 2))
rng = random.Random(1)
starts = [rng.uniform(-30, 30) for _ in range(20)]
hc = [hill_climb(s) for s in starts]
an = [anneal(s, random.Random(i)) for i, s in enumerate(starts)]
found_hc = sum(abs(x - glob) < 0.5 for x in hc)
found_an = sum(abs(x - glob) < 0.5 for x in an)
print(found_hc, found_an)
```

```text
-1.54 -9.76
4 20
```

Aynı 20 başlangıç noktasından tepe tırmanma yalnızca 4 kez gerçek en iyiyi
buldu; kalanlarda başladığı çukurda kaldı. Tavlama benzetimi 20'de 20.

## Makine öğrenmesinde

- **Gradyan inişi** bir yerel aramadır: eğimin tersine küçük adımlar atar ve
  yerel en iyide takılabilir. Rastgele başlangıç, momentum ve öğrenme oranı
  takvimi (tavlamadaki sıcaklık gibi) bu yüzden var.
- **Hiperparametre araması:** ızgara araması kaba kuvvettir; rastgele arama ve
  Bayes optimizasyonu sezgiseldir.
- **Özellik seçimi:** ileri/geri seçim (bölüm 02'deki açgözlü yöntem) yerel
  aramadır.
- **K-ortalamalar** her çalıştırmada bir yerel en iyiye iner; scikit-learn bu
  yüzden birkaç rastgele başlangıç deneyip en iyisini tutar (`n_init`).

## Özet

- Olasılık sayısı patlayan problemlerde kaba kuvvet ancak küçük örnekte
  mümkün; sezgisel yöntemler iyi bir cevabı hızla bulur, en iyiyi garanti etmez.
- En yakın komşu: açgözlü kurulum, `O(n²)`.
- 2-opt: iki kenarı değiştirip parçayı ters çevirerek yerel iyileştirme.
- Yerel arama yerel en iyide takılabilir; tavlama benzetimi kötüleşen adımı
  azalan bir olasılıkla kabul ederek çukurdan çıkar.
