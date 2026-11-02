# A/A Testi ve Örneklem Oranı Uyumsuzluğu

Bir deney sisteminin sonucuna güvenmeden önce sistemin kendisine
güvenmek gerekir: atama gerçekten rastgele mi, kayıtlar eksiksiz mi, test
sözünü tutuyor mu? Bu bölüm bunu sınamanın iki aracını gösteriyor: **A/A
testi** ve **örneklem oranı uyumsuzluğu** (sample ratio mismatch, SRM)
denetimi.

## A/A testi: iki grup da aynı şeyi görürse

A/A testinde iki gruba da **aynı** sürüm gösterilir. Gerçek fark sıfırdır;
bu yüzden test yalnızca α kadar yanlış alarm vermeli ve p değerleri, p
Değeri ve Yanlış Yorumları bölümünde gördüğümüz gibi düzgün dağılmalı.
Mağazanın kayıtlarında 1000 A/A testi yapalım (gelir, Welch t-testi):

```python
import numpy as np
from scipy import stats
from ab_data import make_user_log

users = make_user_log()
rng = np.random.default_rng(91)
revenue = users["revenue"]
p_values = []
for _ in range(1000):
    in_b = rng.random(len(users)) < 0.5
    test = stats.ttest_ind(revenue[in_b], revenue[~in_b], equal_var=False)
    p_values.append(test.pvalue)
p_values = np.array(p_values)
print(round(float((p_values < 0.05).mean()), 3))
print(np.histogram(p_values, bins=10, range=(0, 1))[0])
```

```text
0.051
[ 96  76  93  78 114 116  93 114 118 102]
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="382.925pt" height="200.885906pt" viewBox="0 0 382.925 200.885906" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 200.885906 
L 382.925 200.885906 
L 382.925 0 
L 0 0 
L 0 200.885906 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 40.925 162.432 
L 375.725 162.432 
L 375.725 7.2 
L 40.925 7.2 
L 40.925 162.432 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 56.143182 162.432 
L 71.361364 162.432 
L 71.361364 49.897075 
L 56.143182 49.897075 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_4">
    <path d="M 71.361364 162.432 
L 86.579545 162.432 
L 86.579545 63.136478 
L 71.361364 63.136478 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_5">
    <path d="M 86.579545 162.432 
L 101.797727 162.432 
L 101.797727 89.615284 
L 86.579545 89.615284 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_6">
    <path d="M 101.797727 162.432 
L 117.015909 162.432 
L 117.015909 67.549612 
L 101.797727 67.549612 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_7">
    <path d="M 117.015909 162.432 
L 132.234091 162.432 
L 132.234091 74.169313 
L 117.015909 74.169313 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_8">
    <path d="M 132.234091 162.432 
L 147.452273 162.432 
L 147.452273 45.48394 
L 132.234091 45.48394 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_9">
    <path d="M 147.452273 162.432 
L 162.670455 162.432 
L 162.670455 94.028418 
L 147.452273 94.028418 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_10">
    <path d="M 162.670455 162.432 
L 177.888636 162.432 
L 177.888636 58.723343 
L 162.670455 58.723343 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_11">
    <path d="M 177.888636 162.432 
L 193.106818 162.432 
L 193.106818 38.864239 
L 177.888636 38.864239 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_12">
    <path d="M 193.106818 162.432 
L 208.325 162.432 
L 208.325 34.451104 
L 193.106818 34.451104 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_13">
    <path d="M 208.325 162.432 
L 223.543182 162.432 
L 223.543182 49.897075 
L 208.325 49.897075 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_14">
    <path d="M 223.543182 162.432 
L 238.761364 162.432 
L 238.761364 19.005134 
L 223.543182 19.005134 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_15">
    <path d="M 238.761364 162.432 
L 253.979545 162.432 
L 253.979545 76.375881 
L 238.761364 76.375881 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_16">
    <path d="M 253.979545 162.432 
L 269.197727 162.432 
L 269.197727 43.277373 
L 253.979545 43.277373 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_17">
    <path d="M 269.197727 162.432 
L 284.415909 162.432 
L 284.415909 43.277373 
L 269.197727 43.277373 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_18">
    <path d="M 284.415909 162.432 
L 299.634091 162.432 
L 299.634091 30.03797 
L 284.415909 30.03797 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_19">
    <path d="M 299.634091 162.432 
L 314.852273 162.432 
L 314.852273 14.592 
L 299.634091 14.592 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_20">
    <path d="M 314.852273 162.432 
L 330.070455 162.432 
L 330.070455 49.897075 
L 314.852273 49.897075 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_21">
    <path d="M 330.070455 162.432 
L 345.288636 162.432 
L 345.288636 45.48394 
L 330.070455 45.48394 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_22">
    <path d="M 345.288636 162.432 
L 360.506818 162.432 
L 360.506818 54.310209 
L 345.288636 54.310209 
z
" clip-path="url(#p867e373a8e)" style="fill: #8b5cf6; opacity: 0.8"/>
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
       <use xlink:href="#m15aed4d867" x="56.143182" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="56.143182" y="177.029656" transform="rotate(-0 56.143182 177.029656)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="117.015909" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="117.015909" y="177.029656" transform="rotate(-0 117.015909 177.029656)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="177.888636" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="177.888636" y="177.029656" transform="rotate(-0 177.888636 177.029656)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="238.761364" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="238.761364" y="177.029656" transform="rotate(-0 238.761364 177.029656)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="299.634091" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="299.634091" y="177.029656" transform="rotate(-0 299.634091 177.029656)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="360.506818" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="360.506818" y="177.029656" transform="rotate(-0 360.506818 177.029656)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="208.325" y="191.283562" transform="rotate(-0 208.325 191.283562)">p değeri</text>
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
       <use xlink:href="#m5c8d5162d3" x="40.925" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="166.230828" transform="rotate(-0 33.925 166.230828)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="118.300657" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="122.099485" transform="rotate(-0 33.925 122.099485)">20</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="74.169313" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="77.968142" transform="rotate(-0 33.925 77.968142)">40</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="30.03797" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="33.836798" transform="rotate(-0 33.925 33.836798)">60</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="84.816" transform="rotate(-90 14.797656 84.816)">Test sayısı</text>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 40.925 52.103642 
L 375.725 52.103642 
" clip-path="url(#p867e373a8e)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: #f97316; stroke-width: 1.5"/>
   </g>
   <g id="patch_23">
    <path d="M 40.925 162.432 
L 40.925 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 375.725 162.432 
L 375.725 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 40.925 162.432 
L 375.725 162.432 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 40.925 7.2 
L 375.725 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p867e373a8e">
   <rect x="40.925" y="7.2" width="334.8" height="155.232"/>
  </clipPath>
 </defs>
</svg>
<figcaption>1000 A/A testinin p değerleri. Kesikli çizgi her dilimde beklenen 50 test: dağılım düz.</figcaption>
</figure>

- Testlerin %5,1 kadarı "anlamlı" çıktı: söz verilen %5'e
  yakın. Gelir çok çarpık olsa da 10 000'er kişide merkezi limit teoremi
  işliyor.
- p değerleri on dilime aşağı yukarı eşit dağılıyor.

Gerçek sistemde A/A testi aynı kodla, aynı atama ve kayıt yoluyla yapılır.
Yanlış alarm oranı %5'ten belirgin büyük çıkarsa (ya da p değerleri bir
uca yığılırsa) sistemde bir sorun vardır: kullanıcı yerine sayfa
gösterimini gözlem saymak, iki grubun farklı kayıt kodundan geçmesi ya da
yanlış bir test.

Tek bir A/A testinin "anlamlı" çıkması sorun değildir; yirmi testte biri
öyle çıkar. Sorun, bunun %5'ten sık olmasıdır. Bu yüzden A/A testleri tek
tek değil, çok sayıda tekrarla değerlendirilir.

## SRM: grupların büyüklüğü beklenene uymuyorsa

50/50 bir testte gruplar tam eşit çıkmaz, ama ne kadar fark şans sayılır?
Bu, Ki-Kare Testleri bölümündeki **uyum iyiliği** sorusudur. Aşağıdaki
deneyde B'nin hiçbir etkisi yok; ama B'nin kayıt kodunda bir hata var ve
satın almayan bazı mobil kullanıcılar kayda hiç ulaşmıyor:

```python
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_assignment_log

log = make_assignment_log(lost_b=0.08)
counts = log["group"].value_counts().sort_index()
print(counts.to_dict())
print(f"{stats.chisquare(counts).pvalue:.1e}")
k = log.groupby("group")["bought"].sum()
print(log.groupby("group")["bought"].mean().round(4).to_dict())
p = proportions_ztest([k["B"], k["A"]], [counts["B"], counts["A"]])[1]
print(round(p, 4))
```

```text
{'A': 24976, 'B': 23973}
5.8e-06
{'A': 0.1104, 'B': 0.1181}
0.0074
```

- B, A'dan 1 003 kişi eksik. Ki-kare testinin p'si
  5,8e-06: 50/50 bir atamada bu kadar fark şansla pek çıkmaz.
- Satın alma oranı B'de daha yüksek görünüyor ve z-testi bunu "anlamlı"
  buluyor (p = 0,0074). Ama B hiçbir şey yapmıyor: kaybolan
  kullanıcılar **satın almayanlar** olduğu için B'nin oranı şişti.

SRM, sonucun **kendisine** değil, sonucun güvenilirliğine dair bir
alarmdır. SRM varsa grupların büyüklüğü değil, **içeriği** de bozulmuş
olabilir ve hiçbir test bunu düzeltemez. Kural: SRM görülürse sonuç
okunmaz, önce neden bulunur.

## Kaybın nerede olduğunu bulmak

SRM'nin nedeni çoğu zaman bir kesimdedir. Kesim kesim bakalım:

```python
for platform, part in log.groupby("platform"):
    c = part["group"].value_counts().sort_index()
    print(platform, c.to_dict(), f"{stats.chisquare(c).pvalue:.1e}")
```

```text
desktop {'A': 10055, 'B': 10180} 3.8e-01
mobile {'A': 14921, 'B': 13793} 2.8e-11
```

Masaüstünde gruplar dengeli, sorun mobilde. Gerçek hayatta bu bir sonraki
adımı söyler: B'nin mobil sayfasında kayıt kodu çalışıyor mu? Sık görülen
nedenler:

- B sürümü bazı cihazlarda yavaş açılıyor ya da çöküyor, kayıt atılamıyor.
- Bot süzgeci iki grupta farklı çalışıyor.
- Kullanıcılar B'den A'ya yönlendiriliyor (ya da tersi).
- Deneyin bir grubu testin ortasında yeniden başlatılıyor.

## Küçük kayıplar görünmez

Kayıp küçükse SRM testi onu yakalayamayabilir, ama sonuç yine bozulur:

```python
small = make_assignment_log(lost_b=0.02)
c = small["group"].value_counts().sort_index()
print(c.to_dict(), round(stats.chisquare(c).pvalue, 3))
print(small.groupby("group")["bought"].mean().round(4).to_dict())
```

```text
{'A': 24976, 'B': 24781} 0.382
{'A': 0.1104, 'B': 0.1142}
```

SRM'nin p'si 0,382: alarm yok. Yine de B'nin satın alma oranı
yalnızca kayıp yüzünden yükselmiş. SRM denetimi gerekli ama yeterli
değildir; kayıt yolunun iki grupta aynı olması tasarımla sağlanır.

## SRM eşiği

SRM denetimi her deneyde, otomatik ve sürekli yapılır. Bu yüzden eşiği
genellikle α = 0,05'ten çok daha sıkı tutulur (ör. 0,001): yüzlerce deneyde
%5'le alarm vermek, sistemi gereksiz alarmlarla doldurur. Gerçek bir kayıp
çoğu zaman p'yi çok daha küçük yapar.

## Özet

- A/A testi, gerçek fark yokken sistemin yanlış alarm oranını ölçer; çok
  tekrarda yaklaşık %5 olmalı.
- SRM, grup büyüklüklerinin tasarımdaki orana uymamasıdır; ki-kare uyum
  iyiliği testiyle sınanır.
- SRM varsa sonuç okunmaz: kayıp çoğu zaman rastgele değildir ve sahte
  etki üretir.
- Neden kesim kesim aranır (platform, tarayıcı, ülke, gün).
- Küçük kayıplar SRM testine takılmayabilir; kayıt yolunun eşitliği
  tasarımla sağlanır.
