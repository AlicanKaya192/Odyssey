# Betimsel İstatistik

100 000 kullanıcının oturum süresini tek tek okuyamazsın. Önce veriyi birkaç
sayıyla **özetlemek** gerekir: tipik değer ne, değerler ne kadar dağınık,
aykırı olan var mı? Bu özet sayılara **betimsel istatistik** (descriptive
statistics) denir. Çıkarımın bütün araçları bu sayıların üstüne kuruluyor:
güven aralığı bir ortalamanın, hipotez testi bir sapmanın etrafında çalışır.
O yüzden önce onları doğru hesaplamayı ve doğru okumayı öğreniyoruz.

## Merkez: ortalama ve medyan

- **Ortalama** (mean): değerlerin toplamı bölü sayısı.
- **Medyan** (median): değerler sıralanınca tam ortadaki değer; yarısı
  altında, yarısı üstünde.
- **Tepe değer** (mode): en sık görülen değer; sayı gibi değil, kategori
  gibi davranan veride (ziyaret sayısı gibi) işe yarar.

Formülle ortalama:

$$\bar{x} = \dfrac{x_1 + x_2 + \dots + x_n}{n} = \dfrac{1}{n}\sum_{i=1}^{n} x_i$$

$\sum$ ("sigma") "hepsini topla" demek; $x_i$ $i$'nci değer.

```python
from ab_data import make_population

users = make_population()
for col in ["minutes", "load_ms"]:
    x = users[col]
    print(col, round(x.mean(), 2), round(x.median(), 2))
print(users["visits"].mode()[0])
```

```text
minutes 9.04 7.49
load_ms 849.75 850.0
3
```

- Sayfa açılış süresinde (`load_ms`) ortalama ve medyan neredeyse aynı:
  değerler ortanın iki yanına eşit dağılmış.
- Oturum süresinde ortalama (9,04) medyandan (7,49)
  belirgin büyük. Birkaç çok uzun oturum ortalamayı yukarı çekiyor; tipik
  kullanıcı ortalamanın söylediğinden kısa kalıyor.
- En sık görülen ziyaret sayısı 3.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="451.450781pt" height="222.808781pt" viewBox="0 0 451.450781 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 451.450781 222.808781 
L 451.450781 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 53.650781 184.608 
L 444.250781 184.608 
L 444.250781 7.2 
L 53.650781 7.2 
L 53.650781 184.608 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 71.405327 184.608 
L 75.843963 184.608 
L 75.843963 182.219063 
L 71.405327 182.219063 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_4">
    <path d="M 75.843963 184.608 
L 80.282599 184.608 
L 80.282599 171.517936 
L 75.843963 171.517936 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_5">
    <path d="M 80.282599 184.608 
L 84.721236 184.608 
L 84.721236 146.974066 
L 80.282599 146.974066 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_6">
    <path d="M 84.721236 184.608 
L 89.159872 184.608 
L 89.159872 113.136251 
L 84.721236 113.136251 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_7">
    <path d="M 89.159872 184.608 
L 93.598509 184.608 
L 93.598509 81.261945 
L 89.159872 81.261945 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_8">
    <path d="M 93.598509 184.608 
L 98.037145 184.608 
L 98.037145 57.176228 
L 93.598509 57.176228 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_9">
    <path d="M 98.037145 184.608 
L 102.475781 184.608 
L 102.475781 35.610347 
L 98.037145 35.610347 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_10">
    <path d="M 102.475781 184.608 
L 106.914418 184.608 
L 106.914418 24.025641 
L 102.475781 24.025641 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_11">
    <path d="M 106.914418 184.608 
L 111.353054 184.608 
L 111.353054 17.74241 
L 106.914418 17.74241 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_12">
    <path d="M 111.353054 184.608 
L 115.79169 184.608 
L 115.79169 17.022457 
L 111.353054 17.022457 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_13">
    <path d="M 115.79169 184.608 
L 120.230327 184.608 
L 120.230327 15.648 
L 115.79169 15.648 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_14">
    <path d="M 120.230327 184.608 
L 124.668963 184.608 
L 124.668963 23.927465 
L 120.230327 23.927465 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_15">
    <path d="M 124.668963 184.608 
L 129.107599 184.608 
L 129.107599 35.872149 
L 124.668963 35.872149 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_16">
    <path d="M 129.107599 184.608 
L 133.546236 184.608 
L 133.546236 36.853904 
L 129.107599 36.853904 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_17">
    <path d="M 133.546236 184.608 
L 137.984872 184.608 
L 137.984872 48.209534 
L 133.546236 48.209534 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_18">
    <path d="M 137.984872 184.608 
L 142.423509 184.608 
L 142.423509 57.045327 
L 137.984872 57.045327 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_19">
    <path d="M 142.423509 184.608 
L 146.862145 184.608 
L 146.862145 69.808139 
L 142.423509 69.808139 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_20">
    <path d="M 146.862145 184.608 
L 151.300781 184.608 
L 151.300781 77.727628 
L 146.862145 77.727628 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_21">
    <path d="M 151.300781 184.608 
L 155.739418 184.608 
L 155.739418 84.665362 
L 151.300781 84.665362 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_22">
    <path d="M 155.739418 184.608 
L 160.178054 184.608 
L 160.178054 91.472195 
L 155.739418 91.472195 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_23">
    <path d="M 160.178054 184.608 
L 164.61669 184.608 
L 164.61669 101.224293 
L 160.178054 101.224293 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_24">
    <path d="M 164.61669 184.608 
L 169.055327 184.608 
L 169.055327 108.620179 
L 164.61669 108.620179 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_25">
    <path d="M 169.055327 184.608 
L 173.493963 184.608 
L 173.493963 116.114241 
L 169.055327 116.114241 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_26">
    <path d="M 173.493963 184.608 
L 177.932599 184.608 
L 177.932599 119.746733 
L 173.493963 119.746733 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_27">
    <path d="M 177.932599 184.608 
L 182.371236 184.608 
L 182.371236 126.25904 
L 177.932599 126.25904 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_28">
    <path d="M 182.371236 184.608 
L 186.809872 184.608 
L 186.809872 131.069639 
L 182.371236 131.069639 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_29">
    <path d="M 186.809872 184.608 
L 191.248509 184.608 
L 191.248509 136.436565 
L 186.809872 136.436565 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_30">
    <path d="M 191.248509 184.608 
L 195.687145 184.608 
L 195.687145 140.134508 
L 191.248509 140.134508 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_31">
    <path d="M 195.687145 184.608 
L 200.125781 184.608 
L 200.125781 146.875891 
L 195.687145 146.875891 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_32">
    <path d="M 200.125781 184.608 
L 204.564418 184.608 
L 204.564418 149.003026 
L 200.125781 149.003026 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_33">
    <path d="M 204.564418 184.608 
L 209.003054 184.608 
L 209.003054 151.195612 
L 204.564418 151.195612 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_34">
    <path d="M 209.003054 184.608 
L 213.44169 184.608 
L 213.44169 154.304502 
L 209.003054 154.304502 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_35">
    <path d="M 213.44169 184.608 
L 217.880327 184.608 
L 217.880327 156.366187 
L 213.44169 156.366187 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_36">
    <path d="M 217.880327 184.608 
L 222.318963 184.608 
L 222.318963 160.031405 
L 217.880327 160.031405 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_37">
    <path d="M 222.318963 184.608 
L 226.757599 184.608 
L 226.757599 160.914984 
L 222.318963 160.914984 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_38">
    <path d="M 226.757599 184.608 
L 231.196236 184.608 
L 231.196236 162.780318 
L 226.757599 162.780318 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_39">
    <path d="M 231.196236 184.608 
L 235.634872 184.608 
L 235.634872 165.431056 
L 231.196236 165.431056 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_40">
    <path d="M 235.634872 184.608 
L 240.073509 184.608 
L 240.073509 167.885443 
L 235.634872 167.885443 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_41">
    <path d="M 240.073509 184.608 
L 244.512145 184.608 
L 244.512145 168.867198 
L 240.073509 168.867198 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_42">
    <path d="M 244.512145 184.608 
L 248.950781 184.608 
L 248.950781 169.947128 
L 244.512145 169.947128 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_43">
    <path d="M 248.950781 184.608 
L 253.389418 184.608 
L 253.389418 172.36879 
L 248.950781 172.36879 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_44">
    <path d="M 253.389418 184.608 
L 257.828054 184.608 
L 257.828054 173.677797 
L 253.389418 173.677797 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_45">
    <path d="M 257.828054 184.608 
L 262.26669 184.608 
L 262.26669 173.645071 
L 257.828054 173.645071 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_46">
    <path d="M 262.26669 184.608 
L 266.705327 184.608 
L 266.705327 174.430475 
L 262.26669 174.430475 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_47">
    <path d="M 266.705327 184.608 
L 271.143963 184.608 
L 271.143963 175.543131 
L 266.705327 175.543131 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_48">
    <path d="M 271.143963 184.608 
L 275.582599 184.608 
L 275.582599 176.36126 
L 271.143963 176.36126 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_49">
    <path d="M 275.582599 184.608 
L 280.021236 184.608 
L 280.021236 176.819412 
L 275.582599 176.819412 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_50">
    <path d="M 280.021236 184.608 
L 284.459872 184.608 
L 284.459872 177.408465 
L 280.021236 177.408465 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_51">
    <path d="M 284.459872 184.608 
L 288.898509 184.608 
L 288.898509 177.50664 
L 284.459872 177.50664 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_52">
    <path d="M 288.898509 184.608 
L 293.337145 184.608 
L 293.337145 177.50664 
L 288.898509 177.50664 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_53">
    <path d="M 293.337145 184.608 
L 297.775781 184.608 
L 297.775781 179.895577 
L 293.337145 179.895577 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_54">
    <path d="M 297.775781 184.608 
L 302.214418 184.608 
L 302.214418 179.568325 
L 297.775781 179.568325 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_55">
    <path d="M 302.214418 184.608 
L 306.653054 184.608 
L 306.653054 179.5356 
L 302.214418 179.5356 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_56">
    <path d="M 306.653054 184.608 
L 311.09169 184.608 
L 311.09169 180.713706 
L 306.653054 180.713706 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_57">
    <path d="M 311.09169 184.608 
L 315.530327 184.608 
L 315.530327 180.615531 
L 311.09169 180.615531 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_58">
    <path d="M 315.530327 184.608 
L 319.968963 184.608 
L 319.968963 181.008232 
L 315.530327 181.008232 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_59">
    <path d="M 319.968963 184.608 
L 324.407599 184.608 
L 324.407599 180.942782 
L 319.968963 180.942782 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_60">
    <path d="M 324.407599 184.608 
L 328.846236 184.608 
L 328.846236 181.171858 
L 324.407599 181.171858 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_61">
    <path d="M 328.846236 184.608 
L 333.284872 184.608 
L 333.284872 181.760911 
L 328.846236 181.760911 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_62">
    <path d="M 333.284872 184.608 
L 337.723509 184.608 
L 337.723509 182.088163 
L 333.284872 182.088163 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_63">
    <path d="M 337.723509 184.608 
L 342.162145 184.608 
L 342.162145 182.448139 
L 337.723509 182.448139 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_64">
    <path d="M 342.162145 184.608 
L 346.600781 184.608 
L 346.600781 182.448139 
L 342.162145 182.448139 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_65">
    <path d="M 346.600781 184.608 
L 351.039418 184.608 
L 351.039418 182.546315 
L 346.600781 182.546315 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_66">
    <path d="M 351.039418 184.608 
L 355.478054 184.608 
L 355.478054 182.448139 
L 351.039418 182.448139 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_67">
    <path d="M 355.478054 184.608 
L 359.91669 184.608 
L 359.91669 182.382689 
L 355.478054 182.382689 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_68">
    <path d="M 359.91669 184.608 
L 364.355327 184.608 
L 364.355327 182.775391 
L 359.91669 182.775391 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_69">
    <path d="M 364.355327 184.608 
L 368.793963 184.608 
L 368.793963 183.102643 
L 364.355327 183.102643 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_70">
    <path d="M 368.793963 184.608 
L 373.232599 184.608 
L 373.232599 182.840841 
L 368.793963 182.840841 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_71">
    <path d="M 373.232599 184.608 
L 377.671236 184.608 
L 377.671236 183.069917 
L 373.232599 183.069917 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_72">
    <path d="M 377.671236 184.608 
L 382.109872 184.608 
L 382.109872 183.135368 
L 377.671236 183.135368 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_73">
    <path d="M 382.109872 184.608 
L 386.548509 184.608 
L 386.548509 183.364444 
L 382.109872 183.364444 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_74">
    <path d="M 386.548509 184.608 
L 390.987145 184.608 
L 390.987145 183.65897 
L 386.548509 183.65897 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_75">
    <path d="M 390.987145 184.608 
L 395.425781 184.608 
L 395.425781 183.560795 
L 390.987145 183.560795 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_76">
    <path d="M 395.425781 184.608 
L 399.864418 184.608 
L 399.864418 183.626245 
L 395.425781 183.626245 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_77">
    <path d="M 399.864418 184.608 
L 404.303054 184.608 
L 404.303054 183.52807 
L 399.864418 183.52807 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_78">
    <path d="M 404.303054 184.608 
L 408.74169 184.608 
L 408.74169 183.495345 
L 404.303054 183.495345 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_79">
    <path d="M 408.74169 184.608 
L 413.180327 184.608 
L 413.180327 183.331719 
L 408.74169 183.331719 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_80">
    <path d="M 413.180327 184.608 
L 417.618963 184.608 
L 417.618963 183.822596 
L 413.180327 183.822596 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_81">
    <path d="M 417.618963 184.608 
L 422.057599 184.608 
L 422.057599 183.691696 
L 417.618963 183.691696 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_82">
    <path d="M 422.057599 184.608 
L 426.496236 184.608 
L 426.496236 183.888046 
L 422.057599 183.888046 
z
" clip-path="url(#p6c98d2d907)" style="fill: #8b5cf6; opacity: 0.8"/>
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
       <use xlink:href="#m15aed4d867" x="66.452245" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="66.452245" y="199.205656" transform="rotate(-0 66.452245 199.205656)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="111.480258" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="111.480258" y="199.205656" transform="rotate(-0 111.480258 199.205656)">5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="156.508271" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="156.508271" y="199.205656" transform="rotate(-0 156.508271 199.205656)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="201.536284" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="201.536284" y="199.205656" transform="rotate(-0 201.536284 199.205656)">15</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="246.564297" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="246.564297" y="199.205656" transform="rotate(-0 246.564297 199.205656)">20</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="291.592309" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="291.592309" y="199.205656" transform="rotate(-0 291.592309 199.205656)">25</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="336.620322" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="336.620322" y="199.205656" transform="rotate(-0 336.620322 199.205656)">30</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="381.648335" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="381.648335" y="199.205656" transform="rotate(-0 381.648335 199.205656)">35</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="426.676348" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="426.676348" y="199.205656" transform="rotate(-0 426.676348 199.205656)">40</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="248.950781" y="213.206437" transform="rotate(-0 248.950781 213.206437)">Oturum süresi (dakika)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_10">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="188.406828" transform="rotate(-0 46.650781 188.406828)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="151.88284" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="155.681668" transform="rotate(-0 46.650781 155.681668)">1000</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="119.15768" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="122.956509" transform="rotate(-0 46.650781 122.956509)">2000</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="86.432521" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="90.231349" transform="rotate(-0 46.650781 90.231349)">3000</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="53.707361" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="57.506189" transform="rotate(-0 46.650781 57.506189)">4000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="20.982201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="24.781029" transform="rotate(-0 46.650781 24.781029)">5000</text>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="95.904" transform="rotate(-90 14.798438 95.904)">Kullanıcı sayısı</text>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 133.904208 184.608 
L 133.904208 7.2 
" clip-path="url(#p6c98d2d907)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="line2d_17">
    <path d="M 147.885113 184.608 
L 147.885113 7.2 
" clip-path="url(#p6c98d2d907)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_83">
    <path d="M 53.650781 184.608 
L 53.650781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_84">
    <path d="M 444.250781 184.608 
L 444.250781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_85">
    <path d="M 53.650781 184.608 
L 444.250781 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_86">
    <path d="M 53.650781 7.2 
L 444.250781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="line2d_18">
     <path d="M 362.197656 20.298437 
L 372.197656 20.298437 
L 382.197656 20.298437 
" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="390.197656" y="23.798437" transform="rotate(-0 390.197656 23.798437)">medyan</text>
    </g>
    <g id="line2d_19">
     <path d="M 362.197656 35.299219 
L 372.197656 35.299219 
L 382.197656 35.299219 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="390.197656" y="38.799219" transform="rotate(-0 390.197656 38.799219)">ortalama</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6c98d2d907">
   <rect x="53.650781" y="7.2" width="390.6" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Oturum sürelerinin dağılımı (40 dakikanın altı). Uzun sağ kuyruk ortalamayı (turuncu) medyanın (kesik çizgi) sağına çekiyor.</figcaption>
</figure>

Uzun kuyruğu sağa doğru uzanan bu şekle **sağa çarpık** (right-skewed)
dağılım denir. Süre, para ve gelir gibi sıfırın altına inemeyen ama çok
büyüyebilen ölçümlerde çok sık görülür.

## Aykırı değer ortalamayı çeker, medyanı çekmez

```python
import numpy as np

minutes = np.array([4.1, 5.0, 5.6, 6.2, 6.9, 7.4, 8.0, 9.3, 11.2, 12.5])
print(round(minutes.mean(), 2), np.median(minutes))
with_outlier = np.append(minutes, 240.0)   # uygulama açık unutulmuş
print(round(with_outlier.mean(), 2), np.median(with_outlier))
```

```text
7.62 7.15
28.75 7.4
```

- Tek bir 240 dakikalık oturum eklenince ortalama 7,62 iken
  28,75 oldu. Medyan ise 7,15 iken 7,4
  oldu; neredeyse kıpırdamadı.
- Medyan aykırılara **dayanıklıdır** (robust). "Tipik kullanıcı" soruluyorsa
  medyan daha dürüst. "Toplam ne kadar zaman harcandı" soruluyorsa ortalama
  gerekir; çünkü ortalama × kişi sayısı = toplam.

## Yayılım: değerler ne kadar dağınık?

İki grubun ortalaması aynı olabilir ama biri çok tutarlı, öteki çok dağınık
olabilir. Yayılımı ölçen sayılar:

- **Açıklık** (range): en büyük eksi en küçük. Tek bir aykırı değer onu
  bozar.
- **Varyans** (variance): her değerin ortalamadan uzaklığının karesinin
  ortalaması.
- **Standart sapma** (standard deviation): varyansın karekökü. Verinin
  kendi biriminde (milisaniye) olduğu için okuması kolaydır.
- **Çeyrekler arası açıklık** (interquartile range, IQR): ortadaki
  yarının genişliği, yani 75. yüzdelik eksi 25. yüzdelik. Aykırılara
  dayanıklı.

Örneklem varyansı ve standart sapması:

$$s^2 = \dfrac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2 \qquad s = \sqrt{s^2}$$

```python
import numpy as np
from ab_data import make_population

users = make_population()
x = users["load_ms"]
print(x.max() - x.min())
print(round(x.var(), 1), round(x.std(), 1))
q1, q3 = np.percentile(x, [25, 75])
print(q1, q3, q3 - q1)
print(np.percentile(x, 95))
```

```text
974
14462.8 120.3
769.0 931.0 162.0
1048.0
```

- Açılış süreleri 974 milisaniyelik bir aralığa yayılmış ama bu
  sayı yalnızca en uç iki kullanıcıya bakıyor.
- Standart sapma 120,3 ms: tipik bir kullanıcı ortalamadan aşağı
  yukarı bu kadar uzakta.
- Kullanıcıların ortadaki yarısı 769 ile 931 ms arasında
  (IQR 162).
- **Yüzdelik** (percentile): değerlerin yüzde kaçının altında kaldığı sınır.
  95. yüzdelik 1 048 ms: kullanıcıların %95'i bundan hızlı. Hız
  ölçümlerinde ortalama yerine sık sık bu kullanılır.

## Neden n değil de n − 1?

Varyans formülünde $n$ yerine $n-1$'e bölünmesi ilk bakışta tuhaf görünür.
Sebebi şu: sapmaları gerçek ortalamaya ($\mu$) göre değil, **örneklemin
kendi** ortalamasına ($\bar{x}$) göre ölçüyoruz. $\bar{x}$ zaten bu
değerlerin tam ortasına oturduğu için uzaklıklar olduğundan biraz küçük
çıkar. $n-1$'e bölmek bunu telafi eder. Sözle ikna olmak zor; ölçelim.

NumPy ve pandas burada farklı davranır, önce onu görelim:

```python
import numpy as np

values = np.array([2.0, 4.0, 4.0, 5.0, 7.0, 9.0])
print(round(values.std(), 3), round(values.std(ddof=1), 3))
```

```text
2.267 2.483
```

- NumPy'nin `std()` ve `var()` fonksiyonları varsayılan olarak $n$'e böler.
  `ddof=1` ("delta degrees of freedom", serbestlik derecesinden çıkarılan)
  verince $n-1$'e böler.
- pandas'ın `std()` ve `var()` fonksiyonları varsayılan olarak **zaten**
  $n-1$'e böler. Aynı veride iki kütüphane farklı sayı verebilir; hangisini
  kullandığını bil.

Şimdi gerçeği bildiğimiz bir dağılımdan (sapması 120, yani varyansı
14 400) 20 000 kez 5'er değer çekip iki formülün ortalamasına bakalım:

```python
import numpy as np

rng = np.random.default_rng(1)
v0, v1 = [], []
for _ in range(20000):
    s = rng.normal(850, 120, size=5)
    v0.append(s.var())           # n'e böl
    v1.append(s.var(ddof=1))     # n - 1'e böl
print(120 ** 2, round(np.mean(v0)), round(np.mean(v1)))
```

```text
14400 11486 14358
```

- $n$'e bölen formül ortalamada 11 486 verdi: gerçeğin yaklaşık beşte
  dördü. Beş kişilik örneklemde $\dfrac{n-1}{n} = \dfrac{4}{5}$ oranında hep
  **eksik** tahmin ediyor.
- $n-1$'e bölen formül 14 358 verdi: gerçeğin çevresinde. Tek tek
  örneklemler yine iki yana oynar ama ortalamada yanlılık yok.
- Örneklem büyüdükçe fark önemsizleşir (10 000 kişide $\dfrac{9999}{10000}$),
  ama küçük örneklemde gerçek bir fark.

## z puanı: "ortalamadan kaç sapma uzakta?"

Bir değerin tek başına büyük mü küçük mü olduğunu söylemek için onu
ortalamaya ve sapmaya göre ölçeriz:

$$z = \dfrac{x - \bar{x}}{s}$$

```python
from ab_data import make_population

users = make_population()
x = users["load_ms"]
z = (x - x.mean()) / x.std()
print(x.iloc[0], round(z.iloc[0], 2))
print(round((z.abs() > 2).mean(), 3), round((z.abs() > 3).mean(), 4))
```

```text
813 -0.31
0.046 0.0029
```

- İlk kullanıcının sayfaları 813 ms'de açılıyor; z puanı
  -0,31: ortalamanın biraz altında, sıradan bir değer.
- Ortalamadan 2 sapmadan fazla uzakta olan kullanıcıların payı
  %4,6, 3 sapmadan fazla uzakta olanlarınki yalnızca %0,29.
  Bu oranlar çan biçimli veriye
  özgü; bir sonraki bölümde normal dağılımla nereden geldiklerini göreceğiz.

## Aykırı değer kuralı: 1,5 × IQR

Çarpık veride "3 sapma" kuralı iyi çalışmaz, çünkü uzun kuyruk sapmayı
şişirir. Yaygın kural: üçüncü çeyrekten 1,5 IQR'den fazla yukarıda (ya da
birinci çeyrekten 1,5 IQR'den fazla aşağıda) olan değer aykırı sayılır.

```python
from ab_data import make_population

users = make_population()
q1, q3 = users["minutes"].quantile([0.25, 0.75])
upper = q3 + 1.5 * (q3 - q1)
print(round(upper, 2), (users["minutes"] > upper).sum())
```

```text
20.92 4680
```

- 20,92 dakikadan uzun 4 680 oturum kuralın dışında kaldı.
- "Aykırı" **silinecek** demek değildir. Bu oturumlar gerçek kullanıcılar
  olabilir. Önce nedenine bak (ölçüm hatası mı, gerçek davranış mı), sonra
  karar ver ve raporda ne yaptığını yaz.

## Özet

- Merkez: ortalama (toplamla ilişkili, aykırıya duyarlı) ve medyan (tipik
  değer, aykırıya dayanıklı). Çarpık veride ikisi ayrışır.
- Yayılım: standart sapma (ortalamaya göre), IQR ve yüzdelikler (sıraya
  göre, dayanıklı).
- Örneklem varyansı $n-1$'e bölünür; NumPy'de `ddof=1` yazılır, pandas
  bunu varsayılan yapar.
- z puanı bir değeri "kaç sapma uzakta" diye ölçer; aykırı aramak için
  çarpık veride 1,5 × IQR kuralı daha güvenilir.
