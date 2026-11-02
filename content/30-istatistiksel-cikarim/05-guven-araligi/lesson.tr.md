# Güven Aralığı

Önceki bölümde tek örneklemden bir tahmin ve onun standart hatasını
hesapladık: "ortalama 8,38, standart hata 0,486". Okuyan biri bunu tek
cümleyle anlamak ister: "Gerçek ortalama büyük olasılıkla **şu ile şu
arasında**." Bu cümlenin istatistikteki adı **güven aralığı** (confidence
interval). Hem tahmini hem belirsizliği tek satırda verdiği için çoğu
zaman tek başına bir p değerinden daha çok şey anlatır.

## Fikir: tahmin ± birkaç standart hata

Merkezi limit teoremi örneklem ortalamasının gerçeğin çevresinde çan
biçiminde dağıldığını söyledi. Normal dağılımda değerlerin %95'i ortalamanın
1,96 standart sapma yakınındadır. O hâlde örneklem ortalamalarının %95'i de
gerçeğin 1,96 standart hata yakınına düşer. Tersinden: tahminin çevresine
1,96 standart hatalık bir pay koyarsak, bu aralık örneklemlerin %95'inde
gerçeği yakalar.

Bir pürüz var: standart hatayı $\sigma$ ile değil, örneklemden gelen $s$ ile
hesaplıyoruz ve $s$ de oynuyor. Bunu hesaba katmak için 1,96 yerine biraz
daha büyük bir çarpan kullanılır. Bu çarpan **t dağılımından** (Student t
distribution) gelir. t dağılımı normale benzer ama kuyrukları daha kalındır;
ne kadar kalın olduğu **serbestlik derecesine** (degrees of freedom) bağlıdır,
ortalama için $n - 1$.

$$\bar{x} \pm t_{0{,}975;\,n-1} \cdot \dfrac{s}{\sqrt{n}}$$

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x = users.sample(n=100, random_state=21)["minutes"]
mean, se = x.mean(), x.std() / np.sqrt(len(x))
t_crit = stats.t.ppf(0.975, df=len(x) - 1)
print(round(t_crit, 3), round(stats.norm.ppf(0.975), 3))
print(round(mean - t_crit * se, 2), round(mean + t_crit * se, 2))
ci = stats.t.interval(0.95, df=len(x) - 1, loc=mean, scale=se)
print([round(float(v), 2) for v in ci])
```

```text
1.984 1.96
7.42 9.35
[7.42, 9.35]
```

- 99 serbestlik derecesinde t çarpanı 1,984, normalinki
  1,96: 100 kişide fark küçük.
- %95 güven aralığı 7,42 ile 9,35 dakika. `stats.t.interval`
  aynı hesabı tek satırda yapıyor.
- Gerçek ortalama (9,04) aralığın içinde. Ama gerçek hayatta bunu
  bilemeyiz; o zaman "%95" neye güveniyor?

## "%95" neyin %95'i?

Güven aralığı bir **yöntemdir**. "%95" yöntemin uzun vadeli başarı oranıdır:
bu yöntemi binlerce örneklemde kullanırsan aralıkların yaklaşık %95'i gerçeği
yakalar. Ölçelim:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x_all = users["minutes"].to_numpy()
true_mean = x_all.mean()
rng = np.random.default_rng(41)
samples = rng.choice(x_all, size=(4000, 100))
means = samples.mean(axis=1)
ses = samples.std(axis=1, ddof=1) / np.sqrt(100)
for level in [0.90, 0.95, 0.99]:
    t = stats.t.ppf((1 + level) / 2, df=99)
    hit = np.abs(means - true_mean) <= t * ses
    print(level, round(hit.mean(), 3))
```

```text
0.9 0.895
0.95 0.947
0.99 0.988
```

Bu orana **kapsama oranı** (coverage) denir. %90, %95 ve %99'luk aralıklar
gerçeği sırasıyla %89,5, %94,7 ve %98,8 oranında
yakaladı: söz verdiklerine çok yakın. Oturum süresi çarpık olduğu için
binde birkaç eksik kalıyorlar.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="405pt" height="278.248781pt" viewBox="0 0 405 278.248781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 278.248781 
L 405 278.248781 
L 405 0 
L 0 0 
L 0 278.248781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 240.048 
L 397.8 240.048 
L 397.8 7.2 
L 7.2 7.2 
L 7.2 240.048 
z
" style="fill: none"/>
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
       <use xlink:href="#m15aed4d867" x="74.168763" y="240.048" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="74.168763" y="254.645656" transform="rotate(-0 74.168763 254.645656)">6</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="146.975445" y="240.048" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="146.975445" y="254.645656" transform="rotate(-0 146.975445 254.645656)">8</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="219.782126" y="240.048" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="219.782126" y="254.645656" transform="rotate(-0 219.782126 254.645656)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="292.588808" y="240.048" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="292.588808" y="254.645656" transform="rotate(-0 292.588808 254.645656)">12</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="365.395489" y="240.048" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="365.395489" y="254.645656" transform="rotate(-0 365.395489 254.645656)">14</text>
     </g>
    </g>
    <g id="text_6">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="268.646438" transform="rotate(-0 202.5 268.646438)">Oturum süresi (dakika)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_6">
    <path d="M 104.232943 229.464 
L 291.720108 229.464 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_7">
    <defs>
     <path id="mc223a7361e" d="M 0 1.25 
C 0.331504 1.25 0.649475 1.118292 0.883883 0.883883 
C 1.118292 0.649475 1.25 0.331504 1.25 0 
C 1.25 -0.331504 1.118292 -0.649475 0.883883 -0.883883 
C 0.649475 -1.118292 0.331504 -1.25 0 -1.25 
C -0.331504 -1.25 -0.649475 -1.118292 -0.883883 -0.883883 
C -1.118292 -0.649475 -1.25 -0.331504 -1.25 0 
C -1.25 0.331504 -1.118292 0.649475 -0.883883 0.883883 
C -0.649475 1.118292 -0.331504 1.25 0 1.25 
z
" style="stroke: currentColor"/>
    </defs>
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="197.976525" y="229.464" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_8">
    <path d="M 91.090477 225.144 
L 228.682515 225.144 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_9">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="159.886496" y="225.144" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_10">
    <path d="M 108.697053 220.824 
L 253.449428 220.824 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_11">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="181.073241" y="220.824" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 54.987541 216.504 
L 202.07463 216.504 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_13">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="128.531086" y="216.504" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 84.107778 212.184 
L 218.264418 212.184 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_15">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="151.186098" y="212.184" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 148.717901 207.864 
L 328.414599 207.864 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_17">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="238.56625" y="207.864" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_18">
    <path d="M 72.068647 203.544 
L 198.778256 203.544 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_19">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="135.423451" y="203.544" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_20">
    <path d="M 107.376775 199.224 
L 279.208483 199.224 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_21">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="193.292629" y="199.224" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_22">
    <path d="M 95.723639 194.904 
L 219.559609 194.904 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_23">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="157.641624" y="194.904" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_24">
    <path d="M 112.363853 190.584 
L 238.473324 190.584 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_25">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="175.418588" y="190.584" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_26">
    <path d="M 88.063827 186.264 
L 189.165795 186.264 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_27">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="138.614811" y="186.264" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_28">
    <path d="M 106.704666 181.944 
L 218.48029 181.944 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_29">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="162.592478" y="181.944" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_30">
    <path d="M 72.105059 177.624 
L 223.932956 177.624 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_31">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="148.019007" y="177.624" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_32">
    <path d="M 129.482776 173.304 
L 290.132446 173.304 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_33">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="209.807611" y="173.304" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_34">
    <path d="M 74.124911 168.984 
L 305.276754 168.984 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_35">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="189.700832" y="168.984" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_36">
    <path d="M 87.774132 164.664 
L 306.334483 164.664 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_37">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="197.054307" y="164.664" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_38">
    <path d="M 163.809983 160.344 
L 319.341203 160.344 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_39">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="241.575593" y="160.344" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_40">
    <path d="M 24.954545 156.024 
L 291.590684 156.024 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_41">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="158.272615" y="156.024" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_42">
    <path d="M 136.005275 151.704 
L 318.969725 151.704 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_43">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="227.4875" y="151.704" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_44">
    <path d="M 73.200474 147.384 
L 218.711829 147.384 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_45">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="145.956151" y="147.384" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_46">
    <path d="M 118.937601 143.064 
L 267.040935 143.064 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_47">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="192.989268" y="143.064" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_48">
    <path d="M 112.944666 138.744 
L 298.297787 138.744 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_49">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="205.621227" y="138.744" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_50">
    <path d="M 122.133883 134.424 
L 275.396646 134.424 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_51">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="198.765264" y="134.424" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_52">
    <path d="M 63.801554 130.104 
L 323.123468 130.104 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_53">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="193.462511" y="130.104" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_54">
    <path d="M 72.944169 125.784 
L 199.480212 125.784 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_55">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="136.21219" y="125.784" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_56">
    <path d="M 82.48715 121.464 
L 176.929104 121.464 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #f97316; stroke-width: 3; stroke-linecap: square"/>
   </g>
   <g id="line2d_57">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="129.708127" y="121.464" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_58">
    <path d="M 110.947747 117.144 
L 373.877993 117.144 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_59">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="242.41287" y="117.144" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_60">
    <path d="M 130.109362 112.824 
L 312.731192 112.824 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_61">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="221.420277" y="112.824" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_62">
    <path d="M 114.217774 108.504 
L 279.866572 108.504 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_63">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="197.042173" y="108.504" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_64">
    <path d="M 91.243499 104.184 
L 222.971917 104.184 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_65">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="157.107708" y="104.184" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_66">
    <path d="M 124.448605 99.864 
L 266.57786 99.864 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_67">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="195.513233" y="99.864" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_68">
    <path d="M 104.364349 95.544 
L 261.737962 95.544 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_69">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="183.051156" y="95.544" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_70">
    <path d="M 93.446357 91.224 
L 232.054095 91.224 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_71">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="162.750226" y="91.224" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_72">
    <path d="M 120.781598 86.904 
L 262.624434 86.904 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_73">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="191.703016" y="86.904" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_74">
    <path d="M 146.522783 82.584 
L 380.045455 82.584 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_75">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="263.284119" y="82.584" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_76">
    <path d="M 133.978331 78.264 
L 272.847184 78.264 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_77">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="203.412757" y="78.264" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_78">
    <path d="M 94.273985 73.944 
L 219.941431 73.944 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_79">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="157.107708" y="73.944" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_80">
    <path d="M 153.948946 69.624 
L 305.685682 69.624 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_81">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="229.817314" y="69.624" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_82">
    <path d="M 108.68454 65.304 
L 322.676826 65.304 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_83">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="215.680683" y="65.304" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_84">
    <path d="M 128.385821 60.984 
L 327.972506 60.984 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_85">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="228.179164" y="60.984" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_86">
    <path d="M 112.593579 56.664 
L 310.492095 56.664 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_87">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="211.542837" y="56.664" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_88">
    <path d="M 70.660407 52.344 
L 216.32531 52.344 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_89">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="143.492859" y="52.344" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_90">
    <path d="M 55.266003 48.024 
L 165.756861 48.024 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #f97316; stroke-width: 3; stroke-linecap: square"/>
   </g>
   <g id="line2d_91">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="110.511432" y="48.024" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_92">
    <path d="M 114.681575 43.704 
L 241.300608 43.704 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_93">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="177.991091" y="43.704" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_94">
    <path d="M 141.074007 39.384 
L 266.964952 39.384 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_95">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="204.01948" y="39.384" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_96">
    <path d="M 98.936322 35.064 
L 185.501161 35.064 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_97">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="142.218742" y="35.064" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_98">
    <path d="M 121.546233 30.744 
L 342.505334 30.744 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_99">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="232.025783" y="30.744" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_100">
    <path d="M 106.30409 26.424 
L 240.917022 26.424 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_101">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="173.610556" y="26.424" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_102">
    <path d="M 78.26799 22.104 
L 198.185027 22.104 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_103">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="138.226509" y="22.104" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_104">
    <path d="M 146.633753 17.784 
L 336.177669 17.784 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_105">
    <g clip-path="url(#pbd7db035e7)">
     <use xlink:href="#mc223a7361e" x="241.405711" y="17.784" style="fill: currentColor; stroke: currentColor"/>
    </g>
   </g>
   <g id="line2d_106">
    <path d="M 184.924741 240.048 
L 184.924741 7.2 
" clip-path="url(#pbd7db035e7)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_3">
    <path d="M 7.2 240.048 
L 7.2 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 397.8 240.048 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 7.2 240.048 
L 397.8 240.048 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 7.2 7.2 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pbd7db035e7">
   <rect x="7.2" y="7.2" width="390.6" height="232.848"/>
  </clipPath>
 </defs>
</svg>
<figcaption>30 kişilik 50 örneklemin %95 güven aralığı. Kesik çizgi gerçek ortalama. Turuncu aralıklar gerçeği kaçırdı; her örneklem başka bir aralık veriyor.</figcaption>
</figure>

**Yaygın yanlış okuma:** "Gerçek ortalamanın 7,42 ile 9,35 arasında olma
olasılığı %95." Gerçek ortalama bir sayıdır, şansa bağlı değil; ya bu
aralıktadır ya değildir. Şansa bağlı olan **aralığın kendisi**: başka
örneklem başka aralık verir. Doğru cümle: "Bu yöntemle kurulan aralıkların
%95'i gerçeği yakalar; elimizdeki aralık bunlardan biri." Gündelik dilde
"gerçek ortalama büyük olasılıkla 7,4 ile 9,4 arasında" demek çoğu zaman
yeterli; ama "%95 olasılık" diye sayı vermek bu yöntemin söylediği şey
değil. (Bayesçi bakış bölümünde o cümleyi gerçekten kurabilen yöntemi
göreceğiz.)

## Daha çok güven, daha geniş aralık

Güveni artırmak bedava değil: %99'luk aralık %95'likten geniştir. Daraltmanın
tek yolu daha çok veri:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x_all = users["minutes"].to_numpy()
rng = np.random.default_rng(41)
for n in [25, 100, 400]:
    samples = rng.choice(x_all, size=(4000, n))
    ses = samples.std(axis=1, ddof=1) / np.sqrt(n)
    width = 2 * stats.t.ppf(0.975, df=n - 1) * ses
    print(n, round(width.mean(), 2))
```

```text
25 4.81
100 2.42
400 1.2
```

Ortalama genişlik 25 kişide 4,81, 100 kişide 2,42, 400
kişide 1,20 dakika: örneklem dört katına çıkınca aralık yarıya
iniyor. Karekök kuralı burada da geçerli.

## Küçük örneklemde t çarpanı neden önemli?

5 kişilik örneklemlerde $s$ çok oynar. Çarpan olarak 1,96 kullanırsak ne
olur?

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
y = users["load_ms"].to_numpy()
rng = np.random.default_rng(42)
samples = rng.choice(y, size=(10000, 5))
means = samples.mean(axis=1)
ses = samples.std(axis=1, ddof=1) / np.sqrt(5)
t4 = stats.t.ppf(0.975, df=4)
print(round(t4, 3))
print(round((np.abs(means - y.mean()) <= 1.96 * ses).mean(), 3))
print(round((np.abs(means - y.mean()) <= t4 * ses).mean(), 3))
```

```text
2.776
0.88
0.95
```

- 4 serbestlik derecesinde t çarpanı 2,776; 1,96'dan çok büyük.
- 1,96 ile kurulan "%95'lik" aralıklar gerçeği yalnızca %88,0
  oranında yakaladı. t çarpanıyla %95,0: söz verilene eşit.
- Örneklem büyüdükçe t çarpanı 1,96'ya yaklaşır; küçük örneklemde fark
  belirleyicidir. `stats.t` kullanmak her durumda güvenli.

## Oranlar için güven aralığı

Bir oran için en basit aralık, ortalamadakinin aynısı:

$$\hat{p} \pm 1{,}96\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n}}$$

Buna **Wald aralığı** denir. Bir de **Wilson aralığı** var: formülü daha
uzun ama aynı işi küçük örneklemde ve 0'a ya da 1'e yakın oranlarda çok daha
iyi yapar. `statsmodels` ikisini de hesaplar:

```python
from statsmodels.stats.proportion import proportion_confint
from ab_data import make_population

users = make_population()
sample = users["bought"].sample(n=400, random_state=25)
k = int(sample.sum())
wald = proportion_confint(k, 400, alpha=0.05, method="normal")
wilson = proportion_confint(k, 400, alpha=0.05, method="wilson")
print(k, [round(v, 4) for v in wald], [round(v, 4) for v in wilson])
```

```text
53 [0.0993, 0.1657] [0.1027, 0.1692]
```

400 kişide 53 kişi alışveriş yapmış. İki aralık birbirine yakın ve
ikisi de gerçek payı (0,114) içeriyor. `alpha=0.05` "%95 güven" demek: dışarıda
kalan pay. Fark küçük örneklemde ortaya çıkıyor:

```python
import numpy as np
from statsmodels.stats.proportion import proportion_confint
from ab_data import make_population

users = make_population()
b = users["bought"].to_numpy()
p = b.mean()
rng = np.random.default_rng(43)
for n in [20, 50, 400]:
    k = rng.choice(b, size=(4000, n)).sum(axis=1)
    lo, hi = proportion_confint(k, n, alpha=0.05, method="normal")
    wl, wh = proportion_confint(k, n, alpha=0.05, method="wilson")
    print(n, round(((lo <= p) & (p <= hi)).mean(), 3),
          round(((wl <= p) & (p <= wh)).mean(), 3))
```

```text
20 0.908 0.977
50 0.916 0.956
400 0.947 0.95
```

- 20 kişide Wald aralığı gerçeği yalnızca %90,8 oranında yakaladı;
  "%95" sözü tutmadı. Wilson %97,7.
- 400 kişide ikisi de %95'e yakın.
- Ders: oranlar için varsayılan olarak Wilson kullan. Wald'ı formülü kolay
  olduğu için bil, ama küçük örneklemde güvenme.

## Özet

- Güven aralığı = tahmin ± çarpan × standart hata. Ortalamada çarpan t
  dağılımından gelir (`stats.t.interval`).
- "%95" yöntemin kapsama oranıdır: binlerce örneklemde aralıkların %95'i
  gerçeği yakalar. Tek bir aralık için "%95 olasılıkla" denmez.
- Güven arttıkça aralık genişler; örneklem dört katına çıkınca yarıya iner.
- Küçük örneklemde 1,96 değil t çarpanı; oranlarda Wald değil Wilson.
