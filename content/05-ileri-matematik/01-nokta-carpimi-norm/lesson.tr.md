# Nokta Çarpımı, Uzunluk ve Benzerlik

Bir müzik uygulaması sana yeni bir şarkı önerirken, bir arama motoru
sorgunla en ilgili sayfayı seçerken ya da bir dil modeli bir kelimenin
cümledeki hangi kelimelerle ilgili olduğuna karar verirken aynı soruyu
soruyor: **bu iki vektör birbirine ne kadar benziyor?**

Bu sorunun matematiksel cevabı **nokta çarpımı**. İki vektörü alıp tek
bir sayı üreten basit bir işlem; ama o sayı iki vektörün aynı yöne ne
kadar baktığını söylüyor. Bu bölümde nokta çarpımını, iki vektör
arasındaki açıyı, izdüşümü, kosinüs benzerliğini ve farklı uzunluk
ölçülerini (normları) göreceğiz.

Ön bilgi: bir önceki bölüm (Vektörler) ve **kosinüs**. Kosinüs MAT 1'in
Trigonometri bölümünde ayrıntılı anlatılıyor; burada ihtiyacımız olan
kısmını kısaca hatırlatacağım.

## Tanım: çarp ve topla

İki vektörün **nokta çarpımı**, karşılıklı bileşenlerin çarpımlarının
toplamıdır:

$$
\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2
$$

**Örnek:** $\mathbf{a} = (3, 4)$ ve $\mathbf{b} = (2, 1)$ için

$$
\mathbf{a} \cdot \mathbf{b} = 3 \cdot 2 + 4 \cdot 1 = 6 + 4 = 10
$$

Sonuç bir **vektör değil, tek bir sayı** (skaler). Bu yüzden nokta
çarpımına **skaler çarpım** da denir. Vektörle skaleri çarpmak (önceki
bölüm) ile iki vektörün nokta çarpımını karıştırma: birincisinin sonucu
vektör, ikincisininki sayı.

Boyut kaç olursa olsun tanım aynı; çarpımların hepsi toplanır:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i
\qquad
(1, 2, 3) \cdot (4, -5, 6) = 4 - 10 + 18 = 12
$$

İki vektör **aynı boyutta** olmalı; yoksa bazı bileşenlerin eşi kalmaz.

### Özellikler

| Özellik | Yazılış |
|---|---|
| Değişme | $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$ |
| Dağılma | $\mathbf{a} \cdot (\mathbf{b} + \mathbf{c}) = \mathbf{a} \cdot \mathbf{b} + \mathbf{a} \cdot \mathbf{c}$ |
| Skaler dışarı çıkar | $(k\,\mathbf{a}) \cdot \mathbf{b} = k\,(\mathbf{a} \cdot \mathbf{b})$ |
| Kendisiyle çarpım | $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2$ |

Son satır önemli: bir vektörün kendisiyle nokta çarpımı, uzunluğunun
karesi. $(3, 4) \cdot (3, 4) = 9 + 16 = 25 = 5^2$. Yani uzunluk nokta
çarpımıyla yazılabiliyor:

$$
\|\mathbf{a}\| = \sqrt{\mathbf{a} \cdot \mathbf{a}}
$$

## Kosinüsü hatırlayalım

Nokta çarpımının geometrik anlamı için bir açının **kosinüsüne** ihtiyacımız
var. Merkezi orijinde, yarıçapı 1 olan bir çember düşün (birim çember).
Pozitif $x$ ekseninden $\theta$ açısı kadar dönünce çemberde vardığın
noktanın **$x$ koordinatı**, $\cos \theta$'dır.

| Açı $\theta$ | $0°$ | $60°$ | $90°$ | $120°$ | $180°$ |
|---|---|---|---|---|---|
| $\cos \theta$ | $1$ | $0.5$ | $0$ | $-0.5$ | $-1$ |

Bilmemiz gereken üç şey:

- Açı $0°$ iken kosinüs en büyük değeri $1$'i alır.
- Açı $90°$'yi geçince kosinüs **negatife** döner; $90°$'de tam $0$.
- Kosinüs her zaman $-1$ ile $1$ arasındadır.

## Geometrik anlam: açı

İki vektör arasındaki açıya $\theta$ dersek:

$$
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\,\cos \theta
$$

<figure class="fig">
<svg viewBox="0 0 292 252" width="292"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="line" x1="66" y1="226" x2="66" y2="26"/><line class="grid" x1="106" y1="226" x2="106" y2="26"/><line class="grid" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="266" y1="226" x2="266" y2="26"/><line class="grid" x1="26" y1="226" x2="266" y2="226"/><line class="line" x1="26" y1="186" x2="266" y2="186"/><line class="grid" x1="26" y1="146" x2="266" y2="146"/><line class="grid" x1="26" y1="106" x2="266" y2="106"/><line class="grid" x1="26" y1="66" x2="266" y2="66"/><line class="grid" x1="26" y1="26" x2="266" y2="26"/><text class="dim" x="26" y="200" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="200" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="200" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="200" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="200" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="200" font-size="10" text-anchor="middle">5</text><text class="dim" x="60" y="230" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">4</text><path class="curve3" d="M108.7,175.3 L108.2,173.6 L107.6,171.8 L107.0,170.1 L106.3,168.4 L105.5,166.7 L104.7,165.1 L103.8,163.5 L102.8,161.9 L101.8,160.4 L100.7,158.9 L99.5,157.5 L98.3,156.1 L97.0,154.8 L95.7,153.5 L94.3,152.3 L92.9,151.1 L91.4,150.1 L89.8,149.0 L88.3,148.1 L86.7,147.2 L85.0,146.3 L83.4,145.6 L81.6,144.9 L79.9,144.3"/><line class="curve" x1="66" y1="186" x2="217.5" y2="148.1"/><polygon class="dot" points="226,146 217.3,152.8 215.2,144.1"/><line class="curve2" x1="66" y1="186" x2="103.2" y2="74.3"/><polygon class="dot2" points="106,66 107.1,76.9 98.6,74.1"/><text class="ink" x="111.5" y="148.9" font-size="15" text-anchor="middle">θ</text><text class="ink" x="232" y="150" font-size="14" text-anchor="start">a</text><text class="ink" x="112" y="66" font-size="14" text-anchor="start">b</text></svg>
  <figcaption>Mor $\mathbf{a} = (4, 1)$ ile turuncu $\mathbf{b} = (1, 3)$ arasındaki açı $\theta$. Nokta çarpımı bu açıyı iki vektörün uzunluklarıyla birlikte tek bir sayıda topluyor.</figcaption>
</figure>

Bir yanda bileşenlerle yapılan basit bir hesap ($a_1 b_1 + a_2 b_2$),
öbür yanda uzunluklar ve açı. İkisinin eşit olması hiç de açık değil;
nereden geldiğine bakalım.

### Neden doğru?

**Kosinüs teoremi**, Pisagor teoreminin dik olmayan üçgenlere
genellenmiş hâli. Kenarları $a$, $b$ ve aralarındaki açı $\theta$ olan
bir üçgende üçüncü kenar $c$ için:

$$
c^2 = a^2 + b^2 - 2ab\cos\theta
$$

$\theta = 90°$ ise $\cos\theta = 0$ ve formül Pisagor'a döner:
$c^2 = a^2 + b^2$.

Şimdi $\mathbf{a}$ ve $\mathbf{b}$ vektörlerinden bir üçgen kur. Üçüncü
kenar, iki ucu birleştiren $\mathbf{a} - \mathbf{b}$ vektörü. Kosinüs
teoremi:

$$
\|\mathbf{a} - \mathbf{b}\|^2 = \|\mathbf{a}\|^2 + \|\mathbf{b}\|^2 - 2\,\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

Sol tarafı nokta çarpımının kurallarıyla açalım
($\|\mathbf{v}\|^2 = \mathbf{v} \cdot \mathbf{v}$ ve dağılma):

$$
(\mathbf{a} - \mathbf{b}) \cdot (\mathbf{a} - \mathbf{b})
= \mathbf{a} \cdot \mathbf{a} - 2\,\mathbf{a} \cdot \mathbf{b} + \mathbf{b} \cdot \mathbf{b}
= \|\mathbf{a}\|^2 - 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2
$$

İki ifade eşit. $\|\mathbf{a}\|^2$ ve $\|\mathbf{b}\|^2$ iki tarafta da
var ve birbirini götürüyor:

$$
-2\,\mathbf{a} \cdot \mathbf{b} = -2\,\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
\quad\Rightarrow\quad
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

Bileşenlerle yapılan basit çarp-topla işlemi, açıyı gizli olarak içinde
taşıyor.

## İşaret ne söyler?

Uzunluklar hiç negatif olmadığı için nokta çarpımının **işaretini**
yalnızca $\cos\theta$ belirler:

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Pozitif: dar açı</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M147.6,115.6 L147.5,115.0 L147.3,114.5 L147.1,113.9 L146.9,113.3 L146.7,112.8 L146.5,112.2 L146.3,111.7 L146.1,111.1 L145.8,110.6 L145.5,110.0 L145.3,109.5 L145.0,109.0 L144.7,108.5 L144.4,108.0 L144.0,107.5 L143.7,107.0 L143.4,106.5 L143.0,106.0 L142.6,105.5 L142.3,105.1 L141.9,104.6 L141.5,104.2 L141.1,103.8 L140.7,103.3"/><line class="curve" x1="122" y1="122" x2="209.5" y2="100.1"/><polygon class="dot" points="218,98 209.3,104.8 207.2,96.1"/><line class="curve2" x1="122" y1="122" x2="187.8" y2="56.2"/><polygon class="dot2" points="194,50 190.1,60.3 183.7,53.9"/></svg>
      <p>$\theta < 90°$. Vektörler kabaca aynı tarafa bakıyor.</p>
    </div>
    <div>
      <h4>Sıfır: dik</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M134.5,117.8 L130.3,105.3 L117.8,109.5"/><line class="curve" x1="122" y1="122" x2="185.7" y2="100.8"/><polygon class="dot" points="194,98 185.9,105.4 183.1,96.9"/><line class="curve2" x1="122" y1="122" x2="100.8" y2="58.3"/><polygon class="dot2" points="98,50 105.4,58.1 96.9,60.9"/></svg>
      <p>$\theta = 90°$. Vektörler birbirinden bağımsız yönlerde.</p>
    </div>
    <div>
      <h4>Negatif: geniş açı</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M147.0,113.7 L146.0,111.1 L144.8,108.7 L143.3,106.4 L141.5,104.2 L139.6,102.3 L137.4,100.6 L135.1,99.1 L132.7,97.9 L130.1,96.9 L127.5,96.2 L124.7,95.7 L122.0,95.6 L119.3,95.7 L116.5,96.2 L113.9,96.9 L111.3,97.9 L108.9,99.1 L106.6,100.6 L104.4,102.3 L102.5,104.2 L100.7,106.4 L99.2,108.7 L98.0,111.1 L97.0,113.7"/><line class="curve" x1="122" y1="122" x2="185.7" y2="100.8"/><polygon class="dot" points="194,98 185.9,105.4 183.1,96.9"/><line class="curve2" x1="122" y1="122" x2="58.3" y2="100.8"/><polygon class="dot2" points="50,98 60.9,96.9 58.1,105.4"/></svg>
      <p>$\theta > 90°$. Vektörler kabaca zıt yönlere bakıyor.</p>
    </div>
  </div>
  <figcaption>Nokta çarpımının işareti, iki vektörün arasındaki açının $90°$'den küçük mü büyük mü olduğunu söylüyor.</figcaption>
</figure>

Şekillerdeki vektörler: dar açıda $(4, 1) \cdot (3, 3) = 15$ (pozitif), dik açıda
$(3, 1) \cdot (-1, 3) = -3 + 3 = 0$, geniş açıda
$(3, 1) \cdot (-3, 1) = -9 + 1 = -8$ (negatif).

### Diklik

İki vektör **ancak ve ancak** nokta çarpımları sıfırsa diktir (sıfır
vektörü dışında):

$$
\mathbf{a} \perp \mathbf{b} \iff \mathbf{a} \cdot \mathbf{b} = 0
$$

Açı ölçmeden, çizmeden diklik kontrolü: $(2, 3) \cdot (-3, 2) = -6 + 6 = 0$,
yani dikler. Düzlemde bir $(p, q)$ vektörüne dik bir vektör bulmanın
pratik yolu bileşenlerin yerini değiştirip birinin işaretini çevirmek:
$(-q, p)$.

Makine öğrenmesinde dik vektörler "birbiri hakkında hiçbir şey söylemeyen"
yönleri temsil ediyor; PCA bölümünde birbirine dik yönler arayacağız.

## İki vektör arasındaki açıyı bulmak

Formülü $\cos\theta$ için çözersek:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

**Örnek:** $\mathbf{a} = (1, 0)$ ve $\mathbf{b} = (1, 1)$.

$$
\cos\theta = \frac{1 \cdot 1 + 0 \cdot 1}{1 \cdot \sqrt{2}} = \frac{1}{\sqrt{2}} \approx 0.707
\quad\Rightarrow\quad \theta = 45°
$$

Şekil bunu doğruluyor: $(1, 1)$ tam çapraz, $x$ ekseniyle $45°$ yapıyor.

**Örnek:** $\mathbf{a} = (3, 4)$, $\mathbf{b} = (2, 1)$.
$\mathbf{a} \cdot \mathbf{b} = 10$, $\|\mathbf{a}\| = 5$,
$\|\mathbf{b}\| = \sqrt{5} \approx 2.236$:

$$
\cos\theta = \frac{10}{5 \cdot 2.236} \approx 0.894
\quad\Rightarrow\quad \theta \approx 26.6°
$$

Kosinüsten açıya geçmek hesap makinesinin $\cos^{-1}$ (arccos)
tuşuyla yapılıyor. Çoğu zaman açının kendisine gerek yok: kosinüs değeri
zaten "ne kadar aynı yöne bakıyorlar" sorusunun cevabı.

## Cauchy–Schwarz eşitsizliği

Kosinüs $-1$ ile $1$ arasında olduğu için:

$$
|\mathbf{a} \cdot \mathbf{b}| \le \|\mathbf{a}\|\,\|\mathbf{b}\|
$$

Nokta çarpımının büyüklüğü, uzunlukların çarpımını **asla aşamaz**. Eşitlik
yalnızca iki vektör aynı ya da tam ters yöne baktığında oluyor
($\cos\theta = \pm 1$). Bu eşitsizlik, bir önceki bölümdeki üçgen
eşitsizliğinin de kanıtında kullanılıyor ve kosinüs benzerliğinin neden
her zaman $-1$ ile $1$ arasında çıktığını açıklıyor.

## İzdüşüm: bir vektörün öteki yöndeki payı

Güneş tam tepedeyken bir sopanın yere düşen gölgesini düşün. **İzdüşüm**,
bir vektörün başka bir vektörün yönündeki "gölgesi".

<figure class="fig">
<svg viewBox="0 0 292 292" width="292"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="26" y1="266" x2="266" y2="266"/><line class="line" x1="26" y1="226" x2="266" y2="226"/><line class="grid" x1="26" y1="186" x2="266" y2="186"/><line class="grid" x1="26" y1="146" x2="266" y2="146"/><line class="grid" x1="26" y1="106" x2="266" y2="106"/><line class="grid" x1="26" y1="66" x2="266" y2="66"/><line class="grid" x1="26" y1="26" x2="266" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve2" x1="66" y1="226" x2="219.8" y2="72.2"/><polygon class="dot2" points="226,66 222.1,76.3 215.7,69.9"/><line class="curve4" x1="66" y1="226" x2="139.8" y2="152.2"/><polygon class="dot3" points="146,146 142.1,156.3 135.7,149.9"/><line class="curve" x1="66" y1="226" x2="177.7" y2="188.8"/><polygon class="dot" points="186,186 177.9,193.4 175.1,184.9"/><line class="curve3" stroke-dasharray="5 4" x1="186" y1="186" x2="146" y2="146"/><path class="curve3" d="M137.5,154.5 L146.0,163.0 L154.5,154.5"/><text class="ink" x="192" y="190" font-size="14" text-anchor="start">a</text><text class="ink" x="232" y="66" font-size="14" text-anchor="start">b</text><text class="ink" x="136" y="140" font-size="12" text-anchor="end">izdüşüm</text></svg>
  <figcaption>Mor $\mathbf{a} = (3, 1)$'in turuncu $\mathbf{b} = (4, 4)$ doğrultusundaki izdüşümü yeşil $(2, 2)$. Kesik çizgi $\mathbf{b}$'ye dik iniyor.</figcaption>
</figure>

**Skaler izdüşüm** (gölgenin uzunluğu):

$$
\text{izd}_{\mathbf{b}}\,\mathbf{a} = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|}
= \|\mathbf{a}\|\cos\theta
$$

**Vektör izdüşüm** (gölgenin kendisi): bu uzunluğu $\mathbf{b}$ yönündeki
birim vektörle çarp:

$$
\text{izd}_{\mathbf{b}}\,\mathbf{a} = \frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}
$$

Şekildeki hesap: $\mathbf{a} \cdot \mathbf{b} = 12 + 4 = 16$,
$\mathbf{b} \cdot \mathbf{b} = 32$, dolayısıyla izdüşüm
$\frac{16}{32}(4, 4) = (2, 2)$. Uzunluğu $\sqrt{8} \approx 2.83$.

$\mathbf{b}$ birim vektörse işler çok sadeleşiyor: skaler izdüşüm doğrudan
$\mathbf{a} \cdot \mathbf{b}$. Örneğin $(4, 2)$'nin $x$ ekseni
($\mathbf{i} = (1, 0)$) üzerindeki izdüşümü $(4, 2) \cdot (1, 0) = 4$:
vektörün $x$ bileşeninin ta kendisi. **Bir vektörün bileşenleri, temel
birim vektörler üzerindeki izdüşümleridir.**

## Kosinüs benzerliği

Makine öğrenmesinde iki vektörün benzerliği çoğu zaman **açılarına**
bakılarak ölçülür, uzunluklarına değil:

$$
\text{benzerlik}(\mathbf{a}, \mathbf{b}) = \cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

Değer $1$'e yakınsa aynı yöne bakıyorlar (çok benzer), $0$ ise ilgisizler,
$-1$ ise zıtlar.

### Neden uzunluk değil de açı?

Üç belgeyi, içlerinde "futbol", "maç" ve "yemek" kelimelerinin kaç kez
geçtiğiyle vektör olarak yazalım:

| Belge | futbol | maç | yemek | Vektör |
|---|---|---|---|---|
| Kısa spor haberi | 2 | 1 | 0 | $(2, 1, 0)$ |
| Uzun spor haberi | 4 | 2 | 0 | $(4, 2, 0)$ |
| Yemek tarifi | 0 | 1 | 3 | $(0, 1, 3)$ |

İki spor haberi aynı konu; biri ötekinin iki katı uzun.

- **Öklid uzaklığı:** kısa haber ile uzun haber arasında $\sqrt{5} \approx 2.24$,
  kısa haber ile tarif arasında $\sqrt{13} \approx 3.61$. Uzaklık, iki
  spor haberini de birbirinden oldukça uzak görüyor.
- **Kosinüs benzerliği:** $(2, 1, 0)$ ile $(4, 2, 0)$ arasında **tam $1$**
  ($(4, 2, 0) = 2 \cdot (2, 1, 0)$, aynı yön). Kısa haber ile tarif
  arasında yalnızca $0.14$.

Kosinüs benzerliği belgenin **uzunluğunu** umursamıyor, yalnızca **neyden
bahsettiğine** (yönüne) bakıyor. Metin, öneri sistemleri ve kelime
gömmeleri için doğru ölçü çoğu zaman bu.

Aynı yöne bakan vektörleri önce birim vektöre çevirirsen (normalleştirme,
önceki bölüm) kosinüs benzerliği düz nokta çarpımına dönüşür; büyük
sistemler hesabı bu yüzden önce normalleştirip sonra nokta çarpımıyla
yapıyor.

## Uzunluğun farklı ölçüleri: normlar

Şimdiye kadar uzunluk için Pisagor'u kullandık. Bu, **birçok** uzunluk
ölçüsünden yalnızca biri; makine öğrenmesinde üçü sık geçiyor.

| Norm | Formül | $(3, -4)$ için | Adı |
|---|---|---|---|
| $L_2$ | $\sqrt{a_1^2 + a_2^2 + \cdots}$ | $5$ | Öklid uzunluğu |
| $L_1$ | $\lvert a_1\rvert + \lvert a_2\rvert + \cdots$ | $7$ | Manhattan uzunluğu |
| $L_\infty$ | en büyük $\lvert a_i\rvert$ | $4$ | En büyük bileşen |

**Manhattan** adı şehir sokaklarından geliyor: ızgara biçiminde bir
şehirde bir yerden bir yere kuş uçuşu değil, sokakları izleyerek
(önce doğu-batı, sonra kuzey-güney) gidersin. $L_1$ uzaklığı o yolun
uzunluğu. Önceki bölümde "bileşenleri toplamak uzunluk değil" demiştik;
doğrusu, **Öklid** uzunluğu değil. Bileşenlerin mutlak değerlerini
toplamak başka bir uzunluk ölçüsü, $L_1$.

Üçünün sırası her zaman aynı: $L_\infty \le L_2 \le L_1$.

Makine öğrenmesinde:

- **$L_2$** en yaygın uzaklık; en yakın komşu, kümeleme.
- **$L_1$** aykırı değerlere daha az duyarlı; kare almadığı için tek bir büyük fark tabloyu ezmiyor.
- **Düzenlileştirme:** modelin ağırlıklarını küçük tutmak için ağırlık vektörünün $L_2$ ya da $L_1$ normu cezaya ekleniyor (Ridge ve Lasso).

## Makine öğrenmesinde nokta çarpımı

- **Doğrusal model:** tahmin $= \mathbf{w} \cdot \mathbf{x} + b$. Ağırlık
  vektörü ile özellik vektörünün nokta çarpımı. $\mathbf{w} = (0.02, 0.5, -0.1)$,
  $\mathbf{x} = (120, 3, 10)$ ve $b = 1$ ise tahmin
  $2.4 + 1.5 - 1 + 1 = 3.9$.
- **Yapay sinir ağındaki nöron:** girdilerin ağırlıklı toplamı, yani yine
  bir nokta çarpımı; ardından bir fonksiyondan geçiyor.
- **Öneri sistemleri:** kullanıcı ve ürün vektörlerinin nokta çarpımı
  "bu kişi bu ürünü ne kadar sever" tahmini.
- **Dil modellerinde dikkat (attention):** bir kelimenin başka bir kelimeye
  ne kadar "dikkat edeceği", iki vektörün nokta çarpımıyla hesaplanıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$(3, 4) \cdot (2, 1) = (6, 4)$</p>
      <p>$\mathbf{a} \cdot \mathbf{b} = 0$ ise vektörlerden biri sıfır</p>
      <p>Benzerlik için yalnızca uzaklığa bakmak</p>
      <p>$\cos\theta = \mathbf{a} \cdot \mathbf{b}$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$(3, 4) \cdot (2, 1) = 6 + 4 = 10$, bir sayı</p>
      <p>Sıfır ise dikler (ya da biri sıfır vektörü)</p>
      <p>Uzunluk önemsizse kosinüs benzerliği</p>
      <p>$\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$</p>
    </div>
  </div>
  <figcaption>Nokta çarpımı bileşenleri çarpıp toplar ve tek bir sayı verir.</figcaption>
</figure>

- **Çarpımları toplamayı unutmak.** Karşılıklı bileşenleri çarpıp bir
  vektör olarak bırakmak nokta çarpımı değil (o başka bir işlem).
- **Uzunluklara bölmeyi unutmak.** $\mathbf{a} \cdot \mathbf{b}$ tek başına
  kosinüs değil; ancak iki vektör de birim uzunluktaysa öyle.
- **Farklı boyutlu vektörler.** Tanımsız.

## Özet

- $\mathbf{a} \cdot \mathbf{b} = \sum a_i b_i$: karşılıklı çarp, topla; sonuç bir sayı.
- $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2$.
- $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta$ (kosinüs teoreminden).
- İşaret açıyı söyler: pozitif dar, sıfır dik, negatif geniş.
- $\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$: kosinüs benzerliği, uzunluktan bağımsız.
- İzdüşüm $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}$; bileşenler, birim vektörler üzerindeki izdüşümlerdir.
- Normlar: $L_2$ (Öklid), $L_1$ (Manhattan), $L_\infty$ (en büyük bileşen).
- ML: doğrusal model $\mathbf{w} \cdot \mathbf{x} + b$, nöron, öneri, dikkat.
