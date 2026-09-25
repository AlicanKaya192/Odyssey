# Kısmi Türev ve Gradyan

Şimdiye kadar tek girdili fonksiyonlarla çalıştık: bir ağırlık, bir kayıp.
Gerçek bir modelin ise binlerce, hatta milyarlarca ağırlığı var ve kayıp
hepsine birden bağlı. "Kaybı azaltmak için hangi ağırlığı ne yöne
itmeliyim?" sorusunun cevabı tek bir türev değil, her ağırlık için bir
türevden oluşan bir vektör: **gradyan**.

Bu bölümde çok değişkenli fonksiyonları, kısmi türevi, gradyanı ve
gradyanın neden "en dik çıkış yönünü" gösterdiğini göreceğiz.

Ön bilgi: Türev Kuralları bölümü, doğrusal cebirde Vektörler ile Nokta
Çarpımı bölümleri.

## Çok değişkenli fonksiyonlar

$f(x, y) = x^2 + 2y^2$ iki girdi alıp bir sayı veriyor. Grafiği bir yüzey:
her $(x, y)$ noktasının üstünde $f(x, y)$ yüksekliğinde bir nokta. Bu
yüzeyi kâğıtta göstermenin en pratik yolu haritalardaki **eş yükselti
eğrileri**: $f$'nin aynı değeri aldığı noktaları birleştiren eğriler.

<figure class="fig">
<svg viewBox="0 0 420 322" width="420"><line class="grid" x1="60.0" y1="270.0" x2="60.0" y2="20.0"/><line class="grid" x1="110.0" y1="270.0" x2="110.0" y2="20.0"/><line class="grid" x1="160.0" y1="270.0" x2="160.0" y2="20.0"/><line class="grid" x1="210.0" y1="270.0" x2="210.0" y2="20.0"/><line class="grid" x1="260.0" y1="270.0" x2="260.0" y2="20.0"/><line class="grid" x1="310.0" y1="270.0" x2="310.0" y2="20.0"/><line class="grid" x1="360.0" y1="270.0" x2="360.0" y2="20.0"/><line class="grid" x1="40.0" y1="245.0" x2="380.0" y2="245.0"/><line class="grid" x1="40.0" y1="195.0" x2="380.0" y2="195.0"/><line class="grid" x1="40.0" y1="145.0" x2="380.0" y2="145.0"/><line class="grid" x1="40.0" y1="95.0" x2="380.0" y2="95.0"/><line class="grid" x1="40.0" y1="45.0" x2="380.0" y2="45.0"/><line class="line" x1="40.0" y1="145.0" x2="380.0" y2="145.0"/><line class="line" x1="210.0" y1="270.0" x2="210.0" y2="20.0"/><text class="dim" x="60.0" y="158.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="110.0" y="158.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="160.0" y="158.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="260.0" y="158.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="310.0" y="158.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="360.0" y="158.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="205.0" y="248.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="205.0" y="198.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="205.0" y="98.0" font-size="9" text-anchor="end">1</text><text class="dim" x="205.0" y="48.0" font-size="9" text-anchor="end">2</text><polyline class="curve" fill="none" points="260.0,145.0 259.7,141.3 258.9,137.6 257.6,134.1 255.7,130.6 253.3,127.3 250.5,124.2 247.2,121.3 243.5,118.7 239.4,116.4 235.0,114.4 230.3,112.7 225.5,111.4 220.4,110.4 215.2,109.8 210.0,109.6 204.8,109.8 199.6,110.4 194.5,111.4 189.7,112.7 185.0,114.4 180.6,116.4 176.5,118.7 172.8,121.3 169.5,124.2 166.7,127.3 164.3,130.6 162.4,134.1 161.1,137.6 160.3,141.3 160.0,145.0 160.3,148.7 161.1,152.4 162.4,155.9 164.3,159.4 166.7,162.7 169.5,165.8 172.8,168.7 176.5,171.3 180.6,173.6 185.0,175.6 189.7,177.3 194.5,178.6 199.6,179.6 204.8,180.2 210.0,180.4 215.2,180.2 220.4,179.6 225.5,178.6 230.3,177.3 235.0,175.6 239.4,173.6 243.5,171.3 247.2,168.7 250.5,165.8 253.3,162.7 255.7,159.4 257.6,155.9 258.9,152.4 259.7,148.7 260.0,145.0"/><polyline class="curve" fill="none" points="280.7,145.0 280.3,139.8 279.2,134.6 277.2,129.5 274.6,124.7 271.2,120.0 267.2,115.6 262.5,111.5 257.3,107.8 251.6,104.5 245.4,101.7 238.8,99.3 231.9,97.4 224.7,96.1 217.4,95.3 210.0,95.0 202.6,95.3 195.3,96.1 188.1,97.4 181.2,99.3 174.6,101.7 168.4,104.5 162.7,107.8 157.5,111.5 152.8,115.6 148.8,120.0 145.4,124.7 142.8,129.5 140.8,134.6 139.7,139.8 139.3,145.0 139.7,150.2 140.8,155.4 142.8,160.5 145.4,165.3 148.8,170.0 152.8,174.4 157.5,178.5 162.7,182.2 168.4,185.5 174.6,188.3 181.2,190.7 188.1,192.6 195.3,193.9 202.6,194.7 210.0,195.0 217.4,194.7 224.7,193.9 231.9,192.6 238.8,190.7 245.4,188.3 251.6,185.5 257.3,182.2 262.5,178.5 267.2,174.4 271.2,170.0 274.6,165.3 277.2,160.5 279.2,155.4 280.3,150.2 280.7,145.0"/><polyline class="curve" fill="none" points="310.0,145.0 309.5,137.6 307.8,130.3 305.1,123.1 301.4,116.2 296.6,109.6 290.9,103.4 284.3,97.7 276.9,92.5 268.8,87.8 260.0,83.8 250.7,80.4 240.9,77.8 230.8,75.8 220.5,74.7 210.0,74.3 199.5,74.7 189.2,75.8 179.1,77.8 169.3,80.4 160.0,83.8 151.2,87.8 143.1,92.5 135.7,97.7 129.1,103.4 123.4,109.6 118.6,116.2 114.9,123.1 112.2,130.3 110.5,137.6 110.0,145.0 110.5,152.4 112.2,159.7 114.9,166.9 118.6,173.8 123.4,180.4 129.1,186.6 135.7,192.3 143.1,197.5 151.2,202.2 160.0,206.2 169.3,209.6 179.1,212.2 189.2,214.2 199.5,215.3 210.0,215.7 220.5,215.3 230.8,214.2 240.9,212.2 250.7,209.6 260.0,206.2 268.8,202.2 276.9,197.5 284.3,192.3 290.9,186.6 296.6,180.4 301.4,173.8 305.1,166.9 307.8,159.7 309.5,152.4 310.0,145.0"/><polyline class="curve" fill="none" points="332.5,145.0 331.8,135.9 329.8,127.0 326.5,118.2 321.9,109.8 316.1,101.7 309.1,94.1 301.0,87.1 292.0,80.6 282.0,74.9 271.2,70.0 259.8,65.9 247.8,62.6 235.5,60.3 222.8,58.9 210.0,58.4 197.2,58.9 184.5,60.3 172.2,62.6 160.2,65.9 148.8,70.0 138.0,74.9 128.0,80.6 119.0,87.1 110.9,94.1 103.9,101.7 98.1,109.8 93.5,118.2 90.2,127.0 88.2,135.9 87.5,145.0 88.2,154.1 90.2,163.0 93.5,171.8 98.1,180.2 103.9,188.3 110.9,195.9 119.0,202.9 128.0,209.4 138.0,215.1 148.8,220.0 160.2,224.1 172.2,227.4 184.5,229.7 197.2,231.1 210.0,231.6 222.8,231.1 235.5,229.7 247.8,227.4 259.8,224.1 271.2,220.0 282.0,215.1 292.0,209.4 301.0,202.9 309.1,195.9 316.1,188.3 321.9,180.2 326.5,171.8 329.8,163.0 331.8,154.1 332.5,145.0"/><line class="curve2" x1="310.0" y1="145.0" x2="338.6" y2="145.0"/><polygon class="dot2" points="345.0,145.0 337.7,148.3 337.7,141.7"/><circle class="dot2" cx="310.0" cy="145.0" r="3.5"/><line class="curve2" x1="310.0" y1="95.0" x2="330.2" y2="74.8"/><polygon class="dot2" points="334.7,70.3 331.8,77.8 327.2,73.2"/><circle class="dot2" cx="310.0" cy="95.0" r="3.5"/><line class="curve2" x1="139.3" y1="95.0" x2="122.8" y2="71.6"/><polygon class="dot2" points="119.1,66.4 126.0,70.5 120.6,74.2"/><circle class="dot2" cx="139.3" cy="95.0" r="3.5"/><line class="curve2" x1="210.0" y1="215.7" x2="210.0" y2="244.3"/><polygon class="dot2" points="210.0,250.7 206.7,243.4 213.3,243.4"/><circle class="dot2" cx="210.0" cy="215.7" r="3.5"/><line class="curve2" x1="110.0" y1="195.0" x2="89.8" y2="215.2"/><polygon class="dot2" points="85.3,219.7 88.2,212.2 92.8,216.8"/><circle class="dot2" cx="110.0" cy="195.0" r="3.5"/><text class="ink" x="45.0" y="35.0" font-size="12" text-anchor="start">f(x, y) = x² + 2y²</text><text class="dim" x="210" y="294" font-size="11" text-anchor="middle">eş yükselti eğrileri f = 1, 2, 4, 6</text><text class="dim" x="210" y="312" font-size="11" text-anchor="middle">gradyan: en dik çıkış yönü, eğriye dik</text></svg>
  <figcaption>f(x, y) = x² + 2y² yüzeyinin eş yükselti eğrileri: iç içe elipsler, merkezde en küçük değer. Turuncu oklar birkaç noktadaki gradyan; her biri o noktadan geçen eğriye dik ve dışarı, yükselişe doğru bakıyor.</figcaption>
</figure>

Eğrilerin sık olduğu yerde yüzey dik, seyrek olduğu yerde yatık.

## Kısmi türev

Birden fazla değişken varsa türevi **bir değişkene göre** alırız; öteki
değişkenleri sabit sayı gibi tutarak. Buna **kısmi türev** denir ve
$\partial$ ("kısmi d") ile yazılır:

$$
\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x + h, y) - f(x, y)}{h}
$$

Örnek: $f(x, y) = x^2 y + 3y$.

- $x$'e göre ($y$ sabit): $\dfrac{\partial f}{\partial x} = 2xy$. ($3y$ sabit, türevi $0$.)
- $y$'ye göre ($x$ sabit): $\dfrac{\partial f}{\partial y} = x^2 + 3$.

**Geometrik anlamı.** $y$'yi sabit tutmak, yüzeyi $y$'nin sabit olduğu bir
düzlemle kesmek demek; kesit tek değişkenli bir eğri. $\frac{\partial f}{\partial x}$
o eğrinin eğimi: doğu yönünde bir adım atınca yükseklik ne kadar değişir?

Kısaltmalar: $f_x$, $f_y$ ya da $\partial_x f$.

## Gradyan

Bütün kısmi türevleri bir vektörde topla:

$$
\nabla f = \left( \frac{\partial f}{\partial x}, \ \frac{\partial f}{\partial y} \right)
$$

$\nabla$ "nabla" diye okunur. $n$ değişkende gradyan $n$ bileşenli bir
vektör. Örnek: $f = x^2 + 2y^2$ için $\nabla f = (2x, 4y)$; $(1, 1)$
noktasında $(2, 4)$.

**Gradyan bir noktaya bağlı bir vektör:** her noktada farklı. Şekildeki
oklar tam olarak bu: her noktaya o noktanın gradyanı çizilmiş.

## Gradyan neden en dik yönü gösterir?

$(x, y)$'den birim vektör $\mathbf{u}$ yönünde küçük bir adım atalım.
Yükseklikteki değişim hızı **yönlü türev**:

$$
D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \lVert \nabla f \rVert \cos \theta
$$

($\theta$, $\nabla f$ ile $\mathbf{u}$ arasındaki açı; nokta çarpımı
bölümündeki formül.)

<figure class="fig">
<svg viewBox="0 0 400 299" width="400"><line class="grid" x1="40.0" y1="245.0" x2="40.0" y2="20.0"/><line class="grid" x1="77.5" y1="245.0" x2="77.5" y2="20.0"/><line class="grid" x1="115.0" y1="245.0" x2="115.0" y2="20.0"/><line class="grid" x1="152.5" y1="245.0" x2="152.5" y2="20.0"/><line class="grid" x1="190.0" y1="245.0" x2="190.0" y2="20.0"/><line class="grid" x1="227.5" y1="245.0" x2="227.5" y2="20.0"/><line class="grid" x1="265.0" y1="245.0" x2="265.0" y2="20.0"/><line class="grid" x1="302.5" y1="245.0" x2="302.5" y2="20.0"/><line class="grid" x1="340.0" y1="245.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="245.0" x2="340.0" y2="245.0"/><line class="grid" x1="40.0" y1="207.5" x2="340.0" y2="207.5"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="40.0" y1="132.5" x2="340.0" y2="132.5"/><line class="grid" x1="40.0" y1="95.0" x2="340.0" y2="95.0"/><line class="grid" x1="40.0" y1="57.5" x2="340.0" y2="57.5"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="curve" x1="77.5" y1="207.5" x2="294.6" y2="98.9"/><polygon class="dot" points="302.5,95.0 295.5,103.5 291.5,95.5"/><line class="curve2" x1="77.5" y1="207.5" x2="119.3" y2="95.5"/><polygon class="dot2" points="122.1,88.0 122.7,98.0 115.1,95.1"/><polyline class="curve3" fill="none" points="117.7,187.4 117.0,185.9 116.1,184.4 115.2,183.0 114.3,181.6 113.3,180.2 112.2,178.9 111.1,177.6 110.0,176.4 108.8,175.2 107.6,174.0 106.3,172.9 105.0,171.9 103.6,170.9 102.2,169.9 100.8,169.0 99.4,168.2 97.9,167.4 96.3,166.6 94.8,166.0 93.2,165.3"/><text class="ink" x="117.6" y="166.9" font-size="13" text-anchor="middle">θ</text><line class="curve3" stroke-dasharray="5 4" x1="122.1" y1="88.0" x2="160.9" y2="165.8"/><text class="ink" x="310.5" y="99.0" font-size="14" text-anchor="start">∇f</text><text class="ink" x="116.1" y="82.0" font-size="12" text-anchor="end">u (birim yön)</text><text class="ink" x="190" y="269" font-size="12" text-anchor="middle">u yönünde değişim hızı = ‖∇f‖ cos θ</text><text class="dim" x="190" y="289" font-size="10.5" text-anchor="middle">θ = 0: en hızlı artış; θ = 90°: değişim yok; θ = 180°: en hızlı azalış</text></svg>
  <figcaption>Yönlü türev, u'nun gradyan üzerine izdüşümünün uzunluğu kadar. Açı küçüldükçe büyüyor; u gradyanla aynı yöne bakınca en büyük değerine, ‖∇f‖'ye ulaşıyor.</figcaption>
</figure>

$\cos \theta$ en fazla $1$ olduğundan:

- **$\theta = 0$**: $\mathbf{u}$ gradyan yönünde; artış en hızlı ve hızı $\lVert \nabla f \rVert$.
- **$\theta = 180°$**: gradyanın tersi; **en hızlı azalış**. Gradyan inişinin gittiği yön.
- **$\theta = 90°$**: değişim yok; bu yön eş yükselti eğrisi boyunca. Bu yüzden gradyan eş yükselti eğrilerine **diktir**.

## Gradyanın sıfır olduğu yerler

Tek değişkende $f' = 0$ yatay teğet demekti; çok değişkende $\nabla f =
\mathbf{0}$ **yatay teğet düzlem** demek. Böyle bir nokta üç türlü olabilir:

| Nokta | Örnek | Görünüm |
|---|---|---|
| yerel en küçük | $x^2 + y^2$, $(0, 0)$ | çanak |
| yerel en büyük | $-x^2 - y^2$, $(0, 0)$ | tepe |
| **eyer noktası** | $x^2 - y^2$, $(0, 0)$ | bir yönde çanak, öbür yönde tümsek |

Eyer noktası tek değişkende olmayan bir şey: at eyeri gibi, $x$ yönünde
dip, $y$ yönünde tepe. Hangisi olduğunu ikinci kısmi türevler söyler.

**İkinci kısmi türevler.** $f_{xx} = \frac{\partial^2 f}{\partial x^2}$,
$f_{yy}$ ve karışık türev $f_{xy} = \frac{\partial^2 f}{\partial x \, \partial y}$.
Düzgün fonksiyonlarda sıra önemli değil: $f_{xy} = f_{yx}$. Bunların
oluşturduğu matris (Hessian) bir sonraki bölümün konusu.

## Makine öğrenmesinde gradyan

**Doğrusal modelin gradyanı.** $\hat{y} = w_1 x_1 + w_2 x_2 + b$, tek
bir örnekte kayıp $L = (\hat{y} - y)^2$. Zincir kuralıyla her ağırlığa
göre:

$$
\frac{\partial L}{\partial w_j} = 2(\hat{y} - y) \, x_j, \qquad \frac{\partial L}{\partial b} = 2(\hat{y} - y)
$$

Vektör olarak: $\nabla_{\mathbf{w}} L = 2(\hat{y} - y) \, \mathbf{x}$. Hata
büyükse ve özellik büyükse o ağırlığın gradyanı da büyük.

**Gradyan inişi.** Kaybı azaltmak için en hızlı azalış yönüne, gradyanın
tersine bir adım:

$$
\mathbf{w} \leftarrow \mathbf{w} - \eta \, \nabla L(\mathbf{w})
$$

Tek değişkendeki $w \leftarrow w - \eta L'(w)$ ile aynı fikir; artık her
ağırlık kendi kısmi türeviyle aynı anda güncelleniyor. Gradyan İnişi
bölümünde ayrıntısıyla göreceğiz.

**Özellik ölçekleme.** Şekildeki elipsler uzundu çünkü $y$ yönünde
fonksiyon daha dik ($2y^2$). Özelliklerin ölçekleri çok farklıysa kaybın
eş yükselti eğrileri çok basık elipsler olur; gradyan merkeze değil
yan duvara bakar ve iniş zikzak çizer. Özellikleri aynı ölçeğe getirmek
eğrileri daireye yaklaştırır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\dfrac{\partial}{\partial x}(x^2 y) = 2x$</p>
      <p>$\dfrac{\partial}{\partial x}(3y) = 3$</p>
      <p>Gradyan bir sayıdır</p>
      <p>Gradyan en küçüğe doğru bakar</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$2xy$: $y$ sabit çarpan olarak kalır</p>
      <p>$0$: $y$ sabitse $3y$ de sabit</p>
      <p>Her değişken için bir bileşenli vektör</p>
      <p>En hızlı artışa bakar; iniş tersine gider</p>
    </div>
  </div>
  <figcaption>Kısmi türevde öteki değişkenler sayı gibi davranır: çarpan olarak kalır, tek başınaysa türevi sıfır olur.</figcaption>
</figure>

## Özet

- Çok değişkenli fonksiyonun grafiği bir yüzey; eş yükselti eğrileri haritası.
- Kısmi türev: öteki değişkenler sabit tutularak alınan türev, $\frac{\partial f}{\partial x}$.
- Gradyan $\nabla f = (f_x, f_y, \ldots)$: kısmi türevlerin vektörü.
- Yönlü türev $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$; en büyük gradyan yönünde, değeri $\lVert \nabla f \rVert$.
- Gradyan en dik çıkış yönü ve eş yükselti eğrilerine dik; tersi en dik iniş.
- $\nabla f = \mathbf{0}$: en küçük, en büyük ya da eyer noktası.
- Doğrusal model: $\nabla_{\mathbf{w}} L = 2(\hat{y} - y)\mathbf{x}$; gradyan inişi $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$.
