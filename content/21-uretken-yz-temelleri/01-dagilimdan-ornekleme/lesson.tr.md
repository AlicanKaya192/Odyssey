# Dağılımdan Örnekleme

Bir önceki bölümde üretmenin "dağılımdan örnek çekmek" olduğunu gördük ve
işi NumPy'nin `multivariate_normal` fonksiyonuna bıraktık. Peki bilgisayar,
yalnızca 0 ile 1 arasında rastgele sayı üretebilirken, istediğimiz bir
dağılımdan nasıl örnek çekiyor? Bu bölüm üretken modellerin en alttaki
mekanizmasını sıfırdan yazıyor: kategorik örnekleme (bir dil modelinin
sıradaki kelimeyi seçmesi tam olarak budur), ters dönüşüm, reddetme yöntemi,
veriden histogramla üretim ve örneklerle olasılık tahmini (Monte Carlo).

## Her şey düzgün dağılımla başlar

`rng.random()` 0 ile 1 arasında **düzgün dağılımlı** (uniform) bir sayı
verir: her aralık eşit şanslıdır. Bilgisayardaki bütün rastgelelik bu tek
kaynaktan türetilir. Ustalık, bu sayıyı istediğimiz dağılıma
**dönüştürmekte**.

## Kategorik örnekleme: sıradaki kelimeyi seçmek

Bir dil modeli bir cümlenin devamı için her kelimeye bir olasılık verir.
Diyelim ki "I bought ___" sonrası için olasılıklar şöyle: `the` 0,45, `a`
0,25, `my` 0,15, `this` 0,10, `your` 0,05. Bunlardan birini, olasılığıyla
orantılı şansla nasıl seçeriz?

<figure class="fig"><svg viewBox="0 0 600 100" xmlns="http://www.w3.org/2000/svg"><rect x="20.0" y="30" width="252.0" height="44" style="fill:none" stroke="currentColor" stroke-width="1.2"/><text x="146.0" y="57" text-anchor="middle" font-size="13" fill="currentColor">the</text><rect x="272.0" y="30" width="140.0" height="44" class="dot" style="fill-opacity:.35" stroke="currentColor" stroke-width="1.2"/><text x="342.0" y="57" text-anchor="middle" font-size="13" fill="currentColor">a</text><rect x="412.0" y="30" width="84.0" height="44" style="fill:none" stroke="currentColor" stroke-width="1.2"/><text x="454.0" y="57" text-anchor="middle" font-size="13" fill="currentColor">my</text><rect x="496.0" y="30" width="56.0" height="44" style="fill:none" stroke="currentColor" stroke-width="1.2"/><text x="524.0" y="57" text-anchor="middle" font-size="13" fill="currentColor">this</text><rect x="552.0" y="30" width="28.0" height="44" style="fill:none" stroke="currentColor" stroke-width="1.2"/><text x="566.0" y="57" text-anchor="middle" font-size="11" fill="currentColor">your</text><text x="20.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">0</text><text x="272.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">0,45</text><text x="412.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">0,7</text><text x="496.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">0,85</text><text x="552.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">0,95</text><text x="580.0" y="92" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">1</text><line x1="367.2" y1="6" x2="367.2" y2="28" class="curve" stroke-width="2"/><polygon points="362.2,22 372.2,22 367.2,29" fill="currentColor"/><text x="375.2" y="16" font-size="12" fill="currentColor">u = 0,62</text></svg><figcaption>Olasılıklar uç uca: cetvelde 0,45 ile 0,70 arası <code>a</code>. Düzgün sayı 0,62 çıktıysa seçilen kelime <code>a</code>.</figcaption></figure>

Olasılıkları uç uca dizip 0–1 cetvelini bölüyoruz: **birikimli toplam**
(cumulative sum) her kelimenin bittiği yeri verir. Düzgün bir sayı çekip
hangi parçaya düştüğüne bakıyoruz. Geniş parçaya düşme şansı büyük:

```python
import numpy as np

words = ["the", "a", "my", "this", "your"]
probs = np.array([0.45, 0.25, 0.15, 0.10, 0.05])
cum = np.cumsum(probs)
print(cum)

rng = np.random.default_rng(3)
for n in [20, 1000, 100000]:
    u = rng.random(n)
    picks = np.searchsorted(cum, u, side="right")
    print(n, (np.bincount(picks, minlength=5) / n).round(3))
```

```text
[0.45 0.7  0.85 0.95 1.  ]
20 [0.5  0.3  0.15 0.   0.05]
1000 [0.452 0.257 0.145 0.103 0.043]
100000 [0.45 0.25 0.15 0.1  0.05]
```

20 çekilişte oranlar dağınık; `this` hiç gelmedi. Örnek arttıkça oranlar
gerçek olasılıklara yaklaşıyor (**büyük sayılar yasası**). Bunun pratik bir
sonucu var: bir dil modeline aynı soruyu bir kez sormak, onun "tipik"
cevabını görmek demek değil; tek bir çekiliş görmek demek.

`np.searchsorted(cum, u, side="right")`, `u`'nun cetvelde hangi parçaya
düştüğünü bulur. NumPy'de aynı işi `rng.choice(5, p=probs)` de yapar; içini
bilmek için bir kez elle yazdık.

## Ters dönüşüm: sürekli bir dağılım

Bir destek hattına çağrılar ortalama 2 dakikada bir geliyor olsun.
İki çağrı arasındaki bekleme süresi **üstel dağılıma** (exponential
distribution) uyar: kısa beklemeler sık, uzunlar seyrek. Bu dağılımın
birikimli fonksiyonu tersine çevrilebiliyor; düzgün sayıyı formüle sokmak
yetiyor. Bu yönteme **ters dönüşüm** (inverse transform sampling) denir:

$$t = -\frac{\ln(1 - u)}{\lambda}$$

Burada $\lambda$ dakikadaki çağrı sayısı (0,5), $u$ düzgün sayı.

```python
rate = 0.5
u = np.random.default_rng(1).random(10000)
waits = -np.log(1 - u) / rate
print("mean  ", waits.mean().round(3))
print("median", np.median(waits).round(3))
```

```text
mean   2.014
median 1.402
```

Ortalama kuramsal değere ($1/\lambda = 2$) çok yakın. Ortancanın (1,4)
ortalamadan küçük olması dağılımın şeklini anlatıyor: beklemelerin yarısı
1,4 dakikadan kısa, ama arada gelen uzun beklemeler ortalamayı yukarı
çekiyor.

## Reddetme yöntemi: formülü olmayan şekiller

Ters dönüşüm her dağılımda işe yaramaz; birikimli fonksiyonu tersine
çevrilemeyen şekiller çok. **Reddetme yöntemi** (rejection sampling) daha
genel bir hile: dağılımın grafiğini bir dikdörtgenin içine koy, dikdörtgene
rastgele nokta at, eğrinin **altına** düşenleri tut, üstündekileri at.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="453.694687pt" height="223.2pt" viewBox="0 0 453.694687 223.2" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 223.2 
L 453.694687 223.2 
L 453.694687 0 
L 0 0 
L 0 223.2 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 30.103125 185 
L 438.543125 185 
L 438.543125 7.2 
L 30.103125 7.2 
L 30.103125 185 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_1">
    <defs>
     <path id="m23ae7838d7" d="M 0 1.5 
C 0.397805 1.5 0.77937 1.341951 1.06066 1.06066 
C 1.341951 0.77937 1.5 0.397805 1.5 0 
C 1.5 -0.397805 1.341951 -0.77937 1.06066 -1.06066 
C 0.77937 -1.341951 0.397805 -1.5 0 -1.5 
C -0.397805 -1.5 -0.77937 -1.341951 -1.06066 -1.06066 
C -1.341951 -0.77937 -1.5 -0.397805 -1.5 0 
C -1.5 0.397805 -1.341951 0.77937 -1.06066 1.06066 
C -0.77937 1.341951 -0.397805 1.5 0 1.5 
z
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#pa4ee9b735a)">
     <use xlink:href="#m23ae7838d7" x="136.955985" y="58.140963" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="152.018848" y="78.337889" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="67.645272" y="167.104163" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="275.208184" y="92.637693" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="106.849439" y="88.102997" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="52.627213" y="151.138716" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="142.411614" y="175.954032" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="298.625066" y="128.226881" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="259.754912" y="56.705853" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="91.394556" y="180.730464" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="206.806845" y="176.63109" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="303.470914" y="71.952234" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="202.785297" y="33.261957" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="288.720961" y="109.506972" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="309.094121" y="140.734371" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="190.058372" y="138.101549" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="106.584565" y="103.273241" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="171.407299" y="147.306433" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="238.842911" y="106.903365" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="394.108696" y="159.468756" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="160.046923" y="73.510612" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="407.590274" y="168.793465" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="222.441559" y="151.773078" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="313.461987" y="42.332237" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="73.890878" y="120.922651" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="72.802896" y="140.24532" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="112.570203" y="180.987788" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="307.765318" y="86.866206" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="293.316675" y="155.795412" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="196.151302" y="55.556694" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="241.094323" y="42.690813" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="272.489195" y="43.197992" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="209.075883" y="108.88453" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="394.529676" y="176.842967" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="280.769671" y="74.14203" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="368.845341" y="180.579448" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="233.52914" y="170.229554" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="312.955231" y="114.604398" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="168.574649" y="164.2184" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="243.647199" y="107.229806" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="71.234504" y="155.033722" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="216.527648" y="178.584918" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="187.391382" y="59.103228" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="271.924933" y="45.796067" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="342.920506" y="121.115624" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="196.417589" y="150.45763" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="110.226764" y="95.899523" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="276.72145" y="70.752394" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="76.106888" y="170.698003" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="370.332405" y="125.784679" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="214.139873" y="177.246659" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="229.625482" y="71.892106" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="283.447187" y="48.798663" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="235.9628" y="178.090457" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="412.951559" y="182.356965" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="264.738221" y="30.929365" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="282.221757" y="154.615957" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="236.999016" y="26.278746" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="122.666274" y="95.690549" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="311.529369" y="103.97964" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="256.826813" y="127.357894" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="151.062631" y="79.9415" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="350.550795" y="77.962806" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="151.257183" y="96.348989" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="75.181664" y="183.981518" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="212.214219" y="22.577545" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="160.147562" y="177.378384" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="189.229423" y="52.7537" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="179.608118" y="91.803375" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="243.913618" y="168.523714" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="90.537084" y="129.729982" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="115.829178" y="135.450089" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="210.022791" y="65.865084" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="280.610681" y="168.45646" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="146.685218" y="109.932475" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="115.491477" y="81.279801" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="260.064314" y="171.990219" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="344.871589" y="158.370362" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="56.253182" y="160.350914" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="105.583933" y="106.537792" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="216.645892" y="28.376731" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="303.223178" y="165.679859" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="399.058383" y="158.968072" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="384.209562" y="148.569512" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="354.304587" y="86.391312" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="281.141765" y="160.061486" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="134.226234" y="102.503773" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="283.643923" y="36.038971" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="187.613974" y="179.818315" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="212.513849" y="106.246056" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="358.727849" y="121.608576" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="253.432799" y="65.906892" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="353.771854" y="95.367441" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="195.931778" y="157.254876" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="277.274335" y="30.834698" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="258.575143" y="131.017064" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="321.581851" y="146.973215" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="254.210631" y="45.311549" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="148.2558" y="75.785122" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="304.127283" y="65.468198" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="113.842201" y="143.36869" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="135.406586" y="83.90401" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="220.270466" y="72.101682" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="364.324371" y="150.098653" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="415.634038" y="160.005728" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="130.032094" y="147.163968" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="291.824068" y="184.633984" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="314.917872" y="154.998365" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="222.055989" y="96.971026" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="270.466309" y="175.172337" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="285.980875" y="148.621177" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="313.068508" y="140.656902" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="128.639361" y="121.740944" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="92.673812" y="160.577286" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="189.642622" y="22.1678" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="262.435294" y="96.469472" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="422.421492" y="173.542482" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="331.7126" y="68.799998" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="139.460142" y="159.925793" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="136.077631" y="65.695869" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="202.685705" y="168.312902" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="296.039792" y="55.692217" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="241.653676" y="36.373574" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="306.853124" y="104.314165" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="231.536611" y="45.367329" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="403.312659" y="166.042248" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="331.081738" y="64.491826" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="75.752417" y="148.6278" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="110.06077" y="165.842683" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="423.356779" y="166.08623" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="352.465883" y="153.892814" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="327.3785" y="149.777995" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="140.539368" y="70.956172" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="322.046718" y="54.495397" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="127.076127" y="136.454709" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="334.474272" y="69.826988" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="315.845488" y="99.615313" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="145.880534" y="142.142426" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="229.186336" y="82.707291" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="394.240926" y="152.833592" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="129.520639" y="107.800541" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="221.385536" y="37.828644" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="175.119521" y="71.808591" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="107.862294" y="81.375765" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="223.561331" y="165.742848" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="356.449745" y="78.399871" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="171.127999" y="93.044979" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="304.271196" y="52.562788" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="329.581024" y="167.512862" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="138.432192" y="177.300804" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="99.631083" y="132.624033" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="92.841637" y="99.828724" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="206.821806" y="49.631905" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="274.174439" y="80.216316" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="274.71098" y="29.628496" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="208.129518" y="116.527537" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="284.522963" y="96.626034" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="231.348244" y="100.58533" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="129.579914" y="68.411577" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="245.085004" y="92.112255" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="203.464167" y="130.208483" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="299.327668" y="152.167569" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="174.401753" y="78.432009" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="293.608817" y="155.208802" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="119.517478" y="126.850258" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="282.393442" y="143.942228" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="135.09306" y="91.995097" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="155.41205" y="157.169582" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="216.784222" y="39.470799" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="143.310427" y="159.880822" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="201.27047" y="86.998442" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="139.319258" y="94.161498" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="329.768371" y="131.73114" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="148.235638" y="140.401924" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="162.129757" y="76.368229" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="104.242957" y="111.248899" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="331.595473" y="167.720693" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="103.723358" y="145.911332" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="152.831725" y="158.924211" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="338.714523" y="89.641739" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="178.719336" y="117.458852" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="298.010518" y="90.853486" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="118.831039" y="76.80462" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="161.791598" y="175.429055" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="372.14948" y="153.079786" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="172.583235" y="143.371493" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="243.355586" y="163.734937" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="135.244737" y="115.760197" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="209.440016" y="37.742923" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="120.630511" y="170.388986" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="395.071476" y="141.925982" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="153.523345" y="79.400947" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="74.659918" y="167.339925" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="205.663301" y="113.359997" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="211.223773" y="83.115144" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="319.864672" y="90.871953" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="171.024021" y="92.852326" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="231.257768" y="14.13708" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="157.140814" y="148.813604" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="326.21572" y="141.013402" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="219.021195" y="167.626915" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="126.791882" y="159.814375" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="362.518524" y="134.450367" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="310.561318" y="150.852271" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="185.088175" y="78.918794" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="190.064952" y="133.809864" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="327.634296" y="182.660922" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="276.782975" y="168.876851" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="405.628451" y="166.29211" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="227.042561" y="74.635388" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="299.320329" y="112.95391" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="252.567206" y="52.599099" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="156.836152" y="97.395754" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="215.336148" y="145.27064" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="324.660195" y="148.665232" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="255.840623" y="144.523358" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="288.403181" y="144.786753" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="229.043343" y="141.842728" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="347.24104" y="82.084872" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="362.618012" y="173.176137" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="180.371875" y="129.995752" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="129.441602" y="158.237028" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="222.911861" y="162.17077" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="377.473249" y="140.509436" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="300.571644" y="34.085247" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="376.129682" y="107.18123" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="299.311596" y="90.400013" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="180.212996" y="65.645912" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="163.45165" y="83.312538" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="67.639558" y="162.124559" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="328.222744" y="66.804095" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="385.533506" y="157.065896" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="198.34918" y="151.454161" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="348.735828" y="75.468041" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="252.228219" y="45.485558" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="306.573729" y="137.304188" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="278.597131" y="79.20025" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="88.519282" y="165.976428" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="154.264444" y="137.091345" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="179.300214" y="124.182698" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="283.166574" y="133.046462" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="83.248866" y="169.342905" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="105.593316" y="144.478305" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="349.199565" y="92.563548" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="322.495372" y="146.099969" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="215.618889" y="75.603008" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="145.284437" y="113.586493" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="312.827189" y="106.47613" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="221.189493" y="149.387204" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="157.34022" y="49.668024" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="387.358745" y="171.672727" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="358.604414" y="83.594952" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="282.44467" y="22.527849" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="293.947248" y="90.498848" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="308.721472" y="124.502275" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="335.72695" y="121.360968" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="134.455071" y="117.141111" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="97.040806" y="158.160601" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="396.218156" y="158.890882" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="113.355161" y="113.423501" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="120.762484" y="107.220159" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="424.701334" y="164.061831" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="375.049226" y="106.862552" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="241.156486" y="162.114423" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="183.513339" y="141.303166" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="287.050083" y="162.234771" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="400.574712" y="169.910802" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="126.685139" y="67.823444" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="268.047086" y="57.972533" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="253.328693" y="57.191933" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="130.223015" y="87.288803" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="404.306722" y="169.283635" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="193.230156" y="122.638192" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="243.732391" y="22.179546" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="162.834965" y="72.310237" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#m23ae7838d7" x="155.524207" y="63.091541" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="PathCollection_2">
    <defs>
     <path id="m9158e41bd1" d="M 0 1.5 
C 0.397805 1.5 0.77937 1.341951 1.06066 1.06066 
C 1.341951 0.77937 1.5 0.397805 1.5 0 
C 1.5 -0.397805 1.341951 -0.77937 1.06066 -1.06066 
C 0.77937 -1.341951 0.397805 -1.5 0 -1.5 
C -0.397805 -1.5 -0.77937 -1.341951 -1.06066 -1.06066 
C -1.341951 -0.77937 -1.5 -0.397805 -1.5 0 
C -1.5 0.397805 -1.341951 0.77937 -1.06066 1.06066 
C -0.77937 1.341951 -0.397805 1.5 0 1.5 
z
" style="stroke: #f97316"/>
    </defs>
    <g clip-path="url(#pa4ee9b735a)">
     <use xlink:href="#m9158e41bd1" x="362.665486" y="66.460742" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="327.676387" y="13.443529" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="425.242665" y="77.578959" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="346.874462" y="26.0167" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="391.34775" y="68.819139" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="376.965209" y="40.397937" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="382.226595" y="56.57711" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="118.417407" y="38.565663" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="45.870596" y="47.665855" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="316.807369" y="13.355195" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="396.77366" y="112.191002" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="371.225353" y="63.257247" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="427.792482" y="136.837465" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="100.263729" y="79.614397" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="104.114996" y="40.854974" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="38.235471" y="86.087533" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="70.706602" y="63.687223" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="336.59511" y="31.537125" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="424.150438" y="115.035754" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="47.26242" y="32.8522" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="408.795188" y="24.554642" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="35.343857" y="25.864691" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="34.108022" y="103.287592" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="368.073723" y="86.697648" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="53.570118" y="52.915611" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="431.143558" y="160.976871" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="50.122154" y="63.146353" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="32.874581" y="45.369064" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="153.575912" y="17.782764" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="401.633632" y="69.14141" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="422.969291" y="137.351584" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="54.378701" y="25.841228" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="51.641042" y="110.975464" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="429.000534" y="113.024613" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="65.276269" y="43.170139" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="366.670337" y="40.23982" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="428.120487" y="67.549855" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="425.349689" y="51.37091" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="48.069458" y="18.593541" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="390.630112" y="83.255153" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="108.766617" y="47.46167" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="73.185571" y="50.433006" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="31.40473" y="101.380843" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="400.492863" y="38.480445" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="78.146126" y="23.985641" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="425.385161" y="46.393368" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="177.181361" y="23.362198" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="65.603137" y="41.530355" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="394.178933" y="53.48152" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="320.302026" y="17.581328" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="427.399678" y="109.112272" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="150.764473" y="23.390305" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="418.821159" y="62.294942" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="92.803359" y="52.461972" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="390.419415" y="55.753694" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="56.939359" y="27.249016" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="368.830381" y="31.602417" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="35.817618" y="83.594129" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="401.042939" y="25.118972" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="61.158125" y="51.510003" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="47.344591" y="125.419749" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="104.288216" y="43.617899" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="281.220876" y="21.814163" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="145.74505" y="24.330365" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="427.558129" y="24.670465" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="34.907932" y="49.705978" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="394.683154" y="69.157524" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="420.741886" y="22.052779" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="434.043189" y="39.002717" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="423.633479" y="117.081776" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="433.581739" y="39.577529" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="130.403497" y="36.801292" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="124.617079" y="28.71794" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="56.805858" y="131.814296" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="99.018542" y="82.810007" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="176.509149" y="16.388734" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="66.054721" y="74.106463" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="91.670959" y="83.0661" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="48.340578" y="122.886868" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="411.041724" y="15.115811" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="413.995636" y="73.130179" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="94.941928" y="30.943912" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="95.106907" y="67.848152" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="103.26863" y="70.835138" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="366.278017" y="24.610508" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="54.111738" y="120.437695" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="53.170412" y="76.685611" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="39.007197" y="147.747857" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="348.303965" y="19.446613" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="376.027617" y="63.83207" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="50.66764" y="15.376028" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="416.19816" y="42.318588" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="58.877339" y="15.668015" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="73.361574" y="116.166971" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="97.693614" y="87.780927" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="79.653233" y="15.181924" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="404.240399" y="33.969921" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="419.337313" y="133.489669" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="83.520964" y="94.189328" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="404.87851" y="112.608336" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="363.658996" y="24.983418" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="170.242258" y="23.328895" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="52.855157" y="134.624772" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="344.116529" y="25.875488" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="121.321425" y="64.448811" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="358.143785" y="64.327323" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="393.640036" y="58.349681" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="74.070364" y="69.898607" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="51.574185" y="118.610856" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="82.9982" y="70.374222" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="112.542784" y="22.501671" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="389.917157" y="25.100264" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="406.106394" y="95.376651" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="359.00229" y="46.620866" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="433.867194" y="100.150127" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="330.743099" y="34.113893" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="34.648559" y="155.01807" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="109.827255" y="63.488106" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="35.613704" y="94.284411" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="99.955069" y="20.102138" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="113.058047" y="13.540875" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="418.036047" y="128.402751" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="382.957991" y="47.288861" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#m9158e41bd1" x="438.526006" y="121.350515" style="fill: #f97316; stroke: #f97316"/>
    </g>
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
       <use xlink:href="#m15aed4d867" x="30.103125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="30.103125" y="199.597656" transform="rotate(-0 30.103125 199.597656)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="111.791125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="111.791125" y="199.597656" transform="rotate(-0 111.791125 199.597656)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="193.479125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="193.479125" y="199.597656" transform="rotate(-0 193.479125 199.597656)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="275.167125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="275.167125" y="199.597656" transform="rotate(-0 275.167125 199.597656)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="356.855125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="356.855125" y="199.597656" transform="rotate(-0 356.855125 199.597656)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="438.543125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="438.543125" y="199.597656" transform="rotate(-0 438.543125 199.597656)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="234.323125" y="213.597656" transform="rotate(-0 234.323125 213.597656)">x</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_7">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="188.798828" transform="rotate(-0 23.103125 188.798828)">0.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="162.058065" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="165.856893" transform="rotate(-0 23.103125 165.856893)">0.2</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="139.116129" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="142.914957" transform="rotate(-0 23.103125 142.914957)">0.4</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="116.174194" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="119.973022" transform="rotate(-0 23.103125 119.973022)">0.6</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="93.232258" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="97.031086" transform="rotate(-0 23.103125 97.031086)">0.8</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="70.290323" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="74.089151" transform="rotate(-0 23.103125 74.089151)">1.0</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="47.348387" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="51.147215" transform="rotate(-0 23.103125 51.147215)">1.2</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="24.406452" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="28.20528" transform="rotate(-0 23.103125 28.20528)">1.4</text>
     </g>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 30.103125 185 
L 38.312974 171.443744 
L 46.522823 158.443642 
L 52.68021 149.058542 
L 58.837597 139.986278 
L 64.994984 131.226852 
L 71.152371 122.780261 
L 77.309758 114.646508 
L 83.467145 106.825591 
L 89.624532 99.317511 
L 95.781919 92.122267 
L 101.939306 85.23986 
L 108.096693 78.67029 
L 114.25408 72.413557 
L 120.411467 66.46966 
L 126.568854 60.8386 
L 132.726241 55.520376 
L 138.883628 50.514989 
L 145.041014 45.822439 
L 151.198401 41.442726 
L 157.355788 37.375849 
L 163.513175 33.621809 
L 169.670562 30.180606 
L 175.827949 27.052239 
L 181.985336 24.236709 
L 188.142723 21.734015 
L 194.30011 19.544159 
L 200.457497 17.667139 
L 206.614884 16.102955 
L 212.772271 14.851609 
L 218.929658 13.913098 
L 225.087045 13.287425 
L 231.244432 12.974588 
L 237.401818 12.974588 
L 243.559205 13.287425 
L 249.716592 13.913098 
L 255.873979 14.851609 
L 262.031366 16.102955 
L 268.188753 17.667139 
L 274.34614 19.544159 
L 280.503527 21.734015 
L 286.660914 24.236709 
L 292.818301 27.052239 
L 298.975688 30.180606 
L 305.133075 33.621809 
L 311.290462 37.375849 
L 317.447849 41.442726 
L 323.605236 45.822439 
L 329.762622 50.514989 
L 335.920009 55.520376 
L 342.077396 60.8386 
L 348.234783 66.46966 
L 354.39217 72.413557 
L 360.549557 78.67029 
L 366.706944 85.23986 
L 372.864331 92.122267 
L 379.021718 99.317511 
L 385.179105 106.825591 
L 391.336492 114.646508 
L 397.493879 122.780261 
L 403.651266 131.226852 
L 409.808653 139.986278 
L 415.96604 149.058542 
L 422.123427 158.443642 
L 428.280813 168.141579 
L 436.490663 181.558797 
L 438.543125 185 
L 438.543125 185 
" clip-path="url(#pa4ee9b735a)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 30.103125 185 
L 30.103125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 438.543125 185 
L 438.543125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 30.103125 185 
L 438.543125 185 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 30.103125 7.2 
L 438.543125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa4ee9b735a">
   <rect x="30.103125" y="7.2" width="408.44" height="177.8"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Dikdörtgene atılan 400 nokta: eğrinin altındakiler (mor) tutulur, üstündekiler (turuncu) atılır. Tutulanlar eğrinin şeklinde dağılır.</figcaption>
</figure>

Örnek: $[0, 1]$ aralığında $f(x) = 6x(1-x)$ yoğunluğu, ortada tepe yapan bir
çan. En yüksek değeri 1,5 olduğu için dikdörtgenin yüksekliği 1,5:

```python
r = np.random.default_rng(2)
x = r.random(10000)
height = r.random(10000) * 1.5
kept = x[height < 6 * x * (1 - x)]
print("accepted", len(kept) / 10000)
print("mean", kept.mean().round(3), "std", kept.std().round(3))
```

```text
accepted 0.664
mean 0.502 std 0.227
```

Noktaların yaklaşık üçte ikisi kabul edildi; kuramsal oran eğrinin altındaki
alanın dikdörtgene oranı: $1 / 1{,}5 \approx 0{,}667$. Tutulan noktaların
ortalaması 0,5 civarında, standart sapması kuramsal değere (0,224) yakın.
Bedeli: atılan her nokta boşa giden hesap. Dikdörtgen eğriye ne kadar kötü
oturursa o kadar çok nokta atılır.

## Veriden üretmek: histogram

Bazen elde formül yoktur, yalnızca veri vardır. En basit üretken model
verinin **histogramıdır**: önce bir aralık (kutu) seçilir, kutunun
olasılığı içindeki örnek oranıdır; sonra kutunun içinde düzgün bir sayı
çekilir. Bream'lerin ağırlığıyla:

```python
from gen_data import make_fish

X, y = make_fish()
weights = X[np.array(y) == "bream", 1]
counts, edges = np.histogram(weights, bins=10)
p = counts / counts.sum()

g = np.random.default_rng(5)
box = g.choice(len(p), size=5000, p=p)
fake = g.uniform(edges[box], edges[box + 1])
print("generated", fake.mean().round(1), fake.std().round(1))
print("real     ", weights.mean().round(1), weights.std().round(1))
print("range", edges[0].round(1), edges[-1].round(1))
print("fake ", fake.min().round(1), fake.max().round(1))
```

```text
generated 552.1 106.6
real      555.5 104.3
range 280.0 822.8
fake  280.3 822.4
```

Ortalama ve yayılım tutuyor. Ama son iki satıra bak: histogram,
gözlediği en hafif ve en ağır balığın **dışına hiç çıkamıyor**. Veride
900 gramlık bir bream yoksa model de asla üretmez. Bu, veriden öğrenen
bütün üretken modellerin küçük bir resmi: **gördüğünün dışını bilmez**.
Normal dağılım gibi bir varsayım bu sınırı aşar, ama o da kendi hatasını
getirir.

## Monte Carlo: örneklerle soru cevaplamak

Örneklemenin ikinci büyük kullanımı, hesaplaması zor olasılıkları
**sayarak** tahmin etmek. Soru: "Bir bream'in 700 gramdan ağır olma olasılığı
ne?" Bream'lere bir normal dağılım uydurup ondan 100 000 balık çekiyor ve
700'ü geçenleri sayıyoruz; aynı oranı verinin kendisinde de ölçüyoruz:

```python
m, s = weights.mean(), weights.std(ddof=1)
sim = np.random.default_rng(9).normal(m, s, 100000)
print("model:", (sim > 700).mean().round(4))
print("data :", (weights > 700).mean().round(4))
print("count:", (weights > 700).sum(), "of", len(weights))
```

```text
model: 0.0846
data : 0.0605
count: 17 of 281
```

Model %8,5 diyor, veride %6. Hangisine güvenmeli? Veride 700 gramı geçen
yalnızca 17 balık var; bir iki balık eksik ya da fazla olsa oran belirgin
oynar. Aynı üreteçten çok daha fazla balık çekip bakalım:

```python
X_big, y_big = make_fish(200000)
big = X_big[np.array(y_big) == "bream", 1]
print("big data:", (big > 700).mean().round(4))
```

```text
big data: 0.079
```

Gerçek oran %7,9 civarında: model, 281 balığın kendisinden daha yakın
tahmin etmiş. Çünkü bu veriyi **gerçekten normal dağılımdan** ürettik ve
modelin varsayımı doğru. Gerçek dünyada bunu bilemezsin: varsayım yanlışsa
Monte Carlo yanlış modeli sadakatle hesaplar, hatayı düzeltmez. Az veride
ise ham oran kuyrukta oynaktır. İkisini birlikte okumak gerekir.

## Özet

- Bütün rastgelelik 0–1 arası düzgün sayıdan türetilir; iş onu istenen
  dağılıma dönüştürmekte.
- **Kategorik örnekleme:** birikimli toplam + `searchsorted`. Dil
  modellerinin sıradaki token'ı seçmesi budur. Az örnekte oranlar oynak.
- **Ters dönüşüm:** birikimli fonksiyonu tersine çevrilebilen dağılımlar
  için tek formül.
- **Reddetme yöntemi:** her şekle uyar ama atılan noktalar kadar hesap
  boşa gider.
- **Histogram:** veriden en basit üretim; gözlenen aralığın dışına çıkamaz.
- **Monte Carlo:** olasılığı sayarak tahmin eder; doğruluğu modelin
  doğruluğuyla sınırlı. Az veride ham oran da kuyrukta oynak.
