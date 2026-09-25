# Doğrusal Regresyonun Matematiği

Makine Öğrenmesi patikasında doğrusal regresyonu tek satırla eğittik ve
modelin bir eğim ile bir kesişim öğrendiğini gördük. Bu bölümde o
sayıların nereden geldiğini açıyoruz: kayıp fonksiyonu, türevi sıfıra
eşitlemek, matris biçimindeki **normal denklemler**, çözümün geometrik
anlamı (dik izdüşüm) ve olasılıkla bağlantısı. Şimdiye kadarki doğrusal
cebir, türev ve olasılık bölümlerinin hepsi burada buluşuyor.

Ön bilgi: Matris Çarpımı; Determinant ve Ters Matris; Kısmi Türev ve
Gradyan; Kovaryans ve Korelasyon; En Çok Olabilirlik Kestirimi.

## Model ve kayıp

Tek özellikli model: $\hat{y} = b + wx$. Her gözlemin **kalıntısı**
$e_i = y_i - \hat{y}_i$. İyi bir doğru, kalıntıları küçük olandır; ama
pozitif ve negatif kalıntılar birbirini götürmesin diye karelerini
toplarız:

$$
\text{SSE}(b, w) = \sum_{i=1}^{n} \big(y_i - b - w x_i\big)^2
$$

Bu **en küçük kareler** yöntemidir.

<figure class="fig">
<svg viewBox="0 0 420 250" width="420"><line class="grid" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><line class="grid" x1="96.7" y1="220.0" x2="96.7" y2="20.0"/><line class="grid" x1="153.3" y1="220.0" x2="153.3" y2="20.0"/><line class="grid" x1="210.0" y1="220.0" x2="210.0" y2="20.0"/><line class="grid" x1="266.7" y1="220.0" x2="266.7" y2="20.0"/><line class="grid" x1="323.3" y1="220.0" x2="323.3" y2="20.0"/><line class="grid" x1="380.0" y1="220.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="220.0" x2="380.0" y2="220.0"/><line class="grid" x1="40.0" y1="189.2" x2="380.0" y2="189.2"/><line class="grid" x1="40.0" y1="158.5" x2="380.0" y2="158.5"/><line class="grid" x1="40.0" y1="127.7" x2="380.0" y2="127.7"/><line class="grid" x1="40.0" y1="96.9" x2="380.0" y2="96.9"/><line class="grid" x1="40.0" y1="66.2" x2="380.0" y2="66.2"/><line class="grid" x1="40.0" y1="35.4" x2="380.0" y2="35.4"/><line class="line" x1="40.0" y1="220.0" x2="380.0" y2="220.0"/><line class="line" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><text class="dim" x="96.7" y="233.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="153.3" y="233.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="210.0" y="233.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="266.7" y="233.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="323.3" y="233.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="35.0" y="192.2" font-size="9" text-anchor="end">1</text><text class="dim" x="35.0" y="161.5" font-size="9" text-anchor="end">2</text><text class="dim" x="35.0" y="130.7" font-size="9" text-anchor="end">3</text><text class="dim" x="35.0" y="99.9" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="69.2" font-size="9" text-anchor="end">5</text><text class="dim" x="35.0" y="38.4" font-size="9" text-anchor="end">6</text><line class="curve2" stroke-width="2.5" x1="96.7" y1="158.5" x2="96.7" y2="133.8"/><line class="curve2" stroke-width="2.5" x1="153.3" y1="96.9" x2="153.3" y2="115.4"/><line class="curve2" stroke-width="2.5" x1="210.0" y1="66.2" x2="210.0" y2="96.9"/><line class="curve2" stroke-width="2.5" x1="266.7" y1="96.9" x2="266.7" y2="78.5"/><line class="curve2" stroke-width="2.5" x1="323.3" y1="66.2" x2="323.3" y2="60.0"/><polyline class="curve" fill="none" points="40.0,152.3 41.4,151.8 42.8,151.4 44.2,150.9 45.7,150.5 47.1,150.0 48.5,149.5 49.9,149.1 51.3,148.6 52.8,148.2 54.2,147.7 55.6,147.2 57.0,146.8 58.4,146.3 59.8,145.8 61.2,145.4 62.7,144.9 64.1,144.5 65.5,144.0 66.9,143.5 68.3,143.1 69.8,142.6 71.2,142.2 72.6,141.7 74.0,141.2 75.4,140.8 76.8,140.3 78.2,139.8 79.7,139.4 81.1,138.9 82.5,138.5 83.9,138.0 85.3,137.5 86.8,137.1 88.2,136.6 89.6,136.2 91.0,135.7 92.4,135.2 93.8,134.8 95.2,134.3 96.7,133.8 98.1,133.4 99.5,132.9 100.9,132.5 102.3,132.0 103.8,131.5 105.2,131.1 106.6,130.6 108.0,130.2 109.4,129.7 110.8,129.2 112.2,128.8 113.7,128.3 115.1,127.8 116.5,127.4 117.9,126.9 119.3,126.5 120.8,126.0 122.2,125.5 123.6,125.1 125.0,124.6 126.4,124.2 127.8,123.7 129.2,123.2 130.7,122.8 132.1,122.3 133.5,121.8 134.9,121.4 136.3,120.9 137.8,120.5 139.2,120.0 140.6,119.5 142.0,119.1 143.4,118.6 144.8,118.2 146.2,117.7 147.7,117.2 149.1,116.8 150.5,116.3 151.9,115.8 153.3,115.4 154.8,114.9 156.2,114.5 157.6,114.0 159.0,113.5 160.4,113.1 161.8,112.6 163.2,112.2 164.7,111.7 166.1,111.2 167.5,110.8 168.9,110.3 170.3,109.8 171.8,109.4 173.2,108.9 174.6,108.5 176.0,108.0 177.4,107.5 178.8,107.1 180.2,106.6 181.7,106.2 183.1,105.7 184.5,105.2 185.9,104.8 187.3,104.3 188.8,103.8 190.2,103.4 191.6,102.9 193.0,102.5 194.4,102.0 195.8,101.5 197.2,101.1 198.7,100.6 200.1,100.2 201.5,99.7 202.9,99.2 204.3,98.8 205.8,98.3 207.2,97.8 208.6,97.4 210.0,96.9 211.4,96.5 212.8,96.0 214.3,95.5 215.7,95.1 217.1,94.6 218.5,94.2 219.9,93.7 221.3,93.2 222.8,92.8 224.2,92.3 225.6,91.8 227.0,91.4 228.4,90.9 229.8,90.5 231.2,90.0 232.7,89.5 234.1,89.1 235.5,88.6 236.9,88.2 238.3,87.7 239.8,87.2 241.2,86.8 242.6,86.3 244.0,85.8 245.4,85.4 246.8,84.9 248.2,84.5 249.7,84.0 251.1,83.5 252.5,83.1 253.9,82.6 255.3,82.2 256.8,81.7 258.2,81.2 259.6,80.8 261.0,80.3 262.4,79.8 263.8,79.4 265.2,78.9 266.7,78.5 268.1,78.0 269.5,77.5 270.9,77.1 272.3,76.6 273.8,76.2 275.2,75.7 276.6,75.2 278.0,74.8 279.4,74.3 280.8,73.8 282.2,73.4 283.7,72.9 285.1,72.5 286.5,72.0 287.9,71.5 289.3,71.1 290.8,70.6 292.2,70.2 293.6,69.7 295.0,69.2 296.4,68.8 297.8,68.3 299.2,67.8 300.7,67.4 302.1,66.9 303.5,66.5 304.9,66.0 306.3,65.5 307.8,65.1 309.2,64.6 310.6,64.2 312.0,63.7 313.4,63.2 314.8,62.8 316.2,62.3 317.7,61.8 319.1,61.4 320.5,60.9 321.9,60.5 323.3,60.0 324.8,59.5 326.2,59.1 327.6,58.6 329.0,58.2 330.4,57.7 331.8,57.2 333.2,56.8 334.7,56.3 336.1,55.8 337.5,55.4 338.9,54.9 340.3,54.5 341.8,54.0 343.2,53.5 344.6,53.1 346.0,52.6 347.4,52.2 348.8,51.7 350.2,51.2 351.7,50.8 353.1,50.3 354.5,49.8 355.9,49.4 357.3,48.9 358.8,48.5 360.2,48.0 361.6,47.5 363.0,47.1 364.4,46.6 365.8,46.2 367.2,45.7 368.7,45.2 370.1,44.8 371.5,44.3 372.9,43.8 374.3,43.4 375.8,42.9 377.2,42.5 378.6,42.0 380.0,41.5"/><circle class="dot" cx="96.7" cy="158.5" r="5"/><circle class="dot" cx="153.3" cy="96.9" r="5"/><circle class="dot" cx="210.0" cy="66.2" r="5"/><circle class="dot" cx="266.7" cy="96.9" r="5"/><circle class="dot" cx="323.3" cy="66.2" r="5"/><circle class="dot3" cx="210.0" cy="96.9" r="5"/><text class="ink" x="220.0" y="114.9" font-size="10" text-anchor="start">(x̄, ȳ) = (3, 4)</text><text class="ink" x="374.3" y="33.4" font-size="11" text-anchor="end">ŷ = 2,2 + 0,6x</text><text class="ink" x="48.5" y="29.2" font-size="10" text-anchor="start">kalıntı eᵢ = yᵢ − ŷᵢ</text></svg>
  <figcaption>Beş nokta ve en küçük kareler doğrusu. Turuncu dikey çizgiler kalıntılar; doğru, bunların karelerinin toplamını en küçük yapan doğru. Doğru her zaman ortalamalar noktasından (x̄, ȳ) geçer.</figcaption>
</figure>

## Türevi sıfıra eşitlemek

İki kısmi türev:

$$
\frac{\partial\,\text{SSE}}{\partial b} = -2\sum (y_i - b - w x_i) = 0
$$

$$
\frac{\partial\,\text{SSE}}{\partial w} = -2\sum x_i (y_i - b - w x_i) = 0
$$

Birinciden $b = \bar{y} - w\bar{x}$: doğru $(\bar{x}, \bar{y})$'den geçer.
Bunu ikinciye koyunca:

$$
w = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{s_{xy}}{s_x^2} = r\,\frac{s_y}{s_x}
$$

Eğim, kovaryansın $x$'in varyansına oranı; korelasyonla da yazılabilir.

**Örnek.** Kovaryans bölümündeki veri: $x = 1, 2, 3, 4, 5$,
$y = 2, 4, 5, 4, 5$. $\sum(x - \bar{x})(y - \bar{y}) = 6$,
$\sum(x - \bar{x})^2 = 10$. $w = 0{,}6$, $b = 4 - 0{,}6 \cdot 3 = 2{,}2$.
Doğru: $\hat{y} = 2{,}2 + 0{,}6x$.

<figure class="fig">
<svg viewBox="0 0 420 250" width="420"><line class="grid" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><line class="grid" x1="84.0" y1="210.0" x2="84.0" y2="20.0"/><line class="grid" x1="118.0" y1="210.0" x2="118.0" y2="20.0"/><line class="grid" x1="152.0" y1="210.0" x2="152.0" y2="20.0"/><line class="grid" x1="186.0" y1="210.0" x2="186.0" y2="20.0"/><line class="grid" x1="220.0" y1="210.0" x2="220.0" y2="20.0"/><line class="grid" x1="254.0" y1="210.0" x2="254.0" y2="20.0"/><line class="grid" x1="288.0" y1="210.0" x2="288.0" y2="20.0"/><line class="grid" x1="322.0" y1="210.0" x2="322.0" y2="20.0"/><line class="grid" x1="356.0" y1="210.0" x2="356.0" y2="20.0"/><line class="grid" x1="390.0" y1="210.0" x2="390.0" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="grid" x1="50.0" y1="178.3" x2="390.0" y2="178.3"/><line class="grid" x1="50.0" y1="146.7" x2="390.0" y2="146.7"/><line class="grid" x1="50.0" y1="115.0" x2="390.0" y2="115.0"/><line class="grid" x1="50.0" y1="83.3" x2="390.0" y2="83.3"/><line class="grid" x1="50.0" y1="51.7" x2="390.0" y2="51.7"/><line class="grid" x1="50.0" y1="20.0" x2="390.0" y2="20.0"/><line class="line" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="line" x1="118.0" y1="210.0" x2="118.0" y2="20.0"/><text class="dim" x="113.0" y="181.3" font-size="9" text-anchor="end">2</text><text class="dim" x="113.0" y="149.7" font-size="9" text-anchor="end">4</text><text class="dim" x="113.0" y="118.0" font-size="9" text-anchor="end">6</text><text class="dim" x="113.0" y="86.3" font-size="9" text-anchor="end">8</text><text class="dim" x="113.0" y="54.7" font-size="9" text-anchor="end">10</text><text class="dim" x="113.0" y="23.0" font-size="9" text-anchor="end">12</text><polyline class="curve" fill="none" points="51.4,16.3 52.8,18.9 54.2,21.5 55.7,24.0 57.1,26.6 58.5,29.1 59.9,31.6 61.3,34.1 62.8,36.5 64.2,39.0 65.6,41.4 67.0,43.7 68.4,46.1 69.8,48.5 71.2,50.8 72.7,53.1 74.1,55.4 75.5,57.6 76.9,59.8 78.3,62.0 79.8,64.2 81.2,66.4 82.6,68.5 84.0,70.7 85.4,72.8 86.8,74.8 88.2,76.9 89.7,78.9 91.1,80.9 92.5,82.9 93.9,84.9 95.3,86.9 96.8,88.8 98.2,90.7 99.6,92.6 101.0,94.4 102.4,96.3 103.8,98.1 105.2,99.9 106.7,101.6 108.1,103.4 109.5,105.1 110.9,106.8 112.3,108.5 113.8,110.2 115.2,111.8 116.6,113.4 118.0,115.0 119.4,116.6 120.8,118.1 122.2,119.7 123.7,121.2 125.1,122.6 126.5,124.1 127.9,125.5 129.3,127.0 130.8,128.4 132.2,129.7 133.6,131.1 135.0,132.4 136.4,133.7 137.8,135.0 139.2,136.3 140.7,137.5 142.1,138.7 143.5,139.9 144.9,141.1 146.3,142.3 147.8,143.4 149.2,144.5 150.6,145.6 152.0,146.7 153.4,147.7 154.8,148.7 156.2,149.7 157.7,150.7 159.1,151.7 160.5,152.6 161.9,153.5 163.3,154.4 164.8,155.3 166.2,156.1 167.6,156.9 169.0,157.8 170.4,158.5 171.8,159.3 173.2,160.0 174.7,160.7 176.1,161.4 177.5,162.1 178.9,162.8 180.3,163.4 181.8,164.0 183.2,164.6 184.6,165.1 186.0,165.7 187.4,166.2 188.8,166.7 190.2,167.2 191.7,167.6 193.1,168.0 194.5,168.4 195.9,168.8 197.3,169.2 198.8,169.5 200.2,169.8 201.6,170.1 203.0,170.4 204.4,170.7 205.8,170.9 207.2,171.1 208.7,171.3 210.1,171.5 211.5,171.6 212.9,171.7 214.3,171.8 215.8,171.9 217.2,172.0 218.6,172.0 220.0,172.0 221.4,172.0 222.8,172.0 224.2,171.9 225.7,171.8 227.1,171.7 228.5,171.6 229.9,171.5 231.3,171.3 232.8,171.1 234.2,170.9 235.6,170.7 237.0,170.4 238.4,170.1 239.8,169.8 241.2,169.5 242.7,169.2 244.1,168.8 245.5,168.4 246.9,168.0 248.3,167.6 249.8,167.2 251.2,166.7 252.6,166.2 254.0,165.7 255.4,165.1 256.8,164.6 258.2,164.0 259.7,163.4 261.1,162.8 262.5,162.1 263.9,161.4 265.3,160.7 266.8,160.0 268.2,159.3 269.6,158.5 271.0,157.8 272.4,156.9 273.8,156.1 275.2,155.3 276.7,154.4 278.1,153.5 279.5,152.6 280.9,151.7 282.3,150.7 283.8,149.7 285.2,148.7 286.6,147.7 288.0,146.7 289.4,145.6 290.8,144.5 292.2,143.4 293.7,142.3 295.1,141.1 296.5,139.9 297.9,138.7 299.3,137.5 300.8,136.3 302.2,135.0 303.6,133.7 305.0,132.4 306.4,131.1 307.8,129.7 309.2,128.4 310.7,127.0 312.1,125.5 313.5,124.1 314.9,122.6 316.3,121.2 317.7,119.7 319.2,118.1 320.6,116.6 322.0,115.0 323.4,113.4 324.8,111.8 326.2,110.2 327.7,108.5 329.1,106.8 330.5,105.1 331.9,103.4 333.3,101.6 334.7,99.9 336.2,98.1 337.6,96.3 339.0,94.4 340.4,92.6 341.8,90.7 343.2,88.8 344.7,86.9 346.1,84.9 347.5,82.9 348.9,80.9 350.3,78.9 351.8,76.9 353.2,74.8 354.6,72.8 356.0,70.7 357.4,68.5 358.8,66.4 360.2,64.2 361.7,62.0 363.1,59.8 364.5,57.6 365.9,55.4 367.3,53.1 368.8,50.8 370.2,48.5 371.6,46.1 373.0,43.8 374.4,41.4 375.8,39.0 377.2,36.5 378.7,34.1 380.1,31.6 381.5,29.1 382.9,26.6 384.3,24.0 385.8,21.5 387.2,18.9 388.6,16.3"/><line class="curve3" stroke-dasharray="5 4" x1="220.0" y1="210.0" x2="220.0" y2="172.0"/><circle class="dot2" cx="220.0" cy="172.0" r="5"/><text class="ink" x="230.0" y="190.0" font-size="11" text-anchor="start">en küçük: w = 0,6, SSE = 2,4</text><text class="dim" x="50.0" y="224.0" font-size="9" text-anchor="middle">−0,4</text><text class="dim" x="118.0" y="224.0" font-size="9" text-anchor="middle">0,0</text><text class="dim" x="186.0" y="224.0" font-size="9" text-anchor="middle">0,4</text><text class="dim" x="254.0" y="224.0" font-size="9" text-anchor="middle">0,8</text><text class="dim" x="322.0" y="224.0" font-size="9" text-anchor="middle">1,2</text><text class="dim" x="390.0" y="224.0" font-size="9" text-anchor="middle">1,6</text><text class="dim" x="390.0" y="238.0" font-size="10" text-anchor="end">eğim w</text><text class="dim" x="126.0" y="18.0" font-size="10" text-anchor="start">SSE(w)</text></svg>
  <figcaption>Her eğim için en iyi kesişim seçilince SSE eğimin ikinci dereceden bir fonksiyonu: 6 − 12w + 10w². Dışbükey bir parabol; tek bir en küçük noktası var, w = 0,6.</figcaption>
</figure>

SSE dışbükey olduğu için türevin sıfır olduğu nokta tek ve en küçüktür.

## Kalıntılar ve R²

Örnekte kalıntılar $-0{,}8$, $0{,}6$, $1$, $-0{,}6$, $-0{,}2$; toplamları
$0$ (birinci denklem tam bunu söylüyor). $\text{SSE} = 2{,}4$.

Hiç özellik kullanmayan model hep $\bar{y}$'yi tahmin eder; onun hatası
**toplam kareler** $\text{SST} = \sum(y_i - \bar{y})^2 = 6$.

$$
R^2 = 1 - \frac{\text{SSE}}{\text{SST}} = 1 - \frac{2{,}4}{6} = 0{,}6
$$

Modelin, $y$'nin varyansının yüzde $60$'ını açıkladığı söylenir. Tek
özellikli regresyonda $R^2 = r^2$: $0{,}775^2 \approx 0{,}6$.

## Matris biçimi

$d$ özellik ve $n$ gözlem için başına bir $1$ sütunu eklenmiş
$n \times (d + 1)$ tasarım matrisi $X$, ağırlık vektörü $w$ (ilk elemanı
kesişim):

$$
\hat{y} = Xw \qquad \text{SSE}(w) = \lVert y - Xw \rVert^2
$$

Gradyan: $\nabla_w \text{SSE} = -2X^\mathsf{T}(y - Xw)$. Sıfıra
eşitleyince **normal denklemler**:

$$
X^\mathsf{T}X \, w = X^\mathsf{T}y \qquad \Rightarrow \qquad w = (X^\mathsf{T}X)^{-1} X^\mathsf{T}y
$$

**Örnek (aynı veri).**

$$
X^\mathsf{T}X = \begin{pmatrix} 5 & 15 \\ 15 & 55 \end{pmatrix} \qquad
X^\mathsf{T}y = \begin{pmatrix} 20 \\ 66 \end{pmatrix}
$$

Determinant $5 \cdot 55 - 15^2 = 50$. Ters matrisle:

$$
w = \frac{1}{50}\begin{pmatrix} 55 & -15 \\ -15 & 5 \end{pmatrix}\begin{pmatrix} 20 \\ 66 \end{pmatrix} = \begin{pmatrix} 2{,}2 \\ 0{,}6 \end{pmatrix}
$$

## Geometri: dik izdüşüm

$Xw$, $X$'in sütunlarının bir doğrusal birleşimi; yani sütun uzayında bir
vektör. En küçük kareler, sütun uzayında $y$'ye **en yakın** vektörü
arıyor. En yakın nokta, $y$'den sütun uzayına inilen **dikmenin**
ayağıdır.

<figure class="fig">
<svg viewBox="0 0 420 260" width="420"><line class="curve3" x1="40.0" y1="240.0" x2="400.0" y2="60.0"/><text class="dim" x="400.0" y="50.0" font-size="10" text-anchor="end">X'in sütun uzayı</text><line class="curve" x1="40.0" y1="240.0" x2="195.0" y2="46.2"/><polygon class="dot" points="200.0,40.0 197.5,49.7 191.1,44.6"/><line class="curve4" x1="40.0" y1="240.0" x2="240.8" y2="139.6"/><polygon class="dot3" points="248.0,136.0 241.7,143.7 238.0,136.4"/><line class="curve2" stroke-dasharray="5 4" x1="200.0" y1="40.0" x2="248.0" y2="136.0"/><line class="line" x1="235.5" y1="142.3" x2="229.2" y2="129.7"/><line class="line" x1="229.2" y1="129.7" x2="241.7" y2="123.5"/><text class="ink" x="192.0" y="36.0" font-size="13" text-anchor="end">y</text><text class="ink" x="256.0" y="152.0" font-size="12" text-anchor="start">ŷ = Xw</text><text class="ink" x="234.0" y="88.0" font-size="12" text-anchor="start">e = y − ŷ</text><text class="dim" x="256.0" y="168.0" font-size="10" text-anchor="start">dik açı: Xᵀe = 0</text></svg>
  <figcaption>y vektörü sütun uzayının dışında. ŷ, y'nin sütun uzayına dik izdüşümü; kalıntı e = y − ŷ sütun uzayına dik. Sütun uzayındaki başka her nokta y'ye daha uzak.</figcaption>
</figure>

Diklik $X^\mathsf{T}e = 0$ demektir; normal denklemlerin kendisi. Bundan
iki sonuç çıkar:

- $1$ sütunu da $X$'te olduğu için kalıntıların toplamı $0$.
- Kalıntılar her özellikle ilişkisizdir; modelin yakalayabileceği doğrusal
  bir iz kalmamıştır.

## Olasılıkla bağlantı

$y_i = x_i^\mathsf{T}w + \varepsilon_i$, $\varepsilon_i \sim
\mathcal{N}(0, \sigma^2)$ bağımsız olsun. En Çok Olabilirlik bölümünde
gördüğümüz gibi NLL, sabit dışında
$\frac{1}{2\sigma^2}\lVert y - Xw \rVert^2$; yani **en küçük kareler
çözümü, normal gürültü altında MLE'dir.** Gürültü varyansının MLE'si
$\hat{\sigma}^2 = \frac{\text{SSE}}{n}$; yansız tahmin
$\frac{\text{SSE}}{n - d - 1}$.

## Pratikte

**Ters matris almak yerine.** $X^\mathsf{T}X$'i tersine çevirmek $d^3$ ile
büyür ve sayısal olarak hassastır. Kütüphaneler QR ayrışımı ya da SVD
(sözde ters) kullanır. Veri çok büyükse Gradyan İnişi bölümündeki gibi
adım adım ilerlenir; SSE dışbükey olduğu için gradyan inişi aynı çözüme
varır.

**Çoklu doğrusallık.** İki özellik neredeyse aynıysa $X^\mathsf{T}X$'in
determinantı sıfıra yaklaşır; ters matris dev sayılar içerir, küçük bir
veri değişikliği katsayıları altüst eder.

**Ridge regresyon.** Kayba $\lambda\lVert w \rVert^2$ cezası eklenir:

$$
w = (X^\mathsf{T}X + \lambda I)^{-1} X^\mathsf{T}y
$$

$\lambda > 0$ iken matris her zaman terslenebilir; katsayılar küçülür ve
kararlı olur. Olasılık dilinde bu, ağırlıklara "sıfır çevresinde normal"
önseli koyup MAP kestirimi yapmaktır. (Uygulamada kesişim genellikle
cezalandırılmaz.)

**Katsayıları yorumlamak.** Çok özellikli modelde $w_j$, **öteki
özellikler sabitken** $x_j$'deki bir birimlik artışın $\hat{y}$'yi ne kadar
değiştirdiğidir. Özellikler farklı ölçeklerdeyse katsayılar
karşılaştırılamaz; önce standartlaştırılır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>kalıntıların mutlak değerleri toplanır</p>
      <p>1 sütunu olmadan X</p>
      <p>y'yi x'e ya da x'i y'ye oturtmak aynı doğruyu verir</p>
      <p>yüksek R², öyleyse neden-sonuç</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>kareleri toplanır; türev alınabilir, çözüm tek</p>
      <p>kesişim için başa 1 sütunu eklenir</p>
      <p>ikisi farklı eğimler verir; hangisinin tahmin edildiği önemli</p>
      <p>R² uyumu ölçer, nedenselliği değil</p>
    </div>
  </div>
  <figcaption>En küçük kareler dikey uzaklıkları, yani y yönündeki hataları küçültür.</figcaption>
</figure>

- **Veri aralığının dışına çıkmak.** Doğru, verinin görüldüğü aralıkta
  sınandı; $x = 100$'de ne olacağı hakkında hiçbir şey söylemez.

## Özet

- Model $\hat{y} = Xw$; kayıp $\text{SSE} = \lVert y - Xw \rVert^2$.
- Tek özellikte $w = \frac{s_{xy}}{s_x^2}$, $b = \bar{y} - w\bar{x}$; doğru
  $(\bar{x}, \bar{y})$'den geçer.
- Normal denklemler $X^\mathsf{T}Xw = X^\mathsf{T}y$; çözüm
  $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$.
- Geometrik olarak $\hat{y}$, $y$'nin sütun uzayına dik izdüşümü;
  $X^\mathsf{T}e = 0$.
- $R^2 = 1 - \frac{\text{SSE}}{\text{SST}}$; tek özellikte $r^2$.
- Normal gürültü altında en küçük kareler MLE'dir; ridge, önsel eklenmiş
  hâlidir.
