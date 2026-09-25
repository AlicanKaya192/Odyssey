# Geometri Temelleri

Geometri şekillerin, uzunlukların, açıların ve alanların matematiği.
Makine öğrenmesinde doğrudan karşına çıktığı yerler şaşırtıcı derecede
çok: iki veri noktasının uzaklığı Pisagor bağıntısının kendisi, iki
vektörün benzerliği aralarındaki açıyla ölçülür, nesne tespit eden bir
model tahmin ettiği kutunun doğruluğunu iki dikdörtgenin örtüşen alanıyla
ölçer. Bu bölümde açıları, üçgenleri, Pisagor bağıntısını, benzerliği,
temel şekillerin çevre ve alanını, çemberi ve cisimlerin hacmini
göreceğiz. Bir sonraki bölüm Trigonometri buradaki dik üçgenlerin üstüne
kurulur.

Ön bilgi: Köklü Sayılar, Oran, Orantı ve Yüzde, Koordinat Düzlemi ve
Doğru.

## Açılar

İki ışının başlangıç noktası ortaksa aralarında bir **açı** oluşur. Açı
**derece** ile ölçülür; tam bir tur $360°$.

| Ad | Ölçü | Örnek |
|---|---|---|
| dar açı | $0°$ ile $90°$ arası | $45°$ |
| dik açı | tam $90°$ | kâğıdın köşesi |
| geniş açı | $90°$ ile $180°$ arası | $120°$ |
| doğru açı | $180°$ | düz bir çizgi |
| tam açı | $360°$ | tam tur |

**Tümler ve bütünler.** Toplamı $90°$ olan iki açı **tümler**, toplamı
$180°$ olan iki açı **bütünler** açılar. $35°$'nin tümleri $55°$,
bütünleri $145°$.

**Ters açılar.** Kesişen iki doğrunun karşılıklı açıları eşittir. Biri
$70°$ ise karşısı da $70°$, yanındakiler $110°$.

**Paralel doğrular ve kesen.** İki paralel doğruyu üçüncü bir doğru
kestiğinde oluşan **iç ters açılar** eşittir (Z harfinin iki köşesi gibi).
Üçgenin açı toplamı bundan çıkar.

## Üçgenler

**İç açıların toplamı $180°$.** Üçgenin tepesinden tabana paralel bir doğru
çiz. Paralel doğruda, tepedeki açının iki yanında taban açılarının
eşleri oluşur (iç ters açılar). Tepedeki üç açı yan yana bir doğru açı
oluşturur.

<figure class="fig">
<svg viewBox="0 0 440 264" width="440"><polygon class="curve" fill="none" points="60,210 380,210 170,50"/><line class="curve3" stroke-dasharray="5 4" x1="20" y1="50" x2="420" y2="50"/><path class="curve2" fill="none" stroke-width="2" d="M 86.0 210.0 A 26 26 0 0 0 74.7 188.6"/><text class="ink" x="97.2" y="195.4" font-size="14" text-anchor="middle">α</text><path class="curve4" fill="none" stroke-width="2" d="M 359.3 194.2 A 26 26 0 0 0 354.0 210.0"/><text class="ink" x="340.2" y="201.6" font-size="14" text-anchor="middle">β</text><path class="curve" fill="none" stroke-width="2" d="M 155.3 71.4 A 26 26 0 0 0 190.7 65.8"/><text class="ink" x="176.6" y="96.5" font-size="14" text-anchor="middle">γ</text><path class="curve2" fill="none" stroke-width="2" d="M 144.0 50.0 A 26 26 0 0 0 155.3 71.4"/><text class="ink" x="132.8" y="74.6" font-size="14" text-anchor="middle">α</text><path class="curve4" fill="none" stroke-width="2" d="M 196.0 50.0 A 26 26 0 0 1 190.7 65.8"/><text class="ink" x="209.8" y="68.4" font-size="14" text-anchor="middle">β</text><text class="ink" x="220" y="250" font-size="12" text-anchor="middle">tepedeki üç açı bir doğru açı: α + γ + β = 180°</text></svg>
  <figcaption>Tabandaki α ve β, paralel doğruda tepenin iki yanında aynen tekrar ediyor. Tepede α, γ ve β yan yana bir düz çizgi oluşturuyor; toplamları 180°.</figcaption>
</figure>

İki açısı $50°$ ve $60°$ olan üçgenin üçüncü açısı $180° - 110° = 70°$.

**Türler.** Kenarlara göre: **eşkenar** (üç kenar eşit, her açı $60°$),
**ikizkenar** (iki kenar eşit, o kenarların karşısındaki açılar eşit),
**çeşitkenar** (hepsi farklı). Açılara göre: **dar açılı**, **dik açılı**
(bir açı $90°$), **geniş açılı** (bir açı $90°$'den büyük).

**Üçgen eşitsizliği.** Her kenar öteki ikisinin toplamından küçüktür:
$a + b > c$. $2$, $3$ ve $6$ uzunluğundaki çubuklarla üçgen kurulamaz,
çünkü $2 + 3 < 6$; kısa iki çubuk birbirine ulaşamaz. "İki nokta
arasındaki en kısa yol düz çizgidir" demenin başka bir yolu.

**Dış açı.** Bir kenar uzatılınca oluşan dış açı, öteki iki iç açının
toplamına eşittir: iç açı $\gamma$ ise dış açı $180° - \gamma = \alpha + \beta$.

## Pisagor bağıntısı

Dik üçgende dik açının karşısındaki en uzun kenara **hipotenüs** denir.
Dik kenarlar $a$ ve $b$, hipotenüs $c$ ise:

$$
a^2 + b^2 = c^2
$$

<figure class="fig">
<svg viewBox="0 0 440 278" width="440"><polygon class="dot" opacity="0.35" points="110,176 198,176 198,264 110,264"/><polygon class="dot2" opacity="0.35" points="110,176 110,110 44,110 44,176"/><polygon class="dot3" opacity="0.35" points="198,176 110,110 176,22 264,88"/><polygon class="curve" fill="none" points="110,176 198,176 110,110"/><polyline class="curve3" fill="none" points="110,165.0 121.0,165.0 121.0,176"/><text class="ink" x="154" y="225" font-size="16" text-anchor="middle">16</text><text class="ink" x="77.0" y="148.0" font-size="16" text-anchor="middle">9</text><text class="ink" x="187.0" y="104.0" font-size="16" text-anchor="middle">25</text><text class="dim" x="154" y="170" font-size="12" text-anchor="middle">4</text><text class="dim" x="118" y="147.0" font-size="12" text-anchor="start">3</text><text class="dim" x="162" y="141.0" font-size="12" text-anchor="start">5</text><text class="ink" x="330" y="240" font-size="14" text-anchor="middle">9 + 16 = 25</text></svg>
  <figcaption>Kenarları 3, 4 ve 5 olan dik üçgenin her kenarına bir kare çizilmiş. Dik kenarlardaki karelerin alanları 9 ve 16; hipotenüsteki karenin alanı 25. Küçük iki karenin toplamı büyük kareye eşit.</figcaption>
</figure>

**Örnek.** $10$ metrelik bir merdiven duvardan $6$ metre uzağa
yaslanıyor. Duvarda ne kadar yükseğe ulaşır? $6^2 + h^2 = 10^2$, yani
$h^2 = 64$ ve $h = 8$ metre.

**Tanıdık üçlüler.** $3$-$4$-$5$, $5$-$12$-$13$, $8$-$15$-$17$ ve bunların
katları ($6$-$8$-$10$ gibi). Hesap yaparken tanımak zaman kazandırır.

**Tersi de doğru.** Kenarlar $a^2 + b^2 = c^2$'yi sağlıyorsa üçgen diktir.
$7$, $24$, $25$: $49 + 576 = 625$ ✓, dik üçgen. Sağlamıyorsa: $c^2$ daha
büyükse geniş açılı, daha küçükse dar açılı.

**Uzaklık formülü buradan.** Koordinat Düzlemi bölümündeki
$d = \sqrt{\Delta x^2 + \Delta y^2}$, yatay ve dikey farkların oluşturduğu
dik üçgenin hipotenüsü. Üç boyutta bir terim eklenir:
$(1, 2, 3)$ ile $(4, 6, 3)$ arası $\sqrt{9 + 16 + 0} = 5$.

## Benzerlik

Açıları aynı, kenarları **orantılı** iki şekle **benzer** denir. Oran $k$
ise her kenar $k$ katı.

**Gölge problemi.** $2$ metrelik bir çubuğun gölgesi $3$ metre; aynı anda
bir ağacın gölgesi $15$ metre. Güneş ışınları iki üçgeni benzer yapar:
$\frac{h}{15} = \frac{2}{3}$, ağaç $10$ metre.

**Özel dik üçgenler.** Trigonometride sürekli kullanılacak iki üçgen:

| Açılar | Kenar oranları | Nereden |
|---|---|---|
| $45°$, $45°$, $90°$ | $1 : 1 : \sqrt{2}$ | karenin köşegeni |
| $30°$, $60°$, $90°$ | $1 : \sqrt{3} : 2$ | eşkenar üçgenin yarısı |

Kenarı $1$ olan karenin köşegeni Pisagor ile $\sqrt{1 + 1} = \sqrt{2}$.
Kenarı $2$ olan eşkenar üçgeni ortadan ikiye bölünce kenarları $1$, $2$ ve
$\sqrt{4 - 1} = \sqrt{3}$ olan bir dik üçgen çıkar.

## Çevre ve alan

**Çevre** kenarların toplamı, **alan** şeklin kapladığı yer; alan birim
kareyle ölçülür ($\text{cm}^2$, $\text{m}^2$).

| Şekil | Çevre | Alan |
|---|---|---|
| kare, kenar $a$ | $4a$ | $a^2$ |
| dikdörtgen, $a \times b$ | $2(a + b)$ | $a \cdot b$ |
| üçgen, taban $t$, yükseklik $h$ | kenarlar toplamı | $\frac{1}{2} t h$ |
| paralelkenar | kenarlar toplamı | $t \cdot h$ |
| yamuk, tabanlar $a$ ve $c$ | kenarlar toplamı | $\frac{(a + c)}{2} h$ |

**Yükseklik** tabana dik olan uzaklık; eğik kenar değil.

<figure class="fig">
<svg viewBox="0 0 440 220" width="440"><rect class="box" x="100" y="30" width="240" height="160"/><polygon class="dot" opacity="0.4" points="100,190 340,190 180,30"/><polygon class="curve" fill="none" points="100,190 340,190 180,30"/><line class="curve2" stroke-dasharray="5 4" x1="180" y1="190" x2="180" y2="30"/><text class="ink" x="220" y="208" font-size="12" text-anchor="middle">taban 6</text><text class="ink" x="186" y="114" font-size="12" text-anchor="start">yükseklik 4</text><text class="ink" x="220" y="20" font-size="13" text-anchor="middle">alan = ½ · 6 · 4 = 12</text></svg>
  <figcaption>Taban 6, yükseklik 4 olan üçgen, 6 × 4'lük dikdörtgenin içine oturuyor. Yükseklik çizgisi dikdörtgeni ikiye bölüyor ve üçgen her parçanın tam yarısını kaplıyor; bu yüzden alan dikdörtgenin yarısı.</figcaption>
</figure>

**Örnek.** Tabanları $4$ ve $10$, yüksekliği $5$ olan yamuğun alanı
$\frac{4 + 10}{2} \cdot 5 = 35$. Yamuk, tabanlarının ortalaması kadar
genişlikte bir dikdörtgen gibi davranır.

## Çember ve daire

**Çember** merkezden eşit uzaklıktaki noktalar; **daire** çemberin içi.
Merkezden çembere uzaklık **yarıçap** $r$, çemberi merkezden geçerek kesen
doğru parçası **çap** $2r$.

Her çemberde çevre ile çapın oranı aynı sayıdır: $\pi \approx 3{,}14159$.

$$
\text{çevre} = 2 \pi r \qquad \text{alan} = \pi r^2
$$

$r = 5$ için çevre $10\pi \approx 31{,}42$, alan $25\pi \approx 78{,}54$.

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><circle class="box" cx="150" cy="120" r="95"/><path class="dot" opacity="0.4" d="M 150 120 L 245 120 A 95 95 0 0 0 197.5 37.7 Z"/><line class="curve" x1="150" y1="120" x2="245" y2="120"/><line class="curve" x1="150" y1="120" x2="197.5" y2="37.7"/><line class="curve2" stroke-dasharray="5 4" x1="133.5" y1="213.6" x2="166.5" y2="26.4"/><circle class="dot3" cx="150" cy="120" r="4"/><text class="ink" x="197.5" y="136" font-size="12" text-anchor="middle">yarıçap r</text><text class="ink" x="128" y="178" font-size="12" text-anchor="end">çap 2r</text><text class="ink" x="180" y="108" font-size="12" text-anchor="start">60°</text><text class="ink" x="265" y="60" font-size="12" text-anchor="start">60° dilim: alanın 1/6'sı</text></svg>
  <figcaption>Yarıçap merkezden çembere, çap bir uçtan öbür uca merkezden geçerek. 60°'lik dilim tam turun 60 / 360 = 1/6'sı; alanı da, yay uzunluğu da dairenin 1/6'sı.</figcaption>
</figure>

**Yay ve dilim.** Merkez açısı $\theta$ derece olan dilim tam turun
$\frac{\theta}{360}$'ı:

$$
\text{yay} = \frac{\theta}{360} \cdot 2\pi r \qquad \text{dilim alanı} = \frac{\theta}{360} \cdot \pi r^2
$$

$r = 6$ ve $\theta = 60°$ için yay $2\pi$, dilim alanı $6\pi$. Trigonometri
bölümünde açıyı dereceyle değil yay uzunluğuyla ölçeceğiz (radyan).

## Cisimler

| Cisim | Hacim | Yüzey alanı |
|---|---|---|
| küp, kenar $a$ | $a^3$ | $6a^2$ |
| dikdörtgenler prizması $a \times b \times c$ | $abc$ | $2(ab + bc + ca)$ |
| silindir, yarıçap $r$, yükseklik $h$ | $\pi r^2 h$ | $2\pi r^2 + 2\pi r h$ |
| küre, yarıçap $r$ | $\frac{4}{3} \pi r^3$ | $4 \pi r^2$ |
| koni | $\frac{1}{3} \pi r^2 h$ | |

Prizma ve silindirin hacmi **taban alanı çarpı yükseklik**; koni aynı
tabanlı silindirin üçte biri. $2 \times 3 \times 4$ kutunun hacmi $24$,
yüzeyi $2(6 + 12 + 8) = 52$. Yarıçapı $3$, yüksekliği $10$ olan silindirin
hacmi $90\pi \approx 282{,}7$.

**Ölçek.** Bütün uzunluklar $k$ katına çıkarsa alan $k^2$, hacim $k^3$
katına çıkar. Kenarı iki katına çıkan küpün yüzeyi $4$, hacmi $8$ kat
olur. Bu yüzden büyük hayvanların bacakları orantısız kalındır: ağırlık
$k^3$ ile, kemik kesiti $k^2$ ile büyür.

## Makine öğrenmesinde geometri

**Uzaklık her yerde.** $k$ en yakın komşu, kümeleme (k-means) ve öneri
sistemleri örnekler arasındaki uzaklığa bakar. Yüz özellikli iki örneğin
uzaklığı, yüz terimli bir Pisagor: $\sqrt{\Delta_1^2 + \dots + \Delta_{100}^2}$.

**Açı ve benzerlik.** İki belgenin ya da iki kelimenin ne kadar benzediği
çoğu zaman aralarındaki açıyla ölçülür: açı küçükse benzerler. Bunun
hesabı Trigonometri ve MAT 2'deki nokta çarpımıyla geliyor.

**IoU.** Bir nesne tespit modeli resimde bir kutu tahmin eder. Tahminin
ne kadar iyi olduğu, gerçek kutu ile tahmin edilen kutunun **kesişim
alanının birleşim alanına oranıyla** ölçülür:

$$
\text{IoU} = \frac{\text{kesişim alanı}}{\text{birleşim alanı}}
$$

<figure class="fig">
<svg viewBox="0 0 440 244" width="440"><rect class="curve" fill="none" stroke-width="2" x="90" y="68" width="176" height="132"/><rect class="curve2" fill="none" stroke-width="2" stroke-dasharray="6 4" x="134" y="24" width="176" height="132"/><rect class="dot3" opacity="0.4" x="134" y="68" width="132" height="88"/><text class="ink" x="94" y="192" font-size="12" text-anchor="start">gerçek kutu</text><text class="ink" x="306" y="16" font-size="12" text-anchor="end">tahmin</text><text class="ink" x="200.0" y="117" font-size="12" text-anchor="middle">kesişim 6</text><text class="ink" x="220" y="230" font-size="14" text-anchor="middle">IoU = 6 / 18 = 1/3</text></svg>
  <figcaption>Gerçek kutu 4 × 3, tahmin 4 × 3, ikisi de 12 birim kare. Örtüşen bölge 3 × 2 = 6. Birleşim 12 + 12 − 6 = 18; ortak bölge iki kez sayılmasın diye bir kez çıkarılıyor. IoU = 6 / 18 = 1/3.</figcaption>
</figure>

IoU $1$ ise kutular çakışık, $0$ ise hiç örtüşmüyor. Pratikte $0{,}5$'in
üstü genellikle "doğru tespit" sayılır.

**Görüntü bir ızgara.** Bir resim piksellerden oluşan bir dikdörtgen;
$224 \times 224$ bir resimde $50\,176$ piksel var. Evrişimli ağlar bu
ızgarada küçük karelerle gezinir.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$a + b = c$ (dik üçgende)</p>
      <p>üçgen alanı $t \cdot h$</p>
      <p>daire alanı $2\pi r$</p>
      <p>uzunluk $2$ kat ⇒ hacim $2$ kat</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$a^2 + b^2 = c^2$</p>
      <p>$\dfrac{1}{2} t h$</p>
      <p>alan $\pi r^2$, çevre $2\pi r$</p>
      <p>hacim $2^3 = 8$ kat</p>
    </div>
  </div>
  <figcaption>Pisagor karelerle çalışır; alan uzunluğun karesiyle, hacim küpüyle büyür.</figcaption>
</figure>

- **Eğik kenarı yükseklik sanmak.** Yükseklik tabana dik ölçülür.
- **Hipotenüsü yanlış seçmek.** Hipotenüs dik açının karşısındaki, en uzun
  kenar; $a^2 + b^2 = c^2$'de $c$ o.

## Özet

- Açılar derece ile; tümler $90°$, bütünler $180°$; ters açılar eşit.
- Üçgenin iç açıları toplamı $180°$; her kenar öteki ikisinin toplamından
  küçük.
- Dik üçgende $a^2 + b^2 = c^2$; tersi de doğru; uzaklık formülü buradan.
- Benzer şekillerde kenarlar orantılı; $45$-$45$-$90$ ve $30$-$60$-$90$
  üçgenleri $1 : 1 : \sqrt{2}$ ve $1 : \sqrt{3} : 2$.
- Alanlar: dikdörtgen $ab$, üçgen $\frac{1}{2} t h$, yamuk
  $\frac{a + c}{2} h$, daire $\pi r^2$; çevre $2\pi r$.
- Hacim: prizma ve silindir taban çarpı yükseklik, küre $\frac{4}{3}\pi r^3$;
  ölçekte alan $k^2$, hacim $k^3$.
- Uzaklık, açı ve IoU makine öğrenmesinin geometrik araçları.
