# İkinci Dereceden Denklemler

Bilinmeyenin karesi girince ($x^2$) denklem değişiyor: artık iki çözüm
olabilir, tek çözüm olabilir ya da hiç gerçek çözüm olmayabilir. Alan
hesapları, fırlatılan bir cismin yolu ve kâr–zarar hesapları ikinci
dereceden denklemlere varıyor. Makine öğrenmesinde de kare hata, ağırlığın
ikinci dereceden bir fonksiyonu: en iyi ağırlığı bulmak bir parabolün
dibini bulmak demek. Bu bölümde dört çözüm yolunu ve diskriminantı
göreceğiz.

Ön bilgi: Çarpanlara Ayırma, Köklü Sayılar.

## Standart biçim

$$
ax^2 + bx + c = 0, \qquad a \neq 0
$$

$a = 0$ olsaydı $x^2$ kaybolur, denklem birinci dereceden olurdu. Çözmeye
başlamadan önce her şeyi bir tarafa topla, öbür taraf **sıfır** olsun.

## Yol 1: Karekök almak

$b = 0$ ise ($x^2 = k$ biçimi) karekök al; **iki işareti de** unutma:

$$
x^2 = 49 \quad\Rightarrow\quad x = 7 \text{ ya da } x = -7
$$

Aynı fikir bir tam karenin eşit olduğu durumda da işler:

$$
(x - 3)^2 = 16 \quad\Rightarrow\quad x - 3 = \pm 4 \quad\Rightarrow\quad x = 7 \text{ ya da } x = -1
$$

## Yol 2: Çarpanlara ayırmak

Çarpım sıfırsa çarpanlardan biri sıfır. İfadeyi çarpanlarına ayır, her
çarpanı sıfıra eşitle:

$$
\begin{aligned}
x^2 - 5x + 6 &= 0 \\
(x - 2)(x - 3) &= 0 \\
x = 2 \;\text{ ya da }\; x &= 3
\end{aligned}
$$

**Sağ taraf sıfır olmalı.** $(x - 1)(x - 2) = 6$'dan "$x - 1 = 6$ ya da $x -
2 = 6$" sonucu çıkmaz. Önce aç, sıfıra topla: $x^2 - 3x - 4 = 0$, $(x -
4)(x + 1) = 0$.

## Yol 3: Kareyi tamamlamak

Çarpanlara kolay ayrılmayan denklemlerde $x^2 + bx$'i bir tam kareye
tamamlarız.

<figure class="fig">
<svg viewBox="0 0 490 300" width="490"><rect class="dot" opacity="0.35" x="150" y="40" width="120" height="120"/><rect class="curve3" x="150" y="40" width="120" height="120"/><text class="ink" x="210.0" y="105.0" font-size="16" text-anchor="middle">x²</text><rect class="dot2" opacity="0.35" x="270" y="40" width="66" height="120"/><rect class="curve3" x="270" y="40" width="66" height="120"/><text class="ink" x="303.0" y="105.0" font-size="14" text-anchor="middle">3x</text><rect class="dot2" opacity="0.35" x="150" y="160" width="120" height="66"/><rect class="curve3" x="150" y="160" width="120" height="66"/><text class="ink" x="210.0" y="198.0" font-size="14" text-anchor="middle">3x</text><rect class="dot3" opacity="0.35" x="270" y="160" width="66" height="66"/><rect class="curve3" stroke-dasharray="5 4" x="270" y="160" width="66" height="66"/><text class="ink" x="303.0" y="198.0" font-size="14" text-anchor="middle">9</text><text class="ink" x="210.0" y="30" font-size="14" text-anchor="middle">x</text><text class="ink" x="303.0" y="30" font-size="14" text-anchor="middle">3</text><text class="ink" x="138" y="105.0" font-size="14" text-anchor="middle">x</text><text class="ink" x="138" y="198.0" font-size="14" text-anchor="middle">3</text><text class="dim" x="243.0" y="252" font-size="11" text-anchor="middle">x² + 6x = x² + 3x + 3x</text><text class="dim" x="243.0" y="268" font-size="11" text-anchor="middle">eksik köşe: 3 · 3 = 9</text><text class="ink" x="243.0" y="288" font-size="13" text-anchor="middle">x² + 6x + 9 = (x + 3)²</text></svg>
  <figcaption>$x^2 + 6x$: bir $x^2$ karesi ve iki tane $3x$ şeridi. Köşeye $3 \cdot 3 = 9$'luk kareyi eklersek kenarı $x + 3$ olan bir kare tamamlanır. Kural: $x$'in katsayısının yarısının karesini ekle.</figcaption>
</figure>

$$
\begin{aligned}
x^2 + 6x - 7 &= 0 \\
x^2 + 6x &= 7 \\
x^2 + 6x + 9 &= 16 &&\text{(iki tarafa } 9 \text{ ekle)} \\
(x + 3)^2 &= 16 \\
x + 3 &= \pm 4 \\
x = 1 \;\text{ ya da }\; x &= -7
\end{aligned}
$$

## Yol 4: Kök formülü

Kareyi tamamlamayı genel $ax^2 + bx + c = 0$ için bir kez yapınca her
denklemde kullanılabilecek formül çıkıyor:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

**Örnek:** $2x^2 - 3x - 5 = 0$. $a = 2$, $b = -3$, $c = -5$.

$$
\begin{aligned}
b^2 - 4ac &= 9 + 40 = 49 \\
x &= \frac{3 \pm 7}{4} \\
x = \frac{10}{4} = \frac{5}{2} \;&\text{ ya da }\; x = \frac{-4}{4} = -1
\end{aligned}
$$

Dikkat edilecekler: $-b$ ($b$ negatifse pozitif olur), kesir çizgisi **hem**
$-b$'nin **hem** kökün altında, payda $2a$.

## Diskriminant: kaç kök var?

Kökün içindeki $\Delta = b^2 - 4ac$ sayısına **diskriminant** denir. Karekökü
alınacağı için işareti her şeyi söyler.

<figure class="fig">
<svg viewBox="0 0 500 202" width="500"><line class="line" x1="20.0" y1="116.2" x2="150.0" y2="116.2"/><polyline class="curve" fill="none" points="20.0,55.0 21.1,58.4 22.2,61.8 23.3,65.1 24.3,68.4 25.4,71.6 26.5,74.8 27.6,77.9 28.7,80.9 29.8,83.9 30.8,86.8 31.9,89.7 33.0,92.5 34.1,95.3 35.2,98.0 36.2,100.6 37.3,103.2 38.4,105.7 39.5,108.2 40.6,110.6 41.7,112.9 42.8,115.2 43.8,117.4 44.9,119.6 46.0,121.7 47.1,123.8 48.2,125.8 49.2,127.7 50.3,129.6 51.4,131.4 52.5,133.2 53.6,134.9 54.7,136.5 55.8,138.1 56.8,139.7 57.9,141.1 59.0,142.6 60.1,143.9 61.2,145.2 62.2,146.5 63.3,147.6 64.4,148.8 65.5,149.8 66.6,150.9 67.7,151.8 68.8,152.7 69.8,153.6 70.9,154.3 72.0,155.1 73.1,155.7 74.2,156.3 75.2,156.9 76.3,157.4 77.4,157.8 78.5,158.2 79.6,158.5 80.7,158.8 81.8,159.0 82.8,159.1 83.9,159.2 85.0,159.2 86.1,159.2 87.2,159.1 88.2,159.0 89.3,158.8 90.4,158.5 91.5,158.2 92.6,157.8 93.7,157.4 94.8,156.9 95.8,156.3 96.9,155.7 98.0,155.1 99.1,154.3 100.2,153.6 101.2,152.7 102.3,151.8 103.4,150.9 104.5,149.8 105.6,148.8 106.7,147.6 107.8,146.5 108.8,145.2 109.9,143.9 111.0,142.6 112.1,141.1 113.2,139.7 114.2,138.1 115.3,136.5 116.4,134.9 117.5,133.2 118.6,131.4 119.7,129.6 120.8,127.7 121.8,125.8 122.9,123.8 124.0,121.7 125.1,119.6 126.2,117.4 127.3,115.2 128.3,112.9 129.4,110.6 130.5,108.2 131.6,105.7 132.7,103.2 133.8,100.6 134.8,98.0 135.9,95.3 137.0,92.5 138.1,89.7 139.2,86.8 140.2,83.9 141.3,80.9 142.4,77.9 143.5,74.8 144.6,71.6 145.7,68.4 146.8,65.1 147.8,61.8 148.9,58.4 150.0,55.0"/><circle class="dot2" cx="43.2" cy="116.2" r="5"/><circle class="dot2" cx="126.8" cy="116.2" r="5"/><text class="ink" x="85.0" y="20" font-size="13" text-anchor="middle">Δ > 0</text><text class="dim" x="85.0" y="190" font-size="11" text-anchor="middle">iki kök</text><line class="line" x1="180.0" y1="116.2" x2="310.0" y2="116.2"/><polyline class="curve" fill="none" points="186.5,31.7 187.6,34.8 188.7,37.9 189.8,40.8 190.8,43.8 191.9,46.6 193.0,49.4 194.1,52.2 195.2,54.9 196.2,57.5 197.3,60.1 198.4,62.6 199.5,65.1 200.6,67.5 201.7,69.8 202.8,72.1 203.8,74.3 204.9,76.5 206.0,78.6 207.1,80.7 208.2,82.7 209.2,84.6 210.3,86.5 211.4,88.3 212.5,90.1 213.6,91.8 214.7,93.5 215.8,95.0 216.8,96.6 217.9,98.1 219.0,99.5 220.1,100.8 221.2,102.1 222.2,103.4 223.3,104.6 224.4,105.7 225.5,106.8 226.6,107.8 227.7,108.7 228.8,109.6 229.8,110.5 230.9,111.3 232.0,112.0 233.1,112.7 234.2,113.3 235.2,113.8 236.3,114.3 237.4,114.7 238.5,115.1 239.6,115.4 240.7,115.7 241.8,115.9 242.8,116.0 243.9,116.1 245.0,116.2 246.1,116.1 247.2,116.0 248.2,115.9 249.3,115.7 250.4,115.4 251.5,115.1 252.6,114.7 253.7,114.3 254.8,113.8 255.8,113.3 256.9,112.7 258.0,112.0 259.1,111.3 260.2,110.5 261.2,109.6 262.3,108.7 263.4,107.8 264.5,106.8 265.6,105.7 266.7,104.6 267.8,103.4 268.8,102.1 269.9,100.8 271.0,99.5 272.1,98.1 273.2,96.6 274.2,95.0 275.3,93.5 276.4,91.8 277.5,90.1 278.6,88.3 279.7,86.5 280.8,84.6 281.8,82.7 282.9,80.7 284.0,78.6 285.1,76.5 286.2,74.3 287.2,72.1 288.3,69.8 289.4,67.5 290.5,65.1 291.6,62.6 292.7,60.1 293.8,57.5 294.8,54.9 295.9,52.2 297.0,49.4 298.1,46.6 299.2,43.8 300.2,40.8 301.3,37.9 302.4,34.8 303.5,31.7"/><circle class="dot2" cx="245.0" cy="116.2" r="5"/><text class="ink" x="245.0" y="20" font-size="13" text-anchor="middle">Δ = 0</text><text class="dim" x="245.0" y="190" font-size="11" text-anchor="middle">tek kök</text><line class="line" x1="340.0" y1="116.2" x2="470.0" y2="116.2"/><polyline class="curve" fill="none" points="356.2,31.7 357.3,34.2 358.4,36.8 359.5,39.2 360.6,41.6 361.7,44.0 362.8,46.3 363.8,48.5 364.9,50.7 366.0,52.8 367.1,54.8 368.2,56.8 369.2,58.8 370.3,60.7 371.4,62.5 372.5,64.2 373.6,66.0 374.7,67.6 375.8,69.2 376.8,70.7 377.9,72.2 379.0,73.6 380.1,75.0 381.2,76.3 382.2,77.5 383.3,78.7 384.4,79.9 385.5,80.9 386.6,81.9 387.7,82.9 388.8,83.8 389.8,84.6 390.9,85.4 392.0,86.1 393.1,86.8 394.2,87.4 395.2,88.0 396.3,88.5 397.4,88.9 398.5,89.3 399.6,89.6 400.7,89.8 401.8,90.0 402.8,90.2 403.9,90.3 405.0,90.3 406.1,90.3 407.2,90.2 408.2,90.0 409.3,89.8 410.4,89.6 411.5,89.3 412.6,88.9 413.7,88.5 414.8,88.0 415.8,87.4 416.9,86.8 418.0,86.1 419.1,85.4 420.2,84.6 421.2,83.8 422.3,82.9 423.4,81.9 424.5,80.9 425.6,79.9 426.7,78.7 427.8,77.5 428.8,76.3 429.9,75.0 431.0,73.6 432.1,72.2 433.2,70.7 434.2,69.2 435.3,67.6 436.4,66.0 437.5,64.2 438.6,62.5 439.7,60.7 440.8,58.8 441.8,56.8 442.9,54.8 444.0,52.8 445.1,50.7 446.2,48.5 447.2,46.3 448.3,44.0 449.4,41.6 450.5,39.2 451.6,36.8 452.7,34.2 453.8,31.7"/><text class="ink" x="405.0" y="20" font-size="13" text-anchor="middle">Δ < 0</text><text class="dim" x="405.0" y="190" font-size="11" text-anchor="middle">gerçek kök yok</text></svg>
  <figcaption>$y = ax^2 + bx + c$ parabolü $x$ eksenini $\Delta > 0$ ise iki yerde keser, $\Delta = 0$ ise tek noktada değer, $\Delta < 0$ ise hiç değmez. Denklemin kökleri, parabolün $x$ eksenini kestiği yerler.</figcaption>
</figure>

| $\Delta$ | Kök sayısı | Örnek |
|---|---|---|
| $\Delta > 0$ | iki farklı gerçek kök | $x^2 - 5x + 6$: $\Delta = 1$ |
| $\Delta = 0$ | tek (çift) kök, $x = -\dfrac{b}{2a}$ | $x^2 - 6x + 9$: $\Delta = 0$ |
| $\Delta < 0$ | gerçek kök yok | $x^2 + x + 1$: $\Delta = -3$ |

## Kökler ve katsayılar

İki kök $x_1$ ve $x_2$ ise

$$
x_1 + x_2 = -\frac{b}{a}, \qquad x_1 \cdot x_2 = \frac{c}{a}
$$

$x^2 - 5x + 6 = 0$ için kökler $2$ ve $3$: toplam $5$, çarpım $6$ ✓. Bu
bağ, bulduğun kökleri sınamanın hızlı yolu.

## Parabolün tepesi

$y = ax^2 + bx + c$'nin grafiği bir **parabol**; $a > 0$ ise yukarı açılır
ve en alt noktası (tepesi) vardır. Tepe, iki kökün tam ortasında:

$$
x_{\text{tepe}} = -\frac{b}{2a}
$$

Kök yoksa bile tepe vardır: $x^2 + x + 1$'in tepesi $x = -\tfrac{1}{2}$'de,
değeri $\tfrac{3}{4}$; parabol hep $x$ ekseninin üstünde.

## Makine öğrenmesinde ikinci derece

Cebirsel İfadeler bölümünde tek bir örnek için kare hatayı açmıştık:
$E(w) = (7 - 2w)^2 = 4w^2 - 28w + 49$. Bu, $w$'ye göre yukarı açılan bir
parabol. En küçük hata tepede:

$$
w = -\frac{-28}{2 \cdot 4} = 3{,}5
$$

$\Delta = 784 - 4 \cdot 4 \cdot 49 = 0$: parabol $x$ eksenine tek noktada
değiyor, yani en küçük hata tam $0$. Birden fazla örnek olunca kareler
toplanır, yine bir parabol çıkar ama dibi genelde sıfırın üstündedir:
bütün noktalardan geçen doğru yoktur. Doğrusal regresyon, bu parabolün
dibini bulmak demek.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$x^2 = 9 \Rightarrow x = 3$</p>
      <p>$x^2 = 5x \Rightarrow x = 5$</p>
      <p>$x = -b \pm \dfrac{\sqrt{\Delta}}{2a}$</p>
      <p>$(x - 1)(x - 2) = 6 \Rightarrow x = 7$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$x = 3$ ya da $x = -3$</p>
      <p>$x(x - 5) = 0$: $x = 0$ ya da $x = 5$</p>
      <p>$x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$</p>
      <p>Önce sağı sıfır yap: $x = 4$ ya da $x = -1$</p>
    </div>
  </div>
  <figcaption>Karekök iki işaret verir, $x$'e bölmek bir kökü kaybettirir, çarpım sıfıra eşit olmalı.</figcaption>
</figure>

- **$x$'e bölmek.** $x^2 = 5x$'i $x$'e bölmek $x = 0$ kökünü siler; bunun
  yerine $x$'i ortak çarpan olarak çıkar.
- **$b$'nin işaretini karıştırmak.** $b = -3$ ise $-b = 3$ ve $b^2 = 9$
  (hiçbir zaman $-9$ değil).

## Özet

- Standart biçim $ax^2 + bx + c = 0$ ($a \neq 0$); önce sağ tarafı sıfır yap.
- $x^2 = k$: $x = \pm\sqrt{k}$ ($k \ge 0$).
- Çarpanlara ayır ve her çarpanı sıfıra eşitle.
- Kareyi tamamla: $x$'in katsayısının yarısının karesini ekle.
- Kök formülü: $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.
- $\Delta = b^2 - 4ac$: pozitifse iki kök, sıfırsa bir kök, negatifse gerçek kök yok.
- $x_1 + x_2 = -\dfrac{b}{a}$, $x_1 x_2 = \dfrac{c}{a}$; tepe $x = -\dfrac{b}{2a}$.
- Kare hata bir parabol; en iyi ağırlık parabolün tepesinde.
