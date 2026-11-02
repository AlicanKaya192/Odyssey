# Olasılık Dağılımları

Mağazaya bugün 20 kişi gelecek. Kaçı alışveriş yapar? Kesin bir sayı
söyleyemezsin, ama "en olası 2", "5 ya da daha fazlası çok nadir" gibi
cümleler kurabilirsin. Bir sonucun **hangi değerleri hangi olasılıkla**
alabileceğini anlatan tabloya ya da formüle **olasılık dağılımı**
(probability distribution) denir.

Dağılımlar çıkarımın dilidir: bir sonraki bölümden itibaren "örneklem
ortalaması nasıl dağılır?" diye soracağız ve cevabı bir dağılımla
vereceğiz. Bu bölümde en sık kullanılan üç dağılımı tanıyıp onları
`scipy.stats` ile kullanacağız ve her birini evrenimizle karşılaştıracağız.

## Rastgele değişken

Sonucu şansa bağlı olan sayıya **rastgele değişken** (random variable)
denir: "20 ziyaretçiden alışveriş yapanların sayısı", "bir sayfanın açılış
süresi". İki tür var:

- **Kesikli** (discrete): sayılabilen değerler alır (0, 1, 2, ...). Kaç kişi
  aldı, kaç kez geldi.
- **Sürekli** (continuous): bir aralıktaki her değeri alabilir. Süre,
  ağırlık, sıcaklık.

## Binom dağılımı: n denemede kaç başarı?

Her ziyaretçi birbirinden bağımsız olarak $p$ olasılıkla alışveriş yapsın.
$n$ ziyaretçiden tam $k$'sının alışveriş yapma olasılığı **binom dağılımı**
(binomial distribution) ile verilir:

$$P(X = k) = \binom{n}{k}\, p^k (1-p)^{n-k}$$

$\binom{n}{k}$ "$n$ kişiden $k$ kişiyi seçmenin yolu sayısı". Elle
hesaplamaya gerek yok; `scipy.stats` yapıyor. Evrenimizde alışveriş
yapanların payı 0,114 idi:

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)
for k in range(6):
    print(k, round(float(buyers.pmf(k)), 3))
print(round(float(buyers.mean()), 2), round(float(buyers.std()), 2))
```

```text
0 0.089
1 0.229
2 0.279
3 0.216
4 0.118
5 0.049
2.28 1.42
```

- `pmf` (probability mass function, olasılık kütle fonksiyonu) tam `k`
  değerinin olasılığı. En olası sonuç 2 kişi
  (0,279).
- Beklenen değer $np = 20 \times 0{,}114 = 2{,}28$, standart sapma
  $\sqrt{np(1-p)} \approx 1{,}42$. Kod ikisini de aynı buldu.

Birikimli sorular için iki fonksiyon daha:

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)
print(round(float(buyers.cdf(1)), 3))
print(round(float(buyers.sf(4)), 3))
print(round(float(buyers.cdf(3) - buyers.cdf(1)), 3))
```

```text
0.318
0.069
0.495
```

- `cdf(k)` (cumulative distribution function, birikimli dağılım) "$k$ ya da
  **daha az**": en fazla 1 kişi alışveriş yapar: 0,318.
- `sf(k)` (survival function, 1 − cdf) "$k$'den **fazla**": 5 ya da daha
  fazla kişi için `sf(4)` yazılır, `sf(5)` değil: 0,069.
- "2 ile 3 arası (ikisi dahil)" = `cdf(3) - cdf(1)`: 0,495. Kesikli
  dağılımda sınırın dahil olup olmadığı sonucu değiştirir; en sık yapılan
  hata budur.

## Formül evreni tutuyor mu?

Binom dağılımı bir **modeldir**: kişilerin bağımsız ve aynı olasılıkla
davrandığını varsayar. Evrenimizden gerçekten 20'şer kişi çekip sayalım:

```python
import numpy as np
from ab_data import make_population

users = make_population()
bought = users["bought"].to_numpy()
rng = np.random.default_rng(3)
counts = []
for _ in range(10000):
    picked = rng.choice(len(bought), size=20, replace=False)
    counts.append(bought[picked].sum())
counts = np.array(counts)
for k in range(6):
    print(k, round(float((counts == k).mean()), 3))
```

```text
0 0.087
1 0.229
2 0.279
3 0.213
4 0.121
5 0.049
```

On bin tekrarda gözlenen paylar binom formülünün verdiğiyle en fazla üç
binde bir farkla örtüşüyor. Evrende kullanıcıların alışveriş olasılığı aslında
ziyaret sayısına göre değişiyor, ama rastgele çekilen 20 kişi için ortalama
olasılık yetiyor.

## Poisson dağılımı: bir zaman aralığında kaç olay?

Bir kullanıcının bir ayda kaç kez geldiği, bir saatte kaç sipariş düştüğü
gibi **sayımlar** için **Poisson dağılımı** kullanılır. Tek bir parametresi
var: ortalama sayı $\lambda$ ("lambda").

$$P(X = k) = \dfrac{\lambda^k e^{-\lambda}}{k!}$$

```python
from scipy import stats
from ab_data import make_population

users = make_population()
share = users["visits"].value_counts(normalize=True).sort_index()
model = stats.poisson(mu=users["visits"].mean())
for k in range(7):
    print(k, round(share[k], 3), round(float(model.pmf(k)), 3))
```

```text
0 0.051 0.05
1 0.148 0.149
2 0.223 0.224
3 0.226 0.224
4 0.168 0.168
5 0.102 0.101
6 0.049 0.05
```

- Ortadaki sütun gerçek paylar, sağdaki Poisson modelinin tahmini. Neredeyse
  aynı: ziyaret sayısı Poisson dağılımına uyuyor.
- Poisson'da ortalama ile varyans eşittir ($\lambda$). Gerçek sayımlarda
  varyans ortalamadan çok büyükse model uymaz; o zaman başka dağılım gerekir.

## Normal dağılım: çan eğrisi

Sürekli değişkenlerin en ünlü dağılımı **normal dağılım** (normal
distribution, Gauss dağılımı da denir): ortalamanın iki yanına simetrik
çan eğrisi. İki parametresi var: ortalama $\mu$ ve standart sapma $\sigma$.
Sayfa açılış süreleri bu biçimde:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x = users["load_ms"]
model = stats.norm(loc=x.mean(), scale=x.std())
print(round(float(model.sf(1000)), 4), round(float((x > 1000).mean()), 4))
print(round(float(model.cdf(900) - model.cdf(800)), 4))
print(round(float(((x > 800) & (x <= 900)).mean()), 4))
print(round(float(model.ppf(0.95)), 1), np.percentile(x, 95))
print(round(float(model.pdf(850)), 5))
```

```text
0.1058 0.1049
0.3224
0.3241
1047.6 1048.0
0.00332
```

- 1000 ms'den yavaş sayfa olasılığı: model 0,1058, gerçek
  0,1049.
- 800–900 ms arası: model 0,3224, gerçek 0,3241.
- `ppf(0.95)` (percent point function, cdf'nin tersi) "altında %95 kalan
  değer": model 1047,6, gerçek 95. yüzdelik 1048,0.
- `pdf(850)` (probability density function, olasılık yoğunluk fonksiyonu)
  0,00332 verdi. Bu bir olasılık **değil**, yoğunluk. Sürekli
  değişkende "tam 850,000... ms" olasılığı sıfırdır; olasılık her zaman bir
  **aralığın** alanıdır (`cdf(b) - cdf(a)`).

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="483.12pt" height="222.406437pt" viewBox="0 0 483.12 222.406437" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.406437 
L 483.12 222.406437 
L 483.12 0 
L 0 0 
L 0 222.406437 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 198.206437 
L 220.254545 198.206437 
L 220.254545 20.798437 
L 7.2 20.798437 
L 7.2 198.206437 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 16.884298 198.206437 
L 20.028466 198.206437 
L 20.028466 198.117339 
L 16.884298 198.117339 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_4">
    <path d="M 20.028466 198.206437 
L 23.172635 198.206437 
L 23.172635 198.117339 
L 20.028466 198.117339 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_5">
    <path d="M 23.172635 198.206437 
L 26.316803 198.206437 
L 26.316803 198.147039 
L 23.172635 198.147039 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_6">
    <path d="M 26.316803 198.206437 
L 29.460972 198.206437 
L 29.460972 197.998542 
L 26.316803 197.998542 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_7">
    <path d="M 29.460972 198.206437 
L 32.60514 198.206437 
L 32.60514 197.879744 
L 29.460972 197.879744 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_8">
    <path d="M 32.60514 198.206437 
L 35.749309 198.206437 
L 35.749309 197.731247 
L 32.60514 197.731247 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_9">
    <path d="M 35.749309 198.206437 
L 38.893478 198.206437 
L 38.893478 197.226357 
L 35.749309 197.226357 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_10">
    <path d="M 38.893478 198.206437 
L 42.037646 198.206437 
L 42.037646 196.959062 
L 38.893478 196.959062 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_11">
    <path d="M 42.037646 198.206437 
L 45.181815 198.206437 
L 45.181815 196.365073 
L 42.037646 196.365073 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_12">
    <path d="M 45.181815 198.206437 
L 48.325983 198.206437 
L 48.325983 195.563189 
L 45.181815 195.563189 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_13">
    <path d="M 48.325983 198.206437 
L 51.470152 198.206437 
L 51.470152 194.018819 
L 48.325983 194.018819 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_14">
    <path d="M 51.470152 198.206437 
L 54.614321 198.206437 
L 54.614321 193.721825 
L 51.470152 193.721825 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_15">
    <path d="M 54.614321 198.206437 
L 57.758489 198.206437 
L 57.758489 189.653005 
L 54.614321 189.653005 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_16">
    <path d="M 57.758489 198.206437 
L 60.902658 198.206437 
L 60.902658 187.247352 
L 57.758489 187.247352 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_17">
    <path d="M 60.902658 198.206437 
L 64.046826 198.206437 
L 64.046826 183.445826 
L 60.902658 183.445826 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_18">
    <path d="M 64.046826 198.206437 
L 67.190995 198.206437 
L 67.190995 179.614601 
L 64.046826 179.614601 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_19">
    <path d="M 67.190995 198.206437 
L 70.335164 198.206437 
L 70.335164 174.595399 
L 67.190995 174.595399 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_20">
    <path d="M 70.335164 198.206437 
L 73.479332 198.206437 
L 73.479332 166.131064 
L 70.335164 166.131064 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_21">
    <path d="M 73.479332 198.206437 
L 76.623501 198.206437 
L 76.623501 158.171619 
L 73.479332 158.171619 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_22">
    <path d="M 76.623501 198.206437 
L 79.767669 198.206437 
L 79.767669 147.776822 
L 76.623501 147.776822 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_23">
    <path d="M 79.767669 198.206437 
L 82.911838 198.206437 
L 82.911838 138.896696 
L 79.767669 138.896696 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_24">
    <path d="M 82.911838 198.206437 
L 86.056007 198.206437 
L 86.056007 123.809391 
L 82.911838 123.809391 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_25">
    <path d="M 86.056007 198.206437 
L 89.200175 198.206437 
L 89.200175 114.038281 
L 86.056007 114.038281 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_26">
    <path d="M 89.200175 198.206437 
L 92.344344 198.206437 
L 92.344344 98.475785 
L 89.200175 98.475785 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_27">
    <path d="M 92.344344 198.206437 
L 95.488512 198.206437 
L 95.488512 87.724595 
L 92.344344 87.724595 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_28">
    <path d="M 95.488512 198.206437 
L 98.632681 198.206437 
L 98.632681 70.291036 
L 95.488512 70.291036 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_29">
    <path d="M 98.632681 198.206437 
L 101.77685 198.206437 
L 101.77685 65.776724 
L 98.632681 65.776724 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_30">
    <path d="M 101.77685 198.206437 
L 104.921018 198.206437 
L 104.921018 55.471025 
L 101.77685 55.471025 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_31">
    <path d="M 104.921018 198.206437 
L 108.065187 198.206437 
L 108.065187 48.04617 
L 104.921018 48.04617 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_32">
    <path d="M 108.065187 198.206437 
L 111.209355 198.206437 
L 111.209355 41.601396 
L 108.065187 41.601396 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_33">
    <path d="M 111.209355 198.206437 
L 114.353524 198.206437 
L 114.353524 29.246437 
L 111.209355 29.246437 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_34">
    <path d="M 114.353524 198.206437 
L 117.497693 198.206437 
L 117.497693 42.997269 
L 114.353524 42.997269 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_35">
    <path d="M 117.497693 198.206437 
L 120.641861 198.206437 
L 120.641861 43.413061 
L 117.497693 43.413061 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_36">
    <path d="M 120.641861 198.206437 
L 123.78603 198.206437 
L 123.78603 48.877754 
L 120.641861 48.877754 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_37">
    <path d="M 123.78603 198.206437 
L 126.930198 198.206437 
L 126.930198 51.253708 
L 123.78603 51.253708 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_38">
    <path d="M 126.930198 198.206437 
L 130.074367 198.206437 
L 130.074367 69.459452 
L 126.930198 69.459452 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_39">
    <path d="M 130.074367 198.206437 
L 133.218536 198.206437 
L 133.218536 82.081706 
L 130.074367 82.081706 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_40">
    <path d="M 133.218536 198.206437 
L 136.362704 198.206437 
L 136.362704 95.416745 
L 133.218536 95.416745 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_41">
    <path d="M 136.362704 198.206437 
L 139.506873 198.206437 
L 139.506873 97.466005 
L 136.362704 97.466005 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_42">
    <path d="M 139.506873 198.206437 
L 142.651041 198.206437 
L 142.651041 121.166142 
L 139.506873 121.166142 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_43">
    <path d="M 142.651041 198.206437 
L 145.79521 198.206437 
L 145.79521 133.5805 
L 142.651041 133.5805 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_44">
    <path d="M 145.79521 198.206437 
L 148.939379 198.206437 
L 148.939379 141.629043 
L 145.79521 141.629043 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_45">
    <path d="M 148.939379 198.206437 
L 152.083547 198.206437 
L 152.083547 150.44977 
L 148.939379 150.44977 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_46">
    <path d="M 152.083547 198.206437 
L 155.227716 198.206437 
L 155.227716 161.676151 
L 152.083547 161.676151 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_47">
    <path d="M 155.227716 198.206437 
L 158.371884 198.206437 
L 158.371884 169.694994 
L 155.227716 169.694994 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_48">
    <path d="M 158.371884 198.206437 
L 161.516053 198.206437 
L 161.516053 175.426982 
L 158.371884 175.426982 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_49">
    <path d="M 161.516053 198.206437 
L 164.660221 198.206437 
L 164.660221 181.485664 
L 161.516053 181.485664 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_50">
    <path d="M 164.660221 198.206437 
L 167.80439 198.206437 
L 167.80439 185.346589 
L 164.660221 185.346589 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_51">
    <path d="M 167.80439 198.206437 
L 170.948559 198.206437 
L 170.948559 189.593606 
L 167.80439 189.593606 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_52">
    <path d="M 170.948559 198.206437 
L 174.092727 198.206437 
L 174.092727 191.583467 
L 170.948559 191.583467 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_53">
    <path d="M 174.092727 198.206437 
L 177.236896 198.206437 
L 177.236896 193.98912 
L 174.092727 193.98912 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_54">
    <path d="M 177.236896 198.206437 
L 180.381064 198.206437 
L 180.381064 195.117698 
L 177.236896 195.117698 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_55">
    <path d="M 180.381064 198.206437 
L 183.525233 198.206437 
L 183.525233 195.53349 
L 180.381064 195.53349 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_56">
    <path d="M 183.525233 198.206437 
L 186.669402 198.206437 
L 186.669402 196.602669 
L 183.525233 196.602669 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_57">
    <path d="M 186.669402 198.206437 
L 189.81357 198.206437 
L 189.81357 197.04816 
L 186.669402 197.04816 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_58">
    <path d="M 189.81357 198.206437 
L 192.957739 198.206437 
L 192.957739 197.612449 
L 189.81357 197.612449 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_59">
    <path d="M 192.957739 198.206437 
L 196.101907 198.206437 
L 196.101907 197.939143 
L 192.957739 197.939143 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_60">
    <path d="M 196.101907 198.206437 
L 199.246076 198.206437 
L 199.246076 197.998542 
L 196.101907 197.998542 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_61">
    <path d="M 199.246076 198.206437 
L 202.390245 198.206437 
L 202.390245 198.05794 
L 199.246076 198.05794 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_62">
    <path d="M 202.390245 198.206437 
L 205.534413 198.206437 
L 205.534413 198.08764 
L 202.390245 198.08764 
z
" clip-path="url(#p6ca38a0ba4)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="26.568595" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="26.568595" y="212.804094" transform="rotate(-0 26.568595 212.804094)">400</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="65.305785" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="65.305785" y="212.804094" transform="rotate(-0 65.305785 212.804094)">600</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="104.042975" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="104.042975" y="212.804094" transform="rotate(-0 104.042975 212.804094)">800</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="142.780165" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="142.780165" y="212.804094" transform="rotate(-0 142.780165 212.804094)">1000</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="181.517355" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="181.517355" y="212.804094" transform="rotate(-0 181.517355 212.804094)">1200</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="220.254545" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="220.254545" y="212.804094" transform="rotate(-0 220.254545 212.804094)">1400</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_7">
    <path d="M 16.884298 198.177981 
L 28.544321 198.005443 
L 34.374333 197.720174 
L 38.908787 197.280705 
L 42.147682 196.773811 
L 45.386578 196.031816 
L 47.977694 195.211841 
L 50.568811 194.133398 
L 52.512148 193.118086 
L 54.455485 191.893773 
L 56.398823 190.429202 
L 58.34216 188.691305 
L 60.285497 186.645808 
L 62.228834 184.258013 
L 64.172172 181.493766 
L 66.115509 178.320613 
L 68.058846 174.709115 
L 70.002184 170.634316 
L 71.945521 166.077303 
L 73.888858 161.026821 
L 75.832195 155.480873 
L 78.423312 147.332428 
L 81.014428 138.374928 
L 84.253324 126.192753 
L 88.139998 110.52394 
L 96.561127 76.117446 
L 99.152243 66.535064 
L 101.09558 59.984902 
L 103.038918 54.115357 
L 104.982255 49.03849 
L 106.277813 46.144086 
L 107.573371 43.67233 
L 108.868929 41.645486 
L 110.164488 40.081992 
L 111.460046 38.996181 
L 112.755604 38.398066 
L 113.403383 38.283802 
L 114.051162 38.293181 
L 114.698941 38.426182 
L 115.34672 38.682496 
L 116.642279 39.562408 
L 117.937837 40.924788 
L 119.233395 42.757114 
L 120.528953 45.042657 
L 121.824511 47.760738 
L 123.12007 50.887039 
L 125.063407 56.28074 
L 127.006744 62.425384 
L 129.597861 71.584887 
L 132.836756 84.172064 
L 138.018989 105.56297 
L 142.553443 124.034867 
L 145.792338 136.379588 
L 148.383454 145.497665 
L 150.974571 153.823656 
L 153.565687 161.294064 
L 155.509025 166.319466 
L 157.452362 170.851759 
L 159.395699 174.902625 
L 161.339036 178.49132 
L 163.282374 181.643063 
L 165.225711 184.38748 
L 167.169048 186.757141 
L 169.112386 188.786255 
L 171.055723 190.509519 
L 172.99906 191.961164 
L 174.942398 193.174177 
L 176.885735 194.179714 
L 179.476851 195.247283 
L 182.067968 196.058561 
L 185.306863 196.79226 
L 188.545759 197.293163 
L 192.432433 197.679651 
L 197.614666 197.964222 
L 205.388015 198.137612 
L 210.570248 198.178475 
L 210.570248 198.178475 
" clip-path="url(#p6ca38a0ba4)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_63">
    <path d="M 7.2 198.206437 
L 7.2 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_64">
    <path d="M 220.254545 198.206437 
L 220.254545 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_65">
    <path d="M 7.2 198.206437 
L 220.254545 198.206437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_66">
    <path d="M 7.2 20.798437 
L 220.254545 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_7">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="14.798437" transform="rotate(-0 113.727273 14.798437)">Sayfa açılış süresi (ms)</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_67">
    <path d="M 262.865455 198.206437 
L 475.92 198.206437 
L 475.92 20.798437 
L 262.865455 20.798437 
L 262.865455 198.206437 
z
" style="fill: none"/>
   </g>
   <g id="patch_68">
    <path d="M 275.212934 198.206437 
L 278.395033 198.206437 
L 278.395033 194.698702 
L 275.212934 194.698702 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_69">
    <path d="M 278.395033 198.206437 
L 281.577131 198.206437 
L 281.577131 173.75041 
L 278.395033 173.75041 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_70">
    <path d="M 281.577131 198.206437 
L 284.75923 198.206437 
L 284.75923 132.78595 
L 281.577131 132.78595 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_71">
    <path d="M 284.75923 198.206437 
L 287.941329 198.206437 
L 287.941329 91.968667 
L 284.75923 91.968667 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_72">
    <path d="M 287.941329 198.206437 
L 291.123428 198.206437 
L 291.123428 59.344277 
L 287.941329 59.344277 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_73">
    <path d="M 291.123428 198.206437 
L 294.305526 198.206437 
L 294.305526 38.273336 
L 291.123428 38.273336 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_74">
    <path d="M 294.305526 198.206437 
L 297.487625 198.206437 
L 297.487625 29.246437 
L 294.305526 29.246437 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_75">
    <path d="M 297.487625 198.206437 
L 300.669724 198.206437 
L 300.669724 33.612709 
L 297.487625 33.612709 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_76">
    <path d="M 300.669724 198.206437 
L 303.851823 198.206437 
L 303.851823 33.980654 
L 300.669724 33.980654 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_77">
    <path d="M 303.851823 198.206437 
L 307.033921 198.206437 
L 307.033921 47.177587 
L 303.851823 47.177587 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_78">
    <path d="M 307.033921 198.206437 
L 310.21602 198.206437 
L 310.21602 57.798911 
L 307.033921 57.798911 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_79">
    <path d="M 310.21602 198.206437 
L 313.398119 198.206437 
L 313.398119 69.548598 
L 310.21602 69.548598 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_80">
    <path d="M 313.398119 198.206437 
L 316.580218 198.206437 
L 316.580218 83.236124 
L 313.398119 83.236124 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_81">
    <path d="M 316.580218 198.206437 
L 319.762317 198.206437 
L 319.762317 94.421629 
L 316.580218 94.421629 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_82">
    <path d="M 319.762317 198.206437 
L 322.944415 198.206437 
L 322.944415 106.073197 
L 319.762317 106.073197 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_83">
    <path d="M 322.944415 198.206437 
L 326.126514 198.206437 
L 326.126514 117.013406 
L 322.944415 117.013406 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_84">
    <path d="M 326.126514 198.206437 
L 329.308613 198.206437 
L 329.308613 124.543998 
L 326.126514 124.543998 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_85">
    <path d="M 329.308613 198.206437 
L 332.490712 198.206437 
L 332.490712 133.644486 
L 329.308613 133.644486 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_86">
    <path d="M 332.490712 198.206437 
L 335.67281 198.206437 
L 335.67281 140.292012 
L 332.490712 140.292012 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_87">
    <path d="M 335.67281 198.206437 
L 338.854909 198.206437 
L 338.854909 147.332012 
L 335.67281 147.332012 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_88">
    <path d="M 338.854909 198.206437 
L 342.037008 198.206437 
L 342.037008 153.685183 
L 338.854909 153.685183 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_89">
    <path d="M 342.037008 198.206437 
L 345.219107 198.206437 
L 345.219107 160.627065 
L 342.037008 160.627065 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_90">
    <path d="M 345.219107 198.206437 
L 348.401205 198.206437 
L 348.401205 163.619678 
L 345.219107 163.619678 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_91">
    <path d="M 348.401205 198.206437 
L 351.583304 198.206437 
L 351.583304 167.642535 
L 348.401205 167.642535 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_92">
    <path d="M 351.583304 198.206437 
L 354.765403 198.206437 
L 354.765403 170.708737 
L 351.583304 170.708737 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_93">
    <path d="M 354.765403 198.206437 
L 357.947502 198.206437 
L 357.947502 174.290061 
L 354.765403 174.290061 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_94">
    <path d="M 357.947502 198.206437 
L 361.1296 198.206437 
L 361.1296 175.909016 
L 357.947502 175.909016 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_95">
    <path d="M 361.1296 198.206437 
L 364.311699 198.206437 
L 364.311699 179.735636 
L 361.1296 179.735636 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_96">
    <path d="M 364.311699 198.206437 
L 367.493798 198.206437 
L 367.493798 181.845183 
L 364.311699 181.845183 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_97">
    <path d="M 367.493798 198.206437 
L 370.675897 198.206437 
L 370.675897 183.34149 
L 367.493798 183.34149 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_98">
    <path d="M 370.675897 198.206437 
L 373.857995 198.206437 
L 373.857995 186.088807 
L 370.675897 186.088807 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_99">
    <path d="M 373.857995 198.206437 
L 377.040094 198.206437 
L 377.040094 187.511525 
L 373.857995 187.511525 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_100">
    <path d="M 377.040094 198.206437 
L 380.222193 198.206437 
L 380.222193 187.80588 
L 377.040094 187.80588 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_101">
    <path d="M 380.222193 198.206437 
L 383.404292 198.206437 
L 383.404292 189.351246 
L 380.222193 189.351246 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_102">
    <path d="M 383.404292 198.206437 
L 386.58639 198.206437 
L 386.58639 190.136194 
L 383.404292 190.136194 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_103">
    <path d="M 386.58639 198.206437 
L 389.768489 198.206437 
L 389.768489 190.921141 
L 386.58639 190.921141 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_104">
    <path d="M 389.768489 198.206437 
L 392.950588 198.206437 
L 392.950588 190.99473 
L 389.768489 190.99473 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_105">
    <path d="M 392.950588 198.206437 
L 396.132687 198.206437 
L 396.132687 192.024974 
L 392.950588 192.024974 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_106">
    <path d="M 396.132687 198.206437 
L 399.314786 198.206437 
L 399.314786 193.643929 
L 396.132687 193.643929 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_107">
    <path d="M 399.314786 198.206437 
L 402.496884 198.206437 
L 402.496884 193.447692 
L 399.314786 193.447692 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_108">
    <path d="M 402.496884 198.206437 
L 405.678983 198.206437 
L 405.678983 194.20811 
L 402.496884 194.20811 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_109">
    <path d="M 405.678983 198.206437 
L 408.861082 198.206437 
L 408.861082 194.551525 
L 405.678983 194.551525 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_110">
    <path d="M 408.861082 198.206437 
L 412.043181 198.206437 
L 412.043181 194.576054 
L 408.861082 194.576054 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_111">
    <path d="M 412.043181 198.206437 
L 415.225279 198.206437 
L 415.225279 195.042117 
L 412.043181 195.042117 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_112">
    <path d="M 415.225279 198.206437 
L 418.407378 198.206437 
L 418.407378 195.655357 
L 415.225279 195.655357 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_113">
    <path d="M 418.407378 198.206437 
L 421.589477 198.206437 
L 421.589477 196.023302 
L 418.407378 196.023302 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_114">
    <path d="M 421.589477 198.206437 
L 424.771576 198.206437 
L 424.771576 196.09689 
L 421.589477 196.09689 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_115">
    <path d="M 424.771576 198.206437 
L 427.953674 198.206437 
L 427.953674 196.09689 
L 424.771576 196.09689 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_116">
    <path d="M 427.953674 198.206437 
L 431.135773 198.206437 
L 431.135773 196.219539 
L 427.953674 196.219539 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_117">
    <path d="M 431.135773 198.206437 
L 434.317872 198.206437 
L 434.317872 196.317657 
L 431.135773 196.317657 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_118">
    <path d="M 434.317872 198.206437 
L 437.499971 198.206437 
L 437.499971 196.587483 
L 434.317872 196.587483 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_119">
    <path d="M 437.499971 198.206437 
L 440.682069 198.206437 
L 440.682069 196.513894 
L 437.499971 196.513894 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_120">
    <path d="M 440.682069 198.206437 
L 443.864168 198.206437 
L 443.864168 197.004486 
L 440.682069 197.004486 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_121">
    <path d="M 443.864168 198.206437 
L 447.046267 198.206437 
L 447.046267 197.200723 
L 443.864168 197.200723 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_122">
    <path d="M 447.046267 198.206437 
L 450.228366 198.206437 
L 450.228366 197.225253 
L 447.046267 197.225253 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_123">
    <path d="M 450.228366 198.206437 
L 453.410464 198.206437 
L 453.410464 197.127134 
L 450.228366 197.127134 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_124">
    <path d="M 453.410464 198.206437 
L 456.592563 198.206437 
L 456.592563 197.102605 
L 453.410464 197.102605 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_125">
    <path d="M 456.592563 198.206437 
L 459.774662 198.206437 
L 459.774662 197.078075 
L 456.592563 197.078075 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_126">
    <path d="M 459.774662 198.206437 
L 462.956761 198.206437 
L 462.956761 197.39696 
L 459.774662 197.39696 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_127">
    <path d="M 462.956761 198.206437 
L 466.13886 198.206437 
L 466.13886 197.372431 
L 462.956761 197.372431 
z
" clip-path="url(#pb878fdf511)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_7">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="272.549752" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="272.549752" y="212.804094" transform="rotate(-0 272.549752 212.804094)">0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="320.97124" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="320.97124" y="212.804094" transform="rotate(-0 320.97124 212.804094)">10</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="369.392727" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="212.804094" transform="rotate(-0 369.392727 212.804094)">20</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="417.814215" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="417.814215" y="212.804094" transform="rotate(-0 417.814215 212.804094)">30</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="466.235702" y="198.206437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="466.235702" y="212.804094" transform="rotate(-0 466.235702 212.804094)">40</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_13">
    <path d="M 272.549752 162.996819 
L 275.788648 157.087738 
L 279.675322 149.446708 
L 284.209776 139.996027 
L 293.926462 119.554033 
L 297.165358 113.301818 
L 299.756474 108.715231 
L 302.347591 104.597558 
L 304.290928 101.868838 
L 306.234265 99.485019 
L 308.177602 97.475296 
L 310.12094 95.864669 
L 311.416498 95.022861 
L 312.712056 94.372303 
L 314.007614 93.916687 
L 315.303173 93.658609 
L 316.598731 93.599541 
L 317.894289 93.739822 
L 319.189847 94.07865 
L 320.485405 94.614092 
L 321.780964 95.343102 
L 323.076522 96.26155 
L 325.019859 97.982826 
L 326.963196 100.096852 
L 328.906534 102.577434 
L 330.849871 105.394333 
L 333.440987 109.614755 
L 336.032104 114.285772 
L 339.270999 120.616416 
L 343.805453 130.063218 
L 353.522139 150.514746 
L 357.408814 158.082058 
L 360.647709 163.914933 
L 363.886605 169.247062 
L 366.477721 173.125435 
L 369.068838 176.649441 
L 371.659954 179.819084 
L 374.251071 182.641842 
L 376.842187 185.131365 
L 379.433303 187.306149 
L 382.02442 189.188244 
L 384.615536 190.802057 
L 387.206652 192.173268 
L 389.797769 193.327896 
L 393.036664 194.505493 
L 396.27556 195.432099 
L 400.162234 196.273828 
L 404.048909 196.883084 
L 408.583363 197.373952 
L 414.413375 197.763178 
L 422.186724 198.026296 
L 433.846748 198.165403 
L 462.349028 198.205862 
L 466.235702 198.206138 
L 466.235702 198.206138 
" clip-path="url(#pb878fdf511)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_128">
    <path d="M 262.865455 198.206437 
L 262.865455 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_129">
    <path d="M 475.92 198.206437 
L 475.92 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_130">
    <path d="M 262.865455 198.206437 
L 475.92 198.206437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_131">
    <path d="M 262.865455 20.798437 
L 475.92 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_13">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="14.798437" transform="rotate(-0 369.392727 14.798437)">Oturum süresi (dakika)</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6ca38a0ba4">
   <rect x="7.2" y="20.798437" width="213.054545" height="177.408"/>
  </clipPath>
  <clipPath id="pb878fdf511">
   <rect x="262.865455" y="20.798437" width="213.054545" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Mor histogram gerçek veri, turuncu eğri aynı ortalama ve sapmalı normal dağılım. Açılış süresine oturuyor; oturum süresinde tepeyi kaçırıyor ve sıfırın soluna taşıyor.</figcaption>
</figure>

## 68–95–99,7 kuralı

Normal dağılımda ortalamadan 1, 2 ve 3 standart sapma içine düşen paylar
hep aynıdır. `stats.norm()` parametresiz yazılınca ortalaması 0, sapması 1
olan **standart normal** dağılımı kurar; z puanlarının dağılımı budur.

```python
from scipy import stats
from ab_data import make_population

users = make_population()
x = users["load_ms"]
for k in [1, 2, 3]:
    model = float(stats.norm.cdf(k) - stats.norm.cdf(-k))
    real = float(((x - x.mean()).abs() <= k * x.std()).mean())
    print(k, round(model, 4), round(real, 4))
```

```text
1 0.6827 0.6838
2 0.9545 0.9542
3 0.9973 0.9971
```

Yaklaşık %68, %95 ve %99,7. Önceki bölümde z puanı 2'yi aşanların payının
yaklaşık %5 çıkmasının sebebi buydu. Bu sayıları ezberlemeye değer:
güven aralığındaki "1,96" bu tablodan geliyor.

## Model veriye uymazsa

Normal dağılım her şeye uymaz. Oturum süresi gibi sağa çarpık bir değişkene
aynı modeli kurmayı deneyelim:

```python
from scipy import stats
from ab_data import make_population

users = make_population()
m = users["minutes"]
model = stats.norm(loc=m.mean(), scale=m.std())
print(round(float(model.cdf(0)), 3))
limit = m.mean() + 2 * m.std()
print(round(float(model.sf(limit)), 3), round(float((m > limit).mean()), 3))
```

```text
0.07
0.023 0.044
```

- Model, **sıfırdan kısa** oturumların payını %7,0 olarak tahmin
  ediyor: imkânsız bir sonuç.
- Ortalamanın 2 sapma üstündeki uzun oturumlar için model %2,3
  diyor, gerçekte %4,4: kuyruğu yaklaşık iki kat küçük tahmin
  ediyor.
- Ders: bir dağılımı kullanmadan önce verinin **biçimine** bak (histogram).
  Uymayan bir model hesabı hatasız yapar ama yanlış cevap verir.

## Özet

| Dağılım | Ne için | scipy | Parametreler |
|---|---|---|---|
| Binom | $n$ denemede başarı sayısı | `stats.binom(n, p)` | $n$, $p$ |
| Poisson | aralıktaki olay sayısı | `stats.poisson(mu)` | $\lambda$ |
| Normal | simetrik sürekli ölçüm | `stats.norm(loc, scale)` | $\mu$, $\sigma$ |

- `pmf` / `pdf`: tek değerin olasılığı / yoğunluğu; `cdf`: o değer ya da
  azı; `sf`: ondan fazlası; `ppf`: verilen payın sınır değeri.
- Kesikli dağılımda "en az 5" = `sf(4)`.
- Model bir varsayımdır; önce verinin biçimiyle karşılaştır.
