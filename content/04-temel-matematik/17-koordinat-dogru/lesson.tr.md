# Koordinat Düzlemi ve Doğru

Koordinat düzlemi, sayılarla şekilleri birbirine bağlayan köprü. Bir nokta
iki sayıyla yazılır, bir doğru bir denklemle; böylece geometri sorusunu
cebirle çözebiliriz, cebir sorusunu da çizerek görebiliriz. Makine
öğrenmesinin en temel modeli olan doğrusal regresyon da tam olarak bir
doğru: verinin içinden geçen en iyi doğruyu arar. Bu bölümde düzlemi,
iki nokta arasındaki uzaklığı, eğimi, doğrunun denklemini ve doğruların
birbirine göre durumunu göreceğiz.

Ön bilgi: Köklü Sayılar, Denklem Sistemleri, Fonksiyonlar.

## Koordinat düzlemi

Birbirini sıfırda dik kesen iki sayı doğrusu: yatay olana $x$ ekseni,
dikey olana $y$ ekseni denir. Kesiştikleri nokta **başlangıç noktası**,
yani $(0, 0)$. Her nokta bir **sıralı ikili** $(x, y)$ ile yazılır: önce
ne kadar sağa (ya da sola), sonra ne kadar yukarı (ya da aşağı).

<figure class="fig">
<svg viewBox="0 0 400 340" width="400"><line class="grid" x1="40.0" y1="320.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="320.0" x2="340.0" y2="320.0"/><line class="grid" x1="70.0" y1="320.0" x2="70.0" y2="20.0"/><line class="grid" x1="40.0" y1="290.0" x2="340.0" y2="290.0"/><line class="grid" x1="100.0" y1="320.0" x2="100.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="340.0" y2="260.0"/><line class="grid" x1="130.0" y1="320.0" x2="130.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="340.0" y2="230.0"/><line class="grid" x1="160.0" y1="320.0" x2="160.0" y2="20.0"/><line class="grid" x1="40.0" y1="200.0" x2="340.0" y2="200.0"/><line class="grid" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="220.0" y1="320.0" x2="220.0" y2="20.0"/><line class="grid" x1="40.0" y1="140.0" x2="340.0" y2="140.0"/><line class="grid" x1="250.0" y1="320.0" x2="250.0" y2="20.0"/><line class="grid" x1="40.0" y1="110.0" x2="340.0" y2="110.0"/><line class="grid" x1="280.0" y1="320.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="80.0" x2="340.0" y2="80.0"/><line class="grid" x1="310.0" y1="320.0" x2="310.0" y2="20.0"/><line class="grid" x1="40.0" y1="50.0" x2="340.0" y2="50.0"/><line class="grid" x1="340.0" y1="320.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="line" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="line" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><text class="dim" x="40.0" y="183.0" font-size="9" text-anchor="middle">−5</text><text class="dim" x="185.0" y="323.0" font-size="9" text-anchor="end">−5</text><text class="dim" x="70.0" y="183.0" font-size="9" text-anchor="middle">−4</text><text class="dim" x="185.0" y="293.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="100.0" y="183.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="185.0" y="263.0" font-size="9" text-anchor="end">−3</text><text class="dim" x="130.0" y="183.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="185.0" y="233.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="160.0" y="183.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="185.0" y="203.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="220.0" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="185.0" y="143.0" font-size="9" text-anchor="end">1</text><text class="dim" x="250.0" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="185.0" y="113.0" font-size="9" text-anchor="end">2</text><text class="dim" x="280.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="185.0" y="83.0" font-size="9" text-anchor="end">3</text><text class="dim" x="310.0" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="185.0" y="53.0" font-size="9" text-anchor="end">4</text><text class="dim" x="340.0" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="185.0" y="23.0" font-size="9" text-anchor="end">5</text><text class="dim" x="289.0" y="41.0" font-size="11" text-anchor="middle">I. bölge</text><text class="dim" x="91.0" y="41.0" font-size="11" text-anchor="middle">II. bölge</text><text class="dim" x="91.0" y="305.0" font-size="11" text-anchor="middle">III. bölge</text><text class="dim" x="289.0" y="305.0" font-size="11" text-anchor="middle">IV. bölge</text><circle class="dot" cx="280.0" cy="110.0" r="5"/><text class="ink" x="288.0" y="103.0" font-size="11" text-anchor="start">A(3, 2)</text><circle class="dot2" cx="130.0" cy="140.0" r="5"/><text class="ink" x="138.0" y="133.0" font-size="11" text-anchor="start">B(−2, 1)</text><circle class="dot3" cx="100.0" cy="230.0" r="5"/><text class="ink" x="108.0" y="223.0" font-size="11" text-anchor="start">C(−3, −2)</text><circle class="dot" cx="250.0" cy="260.0" r="5"/><text class="ink" x="258.0" y="253.0" font-size="11" text-anchor="start">D(2, −3)</text><text class="ink" x="348.0" y="174.0" font-size="12" text-anchor="start">x</text><text class="ink" x="190.0" y="14.0" font-size="12" text-anchor="middle">y</text></svg>
  <figcaption>Eksenler düzlemi dört bölgeye ayırır. A(3, 2) sağda ve yukarıda, B(−2, 1) solda ve yukarıda, C(−3, −2) solda ve aşağıda, D(2, −3) sağda ve aşağıda.</figcaption>
</figure>

| Bölge | $x$ | $y$ | Örnek |
|---|---|---|---|
| I. bölge | $+$ | $+$ | $(3, 2)$ |
| II. bölge | $-$ | $+$ | $(-2, 1)$ |
| III. bölge | $-$ | $-$ | $(-3, -2)$ |
| IV. bölge | $+$ | $-$ | $(2, -3)$ |

**Sıra önemli:** $(3, 2)$ ile $(2, 3)$ farklı noktalar. Eksen üzerindeki
noktalar hiçbir bölgeye ait değil: $x$ ekseninde $y = 0$, $y$ ekseninde
$x = 0$.

## İki nokta arasındaki uzaklık

İki noktayı birleştiren doğru parçası, yatay ve dikey farklarla bir dik
üçgenin hipotenüsü olur. Pisagor bağıntısı uzaklığı verir.

<figure class="fig">
<svg viewBox="0 0 400 296.0" width="400"><line class="grid" x1="40.0" y1="260.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="280.0" y2="260.0"/><line class="grid" x1="74.3" y1="260.0" x2="74.3" y2="20.0"/><line class="grid" x1="40.0" y1="225.7" x2="280.0" y2="225.7"/><line class="grid" x1="108.6" y1="260.0" x2="108.6" y2="20.0"/><line class="grid" x1="40.0" y1="191.4" x2="280.0" y2="191.4"/><line class="grid" x1="142.9" y1="260.0" x2="142.9" y2="20.0"/><line class="grid" x1="40.0" y1="157.1" x2="280.0" y2="157.1"/><line class="grid" x1="177.1" y1="260.0" x2="177.1" y2="20.0"/><line class="grid" x1="40.0" y1="122.9" x2="280.0" y2="122.9"/><line class="grid" x1="211.4" y1="260.0" x2="211.4" y2="20.0"/><line class="grid" x1="40.0" y1="88.6" x2="280.0" y2="88.6"/><line class="grid" x1="245.7" y1="260.0" x2="245.7" y2="20.0"/><line class="grid" x1="40.0" y1="54.3" x2="280.0" y2="54.3"/><line class="grid" x1="280.0" y1="260.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="280.0" y2="20.0"/><line class="line" x1="40.0" y1="225.7" x2="280.0" y2="225.7"/><line class="line" x1="74.3" y1="260.0" x2="74.3" y2="20.0"/><text class="dim" x="40.0" y="238.7" font-size="9" text-anchor="middle">−1</text><text class="dim" x="69.3" y="263.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="108.6" y="238.7" font-size="9" text-anchor="middle">1</text><text class="dim" x="69.3" y="194.4" font-size="9" text-anchor="end">1</text><text class="dim" x="142.9" y="238.7" font-size="9" text-anchor="middle">2</text><text class="dim" x="69.3" y="160.1" font-size="9" text-anchor="end">2</text><text class="dim" x="177.1" y="238.7" font-size="9" text-anchor="middle">3</text><text class="dim" x="69.3" y="125.9" font-size="9" text-anchor="end">3</text><text class="dim" x="211.4" y="238.7" font-size="9" text-anchor="middle">4</text><text class="dim" x="69.3" y="91.6" font-size="9" text-anchor="end">4</text><text class="dim" x="245.7" y="238.7" font-size="9" text-anchor="middle">5</text><text class="dim" x="69.3" y="57.3" font-size="9" text-anchor="end">5</text><text class="dim" x="280.0" y="238.7" font-size="9" text-anchor="middle">6</text><text class="dim" x="69.3" y="23.0" font-size="9" text-anchor="end">6</text><polygon class="curve2" fill="none" points="108.6,191.4 211.4,191.4 211.4,54.3"/><line class="curve" x1="108.6" y1="191.4" x2="211.4" y2="54.3"/><polyline class="dim" fill="none" stroke-width="1" points="202.9,191.4 202.9,182.9 211.4,182.9"/><circle class="dot" cx="108.6" cy="191.4" r="5"/><circle class="dot" cx="211.4" cy="54.3" r="5"/><text class="ink" x="100.6" y="183.4" font-size="11" text-anchor="end">P(1, 1)</text><text class="ink" x="219.4" y="50.3" font-size="11" text-anchor="start">Q(4, 5)</text><text class="ink" x="160.0" y="208.4" font-size="11" text-anchor="middle">Δx = 4 − 1 = 3</text><text class="ink" x="219.4" y="126.9" font-size="11" text-anchor="start">Δy = 5 − 1 = 4</text><text class="ink" x="160.0" y="286.0" font-size="13" text-anchor="middle">d = √(3² + 4²) = 5</text></svg>
  <figcaption>P(1, 1) ile Q(4, 5) arasında yatay fark 3, dikey fark 4. Bu iki kenar dik üçgen oluşturur; hipotenüs, yani PQ uzaklığı, 5.</figcaption>
</figure>

$$
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

$P(1, 1)$ ve $Q(4, 5)$ için $d = \sqrt{3^2 + 4^2} = \sqrt{25} = 5$.
Farkların karesi alındığı için hangi noktanın önce yazıldığı fark etmez.

**Orta nokta.** İki noktanın tam ortası, koordinatların ortalaması:

$$
M = \left( \frac{x_1 + x_2}{2}, \ \frac{y_1 + y_2}{2} \right)
$$

$A(-2, 3)$ ve $B(4, 7)$ için $M = \left( \frac{2}{2}, \frac{10}{2} \right) = (1, 5)$.

## Eğim

Bir doğrunun **eğimi**, sağa doğru bir birim gidince kaç birim yükseldiği.
İki noktasından hesaplanır: dikey değişim bölü yatay değişim.

$$
m = \frac{\Delta y}{\Delta x} = \frac{y_2 - y_1}{x_2 - x_1}
$$

<figure class="fig">
<svg viewBox="0 0 440 322.0" width="440"><line class="grid" x1="40.0" y1="280.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="280.0" x2="300.0" y2="280.0"/><line class="grid" x1="63.6" y1="280.0" x2="63.6" y2="20.0"/><line class="grid" x1="40.0" y1="256.4" x2="300.0" y2="256.4"/><line class="grid" x1="87.3" y1="280.0" x2="87.3" y2="20.0"/><line class="grid" x1="40.0" y1="232.7" x2="300.0" y2="232.7"/><line class="grid" x1="110.9" y1="280.0" x2="110.9" y2="20.0"/><line class="grid" x1="40.0" y1="209.1" x2="300.0" y2="209.1"/><line class="grid" x1="134.5" y1="280.0" x2="134.5" y2="20.0"/><line class="grid" x1="40.0" y1="185.5" x2="300.0" y2="185.5"/><line class="grid" x1="158.2" y1="280.0" x2="158.2" y2="20.0"/><line class="grid" x1="40.0" y1="161.8" x2="300.0" y2="161.8"/><line class="grid" x1="181.8" y1="280.0" x2="181.8" y2="20.0"/><line class="grid" x1="40.0" y1="138.2" x2="300.0" y2="138.2"/><line class="grid" x1="205.5" y1="280.0" x2="205.5" y2="20.0"/><line class="grid" x1="40.0" y1="114.5" x2="300.0" y2="114.5"/><line class="grid" x1="229.1" y1="280.0" x2="229.1" y2="20.0"/><line class="grid" x1="40.0" y1="90.9" x2="300.0" y2="90.9"/><line class="grid" x1="252.7" y1="280.0" x2="252.7" y2="20.0"/><line class="grid" x1="40.0" y1="67.3" x2="300.0" y2="67.3"/><line class="grid" x1="276.4" y1="280.0" x2="276.4" y2="20.0"/><line class="grid" x1="40.0" y1="43.6" x2="300.0" y2="43.6"/><line class="grid" x1="300.0" y1="280.0" x2="300.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="300.0" y2="20.0"/><line class="line" x1="40.0" y1="256.4" x2="300.0" y2="256.4"/><line class="line" x1="63.6" y1="280.0" x2="63.6" y2="20.0"/><text class="dim" x="110.9" y="269.4" font-size="9" text-anchor="middle">2</text><text class="dim" x="58.6" y="212.1" font-size="9" text-anchor="end">2</text><text class="dim" x="158.2" y="269.4" font-size="9" text-anchor="middle">4</text><text class="dim" x="58.6" y="164.8" font-size="9" text-anchor="end">4</text><text class="dim" x="205.5" y="269.4" font-size="9" text-anchor="middle">6</text><text class="dim" x="58.6" y="117.5" font-size="9" text-anchor="end">6</text><text class="dim" x="252.7" y="269.4" font-size="9" text-anchor="middle">8</text><text class="dim" x="58.6" y="70.3" font-size="9" text-anchor="end">8</text><text class="dim" x="300.0" y="269.4" font-size="9" text-anchor="middle">10</text><text class="dim" x="58.6" y="23.0" font-size="9" text-anchor="end">10</text><line class="curve" x1="51.8" y1="256.4" x2="170.0" y2="20.0"/><line class="curve2" x1="87.3" y1="185.5" x2="158.2" y2="185.5"/><line class="curve2" x1="158.2" y1="185.5" x2="158.2" y2="43.6"/><circle class="dot" cx="87.3" cy="185.5" r="5"/><circle class="dot" cx="158.2" cy="43.6" r="5"/><circle class="dot3" cx="63.6" cy="232.7" r="5"/><text class="ink" x="129.8" y="201.5" font-size="11" text-anchor="middle">yatay değişim Δx = 3</text><text class="ink" x="166.2" y="118.5" font-size="11" text-anchor="start">dikey değişim Δy = 6</text><text class="ink" x="81.3" y="177.5" font-size="11" text-anchor="end">(1, 3)</text><text class="ink" x="150.2" y="37.6" font-size="11" text-anchor="end">(4, 9)</text><text class="dim" x="73.6" y="248.7" font-size="11" text-anchor="start">y eksenini kestiği yer b = 1</text><text class="ink" x="193.6" y="310.0" font-size="13" text-anchor="middle">eğim m = 6 / 3 = 2</text></svg>
  <figcaption>(1, 3) ile (4, 9) arasında sağa 3 birim gidilince doğru 6 birim yükseliyor; eğim 6 / 3 = 2. Doğru y eksenini 1'de kesiyor.</figcaption>
</figure>

Eğimin işareti doğrunun yönünü söyler:

| Eğim | Doğru | Örnek |
|---|---|---|
| $m > 0$ | sağa doğru yükselir | $y = 2x + 1$ |
| $m < 0$ | sağa doğru alçalır | $y = -x + 4$ |
| $m = 0$ | yatay | $y = 3$ |
| tanımsız | dikey | $x = 2$ |

Dikey bir doğruda $\Delta x = 0$ olur, sıfıra bölünemediği için eğim
tanımsızdır. Denklem Sistemleri bölümündeki "eğimden gitmek" de buydu:
her adımda $x$ bir artınca $y$ eğim kadar değişiyor.

## Doğrunun denklemi

**Eğim–kesişim biçimi.** Eğimi $m$ olan ve $y$ eksenini $b$'de kesen doğru:

$$
y = mx + b
$$

Yukarıdaki doğrunun eğimi $2$; $(1, 3)$ noktasını koyunca $3 = 2 \cdot 1 + b$,
buradan $b = 1$. Denklem $y = 2x + 1$.

**Nokta–eğim biçimi.** Bir noktası $(x_1, y_1)$ ve eğimi $m$ bilinen doğru:

$$
y - y_1 = m(x - x_1)
$$

Eğimi $3$ olan ve $(2, 5)$'ten geçen doğru: $y - 5 = 3(x - 2)$, yani
$y = 3x - 1$.

**Genel biçim.** $ax + by + c = 0$. Örneğin $2x + 3y - 6 = 0$. $y$'yi
yalnız bırakınca $y = -\frac{2}{3}x + 2$: eğim $-\frac{2}{3}$. Eksenleri
kestiği yerler de kolay bulunur: $x = 0$ koyunca $y = 2$, $y = 0$ koyunca
$x = 3$.

**Yatay ve dikey doğrular.** $y = 4$ yatay bir doğru, eğimi $0$. $x = 3$
dikey bir doğru; eğimi tanımsız ve $y = mx + b$ biçiminde yazılamaz. Dikey
doğru testini hatırla: $x = 3$ doğrusu bir fonksiyonun grafiği değil.

**Nokta doğrunun üstünde mi?** Koordinatları denklemde yerine koy; eşitlik
sağlanıyorsa üstünde. $(2, 5)$ için $y = 2x + 1$: $2 \cdot 2 + 1 = 5$ ✓.

## Paralel ve dik doğrular

<figure class="fig">
<svg viewBox="0 0 400 385" width="400"><line class="grid" x1="40.0" y1="320.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="320.0" x2="340.0" y2="320.0"/><line class="grid" x1="70.0" y1="320.0" x2="70.0" y2="20.0"/><line class="grid" x1="40.0" y1="290.0" x2="340.0" y2="290.0"/><line class="grid" x1="100.0" y1="320.0" x2="100.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="340.0" y2="260.0"/><line class="grid" x1="130.0" y1="320.0" x2="130.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="340.0" y2="230.0"/><line class="grid" x1="160.0" y1="320.0" x2="160.0" y2="20.0"/><line class="grid" x1="40.0" y1="200.0" x2="340.0" y2="200.0"/><line class="grid" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="220.0" y1="320.0" x2="220.0" y2="20.0"/><line class="grid" x1="40.0" y1="140.0" x2="340.0" y2="140.0"/><line class="grid" x1="250.0" y1="320.0" x2="250.0" y2="20.0"/><line class="grid" x1="40.0" y1="110.0" x2="340.0" y2="110.0"/><line class="grid" x1="280.0" y1="320.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="80.0" x2="340.0" y2="80.0"/><line class="grid" x1="310.0" y1="320.0" x2="310.0" y2="20.0"/><line class="grid" x1="40.0" y1="50.0" x2="340.0" y2="50.0"/><line class="grid" x1="340.0" y1="320.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="line" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="line" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><text class="dim" x="40.0" y="183.0" font-size="9" text-anchor="middle">−5</text><text class="dim" x="185.0" y="323.0" font-size="9" text-anchor="end">−5</text><text class="dim" x="70.0" y="183.0" font-size="9" text-anchor="middle">−4</text><text class="dim" x="185.0" y="293.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="100.0" y="183.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="185.0" y="263.0" font-size="9" text-anchor="end">−3</text><text class="dim" x="130.0" y="183.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="185.0" y="233.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="160.0" y="183.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="185.0" y="203.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="220.0" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="185.0" y="143.0" font-size="9" text-anchor="end">1</text><text class="dim" x="250.0" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="185.0" y="113.0" font-size="9" text-anchor="end">2</text><text class="dim" x="280.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="185.0" y="83.0" font-size="9" text-anchor="end">3</text><text class="dim" x="310.0" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="185.0" y="53.0" font-size="9" text-anchor="end">4</text><text class="dim" x="340.0" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="185.0" y="23.0" font-size="9" text-anchor="end">5</text><line class="curve" x1="100.0" y1="320.0" x2="250.0" y2="20.0"/><line class="curve" x1="160.0" y1="320.0" x2="310.0" y2="20.0"/><line class="curve3" x1="40.0" y1="65.0" x2="340.0" y2="215.0"/><text class="ink" x="236.0" y="36.0" font-size="11" text-anchor="end">y = 2x + 1</text><text class="ink" x="316.0" y="56.0" font-size="11" text-anchor="start">y = 2x − 3</text><text class="ink" x="43.0" y="57.0" font-size="11" text-anchor="start">y = −½x + 1</text><text class="ink" x="190" y="355" font-size="12" text-anchor="middle">paralel: aynı eğim (m = 2)</text><text class="ink" x="190" y="375" font-size="12" text-anchor="middle">dik: eğimlerin çarpımı −1 (2 · (−½) = −1)</text></svg>
  <figcaption>y = 2x + 1 ile y = 2x − 3 doğrularının eğimi aynı (2), yalnızca y eksenini kestikleri yer farklı: paralel, hiç kesişmezler. Üçüncü doğrunun eğimi −½; 2 ile çarpımı −1 olduğu için ötekilere dik.</figcaption>
</figure>

- **Paralel:** eğimler eşit, $m_1 = m_2$ (ve $b$'ler farklı; $b$ de aynıysa
  iki denklem aynı doğru).
- **Dik:** eğimlerin çarpımı $-1$, yani $m_2 = -\dfrac{1}{m_1}$. Eğimi
  ters çevir, işaretini değiştir: $2$'ye dik eğim $-\frac{1}{2}$,
  $-\frac{3}{4}$'e dik eğim $\frac{4}{3}$.

Yatay ile dikey doğru da birbirine diktir; orada eğimlerden biri tanımsız
olduğu için çarpım kuralı kullanılmaz.

## İki doğrunun kesişimi

Kesişim noktası iki denklemi birden sağlar; bu bir denklem sistemi.
$y = 2x + 1$ ve $y = -x + 7$ için sağ tarafları eşitle:

$$
\begin{aligned}
&2x + 1 = -x + 7 \\
\Rightarrow\; &3x = 6 \\
\Rightarrow\; &x = 2
\end{aligned}
$$

$y = 2 \cdot 2 + 1 = 5$; kesişim $(2, 5)$. Eğimler eşitse ya hiç kesişmez
(paralel) ya da doğrular çakışıktır.

## Makine öğrenmesinde doğru

**Doğrusal regresyon bir doğru.** $\hat{y} = wx + b$ modelinde $w$ eğim,
$b$ de $y$ eksenini kestiği yer. Ev fiyatını metrekareden tahmin eden
$\hat{y} = 3x + 50$ modeli (bin TL) "her metrekare fiyata 3 bin TL
ekliyor, taban 50 bin TL" diyor. Eğitim, noktaların arasından geçen en
iyi $w$ ve $b$'yi bulmak.

**Hata dikey bir uzaklık.** Bir veri noktası $(x_i, y_i)$ ile doğru
arasındaki dikey fark $y_i - \hat{y}_i$, o örnekteki hata. Kayıp
fonksiyonu bu farkların karelerini toplar.

**Uzaklık formülü her yerde.** $k$ en yakın komşu yöntemi yeni bir örneği,
ona en yakın örneklere bakarak sınıflar; "en yakın" burada gördüğümüz
uzaklık formülüyle ölçülür (öklid uzaklığı).

**Karar sınırı bir doğru.** İki özellikli bir sınıflandırıcı, düzlemi
$w_1 x_1 + w_2 x_2 + b = 0$ doğrusuyla ikiye böler: bir yanı bir sınıf,
öbür yanı öteki sınıf. Bu, doğrunun genel biçimi.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$m = \dfrac{x_2 - x_1}{y_2 - y_1}$</p>
      <p>$m = \dfrac{y_2 - y_1}{x_1 - x_2}$</p>
      <p>$d = (x_2 - x_1) + (y_2 - y_1)$</p>
      <p>Dik eğim: $2 \to -2$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$m = \dfrac{y_2 - y_1}{x_2 - x_1}$</p>
      <p>Pay ve paydada aynı sıra</p>
      <p>$d = \sqrt{\Delta x^2 + \Delta y^2}$</p>
      <p>Dik eğim: $2 \to -\dfrac{1}{2}$</p>
    </div>
  </div>
  <figcaption>Eğimde önce dikey değişim yazılır ve iki farkta noktaların sırası aynı olur.</figcaption>
</figure>

- **Sıralı ikiliyi ters okumak.** $(3, 2)$'de önce $x$: sağa $3$, yukarı $2$.
- **Dikey doğruya eğim vermek.** $x = 3$ doğrusunun eğimi $0$ değil,
  tanımsız. Eğimi $0$ olan doğru yatay doğru.

## Özet

- Nokta $(x, y)$: önce yatay, sonra dikey; dört bölgede işaretler değişir.
- Uzaklık $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$; orta nokta koordinatların ortalaması.
- Eğim $m = \dfrac{y_2 - y_1}{x_2 - x_1}$; yatayda $0$, dikeyde tanımsız.
- Doğru: $y = mx + b$, $y - y_1 = m(x - x_1)$ ya da $ax + by + c = 0$.
- Paralel doğruların eğimi eşit; dik doğruların eğimlerinin çarpımı $-1$.
- Kesişim, iki doğrunun denklem sistemi çözülerek bulunur.
- Doğrusal regresyon bir doğru, hata dikey bir uzaklık, karar sınırı bir doğru denklemi.
