# Bileşenler ve Ayrıştırma

Bölüm 00'da bir zaman serisinin içinde üç şeyin üst üste bindiğini söylemiştik:
trend, mevsimsellik ve gürültü. O günden beri onları hep **göz kararı** ayırdın:
hareketli ortalamayla trendi gördün, `groupby(index.dayofweek)` ile haftalık
deseni, mevsim grafiğiyle yıllık olanı.

Bu bölüm aynı işi **sayıyla** yapıyor: seriyi üç ayrı seriye bölüyorsun ve
üçünü topladığında elindeki veri, eksiksiz, geri geliyor. Buna **ayrıştırma**
(decomposition) deniyor.

Bu bölümle birlikte yeni bir kütüphane giriyor: **statsmodels**. Zaman serisi
modellerinin Python'daki standart adresi; patikanın kalanında hep yanında
olacak.

## 1. Üç bileşen

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Trend</span><span>Serinin yavaş değişen düzeyi. Haftalar, aylar içinde nereye gidiyor?</span></div>
<div class="anat-row"><span>Mevsim</span><span>Sabit uzunlukta tekrar eden desen: haftanın günü, yılın ayı, günün saati.</span></div>
<div class="anat-row"><span>Kalıntı</span><span>İlk ikisi çıkarılınca geriye kalan. Gürültü, olaylar ve modelin kaçırdığı her şey.</span></div>
</div>
<figcaption>Ayrıştırmanın üç çıktısı. Üçü de seriyle <b>aynı uzunlukta</b> birer seri.</figcaption>
</figure>

En basit hâliyle:

$$\text{gözlem} = \text{trend} + \text{mevsim} + \text{kalıntı}$$

Bu **toplamsal** modeldir. Günlük mağaza satışında 12 Mart 2024 Salı günü için
sayılar şöyle çıkacak:

```text
256  =  287.9  +  (-39.6)  +  7.8
```

Okunuşu: o günlerde mağazanın düzeyi 288 civarında; salı günleri ortalamanın
40 altında geçiyor; o salı beklenenden 8 fazla satılmış.

## 2. Elle ayrıştırma: üç adım

Kütüphaneyi çağırmadan önce işi bir kez elle yap; içinde bilmediğin hiçbir şey
yok.

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
```

**Adım 1 — Trend.** Mevsimin boyu kadar (7 gün) **ortalanmış** hareketli
ortalama. Pencere tam bir haftayı kapladığı için her günden bir tane içeriyor
ve haftalık desen kendini götürüyor (Bölüm 07):

```python
trend = s.rolling(7, center=True).mean()
```

Ortalanmış olması önemli: geriye dönük ortalama trendi 3 gün geç gösterirdi.
Bedeli: ilk 3 ve son 3 günün trendi yok (`NaN`).

**Adım 2 — Mevsim.** Trendi çıkar, sonra kalanın haftanın gününe göre
ortalamasını al:

```python
detrended = s - trend
pattern = detrended.groupby(detrended.index.dayofweek).mean()
pattern = pattern - pattern.mean()      # toplami sifir olsun
print(pattern.round(1).tolist())
# [-42.6, -39.6, -31.1, -18.7, 19.0, 76.2, 36.7]
```

Yedi sayı: pazartesi trendin 42.6 altında, cumartesi 76.2 üstünde. Toplamları
sıfır; böylece mevsim bileşeni düzeyi değiştirmiyor, yalnızca hafta içinde
dağıtıyor.

Bu yedi sayıyı bütün tarihlere yay:

```python
seasonal = pd.Series(pattern.loc[s.index.dayofweek].values, index=s.index)
```

**Adım 3 — Kalıntı.** Geriye kalan:

```python
resid = s - trend - seasonal
print(round(resid.std(), 2), round(s.std(), 2))     # 12.32 58.94
```

Serinin standart sapması 58.9 idi; trend ve haftalık desen çıkarılınca 12.3
kaldı. Oynaklığın büyük kısmı **açıklanabilir** yapıdan geliyormuş.

## 3. `seasonal_decompose`

statsmodels aynı üç adımı tek çağrıda yapıyor:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(s, model="additive", period=7)

result.trend        # Adim 1
result.seasonal     # Adim 2
result.resid        # Adim 3
result.observed     # serinin kendisi
```

Sonuçlar elle bulduklarınla **birebir aynı** (ölçüldü). `period` mevsimin kaç
gözlem sürdüğü: günlük veride haftalık desen için 7, aylık veride yıllık desen
için 12, saatlik veride günlük desen için 24.

<figure class="fig">
  <svg viewBox="0 0 680 464" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="44" y1="98.8" x2="666" y2="98.8"/><text class="dim" x="38" y="102.3" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="75.5" x2="666" y2="75.5"/><text class="dim" x="38" y="79.0" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="52.3" x2="666" y2="52.3"/><text class="dim" x="38" y="55.8" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="29.0" x2="666" y2="29.0"/><text class="dim" x="38" y="32.5" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="104" x2="666" y2="104"/><polyline class="curve3" style="stroke-width:1.3" points="44.0,83.7 45.7,86.9 47.4,86.5 49.1,82.5 50.8,67.8 52.5,53.2 54.2,65.7 55.9,90.2 57.6,87.2 59.3,83.7 61.0,79.0 62.7,72.0 64.4,51.6 66.2,66.2 67.9,84.1 69.6,89.7 71.3,82.3 73.0,81.6 74.7,76.4 76.4,53.4 78.1,67.4 79.8,84.8 81.5,89.2 83.2,84.4 84.9,79.9 86.6,75.7 88.3,56.4 90.0,64.8 91.7,89.9 93.4,88.3 95.1,82.3 96.8,74.1 98.5,73.7 100.2,54.8 101.9,68.3 103.6,84.1 105.3,88.3 107.1,84.4 108.8,78.5 110.5,75.1 112.2,55.0 113.9,67.8 115.6,93.0 117.3,88.8 119.0,85.3 120.7,83.4 122.4,70.6 124.1,58.1 125.8,67.4 127.5,87.6 129.2,82.3 130.9,84.1 132.6,84.6 134.3,69.5 136.0,57.6 137.7,67.8 139.4,92.5 141.1,89.0 142.8,85.8 144.5,87.2 146.2,75.1 148.0,58.8 149.7,71.1 151.4,86.2 153.1,84.4 154.8,90.4 156.5,88.8 158.2,78.3 159.9,56.0 161.6,73.0 163.3,91.1 165.0,85.8 166.7,85.5 168.4,81.8 170.1,75.3 171.8,54.6 173.5,71.8 175.2,94.1 176.9,89.5 178.6,80.6 180.3,80.9 182.0,76.9 183.7,65.3 185.4,71.1 187.1,90.2 188.8,88.8 190.6,88.8 192.3,88.1 194.0,78.3 195.7,60.9 197.4,68.5 199.1,89.2 200.8,91.3 202.5,89.5 204.2,83.0 205.9,74.6 207.6,61.6 209.3,78.5 211.0,96.0 212.7,89.5 214.4,86.7 216.1,85.3 217.8,77.8 219.5,63.7 221.2,72.5 222.9,96.7 224.6,93.7 226.3,88.5 228.0,87.8 229.7,79.0 231.5,64.3 233.2,73.2 234.9,94.8 236.6,95.1 238.3,89.7 240.0,92.0 241.7,79.7 243.4,68.5 245.1,71.8 246.8,87.6 248.5,95.8 250.2,88.5 251.9,89.2 253.6,81.3 255.3,66.7 257.0,74.1 258.7,92.5 260.4,94.8 262.1,93.0 263.8,85.5 265.5,76.4 267.2,68.5 268.9,76.2 270.6,91.8 272.4,87.8 274.1,90.9 275.8,87.4 277.5,82.7 279.2,63.7 280.9,74.4 282.6,95.5 284.3,93.4 286.0,86.0 287.7,84.8 289.4,76.7 291.1,68.8 292.8,79.0 294.5,98.8 296.2,92.0 297.9,94.8 299.6,91.6 301.3,77.6 303.0,71.3 304.7,74.6 306.4,97.9 308.1,93.4 309.8,85.8 311.5,88.1 313.2,81.3 315.0,67.1 316.7,76.7 318.4,96.2 320.1,97.9 321.8,94.1 323.5,85.3 325.2,77.4 326.9,64.8 328.6,76.0 330.3,93.0 332.0,92.7 333.7,90.2 335.4,84.8 337.1,77.1 338.8,67.1 340.5,77.8 342.2,99.7 343.9,95.1 345.6,91.8 347.3,88.8 349.0,80.2 350.7,64.8 352.4,72.7 354.1,98.1 355.9,95.5 357.6,93.7 359.3,86.5 361.0,75.1 362.7,64.8 364.4,73.7 366.1,95.3 367.8,95.1 369.5,92.5 371.2,83.7 372.9,79.5 374.6,65.3 376.3,72.7 378.0,93.2 379.7,89.5 381.4,90.4 383.1,86.5 384.8,77.4 386.5,65.5 388.2,74.6 389.9,91.3 391.6,91.3 393.3,91.3 395.0,86.7 396.8,71.6 398.5,63.7 400.2,74.8 401.9,91.3 403.6,86.9 405.3,89.7 407.0,86.7 408.7,78.3 410.4,65.7 412.1,72.3 413.8,89.0 415.5,89.5 417.2,88.3 418.9,89.7 420.6,77.4 422.3,64.1 424.0,78.1 425.7,92.7 427.4,88.3 429.1,90.4 430.8,86.7 432.5,71.1 434.2,58.5 435.9,66.9 437.6,87.2 439.4,87.4 441.1,87.2 442.8,82.5 444.5,70.9 446.2,58.3 447.9,68.8 449.6,89.2 451.3,86.0 453.0,87.6 454.7,78.5 456.4,71.1 458.1,59.5 459.8,63.7 461.5,93.4 463.2,93.4 464.9,83.9 466.6,83.9 468.3,74.4 470.0,55.3 471.7,64.3 473.4,82.5 475.1,85.5 476.8,86.5 478.5,79.7 480.3,72.5 482.0,56.7 483.7,63.2 485.4,84.1 487.1,90.6 488.8,81.1 490.5,79.9 492.2,69.2 493.9,56.7 495.6,67.6 497.3,87.8 499.0,83.7 500.7,83.4 502.4,80.4 504.1,67.4 505.8,55.0 507.5,68.8 509.2,84.6 510.9,87.4 512.6,81.8 514.3,75.7 516.0,70.9 517.7,53.2 519.4,66.2 521.2,85.3 522.9,85.5 524.6,86.0 526.3,78.3 528.0,65.3 529.7,53.9 531.4,61.3 533.1,86.2 534.8,87.6 536.5,77.1 538.2,75.7 539.9,66.4 541.6,51.3 543.3,65.5 545.0,81.3 546.7,83.9 548.4,75.3 550.1,78.1 551.8,66.9 553.5,48.8 555.2,60.6 556.9,82.0 558.6,81.6 560.3,78.8 562.0,76.9 563.8,61.3 565.5,47.1 567.2,59.7 568.9,82.0 570.6,83.2 572.3,79.5 574.0,74.1 575.7,63.7 577.4,42.0 579.1,58.3 580.8,80.9 582.5,82.7 584.2,74.8 585.9,74.8 587.6,58.5 589.3,50.2 591.0,53.9 592.7,81.8 594.4,80.2 596.1,80.2 597.8,72.0 599.5,59.9 601.2,48.3 602.9,56.2 604.7,82.7 606.4,78.5 608.1,76.2 609.8,76.2 611.5,67.1 613.2,44.8 614.9,53.9 616.6,82.7 618.3,77.8 620.0,73.4 621.7,72.3 623.4,62.3 625.1,40.8 626.8,49.9 628.5,76.9 630.2,71.6 631.9,75.3 633.6,61.3 635.3,54.8 637.0,37.1 638.7,44.3 640.4,75.3 642.1,73.7 643.8,70.2 645.6,70.9 647.3,50.2 649.0,31.5 650.7,45.3 652.4,74.1 654.1,65.3 655.8,66.2 657.5,62.5 659.2,46.7 660.9,28.3 662.6,42.0 664.3,66.4 666.0,64.6"/><text class="ink" x="44" y="14" font-size="12" text-anchor="start" font-weight="600">Gözlem</text></g><g transform="translate(0,112)"><line class="grid" x1="44" y1="101.2" x2="666" y2="101.2"/><text class="dim" x="38" y="104.7" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="75.8" x2="666" y2="75.8"/><text class="dim" x="38" y="79.3" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="50.3" x2="666" y2="50.3"/><text class="dim" x="38" y="53.8" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="24.9" x2="666" y2="24.9"/><text class="dim" x="38" y="28.4" font-size="10.5" text-anchor="end">400</text><line class="line" x1="44" y1="104" x2="666" y2="104"/><polyline class="curve" style="stroke-width:1.3" points="44.0,64.1 45.7,65.7 47.4,70.5 49.1,75.1 50.8,77.1 52.5,77.2 54.2,76.3 55.9,75.2 57.6,76.5 59.3,76.0 61.0,76.1 62.7,74.3 64.4,75.1 66.2,74.6 67.9,75.4 69.6,76.8 71.3,77.4 73.0,77.7 74.7,78.0 76.4,77.8 78.1,78.5 79.8,78.0 81.5,77.7 83.2,78.7 84.9,77.9 86.6,79.5 88.3,79.2 90.0,78.5 91.7,76.7 93.4,76.1 95.1,75.6 96.8,76.7 98.5,74.8 100.2,74.8 101.9,75.5 103.6,76.9 105.3,77.3 107.1,77.4 108.8,77.2 110.5,80.0 112.2,80.1 113.9,80.4 115.6,82.0 117.3,80.6 119.0,81.5 120.7,81.4 122.4,79.7 124.1,77.7 125.8,77.3 127.5,77.7 129.2,77.3 130.9,77.2 132.6,77.3 134.3,78.8 136.0,80.9 137.7,81.5 139.4,82.3 141.1,84.0 142.8,84.4 144.5,85.4 146.2,83.4 148.0,82.0 149.7,83.4 151.4,83.9 153.1,84.9 154.8,84.1 156.5,84.7 158.2,86.2 159.9,86.6 161.6,85.1 163.3,82.9 165.0,82.0 166.7,81.5 168.4,81.2 170.1,82.1 171.8,83.3 173.5,81.7 175.2,81.5 176.9,82.0 178.6,85.3 180.3,85.1 182.0,83.9 183.7,83.6 185.4,86.2 187.1,88.4 188.8,88.9 190.6,87.5 192.3,86.7 194.0,86.4 195.7,87.2 197.4,87.4 199.1,85.8 200.8,84.7 202.5,84.9 204.2,88.0 205.9,90.1 207.6,89.5 209.3,88.7 211.0,89.4 212.7,90.4 214.4,91.1 216.1,89.2 217.8,89.4 219.5,90.7 221.2,91.3 222.9,92.1 224.6,92.4 226.3,92.7 228.0,92.9 229.7,92.3 231.5,92.7 233.2,93.1 234.9,94.4 236.6,94.6 238.3,95.9 240.0,95.5 241.7,93.2 243.4,93.5 245.1,93.1 246.8,92.2 248.5,92.7 250.2,92.1 251.9,92.9 253.6,94.4 255.3,94.1 257.0,95.5 258.7,94.3 260.4,92.8 262.1,93.4 263.8,94.0 265.5,93.8 267.2,91.6 268.9,91.0 270.6,91.6 272.4,93.5 274.1,92.0 275.8,91.4 277.5,92.6 279.2,94.3 280.9,92.8 282.6,92.0 284.3,90.1 286.0,91.7 287.7,93.2 289.4,94.2 291.1,93.7 292.8,96.5 294.5,98.6 296.2,98.9 297.9,99.7 299.6,98.3 301.3,98.0 303.0,98.5 304.7,95.6 306.4,94.5 308.1,95.7 309.8,94.4 311.5,95.1 313.2,94.5 315.0,95.9 316.7,98.6 318.4,97.7 320.1,96.4 321.8,95.7 323.5,95.5 325.2,94.5 326.9,92.9 328.6,91.6 330.3,91.5 332.0,91.4 333.7,92.1 335.4,92.7 337.1,94.8 338.8,95.6 340.5,96.1 342.2,97.3 343.9,98.3 345.6,97.5 347.3,95.9 349.0,95.4 350.7,95.6 352.4,96.2 354.1,95.4 355.9,93.8 357.6,93.8 359.3,94.1 361.0,93.2 362.7,93.1 364.4,92.7 366.1,91.9 367.8,93.2 369.5,93.4 371.2,93.1 372.9,92.4 374.6,90.7 376.3,90.0 378.0,90.9 379.7,90.3 381.4,90.3 383.1,90.9 384.8,90.3 386.5,90.9 388.2,91.2 389.9,91.3 391.6,89.5 393.3,88.9 395.0,88.9 396.8,88.9 398.5,87.6 400.2,87.1 401.9,87.1 403.6,89.2 405.3,89.8 407.0,89.0 408.7,88.3 410.4,89.1 412.1,88.7 413.8,89.6 415.5,89.3 417.2,88.8 418.9,90.6 420.6,91.8 422.3,91.4 424.0,92.1 425.7,91.1 427.4,89.2 429.1,87.4 430.8,83.9 432.5,82.2 434.2,81.9 435.9,80.9 437.6,79.6 439.4,79.5 441.1,79.4 442.8,80.0 444.5,80.7 446.2,80.2 447.9,80.4 449.6,79.1 451.3,79.2 453.0,79.6 454.7,78.0 456.4,79.3 458.1,81.6 459.8,80.4 461.5,82.1 463.2,83.1 464.9,81.8 466.6,82.0 468.3,78.6 470.0,76.1 471.7,76.9 473.4,75.6 475.1,75.1 476.8,75.5 478.5,75.1 480.3,75.6 482.0,77.2 483.7,75.6 485.4,75.6 487.1,74.6 488.8,74.6 490.5,76.0 492.2,77.2 493.9,75.0 495.6,75.7 497.3,75.9 499.0,75.3 500.7,74.8 502.4,75.1 504.1,74.1 505.8,75.3 507.5,74.8 509.2,73.3 510.9,74.4 512.6,73.8 514.3,73.0 516.0,73.2 517.7,72.7 519.4,74.0 521.2,74.8 522.9,73.0 524.6,73.2 526.3,71.7 528.0,72.0 529.7,72.7 531.4,69.9 533.1,69.1 534.8,69.5 536.5,68.7 538.2,70.0 539.9,68.4 541.6,67.3 543.3,66.7 545.0,67.4 546.7,67.6 548.4,66.8 550.1,65.2 551.8,65.5 553.5,64.7 555.2,65.8 556.9,65.5 558.6,63.7 560.3,63.2 562.0,62.9 563.8,62.9 565.5,63.4 567.2,63.6 568.9,62.8 570.6,63.5 572.3,61.9 574.0,61.5 575.7,61.1 577.4,60.9 579.1,59.5 580.8,59.7 582.5,58.1 584.2,60.7 585.9,59.3 587.6,59.6 589.3,58.8 591.0,60.4 592.7,59.6 594.4,60.0 596.1,59.4 597.8,60.1 599.5,60.4 601.2,59.9 602.9,58.7 604.7,60.0 606.4,62.3 608.1,61.2 609.8,60.4 611.5,60.4 613.2,60.2 614.9,59.3 616.6,58.1 618.3,56.6 620.0,55.3 621.7,54.1 623.4,52.3 625.1,50.3 626.8,50.9 628.5,47.5 630.2,45.2 631.9,44.0 633.6,42.3 635.3,41.7 637.0,42.4 638.7,40.8 640.4,43.8 642.1,42.3 643.8,40.6 645.6,40.9 647.3,40.5 649.0,37.9 650.7,36.7 652.4,34.0 654.1,32.9 655.8,31.9 657.5,30.9 659.2,28.5 660.9,28.3"/><text class="ink" x="44" y="14" font-size="12" text-anchor="start" font-weight="600">Trend</text></g><g transform="translate(0,224)"><line class="line" x1="44" y1="74.1" x2="666" y2="74.1"/><text class="dim" x="38" y="77.6" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="44.1" x2="666" y2="44.1"/><text class="dim" x="38" y="47.6" font-size="10.5" text-anchor="end">50</text><line class="line" x1="44" y1="104" x2="666" y2="104"/><polyline class="curve2" style="stroke-width:1.3" points="44.0,99.7 45.7,97.9 47.4,92.8 49.1,85.4 50.8,62.7 52.5,28.3 54.2,52.0 55.9,99.7 57.6,97.9 59.3,92.8 61.0,85.4 62.7,62.7 64.4,28.3 66.2,52.0 67.9,99.7 69.6,97.9 71.3,92.8 73.0,85.4 74.7,62.7 76.4,28.3 78.1,52.0 79.8,99.7 81.5,97.9 83.2,92.8 84.9,85.4 86.6,62.7 88.3,28.3 90.0,52.0 91.7,99.7 93.4,97.9 95.1,92.8 96.8,85.4 98.5,62.7 100.2,28.3 101.9,52.0 103.6,99.7 105.3,97.9 107.1,92.8 108.8,85.4 110.5,62.7 112.2,28.3 113.9,52.0 115.6,99.7 117.3,97.9 119.0,92.8 120.7,85.4 122.4,62.7 124.1,28.3 125.8,52.0 127.5,99.7 129.2,97.9 130.9,92.8 132.6,85.4 134.3,62.7 136.0,28.3 137.7,52.0 139.4,99.7 141.1,97.9 142.8,92.8 144.5,85.4 146.2,62.7 148.0,28.3 149.7,52.0 151.4,99.7 153.1,97.9 154.8,92.8 156.5,85.4 158.2,62.7 159.9,28.3 161.6,52.0 163.3,99.7 165.0,97.9 166.7,92.8 168.4,85.4 170.1,62.7 171.8,28.3 173.5,52.0 175.2,99.7 176.9,97.9 178.6,92.8 180.3,85.4 182.0,62.7 183.7,28.3 185.4,52.0 187.1,99.7 188.8,97.9 190.6,92.8 192.3,85.4 194.0,62.7 195.7,28.3 197.4,52.0 199.1,99.7 200.8,97.9 202.5,92.8 204.2,85.4 205.9,62.7 207.6,28.3 209.3,52.0 211.0,99.7 212.7,97.9 214.4,92.8 216.1,85.4 217.8,62.7 219.5,28.3 221.2,52.0 222.9,99.7 224.6,97.9 226.3,92.8 228.0,85.4 229.7,62.7 231.5,28.3 233.2,52.0 234.9,99.7 236.6,97.9 238.3,92.8 240.0,85.4 241.7,62.7 243.4,28.3 245.1,52.0 246.8,99.7 248.5,97.9 250.2,92.8 251.9,85.4 253.6,62.7 255.3,28.3 257.0,52.0 258.7,99.7 260.4,97.9 262.1,92.8 263.8,85.4 265.5,62.7 267.2,28.3 268.9,52.0 270.6,99.7 272.4,97.9 274.1,92.8 275.8,85.4 277.5,62.7 279.2,28.3 280.9,52.0 282.6,99.7 284.3,97.9 286.0,92.8 287.7,85.4 289.4,62.7 291.1,28.3 292.8,52.0 294.5,99.7 296.2,97.9 297.9,92.8 299.6,85.4 301.3,62.7 303.0,28.3 304.7,52.0 306.4,99.7 308.1,97.9 309.8,92.8 311.5,85.4 313.2,62.7 315.0,28.3 316.7,52.0 318.4,99.7 320.1,97.9 321.8,92.8 323.5,85.4 325.2,62.7 326.9,28.3 328.6,52.0 330.3,99.7 332.0,97.9 333.7,92.8 335.4,85.4 337.1,62.7 338.8,28.3 340.5,52.0 342.2,99.7 343.9,97.9 345.6,92.8 347.3,85.4 349.0,62.7 350.7,28.3 352.4,52.0 354.1,99.7 355.9,97.9 357.6,92.8 359.3,85.4 361.0,62.7 362.7,28.3 364.4,52.0 366.1,99.7 367.8,97.9 369.5,92.8 371.2,85.4 372.9,62.7 374.6,28.3 376.3,52.0 378.0,99.7 379.7,97.9 381.4,92.8 383.1,85.4 384.8,62.7 386.5,28.3 388.2,52.0 389.9,99.7 391.6,97.9 393.3,92.8 395.0,85.4 396.8,62.7 398.5,28.3 400.2,52.0 401.9,99.7 403.6,97.9 405.3,92.8 407.0,85.4 408.7,62.7 410.4,28.3 412.1,52.0 413.8,99.7 415.5,97.9 417.2,92.8 418.9,85.4 420.6,62.7 422.3,28.3 424.0,52.0 425.7,99.7 427.4,97.9 429.1,92.8 430.8,85.4 432.5,62.7 434.2,28.3 435.9,52.0 437.6,99.7 439.4,97.9 441.1,92.8 442.8,85.4 444.5,62.7 446.2,28.3 447.9,52.0 449.6,99.7 451.3,97.9 453.0,92.8 454.7,85.4 456.4,62.7 458.1,28.3 459.8,52.0 461.5,99.7 463.2,97.9 464.9,92.8 466.6,85.4 468.3,62.7 470.0,28.3 471.7,52.0 473.4,99.7 475.1,97.9 476.8,92.8 478.5,85.4 480.3,62.7 482.0,28.3 483.7,52.0 485.4,99.7 487.1,97.9 488.8,92.8 490.5,85.4 492.2,62.7 493.9,28.3 495.6,52.0 497.3,99.7 499.0,97.9 500.7,92.8 502.4,85.4 504.1,62.7 505.8,28.3 507.5,52.0 509.2,99.7 510.9,97.9 512.6,92.8 514.3,85.4 516.0,62.7 517.7,28.3 519.4,52.0 521.2,99.7 522.9,97.9 524.6,92.8 526.3,85.4 528.0,62.7 529.7,28.3 531.4,52.0 533.1,99.7 534.8,97.9 536.5,92.8 538.2,85.4 539.9,62.7 541.6,28.3 543.3,52.0 545.0,99.7 546.7,97.9 548.4,92.8 550.1,85.4 551.8,62.7 553.5,28.3 555.2,52.0 556.9,99.7 558.6,97.9 560.3,92.8 562.0,85.4 563.8,62.7 565.5,28.3 567.2,52.0 568.9,99.7 570.6,97.9 572.3,92.8 574.0,85.4 575.7,62.7 577.4,28.3 579.1,52.0 580.8,99.7 582.5,97.9 584.2,92.8 585.9,85.4 587.6,62.7 589.3,28.3 591.0,52.0 592.7,99.7 594.4,97.9 596.1,92.8 597.8,85.4 599.5,62.7 601.2,28.3 602.9,52.0 604.7,99.7 606.4,97.9 608.1,92.8 609.8,85.4 611.5,62.7 613.2,28.3 614.9,52.0 616.6,99.7 618.3,97.9 620.0,92.8 621.7,85.4 623.4,62.7 625.1,28.3 626.8,52.0 628.5,99.7 630.2,97.9 631.9,92.8 633.6,85.4 635.3,62.7 637.0,28.3 638.7,52.0 640.4,99.7 642.1,97.9 643.8,92.8 645.6,85.4 647.3,62.7 649.0,28.3 650.7,52.0 652.4,99.7 654.1,97.9 655.8,92.8 657.5,85.4 659.2,62.7 660.9,28.3 662.6,52.0 664.3,99.7 666.0,97.9"/><text class="ink" x="44" y="14" font-size="12" text-anchor="start" font-weight="600">Mevsim</text></g><g transform="translate(0,336)"><line class="grid" x1="44" y1="91.4" x2="666" y2="91.4"/><text class="dim" x="38" y="94.9" font-size="10.5" text-anchor="end">−25</text><line class="line" x1="44" y1="66.6" x2="666" y2="66.6"/><text class="dim" x="38" y="70.1" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="41.8" x2="666" y2="41.8"/><text class="dim" x="38" y="45.3" font-size="10.5" text-anchor="end">25</text><line class="line" x1="44" y1="104" x2="666" y2="104"/><line class="line" x1="44.0" y1="104" x2="44.0" y2="108"/><text class="dim" x="44.0" y="120" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="146.2" y1="104" x2="146.2" y2="108"/><text class="dim" x="146.2" y="120" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="250.2" y1="104" x2="250.2" y2="108"/><text class="dim" x="250.2" y="120" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="354.1" y1="104" x2="354.1" y2="108"/><text class="dim" x="354.1" y="120" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="459.8" y1="104" x2="459.8" y2="108"/><text class="dim" x="459.8" y="120" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="563.8" y1="104" x2="563.8" y2="108"/><text class="dim" x="563.8" y="120" font-size="10.5" text-anchor="middle">Kas</text><polyline class="curve4" style="stroke-width:1.3" points="44.0,81.9 45.7,95.4 47.4,92.6 49.1,79.2 50.8,50.2 52.5,44.3 54.2,60.4 55.9,88.0 57.6,75.5 59.3,70.1 61.0,62.2 62.7,73.5 64.4,41.5 66.2,65.6 67.9,61.8 69.6,85.8 71.3,61.4 73.0,70.0 74.7,85.1 76.4,44.0 78.1,63.0 79.8,59.8 81.5,82.0 83.2,67.8 84.9,62.8 86.6,79.2 88.3,54.2 90.0,52.0 91.7,84.0 93.4,81.3 95.1,65.0 96.8,40.4 98.5,79.3 100.2,55.8 101.9,72.8 103.6,58.9 105.3,78.8 107.1,70.3 108.8,58.1 110.5,75.2 112.2,46.4 113.9,61.2 115.6,86.7 117.3,74.5 119.0,66.2 120.7,70.9 122.4,57.0 124.1,64.1 125.8,65.3 127.5,72.2 129.2,53.1 130.9,69.8 132.6,83.7 134.3,53.7 136.0,55.8 137.7,59.2 139.4,84.1 141.1,68.8 142.8,62.7 144.5,78.9 146.2,68.6 148.0,58.7 149.7,69.3 151.4,54.1 153.1,47.1 154.8,83.1 156.5,87.3 158.2,77.1 159.9,37.8 161.6,73.9 163.3,76.9 165.0,58.9 166.7,67.2 168.4,64.3 170.1,72.1 171.8,38.3 173.5,75.5 175.2,92.6 176.9,74.7 178.6,39.1 180.3,52.7 182.0,75.6 183.7,83.2 185.4,63.9 187.1,62.2 188.8,58.3 190.6,69.5 192.3,80.3 194.0,76.6 195.7,57.5 197.4,50.6 199.1,63.3 200.8,77.4 202.5,77.6 204.2,56.0 205.9,53.6 207.6,55.9 209.3,90.8 211.0,85.1 212.7,58.3 214.4,53.6 216.1,63.6 217.8,68.8 219.5,62.5 221.2,59.9 222.9,82.9 224.6,72.2 226.3,58.5 228.0,67.3 229.7,68.1 231.5,61.6 233.2,59.4 234.9,70.4 236.6,73.9 238.3,57.0 240.0,80.1 241.7,69.3 243.4,78.0 245.1,53.4 246.8,43.9 248.5,80.5 250.2,59.4 251.9,73.3 253.6,73.9 255.3,68.8 257.0,58.7 258.7,60.6 260.4,76.4 262.1,75.9 263.8,55.1 265.5,54.3 267.2,81.5 268.9,76.4 270.6,63.0 272.4,45.3 274.1,69.6 275.8,68.2 277.5,83.4 279.2,55.5 280.9,64.9 282.6,78.1 284.3,75.7 286.0,49.4 287.7,53.9 289.4,54.5 291.1,78.4 292.8,77.5 294.5,79.0 296.2,52.7 297.9,71.5 299.6,72.5 301.3,51.0 303.0,80.1 304.7,60.4 306.4,83.0 308.1,64.8 309.8,43.2 311.5,64.1 313.2,73.7 315.0,67.2 316.7,63.6 318.4,70.0 320.1,82.2 321.8,76.3 323.5,51.3 325.2,57.0 326.9,63.3 328.6,74.1 330.3,68.1 332.0,70.2 333.7,66.4 335.4,54.7 337.1,55.3 338.8,67.9 340.5,73.4 342.2,85.6 343.9,66.8 345.6,62.8 347.3,65.3 349.0,67.0 350.7,58.0 352.4,51.4 354.1,82.3 355.9,77.4 357.6,78.0 359.3,59.0 361.0,49.5 362.7,62.8 364.4,62.1 366.1,77.3 367.8,76.6 369.5,73.9 371.2,49.0 372.9,69.8 374.6,69.5 376.3,63.3 378.0,70.3 379.7,58.6 381.4,70.9 383.1,65.2 384.8,65.0 386.5,70.1 388.2,69.0 389.9,61.6 391.6,68.1 393.3,77.7 395.0,70.0 396.8,42.9 398.5,68.6 400.2,78.1 401.9,69.8 403.6,49.8 405.3,68.9 407.0,69.9 408.7,73.0 410.4,74.6 412.1,64.0 413.8,55.0 415.5,60.4 417.2,65.0 418.9,79.6 420.6,62.2 422.3,63.1 424.0,82.2 425.7,67.9 427.4,55.8 429.1,76.6 430.8,79.8 432.5,54.1 434.2,57.9 435.9,56.4 437.6,66.6 439.4,70.6 441.1,78.3 442.8,69.6 444.5,56.1 446.2,60.1 447.9,65.3 449.6,76.4 451.3,65.3 453.0,80.0 454.7,56.7 456.4,59.8 458.1,62.4 459.8,43.4 461.5,88.4 463.2,89.3 464.9,59.7 466.6,71.6 468.3,74.9 470.0,55.2 471.7,53.1 473.4,54.4 475.1,71.3 476.8,82.9 478.5,67.2 480.3,72.8 482.0,59.0 483.7,50.9 485.4,61.3 487.1,94.0 488.8,61.9 490.5,66.5 492.2,56.0 493.9,63.4 495.6,69.4 497.3,76.8 499.0,63.0 500.7,71.5 502.4,70.1 504.1,54.0 505.8,55.9 507.5,76.2 509.2,67.9 510.9,80.5 512.6,66.4 514.3,54.4 516.0,70.5 517.7,53.1 519.4,66.9 521.2,68.0 522.9,75.3 524.6,85.4 526.3,67.9 528.0,49.2 529.7,56.0 531.4,54.0 533.1,83.0 534.8,91.2 536.5,56.6 538.2,60.4 539.9,61.1 541.6,55.6 543.3,78.1 545.0,65.5 546.7,79.0 548.4,52.4 550.1,79.5 551.8,68.8 553.5,49.7 555.2,58.9 556.9,72.2 558.6,76.6 560.3,74.2 562.0,79.1 563.8,50.0 565.5,45.3 567.2,59.2 568.9,77.5 570.6,83.9 572.3,79.7 574.0,70.0 575.7,63.5 577.4,28.3 579.1,61.3 580.8,78.5 582.5,92.4 584.2,62.3 585.9,77.2 587.6,44.6 589.3,67.2 591.0,40.7 592.7,82.7 594.4,77.9 596.1,87.5 597.8,63.6 599.5,48.9 601.2,57.0 602.9,54.0 604.7,85.8 606.4,66.5 608.1,67.2 609.8,80.9 611.5,79.6 613.2,41.6 614.9,42.8 616.6,89.5 618.3,74.6 620.0,66.7 621.7,76.4 623.4,74.7 625.1,44.0 626.8,42.4 628.5,85.4 630.2,70.1 631.9,96.7 633.6,52.9 635.3,63.5 637.0,43.6 638.7,38.3 640.4,85.7 642.1,84.5 643.8,81.5 645.6,96.2 647.3,46.1 649.0,28.6 650.7,50.3 652.4,99.7 654.1,67.1 655.8,81.5 657.5,79.9 659.2,54.5 660.9,33.4"/><text class="ink" x="44" y="14" font-size="12" text-anchor="start" font-weight="600">Kalıntı</text></g></svg>
  <figcaption>2024 yılı günlük satışı ve üç bileşeni. Dört panelin dikey ölçeği farklı: mevsim ±80, kalıntı ±40 aralığında. Alttaki üç paneli topla, üstteki çıkar.</figcaption>
</figure>

Dört paneli yukarıdan aşağıya oku:

- **Gözlem**: zikzaklı ham seri.
- **Trend**: zikzak gitmiş, yavaş dalga kalmış.
- **Mevsim**: her hafta birebir aynı yedi sayı.
- **Kalıntı**: sıfırın etrafında, desensiz görünen bir saçılma.

Aynı grafiği `result.plot()` tek satırda çiziyor.

## 4. Kalıntıyı oku

Ayrıştırmanın en değerli çıktısı çoğu zaman kalıntıdır: **beklenenin dışında**
ne olduğunu söylüyor.

```python
print(result.resid.abs().sort_values(ascending=False).head(3).round(1))
# 2023-12-30    47.5
# 2024-11-09    38.6
# 2022-05-14    38.4
```

30 Aralık 2023, trendin ve "cumartesi" payının açıkladığından 47.5 birim fazla.
Bölüm 07'de olağandışı günleri hareketli z-skoruyla aramıştın; kalıntı aynı işi
haftalık deseni de hesaba katarak yapıyor: cumartesi yüksek diye alarm vermiyor.

İyi bir ayrıştırmada kalıntı **desensiz** olmalı. Bunu sorgula:

```python
print(result.trend.groupby(result.trend.index.month).mean().round(0).tolist())
# [265, 259, 249, 237, 232, 231, 236, 250, 266, 280, 291, 322]
```

Trend bileşeni Haziran'da 231, Aralık'ta 322. Bu bir "yön" değil, **yıllık
mevsim**. `period=7` dediğin için ayrıştırma yalnızca haftalık deseni ayırdı;
haftadan yavaş olan her şey, yıllık dalga dahil, trendin içinde kaldı.

**"Trend" sandığın şey, seçtiğin periyottan yavaş olan her şeydir.** Yıllık
deseni de ayırmak için Kısım 8'e bak.

## 5. Toplamsal mı, çarpımsal mı?

Bölüm 09'da yolcu serisinde bir şey görmüştün: yaz–kış farkı 61'den 183'e
çıkıyor ama oranı hep 1.6. Mevsim, düzeyle **orantılı** büyüyor. Toplamsal
model "Ağustos her yıl +58" diyor; oysa 2013'te +30, 2024'te +100 civarı
gerekiyor.

Bu durumda bileşenler toplanmaz, **çarpılır**:

$$\text{gözlem} = \text{trend} \times \text{mevsim} \times \text{kalıntı}$$

```python
p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

mul = seasonal_decompose(p, model="multiplicative", period=12)
print(mul.seasonal.iloc[:12].round(3).tolist())
# [0.87, 0.83, 0.94, 0.964, 1.005, 1.12, 1.238, 1.255, 1.053, 0.95, 0.851, 0.924]
```

Mevsim artık fark değil **çarpan**: Ağustos trendin 1.255 katı (%25.5 üstünde),
Şubat 0.83 katı (%17 altında). Çarpanların ortalaması 1.

<figure class="fig">
<div class="versus">
<div><h4>Toplamsal</h4><p>gözlem = trend + mevsim + kalıntı</p><p>Mevsim <b>birim</b> cinsinden: "cumartesi +76".</p><p>Dalgaların boyu düzey ne olursa olsun aynı.</p></div>
<div><h4>Çarpımsal</h4><p>gözlem = trend × mevsim × kalıntı</p><p>Mevsim <b>oran</b>: "Ağustos × 1.255".</p><p>Dalgalar düzeyle birlikte büyüyor.</p></div>
</div>
<figcaption>Karar için seriyi çiz: dalgaların boyu yıllar içinde büyüyorsa çarpımsal.</figcaption>
</figure>

Yanlış modeli seçersen bunu **kalıntı** söyler:

<figure class="fig">
  <svg viewBox="0 0 680 220" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="40" y1="190.0" x2="316" y2="190.0"/><text class="dim" x="34" y="193.5" font-size="10.5" text-anchor="end">−40</text><line class="grid" x1="40" y1="149.5" x2="316" y2="149.5"/><text class="dim" x="34" y="153.0" font-size="10.5" text-anchor="end">−20</text><line class="line" x1="40" y1="109.0" x2="316" y2="109.0"/><text class="dim" x="34" y="112.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="68.5" x2="316" y2="68.5"/><text class="dim" x="34" y="72.0" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="40" y1="28.0" x2="316" y2="28.0"/><text class="dim" x="34" y="31.5" font-size="10.5" text-anchor="end">40</text><line class="line" x1="40" y1="190" x2="316" y2="190"/><line class="line" x1="63.2" y1="190" x2="63.2" y2="194"/><text class="dim" x="63.2" y="206" font-size="10.5" text-anchor="middle">2014</text><line class="line" x1="155.8" y1="190" x2="155.8" y2="194"/><text class="dim" x="155.8" y="206" font-size="10.5" text-anchor="middle">2018</text><line class="line" x1="248.4" y1="190" x2="248.4" y2="194"/><text class="dim" x="248.4" y="206" font-size="10.5" text-anchor="middle">2022</text><rect class="dot2" x="50.9" y="109.0" width="1.4" height="44.5" rx="3" opacity="0.9"/><rect class="dot2" x="52.8" y="109.0" width="1.4" height="46.7" rx="3" opacity="0.9"/><rect class="dot2" x="54.8" y="109.0" width="1.3" height="11.0" rx="3" opacity="0.9"/><rect class="dot2" x="56.7" y="102.2" width="1.3" height="6.8" rx="3" opacity="0.9"/><rect class="dot2" x="58.6" y="79.2" width="1.4" height="29.8" rx="3" opacity="0.9"/><rect class="dot2" x="60.6" y="93.8" width="1.3" height="15.2" rx="3" opacity="0.9"/><rect class="dot2" x="62.5" y="81.8" width="1.3" height="27.2" rx="3" opacity="0.9"/><rect class="dot2" x="64.4" y="74.7" width="1.4" height="34.3" rx="3" opacity="0.9"/><rect class="dot2" x="66.3" y="96.3" width="1.4" height="12.7" rx="3" opacity="0.9"/><rect class="dot2" x="68.3" y="94.8" width="1.3" height="14.2" rx="3" opacity="0.9"/><rect class="dot2" x="70.2" y="109.0" width="1.4" height="3.4" rx="3" opacity="0.9"/><rect class="dot2" x="72.1" y="109.0" width="1.4" height="25.8" rx="3" opacity="0.9"/><rect class="dot2" x="74.1" y="109.0" width="1.3" height="46.4" rx="3" opacity="0.9"/><rect class="dot2" x="76.0" y="109.0" width="1.3" height="53.1" rx="3" opacity="0.9"/><rect class="dot2" x="77.9" y="109.0" width="1.4" height="13.3" rx="3" opacity="0.9"/><rect class="dot2" x="79.9" y="97.6" width="1.3" height="11.4" rx="3" opacity="0.9"/><rect class="dot2" x="81.8" y="87.1" width="1.3" height="21.9" rx="3" opacity="0.9"/><rect class="dot2" x="83.7" y="92.4" width="1.4" height="16.6" rx="3" opacity="0.9"/><rect class="dot2" x="85.6" y="81.4" width="1.4" height="27.6" rx="3" opacity="0.9"/><rect class="dot2" x="87.6" y="76.1" width="1.3" height="32.9" rx="3" opacity="0.9"/><rect class="dot2" x="89.5" y="109.0" width="1.4" height="0.7" rx="3" opacity="0.9"/><rect class="dot2" x="91.4" y="100.6" width="1.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="93.4" y="106.9" width="1.3" height="2.1" rx="3" opacity="0.9"/><rect class="dot2" x="95.3" y="109.0" width="1.3" height="19.2" rx="3" opacity="0.9"/><rect class="dot2" x="97.2" y="109.0" width="1.4" height="37.6" rx="3" opacity="0.9"/><rect class="dot2" x="99.2" y="109.0" width="1.3" height="40.5" rx="3" opacity="0.9"/><rect class="dot2" x="101.1" y="109.0" width="1.3" height="8.0" rx="3" opacity="0.9"/><rect class="dot2" x="103.0" y="105.9" width="1.4" height="3.1" rx="3" opacity="0.9"/><rect class="dot2" x="104.9" y="83.5" width="1.4" height="25.5" rx="3" opacity="0.9"/><rect class="dot2" x="106.9" y="102.8" width="1.3" height="6.2" rx="3" opacity="0.9"/><rect class="dot2" x="108.8" y="89.7" width="1.4" height="19.3" rx="3" opacity="0.9"/><rect class="dot2" x="110.7" y="78.5" width="1.4" height="30.5" rx="3" opacity="0.9"/><rect class="dot2" x="112.7" y="104.4" width="1.3" height="4.6" rx="3" opacity="0.9"/><rect class="dot2" x="114.6" y="104.1" width="1.3" height="4.9" rx="3" opacity="0.9"/><rect class="dot2" x="116.5" y="108.0" width="1.4" height="1.0" rx="3" opacity="0.9"/><rect class="dot2" x="118.5" y="109.0" width="1.3" height="18.4" rx="3" opacity="0.9"/><rect class="dot2" x="120.4" y="109.0" width="1.3" height="31.4" rx="3" opacity="0.9"/><rect class="dot2" x="122.3" y="109.0" width="1.4" height="32.6" rx="3" opacity="0.9"/><rect class="dot2" x="124.2" y="103.3" width="1.4" height="5.7" rx="3" opacity="0.9"/><rect class="dot2" x="126.2" y="109.0" width="1.3" height="5.4" rx="3" opacity="0.9"/><rect class="dot2" x="128.1" y="92.1" width="1.4" height="16.9" rx="3" opacity="0.9"/><rect class="dot2" x="130.0" y="101.9" width="1.4" height="7.1" rx="3" opacity="0.9"/><rect class="dot2" x="132.0" y="99.8" width="1.3" height="9.2" rx="3" opacity="0.9"/><rect class="dot2" x="133.9" y="81.3" width="1.3" height="27.7" rx="3" opacity="0.9"/><rect class="dot2" x="135.8" y="100.7" width="1.4" height="8.3" rx="3" opacity="0.9"/><rect class="dot2" x="137.8" y="109.0" width="1.3" height="3.6" rx="3" opacity="0.9"/><rect class="dot2" x="139.7" y="109.0" width="1.3" height="0.7" rx="3" opacity="0.9"/><rect class="dot2" x="141.6" y="109.0" width="1.4" height="12.0" rx="3" opacity="0.9"/><rect class="dot2" x="143.5" y="109.0" width="1.4" height="17.0" rx="3" opacity="0.9"/><rect class="dot2" x="145.5" y="109.0" width="1.3" height="19.9" rx="3" opacity="0.9"/><rect class="dot2" x="147.4" y="109.0" width="1.4" height="2.9" rx="3" opacity="0.9"/><rect class="dot2" x="149.3" y="102.7" width="1.4" height="6.3" rx="3" opacity="0.9"/><rect class="dot2" x="151.3" y="94.9" width="1.3" height="14.1" rx="3" opacity="0.9"/><rect class="dot2" x="153.2" y="109.0" width="1.3" height="1.4" rx="3" opacity="0.9"/><rect class="dot2" x="155.1" y="100.3" width="1.4" height="8.7" rx="3" opacity="0.9"/><rect class="dot2" x="157.1" y="100.6" width="1.3" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="159.0" y="106.3" width="1.3" height="2.7" rx="3" opacity="0.9"/><rect class="dot2" x="160.9" y="109.0" width="1.4" height="4.4" rx="3" opacity="0.9"/><rect class="dot2" x="162.8" y="109.0" width="1.4" height="2.6" rx="3" opacity="0.9"/><rect class="dot2" x="164.8" y="109.0" width="1.3" height="9.6" rx="3" opacity="0.9"/><rect class="dot2" x="166.7" y="101.2" width="1.4" height="7.8" rx="3" opacity="0.9"/><rect class="dot2" x="168.6" y="108.7" width="1.4" height="0.3" rx="3" opacity="0.9"/><rect class="dot2" x="170.6" y="109.0" width="1.3" height="8.5" rx="3" opacity="0.9"/><rect class="dot2" x="172.5" y="109.0" width="1.4" height="4.8" rx="3" opacity="0.9"/><rect class="dot2" x="174.4" y="105.1" width="1.4" height="3.9" rx="3" opacity="0.9"/><rect class="dot2" x="176.4" y="109.0" width="1.3" height="14.4" rx="3" opacity="0.9"/><rect class="dot2" x="178.3" y="108.9" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot2" x="180.2" y="104.7" width="1.4" height="4.3" rx="3" opacity="0.9"/><rect class="dot2" x="182.1" y="99.4" width="1.4" height="9.6" rx="3" opacity="0.9"/><rect class="dot2" x="184.1" y="102.2" width="1.3" height="6.8" rx="3" opacity="0.9"/><rect class="dot2" x="186.0" y="109.0" width="1.4" height="2.5" rx="3" opacity="0.9"/><rect class="dot2" x="187.9" y="109.0" width="1.4" height="8.9" rx="3" opacity="0.9"/><rect class="dot2" x="189.9" y="104.0" width="1.3" height="5.0" rx="3" opacity="0.9"/><rect class="dot2" x="191.8" y="95.5" width="1.4" height="13.5" rx="3" opacity="0.9"/><rect class="dot2" x="193.7" y="107.4" width="1.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot2" x="195.7" y="109.0" width="1.3" height="3.5" rx="3" opacity="0.9"/><rect class="dot2" x="197.6" y="109.0" width="1.3" height="4.9" rx="3" opacity="0.9"/><rect class="dot2" x="199.5" y="109.0" width="1.4" height="6.5" rx="3" opacity="0.9"/><rect class="dot2" x="201.5" y="109.0" width="1.3" height="5.9" rx="3" opacity="0.9"/><rect class="dot2" x="203.4" y="109.0" width="1.3" height="14.3" rx="3" opacity="0.9"/><rect class="dot2" x="205.3" y="109.0" width="1.4" height="4.4" rx="3" opacity="0.9"/><rect class="dot2" x="207.2" y="109.0" width="1.4" height="5.6" rx="3" opacity="0.9"/><rect class="dot2" x="209.2" y="98.3" width="1.3" height="10.7" rx="3" opacity="0.9"/><rect class="dot2" x="211.1" y="102.9" width="1.4" height="6.1" rx="3" opacity="0.9"/><rect class="dot2" x="213.0" y="88.6" width="1.4" height="20.4" rx="3" opacity="0.9"/><rect class="dot2" x="215.0" y="93.0" width="1.3" height="16.0" rx="3" opacity="0.9"/><rect class="dot2" x="216.9" y="105.8" width="1.3" height="3.2" rx="3" opacity="0.9"/><rect class="dot2" x="218.8" y="102.7" width="1.4" height="6.3" rx="3" opacity="0.9"/><rect class="dot2" x="220.8" y="109.0" width="1.3" height="14.5" rx="3" opacity="0.9"/><rect class="dot2" x="222.7" y="109.0" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot2" x="224.6" y="109.0" width="1.4" height="19.1" rx="3" opacity="0.9"/><rect class="dot2" x="226.5" y="109.0" width="1.4" height="9.1" rx="3" opacity="0.9"/><rect class="dot2" x="228.5" y="109.0" width="1.3" height="23.1" rx="3" opacity="0.9"/><rect class="dot2" x="230.4" y="109.0" width="1.4" height="19.3" rx="3" opacity="0.9"/><rect class="dot2" x="232.3" y="107.3" width="1.4" height="1.7" rx="3" opacity="0.9"/><rect class="dot2" x="234.3" y="108.0" width="1.3" height="1.0" rx="3" opacity="0.9"/><rect class="dot2" x="236.2" y="68.5" width="1.3" height="40.5" rx="3" opacity="0.9"/><rect class="dot2" x="238.1" y="53.2" width="1.4" height="55.8" rx="3" opacity="0.9"/><rect class="dot2" x="240.1" y="106.1" width="1.3" height="2.9" rx="3" opacity="0.9"/><rect class="dot2" x="242.0" y="109.0" width="1.3" height="14.1" rx="3" opacity="0.9"/><rect class="dot2" x="243.9" y="109.0" width="1.4" height="25.0" rx="3" opacity="0.9"/><rect class="dot2" x="245.8" y="109.0" width="1.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="247.8" y="109.0" width="1.3" height="20.8" rx="3" opacity="0.9"/><rect class="dot2" x="249.7" y="109.0" width="1.4" height="24.6" rx="3" opacity="0.9"/><rect class="dot2" x="251.6" y="109.0" width="1.4" height="2.8" rx="3" opacity="0.9"/><rect class="dot2" x="253.6" y="105.8" width="1.3" height="3.2" rx="3" opacity="0.9"/><rect class="dot2" x="255.5" y="109.0" width="1.3" height="9.6" rx="3" opacity="0.9"/><rect class="dot2" x="257.4" y="93.6" width="1.4" height="15.4" rx="3" opacity="0.9"/><rect class="dot2" x="259.4" y="56.0" width="1.3" height="53.0" rx="3" opacity="0.9"/><rect class="dot2" x="261.3" y="85.3" width="1.3" height="23.7" rx="3" opacity="0.9"/><rect class="dot2" x="263.2" y="88.6" width="1.4" height="20.4" rx="3" opacity="0.9"/><rect class="dot2" x="265.1" y="109.0" width="1.4" height="15.8" rx="3" opacity="0.9"/><rect class="dot2" x="267.1" y="109.0" width="1.3" height="21.2" rx="3" opacity="0.9"/><rect class="dot2" x="269.0" y="109.0" width="1.4" height="11.4" rx="3" opacity="0.9"/><rect class="dot2" x="270.9" y="109.0" width="1.4" height="21.0" rx="3" opacity="0.9"/><rect class="dot2" x="272.9" y="109.0" width="1.3" height="35.3" rx="3" opacity="0.9"/><rect class="dot2" x="274.8" y="109.0" width="1.3" height="11.5" rx="3" opacity="0.9"/><rect class="dot2" x="276.7" y="109.0" width="1.4" height="23.5" rx="3" opacity="0.9"/><rect class="dot2" x="278.7" y="109.0" width="1.3" height="6.1" rx="3" opacity="0.9"/><rect class="dot2" x="280.6" y="73.8" width="1.3" height="35.2" rx="3" opacity="0.9"/><rect class="dot2" x="282.5" y="67.5" width="1.4" height="41.5" rx="3" opacity="0.9"/><rect class="dot2" x="284.4" y="34.3" width="1.4" height="74.7" rx="3" opacity="0.9"/><rect class="dot2" x="286.4" y="107.9" width="1.3" height="1.1" rx="3" opacity="0.9"/><rect class="dot2" x="288.3" y="108.1" width="1.4" height="0.9" rx="3" opacity="0.9"/><rect class="dot2" x="290.2" y="109.0" width="1.4" height="55.4" rx="3" opacity="0.9"/><rect class="dot2" x="292.2" y="109.0" width="1.3" height="11.8" rx="3" opacity="0.9"/><rect class="dot2" x="294.1" y="109.0" width="1.3" height="34.1" rx="3" opacity="0.9"/><rect class="dot2" x="296.0" y="109.0" width="1.4" height="63.6" rx="3" opacity="0.9"/><rect class="dot2" x="298.0" y="109.0" width="1.3" height="4.4" rx="3" opacity="0.9"/><rect class="dot2" x="299.9" y="99.0" width="1.3" height="10.0" rx="3" opacity="0.9"/><rect class="dot2" x="301.8" y="108.2" width="1.4" height="0.8" rx="3" opacity="0.9"/><rect class="dot2" x="303.7" y="81.6" width="1.4" height="27.4" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Toplamsal modelin kalıntısı (bin yolcu)</text></g><g transform="translate(350,0)"><line class="grid" x1="40" y1="190.0" x2="316" y2="190.0"/><text class="dim" x="34" y="193.5" font-size="10.5" text-anchor="end">−40</text><line class="grid" x1="40" y1="149.5" x2="316" y2="149.5"/><text class="dim" x="34" y="153.0" font-size="10.5" text-anchor="end">−20</text><line class="line" x1="40" y1="109.0" x2="316" y2="109.0"/><text class="dim" x="34" y="112.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="68.5" x2="316" y2="68.5"/><text class="dim" x="34" y="72.0" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="40" y1="28.0" x2="316" y2="28.0"/><text class="dim" x="34" y="31.5" font-size="10.5" text-anchor="end">40</text><line class="line" x1="40" y1="190" x2="316" y2="190"/><line class="line" x1="63.2" y1="190" x2="63.2" y2="194"/><text class="dim" x="63.2" y="206" font-size="10.5" text-anchor="middle">2014</text><line class="line" x1="155.8" y1="190" x2="155.8" y2="194"/><text class="dim" x="155.8" y="206" font-size="10.5" text-anchor="middle">2018</text><line class="line" x1="248.4" y1="190" x2="248.4" y2="194"/><text class="dim" x="248.4" y="206" font-size="10.5" text-anchor="middle">2022</text><rect class="dot" x="50.9" y="107.4" width="1.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="52.8" y="106.3" width="1.4" height="2.7" rx="3" opacity="0.9"/><rect class="dot" x="54.8" y="109.0" width="1.3" height="0.0" rx="3" opacity="0.9"/><rect class="dot" x="56.7" y="109.0" width="1.3" height="1.4" rx="3" opacity="0.9"/><rect class="dot" x="58.6" y="108.8" width="1.4" height="0.2" rx="3" opacity="0.9"/><rect class="dot" x="60.6" y="108.1" width="1.3" height="0.9" rx="3" opacity="0.9"/><rect class="dot" x="62.5" y="107.9" width="1.3" height="1.1" rx="3" opacity="0.9"/><rect class="dot" x="64.4" y="109.0" width="1.4" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="66.3" y="107.8" width="1.4" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="68.3" y="103.6" width="1.3" height="5.4" rx="3" opacity="0.9"/><rect class="dot" x="70.2" y="109.0" width="1.4" height="1.5" rx="3" opacity="0.9"/><rect class="dot" x="72.1" y="108.7" width="1.4" height="0.3" rx="3" opacity="0.9"/><rect class="dot" x="74.1" y="109.0" width="1.3" height="2.9" rx="3" opacity="0.9"/><rect class="dot" x="76.0" y="109.0" width="1.3" height="4.7" rx="3" opacity="0.9"/><rect class="dot" x="77.9" y="109.0" width="1.4" height="2.4" rx="3" opacity="0.9"/><rect class="dot" x="79.9" y="106.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="81.8" y="109.0" width="1.3" height="3.3" rx="3" opacity="0.9"/><rect class="dot" x="83.7" y="105.7" width="1.4" height="3.3" rx="3" opacity="0.9"/><rect class="dot" x="85.6" y="105.1" width="1.4" height="3.9" rx="3" opacity="0.9"/><rect class="dot" x="87.6" y="107.4" width="1.3" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="89.5" y="109.0" width="1.4" height="7.1" rx="3" opacity="0.9"/><rect class="dot" x="91.4" y="107.4" width="1.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="93.4" y="106.9" width="1.3" height="2.1" rx="3" opacity="0.9"/><rect class="dot" x="95.3" y="107.0" width="1.3" height="2.0" rx="3" opacity="0.9"/><rect class="dot" x="97.2" y="109.0" width="1.4" height="2.0" rx="3" opacity="0.9"/><rect class="dot" x="99.2" y="109.0" width="1.3" height="2.0" rx="3" opacity="0.9"/><rect class="dot" x="101.1" y="109.0" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="103.0" y="109.0" width="1.4" height="1.7" rx="3" opacity="0.9"/><rect class="dot" x="104.9" y="105.5" width="1.4" height="3.5" rx="3" opacity="0.9"/><rect class="dot" x="106.9" y="109.0" width="1.3" height="2.2" rx="3" opacity="0.9"/><rect class="dot" x="108.8" y="108.2" width="1.4" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="110.7" y="105.0" width="1.4" height="4.0" rx="3" opacity="0.9"/><rect class="dot" x="112.7" y="109.0" width="1.3" height="1.7" rx="3" opacity="0.9"/><rect class="dot" x="114.6" y="108.9" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="116.5" y="107.8" width="1.4" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="118.5" y="109.0" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="120.4" y="109.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="122.3" y="109.0" width="1.4" height="2.4" rx="3" opacity="0.9"/><rect class="dot" x="124.2" y="102.7" width="1.4" height="6.3" rx="3" opacity="0.9"/><rect class="dot" x="126.2" y="109.0" width="1.3" height="5.5" rx="3" opacity="0.9"/><rect class="dot" x="128.1" y="107.9" width="1.4" height="1.1" rx="3" opacity="0.9"/><rect class="dot" x="130.0" y="108.7" width="1.4" height="0.3" rx="3" opacity="0.9"/><rect class="dot" x="132.0" y="109.0" width="1.3" height="2.5" rx="3" opacity="0.9"/><rect class="dot" x="133.9" y="102.9" width="1.3" height="6.1" rx="3" opacity="0.9"/><rect class="dot" x="135.8" y="107.0" width="1.4" height="2.0" rx="3" opacity="0.9"/><rect class="dot" x="137.8" y="109.0" width="1.3" height="3.8" rx="3" opacity="0.9"/><rect class="dot" x="139.7" y="108.9" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="141.6" y="108.3" width="1.4" height="0.7" rx="3" opacity="0.9"/><rect class="dot" x="143.5" y="109.0" width="1.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="145.5" y="109.0" width="1.3" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="147.4" y="108.6" width="1.4" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="149.3" y="106.6" width="1.4" height="2.4" rx="3" opacity="0.9"/><rect class="dot" x="151.3" y="106.2" width="1.3" height="2.8" rx="3" opacity="0.9"/><rect class="dot" x="153.2" y="109.0" width="1.3" height="2.8" rx="3" opacity="0.9"/><rect class="dot" x="155.1" y="108.7" width="1.4" height="0.3" rx="3" opacity="0.9"/><rect class="dot" x="157.1" y="109.0" width="1.3" height="1.9" rx="3" opacity="0.9"/><rect class="dot" x="159.0" y="108.9" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="160.9" y="109.0" width="1.4" height="3.2" rx="3" opacity="0.9"/><rect class="dot" x="162.8" y="109.0" width="1.4" height="0.9" rx="3" opacity="0.9"/><rect class="dot" x="164.8" y="109.0" width="1.3" height="0.3" rx="3" opacity="0.9"/><rect class="dot" x="166.7" y="103.6" width="1.4" height="5.4" rx="3" opacity="0.9"/><rect class="dot" x="168.6" y="106.2" width="1.4" height="2.8" rx="3" opacity="0.9"/><rect class="dot" x="170.6" y="109.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="172.5" y="109.0" width="1.4" height="2.2" rx="3" opacity="0.9"/><rect class="dot" x="174.4" y="108.5" width="1.4" height="0.5" rx="3" opacity="0.9"/><rect class="dot" x="176.4" y="109.0" width="1.3" height="7.2" rx="3" opacity="0.9"/><rect class="dot" x="178.3" y="109.0" width="1.3" height="1.3" rx="3" opacity="0.9"/><rect class="dot" x="180.2" y="109.0" width="1.4" height="0.0" rx="3" opacity="0.9"/><rect class="dot" x="182.1" y="104.4" width="1.4" height="4.6" rx="3" opacity="0.9"/><rect class="dot" x="184.1" y="106.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="186.0" y="109.0" width="1.4" height="0.9" rx="3" opacity="0.9"/><rect class="dot" x="187.9" y="109.0" width="1.4" height="2.2" rx="3" opacity="0.9"/><rect class="dot" x="189.9" y="109.0" width="1.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="191.8" y="106.3" width="1.4" height="2.7" rx="3" opacity="0.9"/><rect class="dot" x="193.7" y="108.7" width="1.4" height="0.3" rx="3" opacity="0.9"/><rect class="dot" x="195.7" y="109.0" width="1.3" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="197.6" y="109.0" width="1.3" height="0.5" rx="3" opacity="0.9"/><rect class="dot" x="199.5" y="109.0" width="1.4" height="1.4" rx="3" opacity="0.9"/><rect class="dot" x="201.5" y="109.0" width="1.3" height="0.9" rx="3" opacity="0.9"/><rect class="dot" x="203.4" y="109.0" width="1.3" height="4.8" rx="3" opacity="0.9"/><rect class="dot" x="205.3" y="109.0" width="1.4" height="0.5" rx="3" opacity="0.9"/><rect class="dot" x="207.2" y="109.0" width="1.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="209.2" y="104.8" width="1.3" height="4.2" rx="3" opacity="0.9"/><rect class="dot" x="211.1" y="107.9" width="1.4" height="1.1" rx="3" opacity="0.9"/><rect class="dot" x="213.0" y="108.1" width="1.4" height="0.9" rx="3" opacity="0.9"/><rect class="dot" x="215.0" y="109.0" width="1.3" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="216.9" y="109.0" width="1.3" height="0.2" rx="3" opacity="0.9"/><rect class="dot" x="218.8" y="104.5" width="1.4" height="4.5" rx="3" opacity="0.9"/><rect class="dot" x="220.8" y="109.0" width="1.3" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="222.7" y="106.2" width="1.3" height="2.8" rx="3" opacity="0.9"/><rect class="dot" x="224.6" y="109.0" width="1.4" height="3.7" rx="3" opacity="0.9"/><rect class="dot" x="226.5" y="107.3" width="1.4" height="1.7" rx="3" opacity="0.9"/><rect class="dot" x="228.5" y="109.0" width="1.3" height="6.4" rx="3" opacity="0.9"/><rect class="dot" x="230.4" y="109.0" width="1.4" height="5.8" rx="3" opacity="0.9"/><rect class="dot" x="232.3" y="108.4" width="1.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="234.3" y="109.0" width="1.3" height="2.6" rx="3" opacity="0.9"/><rect class="dot" x="236.2" y="106.1" width="1.3" height="2.9" rx="3" opacity="0.9"/><rect class="dot" x="238.1" y="102.5" width="1.4" height="6.5" rx="3" opacity="0.9"/><rect class="dot" x="240.1" y="109.0" width="1.3" height="1.2" rx="3" opacity="0.9"/><rect class="dot" x="242.0" y="109.0" width="1.3" height="2.1" rx="3" opacity="0.9"/><rect class="dot" x="243.9" y="109.0" width="1.4" height="1.7" rx="3" opacity="0.9"/><rect class="dot" x="245.8" y="107.7" width="1.4" height="1.3" rx="3" opacity="0.9"/><rect class="dot" x="247.8" y="109.0" width="1.3" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="249.7" y="109.0" width="1.4" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="251.6" y="106.5" width="1.4" height="2.5" rx="3" opacity="0.9"/><rect class="dot" x="253.6" y="106.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="255.5" y="109.0" width="1.3" height="3.2" rx="3" opacity="0.9"/><rect class="dot" x="257.4" y="109.0" width="1.4" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="259.4" y="107.1" width="1.3" height="1.9" rx="3" opacity="0.9"/><rect class="dot" x="261.3" y="109.0" width="1.3" height="6.2" rx="3" opacity="0.9"/><rect class="dot" x="263.2" y="106.0" width="1.4" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="265.1" y="109.0" width="1.4" height="1.5" rx="3" opacity="0.9"/><rect class="dot" x="267.1" y="106.0" width="1.3" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="269.0" y="107.3" width="1.4" height="1.7" rx="3" opacity="0.9"/><rect class="dot" x="270.9" y="107.1" width="1.4" height="1.9" rx="3" opacity="0.9"/><rect class="dot" x="272.9" y="109.0" width="1.3" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="274.8" y="108.2" width="1.3" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="276.7" y="109.0" width="1.4" height="4.7" rx="3" opacity="0.9"/><rect class="dot" x="278.7" y="109.0" width="1.3" height="2.0" rx="3" opacity="0.9"/><rect class="dot" x="280.6" y="106.2" width="1.3" height="2.8" rx="3" opacity="0.9"/><rect class="dot" x="282.5" y="109.0" width="1.4" height="4.5" rx="3" opacity="0.9"/><rect class="dot" x="284.4" y="106.8" width="1.4" height="2.2" rx="3" opacity="0.9"/><rect class="dot" x="286.4" y="109.0" width="1.3" height="3.3" rx="3" opacity="0.9"/><rect class="dot" x="288.3" y="104.5" width="1.4" height="4.5" rx="3" opacity="0.9"/><rect class="dot" x="290.2" y="109.0" width="1.4" height="4.7" rx="3" opacity="0.9"/><rect class="dot" x="292.2" y="105.9" width="1.3" height="3.1" rx="3" opacity="0.9"/><rect class="dot" x="294.1" y="108.3" width="1.3" height="0.7" rx="3" opacity="0.9"/><rect class="dot" x="296.0" y="109.0" width="1.4" height="5.2" rx="3" opacity="0.9"/><rect class="dot" x="298.0" y="105.0" width="1.3" height="4.0" rx="3" opacity="0.9"/><rect class="dot" x="299.9" y="103.3" width="1.3" height="5.7" rx="3" opacity="0.9"/><rect class="dot" x="301.8" y="109.0" width="1.4" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="303.7" y="109.0" width="1.4" height="1.6" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Çarpımsal modelin kalıntısı (%)</text></g></svg>
  <figcaption>Aynı seri, iki model, aynı dikey ölçek. Solda kalıntı uçlarda büyük, ortada küçük ve işareti düzenli değişiyor: model yanlış. Sağda her yıl aynı dar bant.</figcaption>
</figure>

Toplamsal modelde Temmuz kalıntısı 2013'te −22, 2023'te +20: model ilk
yıllarda mevsimi fazla, son yıllarda eksik tahmin ediyor. Kalıntıda desen var,
yani model yanlış. Çarpımsal modelde kalıntı bütün yıllarda %±3.6 içinde.

**Logaritma köprüsü.** $\log(a \times b) = \log a + \log b$ olduğu için
çarpımsal bir serinin logaritması toplamsaldır. Yalnızca toplamsal çalışan bir
yöntemin (aşağıdaki STL gibi) önüne `np.log(p)` koyarsın, sonucu `np.exp` ile
geri çevirirsin. Bölüm 09'daki logaritmik eksenin dalgaları eşitlemesinin
nedeni de bu.

Çarpımsal model sıfır ya da eksi değer içeren seride çalışmaz.

## 6. Mevsimsellikten arındırılmış seri

Haberlerde "mevsim etkisinden arındırılmış işsizlik" diye duyduğun şey:
seriden yalnızca mevsim bileşenini çıkarmak.

```python
adjusted = p / mul.seasonal          # toplamsal modelde: s - result.seasonal
```

2024 yazının sonu:

```text
             ham    arindirilmis
2024-07      487       393.3
2024-08      480       382.6
2024-09      430       408.2
```

Ham seri Eylül'de **%10.4 düşüş** gösteriyor. Arındırılmış seri **%6.7 artış**:
Eylül'de yolcu her yıl azalır, bu yıl beklenenden az azalmış. "İşler kötüye
mi gidiyor?" sorusunun cevabı ham seride değil, arındırılmış seride.

Günlük satışta da aynı: 2 Kasım 2024 Cumartesi 422, 4 Kasım Pazartesi 272.
Haftalık pay çıkarılınca 345.8 ve 314.6: aradaki 150 birimlik farkın çoğu
"cumartesi olmak"tan geliyormuş.

## 7. Klasik yöntemin sınırları ve STL

`seasonal_decompose` klasik yöntem; basit ve şeffaf, ama üç zayıflığı var:

1. **Uçlar boş.** Ortalanmış pencere yüzünden başta ve sonda yarım periyot
   trend yok. Aylık veride son 6 ay: tam da en çok merak ettiğin kısım.
2. **Mevsim hiç değişmiyor.** Her cumartesi için tek sayı: 76.2. Oysa mağaza
   büyüdükçe cumartesi payı da büyüyor.
3. **Aykırı değere dayanıksız.** Tek bir sıçrama, ortalamaya girdiği yedi günün
   trendini yukarı çekiyor.

**STL** (LOESS ile mevsim–trend ayrıştırması) üçünü de çözüyor:

```python
from statsmodels.tsa.seasonal import STL

fit = STL(s, period=7, robust=True).fit()
fit.trend, fit.seasonal, fit.resid
```

- Uçlarda `NaN` yok: trend ilk günden son güne tanımlı.
- Mevsim zamanla **yavaşça değişebiliyor**: cumartesi payı 2022'de ortalama
  66.6, 2024'te 85.7.
- `robust=True` aykırı günlere düşük ağırlık veriyor.

Üçüncüsünü web trafiğinde gör. 14 Mart 2024'te kampanya günü: 9593 ziyaret,
normal düzey 3750 civarı.

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="194.1" x2="666" y2="194.1"/><text class="dim" x="38" y="197.6" font-size="10.5" text-anchor="end">4,000</text><line class="grid" x1="44" y1="151.4" x2="666" y2="151.4"/><text class="dim" x="38" y="154.9" font-size="10.5" text-anchor="end">6,000</text><line class="grid" x1="44" y1="108.6" x2="666" y2="108.6"/><text class="dim" x="38" y="112.1" font-size="10.5" text-anchor="end">8,000</text><line class="grid" x1="44" y1="65.9" x2="666" y2="65.9"/><text class="dim" x="38" y="69.4" font-size="10.5" text-anchor="end">10,000</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="117.2" y1="230" x2="117.2" y2="234"/><text class="dim" x="117.2" y="246" font-size="10.5" text-anchor="middle">1 Mar</text><line class="line" x1="245.2" y1="230" x2="245.2" y2="234"/><text class="dim" x="245.2" y="246" font-size="10.5" text-anchor="middle">8 Mar</text><line class="line" x1="355.0" y1="230" x2="355.0" y2="234"/><text class="dim" x="355.0" y="246" font-size="10.5" text-anchor="middle">14 Mar</text><line class="line" x1="501.4" y1="230" x2="501.4" y2="234"/><text class="dim" x="501.4" y="246" font-size="10.5" text-anchor="middle">22 Mar</text><line class="line" x1="629.4" y1="230" x2="629.4" y2="234"/><text class="dim" x="629.4" y="246" font-size="10.5" text-anchor="middle">29 Mar</text><polyline class="curve3" style="stroke-width:1.4" points="44.0,197.2 62.3,194.3 80.6,196.8 98.9,197.5 117.2,193.6 135.5,219.1 153.8,218.0 172.1,195.9 190.4,191.4 208.6,197.5 226.9,190.7 245.2,188.2 263.5,218.8 281.8,212.4 300.1,185.0 318.4,192.2 336.7,199.7 355.0,74.6 373.3,194.9 391.6,212.3 409.9,216.2 428.2,190.8 446.5,195.2 464.8,197.2 483.1,192.5 501.4,198.7 519.6,218.6 537.9,216.4 556.2,194.0 574.5,191.8 592.8,196.0 611.1,191.5 629.4,192.4 647.7,222.9 666.0,221.2"/><circle class="dim" cx="44.0" cy="197.2" r="2.4"/><circle class="dim" cx="62.3" cy="194.3" r="2.4"/><circle class="dim" cx="80.6" cy="196.8" r="2.4"/><circle class="dim" cx="98.9" cy="197.5" r="2.4"/><circle class="dim" cx="117.2" cy="193.6" r="2.4"/><circle class="dim" cx="135.5" cy="219.1" r="2.4"/><circle class="dim" cx="153.8" cy="218.0" r="2.4"/><circle class="dim" cx="172.1" cy="195.9" r="2.4"/><circle class="dim" cx="190.4" cy="191.4" r="2.4"/><circle class="dim" cx="208.6" cy="197.5" r="2.4"/><circle class="dim" cx="226.9" cy="190.7" r="2.4"/><circle class="dim" cx="245.2" cy="188.2" r="2.4"/><circle class="dim" cx="263.5" cy="218.8" r="2.4"/><circle class="dim" cx="281.8" cy="212.4" r="2.4"/><circle class="dim" cx="300.1" cy="185.0" r="2.4"/><circle class="dim" cx="318.4" cy="192.2" r="2.4"/><circle class="dim" cx="336.7" cy="199.7" r="2.4"/><circle class="dim" cx="355.0" cy="74.6" r="2.4"/><circle class="dim" cx="373.3" cy="194.9" r="2.4"/><circle class="dim" cx="391.6" cy="212.3" r="2.4"/><circle class="dim" cx="409.9" cy="216.2" r="2.4"/><circle class="dim" cx="428.2" cy="190.8" r="2.4"/><circle class="dim" cx="446.5" cy="195.2" r="2.4"/><circle class="dim" cx="464.8" cy="197.2" r="2.4"/><circle class="dim" cx="483.1" cy="192.5" r="2.4"/><circle class="dim" cx="501.4" cy="198.7" r="2.4"/><circle class="dim" cx="519.6" cy="218.6" r="2.4"/><circle class="dim" cx="537.9" cy="216.4" r="2.4"/><circle class="dim" cx="556.2" cy="194.0" r="2.4"/><circle class="dim" cx="574.5" cy="191.8" r="2.4"/><circle class="dim" cx="592.8" cy="196.0" r="2.4"/><circle class="dim" cx="611.1" cy="191.5" r="2.4"/><circle class="dim" cx="629.4" cy="192.4" r="2.4"/><circle class="dim" cx="647.7" cy="222.9" r="2.4"/><circle class="dim" cx="666.0" cy="221.2" r="2.4"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,202.8 62.3,202.7 80.6,202.4 98.9,202.4 117.2,202.2 135.5,201.8 153.8,201.9 172.1,200.9 190.4,200.1 208.6,200.1 226.9,199.3 245.2,197.7 263.5,197.8 281.8,198.2 300.1,181.6 318.4,182.5 336.7,181.6 355.0,182.1 373.3,183.0 391.6,183.4 409.9,183.0 428.2,199.9 446.5,200.4 464.8,201.3 483.1,201.4 501.4,201.8 519.6,201.3 537.9,201.2 556.2,201.0 574.5,200.1 592.8,200.7 611.1,201.4 629.4,201.8 647.7,201.8 666.0,201.3"/><polyline class="curve" style="stroke-width:2.4" points="44.0,202.4 62.3,202.4 80.6,202.5 98.9,202.4 117.2,202.1 135.5,201.7 153.8,201.3 172.1,200.8 190.4,200.3 208.6,199.8 226.9,199.3 245.2,199.0 263.5,198.9 281.8,199.0 300.1,199.2 318.4,199.3 336.7,199.5 355.0,199.7 373.3,200.0 391.6,200.3 409.9,200.6 428.2,200.7 446.5,200.8 464.8,201.0 483.1,201.1 501.4,201.1 519.6,201.1 537.9,201.0 556.2,200.9 574.5,200.9 592.8,201.0 611.1,201.2 629.4,201.2 647.7,201.3 666.0,201.3"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">ziyaret</text><line class="curve2" x1="149" y1="38" x2="167" y2="38"/><text class="ink" x="173" y="42" font-size="11">klasik trend</text><line class="curve" x1="279" y1="38" x2="297" y2="38"/><text class="ink" x="303" y="42" font-size="11">dayanıklı STL trendi</text></svg>
  <figcaption>14 Mart'taki tek günlük sıçrama klasik trendi yedi gün boyunca yukarı çekiyor. Dayanıklı STL trendi sıçramayı görmezden geliyor.</figcaption>
</figure>

Klasik trend sıçramanın etrafındaki yedi günde 800 birim yukarı kabarıyor
(14 Mart'ta 4560). Sonuç: sıçramadan **bir gün önce** kalıntı −1206. Hiçbir şey
olmayan bir gün, komşusu yüzünden olağandışı görünüyor. Dayanıklı STL'de trend
3737'de düz kalıyor ve sıçramanın tamamı (5474) kalıntıya, yani ait olduğu yere
gidiyor.

STL yalnızca toplamsal çalışır; çarpımsal seri için logaritma köprüsünü kullan.

## 8. Birden çok mevsim: MSTL

Günlük satışta iki desen var: haftalık ve yıllık. `MSTL` ikisini birden ayırır:

```python
from statsmodels.tsa.seasonal import MSTL

fit = MSTL(s, periods=(7, 365)).fit()
print(fit.seasonal.columns.tolist())     # ['seasonal_7', 'seasonal_365']
print(round(fit.resid.std(), 2))         # 5.89
```

Kalıntının standart sapması 12.32'den 5.89'a indi: yıllık dalga artık trendin
içinde saklanmıyor, kendi bileşeninde. Trend de gerçek bir yön oldu: 207'den
311'e düz bir yükseliş.

Saatlik veride tipik seçim `periods=(24, 168)`: günün saati ve haftanın günü.

Bir periyodu ayırmak için veride o periyottan **en az iki tam tur** olmalı;
üç yıllık veriyle yıllık desen ancak ayrılıyor.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `period` vermemek ya da yanlış vermek | Hata, ya da mevsim kalıntıya sızıyor | Günlük–haftalık 7, aylık–yıllık 12, saatlik–günlük 24 |
| İndekste eksik gün varken ayrıştırmak | Desen kayıyor: "7 satır" artık 7 gün değil | Önce `asfreq("D")`, eksikleri doldur (Bölüm 13) |
| Büyüyen dalgaya toplamsal model | Kalıntıda yelpaze ve desen | Çarpımsal model ya da logaritma |
| Trend bileşenini "yön" sanmak | Yıllık mevsimi büyüme diye okumak | Trend = periyottan yavaş her şey; MSTL ile ayır |
| Uçlardaki `NaN`'ı unutmak | Son günlerin trendi yok, toplamlar eksik | STL kullan ya da `dropna()` |
| Aykırı günlerle klasik yöntem | Komşu günler sahte kalıntı alıyor | `STL(..., robust=True)` |
| Kalıntıya bakmamak | Yanlış model fark edilmiyor | Kalıntıyı çiz, aya ve güne göre grupla |

## Özet

- Ayrıştırma seriyi **trend + mevsim + kalıntı** olarak üç seriye böler;
  üçünün toplamı (ya da çarpımı) seriyi geri verir.
- Klasik yöntem üç adım: ortalanmış hareketli ortalama → trendsiz serinin
  mevsim konumuna göre ortalaması → kalan.
- `seasonal_decompose(s, model=..., period=...)` bunu yapar; `.trend`,
  `.seasonal`, `.resid`.
- **Toplamsal**: dalga boyu sabit. **Çarpımsal**: dalga düzeyle büyüyor;
  mevsim bir çarpan. Logaritma çarpımsalı toplamsala çevirir.
- **Kalıntı** desensiz olmalı; desen varsa model eksik ya da yanlış.
- **Arındırılmış seri** = seri − mevsim (ya da seri / mevsim): dönemler
  arasında adil karşılaştırma.
- **STL**: uçlarda boşluk yok, mevsim zamanla değişebilir, `robust=True` ile
  aykırı değere dayanıklı. **MSTL**: birden çok periyot.

Sıradaki bölüm kalıntının ve trendin bir özelliğine bakıyor: serinin
istatistikleri zamanla değişiyor mu? Buna **durağanlık** deniyor ve ARIMA'ya
giden yolun ilk adımı.
