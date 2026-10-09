# math ve statistics

Hesap makinesinin yapabildiği her şey Python'da var: `+`, `-`, `*`, `/`,
`**`. Karekök, logaritma, kombinasyon, en büyük ortak bölen gibi işler için
**`math`**, ortalama, medyan, standart sapma, korelasyon gibi istatistikler için
**`statistics`** modülü kullanılır. İkisi de standart kütüphanede; küçük
verilerde NumPy'a gerek bırakmazlar. Bu bölümde önce ondalıklı sayıların bir
tuzağını, sonra iki modülün en çok kullanılan fonksiyonlarını görüyoruz.

## Ondalıklı sayılar tam değildir

Bilgisayar ondalıklı sayıları ikilik tabanda saklar; `0.1` gibi sayılar tam
olarak yazılamaz ve küçük hatalar birikir.

```python
import math

print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
total = 0.0
for value in [0.1] * 10:
    total += value
print(total, sum([0.1] * 10), math.fsum([0.1] * 10))
```

```text
0.30000000000000004 False
True
0.9999999999999999 1.0 1.0
```

`0.1 + 0.2` tam `0.3` değil; bu yüzden ondalıklı sayılar `==` ile değil
**`math.isclose`** ile karşılaştırılır. Döngüyle on kez `0.1` eklemek
`0.9999999999999999` veriyor: her toplamada küçük bir hata ekleniyor.
`math.fsum` hataları telafi ederek tam `1.0` buluyor; Python 3.12'den beri
yerleşik `sum()` da ondalıklı sayılarda aynı telafiyi yapıyor. Kendi
döngünle biriktiriyorsan hata büyür.

## Yuvarlamak

```python
import math

print(math.floor(-2.5), math.ceil(-2.5), math.trunc(-2.5))
print(round(2.5), round(3.5), round(2.675, 2))
```

```text
-3 -2 -2
2 4 2.67
```

`floor` aşağı (−3), `ceil` yukarı (−2), `trunc` sıfıra doğru (−2) yuvarlar;
negatif sayılarda fark görünür. Yerleşik `round` ise **bankacı yuvarlaması**
yapar: tam yarıda en yakın **çift** sayıya gider, bu yüzden `round(2.5)` 2,
`round(3.5)` 4. `round(2.675, 2)` 2.68 değil 2.67: `2.675` ikilik tabanda
biraz küçük saklanıyor. Para hesabı gibi kesin yuvarlama gereken yerde
`decimal` modülü kullanılır (İleri Python modülünde).

## Tam sayı hesapları

```python
import math

print(math.prod([1, 2, 3, 4]), math.factorial(5))
print(math.comb(10, 3), math.perm(10, 3))
print(math.gcd(24, 36), math.lcm(4, 6), math.isqrt(17))
```

```text
24 120
120 720
12 12 4
```

`prod` çarpım, `factorial` faktöriyel. `comb(10, 3)` on kişiden üç kişilik
**grup** seçmenin yolu (120), `perm(10, 3)` sıranın önemli olduğu dizilişlerin
sayısı (720). `gcd` en büyük ortak bölen, `lcm` en küçük ortak kat. `isqrt`
tam sayı karekökü (17'nin karekökünün tam kısmı 4); büyük sayılarda
`int(math.sqrt(n))`'den güvenilirdir, çünkü ondalığa geçmez.

## Logaritma, üs, uzaklık ve özel değerler

```python
import math

print(math.log(100, 10), math.log10(1000), math.log2(1024))
print(round(math.exp(1), 6), math.hypot(3, 4), math.dist((0, 0), (3, 4)))
print(math.inf > 10 ** 100, math.isnan(math.nan), math.nan == math.nan)
```

```text
2.0 3.0 10.0
2.718282 5.0 5.0
True True False
```

`log(x, taban)` her tabanda, `log10` ve `log2` kısa yazımlar; tabansız
`log(x)` doğal logaritmadır (e tabanı). `hypot` dik üçgenin hipotenüsü,
`dist` iki nokta arasındaki uzaklık. `math.inf` sonsuzdan büyük sayı yok
demek; `math.nan` "sayı değil" (not a number) ve **kendisine bile eşit
değil**: bir değerin `nan` olup olmadığına `math.isnan` ile bakılır.

## statistics: konum ve yayılma

```python
import statistics as st

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(st.mean(data), st.median(data), st.mode(data))
print(st.multimode([1, 1, 2, 2, 3]))
print(st.pstdev(data), round(st.stdev(data), 4))
print(st.quantiles(data, n=4))
```

```text
5 4.5 4
[1, 2]
2.0 2.1381
[4.0, 4.5, 6.5]
```

Ortalama 5, medyan 4,5 (çift sayıda değerde ortadaki ikisinin ortalaması),
en sık değer 4. Birden çok en sık değer varsa `multimode` hepsini verir.
İki standart sapma var: **`pstdev`** veriyi bütün kitle sayar ve `n`'ye böler
(2,0); **`stdev`** veriyi bir **örneklem** sayar ve `n − 1`'e böler (2,1381).
Elindeki veri daha büyük bir topluluktan alınmış bir parçaysa `stdev`
kullanılır. `quantiles(n=4)` veriyi dört eşit parçaya bölen üç kesim noktası:
çeyrekler (4,0, 4,5, 6,5).

## İlişki ve dağılım

```python
import statistics as st

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
print(round(st.correlation(x, y), 4))
print(st.linear_regression(x, y))
iq = st.NormalDist(mu=100, sigma=15)
print(round(iq.cdf(130), 4), round(iq.inv_cdf(0.975), 2))
```

```text
0.7746
LinearRegression(slope=0.6, intercept=2.2)
0.9772 129.4
```

`correlation` Pearson korelasyonu (0,7746: güçlü, artı yönde ilişki).
`linear_regression` en küçük kareler doğrusunun eğimini ve kesişimini verir:
`y ≈ 0.6 x + 2.2`. `NormalDist` bir normal dağılım nesnesi: ortalaması 100,
standart sapması 15 olan bir dağılımda 130'un altında kalma olasılığı
%97,72 (`cdf`), en alttaki %97,5'i ayıran değer 129,4 (`inv_cdf`).

## Özet

- Ondalıklı sayılar `math.isclose` ile karşılaştırılır; uzun toplamlarda
  `math.fsum` ya da `sum` (kendi döngünle `+=` hata biriktirir).
- `floor`, `ceil`, `trunc`; `round` bankacı yuvarlaması yapar.
- `prod`, `factorial`, `comb`, `perm`, `gcd`, `lcm`, `isqrt`; `log`,
  `exp`, `hypot`, `dist`; `inf` ve `nan` (`isnan`).
- `statistics`: `mean`, `median`, `mode`, `multimode`, `stdev` (örneklem)
  ile `pstdev` (kitle), `quantiles`, `correlation`, `linear_regression`,
  `NormalDist`.
