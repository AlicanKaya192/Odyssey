# Türev Kuralları ve Zincir Kuralı

Türevi tanımdan almak her seferinde bir limit hesabı demek. Neyse ki
buna gerek yok: birkaç kural ile her türlü formülün türevi parça parça
bulunuyor. Bu kuralların en önemlisi **zincir kuralı**; iç içe
fonksiyonların türevini veriyor. Bir sinir ağı iç içe fonksiyonlardan
başka bir şey değil ve onu eğiten **geri yayılım** algoritması, zincir
kuralının defalarca uygulanması.

Ön bilgi: Türev bölümü, MAT 1'deki Fonksiyonlar (bileşke).

## Kuvvet kuralı

Her gerçek $n$ için:

$$
\frac{d}{dx} x^n = n x^{n - 1}
$$

Kökleri ve kesirleri önce üs olarak yaz, sonra kuralı uygula:

| Fonksiyon | Üslü yazım | Türev |
|---|---|---|
| $\sqrt{x}$ | $x^{1/2}$ | $\frac{1}{2} x^{-1/2} = \dfrac{1}{2\sqrt{x}}$ |
| $\dfrac{1}{x^2}$ | $x^{-2}$ | $-2x^{-3} = -\dfrac{2}{x^3}$ |
| $\sqrt[3]{x^2}$ | $x^{2/3}$ | $\frac{2}{3} x^{-1/3}$ |

**Toplam ve sabit kat** (önceki bölümden): $(af + bg)' = af' + bg'$.

## Çarpım kuralı

İki fonksiyonun çarpımının türevi, türevlerin çarpımı **değil**:

$$
(f g)' = f' g + f g'
$$

Kontrol: $x \cdot x = x^2$'nin türevi $2x$; "türevlerin çarpımı" $1 \cdot 1 = 1$
derdi. Kurala göre $1 \cdot x + x \cdot 1 = 2x$ ✓.

<figure class="fig">
<svg viewBox="0 0 380 288" width="380"><rect class="box" x="60" y="70" width="240" height="160"/><rect class="dot" opacity="0.25" x="60" y="30" width="240" height="40"/><rect class="dot2" opacity="0.3" x="300" y="70" width="50" height="160"/><rect class="dot3" opacity="0.3" x="300" y="30" width="50" height="40"/><rect class="line" x="60" y="30" width="240" height="40"/><rect class="line" x="300" y="70" width="50" height="160"/><rect class="line" x="300" y="30" width="50" height="40"/><text class="ink" x="180.0" y="155.0" font-size="16" text-anchor="middle">f · g</text><text class="ink" x="180.0" y="55.0" font-size="13" text-anchor="middle">f · Δg</text><text class="ink" x="325.0" y="155.0" font-size="12" text-anchor="middle">g · Δf</text><text class="dim" x="325.0" y="22" font-size="10" text-anchor="middle">Δf · Δg</text><text class="ink" x="180.0" y="250" font-size="13" text-anchor="middle">f</text><text class="ink" x="325.0" y="250" font-size="12" text-anchor="middle">Δf</text><text class="ink" x="48" y="155.0" font-size="13" text-anchor="end">g</text><text class="ink" x="48" y="55.0" font-size="12" text-anchor="end">Δg</text><text class="dim" x="190" y="278" font-size="11.5" text-anchor="middle">alanın artışı ≈ f · Δg + g · Δf (köşedeki küçük kare ihmal edilir)</text></svg>
  <figcaption>Kenarları f ve g olan dikdörtgenin alanı f · g. Kenarlar Δf ve Δg kadar uzarsa alan iki şerit kadar artar: g · Δf ve f · Δg. Köşedeki Δf · Δg karesi, ikinci dereceden küçük olduğu için limitte kaybolur. Çarpım kuralının iki terimi bu iki şerit.</figcaption>
</figure>

Örnek: $x^2 e^x$ için $f = x^2$, $g = e^x$:

$$
(x^2 e^x)' = 2x \cdot e^x + x^2 \cdot e^x = (x^2 + 2x) e^x
$$

## Bölüm kuralı

$$
\left( \frac{f}{g} \right)' = \frac{f' g - f g'}{g^2}
$$

Paydaki sıra önemli: önce **pay**ın türevi. Örnek:

$$
\left( \frac{x}{x + 1} \right)' = \frac{1 \cdot (x + 1) - x \cdot 1}{(x + 1)^2} = \frac{1}{(x + 1)^2}
$$

Bölüm kuralı ezberlenmek zorunda değil: $\frac{f}{g} = f \cdot g^{-1}$
yazıp çarpım ve zincir kuralıyla aynı sonuca varılır.

## Zincir kuralı

$e^{3x}$, $(2x + 1)^5$, $\ln(1 + x^2)$: hepsi **bir fonksiyonun içinde
başka bir fonksiyon**. $y = f(u)$ ve $u = g(x)$ ise:

$$
\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = f'(g(x)) \cdot g'(x)
$$

Sözle: **dıştakinin türevi (içi olduğu gibi kalarak) çarpı içtekinin
türevi.**

<figure class="fig">
  <div class="flow">
    <span class="node">girdi<br><b>x</b></span>
    <span class="arrow">×3</span>
    <span class="node acc">iç<br><b>u = 3x</b></span>
    <span class="arrow">×2</span>
    <span class="node">dış<br><b>y = 2u</b></span>
  </div>
  <figcaption>Dişliler gibi: x bir birim dönünce u üç birim, u bir birim dönünce y iki birim dönüyor. Öyleyse x bir birim dönünce y 3 · 2 = 6 birim döner. Değişim hızları zincir boyunca çarpılır.</figcaption>
</figure>

Leibniz yazımında kural kesir sadeleşmesi gibi görünüyor: $du$'lar
"sadeleşiyor". Gerçek kesir değiller ama bu görüntü doğru sonucu
hatırlatıyor.

**Örnekler.**

| Fonksiyon | Dış, iç | Türev |
|---|---|---|
| $(3x + 1)^5$ | $u^5$, $u = 3x + 1$ | $5(3x + 1)^4 \cdot 3 = 15(3x + 1)^4$ |
| $e^{-x^2}$ | $e^u$, $u = -x^2$ | $e^{-x^2} \cdot (-2x)$ |
| $\ln(1 + x^2)$ | $\ln u$, $u = 1 + x^2$ | $\dfrac{1}{1 + x^2} \cdot 2x$ |
| $\sqrt{x^2 + 9}$ | $\sqrt{u}$, $u = x^2 + 9$ | $\dfrac{x}{\sqrt{x^2 + 9}}$ |

**Üç ve daha fazla halka.** Zincir uzarsa çarpım da uzar:
$\big(f(g(h(x)))\big)' = f'(g(h(x))) \cdot g'(h(x)) \cdot h'(x)$.

## Üstel ve logaritmik fonksiyonlar

Zincir kuralının sık kullanılan sonuçları:

| Fonksiyon | Türev |
|---|---|
| $e^{kx}$ | $k e^{kx}$ |
| $e^{g(x)}$ | $g'(x) e^{g(x)}$ |
| $a^x = e^{x \ln a}$ | $a^x \ln a$ |
| $\ln g(x)$ | $\dfrac{g'(x)}{g(x)}$ |

Son satır çok işe yarar: $\ln$'in türevi "içinin türevi bölü içi".
$(\ln(x^2 + 1))' = \dfrac{2x}{x^2 + 1}$.

## Sigmoidin türevi

$\sigma(x) = (1 + e^{-x})^{-1}$. Zincir kuralıyla (dış $u^{-1}$, iç
$1 + e^{-x}$):

$$
\sigma'(x) = -(1 + e^{-x})^{-2} \cdot (-e^{-x}) = \frac{e^{-x}}{(1 + e^{-x})^2}
$$

Bu ifade şaşırtıcı derecede düzenli bir biçime giriyor:

$$
\begin{aligned}
\frac{e^{-x}}{(1 + e^{-x})^2} &= \frac{1}{1 + e^{-x}} \cdot \frac{e^{-x}}{1 + e^{-x}} \\
&= \sigma(x) \big(1 - \sigma(x)\big)
\end{aligned}
$$

<figure class="fig">
<svg viewBox="0 0 480 256" width="480"><line class="grid" x1="40.0" y1="240.0" x2="40.0" y2="20.0"/><line class="grid" x1="68.6" y1="240.0" x2="68.6" y2="20.0"/><line class="grid" x1="97.1" y1="240.0" x2="97.1" y2="20.0"/><line class="grid" x1="125.7" y1="240.0" x2="125.7" y2="20.0"/><line class="grid" x1="154.3" y1="240.0" x2="154.3" y2="20.0"/><line class="grid" x1="182.9" y1="240.0" x2="182.9" y2="20.0"/><line class="grid" x1="211.4" y1="240.0" x2="211.4" y2="20.0"/><line class="grid" x1="240.0" y1="240.0" x2="240.0" y2="20.0"/><line class="grid" x1="268.6" y1="240.0" x2="268.6" y2="20.0"/><line class="grid" x1="297.1" y1="240.0" x2="297.1" y2="20.0"/><line class="grid" x1="325.7" y1="240.0" x2="325.7" y2="20.0"/><line class="grid" x1="354.3" y1="240.0" x2="354.3" y2="20.0"/><line class="grid" x1="382.9" y1="240.0" x2="382.9" y2="20.0"/><line class="grid" x1="411.4" y1="240.0" x2="411.4" y2="20.0"/><line class="grid" x1="440.0" y1="240.0" x2="440.0" y2="20.0"/><line class="grid" x1="40.0" y1="221.7" x2="440.0" y2="221.7"/><line class="grid" x1="40.0" y1="175.8" x2="440.0" y2="175.8"/><line class="grid" x1="40.0" y1="130.0" x2="440.0" y2="130.0"/><line class="grid" x1="40.0" y1="84.2" x2="440.0" y2="84.2"/><line class="grid" x1="40.0" y1="38.3" x2="440.0" y2="38.3"/><line class="line" x1="40.0" y1="221.7" x2="440.0" y2="221.7"/><line class="line" x1="240.0" y1="240.0" x2="240.0" y2="20.0"/><text class="dim" x="68.6" y="234.7" font-size="9" text-anchor="middle">−6</text><text class="dim" x="125.7" y="234.7" font-size="9" text-anchor="middle">−4</text><text class="dim" x="182.9" y="234.7" font-size="9" text-anchor="middle">−2</text><text class="dim" x="297.1" y="234.7" font-size="9" text-anchor="middle">2</text><text class="dim" x="354.3" y="234.7" font-size="9" text-anchor="middle">4</text><text class="dim" x="411.4" y="234.7" font-size="9" text-anchor="middle">6</text><text class="dim" x="235.0" y="41.3" font-size="9" text-anchor="end">1</text><polyline class="curve" fill="none" points="40.0,221.5 41.7,221.5 43.3,221.5 45.0,221.5 46.7,221.5 48.3,221.4 50.0,221.4 51.7,221.4 53.3,221.4 55.0,221.4 56.7,221.4 58.3,221.3 60.0,221.3 61.7,221.3 63.3,221.3 65.0,221.3 66.7,221.2 68.3,221.2 70.0,221.2 71.7,221.2 73.3,221.1 75.0,221.1 76.7,221.1 78.3,221.0 80.0,221.0 81.7,221.0 83.3,220.9 85.0,220.9 86.7,220.8 88.3,220.8 90.0,220.7 91.7,220.7 93.3,220.6 95.0,220.5 96.7,220.5 98.3,220.4 100.0,220.3 101.7,220.2 103.3,220.1 105.0,220.1 106.7,220.0 108.3,219.9 110.0,219.7 111.7,219.6 113.3,219.5 115.0,219.4 116.7,219.3 118.3,219.1 120.0,219.0 121.7,218.8 123.3,218.6 125.0,218.4 126.7,218.3 128.3,218.1 130.0,217.8 131.7,217.6 133.3,217.4 135.0,217.1 136.7,216.9 138.3,216.6 140.0,216.3 141.7,216.0 143.3,215.6 145.0,215.3 146.7,214.9 148.3,214.5 150.0,214.1 151.7,213.7 153.3,213.2 155.0,212.8 156.7,212.3 158.3,211.7 160.0,211.2 161.7,210.6 163.3,209.9 165.0,209.3 166.7,208.6 168.3,207.9 170.0,207.1 171.7,206.3 173.3,205.5 175.0,204.6 176.7,203.7 178.3,202.7 180.0,201.7 181.7,200.6 183.3,199.5 185.0,198.3 186.7,197.1 188.3,195.8 190.0,194.5 191.7,193.1 193.3,191.7 195.0,190.2 196.7,188.7 198.3,187.1 200.0,185.4 201.7,183.7 203.3,181.9 205.0,180.0 206.7,178.1 208.3,176.2 210.0,174.1 211.7,172.1 213.3,169.9 215.0,167.7 216.7,165.5 218.3,163.2 220.0,160.8 221.7,158.4 223.3,156.0 225.0,153.5 226.7,151.0 228.3,148.5 230.0,145.9 231.7,143.3 233.3,140.6 235.0,138.0 236.7,135.3 238.3,132.7 240.0,130.0 241.7,127.3 243.3,124.7 245.0,122.0 246.7,119.4 248.3,116.7 250.0,114.1 251.7,111.5 253.3,109.0 255.0,106.5 256.7,104.0 258.3,101.6 260.0,99.2 261.7,96.8 263.3,94.5 265.0,92.3 266.7,90.1 268.3,87.9 270.0,85.9 271.7,83.8 273.3,81.9 275.0,80.0 276.7,78.1 278.3,76.3 280.0,74.6 281.7,72.9 283.3,71.3 285.0,69.8 286.7,68.3 288.3,66.9 290.0,65.5 291.7,64.2 293.3,62.9 295.0,61.7 296.7,60.5 298.3,59.4 300.0,58.3 301.7,57.3 303.3,56.3 305.0,55.4 306.7,54.5 308.3,53.7 310.0,52.9 311.7,52.1 313.3,51.4 315.0,50.7 316.7,50.1 318.3,49.4 320.0,48.8 321.7,48.3 323.3,47.7 325.0,47.2 326.7,46.8 328.3,46.3 330.0,45.9 331.7,45.5 333.3,45.1 335.0,44.7 336.7,44.4 338.3,44.0 340.0,43.7 341.7,43.4 343.3,43.1 345.0,42.9 346.7,42.6 348.3,42.4 350.0,42.2 351.7,41.9 353.3,41.7 355.0,41.6 356.7,41.4 358.3,41.2 360.0,41.0 361.7,40.9 363.3,40.7 365.0,40.6 366.7,40.5 368.3,40.4 370.0,40.3 371.7,40.1 373.3,40.0 375.0,39.9 376.7,39.9 378.3,39.8 380.0,39.7 381.7,39.6 383.3,39.5 385.0,39.5 386.7,39.4 388.3,39.3 390.0,39.3 391.7,39.2 393.3,39.2 395.0,39.1 396.7,39.1 398.3,39.0 400.0,39.0 401.7,39.0 403.3,38.9 405.0,38.9 406.7,38.9 408.3,38.8 410.0,38.8 411.7,38.8 413.3,38.8 415.0,38.7 416.7,38.7 418.3,38.7 420.0,38.7 421.7,38.7 423.3,38.6 425.0,38.6 426.7,38.6 428.3,38.6 430.0,38.6 431.7,38.6 433.3,38.5 435.0,38.5 436.7,38.5 438.3,38.5 440.0,38.5"/><polyline class="curve2" fill="none" points="40.0,221.5 41.7,221.5 43.3,221.5 45.0,221.5 46.7,221.5 48.3,221.4 50.0,221.4 51.7,221.4 53.3,221.4 55.0,221.4 56.7,221.4 58.3,221.4 60.0,221.3 61.7,221.3 63.3,221.3 65.0,221.3 66.7,221.2 68.3,221.2 70.0,221.2 71.7,221.2 73.3,221.1 75.0,221.1 76.7,221.1 78.3,221.0 80.0,221.0 81.7,221.0 83.3,220.9 85.0,220.9 86.7,220.8 88.3,220.8 90.0,220.7 91.7,220.7 93.3,220.6 95.0,220.5 96.7,220.5 98.3,220.4 100.0,220.3 101.7,220.2 103.3,220.2 105.0,220.1 106.7,220.0 108.3,219.9 110.0,219.8 111.7,219.7 113.3,219.5 115.0,219.4 116.7,219.3 118.3,219.1 120.0,219.0 121.7,218.8 123.3,218.7 125.0,218.5 126.7,218.3 128.3,218.1 130.0,217.9 131.7,217.7 133.3,217.5 135.0,217.2 136.7,217.0 138.3,216.7 140.0,216.5 141.7,216.2 143.3,215.8 145.0,215.5 146.7,215.2 148.3,214.8 150.0,214.4 151.7,214.0 153.3,213.6 155.0,213.2 156.7,212.7 158.3,212.3 160.0,211.8 161.7,211.2 163.3,210.7 165.0,210.1 166.7,209.5 168.3,208.9 170.0,208.3 171.7,207.6 173.3,206.9 175.0,206.2 176.7,205.4 178.3,204.6 180.0,203.8 181.7,203.0 183.3,202.2 185.0,201.3 186.7,200.4 188.3,199.5 190.0,198.5 191.7,197.6 193.3,196.6 195.0,195.6 196.7,194.6 198.3,193.6 200.0,192.6 201.7,191.5 203.3,190.5 205.0,189.5 206.7,188.5 208.3,187.5 210.0,186.5 211.7,185.5 213.3,184.5 215.0,183.6 216.7,182.7 218.3,181.8 220.0,181.0 221.7,180.2 223.3,179.5 225.0,178.9 226.7,178.2 228.3,177.7 230.0,177.2 231.7,176.8 233.3,176.5 235.0,176.2 236.7,176.0 238.3,175.9 240.0,175.8 241.7,175.9 243.3,176.0 245.0,176.2 246.7,176.5 248.3,176.8 250.0,177.2 251.7,177.7 253.3,178.2 255.0,178.9 256.7,179.5 258.3,180.2 260.0,181.0 261.7,181.8 263.3,182.7 265.0,183.6 266.7,184.5 268.3,185.5 270.0,186.5 271.7,187.5 273.3,188.5 275.0,189.5 276.7,190.5 278.3,191.5 280.0,192.6 281.7,193.6 283.3,194.6 285.0,195.6 286.7,196.6 288.3,197.6 290.0,198.5 291.7,199.5 293.3,200.4 295.0,201.3 296.7,202.2 298.3,203.0 300.0,203.8 301.7,204.6 303.3,205.4 305.0,206.2 306.7,206.9 308.3,207.6 310.0,208.3 311.7,208.9 313.3,209.5 315.0,210.1 316.7,210.7 318.3,211.2 320.0,211.8 321.7,212.3 323.3,212.7 325.0,213.2 326.7,213.6 328.3,214.0 330.0,214.4 331.7,214.8 333.3,215.2 335.0,215.5 336.7,215.8 338.3,216.2 340.0,216.5 341.7,216.7 343.3,217.0 345.0,217.2 346.7,217.5 348.3,217.7 350.0,217.9 351.7,218.1 353.3,218.3 355.0,218.5 356.7,218.7 358.3,218.8 360.0,219.0 361.7,219.1 363.3,219.3 365.0,219.4 366.7,219.5 368.3,219.7 370.0,219.8 371.7,219.9 373.3,220.0 375.0,220.1 376.7,220.2 378.3,220.2 380.0,220.3 381.7,220.4 383.3,220.5 385.0,220.5 386.7,220.6 388.3,220.7 390.0,220.7 391.7,220.8 393.3,220.8 395.0,220.9 396.7,220.9 398.3,221.0 400.0,221.0 401.7,221.0 403.3,221.1 405.0,221.1 406.7,221.1 408.3,221.2 410.0,221.2 411.7,221.2 413.3,221.2 415.0,221.3 416.7,221.3 418.3,221.3 420.0,221.3 421.7,221.4 423.3,221.4 425.0,221.4 426.7,221.4 428.3,221.4 430.0,221.4 431.7,221.4 433.3,221.5 435.0,221.5 436.7,221.5 438.3,221.5 440.0,221.5"/><circle class="dot2" cx="240.0" cy="175.8" r="4.5"/><text class="ink" x="337.4" y="63.5" font-size="12" text-anchor="start">σ(x)</text><text class="ink" x="191.1" y="179.0" font-size="11" text-anchor="end">σ′(x) = σ(x)(1 − σ(x))</text><text class="ink" x="250.0" y="165.8" font-size="11" text-anchor="start">en büyük eğim: σ′(0) = 0,25</text><text class="dim" x="380.0" y="199.7" font-size="11" text-anchor="middle">uçlarda eğim ≈ 0</text></svg>
  <figcaption>Mor eğri sigmoid, turuncu eğri türevi. Türev en fazla 0,25 (x = 0'da); x büyüdükçe iki yönde de hızla sıfıra iniyor.</figcaption>
</figure>

Hesap açısından çok değerli: ileri geçişte $\sigma$ zaten hesaplanmış,
türev için yeni bir üstel gerekmiyor. Ama bir uyarı da taşıyor:
$\sigma' \le 0{,}25$.

## Makine öğrenmesinde zincir kuralı

**Tek bir nöron.** $z = wx + b$, $\hat{y} = \sigma(z)$, kayıp
$L = (\hat{y} - y)^2$. $L$, $w$'ye üç halkalı bir zincirle bağlı:

$$
\begin{aligned}
\frac{\partial L}{\partial w} &= \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w} \\
&= 2(\hat{y} - y) \cdot \sigma(z)\big(1 - \sigma(z)\big) \cdot x
\end{aligned}
$$

($\partial$ "kısmi türev": öteki değişkenler sabit tutularak alınan
türev; Kısmi Türev bölümünde ayrıntısı var.) $b$ için son halka
$\frac{\partial z}{\partial b} = 1$; ilk iki halka aynı. **Geri yayılım**
bu ortak halkaları bir kez hesaplayıp sondan başa doğru paylaştırıyor.

**Kaybolan gradyan.** Sigmoidli $10$ katmanlı bir ağda ilk katmanın
gradyanı $10$ tane $\sigma'$ çarpanı taşır. Her biri en fazla $0{,}25$:
$0{,}25^{10} \approx 0{,}000001$. İlk katmanlar neredeyse hiç öğrenemez.
ReLU'nun türevi pozitif bölgede tam $1$; çarpım küçülmüyor. Derin ağlarda
ReLU'nun yaygınlaşmasının ana nedeni bu.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$(fg)' = f' g'$</p>
      <p>$\left( \dfrac{f}{g} \right)' = \dfrac{f'}{g'}$</p>
      <p>$\big((3x + 1)^5\big)' = 5(3x + 1)^4$</p>
      <p>$(e^{2x})' = e^{2x}$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$(fg)' = f' g + f g'$</p>
      <p>$\left( \dfrac{f}{g} \right)' = \dfrac{f' g - f g'}{g^2}$</p>
      <p>$15(3x + 1)^4$: içtekinin türevi $3$</p>
      <p>$(e^{2x})' = 2e^{2x}$</p>
    </div>
  </div>
  <figcaption>Zincir kuralında en sık hata içtekinin türevini unutmak.</figcaption>
</figure>

- **Bölüm kuralında sırayı çevirmek.** $f g' - f' g$ yazmak sonucun
  işaretini ters çevirir.
- **$(a^x)'$ ile $(x^a)'$'yı karıştırmak.** $x^3$ kuvvet kuralı ($3x^2$),
  $3^x$ üstel ($3^x \ln 3$).

## Özet

- Kuvvet: $(x^n)' = n x^{n-1}$; kökleri ve kesirleri üs olarak yaz.
- Çarpım: $(fg)' = f'g + fg'$. Bölüm: $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$.
- Zincir: $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$; dıştakinin türevi çarpı içtekinin türevi.
- $(e^{g})' = g' e^{g}$, $(\ln g)' = \frac{g'}{g}$, $(a^x)' = a^x \ln a$.
- $\sigma' = \sigma(1 - \sigma) \le 0{,}25$.
- Nöronun gradyanı zincir kuralı; geri yayılım ortak halkaları paylaşıyor; sigmoid derin ağlarda gradyanı söndürüyor.
