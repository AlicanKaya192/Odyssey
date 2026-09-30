# Üstel Düzleştirme

Bölüm 14'teki temel yöntemlerin iki ucu vardı. **Naif** yalnızca son gözleme
bakıyor: çok çevik ama her gürültüye kanıyor. **Ortalama** bütün geçmişe eşit
ağırlık veriyor: sakin ama üç yıl önceki günü dünle bir tutuyor.

Arada makul bir yol var: **bütün geçmişe bak, ama yakın olana daha çok
güven.** Üstel düzleştirme tam olarak bu. 1950'lerden beri kullanılıyor, tek
satırda kuruluyor ve gerçek tahmin yarışmalarında çok daha karmaşık yöntemlerle
başa baş gidiyor. Bu bölümde onu üç adımda kuruyorsun: önce düzey, sonra trend,
sonra mevsim.

## 1. Fikir: azalan ağırlıklar

Tahmin, geçmiş gözlemlerin **ağırlıklı ortalaması**. En yeni gözlem `α` (alfa)
kadar ağırlık alıyor; bir önceki onun `(1 − α)` katı, bir öncekinin öncesi yine
`(1 − α)` katı...

`α = 0.3` için ağırlıklar: 0.30, 0.21, 0.147, 0.103, 0.072, 0.050...

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="200.0" x2="666" y2="200.0"/><text class="dim" x="38" y="203.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="169.6" x2="666" y2="169.6"/><text class="dim" x="38" y="173.1" font-size="10.5" text-anchor="end">0.2</text><line class="grid" x1="44" y1="139.3" x2="666" y2="139.3"/><text class="dim" x="38" y="142.8" font-size="10.5" text-anchor="end">0.4</text><line class="grid" x1="44" y1="108.9" x2="666" y2="108.9"/><text class="dim" x="38" y="112.4" font-size="10.5" text-anchor="end">0.6</text><line class="grid" x1="44" y1="78.6" x2="666" y2="78.6"/><text class="dim" x="38" y="82.1" font-size="10.5" text-anchor="end">0.8</text><line class="grid" x1="44" y1="48.2" x2="666" y2="48.2"/><text class="dim" x="38" y="51.7" font-size="10.5" text-anchor="end">1</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="63.4" y1="200" x2="63.4" y2="204"/><text class="dim" x="63.4" y="216" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="160.6" y1="200" x2="160.6" y2="204"/><text class="dim" x="160.6" y="216" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="257.8" y1="200" x2="257.8" y2="204"/><text class="dim" x="257.8" y="216" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="355.0" y1="200" x2="355.0" y2="204"/><text class="dim" x="355.0" y="216" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="452.2" y1="200" x2="452.2" y2="204"/><text class="dim" x="452.2" y="216" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="549.4" y1="200" x2="549.4" y2="204"/><text class="dim" x="549.4" y="216" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="646.6" y1="200" x2="646.6" y2="204"/><text class="dim" x="646.6" y="216" font-size="10.5" text-anchor="middle">12</text><polyline class="curve2" style="stroke-width:2" points="63.4,63.4 112.0,186.3 160.6,198.6 209.2,199.9 257.8,200.0 306.4,200.0 355.0,200.0 403.6,200.0 452.2,200.0 500.8,200.0 549.4,200.0 598.0,200.0 646.6,200.0"/><circle class="dot2" cx="63.4" cy="63.4" r="3"/><circle class="dot2" cx="112.0" cy="186.3" r="3"/><circle class="dot2" cx="160.6" cy="198.6" r="3"/><circle class="dot2" cx="209.2" cy="199.9" r="3"/><circle class="dot2" cx="257.8" cy="200.0" r="3"/><circle class="dot2" cx="306.4" cy="200.0" r="3"/><circle class="dot2" cx="355.0" cy="200.0" r="3"/><circle class="dot2" cx="403.6" cy="200.0" r="3"/><circle class="dot2" cx="452.2" cy="200.0" r="3"/><circle class="dot2" cx="500.8" cy="200.0" r="3"/><circle class="dot2" cx="549.4" cy="200.0" r="3"/><circle class="dot2" cx="598.0" cy="200.0" r="3"/><circle class="dot2" cx="646.6" cy="200.0" r="3"/><polyline class="curve4" style="stroke-width:2" points="63.4,124.1 112.0,162.1 160.6,181.0 209.2,190.5 257.8,195.3 306.4,197.6 355.0,198.8 403.6,199.4 452.2,199.7 500.8,199.9 549.4,199.9 598.0,200.0 646.6,200.0"/><circle class="dot3" cx="63.4" cy="124.1" r="3"/><circle class="dot3" cx="112.0" cy="162.1" r="3"/><circle class="dot3" cx="160.6" cy="181.0" r="3"/><circle class="dot3" cx="209.2" cy="190.5" r="3"/><circle class="dot3" cx="257.8" cy="195.3" r="3"/><circle class="dot3" cx="306.4" cy="197.6" r="3"/><circle class="dot3" cx="355.0" cy="198.8" r="3"/><circle class="dot3" cx="403.6" cy="199.4" r="3"/><circle class="dot3" cx="452.2" cy="199.7" r="3"/><circle class="dot3" cx="500.8" cy="199.9" r="3"/><circle class="dot3" cx="549.4" cy="199.9" r="3"/><circle class="dot3" cx="598.0" cy="200.0" r="3"/><circle class="dot3" cx="646.6" cy="200.0" r="3"/><polyline class="curve" style="stroke-width:2" points="63.4,169.6 112.0,175.7 160.6,180.6 209.2,184.5 257.8,187.6 306.4,190.1 355.0,192.0 403.6,193.6 452.2,194.9 500.8,195.9 549.4,196.7 598.0,197.4 646.6,197.9"/><circle class="dot" cx="63.4" cy="169.6" r="3"/><circle class="dot" cx="112.0" cy="175.7" r="3"/><circle class="dot" cx="160.6" cy="180.6" r="3"/><circle class="dot" cx="209.2" cy="184.5" r="3"/><circle class="dot" cx="257.8" cy="187.6" r="3"/><circle class="dot" cx="306.4" cy="190.1" r="3"/><circle class="dot" cx="355.0" cy="192.0" r="3"/><circle class="dot" cx="403.6" cy="193.6" r="3"/><circle class="dot" cx="452.2" cy="194.9" r="3"/><circle class="dot" cx="500.8" cy="195.9" r="3"/><circle class="dot" cx="549.4" cy="196.7" r="3"/><circle class="dot" cx="598.0" cy="197.4" r="3"/><circle class="dot" cx="646.6" cy="197.9" r="3"/><line class="curve2" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">α = 0.9</text><line class="curve4" x1="149" y1="38" x2="167" y2="38"/><text class="ink" x="173" y="42" font-size="11">α = 0.5</text><line class="curve" x1="244" y1="38" x2="262" y2="38"/><text class="ink" x="268" y="42" font-size="11">α = 0.2</text></svg>
  <figcaption>Yatay eksen gözlemin kaç adım geride olduğu (0 en yeni), dikey eksen aldığı ağırlık. Büyük α'da ağırlığın neredeyse tamamı son gözlemde; küçük α'da uzun bir geçmişe yayılıyor.</figcaption>
</figure>

- `α` büyükse ağırlık son birkaç gözlemde toplanır: **çevik**, gürültüye açık.
- `α` küçükse ağırlık geniş bir geçmişe yayılır: **sakin**, değişime geç uyar.
- `α = 1` naif tahmindir; `α` sıfıra yaklaştıkça ortalamaya benzer.

## 2. Basit üstel düzleştirme

Ağırlıkları tek tek hesaplamak gerekmiyor. Aynı sonucu tek bir güncelleme
kuralı veriyor:

$$\text{yeni düzey} = \alpha \times \text{gözlem} + (1 - \alpha) \times \text{eski düzey}$$

Her yeni gözlemde düzeyi, gözleme doğru `α` kadar çek.

```python
def smooth(values, alpha):
    level = values[0]
    levels = []
    for value in values:
        level = alpha * value + (1 - alpha) * level
        levels.append(level)
    return levels
```

`α = 0.5` ile beş gün:

| Gözlem | 351 | 223 | 223 | 264 | 264 |
|---|---|---|---|---|---|
| Düzey | 351.0 | 287.0 | 255.0 | 259.5 | 261.8 |

İkinci gün gözlem 223'e düşünce düzey yarı yolda 287'ye iniyor; üçüncü gün bir
yarım adım daha. pandas'ta aynısı:

```python
levels = s.ewm(alpha=0.5, adjust=False).mean()
```

**Tahmin, son düzeyin kendisi** ve bütün ufuk için aynı: düz bir çizgi. Basit
üstel düzleştirme trendi ve mevsimi olmayan seriler için.

## 3. Alfa kaç olmalı?

Haftalık payı çıkarılmış günlük satışta (Bölüm 10'daki arındırılmış seri) bir
gün sonrasının hatası, `α`'ya göre:

| `α` | 0.05 | 0.1 | 0.2 | 0.5 | 1.0 (naif) |
|---|---|---|---|---|---|
| MAE | 12.55 | 11.46 | **11.21** | 11.83 | 13.53 |

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="180.2" x2="666" y2="180.2"/><text class="dim" x="38" y="183.7" font-size="10.5" text-anchor="end">260</text><line class="grid" x1="44" y1="139.2" x2="666" y2="139.2"/><text class="dim" x="38" y="142.7" font-size="10.5" text-anchor="end">280</text><line class="grid" x1="44" y1="98.2" x2="666" y2="98.2"/><text class="dim" x="38" y="101.7" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="57.2" x2="666" y2="57.2"/><text class="dim" x="38" y="60.7" font-size="10.5" text-anchor="end">320</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">1 Tem</text><line class="line" x1="139.7" y1="220" x2="139.7" y2="224"/><text class="dim" x="139.7" y="236" font-size="10.5" text-anchor="middle">15 Tem</text><line class="line" x1="255.9" y1="220" x2="255.9" y2="224"/><text class="dim" x="255.9" y="236" font-size="10.5" text-anchor="middle">1 Ağu</text><line class="line" x1="351.6" y1="220" x2="351.6" y2="224"/><text class="dim" x="351.6" y="236" font-size="10.5" text-anchor="middle">15 Ağu</text><line class="line" x1="467.8" y1="220" x2="467.8" y2="224"/><text class="dim" x="467.8" y="236" font-size="10.5" text-anchor="middle">1 Eyl</text><line class="line" x1="563.5" y1="220" x2="563.5" y2="224"/><text class="dim" x="563.5" y="236" font-size="10.5" text-anchor="middle">15 Eyl</text><polyline class="curve3" style="stroke-width:1.2" points="44.0,209.8 50.8,193.3 57.7,194.5 64.5,156.2 71.3,133.1 78.2,160.2 85.0,157.1 91.8,185.2 98.7,189.2 105.5,184.2 112.4,131.6 119.2,172.0 126.0,164.3 132.9,148.9 139.7,166.8 146.5,140.0 153.4,165.7 160.2,156.2 167.0,153.6 173.9,166.3 180.7,165.3 187.5,150.3 194.4,156.4 201.2,173.9 208.0,158.3 214.9,102.3 221.7,149.9 228.5,167.3 235.4,150.3 242.2,117.4 249.1,159.6 255.9,158.3 262.7,161.8 269.6,168.4 276.4,144.8 283.2,129.8 290.1,140.0 296.9,147.3 303.7,185.0 310.6,153.6 317.4,154.0 324.2,196.1 331.1,162.6 337.9,129.7 344.7,165.7 351.6,158.3 358.4,98.2 365.3,104.8 372.1,97.6 378.9,113.4 385.8,121.5 392.6,137.0 399.4,121.4 406.3,96.1 413.1,102.7 419.9,114.0 426.8,131.9 433.6,109.2 440.4,141.1 447.3,86.5 454.1,98.2 460.9,113.0 467.8,68.9 474.6,168.8 481.5,174.8 488.3,108.3 495.1,133.7 502.0,126.9 508.8,76.1 515.6,75.0 522.5,72.4 529.3,105.1 536.1,130.9 543.0,96.8 549.8,110.5 556.6,88.4 563.5,64.8 570.3,86.8 577.1,150.2 584.0,83.7 590.8,98.8 597.6,81.8 604.5,88.4 611.3,103.8 618.2,119.6 625.0,88.7 631.8,104.2 638.7,102.9 645.5,65.4 652.3,74.0 659.2,114.0 666.0,90.9"/><polyline class="curve2" style="stroke-width:1.8" points="44.0,203.9 50.8,194.4 57.7,194.4 64.5,160.1 71.3,135.8 78.2,157.7 85.0,157.1 91.8,182.4 98.7,188.5 105.5,184.6 112.4,136.9 119.2,168.5 126.0,164.7 132.9,150.5 139.7,165.1 146.5,142.5 153.4,163.4 160.2,157.0 167.0,153.9 173.9,165.1 180.7,165.3 187.5,151.8 194.4,155.9 201.2,172.1 208.0,159.7 214.9,108.0 221.7,145.7 228.5,165.2 235.4,151.8 242.2,120.9 249.1,155.7 255.9,158.0 262.7,161.4 269.6,167.7 276.4,147.1 283.2,131.6 290.1,139.1 296.9,146.5 303.7,181.1 310.6,156.3 317.4,154.2 324.2,191.9 331.1,165.6 337.9,133.3 344.7,162.5 351.6,158.7 358.4,104.2 365.3,104.7 372.1,98.3 378.9,111.9 385.8,120.6 392.6,135.4 399.4,122.8 406.3,98.8 413.1,102.3 419.9,112.8 426.8,130.0 433.6,111.3 440.4,138.1 447.3,91.7 454.1,97.5 460.9,111.4 467.8,73.1 474.6,159.2 481.5,173.3 488.3,114.8 495.1,131.8 502.0,127.4 508.8,81.2 515.6,75.7 522.5,72.7 529.3,101.9 536.1,128.0 543.0,99.9 549.8,109.4 556.6,90.5 563.5,67.4 570.3,84.8 577.1,143.7 584.0,89.7 590.8,97.9 597.6,83.4 604.5,87.9 611.3,102.2 618.2,117.8 625.0,91.6 631.8,103.0 638.7,102.9 645.5,69.1 652.3,73.5 659.2,110.0 666.0,92.8"/><polyline class="curve" style="stroke-width:2.4" points="44.0,178.7 50.8,181.6 57.7,184.2 64.5,178.6 71.3,169.5 78.2,167.6 85.0,165.5 91.8,169.5 98.7,173.4 105.5,175.6 112.4,166.8 119.2,167.8 126.0,167.1 132.9,163.5 139.7,164.1 146.5,159.3 153.4,160.6 160.2,159.7 167.0,158.5 173.9,160.0 180.7,161.1 187.5,158.9 194.4,158.4 201.2,161.5 208.0,160.9 214.9,149.2 221.7,149.3 228.5,152.9 235.4,152.4 242.2,145.4 249.1,148.2 255.9,150.3 262.7,152.6 269.6,155.7 276.4,153.5 283.2,148.8 290.1,147.0 296.9,147.1 303.7,154.7 310.6,154.4 317.4,154.3 324.2,162.7 331.1,162.7 337.9,156.1 344.7,158.0 351.6,158.1 358.4,146.1 365.3,137.8 372.1,129.8 378.9,126.5 385.8,125.5 392.6,127.8 399.4,126.5 406.3,120.4 413.1,116.9 419.9,116.3 426.8,119.4 433.6,117.4 440.4,122.1 447.3,115.0 454.1,111.6 460.9,111.9 467.8,103.3 474.6,116.4 481.5,128.1 488.3,124.1 495.1,126.0 502.0,126.2 508.8,116.2 515.6,108.0 522.5,100.8 529.3,101.7 536.1,107.5 543.0,105.4 549.8,106.4 556.6,102.8 563.5,95.2 570.3,93.5 577.1,104.9 584.0,100.6 590.8,100.3 597.6,96.6 604.5,94.9 611.3,96.7 618.2,101.3 625.0,98.8 631.8,99.8 638.7,100.5 645.5,93.4 652.3,89.6 659.2,94.4 666.0,93.7"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">arındırılmış satış</text><line class="curve2" x1="226" y1="38" x2="244" y2="38"/><text class="ink" x="250" y="42" font-size="11">düzey, α = 0.9</text><line class="curve" x1="370" y1="38" x2="388" y2="38"/><text class="ink" x="394" y="42" font-size="11">düzey, α = 0.2</text></svg>
  <figcaption>α = 0.9 her zikzağı izliyor: gürültüyü de tahmin sayıyor. α = 0.2 gürültüyü süzüp yavaş değişen düzeyi bırakıyor.</figcaption>
</figure>

En iyi değer 0.2 civarında ve naiften %17 iyi: bu seride günlük oynamanın çoğu
gürültü, düzey yavaş değişiyor. Çok küçük `α` (0.05) ise düzeyin gerçek
hareketini kaçırıyor.

Elle aramaya gerek yok; statsmodels `α`'yı eğitim verisindeki bir adımlık
hatayı en küçük yapacak biçimde kendisi buluyor:

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

fit = ExponentialSmoothing(train).fit()
print(round(fit.params["smoothing_level"], 3))     # 0.186
forecast = fit.forecast(28)
```

Bulunan `α` seri hakkında bir teşhis de veriyor. Hisse fiyatında sonuç **1.0**:
model "son değerden başka hiçbir şeye güvenme" diyor. Rastgele yürüyüşün
(Bölüm 11) en iyi tahmini naif; üstel düzleştirme bunu kendiliğinden buldu.

## 4. Trend: Holt yöntemi

Trendli seride düz çizgi hep geride kalır. Holt yöntemi ikinci bir sayı daha
izliyor: **eğim**. Düzey için `α`, eğim için `β` (beta) ayrı ayrı güncelleniyor
ve tahmin bir doğru oluyor:

$$\text{tahmin}_h = \text{düzey} + h \times \text{eğim}$$

Yıllık yolcu toplamında (2013–2022 eğitim, 2023–2024 test):

```python
fit = ExponentialSmoothing(train, trend="add").fit()
```

| Model | 2023 | 2024 | MAE |
|---|---|---|---|
| Gerçek | 4195 | 4680 | |
| Trendsiz | 3816 | 3816 | 621.5 |
| Toplamsal trend (`trend="add"`) | 4071 | 4326 | 239.3 |
| Çarpımsal trend (`trend="mul"`) | 4233 | 4690 | 23.5 |

Toplamsal trend her yıl **sabit bir miktar** ekliyor; çarpımsal trend **sabit
bir oranla** büyütüyor. Yolcu sayısı yılda %10 büyüdüğü için (Bölüm 11)
çarpımsal olan on kat isabetli.

**Sönümlü trend.** Doğrusal trend sonsuza kadar aynı eğimle gider; uzun ufukta
bu çoğu zaman fazla iyimserdir. `damped_trend=True` eğimi her adımda biraz
küçültür (`φ` katsayısıyla) ve tahmin zamanla yataya döner. Uzun ufuklu
tahminlerde güvenli seçim.

## 5. Mevsim: Holt–Winters

Üçüncü bileşen mevsim. Model artık üç şeyi birden izliyor ve her birinin kendi
katsayısı var:

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Düzey · α</span><span>Serinin mevsimden arındırılmış güncel seviyesi.</span></div>
<div class="anat-row"><span>Eğim · β</span><span>Düzeyin adım başına değişimi. İsteğe bağlı.</span></div>
<div class="anat-row"><span>Mevsim · γ</span><span>Mevsimin her konumu için bir pay (haftanın 7 günü, yılın 12 ayı).</span></div>
</div>
<figcaption>Bölüm 10'daki ayrıştırmanın aynısı, ama bileşenler her yeni gözlemle <b>güncelleniyor</b> ve ileriye taşınabiliyor.</figcaption>
</figure>

Günlük satışta (eğitim 5 Kasım 2024'e kadar), trendsiz ve toplamsal mevsimli
model:

```python
fit = ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()

print(round(fit.level.iloc[-1], 1))                 # 314.0
print(fit.season.iloc[-7:].round(1).tolist())
# [-23.2, -11.1, 35.3, 96.0, 48.3, -39.3, -41.3]   (carsamba ... sali)
```

Tahmin bu iki parçanın toplamı: ilk cumartesi için 314.0 + 96.0 = **410.0**,
ilk salı için 314.0 − 41.3 = 272.7.

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.9" x2="666" y2="210.9"/><text class="dim" x="38" y="214.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="175.7" x2="666" y2="175.7"/><text class="dim" x="38" y="179.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="140.5" x2="666" y2="140.5"/><text class="dim" x="38" y="144.0" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="105.3" x2="666" y2="105.3"/><text class="dim" x="38" y="108.8" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="70.1" x2="666" y2="70.1"/><text class="dim" x="38" y="73.6" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="34.9" x2="666" y2="34.9"/><text class="dim" x="38" y="38.4" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">9 Eki</text><line class="line" x1="202.3" y1="230" x2="202.3" y2="234"/><text class="dim" x="202.3" y="246" font-size="10.5" text-anchor="middle">23 Eki</text><line class="line" x1="360.7" y1="230" x2="360.7" y2="234"/><text class="dim" x="360.7" y="246" font-size="10.5" text-anchor="middle">6 Kas</text><line class="line" x1="519.0" y1="230" x2="519.0" y2="234"/><text class="dim" x="519.0" y="246" font-size="10.5" text-anchor="middle">20 Kas</text><rect class="box" x="355.0" y="32" width="311.0" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,207.4 55.3,184.2 66.6,144.7 77.9,110.2 89.2,132.8 100.5,208.1 111.9,212.3 123.2,180.7 134.5,176.4 145.8,148.3 157.1,102.5 168.4,145.4 179.7,193.3 191.0,201.1 202.3,175.0 213.6,183.5 224.9,149.7 236.3,94.7 247.6,130.6 258.9,195.4 270.2,194.0 281.5,185.6 292.8,180.0 304.1,132.8 315.4,89.8 326.7,127.8 338.0,195.4 349.3,199.0 360.7,187.7 372.0,171.5 383.3,139.8 394.6,74.3 405.9,123.6 417.2,191.9 428.5,197.6 439.8,173.6 451.1,173.6 462.4,124.3 473.7,99.0 485.1,110.2 496.4,194.7 507.7,189.8 519.0,189.8 530.3,165.2 541.6,128.5 552.9,93.3 564.2,117.3 575.5,197.6 586.8,184.9 598.1,177.8 609.5,177.8 620.8,150.4 632.1,82.8 643.4,110.2 654.7,197.6 666.0,182.8"/><polyline class="curve" style="stroke-width:2.4" points="360.7,182.2 372.0,173.7 383.3,141.0 394.6,98.3 405.9,131.9 417.2,193.5 428.5,194.2 439.8,182.2 451.1,173.7 462.4,141.0 473.7,98.3 485.1,131.9 496.4,193.5 507.7,194.2 519.0,182.2 530.3,173.7 541.6,141.0 552.9,98.3 564.2,131.9 575.5,193.5 586.8,194.2 598.1,182.2 609.5,173.7 620.8,141.0 632.1,98.3 643.4,131.9 654.7,193.5 666.0,194.2"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">Holt–Winters tahmini</text></svg>
  <figcaption>Gölgeli bölge 28 günlük test. Tahmin her hafta aynı yedi sayı: düzey (314) artı o günün mevsim payı. Trend bileşeni olmadığı için Kasım sonundaki yükselişi izleyemiyor.</figcaption>
</figure>

Mevsimsel naiften farkı ne? Mevsimsel naif **tek bir haftayı** kopyalıyor; o
haftanın sürprizleri de tahmine geçiyor. Holt–Winters haftalık payları bütün
geçmişten, yakın haftalara daha çok ağırlık vererek öğreniyor.

## 6. Toplamsal mı, çarpımsal mı?

Bölüm 10'daki karar burada da geçerli: dalgalar düzeyle birlikte büyüyorsa
çarpımsal. Aylık yolcu serisinde 2024 tahmini:

| Model | MAE | Yüzde hata |
|---|---|---|
| Mevsimsel naif × büyüme (Bölüm 14'ün çıtası) | 11.11 | %2.8 |
| Toplamsal trend + toplamsal mevsim | 9.90 | %2.4 |
| Toplamsal trend + çarpımsal mevsim | 8.61 | %2.2 |
| Çarpımsal trend + çarpımsal mevsim | **6.53** | %1.7 |

```python
fit = ExponentialSmoothing(
    train, trend="mul", seasonal="mul", seasonal_periods=12
).fit()
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Oca 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Tem 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Oca 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Tem 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Oca 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Tem 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve2" style="stroke-width:2.2" points="470.5,174.7 488.3,182.6 506.1,156.3 523.8,153.9 541.6,141.5 559.4,110.8 577.1,91.0 594.9,79.6 612.7,126.8 630.5,140.3 648.2,167.8 666.0,145.4"/><polyline class="curve" style="stroke-width:2.2" points="470.5,176.7 488.3,183.8 506.1,156.1 523.8,149.9 541.6,137.2 559.4,107.0 577.1,76.1 594.9,69.4 612.7,117.7 630.5,140.2 648.2,164.3 666.0,142.6"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve2" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">toplamsal</text><line class="curve" x1="251" y1="40" x2="269" y2="40"/><text class="ink" x="275" y="44" font-size="11">çarpımsal</text></svg>
  <figcaption>2024'ün tahmini. İki model de deseni yakalıyor; çarpımsal olan yaz tepesinin boyunu da tutturuyor, çünkü mevsimi düzeyle birlikte büyütüyor.</figcaption>
</figure>

Serinin yapısına uyan model (yüzdeyle büyüme, orantılı mevsim) çıtayı %41
aşıyor. Çarpımsal bileşenler yalnızca **hep artı** değerli serilerde çalışır.

## 7. Katsayıları okumak

Bulunan katsayılar, serinin ne kadar "oynak" olduğunu söyler:

| Katsayı | Küçük (0'a yakın) | Büyük (1'e yakın) |
|---|---|---|
| `α` (düzey) | Düzey kararlı; günlük oynama gürültü | Düzey sürekli kayıyor; son değer önemli |
| `β` (eğim) | Eğim sabit | Eğim sık değişiyor |
| `γ` (mevsim) | Desen yıldan yıla aynı | Desen evriliyor |

Yolcu modelinde üçü de **0.00**: model başlangıçta bulduğu büyüme oranını
(ayda %0.85) ve on iki ay çarpanını hiç değiştirmiyor. Bu "model öğrenmedi"
demek değil; "desen o kadar kararlı ki güncellemeye gerek yok" demek.

Günlük satışta `α = 0.18`, `γ = 0.13`: düzey de haftalık paylar da yavaş yavaş
güncelleniyor.

`α` 1'e çok yakın çıkarsa model aslında naif tahmine dönmüştür; düzleştirecek
bir şey bulamamıştır.

## 8. Sınama: çıtayı geçiyor mu?

Bölüm 15'in düzeneği: 13 başlangıç, 28 günlük ufuk.

| Yöntem | Ortalama MAE | En kötü deney | Mevsimsel naifi geçtiği deney |
|---|---|---|---|
| Mevsimsel naif | 17.95 | 41.3 | |
| Holt–Winters, trendsiz + toplamsal mevsim | **15.91** | 38.6 | 12 / 13 |
| Toplamsal trend + toplamsal mevsim | 16.81 | 51.3 | 12 / 13 |
| Toplamsal trend + çarpımsal mevsim | 15.45 | 46.9 | 11 / 13 |

Üç şey görülüyor:

**Kazanç gerçek ama mütevazı.** Trendsiz model 13 deneyin 12'sinde önde; fark
ortalama 2.0, deneyler arası oynaklığı 1.9. Bölüm 15'teki "berabere"den farklı:
burada fark **tutarlı**. Beceri 1 − 15.91 / 17.95 = 0.11.

**Tek ayrım bunu göstermezdi.** 5 Kasım ayrımında MAE 11.73 ve 11.64: neredeyse
aynı. Fark ancak çok deneyle ortaya çıktı.

**Trend eklemek riski artırıyor.** Trendli modellerin en kötü deneyi 47–51;
trendsizin 38.6. Trend, yıl sonundaki yükselişi 28 gün ileriye uzatıp Ocak'ta
büyük ıskalıyor. Ortalama hata benzer, **en kötü durum** farklı. Seçerken
ikisine birden bak.

## 9. Sınırları

- **Tek mevsim.** `seasonal_periods` tek bir sayı. Günlük veride haftalık
  deseni alırsın; yıllık deseni alamazsın.
- **Uzun mevsim zor.** Her konum için ayrı bir pay öğreniyor; `365` konumlu bir
  mevsim için üç yıllık veri yetmez.
- **Takvimi bilmez.** Bayram, kampanya, tatil: en kötü deney hâlâ yıl dönümünde.
- **Dış bilgi alamaz.** Fiyat, hava durumu gibi değişkenler modele giremez.

Bölüm 17 (ARIMA) kısa dönem hafızayı, Bölüm 18 takvimi ve dış değişkenleri
ekliyor.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Mevsimli seride `seasonal` vermemek | Düz ya da doğrusal tahmin; desen yok | `seasonal="add"` / `"mul"` ve `seasonal_periods` |
| `seasonal_periods`'u yanlış vermek | Desen kayıyor | Satır sayısıyla: günlük–haftalık 7, aylık–yıllık 12 |
| Sıfır ya da eksi değerli seride çarpımsal bileşen | Hata | Toplamsal, ya da önce dönüştür |
| Eksik günleri olan indeks | Mevsim konumları kayıyor | `asfreq`, sonra doldur (Bölüm 13) |
| Uzun ufukta sönümsüz trend | Gerçekçi olmayan büyüme | `damped_trend=True` |
| Eğitim uyumuna bakıp model seçmek | Karmaşık model hep "kazanır" | Örnek dışı hata, kayan başlangıç |
| Yalnızca ortalama hataya bakmak | En kötü durum gizlenir | En kötü deneye de bak |
| Temel yöntemle karşılaştırmamak | Kazancın boyu bilinmez | Aynı düzenekte mevsimsel naif |

## Özet

- Üstel düzleştirme geçmişin **ağırlıklı ortalaması**; ağırlıklar geriye doğru
  üstel azalır. Hızı `α` belirler.
- **Basit** sürüm yalnızca düzeyi izler; tahmini düz çizgi. `α = 1` naif.
- **Holt** eğimi ekler; toplamsal trend sabit miktar, çarpımsal trend sabit
  oran. **Sönümlü** trend uzun ufukta güvenli.
- **Holt–Winters** mevsimi ekler; dalgalar düzeyle büyüyorsa çarpımsal.
- `ExponentialSmoothing(train, trend=..., seasonal=..., seasonal_periods=m)
  .fit()`; katsayılar `fit.params`, tahmin `fit.forecast(h)`.
- Katsayılar teşhis verir: 0'a yakın kararlı, 1'e yakın oynak.
- Günlük satışta mevsimsel naifi 13 deneyin 12'sinde geçiyor; kazanç %11.
  Yolcu serisinde çıtayı %41 aşıyor.

Üstel düzleştirme seriyi bileşenleriyle anlatıyor. Sıradaki model başka bir
yoldan gidiyor: serinin **hafızasını** (Bölüm 12) doğrudan modelliyor. ARIMA.
