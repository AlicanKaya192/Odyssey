# Hipotez Testinin Mantığı

Sunucu ekibi altyapıyı değiştirdi. Değişiklikten sonra 40 sayfa açılışını
ölçtün; ortalama 850 ms'den biraz daha yüksek çıktı. Sayfalar gerçekten mi
yavaşladı, yoksa bu fark rastgele 40 ölçümün doğal oynaması mı? Bu soruyu
düzenli biçimde cevaplamanın yoluna **hipotez testi** (hypothesis test)
denir. Önce neden gerekli olduğunu görelim: ölçümler her zaman oynar; ilk
bölümde aynı evrenden çekilen beş örneklemin beş farklı ortalama verdiğini
gördük. "Fark var" demek için farkın **şansla açıklanamayacak kadar büyük**
olduğunu göstermek gerekir.

## Veri

```python
from ab_data import make_speed_test

loads = make_speed_test()
print(len(loads), round(loads.mean(), 1), round(loads.std(ddof=1), 1))
```

```text
40 883.2 123.5
```

40 ölçümün ortalaması 883,2 ms; değişiklikten önceki ortalama
850 ms. Fark 33,2 ms.

## İki hipotez

Test iki cümleyle başlar:

- **Sıfır hipotezi** (null hypothesis, $H_0$): "Hiçbir şey değişmedi." Gerçek
  ortalama hâlâ 850 ms; gördüğümüz fark şanstan.
- **Alternatif hipotez** (alternative hypothesis, $H_1$): "Bir şey değişti."
  Gerçek ortalama 850 ms değil.

Test $H_0$'ı **kanıtlamaya** çalışmaz. Şunu sorar: "$H_0$ doğru olsaydı,
en az bu kadar büyük bir fark görmek ne kadar olası olurdu?" Cevap çok
küçükse $H_0$'a inanmak zorlaşır.

<figure class="fig">
<div class="flow">
<span class="node">H₀'ı yaz</span>
<span class="arrow">→</span>
<span class="node">H₀ dünyasını kur</span>
<span class="arrow">→</span>
<span class="node">Veriyi onunla karşılaştır</span>
<span class="arrow">→</span>
<span class="node acc">Karar</span>
</div>
<figcaption>Hipotez testinin dört adımı. "H₀ dünyası": hiçbir şey değişmeseydi
ölçümlerin nasıl dağılacağı.</figcaption>
</figure>

## H₀ dünyasını benzetimle kurmak

Evren elimizde: değişiklikten önceki bütün açılış süreleri. Hiçbir şey
değişmeseydi 40'lık örneklemler oradan gelirdi. 20 000 tane çekip kaçının
ortalamasının 850'den **en az bizimki kadar uzak** düştüğünü sayalım (iki
yöne de: daha hızlı ya da daha yavaş).

```python
import numpy as np
from ab_data import make_population, make_speed_test

old = make_population()["load_ms"].to_numpy()
loads = make_speed_test()
gap = abs(loads.mean() - 850)
rng = np.random.default_rng(71)
means = rng.choice(old, size=(20000, 40)).mean(axis=1)
far = np.abs(means - old.mean()) >= gap
print(round(far.mean(), 4))
```

```text
0.0797
```

Hiçbir şey değişmemiş bir dünyada bile 40'lık örneklemlerin yaklaşık
0,080 kadarı bu kadar uzak bir ortalama veriyor. Bu sayı
**p değeri**nin (p-value) ta kendisi: "$H_0$ doğruysa en az bu kadar uç bir
sonuç görme olasılığı".

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="405pt" height="223.061906pt" viewBox="0 0 405 223.061906" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 223.061906 
L 405 223.061906 
L 405 0 
L 0 0 
L 0 223.061906 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 184.608 
L 397.8 184.608 
L 397.8 7.2 
L 7.2 7.2 
L 7.2 184.608 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 24.954545 184.608 
L 29.886364 184.608 
L 29.886364 184.608 
L 24.954545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_4">
    <path d="M 29.886364 184.608 
L 34.818182 184.608 
L 34.818182 184.608 
L 29.886364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_5">
    <path d="M 34.818182 184.608 
L 39.75 184.608 
L 39.75 184.608 
L 34.818182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_6">
    <path d="M 39.75 184.608 
L 44.681818 184.608 
L 44.681818 184.608 
L 39.75 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_7">
    <path d="M 44.681818 184.608 
L 49.613636 184.608 
L 49.613636 184.608 
L 44.681818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_8">
    <path d="M 49.613636 184.608 
L 54.545455 184.608 
L 54.545455 184.608 
L 49.613636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_9">
    <path d="M 54.545455 184.608 
L 59.477273 184.608 
L 59.477273 184.608 
L 54.545455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_10">
    <path d="M 59.477273 184.608 
L 64.409091 184.608 
L 64.409091 184.608 
L 59.477273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_11">
    <path d="M 64.409091 184.608 
L 69.340909 184.608 
L 69.340909 184.608 
L 64.409091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_12">
    <path d="M 69.340909 184.608 
L 74.272727 184.608 
L 74.272727 184.608 
L 69.340909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_13">
    <path d="M 74.272727 184.608 
L 79.204545 184.608 
L 79.204545 184.608 
L 74.272727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_14">
    <path d="M 79.204545 184.608 
L 84.136364 184.608 
L 84.136364 184.608 
L 79.204545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_15">
    <path d="M 84.136364 184.608 
L 89.068182 184.608 
L 89.068182 184.608 
L 84.136364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_16">
    <path d="M 89.068182 184.608 
L 94 184.608 
L 94 184.608 
L 89.068182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_17">
    <path d="M 94 184.608 
L 98.931818 184.608 
L 98.931818 184.608 
L 94 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_18">
    <path d="M 98.931818 184.608 
L 103.863636 184.608 
L 103.863636 184.608 
L 98.931818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_19">
    <path d="M 103.863636 184.608 
L 108.795455 184.608 
L 108.795455 184.608 
L 103.863636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_20">
    <path d="M 108.795455 184.608 
L 113.727273 184.608 
L 113.727273 184.608 
L 108.795455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_21">
    <path d="M 113.727273 184.608 
L 118.659091 184.608 
L 118.659091 184.608 
L 113.727273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_22">
    <path d="M 118.659091 184.608 
L 123.590909 184.608 
L 123.590909 184.608 
L 118.659091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_23">
    <path d="M 123.590909 184.608 
L 128.522727 184.608 
L 128.522727 184.608 
L 123.590909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_24">
    <path d="M 128.522727 184.608 
L 133.454545 184.608 
L 133.454545 184.608 
L 128.522727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_25">
    <path d="M 133.454545 184.608 
L 138.386364 184.608 
L 138.386364 171.368597 
L 133.454545 171.368597 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_26">
    <path d="M 138.386364 184.608 
L 143.318182 184.608 
L 143.318182 142.368 
L 138.386364 142.368 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_27">
    <path d="M 143.318182 184.608 
L 148.25 184.608 
L 148.25 128.025313 
L 143.318182 128.025313 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_28">
    <path d="M 148.25 184.608 
L 153.181818 184.608 
L 153.181818 121.405612 
L 148.25 121.405612 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_29">
    <path d="M 153.181818 184.608 
L 158.113636 184.608 
L 158.113636 111.948896 
L 153.181818 111.948896 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_30">
    <path d="M 158.113636 184.608 
L 163.045455 184.608 
L 163.045455 101.073672 
L 158.113636 101.073672 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_31">
    <path d="M 163.045455 184.608 
L 167.977273 184.608 
L 167.977273 85.312478 
L 163.045455 85.312478 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_32">
    <path d="M 167.977273 184.608 
L 172.909091 184.608 
L 172.909091 76.170985 
L 167.977273 76.170985 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_33">
    <path d="M 172.909091 184.608 
L 177.840909 184.608 
L 177.840909 54.420537 
L 172.909091 54.420537 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_34">
    <path d="M 177.840909 184.608 
L 182.772727 184.608 
L 182.772727 40.86591 
L 177.840909 40.86591 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_35">
    <path d="M 182.772727 184.608 
L 187.704545 184.608 
L 187.704545 33.300537 
L 182.772727 33.300537 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_36">
    <path d="M 187.704545 184.608 
L 192.636364 184.608 
L 192.636364 15.805612 
L 187.704545 15.805612 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_37">
    <path d="M 192.636364 184.608 
L 197.568182 184.608 
L 197.568182 20.061134 
L 192.636364 20.061134 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_38">
    <path d="M 197.568182 184.608 
L 202.5 184.608 
L 202.5 19.588299 
L 197.568182 19.588299 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_39">
    <path d="M 202.5 184.608 
L 207.431818 184.608 
L 207.431818 15.648 
L 202.5 15.648 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_40">
    <path d="M 207.431818 184.608 
L 212.363636 184.608 
L 212.363636 21.637254 
L 207.431818 21.637254 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_41">
    <path d="M 212.363636 184.608 
L 217.295455 184.608 
L 217.295455 28.887403 
L 212.363636 28.887403 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_42">
    <path d="M 217.295455 184.608 
L 222.227273 184.608 
L 222.227273 34.246209 
L 217.295455 34.246209 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_43">
    <path d="M 222.227273 184.608 
L 227.159091 184.608 
L 227.159091 53.317254 
L 222.227273 53.317254 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_44">
    <path d="M 227.159091 184.608 
L 232.090909 184.608 
L 232.090909 55.523821 
L 227.159091 55.523821 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_45">
    <path d="M 232.090909 184.608 
L 237.022727 184.608 
L 237.022727 69.393672 
L 232.090909 69.393672 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_46">
    <path d="M 237.022727 184.608 
L 241.954545 184.608 
L 241.954545 83.89397 
L 237.022727 83.89397 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_47">
    <path d="M 241.954545 184.608 
L 246.886364 184.608 
L 246.886364 96.818149 
L 241.954545 96.818149 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_48">
    <path d="M 246.886364 184.608 
L 251.818182 184.608 
L 251.818182 105.486806 
L 246.886364 105.486806 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_49">
    <path d="M 251.818182 184.608 
L 256.75 184.608 
L 256.75 130.074269 
L 251.818182 130.074269 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_50">
    <path d="M 256.75 184.608 
L 261.681818 184.608 
L 261.681818 131.808 
L 256.75 131.808 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_51">
    <path d="M 261.681818 184.608 
L 266.613636 184.608 
L 266.613636 141.737552 
L 261.681818 141.737552 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_52">
    <path d="M 266.613636 184.608 
L 271.545455 184.608 
L 271.545455 177.830687 
L 266.613636 177.830687 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_53">
    <path d="M 271.545455 184.608 
L 276.477273 184.608 
L 276.477273 184.608 
L 271.545455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_54">
    <path d="M 276.477273 184.608 
L 281.409091 184.608 
L 281.409091 184.608 
L 276.477273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_55">
    <path d="M 281.409091 184.608 
L 286.340909 184.608 
L 286.340909 184.608 
L 281.409091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_56">
    <path d="M 286.340909 184.608 
L 291.272727 184.608 
L 291.272727 184.608 
L 286.340909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_57">
    <path d="M 291.272727 184.608 
L 296.204545 184.608 
L 296.204545 184.608 
L 291.272727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_58">
    <path d="M 296.204545 184.608 
L 301.136364 184.608 
L 301.136364 184.608 
L 296.204545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_59">
    <path d="M 301.136364 184.608 
L 306.068182 184.608 
L 306.068182 184.608 
L 301.136364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_60">
    <path d="M 306.068182 184.608 
L 311 184.608 
L 311 184.608 
L 306.068182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_61">
    <path d="M 311 184.608 
L 315.931818 184.608 
L 315.931818 184.608 
L 311 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_62">
    <path d="M 315.931818 184.608 
L 320.863636 184.608 
L 320.863636 184.608 
L 315.931818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_63">
    <path d="M 320.863636 184.608 
L 325.795455 184.608 
L 325.795455 184.608 
L 320.863636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_64">
    <path d="M 325.795455 184.608 
L 330.727273 184.608 
L 330.727273 184.608 
L 325.795455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_65">
    <path d="M 330.727273 184.608 
L 335.659091 184.608 
L 335.659091 184.608 
L 330.727273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_66">
    <path d="M 335.659091 184.608 
L 340.590909 184.608 
L 340.590909 184.608 
L 335.659091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_67">
    <path d="M 340.590909 184.608 
L 345.522727 184.608 
L 345.522727 184.608 
L 340.590909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_68">
    <path d="M 345.522727 184.608 
L 350.454545 184.608 
L 350.454545 184.608 
L 345.522727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_69">
    <path d="M 350.454545 184.608 
L 355.386364 184.608 
L 355.386364 184.608 
L 350.454545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_70">
    <path d="M 355.386364 184.608 
L 360.318182 184.608 
L 360.318182 184.608 
L 355.386364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_71">
    <path d="M 360.318182 184.608 
L 365.25 184.608 
L 365.25 184.608 
L 360.318182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_72">
    <path d="M 365.25 184.608 
L 370.181818 184.608 
L 370.181818 184.608 
L 365.25 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_73">
    <path d="M 370.181818 184.608 
L 375.113636 184.608 
L 375.113636 184.608 
L 370.181818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_74">
    <path d="M 375.113636 184.608 
L 380.045455 184.608 
L 380.045455 184.608 
L 375.113636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_75">
    <path d="M 24.954545 184.608 
L 29.886364 184.608 
L 29.886364 184.608 
L 24.954545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_76">
    <path d="M 29.886364 184.608 
L 34.818182 184.608 
L 34.818182 184.608 
L 29.886364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_77">
    <path d="M 34.818182 184.608 
L 39.75 184.608 
L 39.75 184.608 
L 34.818182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_78">
    <path d="M 39.75 184.608 
L 44.681818 184.608 
L 44.681818 184.608 
L 39.75 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_79">
    <path d="M 44.681818 184.608 
L 49.613636 184.608 
L 49.613636 184.608 
L 44.681818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_80">
    <path d="M 49.613636 184.608 
L 54.545455 184.608 
L 54.545455 184.608 
L 49.613636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_81">
    <path d="M 54.545455 184.608 
L 59.477273 184.608 
L 59.477273 184.450388 
L 54.545455 184.450388 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_82">
    <path d="M 59.477273 184.608 
L 64.409091 184.608 
L 64.409091 184.608 
L 59.477273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_83">
    <path d="M 64.409091 184.608 
L 69.340909 184.608 
L 69.340909 184.135164 
L 64.409091 184.135164 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_84">
    <path d="M 69.340909 184.608 
L 74.272727 184.608 
L 74.272727 184.608 
L 69.340909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_85">
    <path d="M 74.272727 184.608 
L 79.204545 184.608 
L 79.204545 183.347104 
L 74.272727 183.347104 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_86">
    <path d="M 79.204545 184.608 
L 84.136364 184.608 
L 84.136364 183.347104 
L 79.204545 183.347104 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_87">
    <path d="M 84.136364 184.608 
L 89.068182 184.608 
L 89.068182 183.189493 
L 84.136364 183.189493 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_88">
    <path d="M 89.068182 184.608 
L 94 184.608 
L 94 181.928597 
L 89.068182 181.928597 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_89">
    <path d="M 94 184.608 
L 98.931818 184.608 
L 98.931818 182.559045 
L 94 182.559045 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_90">
    <path d="M 98.931818 184.608 
L 103.863636 184.608 
L 103.863636 180.982925 
L 98.931818 180.982925 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_91">
    <path d="M 103.863636 184.608 
L 108.795455 184.608 
L 108.795455 178.303522 
L 103.863636 178.303522 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_92">
    <path d="M 108.795455 184.608 
L 113.727273 184.608 
L 113.727273 175.781731 
L 108.795455 175.781731 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_93">
    <path d="M 113.727273 184.608 
L 118.659091 184.608 
L 118.659091 173.890388 
L 113.727273 173.890388 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_94">
    <path d="M 118.659091 184.608 
L 123.590909 184.608 
L 123.590909 169.634866 
L 118.659091 169.634866 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_95">
    <path d="M 123.590909 184.608 
L 128.522727 184.608 
L 128.522727 165.221731 
L 123.590909 165.221731 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_96">
    <path d="M 128.522727 184.608 
L 133.454545 184.608 
L 133.454545 155.134567 
L 128.522727 155.134567 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_97">
    <path d="M 133.454545 184.608 
L 138.386364 184.608 
L 138.386364 163.172776 
L 133.454545 163.172776 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_98">
    <path d="M 138.386364 184.608 
L 143.318182 184.608 
L 143.318182 184.608 
L 138.386364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_99">
    <path d="M 143.318182 184.608 
L 148.25 184.608 
L 148.25 184.608 
L 143.318182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_100">
    <path d="M 148.25 184.608 
L 153.181818 184.608 
L 153.181818 184.608 
L 148.25 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_101">
    <path d="M 153.181818 184.608 
L 158.113636 184.608 
L 158.113636 184.608 
L 153.181818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_102">
    <path d="M 158.113636 184.608 
L 163.045455 184.608 
L 163.045455 184.608 
L 158.113636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_103">
    <path d="M 163.045455 184.608 
L 167.977273 184.608 
L 167.977273 184.608 
L 163.045455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_104">
    <path d="M 167.977273 184.608 
L 172.909091 184.608 
L 172.909091 184.608 
L 167.977273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_105">
    <path d="M 172.909091 184.608 
L 177.840909 184.608 
L 177.840909 184.608 
L 172.909091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_106">
    <path d="M 177.840909 184.608 
L 182.772727 184.608 
L 182.772727 184.608 
L 177.840909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_107">
    <path d="M 182.772727 184.608 
L 187.704545 184.608 
L 187.704545 184.608 
L 182.772727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_108">
    <path d="M 187.704545 184.608 
L 192.636364 184.608 
L 192.636364 184.608 
L 187.704545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_109">
    <path d="M 192.636364 184.608 
L 197.568182 184.608 
L 197.568182 184.608 
L 192.636364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_110">
    <path d="M 197.568182 184.608 
L 202.5 184.608 
L 202.5 184.608 
L 197.568182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_111">
    <path d="M 202.5 184.608 
L 207.431818 184.608 
L 207.431818 184.608 
L 202.5 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_112">
    <path d="M 207.431818 184.608 
L 212.363636 184.608 
L 212.363636 184.608 
L 207.431818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_113">
    <path d="M 212.363636 184.608 
L 217.295455 184.608 
L 217.295455 184.608 
L 212.363636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_114">
    <path d="M 217.295455 184.608 
L 222.227273 184.608 
L 222.227273 184.608 
L 217.295455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_115">
    <path d="M 222.227273 184.608 
L 227.159091 184.608 
L 227.159091 184.608 
L 222.227273 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_116">
    <path d="M 227.159091 184.608 
L 232.090909 184.608 
L 232.090909 184.608 
L 227.159091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_117">
    <path d="M 232.090909 184.608 
L 237.022727 184.608 
L 237.022727 184.608 
L 232.090909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_118">
    <path d="M 237.022727 184.608 
L 241.954545 184.608 
L 241.954545 184.608 
L 237.022727 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_119">
    <path d="M 241.954545 184.608 
L 246.886364 184.608 
L 246.886364 184.608 
L 241.954545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_120">
    <path d="M 246.886364 184.608 
L 251.818182 184.608 
L 251.818182 184.608 
L 246.886364 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_121">
    <path d="M 251.818182 184.608 
L 256.75 184.608 
L 256.75 184.608 
L 251.818182 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_122">
    <path d="M 256.75 184.608 
L 261.681818 184.608 
L 261.681818 184.608 
L 256.75 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_123">
    <path d="M 261.681818 184.608 
L 266.613636 184.608 
L 266.613636 184.608 
L 261.681818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_124">
    <path d="M 266.613636 184.608 
L 271.545455 184.608 
L 271.545455 160.178149 
L 266.613636 160.178149 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_125">
    <path d="M 271.545455 184.608 
L 276.477273 184.608 
L 276.477273 157.81397 
L 271.545455 157.81397 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_126">
    <path d="M 276.477273 184.608 
L 281.409091 184.608 
L 281.409091 161.911881 
L 276.477273 161.911881 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_127">
    <path d="M 281.409091 184.608 
L 286.340909 184.608 
L 286.340909 169.004418 
L 281.409091 169.004418 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_128">
    <path d="M 286.340909 184.608 
L 291.272727 184.608 
L 291.272727 172.471881 
L 286.340909 172.471881 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_129">
    <path d="M 291.272727 184.608 
L 296.204545 184.608 
L 296.204545 176.885015 
L 291.272727 176.885015 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_130">
    <path d="M 296.204545 184.608 
L 301.136364 184.608 
L 301.136364 178.303522 
L 296.204545 178.303522 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_131">
    <path d="M 301.136364 184.608 
L 306.068182 184.608 
L 306.068182 181.928597 
L 301.136364 181.928597 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_132">
    <path d="M 306.068182 184.608 
L 311 184.608 
L 311 181.770985 
L 306.068182 181.770985 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_133">
    <path d="M 311 184.608 
L 315.931818 184.608 
L 315.931818 182.086209 
L 311 182.086209 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_134">
    <path d="M 315.931818 184.608 
L 320.863636 184.608 
L 320.863636 183.504716 
L 315.931818 183.504716 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_135">
    <path d="M 320.863636 184.608 
L 325.795455 184.608 
L 325.795455 183.81994 
L 320.863636 183.81994 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_136">
    <path d="M 325.795455 184.608 
L 330.727273 184.608 
L 330.727273 184.608 
L 325.795455 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_137">
    <path d="M 330.727273 184.608 
L 335.659091 184.608 
L 335.659091 183.662328 
L 330.727273 183.662328 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_138">
    <path d="M 335.659091 184.608 
L 340.590909 184.608 
L 340.590909 184.608 
L 335.659091 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_139">
    <path d="M 340.590909 184.608 
L 345.522727 184.608 
L 345.522727 184.608 
L 340.590909 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_140">
    <path d="M 345.522727 184.608 
L 350.454545 184.608 
L 350.454545 184.292776 
L 345.522727 184.292776 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_141">
    <path d="M 350.454545 184.608 
L 355.386364 184.608 
L 355.386364 184.608 
L 350.454545 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_142">
    <path d="M 355.386364 184.608 
L 360.318182 184.608 
L 360.318182 184.450388 
L 355.386364 184.450388 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_143">
    <path d="M 360.318182 184.608 
L 365.25 184.608 
L 365.25 184.450388 
L 360.318182 184.450388 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_144">
    <path d="M 365.25 184.608 
L 370.181818 184.608 
L 370.181818 184.608 
L 365.25 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_145">
    <path d="M 370.181818 184.608 
L 375.113636 184.608 
L 375.113636 184.608 
L 370.181818 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_146">
    <path d="M 375.113636 184.608 
L 380.045455 184.608 
L 380.045455 184.608 
L 375.113636 184.608 
z
" clip-path="url(#p25c80dc223)" style="fill: #f97316; opacity: 0.9"/>
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
       <use xlink:href="#m15aed4d867" x="54.545455" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="54.545455" y="199.205656" transform="rotate(-0 54.545455 199.205656)">775</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="103.863636" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="103.863636" y="199.205656" transform="rotate(-0 103.863636 199.205656)">800</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="153.181818" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="153.181818" y="199.205656" transform="rotate(-0 153.181818 199.205656)">825</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="202.5" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="199.205656" transform="rotate(-0 202.5 199.205656)">850</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="251.818182" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="251.818182" y="199.205656" transform="rotate(-0 251.818182 199.205656)">875</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="301.136364" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="301.136364" y="199.205656" transform="rotate(-0 301.136364 199.205656)">900</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="350.454545" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.454545" y="199.205656" transform="rotate(-0 350.454545 199.205656)">925</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="213.459563" transform="rotate(-0 202.5 213.459563)">40 ölçümün ortalaması (ms), hiçbir şey değişmeseydi</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_8">
    <path d="M 268.043864 184.608 
L 268.043864 7.2 
" clip-path="url(#p25c80dc223)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_147">
    <path d="M 7.2 184.608 
L 7.2 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_148">
    <path d="M 397.8 184.608 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_149">
    <path d="M 7.2 184.608 
L 397.8 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_150">
    <path d="M 7.2 7.2 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_151">
     <path d="M 15.3 22.138594 
L 33.3 22.138594 
L 33.3 15.838594 
L 15.3 15.838594 
z
" style="fill: #8b5cf6; opacity: 0.75"/>
    </g>
    <g id="text_9">
     <text style="font-size: 9px; font-family:inherit; text-anchor: start; fill: currentColor" x="40.5" y="22.138594" transform="rotate(-0 40.5 22.138594)">daha yakın</text>
    </g>
    <g id="patch_152">
     <path d="M 15.3 35.639297 
L 33.3 35.639297 
L 33.3 29.339297 
L 15.3 29.339297 
z
" style="fill: #f97316; opacity: 0.9"/>
    </g>
    <g id="text_10">
     <text style="font-size: 9px; font-family:inherit; text-anchor: start; fill: currentColor" x="40.5" y="35.639297" transform="rotate(-0 40.5 35.639297)">en az bizimki kadar uzak</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p25c80dc223">
   <rect x="7.2" y="7.2" width="390.6" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>H₀ dünyasında 20 000 örneklem ortalaması. Kesik çizgi bizim ortalamamız. Turuncu kuyrukların payı p değeri.</figcaption>
</figure>

## Aynı şey formülle: t-testi

Evren çoğu zaman elimizde olmaz. O zaman H₀ dünyasını merkezi limit
teoreminden kurarız: örneklem ortalaması, $H_0$ doğruysa $\mu_0 = 850$
merkezli ve $s/\sqrt{n}$ genişlikli bir dağılımdan gelir. Farkı standart
hata cinsinden ölçen sayıya **test istatistiği** (test statistic) denir:

$$t = \dfrac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

```python
from scipy import stats
from ab_data import make_speed_test

loads = make_speed_test()
result = stats.ttest_1samp(loads, 850)
print(round(result.statistic, 3), round(result.pvalue, 4))
```

```text
1.702 0.0968
```

- $t$ = 1,702: ortalama, 850'den yaklaşık 1,7 standart hata uzakta.
- p = 0,0968. Benzetimdekine (0,080) yakın ama aynı değil:
  benzetim evrenin gerçek sapmasını biliyordu, t-testi ise sapmayı
  örneklemden tahmin ediyor ve t dağılımının kalın kuyruklarıyla bunun
  bedelini ödüyor.

## Karar: α eşiği

Ne kadar küçük p "yeterince küçük"? Bunu veriye bakmadan **önce** seçeriz.
Bu eşiğe **anlamlılık düzeyi** (significance level, $\alpha$) denir; en
yaygını 0,05.

- $p < \alpha$ ise "$H_0$'ı reddediyoruz": fark **istatistiksel olarak
  anlamlı** (statistically significant).
- $p \ge \alpha$ ise "$H_0$'ı reddedemiyoruz".

Burada p = 0,0968 > 0,05: $H_0$ reddedilemedi. Dikkat: bu "hiçbir şey
değişmedi" demek **değil**. Veriyi biz ürettik ve gerçeği biliyoruz: yeni
sunucunun gerçek ortalaması 890 ms, yani 40 ms yavaşlama **var**. 40 ölçüm
onu göstermeye yetmedi.

## İki tür hata

| | $H_0$ gerçekten doğru | $H_0$ gerçekten yanlış |
|---|---|---|
| $H_0$ reddedildi | **I. tür hata** (yanlış alarm) | doğru karar |
| $H_0$ reddedilmedi | doğru karar | **II. tür hata** (kaçırma) |

- **I. tür hata** (type I error): fark yokken "var" demek. Olasılığı tam
  $\alpha$'dır; eşiği biz seçtiğimiz için bu hatayı biz kontrol ederiz.
- **II. tür hata** (type II error): fark varken onu kaçırmak. Bizim sunucu
  örneğimizde olan bu.
- **Güç** (power): fark varken onu yakalama olasılığı, yani 1 − II. tür hata
  olasılığı.

İkisini de benzetimle ölçelim. Önce hiçbir şeyin değişmediği dünyada,
sonra açılışların gerçekten 40 ms yavaşladığı dünyada:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

old = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(72)
same = rng.choice(old, size=(5000, 40))
p = stats.ttest_1samp(same, 850, axis=1).pvalue
print("H0", round((p < 0.05).mean(), 3))
for n in [40, 160]:
    slower = rng.choice(old, size=(5000, n)) + 40
    p = stats.ttest_1samp(slower, 850, axis=1).pvalue
    print(n, round((p < 0.05).mean(), 3))
```

```text
H0 0.052
40 0.525
160 0.984
```

- Hiçbir şey değişmeyen dünyada testlerin %5,2 kadarı yanlış alarm
  verdi: $\alpha = 0{,}05$ sözünü tuttu.
- Gerçek bir 40 ms yavaşlamada 40 ölçümle testlerin yalnızca %52,5
  kadarı onu yakaladı. Bizim testimizin kaçırması şanssızlık değil, sık
  olan bir şey: bu tasarımın gücü yazı tura kadar.
- 160 ölçümle güç %98,4. Fark aynı, veri dört kat: kaçırma
  neredeyse hiç kalmıyor. Kaç ölçüm gerektiğini önceden hesaplamaya **güç
  analizi** denir; ileride ayrı bir bölüm.

## Tek yönlü mü, iki yönlü mü?

Yukarıdaki test **iki yönlüydü** (two-sided): "850'den farklı mı?" Bazen soru
tek yönlüdür: "yavaşladı mı?" O zaman yalnızca bir kuyruğa bakılır:

```python
from scipy import stats
from ab_data import make_speed_test

loads = make_speed_test()
print(round(stats.ttest_1samp(loads, 850, alternative="greater").pvalue, 4))
```

```text
0.0484
```

Tek yönlü p = 0,0484: iki yönlünün yarısı ve 0,05'in altında. Burada
bir tuzak var. Yön, veriye bakmadan **önce** ve konunun gereği seçilir.
Sonucu görüp "o zaman tek yönlü yapayım" demek, aynı veriyi iki kez sınayıp
işine geleni seçmektir ve yanlış alarm oranını gizlice ikiye katlar. Bir
sonraki bölümde bu tür kandırmacaları ayrıntılı göreceğiz.

## Özet

- Hipotez testi "$H_0$ doğru olsaydı bu kadar uç sonuç ne kadar olası?" diye
  sorar; cevap p değeridir.
- H₀ dünyası benzetimle (evren elindeyse) ya da formülle (t-testi) kurulur.
- $\alpha$ veriye bakmadan seçilir; $p < \alpha$ ise $H_0$ reddedilir.
- "Reddedilemedi" ≠ "fark yok". I. tür hata yanlış alarm, II. tür hata
  kaçırma; güç kaçırmama olasılığı ve örneklemle artar.
- Tek yönlü test yalnızca önceden ve gerekçeyle seçilir.
