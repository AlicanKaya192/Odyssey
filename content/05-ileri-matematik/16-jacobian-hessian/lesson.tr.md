# Jacobian, Hessian ve Çok Değişkenli Zincir Kuralı

Gradyan, **tek bir sayı veren** çok değişkenli bir fonksiyonun türeviydi.
Ama bir sinir ağı katmanı bir vektör alıp **bir vektör** veriyor: $3$
girdi, $5$ çıktı. Böyle bir fonksiyonun türevi bir matris: **Jacobian**.
Katmanlar art arda bağlanınca türevleri de art arda çarpılır; geri
yayılım tam olarak bu matris çarpımı. İkinci türevler de bir matris
oluşturur: **Hessian**. Kaybın ne kadar kıvrık olduğunu, bir noktanın dip
mi eyer mi olduğunu o söyler.

Ön bilgi: Kısmi Türev ve Gradyan bölümü, doğrusal cebirde Matris Çarpımı,
Determinant ve Özdeğerler bölümleri.

## Vektör değerli fonksiyonlar ve Jacobian

$F(x, y) = (x^2 y, \ x + 3y)$ iki girdi alıp iki çıktı veriyor. Her
çıktının her girdiye göre kısmi türevini bir matrise diz:

$$
J = \begin{bmatrix} \dfrac{\partial F_1}{\partial x} & \dfrac{\partial F_1}{\partial y} \\[2mm] \dfrac{\partial F_2}{\partial x} & \dfrac{\partial F_2}{\partial y} \end{bmatrix} = \begin{bmatrix} 2xy & x^2 \\ 1 & 3 \end{bmatrix}
$$

**Satır $i$, $i$'nci çıktının gradyanı; sütun $j$, $j$'nci girdi değişince
bütün çıktıların nasıl değiştiği.** $m$ çıktı ve $n$ girdi varsa Jacobian
$m \times n$ boyutunda. Tek çıktılı bir fonksiyonda Jacobian tek satır:
gradyanın kendisi.

## Jacobian yerel bir doğrusal dönüşüm

Tek değişkende teğet doğru, fonksiyonun noktanın yanındaki en iyi
doğrusal taklidiydi. Çok değişkende bu rolü Jacobian oynar:

$$
F(\mathbf{p} + \mathbf{h}) \approx F(\mathbf{p}) + J \, \mathbf{h}
$$

<figure class="fig">
<svg viewBox="0 0 460 274" width="460"><line class="grid" x1="41.2" y1="200.0" x2="41.2" y2="30.0"/><line class="grid" x1="67.8" y1="200.0" x2="67.8" y2="30.0"/><line class="grid" x1="94.4" y1="200.0" x2="94.4" y2="30.0"/><line class="grid" x1="120.9" y1="200.0" x2="120.9" y2="30.0"/><line class="grid" x1="147.5" y1="200.0" x2="147.5" y2="30.0"/><line class="grid" x1="174.1" y1="200.0" x2="174.1" y2="30.0"/><line class="grid" x1="20.0" y1="178.8" x2="190.0" y2="178.8"/><line class="grid" x1="20.0" y1="152.2" x2="190.0" y2="152.2"/><line class="grid" x1="20.0" y1="125.6" x2="190.0" y2="125.6"/><line class="grid" x1="20.0" y1="99.1" x2="190.0" y2="99.1"/><line class="grid" x1="20.0" y1="72.5" x2="190.0" y2="72.5"/><line class="grid" x1="20.0" y1="45.9" x2="190.0" y2="45.9"/><line class="grid" x1="269.0" y1="200.0" x2="269.0" y2="30.0"/><line class="grid" x1="292.8" y1="200.0" x2="292.8" y2="30.0"/><line class="grid" x1="316.5" y1="200.0" x2="316.5" y2="30.0"/><line class="grid" x1="340.2" y1="200.0" x2="340.2" y2="30.0"/><line class="grid" x1="364.0" y1="200.0" x2="364.0" y2="30.0"/><line class="grid" x1="387.8" y1="200.0" x2="387.8" y2="30.0"/><line class="grid" x1="411.5" y1="200.0" x2="411.5" y2="30.0"/><line class="grid" x1="435.2" y1="200.0" x2="435.2" y2="30.0"/><line class="grid" x1="250.0" y1="180.0" x2="440.0" y2="180.0"/><line class="grid" x1="250.0" y1="155.0" x2="440.0" y2="155.0"/><line class="grid" x1="250.0" y1="130.0" x2="440.0" y2="130.0"/><line class="grid" x1="250.0" y1="105.0" x2="440.0" y2="105.0"/><line class="grid" x1="250.0" y1="80.0" x2="440.0" y2="80.0"/><line class="grid" x1="250.0" y1="55.0" x2="440.0" y2="55.0"/><line class="grid" x1="250.0" y1="30.0" x2="440.0" y2="30.0"/><polygon class="dot" opacity="0.25" points="94.4,125.6 136.9,125.6 136.9,83.1 94.4,83.1 94.4,125.6"/><polygon class="curve" fill="none" points="94.4,125.6 136.9,125.6 136.9,83.1 94.4,83.1 94.4,125.6"/><circle class="dot2" cx="94.4" cy="125.6" r="4.5"/><polygon class="dot" opacity="0.25" points="316.5,180.0 320.3,178.0 324.3,176.0 328.2,174.0 332.3,172.0 336.5,170.0 340.7,168.0 345.0,166.0 349.3,164.0 353.8,162.0 358.3,160.0 362.9,158.0 367.6,156.0 372.3,154.0 377.1,152.0 382.0,150.0 387.0,148.0 392.1,146.0 397.2,144.0 402.4,142.0 407.7,140.0 405.8,136.0 403.9,131.8 402.0,127.6 400.1,123.4 398.2,119.0 396.3,114.6 394.4,110.0 392.5,105.4 390.6,100.8 388.7,96.0 386.8,91.2 384.9,86.2 383.0,81.2 381.1,76.2 379.2,71.0 377.3,65.8 375.4,60.4 373.5,55.0 371.6,49.6 369.7,44.0 364.4,46.0 359.2,48.0 354.1,50.0 349.0,52.0 344.0,54.0 339.1,56.0 334.3,58.0 329.6,60.0 324.9,62.0 320.3,64.0 315.8,66.0 311.3,68.0 307.0,70.0 302.7,72.0 298.5,74.0 294.3,76.0 290.2,78.0 286.3,80.0 282.3,82.0 278.5,84.0 280.4,89.6 282.3,95.0 284.2,100.4 286.1,105.8 288.0,111.0 289.9,116.2 291.8,121.2 293.7,126.2 295.6,131.2 297.5,136.0 299.4,140.8 301.3,145.4 303.2,150.0 305.1,154.6 307.0,159.0 308.9,163.4 310.8,167.6 312.7,171.8 314.6,176.0"/><polygon class="curve" fill="none" points="316.5,180.0 320.3,178.0 324.3,176.0 328.2,174.0 332.3,172.0 336.5,170.0 340.7,168.0 345.0,166.0 349.3,164.0 353.8,162.0 358.3,160.0 362.9,158.0 367.6,156.0 372.3,154.0 377.1,152.0 382.0,150.0 387.0,148.0 392.1,146.0 397.2,144.0 402.4,142.0 407.7,140.0 405.8,136.0 403.9,131.8 402.0,127.6 400.1,123.4 398.2,119.0 396.3,114.6 394.4,110.0 392.5,105.4 390.6,100.8 388.7,96.0 386.8,91.2 384.9,86.2 383.0,81.2 381.1,76.2 379.2,71.0 377.3,65.8 375.4,60.4 373.5,55.0 371.6,49.6 369.7,44.0 364.4,46.0 359.2,48.0 354.1,50.0 349.0,52.0 344.0,54.0 339.1,56.0 334.3,58.0 329.6,60.0 324.9,62.0 320.3,64.0 315.8,66.0 311.3,68.0 307.0,70.0 302.7,72.0 298.5,74.0 294.3,76.0 290.2,78.0 286.3,80.0 282.3,82.0 278.5,84.0 280.4,89.6 282.3,95.0 284.2,100.4 286.1,105.8 288.0,111.0 289.9,116.2 291.8,121.2 293.7,126.2 295.6,131.2 297.5,136.0 299.4,140.8 301.3,145.4 303.2,150.0 305.1,154.6 307.0,159.0 308.9,163.4 310.8,167.6 312.7,171.8 314.6,176.0"/><polygon class="curve2" fill="none" stroke-dasharray="5 4" points="316.5,180.0 392.5,140.0 354.5,60.0 278.5,100.0 316.5,180.0"/><circle class="dot2" cx="316.5" cy="180.0" r="4.5"/><text class="ink" x="105" y="18" font-size="11" text-anchor="middle">girdi: (1, 1) çevresinde küçük kare</text><text class="ink" x="345" y="18" font-size="11" text-anchor="middle">çıktı: F'nin görüntüsü</text><line class="curve3" x1="200" y1="115" x2="238" y2="115"/><polygon class="dim" points="242,115 234,110 234,120"/><text class="ink" x="220.0" y="108" font-size="13" text-anchor="middle">F</text><line class="curve" x1="60" y1="220" x2="84" y2="220"/><text class="ink" x="90" y="224" font-size="11" text-anchor="start">gerçek görüntü (eğri kenarlı)</text><line class="curve2" stroke-dasharray="5 4" x1="60" y1="240" x2="84" y2="240"/><text class="ink" x="90" y="244" font-size="11" text-anchor="start">J ile yaklaşım: paralelkenar</text><text class="dim" x="90" y="264" font-size="11" text-anchor="start">alan det J = 5 katına çıkıyor</text></svg>
  <figcaption>F(x, y) = (x² − y, x + y²), (1, 1) çevresinde. Küçük kare, F altında kenarları hafifçe eğri bir dörtgene gidiyor. Jacobian J = [[2, −1], [1, 2]] bunu bir paralelkenarla taklit ediyor; kare ne kadar küçükse taklit o kadar iyi.</figcaption>
</figure>

İki sonucu var:

- **Doğrusal katmanın Jacobian'ı ağırlık matrisidir.** $\mathbf{z} = W\mathbf{x} + \mathbf{b}$ için $J = W$; doğrusal bir fonksiyonun taklidi kendisi.
- **$\lvert \det J \rvert$ yerel alan (hacim) ölçeğidir.** Şekilde $\det J = 4 + 1 = 5$: küçük bölgeler beş kat büyüyor. Olasılık dağılımlarını dönüştüren modeller (normalizing flow) bu determinanttan yararlanıyor.

## Çok değişkenli zincir kuralı

$z = f(x, y)$ ve $x$, $y$ de $t$'ye bağlıysa $t$ değişince $z$ iki yoldan
etkilenir: $x$ üzerinden ve $y$ üzerinden. Etkiler toplanır:

$$
\frac{dz}{dt} = \frac{\partial z}{\partial x} \frac{dx}{dt} + \frac{\partial z}{\partial y} \frac{dy}{dt}
$$

Örnek: $z = x^2 y$, $x = 2t$, $y = t^2 + 1$, $t = 1$ ($x = 2$, $y = 2$):
$\frac{dz}{dt} = 2xy \cdot 2 + x^2 \cdot 2t = 16 + 8 = 24$.

**Matris hâli.** Her halka bir Jacobian; zincir boyunca Jacobianlar
**çarpılır**:

$$
J_{g \circ f}(\mathbf{x}) = J_g\big(f(\mathbf{x})\big) \cdot J_f(\mathbf{x})
$$

Tek değişkendeki "dıştakinin türevi çarpı içtekinin türevi" kuralının
aynısı; yalnızca sayılar matris oldu ve çarpma sırası önemli.

<figure class="fig">
  <div class="flow">
    <span class="node">girdi<br><b>x</b></span>
    <span class="arrow">W</span>
    <span class="node">katman<br><b>z = Wx</b></span>
    <span class="arrow">σ</span>
    <span class="node">aktivasyon<br><b>a = σ(z)</b></span>
    <span class="arrow">→</span>
    <span class="node acc">kayıp<br><b>L</b></span>
  </div>
  <figcaption>İleri geçiş soldan sağa. Geri yayılım sağdan sola: ∂L/∂a ile başlar, σ'nın Jacobian'ıyla, sonra W'nun Jacobian'ıyla çarpılarak girdiye kadar döner.</figcaption>
</figure>

## Hessian

Tek çıktılı $f$'nin bütün ikinci kısmi türevleri bir kare matris
oluşturur:

$$
H = \begin{bmatrix} f_{xx} & f_{xy} \\ f_{yx} & f_{yy} \end{bmatrix}
$$

Karışık türevler eşit olduğu için Hessian **simetrik**. Hessian,
gradyanın Jacobian'ı: gradyanın her bileşeninin her değişkene göre
türevi.

**İkinci dereceden Taylor.** Tek değişkendeki $\frac{1}{2} f'' h^2$ teriminin
çok değişkenli karşılığı:

$$
f(\mathbf{p} + \mathbf{h}) \approx f(\mathbf{p}) + \nabla f \cdot \mathbf{h} + \tfrac{1}{2} \, \mathbf{h}^\mathsf{T} H \, \mathbf{h}
$$

**Kritik noktayı sınıflandırmak.** $\nabla f = \mathbf{0}$ olan bir noktada
Hessian'ın **özdeğerlerine** bak:

| Özdeğerler | Nokta |
|---|---|
| hepsi pozitif | yerel en küçük |
| hepsi negatif | yerel en büyük |
| bazısı pozitif, bazısı negatif | eyer noktası |
| biri sıfır | karar verilemez |

<figure class="fig">
<svg viewBox="0 0 460 260" width="460"><line class="grid" x1="20.0" y1="210.0" x2="20.0" y2="20.0"/><line class="grid" x1="67.5" y1="210.0" x2="67.5" y2="20.0"/><line class="grid" x1="115.0" y1="210.0" x2="115.0" y2="20.0"/><line class="grid" x1="162.5" y1="210.0" x2="162.5" y2="20.0"/><line class="grid" x1="210.0" y1="210.0" x2="210.0" y2="20.0"/><line class="grid" x1="20.0" y1="210.0" x2="210.0" y2="210.0"/><line class="grid" x1="20.0" y1="162.5" x2="210.0" y2="162.5"/><line class="grid" x1="20.0" y1="115.0" x2="210.0" y2="115.0"/><line class="grid" x1="20.0" y1="67.5" x2="210.0" y2="67.5"/><line class="grid" x1="20.0" y1="20.0" x2="210.0" y2="20.0"/><line class="line" x1="20.0" y1="115.0" x2="210.0" y2="115.0"/><line class="line" x1="115.0" y1="210.0" x2="115.0" y2="20.0"/><line class="grid" x1="250.0" y1="210.0" x2="250.0" y2="20.0"/><line class="grid" x1="297.5" y1="210.0" x2="297.5" y2="20.0"/><line class="grid" x1="345.0" y1="210.0" x2="345.0" y2="20.0"/><line class="grid" x1="392.5" y1="210.0" x2="392.5" y2="20.0"/><line class="grid" x1="440.0" y1="210.0" x2="440.0" y2="20.0"/><line class="grid" x1="250.0" y1="210.0" x2="440.0" y2="210.0"/><line class="grid" x1="250.0" y1="162.5" x2="440.0" y2="162.5"/><line class="grid" x1="250.0" y1="115.0" x2="440.0" y2="115.0"/><line class="grid" x1="250.0" y1="67.5" x2="440.0" y2="67.5"/><line class="grid" x1="250.0" y1="20.0" x2="440.0" y2="20.0"/><line class="line" x1="250.0" y1="115.0" x2="440.0" y2="115.0"/><line class="line" x1="345.0" y1="210.0" x2="345.0" y2="20.0"/><polyline class="curve" fill="none" points="143.5,115.0 143.1,110.5 142.1,106.2 140.4,102.1 138.1,98.2 135.2,94.8 131.8,91.9 127.9,89.6 123.8,87.9 119.5,86.9 115.0,86.5 110.5,86.9 106.2,87.9 102.1,89.6 98.2,91.9 94.8,94.8 91.9,98.2 89.6,102.1 87.9,106.2 86.9,110.5 86.5,115.0 86.9,119.5 87.9,123.8 89.6,127.9 91.9,131.8 94.8,135.2 98.2,138.1 102.1,140.4 106.2,142.1 110.5,143.1 115.0,143.5 119.5,143.1 123.8,142.1 127.9,140.4 131.8,138.1 135.2,135.2 138.1,131.8 140.4,127.9 142.1,123.8 143.1,119.5 143.5,115.0"/><polyline class="curve" fill="none" points="167.2,115.0 166.6,106.8 164.7,98.9 161.6,91.3 157.3,84.3 151.9,78.1 145.7,72.7 138.7,68.4 131.1,65.3 123.2,63.4 115.0,62.7 106.8,63.4 98.9,65.3 91.3,68.4 84.3,72.7 78.1,78.1 72.7,84.3 68.4,91.3 65.3,98.9 63.4,106.8 62.7,115.0 63.4,123.2 65.3,131.1 68.4,138.7 72.7,145.7 78.1,151.9 84.3,157.3 91.3,161.6 98.9,164.7 106.8,166.6 115.0,167.2 123.2,166.6 131.1,164.7 138.7,161.6 145.7,157.3 151.9,151.9 157.3,145.7 161.6,138.7 164.7,131.1 166.6,123.2 167.2,115.0"/><polyline class="curve" fill="none" points="191.0,115.0 190.1,103.1 187.3,91.5 182.7,80.5 176.5,70.3 168.7,61.3 159.7,53.5 149.5,47.3 138.5,42.7 126.9,39.9 115.0,39.0 103.1,39.9 91.5,42.7 80.5,47.3 70.3,53.5 61.3,61.3 53.5,70.3 47.3,80.5 42.7,91.5 39.9,103.1 39.0,115.0 39.9,126.9 42.7,138.5 47.3,149.5 53.5,159.7 61.3,168.7 70.3,176.5 80.5,182.7 91.5,187.3 103.1,190.1 115.0,191.0 126.9,190.1 138.5,187.3 149.5,182.7 159.7,176.5 168.7,168.7 176.5,159.7 182.7,149.5 187.3,138.5 190.1,126.9 191.0,115.0"/><polyline class="curve" fill="none" points="437.6,197.3 434.8,194.2 432.1,191.0 429.3,187.8 426.6,184.7 423.9,181.5 421.3,178.3 418.7,175.2 416.1,172.0 413.6,168.8 411.1,165.7 408.7,162.5 406.4,159.3 404.2,156.2 402.0,153.0 399.9,149.8 398.0,146.7 396.2,143.5 394.5,140.3 392.9,137.2 391.5,134.0 390.3,130.8 389.3,127.7 388.5,124.5 388.0,121.3 387.6,118.2 387.5,115.0 387.6,111.8 388.0,108.7 388.5,105.5 389.3,102.3 390.3,99.2 391.5,96.0 392.9,92.8 394.5,89.7 396.2,86.5 398.0,83.3 399.9,80.2 402.0,77.0 404.2,73.8 406.4,70.7 408.7,67.5 411.1,64.3 413.6,61.2 416.1,58.0 418.7,54.8 421.3,51.7 423.9,48.5 426.6,45.3 429.3,42.2 432.1,39.0 434.8,35.8 437.6,32.7"/><polyline class="curve" fill="none" points="252.4,197.3 255.2,194.2 257.9,191.0 260.7,187.8 263.4,184.7 266.1,181.5 268.7,178.3 271.3,175.2 273.9,172.0 276.4,168.8 278.9,165.7 281.3,162.5 283.6,159.3 285.8,156.2 288.0,153.0 290.1,149.8 292.0,146.7 293.8,143.5 295.5,140.3 297.1,137.2 298.5,134.0 299.7,130.8 300.7,127.7 301.5,124.5 302.0,121.3 302.4,118.2 302.5,115.0 302.4,111.8 302.0,108.7 301.5,105.5 300.7,102.3 299.7,99.2 298.5,96.0 297.1,92.8 295.5,89.7 293.8,86.5 292.0,83.3 290.1,80.2 288.0,77.0 285.8,73.8 283.6,70.7 281.3,67.5 278.9,64.3 276.4,61.2 273.9,58.0 271.3,54.8 268.7,51.7 266.1,48.5 263.4,45.3 260.7,42.2 257.9,39.0 255.2,35.8 252.4,32.7"/><polyline class="curve" fill="none" points="439.5,181.5 437.3,178.3 435.2,175.2 433.1,172.0 431.1,168.8 429.1,165.7 427.3,162.5 425.5,159.3 423.8,156.2 422.2,153.0 420.7,149.8 419.3,146.7 418.0,143.5 416.8,140.3 415.7,137.2 414.8,134.0 414.0,130.8 413.4,127.7 412.8,124.5 412.5,121.3 412.2,118.2 412.2,115.0 412.2,111.8 412.5,108.7 412.8,105.5 413.4,102.3 414.0,99.2 414.8,96.0 415.7,92.8 416.8,89.7 418.0,86.5 419.3,83.3 420.7,80.2 422.2,77.0 423.8,73.8 425.5,70.7 427.3,67.5 429.1,64.3 431.1,61.2 433.1,58.0 435.2,54.8 437.3,51.7 439.5,48.5"/><polyline class="curve" fill="none" points="250.5,181.5 252.7,178.3 254.8,175.2 256.9,172.0 258.9,168.8 260.9,165.7 262.7,162.5 264.5,159.3 266.2,156.2 267.8,153.0 269.3,149.8 270.7,146.7 272.0,143.5 273.2,140.3 274.3,137.2 275.2,134.0 276.0,130.8 276.6,127.7 277.2,124.5 277.5,121.3 277.8,118.2 277.8,115.0 277.8,111.8 277.5,108.7 277.2,105.5 276.6,102.3 276.0,99.2 275.2,96.0 274.3,92.8 273.2,89.7 272.0,86.5 270.7,83.3 269.3,80.2 267.8,77.0 266.2,73.8 264.5,70.7 262.7,67.5 260.9,64.3 258.9,61.2 256.9,58.0 254.8,54.8 252.7,51.7 250.5,48.5"/><polyline class="curve2" fill="none" points="262.7,22.4 265.8,25.2 269.0,27.9 272.2,30.7 275.3,33.4 278.5,36.1 281.7,38.7 284.8,41.3 288.0,43.9 291.2,46.4 294.3,48.9 297.5,51.3 300.7,53.6 303.8,55.8 307.0,58.0 310.2,60.1 313.3,62.0 316.5,63.8 319.7,65.5 322.8,67.1 326.0,68.5 329.2,69.7 332.3,70.7 335.5,71.5 338.7,72.0 341.8,72.4 345.0,72.5 348.2,72.4 351.3,72.0 354.5,71.5 357.7,70.7 360.8,69.7 364.0,68.5 367.2,67.1 370.3,65.5 373.5,63.8 376.7,62.0 379.8,60.1 383.0,58.0 386.2,55.8 389.3,53.6 392.5,51.3 395.7,48.9 398.8,46.4 402.0,43.9 405.2,41.3 408.3,38.7 411.5,36.1 414.7,33.4 417.8,30.7 421.0,27.9 424.2,25.2 427.3,22.4"/><polyline class="curve2" fill="none" points="262.7,207.6 265.8,204.8 269.0,202.1 272.2,199.3 275.3,196.6 278.5,193.9 281.7,191.3 284.8,188.7 288.0,186.1 291.2,183.6 294.3,181.1 297.5,178.7 300.7,176.4 303.8,174.2 307.0,172.0 310.2,169.9 313.3,168.0 316.5,166.2 319.7,164.5 322.8,162.9 326.0,161.5 329.2,160.3 332.3,159.3 335.5,158.5 338.7,158.0 341.8,157.6 345.0,157.5 348.2,157.6 351.3,158.0 354.5,158.5 357.7,159.3 360.8,160.3 364.0,161.5 367.2,162.9 370.3,164.5 373.5,166.2 376.7,168.0 379.8,169.9 383.0,172.0 386.2,174.2 389.3,176.4 392.5,178.7 395.7,181.1 398.8,183.6 402.0,186.1 405.2,188.7 408.3,191.3 411.5,193.9 414.7,196.6 417.8,199.3 421.0,202.1 424.2,204.8 427.3,207.6"/><polyline class="curve2" fill="none" points="278.5,20.5 281.7,22.7 284.8,24.8 288.0,26.9 291.2,28.9 294.3,30.9 297.5,32.7 300.7,34.5 303.8,36.2 307.0,37.8 310.2,39.3 313.3,40.7 316.5,42.0 319.7,43.2 322.8,44.3 326.0,45.2 329.2,46.0 332.3,46.6 335.5,47.2 338.7,47.5 341.8,47.8 345.0,47.8 348.2,47.8 351.3,47.5 354.5,47.2 357.7,46.6 360.8,46.0 364.0,45.2 367.2,44.3 370.3,43.2 373.5,42.0 376.7,40.7 379.8,39.3 383.0,37.8 386.2,36.2 389.3,34.5 392.5,32.7 395.7,30.9 398.8,28.9 402.0,26.9 405.2,24.8 408.3,22.7 411.5,20.5"/><polyline class="curve2" fill="none" points="278.5,209.5 281.7,207.3 284.8,205.2 288.0,203.1 291.2,201.1 294.3,199.1 297.5,197.3 300.7,195.5 303.8,193.8 307.0,192.2 310.2,190.7 313.3,189.3 316.5,188.0 319.7,186.8 322.8,185.7 326.0,184.8 329.2,184.0 332.3,183.4 335.5,182.8 338.7,182.5 341.8,182.2 345.0,182.2 348.2,182.2 351.3,182.5 354.5,182.8 357.7,183.4 360.8,184.0 364.0,184.8 367.2,185.7 370.3,186.8 373.5,188.0 376.7,189.3 379.8,190.7 383.0,192.2 386.2,193.8 389.3,195.5 392.5,197.3 395.7,199.1 398.8,201.1 402.0,203.1 405.2,205.2 408.3,207.3 411.5,209.5"/><circle class="dot3" cx="115.0" cy="115.0" r="5"/><circle class="dot3" cx="345.0" cy="115.0" r="5"/><text class="ink" x="115" y="232" font-size="12" text-anchor="middle">x² + y²: en küçük</text><text class="dim" x="115" y="250" font-size="10.5" text-anchor="middle">H'nin özdeğerleri 2 ve 2 (ikisi de pozitif)</text><text class="ink" x="345" y="232" font-size="12" text-anchor="middle">x² − y²: eyer noktası</text><text class="dim" x="345" y="250" font-size="10.5" text-anchor="middle">H'nin özdeğerleri 2 ve −2 (işaretleri farklı)</text></svg>
  <figcaption>Solda çanak: bütün yönlerde yukarı bükük, H'nin iki özdeğeri de pozitif. Sağda eyer: x yönünde yukarı, y yönünde aşağı bükük; eş yükselti eğrileri hiperboller, özdeğerlerin işaretleri farklı.</figcaption>
</figure>

İki değişkende kısa yol: $\det H = f_{xx} f_{yy} - f_{xy}^2$. $\det H > 0$
ve $f_{xx} > 0$ ise en küçük; $\det H > 0$ ve $f_{xx} < 0$ ise en büyük;
$\det H < 0$ ise eyer. (Determinant özdeğerlerin çarpımı: negatifse
işaretler farklı.)

## Makine öğrenmesinde Jacobian ve Hessian

**Geri yayılım Jacobian çarpımıdır; ama Jacobianlar kurulmaz.** Bir
katmanda $1000$ girdi ve $1000$ çıktı varsa Jacobian'da bir milyon sayı
var. Kütüphaneler bu matrisi hiç oluşturmadan, kaybın gradyan vektörünü
sağdan sola taşıyarak **vektör–Jacobian çarpımını** doğrudan hesaplıyor:
doğrusal katmanda $\frac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T} \frac{\partial L}{\partial \mathbf{z}}$.

**Eleman eleman aktivasyonların Jacobian'ı köşegen.** $a_i = \sigma(z_i)$
yalnızca kendi $z_i$'sine bağlı; Jacobian köşegeninde $\sigma'(z_i)$,
başka yerde sıfır. Çarpım, vektörü eleman eleman $\sigma'$ ile çarpmaya
iniyor.

**Hessian eğriliği ve öğrenme oranını anlatır.** Kaybın Hessian'ının en
büyük özdeğeri $\lambda_{\max}$, en dik kıvrılan yönü söyler. Gradyan
inişinin kararlı kalması için öğrenme oranı yaklaşık $\frac{2}{\lambda_{\max}}$'tan
küçük olmalı. En büyük ile en küçük özdeğerin oranı (koşul sayısı)
büyükse eş yükselti eğrileri basık elipslerdir ve iniş zikzak çizer.

**Newton yöntemi çok değişkende.** $\Delta = -H^{-1} \nabla f$. Eğriliği
her yönde hesaba kattığı için birkaç adımda yakınsar; ama $n$ parametrede
$n \times n$'lik Hessian'ı kurup ters çevirmek büyük modellerde imkânsız.
Adam gibi yöntemler Hessian'ın köşegenine kaba bir yaklaşım kullanarak bu
fikirden pay alıyor.

**Eyer noktaları.** Çok boyutlu kayıplarda gradyanın sıfır olduğu
noktaların çoğu en küçük değil eyer: binlerce yönün hepsinde birden
yukarı bükük olmak zor. Gradyan inişinin küçük gürültüsü eyerden kaçmaya
yardım ediyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>Jacobian'da satır = girdi</p>
      <p>$J_{g \circ f} = J_f J_g$</p>
      <p>$\nabla f = \mathbf{0}$ ise en küçük</p>
      <p>$\det H > 0$ ise en küçük</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Satır = çıktı, sütun = girdi</p>
      <p>$J_{g \circ f} = J_g J_f$ (dıştaki solda)</p>
      <p>Hessian'ın özdeğerlerine bak</p>
      <p>Ayrıca $f_{xx} > 0$ olmalı</p>
    </div>
  </div>
  <figcaption>Hem en küçükte hem en büyükte det H pozitif; ikisini ayıran köşegenin işareti.</figcaption>
</figure>

- **Zincir kuralında bir yolu unutmak.** $z$, $t$'ye hem $x$ hem $y$
  üzerinden bağlıysa iki terim de toplanır.

## Özet

- Jacobian: vektör değerli fonksiyonun türevi; satır $i$, çıktı $i$'nin gradyanı; $m \times n$.
- $F(\mathbf{p} + \mathbf{h}) \approx F(\mathbf{p}) + J\mathbf{h}$; doğrusal katmanda $J = W$; $\lvert \det J \rvert$ yerel hacim ölçeği.
- Zincir kuralı: yollar toplanır, $\frac{dz}{dt} = z_x x' + z_y y'$; matris hâli $J_{g \circ f} = J_g J_f$.
- Hessian: ikinci kısmi türevlerin simetrik matrisi; Taylor'da $\frac{1}{2}\mathbf{h}^\mathsf{T} H \mathbf{h}$.
- Özdeğerler: hepsi pozitif en küçük, hepsi negatif en büyük, karışık eyer.
- Geri yayılım vektör–Jacobian çarpımı; Hessian eğrilik, öğrenme oranı sınırı ve Newton adımı $-H^{-1}\nabla f$.
