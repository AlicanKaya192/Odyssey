# Doğrusal Bağımsızlık, Taban ve Rank

Bir ev veri setinde üç sütun olsun: metrekare, oda sayısı ve "yüz
metrekare cinsinden alan". Üçüncü sütun birinciden başka bir şey
söylemiyor; yalnızca 100'e bölünmüş hâli. Kâğıt üzerinde üç özellik var,
ama gerçekte **iki** bağımsız bilgi.

Bu bölüm tam olarak bu soruyu matematikle soruyor: bir grup vektörün
içinde **kaç tane gerçekten farklı yön** var? Cevabın adı **rank**. Yol
boyunca doğrusal bağımsızlık, germe, taban ve boyut kavramlarını
göreceğiz. Bunlar özdeğerler, SVD ve PCA bölümlerinin temeli.

Ön bilgi: Doğrusal Sistemler ve Gauss Eleme bölümü.

## Doğrusal kombinasyon ve germe

Vektörler bölümünden hatırla: $\mathbf{v}_1, \dots, \mathbf{v}_k$
vektörlerinin **doğrusal kombinasyonu**, onları sayılarla çarpıp
toplamak:

$$
c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k
$$

Katsayılara bütün olası değerleri verince ulaşılabilen vektörlerin
hepsine bu vektörlerin **germesi** (span) denir:
$\operatorname{span}(\mathbf{v}_1, \dots, \mathbf{v}_k)$.

- Sıfır olmayan tek bir vektörün germesi, başlangıç noktasından geçen bir
  **doğru**: $c\,\mathbf{v}$'nin bütün değerleri.
- Aynı doğrultuda olmayan iki vektörün germesi bir **düzlem**. Düzlemde
  çalışıyorsak bu, **bütün düzlem** demek.
- Aynı doğrultudaki iki vektörün germesi yine yalnızca bir **doğru**.
  İkinci vektör yeni bir yön eklemiyor.

<figure class="fig">
<svg viewBox="0 0 420 210" width="420"><line class="grid" x1="20" y1="182" x2="20" y2="14"/><line class="grid" x1="48" y1="182" x2="48" y2="14"/><line class="grid" x1="76" y1="182" x2="76" y2="14"/><line class="line" x1="104" y1="182" x2="104" y2="14"/><line class="grid" x1="132" y1="182" x2="132" y2="14"/><line class="grid" x1="160" y1="182" x2="160" y2="14"/><line class="grid" x1="188" y1="182" x2="188" y2="14"/><line class="grid" x1="20" y1="182" x2="188" y2="182"/><line class="grid" x1="20" y1="154" x2="188" y2="154"/><line class="grid" x1="20" y1="126" x2="188" y2="126"/><line class="line" x1="20" y1="98" x2="188" y2="98"/><line class="grid" x1="20" y1="70" x2="188" y2="70"/><line class="grid" x1="20" y1="42" x2="188" y2="42"/><line class="grid" x1="20" y1="14" x2="188" y2="14"/><line class="curve4" x1="20.0" y1="182.0" x2="188.0" y2="14.0"/><line class="curve2" x1="104" y1="98" x2="154.9" y2="47.1"/><polygon class="dot2" points="160,42 156.8,50.4 151.6,45.2"/><line class="curve" x1="104" y1="98" x2="126.9" y2="75.1"/><polygon class="dot" points="132,70 128.8,78.4 123.6,73.2"/><text class="ink" x="138" y="80" font-size="12" text-anchor="start">v</text><text class="ink" x="166" y="46" font-size="12" text-anchor="start">w</text><text class="ink" x="104.0" y="200" font-size="11" text-anchor="middle">Bağımlı: w = 2v, yalnızca bir doğru</text><line class="grid" x1="226" y1="182" x2="226" y2="14"/><line class="grid" x1="254" y1="182" x2="254" y2="14"/><line class="grid" x1="282" y1="182" x2="282" y2="14"/><line class="line" x1="310" y1="182" x2="310" y2="14"/><line class="grid" x1="338" y1="182" x2="338" y2="14"/><line class="grid" x1="366" y1="182" x2="366" y2="14"/><line class="grid" x1="394" y1="182" x2="394" y2="14"/><line class="grid" x1="226" y1="182" x2="394" y2="182"/><line class="grid" x1="226" y1="154" x2="394" y2="154"/><line class="grid" x1="226" y1="126" x2="394" y2="126"/><line class="line" x1="226" y1="98" x2="394" y2="98"/><line class="grid" x1="226" y1="70" x2="394" y2="70"/><line class="grid" x1="226" y1="42" x2="394" y2="42"/><line class="grid" x1="226" y1="14" x2="394" y2="14"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="310.0" y1="182.0" x2="394.0" y2="140.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="182.0" x2="394.0" y2="98.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="310.0" y1="182.0" x2="226.0" y2="98.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="140.0" x2="394.0" y2="56.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="394.0" y1="182.0" x2="226.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="98.0" x2="394.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="394.0" y1="98.0" x2="310.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="56.0" x2="310.0" y2="14.0"/><line class="curve" x1="310" y1="98" x2="359.6" y2="73.2"/><polygon class="dot" points="366,70 360.3,77.0 357.0,70.4"/><line class="curve2" x1="310" y1="98" x2="287.1" y2="75.1"/><polygon class="dot2" points="282,70 290.4,73.2 285.2,78.4"/><line class="curve4" x1="310" y1="98" x2="334.8" y2="48.4"/><polygon class="dot3" points="338,42 337.6,51.0 331.0,47.7"/><text class="ink" x="372" y="74" font-size="12" text-anchor="start">v</text><text class="ink" x="276" y="74" font-size="12" text-anchor="end">w</text><text class="ink" x="344" y="42" font-size="11" text-anchor="start">v + w</text><text class="ink" x="310.0" y="200" font-size="11" text-anchor="middle">Bağımsız: her nokta a·v + b·w</text></svg>
  <figcaption>Solda $\mathbf{w} = 2\mathbf{v}$: ikisinin her kombinasyonu yeşil doğru üzerinde kalıyor. Sağda $\mathbf{v} = (2, 1)$ ve $\mathbf{w} = (-1, 1)$ farklı yönlerde; kesikli ızgaranın her köşesi bir $a\mathbf{v} + b\mathbf{w}$ ve ızgara bütün düzlemi kaplıyor. Yeşil ok $\mathbf{v} + \mathbf{w} = (1, 2)$.</figcaption>
</figure>

Germe, "bu vektörlerle nerelere gidebilirim?" sorusunun cevabı.
Matrislerle bağı da açık: $A\mathbf{x}$, $A$'nın sütunlarının bir
doğrusal kombinasyonu (sütun bakışı). Öyleyse **$A\mathbf{x}$'in
alabileceği bütün değerler, $A$'nın sütunlarının germesi**. Buna $A$'nın
**sütun uzayı** denir.

## Doğrusal bağımlılık ve bağımsızlık

Bir vektör grubunda vektörlerden biri **ötekilerin doğrusal
kombinasyonuysa** grup **doğrusal bağımlıdır**: o vektör yeni bir yön
eklemiyor, fazlalık. Hiçbiri ötekilerin kombinasyonu değilse grup
**doğrusal bağımsızdır**.

Örnek: $\mathbf{v}_1 = (1, 2, 1)$, $\mathbf{v}_2 = (2, 1, 0)$,
$\mathbf{v}_3 = (3, 3, 1)$. Dikkatli bakınca $\mathbf{v}_3 = \mathbf{v}_1 +
\mathbf{v}_2$: grup bağımlı. Üç vektör var ama gerdikleri şey yalnızca bir
düzlem.

### Resmî tanım

Bu tanımın denklemle yazılmış hâli daha kullanışlı:

$$
c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k = \mathbf{0}
$$

denkleminin **tek** çözümü $c_1 = c_2 = \cdots = c_k = 0$ ise vektörler
bağımsızdır. Sıfır olmayan bir çözüm varsa bağımlıdır.

İki tanım aynı şeyi söylüyor: örneğimizde $\mathbf{v}_1 + \mathbf{v}_2 -
\mathbf{v}_3 = \mathbf{0}$, yani $c = (1, 1, -1)$ sıfır olmayan bir çözüm.
Bunu $\mathbf{v}_3$ için çözünce $\mathbf{v}_3 = \mathbf{v}_1 +
\mathbf{v}_2$ geri geliyor.

### Bağımsızlığı nasıl sınarız?

**İki vektör:** biri ötekinin katıysa bağımlı, değilse bağımsız.
$(2, 1)$ ile $(4, 2)$ bağımlı; $(2, 1)$ ile $(1, 2)$ bağımsız.

**Genel yol:** vektörleri bir matrisin sütunları yap ve Gauss eleme uygula.

$$
c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k = \mathbf{0}
\quad \Longleftrightarrow \quad
A\mathbf{c} = \mathbf{0}
$$

Önceki bölümden: bu sistemin tek çözümü ancak **her sütunda pivot** varsa
$\mathbf{c} = \mathbf{0}$. Pivotsuz bir sütun serbest değişken, serbest
değişken sıfır olmayan bir çözüm demek.

$$
\text{sütunlar bağımsız} \iff \text{her sütunda pivot var}
$$

**Kare matris:** $n$ boyutta $n$ vektör için en kısa yol determinant.
$\det A \ne 0$ ise bağımsız, $\det A = 0$ ise bağımlı.
$\mathbf{v}_1 = (1, 0, 1)$, $\mathbf{v}_2 = (0, 1, 1)$, $\mathbf{v}_3 =
(1, 1, 0)$ için:

$$
\det \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 1 & 1 & 0 \end{bmatrix} = 1 \cdot (0 - 1) - 0 + 1 \cdot (0 - 1) = -2 \ne 0
$$

Bu üçü bağımsız.

### Çok fazla vektör her zaman bağımlıdır

$n$ boyutlu uzayda $n$'den fazla vektör **her zaman** bağımlıdır. Düzlemde
üç vektör alırsan biri mutlaka ötekilerin kombinasyonudur. Neden?
Matrisin $n$ satırı var, en fazla $n$ pivot olabilir; $n$'den fazla sütun
varsa en az birinin pivotu yok.

Sıfır vektörü içeren her grup da bağımlıdır: $1 \cdot \mathbf{0} =
\mathbf{0}$ sıfır olmayan bir çözüm.

## Taban ve boyut

Bir uzayın **tabanı**, o uzayı **geren** ve **bağımsız** olan bir vektör
grubudur. İki şartın ikisi de önemli:

- **Geriyor:** uzayın her vektörü bu vektörlerin bir kombinasyonu. Eksik
  yön yok.
- **Bağımsız:** hiçbiri fazlalık değil. Fazla yön yok.

En tanıdık taban **standart taban**: $\mathbf{e}_1 = (1, 0)$ ve
$\mathbf{e}_2 = (0, 1)$. Her $(x, y) = x\,\mathbf{e}_1 + y\,\mathbf{e}_2$.

Ama tek taban o değil. Düzlemde aynı doğrultuda olmayan **her** iki vektör
bir taban. Bir uzayın bütün tabanlarında aynı sayıda vektör vardır; bu
sayıya uzayın **boyutu** denir. Düzlem 2 boyutlu, bildiğimiz uzay 3
boyutlu, 784 pikselli bir görüntü 784 boyutlu bir uzayda yaşıyor.

### Başka bir tabanda koordinat

Bir taban seçince her vektör o tabana göre **tek bir şekilde** yazılır.
Katsayılar vektörün o tabandaki **koordinatları**.

$\mathbf{b}_1 = (1, 1)$ ve $\mathbf{b}_2 = (1, -1)$ tabanında $(3, 1)$'in
koordinatları nedir? $c_1\mathbf{b}_1 + c_2\mathbf{b}_2 = (3, 1)$
denklemini bileşen bileşen yaz:

$$
\begin{aligned}
c_1 + c_2 &= 3 \\
c_1 - c_2 &= 1
\end{aligned}
$$

Toplayınca $2c_1 = 4$, $c_1 = 2$; sonra $c_2 = 1$.

<figure class="fig">
<svg viewBox="0 0 280 246" width="280"><line class="grid" x1="40" y1="214" x2="40" y2="14"/><line class="line" x1="80" y1="214" x2="80" y2="14"/><line class="grid" x1="120" y1="214" x2="120" y2="14"/><line class="grid" x1="160" y1="214" x2="160" y2="14"/><line class="grid" x1="200" y1="214" x2="200" y2="14"/><line class="grid" x1="240" y1="214" x2="240" y2="14"/><line class="grid" x1="40" y1="214" x2="240" y2="214"/><line class="grid" x1="40" y1="174" x2="240" y2="174"/><line class="line" x1="40" y1="134" x2="240" y2="134"/><line class="grid" x1="40" y1="94" x2="240" y2="94"/><line class="grid" x1="40" y1="54" x2="240" y2="54"/><line class="grid" x1="40" y1="14" x2="240" y2="14"/><text class="dim" x="40" y="147" font-size="9" text-anchor="middle">-1</text><text class="dim" x="120" y="147" font-size="9" text-anchor="middle">1</text><text class="dim" x="160" y="147" font-size="9" text-anchor="middle">2</text><text class="dim" x="200" y="147" font-size="9" text-anchor="middle">3</text><text class="dim" x="240" y="147" font-size="9" text-anchor="middle">4</text><text class="dim" x="75" y="217" font-size="9" text-anchor="end">-2</text><text class="dim" x="75" y="177" font-size="9" text-anchor="end">-1</text><text class="dim" x="75" y="97" font-size="9" text-anchor="end">1</text><text class="dim" x="75" y="57" font-size="9" text-anchor="end">2</text><text class="dim" x="75" y="17" font-size="9" text-anchor="end">3</text><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="94.0" x2="120.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="174.0" x2="80.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="174.0" x2="200.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="94.0" x2="160.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="80.0" y1="214.0" x2="240.0" y2="54.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="14.0" x2="240.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="160.0" y1="214.0" x2="240.0" y2="134.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="120.0" y1="14.0" x2="240.0" y2="134.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="200.0" y1="14.0" x2="240.0" y2="54.0"/><line class="curve" x1="80" y1="134" x2="114.9" y2="99.1"/><polygon class="dot" points="120,94 116.8,102.4 111.6,97.2"/><line class="curve" x1="120" y1="94" x2="154.9" y2="59.1"/><polygon class="dot" points="160,54 156.8,62.4 151.6,57.2"/><line class="curve2" x1="160" y1="54" x2="194.9" y2="88.9"/><polygon class="dot2" points="200,94 191.6,90.8 196.8,85.6"/><line class="curve4" x1="80" y1="134" x2="193.2" y2="96.3"/><polygon class="dot3" points="200,94 193.4,100.1 191.0,93.1"/><text class="ink" x="94.0" y="112.0" font-size="12" text-anchor="end">b₁</text><text class="ink" x="186.0" y="72.0" font-size="12" text-anchor="start">b₂</text><text class="ink" x="206" y="106" font-size="11" text-anchor="start">(3, 1)</text><text class="ink" x="140.0" y="234" font-size="12" text-anchor="middle">(3, 1) = 2·b₁ + 1·b₂: yeni koordinatlar (2, 1)</text></svg>
  <figcaption>Kesikli ızgara $\mathbf{b}_1$ ve $\mathbf{b}_2$ yönlerinde. $(3, 1)$'e gitmek için iki kez $\mathbf{b}_1$ (mor), bir kez $\mathbf{b}_2$ (turuncu) yürümek yetiyor. Aynı nokta standart tabanda $(3, 1)$, yeni tabanda $(2, 1)$.</figcaption>
</figure>

Nokta aynı, yalnızca onu anlatmak için kullandığımız "cetveller"
değişti. **Koordinat değiştirmek**, doğrusal cebirin ve makine
öğrenmesinin en güçlü fikirlerinden biri: doğru tabanı seçince
karmaşık görünen bir problem basitleşiyor. Özdeğerler ve PCA bölümleri
tam olarak "en iyi taban hangisi?" sorusunu soruyor.

## Rank

Bir matrisin **rankı**, bağımsız sütunlarının sayısı. Eşdeğer tanımlar:

$$
\operatorname{rank} A = \text{bağımsız sütun sayısı} = \text{pivot sayısı} = \text{sütun uzayının boyutu}
$$

Şaşırtıcı ve önemli bir gerçek: **bağımsız satır sayısı da aynı sayı.**
$\operatorname{rank} A = \operatorname{rank} A^\mathsf{T}$. Eleme her satırı
ya bir pivot satırına ya da sıfır satırına çevirir; pivot sayısı hem
satırlar hem sütunlar için aynı bilgiyi verir.

Örnek:

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{bmatrix}
$$

2. satır 1. satırın 2 katı; bunu elemede de görürüz. $R_2 - 2R_1$ ve
$R_3 - R_1$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{bmatrix}
\;\xrightarrow{R_2 \leftrightarrow R_3}\;
\begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -2 \\ 0 & 0 & 0 \end{bmatrix}
$$

İki pivot: $\operatorname{rank} A = 2$. Üç sütun var ama yalnızca ikisi
bağımsız; üç satır var ama yalnızca ikisi bağımsız.

**Sınırlar:** $m \times n$ bir matriste $\operatorname{rank} A \le
\min(m, n)$. Rank bu sınıra eşitse matrise **tam ranklı** denir. Kare bir
matris tam ranklıysa ($\operatorname{rank} = n$) tersinirdir.

## Çekirdek ve rank–sıfırlık teoremi

$A\mathbf{x} = \mathbf{0}$ denkleminin bütün çözümlerine $A$'nın
**çekirdeği** (sıfır uzayı, null space) denir: $A$'nın sıfıra götürdüğü
vektörler. $\mathbf{x} = \mathbf{0}$ her zaman içinde; soru, başka
vektörlerin de olup olmadığı.

Yukarıdaki $A$ için basamak biçiminden:

$$
\begin{aligned}
x + 2y + 3z &= 0 \\
-y - 2z &= 0
\end{aligned}
$$

$z = t$ serbest: $y = -2t$, $x = -2y - 3z = 4t - 3t = t$. Çekirdek
$t\,(1, -2, 1)$ doğrusu. Sağlama: $A(1, -2, 1) = (1 - 4 + 3,\ 2 - 8 + 6,\ 1 - 2 + 1) = (0, 0, 0)$. ✓

Çekirdeğin boyutu serbest değişken sayısı, rank ise pivot sayısı.
Her sütun ya pivotlu ya serbest olduğu için:

$$
\operatorname{rank} A + \dim(\text{çekirdek}) = n \quad (\text{sütun sayısı})
$$

Buna **rank–sıfırlık teoremi** denir. Örneğimizde $2 + 1 = 3$.

<figure class="fig">
<svg viewBox="0 0 420 210" width="420"><line class="grid" x1="20" y1="182" x2="20" y2="14"/><line class="grid" x1="48" y1="182" x2="48" y2="14"/><line class="grid" x1="76" y1="182" x2="76" y2="14"/><line class="line" x1="104" y1="182" x2="104" y2="14"/><line class="grid" x1="132" y1="182" x2="132" y2="14"/><line class="grid" x1="160" y1="182" x2="160" y2="14"/><line class="grid" x1="188" y1="182" x2="188" y2="14"/><line class="grid" x1="20" y1="182" x2="188" y2="182"/><line class="grid" x1="20" y1="154" x2="188" y2="154"/><line class="grid" x1="20" y1="126" x2="188" y2="126"/><line class="line" x1="20" y1="98" x2="188" y2="98"/><line class="grid" x1="20" y1="70" x2="188" y2="70"/><line class="grid" x1="20" y1="42" x2="188" y2="42"/><line class="grid" x1="20" y1="14" x2="188" y2="14"/><line class="curve2" x1="20.0" y1="56.0" x2="188.0" y2="140.0"/><circle class="dot2" cx="48" cy="70" r="3.5"/><circle class="dot2" cx="160" cy="126" r="3.5"/><text class="ink" x="156" y="144" font-size="11" text-anchor="end">(2, −1)</text><text class="ink" x="104.0" y="200" font-size="11" text-anchor="middle">Çekirdek: Ax = 0 olan noktalar</text><line class="grid" x1="226" y1="182" x2="226" y2="14"/><line class="grid" x1="254" y1="182" x2="254" y2="14"/><line class="grid" x1="282" y1="182" x2="282" y2="14"/><line class="line" x1="310" y1="182" x2="310" y2="14"/><line class="grid" x1="338" y1="182" x2="338" y2="14"/><line class="grid" x1="366" y1="182" x2="366" y2="14"/><line class="grid" x1="394" y1="182" x2="394" y2="14"/><line class="grid" x1="226" y1="182" x2="394" y2="182"/><line class="grid" x1="226" y1="154" x2="394" y2="154"/><line class="grid" x1="226" y1="126" x2="394" y2="126"/><line class="line" x1="226" y1="98" x2="394" y2="98"/><line class="grid" x1="226" y1="70" x2="394" y2="70"/><line class="grid" x1="226" y1="42" x2="394" y2="42"/><line class="grid" x1="226" y1="14" x2="394" y2="14"/><line class="curve" x1="268.0" y1="182.0" x2="352.0" y2="14.0"/><circle class="dot" cx="338" cy="42" r="3.5"/><circle class="dot" cx="282" cy="154" r="3.5"/><circle class="dot" cx="324.0" cy="70" r="3.5"/><text class="ink" x="330" y="38" font-size="11" text-anchor="end">A(1, 0) = (1, 2)</text><text class="ink" x="310.0" y="200" font-size="11" text-anchor="middle">Sütun uzayı: bütün çıktılar</text></svg>
  <figcaption>$A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ için rank 1. Soldaki turuncu doğru üzerindeki her nokta $A$ ile sıfıra gidiyor (çekirdek, boyutu 1). Sağdaki mor doğru, $A$'nın üretebildiği bütün çıktılar (sütun uzayı, boyutu 1). $1 + 1 = 2$ sütun.</figcaption>
</figure>

Geometrik anlamı: $A$ bir yönü tamamen "yok ediyor" (çekirdek) ve kalan
yönleri sütun uzayına taşıyor. Ne kadar çok yön yok olursa sütun uzayı o
kadar küçük kalıyor.

## Rank ve denklem sistemleri

Önceki bölümdeki üç durum rank ile tek cümlede söylenebilir:

| Durum | Rank ile |
|---|---|
| Çözüm var | $\operatorname{rank} A = \operatorname{rank}\,[A \mid \mathbf{b}]$ ($\mathbf{b}$ sütun uzayında) |
| Çözüm yok | $\operatorname{rank}\,[A \mid \mathbf{b}] > \operatorname{rank} A$ |
| Tek çözüm | çözüm var ve $\operatorname{rank} A = n$ (çekirdek yalnızca $\mathbf{0}$) |
| Sonsuz çözüm | çözüm var ve $\operatorname{rank} A < n$ |

Sonsuz çözümde bütün çözümler, **bir** çözümün üstüne çekirdekteki
vektörlerin eklenmesiyle bulunur: $A\mathbf{x}_0 = \mathbf{b}$ ve
$A\mathbf{n} = \mathbf{0}$ ise $A(\mathbf{x}_0 + \mathbf{n}) = \mathbf{b}$.

### Tersinir matris: aynı şeyin altı yüzü

Kare bir $n \times n$ matris $A$ için şu cümlelerin **hepsi birbirine
denk**; biri doğruysa hepsi doğru:

| | |
|---|---|
| 1 | $A$ tersinir |
| 2 | $\det A \ne 0$ |
| 3 | $\operatorname{rank} A = n$ |
| 4 | Sütunlar bağımsız (satırlar da) |
| 5 | Çekirdek yalnızca $\mathbf{0}$ |
| 6 | Her $\mathbf{b}$ için $A\mathbf{x} = \mathbf{b}$'nin tek çözümü var |

Önceki üç bölümde bunları ayrı ayrı gördük; şimdi aynı gerçeğin farklı
yüzleri olduğu ortaya çıkıyor.

## Makine öğrenmesinde rank

**Tekrarlayan özellikler.** Bölümün başındaki ev tablosunda bir sütun
ötekinin 100'e bölünmüşü; veri matrisinin rankı sütun sayısından az.
Önceki bölümde gördüğümüz $X^\mathsf{T}X$'in tekil çıkması tam olarak bu:
$X$ tam ranklı değilse $X^\mathsf{T}X$ tersinmez. Çekirdekteki bir vektör
modelin ağırlıklarına eklenirse tahminler hiç değişmiyor; bu yüzden
ağırlıklar tek değil.

**Gerçek boyut.** Bir veri seti 1000 sütunlu olabilir ama rankı (ya da
yaklaşık rankı) çok daha küçük olabilir: veri aslında daha az boyutlu bir
alt uzayda duruyor. Boyut indirgeme (PCA) bu gerçek boyutu bulup veriyi
o tabanda anlatıyor.

**Düşük ranklı yaklaşım.** Bir film sitesinde kullanıcı × film puan
matrisi milyonlarca hücreli ama zevkler birkaç temel eğilimden (aksiyon
sevmek, romantik komedi sevmek…) oluşuyor. Matris yaklaşık olarak düşük
ranklı; öneri sistemleri bunu kullanıyor. SVD bölümünde bir matrisin en
iyi düşük ranklı yaklaşımını bulacağız.

**Gömme (embedding) boyutu.** Kelimeleri ya da görüntüleri 300 veya 768
boyutlu vektörlerle anlatan modeller, anlamın o kadar bağımsız yönle
yakalanabileceğini varsayıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>Düzlemde üç vektör bağımsız olabilir</p>
      <p>Hiçbiri ötekinin katı değilse bağımsızdır (3+ vektör)</p>
      <p>Rank = sıfır olmayan satır sayısı (elemeden önce)</p>
      <p>Taban tektir</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$n$ boyutta en fazla $n$ bağımsız vektör</p>
      <p>Biri ötekilerin <b>kombinasyonu</b> olabilir; eleme gerek</p>
      <p>Rank = elemeden sonraki pivot sayısı</p>
      <p>Her uzayın sonsuz tabanı var; boyutları aynı</p>
    </div>
  </div>
  <figcaption>Üç vektörün ikişer ikişer "paralel olmaması" bağımsızlık için yetmez: $(1, 2, 1)$, $(2, 1, 0)$ ve toplamları $(3, 3, 1)$ ikişer ikişer paralel değil ama bağımlı.</figcaption>
</figure>

- **Rankı elemeden okumaya çalışmak.** Bağımlılık gözle görülmeyebilir;
  pivotları saymak en güvenli yol.
- **Satır rankı ile sütun rankını ayrı sanmak.** Her zaman eşitler.
- **Çekirdeği boş sanmak.** Çekirdek her zaman $\mathbf{0}$'ı içerir; soru
  başka bir şey içerip içermediği.

## Özet

- Germe: vektörlerin bütün kombinasyonları. $A$'nın sütunlarının germesi = sütun uzayı = $A\mathbf{x}$'in bütün değerleri.
- Bağımsızlık: $c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k = \mathbf{0}$'ın tek çözümü $\mathbf{c} = \mathbf{0}$. Sınama: her sütunda pivot; kare ise $\det \ne 0$.
- $n$ boyutta $n$'den fazla vektör her zaman bağımlı.
- Taban: geren ve bağımsız grup. Boyut = tabandaki vektör sayısı. Her vektörün bir tabanda tek koordinatı var.
- Rank = bağımsız sütun sayısı = pivot sayısı = bağımsız satır sayısı; $\le \min(m, n)$.
- Çekirdek: $A\mathbf{x} = \mathbf{0}$'ın çözümleri. $\operatorname{rank} A + \dim(\text{çekirdek}) = n$.
- Kare $A$: tersinir $\iff \det \ne 0 \iff$ rank $n$ $\iff$ sütunlar bağımsız $\iff$ çekirdek $\{\mathbf{0}\}$.
- ML: tekrarlayan özellik $\Rightarrow$ düşük rank, tek olmayan ağırlıklar; verinin gerçek boyutu; düşük ranklı yaklaşım.
