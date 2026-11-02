# Örneklem Dağılımı ve Merkezi Limit Teoremi

İlk bölümde bin örneklem çekip ortalamalarının nasıl oynadığını gördük.
Gerçek hayatta ise **tek** örneklemin var. O tek ortalamanın gerçeğe ne
kadar yakın olduğunu nasıl bileceğiz? Cevap şaşırtıcı derecede genel bir
sonuçta: örneklem ortalamaları, veri ne biçimde olursa olsun, örneklem
yeterince büyükse **çan biçimli** dağılır ve bu çanın genişliğini tek
örneklemden hesaplayabiliriz. Bu sonuca **merkezi limit teoremi** (central
limit theorem, kısaca MLT) denir. Güven aralığı da hipotez testi de onun
üstüne kurulu.

## Örneklem dağılımı

Aynı büyüklükte çok sayıda örneklem çekip her birinin ortalamasını
hesaplarsan, bu ortalamaların kendisi bir dağılım oluşturur. Buna
ortalamanın **örneklem dağılımı** (sampling distribution) denir. Dikkat:
verinin dağılımından farklı bir şey. Veri tek tek kullanıcıların, örneklem
dağılımı ise **ortalamaların** dağılımı.

Oturum süresi sağa çarpık bir değişkendi. Ondan 2, 10, 50 ve 200 kişilik
5000'er örneklem çekelim. Evren 100 000 kişi olduğu için burada seçimi
**iadeli** (with replacement) yapıyoruz: aynı kişinin iki kez seçilme
olasılığı ihmal edilecek kadar küçük, kod da çok daha hızlı.

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x = users["minutes"].to_numpy()
mu, sigma = x.mean(), x.std()
print(round(mu, 2), round(sigma, 2), round(float(stats.skew(x)), 2))
rng = np.random.default_rng(5)
for n in [2, 10, 50, 200]:
    means = rng.choice(x, size=(5000, n)).mean(axis=1)
    print(n, round(means.mean(), 2), round(means.std(), 3),
          round(sigma / np.sqrt(n), 3), round(float(stats.skew(means)), 2))
```

```text
9.04 6.13 2.3
2 8.96 4.337 4.333 1.7
10 9.02 1.952 1.938 0.74
50 9.03 0.854 0.867 0.3
200 9.04 0.438 0.433 0.15
```

İlk satır evren: ortalama $\mu$, standart sapma $\sigma$ ve **çarpıklık**
(skewness). Çarpıklık simetrik veride 0'dır; sağa çarpık veride pozitiftir.
Sonraki satırların sütunları: örneklem büyüklüğü, 5000 ortalamanın
ortalaması, 5000 ortalamanın standart sapması, $\sigma / \sqrt{n}$ formülü
ve ortalamaların çarpıklığı.

Üç şey görüyoruz:

1. **Merkez doğru yerde.** Ortalamaların ortalaması her $n$'de
   9,04'ün çevresinde. Örneklem ortalaması gerçeği ne yukarı ne
   aşağı iter; ortalamada doğru tahmin eder.
2. **Genişlik $\sigma / \sqrt{n}$.** Ortalamaların sapması formülle
   neredeyse aynı: 200 kişide 0,438, formül 0,433.
3. **Biçim çana döner.** Verinin çarpıklığı 2,3; 2 kişilik
   ortalamalarda 1,70, 50 kişide 0,30, 200 kişide
   0,15. Örneklem büyüdükçe ortalamaların dağılımı simetrikleşiyor.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="495.463748pt" height="221.30725pt" viewBox="0 0 495.463748 221.30725" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 221.30725 
L 495.463748 221.30725 
L 495.463748 0 
L 0 0 
L 0 221.30725 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 8.383748 181.573656 
L 149.524924 181.573656 
L 149.524924 20.797656 
L 8.383748 20.797656 
L 8.383748 181.573656 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 14.799256 181.573656 
L 17.365459 181.573656 
L 17.365459 177.935161 
L 14.799256 177.935161 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_4">
    <path d="M 17.365459 181.573656 
L 19.931662 181.573656 
L 19.931662 166.41326 
L 17.365459 166.41326 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_5">
    <path d="M 19.931662 181.573656 
L 22.497865 181.573656 
L 22.497865 134.879636 
L 19.931662 134.879636 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_6">
    <path d="M 22.497865 181.573656 
L 25.064068 181.573656 
L 25.064068 80.908627 
L 22.497865 80.908627 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_7">
    <path d="M 25.064068 181.573656 
L 27.630272 181.573656 
L 27.630272 51.800666 
L 25.064068 51.800666 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_8">
    <path d="M 27.630272 181.573656 
L 30.196475 181.573656 
L 30.196475 29.969696 
L 27.630272 29.969696 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_9">
    <path d="M 30.196475 181.573656 
L 32.762678 181.573656 
L 32.762678 28.453656 
L 30.196475 28.453656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_10">
    <path d="M 32.762678 181.573656 
L 35.328881 181.573656 
L 35.328881 42.401221 
L 32.762678 42.401221 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_11">
    <path d="M 35.328881 181.573656 
L 37.895084 181.573656 
L 37.895084 46.646131 
L 35.328881 46.646131 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_12">
    <path d="M 37.895084 181.573656 
L 40.461288 181.573656 
L 40.461288 62.716151 
L 37.895084 62.716151 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_13">
    <path d="M 40.461288 181.573656 
L 43.027491 181.573656 
L 43.027491 86.366369 
L 40.461288 86.366369 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_14">
    <path d="M 43.027491 181.573656 
L 45.593694 181.573656 
L 45.593694 95.765815 
L 43.027491 95.765815 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_15">
    <path d="M 45.593694 181.573656 
L 48.159897 181.573656 
L 48.159897 117.899993 
L 45.593694 117.899993 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_16">
    <path d="M 48.159897 181.573656 
L 50.7261 181.573656 
L 50.7261 126.086607 
L 48.159897 126.086607 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_17">
    <path d="M 50.7261 181.573656 
L 53.292304 181.573656 
L 53.292304 137.911716 
L 50.7261 137.911716 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_18">
    <path d="M 53.292304 181.573656 
L 55.858507 181.573656 
L 55.858507 147.917577 
L 53.292304 147.917577 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_19">
    <path d="M 55.858507 181.573656 
L 58.42471 181.573656 
L 58.42471 153.981735 
L 55.858507 153.981735 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_20">
    <path d="M 58.42471 181.573656 
L 60.990913 181.573656 
L 60.990913 159.742686 
L 58.42471 159.742686 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_21">
    <path d="M 60.990913 181.573656 
L 63.557116 181.573656 
L 63.557116 165.200429 
L 60.990913 165.200429 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_22">
    <path d="M 63.557116 181.573656 
L 66.12332 181.573656 
L 66.12332 167.626092 
L 63.557116 167.626092 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_23">
    <path d="M 66.12332 181.573656 
L 68.689523 181.573656 
L 68.689523 169.445339 
L 66.12332 169.445339 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_24">
    <path d="M 68.689523 181.573656 
L 71.255726 181.573656 
L 71.255726 172.780627 
L 68.689523 172.780627 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_25">
    <path d="M 71.255726 181.573656 
L 73.821929 181.573656 
L 73.821929 174.903082 
L 71.255726 174.903082 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_26">
    <path d="M 73.821929 181.573656 
L 76.388133 181.573656 
L 76.388133 176.419122 
L 73.821929 176.419122 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_27">
    <path d="M 76.388133 181.573656 
L 78.954336 181.573656 
L 78.954336 176.72233 
L 76.388133 176.72233 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_28">
    <path d="M 78.954336 181.573656 
L 81.520539 181.573656 
L 81.520539 175.20629 
L 78.954336 175.20629 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_29">
    <path d="M 81.520539 181.573656 
L 84.086742 181.573656 
L 84.086742 178.541577 
L 81.520539 178.541577 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_30">
    <path d="M 84.086742 181.573656 
L 86.652945 181.573656 
L 86.652945 178.844785 
L 84.086742 178.844785 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_31">
    <path d="M 86.652945 181.573656 
L 89.219149 181.573656 
L 89.219149 179.451201 
L 86.652945 179.451201 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_32">
    <path d="M 89.219149 181.573656 
L 91.785352 181.573656 
L 91.785352 177.631953 
L 89.219149 177.631953 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_33">
    <path d="M 91.785352 181.573656 
L 94.351555 181.573656 
L 94.351555 179.451201 
L 91.785352 179.451201 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_34">
    <path d="M 94.351555 181.573656 
L 96.917758 181.573656 
L 96.917758 180.664032 
L 94.351555 180.664032 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_35">
    <path d="M 96.917758 181.573656 
L 99.483961 181.573656 
L 99.483961 180.664032 
L 96.917758 180.664032 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_36">
    <path d="M 99.483961 181.573656 
L 102.050165 181.573656 
L 102.050165 180.360825 
L 99.483961 180.360825 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_37">
    <path d="M 102.050165 181.573656 
L 104.616368 181.573656 
L 104.616368 180.96724 
L 102.050165 180.96724 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_38">
    <path d="M 104.616368 181.573656 
L 107.182571 181.573656 
L 107.182571 180.96724 
L 104.616368 180.96724 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_39">
    <path d="M 107.182571 181.573656 
L 109.748774 181.573656 
L 109.748774 180.96724 
L 107.182571 180.96724 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_40">
    <path d="M 109.748774 181.573656 
L 112.314977 181.573656 
L 112.314977 180.664032 
L 109.748774 180.664032 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_41">
    <path d="M 112.314977 181.573656 
L 114.881181 181.573656 
L 114.881181 181.573656 
L 112.314977 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_42">
    <path d="M 114.881181 181.573656 
L 117.447384 181.573656 
L 117.447384 181.573656 
L 114.881181 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_43">
    <path d="M 117.447384 181.573656 
L 120.013587 181.573656 
L 120.013587 180.96724 
L 117.447384 180.96724 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_44">
    <path d="M 120.013587 181.573656 
L 122.57979 181.573656 
L 122.57979 181.573656 
L 120.013587 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_45">
    <path d="M 122.57979 181.573656 
L 125.145993 181.573656 
L 125.145993 181.573656 
L 122.57979 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_46">
    <path d="M 125.145993 181.573656 
L 127.712197 181.573656 
L 127.712197 181.573656 
L 125.145993 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_47">
    <path d="M 127.712197 181.573656 
L 130.2784 181.573656 
L 130.2784 181.573656 
L 127.712197 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_48">
    <path d="M 130.2784 181.573656 
L 132.844603 181.573656 
L 132.844603 181.573656 
L 130.2784 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_49">
    <path d="M 132.844603 181.573656 
L 135.410806 181.573656 
L 135.410806 181.270448 
L 132.844603 181.270448 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_50">
    <path d="M 135.410806 181.573656 
L 137.97701 181.573656 
L 137.97701 181.573656 
L 135.410806 181.573656 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_51">
    <path d="M 137.97701 181.573656 
L 140.543213 181.573656 
L 140.543213 181.270448 
L 137.97701 181.270448 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_52">
    <path d="M 140.543213 181.573656 
L 143.109416 181.573656 
L 143.109416 181.270448 
L 140.543213 181.270448 
z
" clip-path="url(#p6402f15322)" style="fill: #8b5cf6; opacity: 0.75"/>
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
       <use xlink:href="#m15aed4d867" x="10.38125" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="10.38125" y="196.171312" transform="rotate(-0 10.38125 196.171312)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="73.047995" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="73.047995" y="196.171312" transform="rotate(-0 73.047995 196.171312)">20</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="135.71474" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="135.71474" y="196.171312" transform="rotate(-0 135.71474 196.171312)">40</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_4">
    <path d="M 14.799256 157.347633 
L 16.515779 151.544355 
L 18.232303 144.941278 
L 20.377958 135.653739 
L 22.952744 123.303805 
L 29.81884 89.334325 
L 31.535363 82.164545 
L 32.822756 77.521222 
L 34.110149 73.636059 
L 35.397542 70.608227 
L 36.255804 69.105931 
L 37.114066 68.037987 
L 37.972328 67.41708 
L 38.83059 67.250621 
L 39.259721 67.338646 
L 40.117983 67.855887 
L 40.976245 68.822335 
L 41.834507 70.226497 
L 42.692769 72.051787 
L 43.980162 75.531445 
L 45.267554 79.819736 
L 46.984078 86.606738 
L 48.700602 94.346778 
L 51.275388 107.057782 
L 56.42496 132.755754 
L 58.570615 142.344661 
L 60.716269 150.827807 
L 62.432793 156.724089 
L 64.149317 161.808149 
L 65.865841 166.101391 
L 67.582365 169.654195 
L 68.869758 171.874651 
L 70.157151 173.752117 
L 71.444544 175.322625 
L 72.731937 176.622512 
L 74.448461 177.995696 
L 76.164984 179.029041 
L 77.881508 179.792649 
L 80.027163 180.458833 
L 82.172818 180.893047 
L 85.176735 181.246587 
L 89.038914 181.455023 
L 95.905009 181.557645 
L 122.94026 181.573656 
L 143.109416 181.573656 
L 143.109416 181.573656 
" clip-path="url(#p6402f15322)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_53">
    <path d="M 8.383748 181.573656 
L 8.383748 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_54">
    <path d="M 149.524924 181.573656 
L 149.524924 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_55">
    <path d="M 8.383748 181.573656 
L 149.524924 181.573656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_56">
    <path d="M 8.383748 20.797656 
L 149.524924 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_4">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="78.954336" y="14.797656" transform="rotate(-0 78.954336 14.797656)">n = 2</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_57">
    <path d="M 177.753159 181.573656 
L 318.894336 181.573656 
L 318.894336 20.797656 
L 177.753159 20.797656 
L 177.753159 181.573656 
z
" style="fill: none"/>
   </g>
   <g id="patch_58">
    <path d="M 184.168667 181.573656 
L 186.73487 181.573656 
L 186.73487 181.098128 
L 184.168667 181.098128 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_59">
    <path d="M 186.73487 181.573656 
L 189.301074 181.573656 
L 189.301074 181.098128 
L 186.73487 181.098128 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_60">
    <path d="M 189.301074 181.573656 
L 191.867277 181.573656 
L 191.867277 181.573656 
L 189.301074 181.573656 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_61">
    <path d="M 191.867277 181.573656 
L 194.43348 181.573656 
L 194.43348 177.293905 
L 191.867277 177.293905 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_62">
    <path d="M 194.43348 181.573656 
L 196.999683 181.573656 
L 196.999683 172.538625 
L 194.43348 172.538625 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_63">
    <path d="M 196.999683 181.573656 
L 199.565887 181.573656 
L 199.565887 166.83229 
L 196.999683 166.83229 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_64">
    <path d="M 199.565887 181.573656 
L 202.13209 181.573656 
L 202.13209 162.07701 
L 199.565887 162.07701 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_65">
    <path d="M 202.13209 181.573656 
L 204.698293 181.573656 
L 204.698293 141.629308 
L 202.13209 141.629308 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_66">
    <path d="M 204.698293 181.573656 
L 207.264496 181.573656 
L 207.264496 132.118749 
L 204.698293 132.118749 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_67">
    <path d="M 207.264496 181.573656 
L 209.830699 181.573656 
L 209.830699 109.293408 
L 207.264496 109.293408 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_68">
    <path d="M 209.830699 181.573656 
L 212.396903 181.573656 
L 212.396903 81.237259 
L 209.830699 81.237259 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_69">
    <path d="M 212.396903 181.573656 
L 214.963106 181.573656 
L 214.963106 76.481979 
L 212.396903 76.481979 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_70">
    <path d="M 214.963106 181.573656 
L 217.529309 181.573656 
L 217.529309 58.887445 
L 214.963106 58.887445 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_71">
    <path d="M 217.529309 181.573656 
L 220.095512 181.573656 
L 220.095512 59.362973 
L 217.529309 59.362973 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_72">
    <path d="M 220.095512 181.573656 
L 222.661715 181.573656 
L 222.661715 28.453656 
L 220.095512 28.453656 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_73">
    <path d="M 222.661715 181.573656 
L 225.227919 181.573656 
L 225.227919 29.404712 
L 222.661715 29.404712 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_74">
    <path d="M 225.227919 181.573656 
L 227.794122 181.573656 
L 227.794122 32.25788 
L 225.227919 32.25788 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_75">
    <path d="M 227.794122 181.573656 
L 230.360325 181.573656 
L 230.360325 37.964215 
L 227.794122 37.964215 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_76">
    <path d="M 230.360325 181.573656 
L 232.926528 181.573656 
L 232.926528 34.63552 
L 230.360325 34.63552 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_77">
    <path d="M 232.926528 181.573656 
L 235.492731 181.573656 
L 235.492731 41.292911 
L 232.926528 41.292911 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_78">
    <path d="M 235.492731 181.573656 
L 238.058935 181.573656 
L 238.058935 67.446948 
L 235.492731 67.446948 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_79">
    <path d="M 238.058935 181.573656 
L 240.625138 181.573656 
L 240.625138 71.251172 
L 238.058935 71.251172 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_80">
    <path d="M 240.625138 181.573656 
L 243.191341 181.573656 
L 243.191341 89.796762 
L 240.625138 89.796762 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_81">
    <path d="M 243.191341 181.573656 
L 245.757544 181.573656 
L 245.757544 112.622103 
L 243.191341 112.622103 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_82">
    <path d="M 245.757544 181.573656 
L 248.323748 181.573656 
L 248.323748 106.915768 
L 245.757544 106.915768 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_83">
    <path d="M 248.323748 181.573656 
L 250.889951 181.573656 
L 250.889951 115.475271 
L 248.323748 115.475271 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_84">
    <path d="M 250.889951 181.573656 
L 253.456154 181.573656 
L 253.456154 138.776141 
L 250.889951 138.776141 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_85">
    <path d="M 253.456154 181.573656 
L 256.022357 181.573656 
L 256.022357 135.922973 
L 253.456154 135.922973 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_86">
    <path d="M 256.022357 181.573656 
L 258.58856 181.573656 
L 258.58856 137.349557 
L 256.022357 137.349557 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_87">
    <path d="M 258.58856 181.573656 
L 261.154764 181.573656 
L 261.154764 148.2867 
L 258.58856 148.2867 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_88">
    <path d="M 261.154764 181.573656 
L 263.720967 181.573656 
L 263.720967 153.517507 
L 261.154764 153.517507 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_89">
    <path d="M 263.720967 181.573656 
L 266.28717 181.573656 
L 266.28717 159.699371 
L 263.720967 159.699371 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_90">
    <path d="M 266.28717 181.573656 
L 268.853373 181.573656 
L 268.853373 162.552538 
L 266.28717 162.552538 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_91">
    <path d="M 268.853373 181.573656 
L 271.419576 181.573656 
L 271.419576 168.734402 
L 268.853373 168.734402 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_92">
    <path d="M 271.419576 181.573656 
L 273.98578 181.573656 
L 273.98578 170.636513 
L 271.419576 170.636513 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_93">
    <path d="M 273.98578 181.573656 
L 276.551983 181.573656 
L 276.551983 171.112041 
L 273.98578 171.112041 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_94">
    <path d="M 276.551983 181.573656 
L 279.118186 181.573656 
L 279.118186 173.965209 
L 276.551983 173.965209 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_95">
    <path d="M 279.118186 181.573656 
L 281.684389 181.573656 
L 281.684389 176.818377 
L 279.118186 176.818377 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_96">
    <path d="M 281.684389 181.573656 
L 284.250592 181.573656 
L 284.250592 177.293905 
L 281.684389 177.293905 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_97">
    <path d="M 284.250592 181.573656 
L 286.816796 181.573656 
L 286.816796 178.244961 
L 284.250592 178.244961 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_98">
    <path d="M 286.816796 181.573656 
L 289.382999 181.573656 
L 289.382999 177.293905 
L 286.816796 177.293905 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_99">
    <path d="M 289.382999 181.573656 
L 291.949202 181.573656 
L 291.949202 179.196016 
L 289.382999 179.196016 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_100">
    <path d="M 291.949202 181.573656 
L 294.515405 181.573656 
L 294.515405 177.769433 
L 291.949202 177.769433 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_101">
    <path d="M 294.515405 181.573656 
L 297.081608 181.573656 
L 297.081608 180.147072 
L 294.515405 180.147072 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_102">
    <path d="M 297.081608 181.573656 
L 299.647812 181.573656 
L 299.647812 180.147072 
L 297.081608 180.147072 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_103">
    <path d="M 299.647812 181.573656 
L 302.214015 181.573656 
L 302.214015 181.573656 
L 299.647812 181.573656 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_104">
    <path d="M 302.214015 181.573656 
L 304.780218 181.573656 
L 304.780218 181.098128 
L 302.214015 181.098128 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_105">
    <path d="M 304.780218 181.573656 
L 307.346421 181.573656 
L 307.346421 181.098128 
L 304.780218 181.098128 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_106">
    <path d="M 307.346421 181.573656 
L 309.912625 181.573656 
L 309.912625 180.6226 
L 307.346421 180.6226 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_107">
    <path d="M 309.912625 181.573656 
L 312.478828 181.573656 
L 312.478828 180.147072 
L 309.912625 180.147072 
z
" clip-path="url(#pa4e2333bdc)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_4">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="195.024922" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="195.024922" y="196.171312" transform="rotate(-0 195.024922 196.171312)">5</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="239.885477" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="239.885477" y="196.171312" transform="rotate(-0 239.885477 196.171312)">10</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="284.746032" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="284.746032" y="196.171312" transform="rotate(-0 284.746032 196.171312)">15</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="248.323748" y="211.704906" transform="rotate(-0 248.323748 211.704906)">Örneklem ortalaması (dakika)</text>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_8">
    <path d="M 184.168667 178.021279 
L 185.885191 176.953634 
L 187.601715 175.623409 
L 189.318239 173.984527 
L 191.034763 171.988155 
L 192.751287 169.584085 
L 194.467811 166.722561 
L 196.184334 163.356556 
L 197.900858 159.444443 
L 199.617382 154.953006 
L 201.333906 149.860658 
L 203.05043 144.160711 
L 205.196085 136.200547 
L 207.34174 127.378623 
L 209.916526 115.835138 
L 213.778704 97.289064 
L 218.499145 74.778513 
L 220.6448 65.510286 
L 222.361324 58.873018 
L 224.077848 53.114689 
L 225.365241 49.467201 
L 226.652633 46.459142 
L 227.940026 44.138347 
L 228.798288 42.991899 
L 229.65655 42.176057 
L 230.514812 41.696751 
L 231.373074 41.557476 
L 232.231336 41.759249 
L 233.089598 42.300597 
L 233.94786 43.177574 
L 234.806122 44.383812 
L 235.664384 45.910592 
L 236.951777 48.777224 
L 238.23917 52.294193 
L 239.526563 56.406315 
L 241.243086 62.704762 
L 243.388741 71.651409 
L 245.963527 83.495173 
L 254.975278 126.205466 
L 257.550063 136.814818 
L 259.695718 144.708426 
L 261.841373 151.66896 
L 263.557897 156.554419 
L 265.274421 160.844831 
L 266.990945 164.566125 
L 268.707469 167.754745 
L 270.423993 170.454487 
L 272.140516 172.713594 
L 273.85704 174.582207 
L 275.573564 176.110249 
L 277.290088 177.345744 
L 279.006612 178.333587 
L 281.152267 179.282074 
L 283.297922 179.977406 
L 285.872707 180.559915 
L 288.876624 180.993092 
L 292.738803 181.30229 
L 298.317506 181.490744 
L 308.616649 181.566569 
L 312.478828 181.571082 
L 312.478828 181.571082 
" clip-path="url(#pa4e2333bdc)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_108">
    <path d="M 177.753159 181.573656 
L 177.753159 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_109">
    <path d="M 318.894336 181.573656 
L 318.894336 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_110">
    <path d="M 177.753159 181.573656 
L 318.894336 181.573656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_111">
    <path d="M 177.753159 20.797656 
L 318.894336 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_9">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="248.323748" y="14.797656" transform="rotate(-0 248.323748 14.797656)">n = 10</text>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_112">
    <path d="M 347.122571 181.573656 
L 488.263748 181.573656 
L 488.263748 20.797656 
L 347.122571 20.797656 
L 347.122571 181.573656 
z
" style="fill: none"/>
   </g>
   <g id="patch_113">
    <path d="M 353.538079 181.573656 
L 356.104282 181.573656 
L 356.104282 180.082228 
L 353.538079 180.082228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_114">
    <path d="M 356.104282 181.573656 
L 358.670485 181.573656 
L 358.670485 178.590799 
L 356.104282 178.590799 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_115">
    <path d="M 358.670485 181.573656 
L 361.236689 181.573656 
L 361.236689 180.082228 
L 358.670485 180.082228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_116">
    <path d="M 361.236689 181.573656 
L 363.802892 181.573656 
L 363.802892 176.602228 
L 361.236689 176.602228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_117">
    <path d="M 363.802892 181.573656 
L 366.369095 181.573656 
L 366.369095 174.116513 
L 363.802892 174.116513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_118">
    <path d="M 366.369095 181.573656 
L 368.935298 181.573656 
L 368.935298 169.642228 
L 366.369095 169.642228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_119">
    <path d="M 368.935298 181.573656 
L 371.501502 181.573656 
L 371.501502 164.670799 
L 368.935298 164.670799 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_120">
    <path d="M 371.501502 181.573656 
L 374.067705 181.573656 
L 374.067705 162.682228 
L 371.501502 162.682228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_121">
    <path d="M 374.067705 181.573656 
L 376.633908 181.573656 
L 376.633908 152.242228 
L 374.067705 152.242228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_122">
    <path d="M 376.633908 181.573656 
L 379.200111 181.573656 
L 379.200111 146.276513 
L 376.633908 146.276513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_123">
    <path d="M 379.200111 181.573656 
L 381.766314 181.573656 
L 381.766314 142.299371 
L 379.200111 142.299371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_124">
    <path d="M 381.766314 181.573656 
L 384.332518 181.573656 
L 384.332518 124.899371 
L 381.766314 124.899371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_125">
    <path d="M 384.332518 181.573656 
L 386.898721 181.573656 
L 386.898721 103.522228 
L 384.332518 103.522228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_126">
    <path d="M 386.898721 181.573656 
L 389.464924 181.573656 
L 389.464924 96.065085 
L 386.898721 96.065085 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_127">
    <path d="M 389.464924 181.573656 
L 392.031127 181.573656 
L 392.031127 78.665085 
L 389.464924 78.665085 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_128">
    <path d="M 392.031127 181.573656 
L 394.59733 181.573656 
L 394.59733 66.236513 
L 392.031127 66.236513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_129">
    <path d="M 394.59733 181.573656 
L 397.163534 181.573656 
L 397.163534 66.236513 
L 394.59733 66.236513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_130">
    <path d="M 397.163534 181.573656 
L 399.729737 181.573656 
L 399.729737 53.807942 
L 397.163534 53.807942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_131">
    <path d="M 399.729737 181.573656 
L 402.29594 181.573656 
L 402.29594 49.333656 
L 399.729737 49.333656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_132">
    <path d="M 402.29594 181.573656 
L 404.862143 181.573656 
L 404.862143 33.922228 
L 402.29594 33.922228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_133">
    <path d="M 404.862143 181.573656 
L 407.428346 181.573656 
L 407.428346 28.453656 
L 404.862143 28.453656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_134">
    <path d="M 407.428346 181.573656 
L 409.99455 181.573656 
L 409.99455 49.333656 
L 407.428346 49.333656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_135">
    <path d="M 409.99455 181.573656 
L 412.560753 181.573656 
L 412.560753 50.327942 
L 409.99455 50.327942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_136">
    <path d="M 412.560753 181.573656 
L 415.126956 181.573656 
L 415.126956 54.802228 
L 412.560753 54.802228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_137">
    <path d="M 415.126956 181.573656 
L 417.693159 181.573656 
L 417.693159 60.270799 
L 415.126956 60.270799 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_138">
    <path d="M 417.693159 181.573656 
L 420.259362 181.573656 
L 420.259362 74.190799 
L 417.693159 74.190799 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_139">
    <path d="M 420.259362 181.573656 
L 422.825566 181.573656 
L 422.825566 76.676513 
L 420.259362 76.676513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_140">
    <path d="M 422.825566 181.573656 
L 425.391769 181.573656 
L 425.391769 102.527942 
L 422.825566 102.527942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_141">
    <path d="M 425.391769 181.573656 
L 427.957972 181.573656 
L 427.957972 105.013656 
L 425.391769 105.013656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_142">
    <path d="M 427.957972 181.573656 
L 430.524175 181.573656 
L 430.524175 128.379371 
L 427.957972 128.379371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_143">
    <path d="M 430.524175 181.573656 
L 433.090379 181.573656 
L 433.090379 123.407942 
L 430.524175 123.407942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_144">
    <path d="M 433.090379 181.573656 
L 435.656582 181.573656 
L 435.656582 136.333656 
L 433.090379 136.333656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_145">
    <path d="M 435.656582 181.573656 
L 438.222785 181.573656 
L 438.222785 152.242228 
L 435.656582 152.242228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_146">
    <path d="M 438.222785 181.573656 
L 440.788988 181.573656 
L 440.788988 149.756513 
L 438.222785 149.756513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_147">
    <path d="M 440.788988 181.573656 
L 443.355191 181.573656 
L 443.355191 160.196513 
L 440.788988 160.196513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_148">
    <path d="M 443.355191 181.573656 
L 445.921395 181.573656 
L 445.921395 167.653656 
L 443.355191 167.653656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_149">
    <path d="M 445.921395 181.573656 
L 448.487598 181.573656 
L 448.487598 163.179371 
L 445.921395 163.179371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_150">
    <path d="M 448.487598 181.573656 
L 451.053801 181.573656 
L 451.053801 171.133656 
L 448.487598 171.133656 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_151">
    <path d="M 451.053801 181.573656 
L 453.620004 181.573656 
L 453.620004 172.625085 
L 451.053801 172.625085 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_152">
    <path d="M 453.620004 181.573656 
L 456.186207 181.573656 
L 456.186207 175.607942 
L 453.620004 175.607942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_153">
    <path d="M 456.186207 181.573656 
L 458.752411 181.573656 
L 458.752411 176.602228 
L 456.186207 176.602228 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_154">
    <path d="M 458.752411 181.573656 
L 461.318614 181.573656 
L 461.318614 175.607942 
L 458.752411 175.607942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_155">
    <path d="M 461.318614 181.573656 
L 463.884817 181.573656 
L 463.884817 179.087942 
L 461.318614 179.087942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_156">
    <path d="M 463.884817 181.573656 
L 466.45102 181.573656 
L 466.45102 177.596513 
L 463.884817 177.596513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_157">
    <path d="M 466.45102 181.573656 
L 469.017223 181.573656 
L 469.017223 179.585085 
L 466.45102 179.585085 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_158">
    <path d="M 469.017223 181.573656 
L 471.583427 181.573656 
L 471.583427 179.087942 
L 469.017223 179.087942 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_159">
    <path d="M 471.583427 181.573656 
L 474.14963 181.573656 
L 474.14963 180.579371 
L 471.583427 180.579371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_160">
    <path d="M 474.14963 181.573656 
L 476.715833 181.573656 
L 476.715833 180.579371 
L 474.14963 180.579371 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_161">
    <path d="M 476.715833 181.573656 
L 479.282036 181.573656 
L 479.282036 181.076513 
L 476.715833 181.076513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_162">
    <path d="M 479.282036 181.573656 
L 481.848239 181.573656 
L 481.848239 181.076513 
L 479.282036 181.076513 
z
" clip-path="url(#p35faa52ab1)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="matplotlib.axis_5">
    <g id="xtick_7">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="385.350018" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="385.350018" y="196.171312" transform="rotate(-0 385.350018 196.171312)">8</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="428.362374" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="428.362374" y="196.171312" transform="rotate(-0 428.362374 196.171312)">10</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="471.374731" y="181.573656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="471.374731" y="196.171312" transform="rotate(-0 471.374731 196.171312)">12</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_6"/>
   <g id="line2d_12">
    <path d="M 353.538079 179.594887 
L 355.683734 178.82558 
L 357.829389 177.807441 
L 359.545913 176.773437 
L 361.262437 175.507238 
L 362.97896 173.971809 
L 364.695484 172.128235 
L 366.412008 169.936712 
L 368.128532 167.357834 
L 369.845056 164.35416 
L 371.56158 160.892047 
L 373.278104 156.943701 
L 374.994628 152.489375 
L 377.140282 146.196713 
L 379.285937 139.109245 
L 381.431592 131.273104 
L 384.006378 121.007433 
L 387.439426 106.259239 
L 394.305521 76.387539 
L 396.451176 68.018726 
L 398.1677 61.993559 
L 399.884224 56.712535 
L 401.171617 53.315359 
L 402.45901 50.452994 
L 403.746403 48.164934 
L 404.604665 46.974753 
L 405.462927 46.061682 
L 406.321189 45.431484 
L 407.17945 45.088149 
L 408.037712 45.033858 
L 408.895974 45.268957 
L 409.754236 45.791952 
L 410.612498 46.599526 
L 411.47076 47.686575 
L 412.758153 49.825746 
L 414.045546 52.547957 
L 415.332939 55.815509 
L 417.049463 60.942728 
L 418.765987 66.838468 
L 420.911642 75.08272 
L 423.486427 85.886772 
L 433.35644 128.368413 
L 435.931226 137.979888 
L 438.07688 145.183561 
L 440.222535 151.596888 
L 442.36819 157.205129 
L 444.084714 161.122413 
L 445.801238 164.554989 
L 447.517762 167.531079 
L 449.234286 170.084622 
L 450.95081 172.253233 
L 452.667333 174.076386 
L 454.383857 175.593864 
L 456.100381 176.844491 
L 457.816905 177.865156 
L 459.96256 178.869486 
L 462.108215 179.627791 
L 464.683001 180.285384 
L 467.686917 180.796383 
L 471.119965 181.151012 
L 475.840406 181.40064 
L 481.848239 181.523061 
L 481.848239 181.523061 
" clip-path="url(#p35faa52ab1)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_163">
    <path d="M 347.122571 181.573656 
L 347.122571 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_164">
    <path d="M 488.263748 181.573656 
L 488.263748 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_165">
    <path d="M 347.122571 181.573656 
L 488.263748 181.573656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_166">
    <path d="M 347.122571 20.797656 
L 488.263748 20.797656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_13">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="417.693159" y="14.797656" transform="rotate(-0 417.693159 14.797656)">n = 50</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6402f15322">
   <rect x="8.383748" y="20.797656" width="141.141176" height="160.776"/>
  </clipPath>
  <clipPath id="pa4e2333bdc">
   <rect x="177.753159" y="20.797656" width="141.141176" height="160.776"/>
  </clipPath>
  <clipPath id="p35faa52ab1">
   <rect x="347.122571" y="20.797656" width="141.141176" height="160.776"/>
  </clipPath>
 </defs>
</svg>
<figcaption>5000 örneklem ortalamasının dağılımı (mor) ve merkezi limit teoreminin öngördüğü normal eğri (turuncu). 2 kişide ortalamalar hâlâ çarpık; 50 kişide eğriye oturuyor.</figcaption>
</figure>

## Teoremin kendisi

Evrenin ortalaması $\mu$, standart sapması $\sigma$ olsun. $n$ kişilik
rastgele örneklemin ortalaması $\bar{X}$, $n$ büyüdükçe yaklaşık olarak
normal dağılır:

$$\bar{X} \approx N\!\left(\mu,\ \dfrac{\sigma}{\sqrt{n}}\right)$$

- Verinin biçimi önemli değil: çarpık, iki tepeli, 0/1 ... Yeter ki
  değerler bağımsız seçilsin ve varyans sonlu olsun.
- Ortalamanın standart sapmasına **standart hata** (standard error, SE)
  denir: $SE = \dfrac{\sigma}{\sqrt{n}}$. "Ortalamanın kendisi ne kadar
  oynar?" sorusunun cevabı. Bir sonraki bölümün konusu.
- "Yeterince büyük" ne kadar? Ezber bir sayı yok; verinin ne kadar çarpık
  olduğuna bağlı. Şimdi bunu ölçelim.

## Çok çarpık veride sabırlı ol

Harcama (`spend`) sütunu çok daha zor bir veri: kullanıcıların çoğu hiç
harcamadı (0), harcayanların bir kısmı çok harcadı. Ortalamaların
"ortalama ± 1,96 SE" aralığının dışına düşme payına iki yandan ayrı ayrı
bakalım. Normal dağılımda her iki yanda %2,5 olmalı:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
y = users["spend"].to_numpy()
mu, sigma = y.mean(), y.std()
print(round(float(stats.skew(y)), 2), round(float((y == 0).mean()), 3))
rng = np.random.default_rng(6)
for n in [5, 30, 500, 3000]:
    means = np.array([rng.choice(y, size=n).mean() for _ in range(4000)])
    se = sigma / np.sqrt(n)
    low = (means < mu - 1.96 * se).mean()
    high = (means > mu + 1.96 * se).mean()
    print(n, round(float(stats.skew(means)), 2), round(low, 3), round(high, 3))
```

```text
6.03 0.886
5 3.24 0.0 0.049
30 1.01 0.0 0.046
500 0.22 0.016 0.03
3000 0.11 0.021 0.025
```

- Verinin çarpıklığı 6,03; hiç harcamayanların payı %88,6.
- 5 ve 30 kişide ortalamalar aralığın **altına hiç düşmüyor**, bütün kaçışlar
  üstte: çan değil, sağa yatık bir dağılım. Toplam kaçış %5'e yakın görünse
  de iki yanın dengesi bozuk.
- 500 kişide denge kurulmaya başlıyor, 3000 kişide iki yan
  %2,1 ve %2,5: %2,5'e yakın.
- Ders: "30 kişi yeter" gibi kurallar oturum süresi kadar çarpık veride
  idare eder, harcama gibi veride etmez. A/B testlerinde gelir metriği tam
  bu yüzden zordur; ikinci modülde buna döneceğiz.

## Oranlar da aynı kurala uyar

Alışveriş yaptı mı (0/1) gibi bir değişkenin ortalaması bir **oran**dır
(alışveriş yapanların payı). 0 ve 1'lerden oluşan bir verinin standart
sapması $\sqrt{p(1-p)}$ olduğu için oranın standart hatası:

$$SE_{\hat{p}} = \sqrt{\dfrac{p(1-p)}{n}}$$

```python
import numpy as np
from ab_data import make_population

users = make_population()
b = users["bought"].to_numpy()
p = b.mean()
rng = np.random.default_rng(7)
for n in [50, 500]:
    shares = rng.choice(b, size=(5000, n)).mean(axis=1)
    print(n, round(shares.mean(), 3), round(shares.std(), 4),
          round(np.sqrt(p * (1 - p) / n), 4))
```

```text
50 0.113 0.0451 0.045
500 0.114 0.0139 0.0142
```

- 50 kişilik örneklemlerde gözlenen oran gerçeğin (0,114) çevresinde
  ama yaklaşık 0,045 oynuyor; formül de aynısını söylüyor.
- 500 kişide oynama 0,014 oluyor. Bir dönüşüm oranını yüzde
  birlik hassasiyetle ölçmek için yüzlerce kişi yetmez; bunun hesabını
  örneklem büyüklüğü bölümünde yapacağız.

## Özet

- Örneklem dağılımı: çok sayıda örneklemin **ortalamalarının** dağılımı.
- Merkezi limit teoremi: örneklem büyüdükçe ortalamalar, verinin biçimi ne
  olursa olsun, $\mu$ merkezli ve $\sigma / \sqrt{n}$ genişlikli bir çana
  yaklaşır.
- Ne kadar büyüklüğün "yeterli" olduğu verinin çarpıklığına bağlı: oturum
  süresinde onlarca kişi, harcamada binlerce kişi.
- Oran da bir ortalamadır; standart hatası $\sqrt{p(1-p)/n}$.
