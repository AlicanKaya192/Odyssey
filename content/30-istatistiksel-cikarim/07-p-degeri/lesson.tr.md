# p Değeri ve Yanlış Yorumları

p değeri istatistiğin en çok kullanılan, en çok da yanlış okunan sayısı.
Tanımı tek cümle: **$H_0$ doğru olsaydı, en az bu kadar uç bir sonuç görme
olasılığı**. Sorun, bu cümlenin kulağa başka şeyler gibi gelmesi: "sonucun
şans eseri olma olasılığı", "$H_0$'ın doğru olma olasılığı", "etkinin
büyüklüğü". Hiçbiri değil. Bu bölümde her yanlış okumayı benzetimle
çürüteceğiz, çünkü p değerinin ne olduğunu en iyi binlerce p değerine
bakarak anlarız.

Örnekler iki grubu karşılaştırıyor: oturum sürelerinden iki ayrı grup çekip
ortalamalarını **iki örneklem t-testi** ile (`stats.ttest_ind`) sınıyoruz.
Testin ayrıntısı bir sonraki bölümde; burada yalnızca verdiği p değerine
bakıyoruz.

## Fark yokken p değerleri nasıl dağılır?

İki grubu aynı evrenden çekelim: gerçek fark sıfır. 10 000 kez:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(91)
a = rng.choice(x, size=(10000, 100))
b = rng.choice(x, size=(10000, 100))
p = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
print(round((p < 0.05).mean(), 3), round((p < 0.5).mean(), 3))
print(np.histogram(p, bins=5, range=(0, 1))[0])
```

```text
0.055 0.507
[2090 2007 2006 1980 1917]
```

- Fark yokken p değeri 0 ile 1 arasında **düzgün** dağılır: her beşte birlik
  dilime yaklaşık 2000 test düşüyor.
- Testlerin yaklaşık %5,5 kadarı 0,05'in altına düştü, yarısı 0,5'in
  altına. Yani fark yokken "anlamlı" sonuç görmek hiç şaşırtıcı değil: her
  yirmi denemede bir olur.

## Fark varken p değerleri nasıl dağılır?

Şimdi ikinci grubun oturumları gerçekten %10 uzun olsun:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(91)
a = rng.choice(x, size=(10000, 100))
b = rng.choice(x, size=(10000, 100)) * 1.10
p = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue
print(round((p < 0.05).mean(), 3))
print(np.round(np.percentile(p, [10, 50, 90]), 3))
```

```text
0.174
[0.022 0.28  0.836]
```

- Gerçek bir etki var ama 100'er kişiyle testlerin yalnızca
  %17,4 kadarı onu "anlamlı" buldu (güç).
- Aynı deneyin tekrarlarında p değeri 0,022 ile 0,836 arasında
  gezindi (10. ve 90. yüzdelik). Bir deneyde p = 0,02 görüp tekrarlayan biri
  ikincide p = 0,6 görebilir. **p değeri tekrarlanabilirliğin ölçüsü
  değildir.**

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="483.12pt" height="225.572344pt" viewBox="0 0 483.12 225.572344" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 225.572344 
L 483.12 225.572344 
L 483.12 0 
L 0 0 
L 0 225.572344 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 187.118437 
L 220.254545 187.118437 
L 220.254545 20.798437 
L 7.2 20.798437 
L 7.2 187.118437 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 16.884298 187.118437 
L 26.568595 187.118437 
L 26.568595 136.925097 
L 16.884298 136.925097 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_4">
    <path d="M 26.568595 187.118437 
L 36.252893 187.118437 
L 36.252893 143.017404 
L 26.568595 143.017404 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_5">
    <path d="M 36.252893 187.118437 
L 45.93719 187.118437 
L 45.93719 136.743237 
L 36.252893 136.743237 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_6">
    <path d="M 45.93719 187.118437 
L 55.621488 187.118437 
L 55.621488 141.744385 
L 45.93719 141.744385 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_7">
    <path d="M 55.621488 187.118437 
L 65.305785 187.118437 
L 65.305785 141.198805 
L 55.621488 141.198805 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_8">
    <path d="M 65.305785 187.118437 
L 74.990083 187.118437 
L 74.990083 139.743925 
L 65.305785 139.743925 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_9">
    <path d="M 74.990083 187.118437 
L 84.67438 187.118437 
L 84.67438 141.835315 
L 74.990083 141.835315 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_10">
    <path d="M 84.67438 187.118437 
L 94.358678 187.118437 
L 94.358678 143.199264 
L 84.67438 143.199264 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_11">
    <path d="M 94.358678 187.118437 
L 104.042975 187.118437 
L 104.042975 140.198575 
L 94.358678 140.198575 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_12">
    <path d="M 104.042975 187.118437 
L 113.727273 187.118437 
L 113.727273 145.654373 
L 104.042975 145.654373 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_13">
    <path d="M 113.727273 187.118437 
L 123.41157 187.118437 
L 123.41157 138.198116 
L 113.727273 138.198116 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_14">
    <path d="M 123.41157 187.118437 
L 133.095868 187.118437 
L 133.095868 142.017175 
L 123.41157 142.017175 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_15">
    <path d="M 133.095868 187.118437 
L 142.780165 187.118437 
L 142.780165 145.654373 
L 133.095868 145.654373 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_16">
    <path d="M 142.780165 187.118437 
L 152.464463 187.118437 
L 152.464463 143.017404 
L 142.780165 143.017404 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_17">
    <path d="M 152.464463 187.118437 
L 162.14876 187.118437 
L 162.14876 141.289735 
L 152.464463 141.289735 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_18">
    <path d="M 162.14876 187.118437 
L 171.833058 187.118437 
L 171.833058 138.470906 
L 162.14876 138.470906 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_19">
    <path d="M 171.833058 187.118437 
L 181.517355 187.118437 
L 181.517355 140.653225 
L 171.833058 140.653225 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_20">
    <path d="M 181.517355 187.118437 
L 191.201653 187.118437 
L 191.201653 143.653914 
L 181.517355 143.653914 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_21">
    <path d="M 191.201653 187.118437 
L 200.88595 187.118437 
L 200.88595 144.745074 
L 191.201653 144.745074 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_22">
    <path d="M 200.88595 187.118437 
L 210.570248 187.118437 
L 210.570248 145.108793 
L 200.88595 145.108793 
z
" clip-path="url(#p6148996116)" style="fill: #8b5cf6; opacity: 0.8"/>
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
       <use xlink:href="#m15aed4d867" x="16.884298" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="16.884298" y="201.716094" transform="rotate(-0 16.884298 201.716094)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="55.621488" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="55.621488" y="201.716094" transform="rotate(-0 55.621488 201.716094)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="94.358678" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="94.358678" y="201.716094" transform="rotate(-0 94.358678 201.716094)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="133.095868" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="133.095868" y="201.716094" transform="rotate(-0 133.095868 201.716094)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="171.833058" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="171.833058" y="201.716094" transform="rotate(-0 171.833058 201.716094)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="210.570248" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.570248" y="201.716094" transform="rotate(-0 210.570248 201.716094)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="215.97" transform="rotate(-0 113.727273 215.97)">p değeri</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_7">
    <path d="M 26.568595 187.118437 
L 26.568595 20.798437 
" clip-path="url(#p6148996116)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_23">
    <path d="M 7.2 187.118437 
L 7.2 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 220.254545 187.118437 
L 220.254545 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 7.2 187.118437 
L 220.254545 187.118437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 7.2 20.798437 
L 220.254545 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_8">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="14.798438" transform="rotate(-0 113.727273 14.798438)">Fark yok</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_27">
    <path d="M 262.865455 187.118437 
L 475.92 187.118437 
L 475.92 20.798437 
L 262.865455 20.798437 
L 262.865455 187.118437 
z
" style="fill: none"/>
   </g>
   <g id="patch_28">
    <path d="M 272.549752 187.118437 
L 282.23405 187.118437 
L 282.23405 28.718437 
L 272.549752 28.718437 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_29">
    <path d="M 282.23405 187.118437 
L 291.918347 187.118437 
L 291.918347 97.097772 
L 282.23405 97.097772 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_30">
    <path d="M 291.918347 187.118437 
L 301.602645 187.118437 
L 301.602645 123.012812 
L 291.918347 123.012812 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_31">
    <path d="M 301.602645 187.118437 
L 311.286942 187.118437 
L 311.286942 128.7414 
L 301.602645 128.7414 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_32">
    <path d="M 311.286942 187.118437 
L 320.97124 187.118437 
L 320.97124 138.379976 
L 311.286942 138.379976 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_33">
    <path d="M 320.97124 187.118437 
L 330.655537 187.118437 
L 330.655537 141.289735 
L 320.97124 141.289735 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_34">
    <path d="M 330.655537 187.118437 
L 340.339835 187.118437 
L 340.339835 144.381354 
L 330.655537 144.381354 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_35">
    <path d="M 340.339835 187.118437 
L 350.024132 187.118437 
L 350.024132 150.382731 
L 340.339835 150.382731 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_36">
    <path d="M 350.024132 187.118437 
L 359.70843 187.118437 
L 359.70843 149.928082 
L 350.024132 149.928082 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_37">
    <path d="M 359.70843 187.118437 
L 369.392727 187.118437 
L 369.392727 153.65621 
L 359.70843 153.65621 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_38">
    <path d="M 369.392727 187.118437 
L 379.077025 187.118437 
L 379.077025 154.20179 
L 369.392727 154.20179 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_39">
    <path d="M 379.077025 187.118437 
L 388.761322 187.118437 
L 388.761322 155.20202 
L 379.077025 155.20202 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_40">
    <path d="M 388.761322 187.118437 
L 398.44562 187.118437 
L 398.44562 156.929689 
L 388.761322 156.929689 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_41">
    <path d="M 398.44562 187.118437 
L 408.129917 187.118437 
L 408.129917 157.566199 
L 398.44562 157.566199 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_42">
    <path d="M 408.129917 187.118437 
L 417.814215 187.118437 
L 417.814215 155.838529 
L 408.129917 155.838529 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_43">
    <path d="M 417.814215 187.118437 
L 427.498512 187.118437 
L 427.498512 159.475728 
L 417.814215 159.475728 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_44">
    <path d="M 427.498512 187.118437 
L 437.18281 187.118437 
L 437.18281 156.838759 
L 427.498512 156.838759 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_45">
    <path d="M 437.18281 187.118437 
L 446.867107 187.118437 
L 446.867107 160.021308 
L 437.18281 160.021308 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_46">
    <path d="M 446.867107 187.118437 
L 456.551405 187.118437 
L 456.551405 161.112467 
L 446.867107 161.112467 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_47">
    <path d="M 456.551405 187.118437 
L 466.235702 187.118437 
L 466.235702 160.294098 
L 456.551405 160.294098 
z
" clip-path="url(#p3735033c02)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_7">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="272.549752" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="272.549752" y="201.716094" transform="rotate(-0 272.549752 201.716094)">0.0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="311.286942" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="311.286942" y="201.716094" transform="rotate(-0 311.286942 201.716094)">0.2</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="350.024132" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.024132" y="201.716094" transform="rotate(-0 350.024132 201.716094)">0.4</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="388.761322" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="388.761322" y="201.716094" transform="rotate(-0 388.761322 201.716094)">0.6</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="427.498512" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="427.498512" y="201.716094" transform="rotate(-0 427.498512 201.716094)">0.8</text>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="466.235702" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="466.235702" y="201.716094" transform="rotate(-0 466.235702 201.716094)">1.0</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="215.97" transform="rotate(-0 369.392727 215.97)">p değeri</text>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_14">
    <path d="M 282.23405 187.118437 
L 282.23405 20.798437 
" clip-path="url(#p3735033c02)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_48">
    <path d="M 262.865455 187.118437 
L 262.865455 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_49">
    <path d="M 475.92 187.118437 
L 475.92 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_50">
    <path d="M 262.865455 187.118437 
L 475.92 187.118437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_51">
    <path d="M 262.865455 20.798437 
L 475.92 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="14.798438" transform="rotate(-0 369.392727 14.798438)">Gerçek fark: %10</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6148996116">
   <rect x="7.2" y="20.798438" width="213.054545" height="166.32"/>
  </clipPath>
  <clipPath id="p3735033c02">
   <rect x="262.865455" y="20.798438" width="213.054545" height="166.32"/>
  </clipPath>
 </defs>
</svg>
<figcaption>10 000'er testin p değerleri. Turuncu çizgi 0,05. Fark yokken p düzgün dağılıyor; fark varken sola yığılıyor ama yine her yere yayılıyor.</figcaption>
</figure>

## Yanlış okuma 1: "p, H₀'ın doğru olma olasılığıdır"

Bir ekip 2000 fikir deniyor. Gerçekte fikirlerin yalnızca onda biri işe
yarıyor (%10 uzatıyor), gerisi hiçbir şey değiştirmiyor. Her fikir 100'er
kişiyle sınanıyor. "Anlamlı" çıkan sonuçların kaçı gerçekten işe yarayan
fikir?

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(92)
for n in [100, 400]:
    works = rng.random(2000) < 0.10
    lift = np.where(works, 1.10, 1.0)[:, None]
    a = rng.choice(x, size=(2000, n))
    b = rng.choice(x, size=(2000, n)) * lift
    sig = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue < 0.05
    false_hits = (sig & ~works).sum()
    print(n, works.sum(), sig.sum(), false_hits, round(false_hits / sig.sum(), 2))
```

```text
100 212 113 80 0.71
400 195 212 102 0.48
```

Sütunlar: kişi sayısı, gerçekten işe yarayan fikir, anlamlı çıkan sonuç,
bunların içinde işe yaramayan ve pay.

- 100 kişilik testlerde anlamlı çıkan sonuç sayısı 113; bunlardan
  80 tanesi aslında **hiçbir şey yapmayan** fikirlerdi: payları
  %71. Her biri p < 0,05 idi.
- 400 kişide güç arttı ve yanlış sonuçların payı %48 oldu; daha
  az, ama yine de küçümsenecek gibi değil.
- Ders: p < 0,05 "bu sonucun yanlış olma olasılığı %5" **demek değil**. O
  olasılık p'ye ek olarak iki şeye bağlı: denenen fikirlerin ne kadarının
  gerçekten işe yaradığı ve testin gücü. İkisi de düşükse "anlamlı"
  sonuçların çoğu yanlış alarmdır.

## Yanlış okuma 2: "Küçük p, büyük etki demektir"

Çok büyük bir örneklemde çok küçük bir fark bile "son derece anlamlı" olur:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(93)
a = rng.choice(x, size=100000)
b = rng.choice(x, size=100000) * 1.01
result = stats.ttest_ind(b, a, equal_var=False)
print(f"{result.pvalue:.1e}", round(b.mean() - a.mean(), 3))
```

```text
1.0e-07 0.146
```

p yaklaşık on milyonda bir; fark ise oturum başına 0,146
dakika, yani 10 saniyeden az. İstatistiksel olarak kesin, pratikte önemsiz
olabilir. p "fark sıfır mı?" sorusuna cevap verir; "fark önemli mi?"
sorusuna değil. Ona **etki büyüklüğü** (effect size) cevap verir; ayrı bir
bölümü var.

## Yanlış okuma 3: "20 şeye baktım, biri anlamlı çıktı"

Bir deneyde 20 farklı metriğe (oturum süresi, tıklama, sepet, ...) bakıldığını
düşün; hiçbirinde gerçek fark yok. En az birinin p < 0,05 çıkma olasılığı?

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(94)
hits = 0
for _ in range(2000):
    a = rng.choice(x, size=(20, 50))
    b = rng.choice(x, size=(20, 50))
    p = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
    hits += (p < 0.05).any()
print(round(hits / 2000, 3), round(1 - 0.95 ** 20, 3))
```

```text
0.626 0.642
```

- 2000 deneyin %62,6 kadarında 20 metrikten en az biri "anlamlı"
  çıktı. Formül $1 - 0{,}95^{20} \approx 0{,}64$ de aynısını söylüyor.
- Sonra yalnızca o metriği raporlamak, ya da anlamlı çıkana kadar veriyi
  farklı biçimlerde kesmek **p-hacking** (p avcılığı) diye bilinir ve
  yanlış sonuç üretmenin en kısa yoludur. Çaresi: hangi metriğe bakılacağını
  önceden yazmak ya da çoklu karşılaştırma düzeltmesi (ikinci modülde).

## Doğru okuma

p değeri tek başına şunu söyler: "Fark olmasaydı bu veri ne kadar
şaşırtıcı olurdu?" Raporda yanına her zaman koy:

- farkın kendisi ve güven aralığı (ne kadar?),
- örneklem büyüklüğü ve güç (kaçırma şansı neydi?),
- kaç şeye bakıldığı (kaç kez denendi?).

Ve şunlardan kaçın: p = 0,049'u "kesin var", p = 0,051'i "kesin yok" diye
okumak. İkisi neredeyse aynı kanıttır; 0,05 bir karar eşiğidir, doğanın
bir sınırı değil.

## Özet

- Fark yokken p düzgün dağılır; her yirmi testte bir "anlamlı" çıkar.
- p, $H_0$'ın doğru olma olasılığı değildir; "anlamlı" sonuçların ne kadarının
  doğru olduğu güce ve denenen fikirlerin isabetine bağlıdır.
- Küçük p büyük etki demek değildir; büyük örneklemde önemsiz fark da
  anlamlı çıkar.
- p tekrarlanabilirliği ölçmez; aynı deney çok farklı p'ler verebilir.
- Çok şeye bakıp anlamlı olanı seçmek yanlış alarmları çoğaltır.
