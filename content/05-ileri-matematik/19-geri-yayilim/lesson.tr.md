# Geri Yayılım: Sinir Ağında Türev

Gradyan inişi her adımda kaybın **bütün** ağırlıklara göre türevini
istiyor. Milyonlarca ağırlıklı bir ağda her ağırlık için ayrı ayrı
sayısal türev almak, her adımda milyonlarca ileri geçiş demek; imkânsız.
**Geri yayılım** bütün bu türevleri tek bir geri geçişle, yaklaşık bir
ileri geçiş maliyetine hesaplıyor. Yeni bir matematik değil: zincir
kuralının akıllıca, sondan başa doğru uygulanması.

Bu bölümde hesap grafiklerini, yerel türevleri, küçük bir ağda geri
yayılımı adım adım ve derin ağlarda ortaya çıkan sorunları göreceğiz.

Ön bilgi: Türev Kuralları ve Zincir Kuralı, Jacobian ve Hessian, Gradyan
İnişi bölümleri.

## Hesap grafiği

Her karmaşık ifade basit işlemlerin art arda uygulanması. Bu işlemleri
düğümler, aralarındaki veri akışını oklar olarak çizince bir **hesap
grafiği** çıkar. $f = (x + y) \cdot z$ için ara değer $q = x + y$,
sonra $f = q \cdot z$.

<figure class="fig">
<svg viewBox="0 0 420 330" width="420"><circle class="box" cx="50" cy="50" r="20"/><text class="ink" x="50" y="55" font-size="14" text-anchor="middle">x</text><circle class="box" cx="50" cy="150" r="20"/><text class="ink" x="50" y="155" font-size="14" text-anchor="middle">y</text><circle class="box" cx="50" cy="250" r="20"/><text class="ink" x="50" y="255" font-size="14" text-anchor="middle">z</text><circle class="dot3" opacity="0.35" cx="200" cy="100" r="20"/><text class="ink" x="200" y="105" font-size="14" text-anchor="middle">+</text><circle class="dot2" opacity="0.35" cx="340" cy="175" r="20"/><text class="ink" x="340" y="180" font-size="14" text-anchor="middle">×</text><line class="line" x1="69.0" y1="56.3" x2="177.2" y2="92.4"/><polygon class="dim" points="181.0,93.7 173.1,94.7 175.3,88.1"/><line class="line" x1="69.0" y1="143.7" x2="177.2" y2="107.6"/><polygon class="dim" points="181.0,106.3 175.3,111.9 173.1,105.3"/><line class="line" x1="217.6" y1="109.4" x2="318.8" y2="163.7"/><polygon class="dim" points="322.4,165.6 314.4,165.2 317.7,159.1"/><line class="line" x1="69.4" y1="245.0" x2="316.8" y2="181.0"/><polygon class="dim" points="320.6,180.0 314.5,185.2 312.8,178.4"/><text class="ink" x="400" y="180" font-size="15" text-anchor="middle">f</text><line class="line" x1="362" y1="175" x2="390" y2="175"/><text class="ink" x="110" y="50" font-size="12" text-anchor="middle">−2</text><text class="dot2" x="110" y="66" font-size="12" text-anchor="middle">−4</text><text class="ink" x="118" y="150" font-size="12" text-anchor="middle">5</text><text class="dot2" x="118" y="166" font-size="12" text-anchor="middle">−4</text><text class="ink" x="250" y="154" font-size="12" text-anchor="middle">q = 3</text><text class="dot2" x="250" y="170" font-size="12" text-anchor="middle">−4</text><text class="ink" x="190" y="226" font-size="12" text-anchor="middle">−4</text><text class="dot2" x="190" y="242" font-size="12" text-anchor="middle">3</text><text class="ink" x="400" y="153" font-size="12" text-anchor="middle">−12</text><text class="dot2" x="400" y="169" font-size="12" text-anchor="middle"></text><text class="dot2" x="400" y="205" font-size="12" text-anchor="middle">1</text><text class="ink" x="200" y="300" font-size="11" text-anchor="middle">ileri geçiş: değerler (üstte)</text><text class="dot2" x="200" y="318" font-size="11" text-anchor="middle">geri geçiş: ∂f/∂(o düğüm) (altta, turuncu)</text></svg>
  <figcaption>x = −2, y = 5, z = −4. İleri geçiş soldan sağa değerleri hesaplıyor: q = 3, f = −12. Geri geçiş sağdan sola türevleri taşıyor: ∂f/∂f = 1 ile başlıyor, çarpma düğümü ∂f/∂q = z = −4 ve ∂f/∂z = q = 3 veriyor, toplama düğümü −4'ü x'e ve y'ye aynen dağıtıyor.</figcaption>
</figure>

**İki geçiş.**

1. **İleri:** girdilerden çıktıya, her düğümün değerini hesapla ve sakla.
2. **Geri:** çıktıda $\frac{\partial f}{\partial f} = 1$ ile başla; her düğümde gelen türevi (**yukarıdan gelen gradyan**) o düğümün **yerel türeviyle** çarpıp girdilerine ilet.

Zincir kuralının kendisi:

$$
\frac{\partial f}{\partial x} = \frac{\partial f}{\partial q} \cdot \frac{\partial q}{\partial x} = (-4) \cdot 1 = -4
$$

## Kapıların davranışı

Her düğüm yalnızca kendi yerel türevini bilmek zorunda. Sık kullanılan
düğümler şaşırtıcı derecede basit kurallarla çalışır:

| Düğüm | İleri | Geri (gelen gradyan $g$) |
|---|---|---|
| toplama $a + b$ | topla | $g$'yi iki girdiye **aynen** dağıt |
| çarpma $a \cdot b$ | çarp | $a$'ya $g \cdot b$, $b$'ye $g \cdot a$: girdileri **değiş tokuş** et |
| $\max(a, b)$ | büyüğü seç | $g$'yi **yalnızca büyük olana** yolla, öbürüne $0$ |
| ReLU | $\max(0, z)$ | $z > 0$ ise $g$, değilse $0$ |
| sigmoid | $\sigma(z)$ | $g \cdot \sigma(1 - \sigma)$ |
| **dallanma** (bir değer iki yerde kullanılıyor) | kopyala | iki daldan gelen gradyanları **topla** |

Son satır önemli: $x$ hem $a$'yı hem $b$'yi etkiliyorsa, $x$'in türevi iki
yolun toplamı. Çok değişkenli zincir kuralında "yollar toplanır" demiştik.

## Küçük bir ağda geri yayılım

Bir girdi, iki gizli nöron (ReLU), bir çıktı:

$$
\begin{aligned}
\mathbf{z} &= W_1 x + \mathbf{b}_1, & \mathbf{a} &= \mathrm{ReLU}(\mathbf{z}) \\
\hat{y} &= \mathbf{w}_2 \cdot \mathbf{a} + b_2, & L &= \tfrac{1}{2}(\hat{y} - y)^2
\end{aligned}
$$

<figure class="fig">
<svg viewBox="0 0 440 290" width="440"><circle class="box" cx="70" cy="120" r="22"/><text class="ink" x="70" y="125" font-size="14" text-anchor="middle">x</text><circle class="box" cx="220" cy="60" r="22"/><text class="ink" x="220" y="65" font-size="14" text-anchor="middle">h₁</text><circle class="box" cx="220" cy="180" r="22"/><text class="ink" x="220" y="185" font-size="14" text-anchor="middle">h₂</text><circle class="box" cx="370" cy="120" r="22"/><text class="ink" x="370" y="125" font-size="14" text-anchor="middle">ŷ</text><line class="line" x1="90.4" y1="111.8" x2="195.9" y2="69.7"/><polygon class="dim" points="199.6,68.2 194.2,74.1 191.6,67.6"/><line class="line" x1="90.4" y1="128.2" x2="195.9" y2="170.3"/><polygon class="dim" points="199.6,171.8 191.6,172.4 194.2,165.9"/><line class="line" x1="240.4" y1="68.2" x2="345.9" y2="110.3"/><polygon class="dim" points="349.6,111.8 341.6,112.4 344.2,105.9"/><line class="line" x1="240.4" y1="171.8" x2="345.9" y2="129.7"/><polygon class="dim" points="349.6,128.2 344.2,134.1 341.6,127.6"/><text class="dim" x="138" y="78" font-size="11" text-anchor="middle">W₁₁ = 1</text><text class="dim" x="138" y="172" font-size="11" text-anchor="middle">W₁₂ = −1</text><text class="dim" x="300" y="78" font-size="11" text-anchor="middle">w₂₁ = 2</text><text class="dim" x="300" y="172" font-size="11" text-anchor="middle">w₂₂ = −1</text><text class="dim" x="220" y="222" font-size="10.5" text-anchor="middle">b₁₂ = 2</text><text class="ink" x="70" y="26" font-size="11" text-anchor="middle">girdi</text><text class="ink" x="220" y="20" font-size="11" text-anchor="middle">gizli katman (ReLU)</text><text class="ink" x="370" y="26" font-size="11" text-anchor="middle">çıktı</text><text class="ink" x="220" y="256" font-size="11" text-anchor="middle">ileri: z = (1, 1), a = (1, 1), ŷ = 1; hedef y = 3, L = 2</text><text class="dot2" x="220" y="276" font-size="11" text-anchor="middle">geri: ∂L/∂ŷ = −2, ∂L/∂a = (−4, 2), ∂L/∂w₂ = (−2, −2)</text></svg>
  <figcaption>x = 1, W₁ = (1, −1), b₁ = (0, 2), w₂ = (2, −1), b₂ = 0, hedef y = 3. Üst satır ileri geçişin değerleri, turuncu satır geri geçişin taşıdığı türevler.</figcaption>
</figure>

**İleri.** $\mathbf{z} = (1, \ -1 + 2) = (1, 1)$, $\mathbf{a} = (1, 1)$,
$\hat{y} = 2 - 1 = 1$, $L = \frac{1}{2}(1 - 3)^2 = 2$.

**Geri**, sondan başa:

| Adım | Formül | Değer |
|---|---|---|
| çıktı | $\frac{\partial L}{\partial \hat{y}} = \hat{y} - y$ | $-2$ |
| çıktı ağırlıkları | $\frac{\partial L}{\partial \mathbf{w}_2} = \frac{\partial L}{\partial \hat{y}} \, \mathbf{a}$ | $(-2, -2)$ |
| gizli çıkışlar | $\frac{\partial L}{\partial \mathbf{a}} = \frac{\partial L}{\partial \hat{y}} \, \mathbf{w}_2$ | $(-4, 2)$ |
| ReLU'dan geçiş | $\frac{\partial L}{\partial \mathbf{z}} = \frac{\partial L}{\partial \mathbf{a}} \odot \mathrm{ReLU}'(\mathbf{z})$ | $(-4, 2)$ |
| ilk katman ağırlıkları | $\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \mathbf{z}} \, x$ | $(-4, 2)$ |

($\odot$ eleman eleman çarpım; iki $z$ de pozitif olduğu için ReLU gradyanı
aynen geçirdi.) Her katmanda aynı iki hareket var: gradyanı **ağırlığın
devriğiyle geri taşı** ve **girdiyle çarparak ağırlığın türevini al**.
Katman sayısı artsa da tarif değişmiyor.

## Neden bu kadar verimli?

**Ters mod.** Türevleri çıktıdan girdiye doğru taşıdığımız için tek bir
geri geçiş, tek bir çıktının (kaybın) **bütün** girdilere ve ağırlıklara
göre türevini veriyor. Maliyeti kabaca bir ileri geçişin birkaç katı.
Ağırlıkları tek tek oynatarak sayısal türev almak ise ağırlık sayısı
kadar ileri geçiş ister.

**Bellek bedeli.** Geri geçişte yerel türevler için ileri geçişteki ara
değerler ($\mathbf{z}$, $\mathbf{a}$) gerekiyor; hepsi saklanıyor. Büyük
modellerin eğitimde çıkarımdan çok daha fazla bellek istemesinin nedeni
bu.

**Otomatik türev.** Derin öğrenme kütüphaneleri ileri geçişi yazarken
hesap grafiğini kendileri kaydediyor ve geri geçişi bu kurallarla
otomatik yapıyor. Kullanıcı yalnızca modeli ve kaybı yazıyor; `backward`
çağrısı bu bölümdeki tabloyu milyonlarca düğüm için dolduruyor.

**Doğrulama.** Elle yazılmış bir geri geçiş, gradyan kontrolüyle
sınanır: birkaç ağırlığı $\pm h$ oynatıp merkezi farkı, geri yayılımın
verdiği türevle karşılaştır.

## Derin ağlarda sorunlar

Bir gradyan $n$ katmandan geçerken $n$ tane yerel türevle çarpılıyor.
Çarpanlar genelde $1$'den küçükse gradyan **söner**, büyükse **patlar**:

- Sigmoidde her çarpan en fazla $0{,}25$: $10$ katmanda $0{,}25^{10} \approx 10^{-6}$.
- Ağırlıklar biraz büyükse, katman başına çarpan $1{,}1$ bile olsa $50$ katmanda $1{,}1^{50} \approx 117$.

**Çareler.**

- **ReLU** gibi aktif bölgede türevi $1$ olan aktivasyonlar.
- **Dikkatli başlangıç** (Xavier, He): ağırlıkları, çarpanların ortalamada $1$ civarında kalacağı ölçekte başlatmak.
- **Artık (residual) bağlantılar:** $\mathbf{a}_{k+1} = \mathbf{a}_k + F(\mathbf{a}_k)$. Türev $I + J_F$; birim matris sayesinde gradyanın geçebileceği bir "otoyol" kalıyor.
- **Normalizasyon katmanları** ve **gradyan kırpma**.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>Geri geçişte ağırlığın kendisiyle çarpmak</p>
      <p>Dallanmada gradyanlardan birini almak</p>
      <p>$\max$ gradyanı iki girdiye de yollar</p>
      <p>Geri yayılım yeni bir türev kuralıdır</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Devriğiyle: $W^\mathsf{T} \frac{\partial L}{\partial \mathbf{z}}$</p>
      <p>Dallardan gelenleri topla</p>
      <p>Yalnızca seçilen girdiye yollar</p>
      <p>Zincir kuralının sondan başa uygulanması</p>
    </div>
  </div>
  <figcaption>Her düğüm yalnızca kendi yerel türevini bilir; geri yayılım bunları zincir kuralıyla birleştirir.</figcaption>
</figure>

## Özet

- Hesap grafiği: basit işlemlerden oluşan düğümler; ileri geçiş değerleri hesaplayıp saklar.
- Geri geçiş $\frac{\partial L}{\partial L} = 1$ ile başlar; her düğümde gelen gradyan × yerel türev.
- Toplama dağıtır, çarpma değiş tokuş eder, max yönlendirir, dallanma toplar.
- Katman başına: $\frac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T}\frac{\partial L}{\partial \mathbf{z}}$, $\frac{\partial L}{\partial W} = \frac{\partial L}{\partial \mathbf{z}}\mathbf{x}^\mathsf{T}$.
- Tek geri geçiş bütün türevleri verir (ters mod); bedeli ara değerleri saklamak.
- Sönen ve patlayan gradyan: çarpanların $1$'den uzak olması; çare ReLU, iyi başlangıç, artık bağlantılar, normalizasyon, kırpma.
