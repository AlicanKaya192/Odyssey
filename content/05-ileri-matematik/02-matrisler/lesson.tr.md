# Matrisler

Elinde üç evin bilgisi olsun: her birinin metrekaresi, oda sayısı ve
yaşı. Önceki bölümlerde her evi bir vektörle anlattık. Üç vektörü alt
alta yazınca ortaya bir **tablo** çıkıyor:

| | Metrekare | Oda | Yaş |
|---|---|---|---|
| 1. ev | 120 | 3 | 10 |
| 2. ev | 80 | 2 | 25 |
| 3. ev | 150 | 4 | 5 |

Bu tablonun sayılardan oluşan gövdesi bir **matris**. Makine öğrenmesinde
veri neredeyse her zaman böyle durur: her satır bir örnek (bir ev, bir
müşteri, bir fotoğraf), her sütun bir özellik. Bir sinir ağının
öğrendiği ağırlıklar da, bir fotoğrafın pikselleri de matris.

Bu bölümde matrisin ne olduğunu, nasıl okunduğunu, özel matrisleri,
matrislerle toplama ve skalerle çarpmayı, **devriği** ve bir matrisin bir
vektörle nasıl çarpıldığını göreceğiz. İki matrisin birbiriyle çarpımı ve
matrislerin düzlemi nasıl döndürüp esnettiği bir sonraki bölümde.

Ön bilgi: Vektörler ve Nokta Çarpımı bölümleri.

## Tanım ve gösterim

**Matris**, sayıların satır ve sütunlara dizildiği dikdörtgen bir
tablodur. Büyük harfle adlandırılır ve köşeli parantez içinde yazılır:

$$
A = \begin{bmatrix} 5 & 2 & 0 & 1 \\ 3 & 7 & 4 & 6 \\ 1 & 8 & 9 & 2 \end{bmatrix}
$$

### Boyut: önce satır, sonra sütun

$A$'da 3 satır ve 4 sütun var; boyutu **$3 \times 4$** ("üçe dört")
yazılır. Sıra hep aynı: **önce satır, sonra sütun**. $4 \times 3$ bir
matris başka bir şekil: 4 satır, 3 sütun.

Boyutu $m \times n$ olan gerçek sayılı matrislerin kümesi
$\mathbb{R}^{m \times n}$ diye yazılır; $A \in \mathbb{R}^{3 \times 4}$.

### Eleman: $a_{ij}$

Matrisin her sayısına **eleman** denir. $i$. satır ile $j$. sütunun
kesiştiği eleman küçük harfle ve iki alt simgeyle yazılır: $a_{ij}$.
Burada da sıra aynı: **önce satır numarası, sonra sütun numarası**.

<figure class="fig">
<svg viewBox="0 0 400 224" width="400"><rect class="box" x="110" y="44" width="38" height="38"/><text class="ink" x="129.0" y="68.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="148" y="44" width="38" height="38"/><text class="ink" x="167.0" y="68.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="186" y="44" width="38" height="38"/><text class="ink" x="205.0" y="68.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="224" y="44" width="38" height="38"/><text class="ink" x="243.0" y="68.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="110" y="82" width="38" height="38"/><text class="ink" x="129.0" y="106.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="148" y="82" width="38" height="38"/><text class="ink" x="167.0" y="106.0" font-size="15" text-anchor="middle">7</text><rect class="box" x="186" y="82" width="38" height="38"/><text class="ink" x="205.0" y="106.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="224" y="82" width="38" height="38"/><text class="ink" x="243.0" y="106.0" font-size="15" text-anchor="middle">6</text><rect class="box" x="110" y="120" width="38" height="38"/><text class="ink" x="129.0" y="144.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="148" y="120" width="38" height="38"/><text class="ink" x="167.0" y="144.0" font-size="15" text-anchor="middle">8</text><rect class="box" x="186" y="120" width="38" height="38"/><text class="ink" x="205.0" y="144.0" font-size="15" text-anchor="middle">9</text><rect class="box" x="224" y="120" width="38" height="38"/><text class="ink" x="243.0" y="144.0" font-size="15" text-anchor="middle">2</text><rect class="curve" x="107" y="79" width="158" height="44" rx="4"/><rect class="curve2" x="183" y="41" width="44" height="120" rx="4"/><text class="ink" x="98" y="106.0" font-size="13" text-anchor="end">2. satır</text><text class="ink" x="205.0" y="30" font-size="13" text-anchor="middle">3. sütun</text><text class="ink" x="205.0" y="184" font-size="14" text-anchor="middle">a₂₃ = 4</text><text class="dim" x="186" y="210" font-size="12" text-anchor="middle">3 satır × 4 sütun</text></svg>
  <figcaption>Mor çerçeve 2. satır, turuncu çerçeve 3. sütun. Kesiştikleri eleman $a_{23} = 4$.</figcaption>
</figure>

Aynı matriste $a_{11} = 5$ (sol üst köşe), $a_{14} = 1$ (ilk satırın
sonu), $a_{32} = 8$. $a_{23}$ ile $a_{32}$ farklı elemanlar: biri
"2. satır 3. sütun", öteki "3. satır 2. sütun".

Genel bir $m \times n$ matris:

$$
A = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
$$

Kısaca $A = [a_{ij}]$ diye de yazılır.

**Tek satırda yazmak.** Formül yazılamayan yerlerde (düz metin, kod,
bu bölümün sınav soruları) matris satır satır, satırlar **noktalı
virgülle** ayrılarak yazılır: `[1 2; 3 4]`, 1. satırı $(1, 2)$ ve 2. satırı
$(3, 4)$ olan $2 \times 2$ matris. `[1; 2]` iki satırlı bir sütun,
`[1 2]` tek satırlık bir satır vektörü.

### Satırlar ve sütunlar birer vektör

Bir matrisin her satırı bir vektör, her sütunu da bir vektör. Ev
tablosunda 1. satır $(120, 3, 10)$, yani 1. evin özellik vektörü;
1. sütun $(120, 80, 150)$, yani bütün evlerin metrekareleri. Bir matrise
**satır vektörlerinin alt alta dizilmesi** ya da **sütun vektörlerinin
yan yana dizilmesi** olarak bakılabilir. İkisi de doğru ve bu bölümün
sonunda ikisine de ihtiyacımız olacak.

**Vektör de bir matris:** $n$ bileşenli bir vektör, $n \times 1$ boyutlu
bir **sütun vektörü** olarak yazılır. Tek satırlık $1 \times n$ bir
matrise **satır vektörü** denir.

$$
\mathbf{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \;(3 \times 1)
\qquad
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix} \;(1 \times 3)
$$

Doğrusal cebirde "vektör" denince aksi söylenmedikçe **sütun vektörü**
anlaşılır.

## Özel matrisler

Bazı matrisler o kadar sık geçiyor ki kendi adları var.

| Adı | Tanımı | Örnek |
|---|---|---|
| Kare matris | Satır sayısı = sütun sayısı ($n \times n$) | $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ |
| Sıfır matris $O$ | Bütün elemanları $0$ | $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$ |
| Köşegen matris | Kare; köşegen dışındaki her eleman $0$ | $\begin{bmatrix} 3 & 0 \\ 0 & -1 \end{bmatrix}$ |
| Birim matris $I$ | Köşegen matris; köşegeni tamamen $1$ | $\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ |
| Üst üçgen | Kare; köşegenin altı $0$ | $\begin{bmatrix} 2 & 5 \\ 0 & 7 \end{bmatrix}$ |
| Alt üçgen | Kare; köşegenin üstü $0$ | $\begin{bmatrix} 2 & 0 \\ 5 & 7 \end{bmatrix}$ |
| Simetrik | Kare; $a_{ij} = a_{ji}$ | $\begin{bmatrix} 2 & 7 \\ 7 & 5 \end{bmatrix}$ |

**Köşegen** (asıl köşegen) derken sol üstten sağ alta inen elemanlar
kastediliyor: $a_{11}, a_{22}, a_{33}, \dots$ Yalnızca kare matrislerde
anlamlı.

**Birim matris** $I$, sayılardaki $1$'in matris dünyasındaki karşılığı:
bir vektörü onunla çarpınca vektör değişmiyor (bunu bu bölümün sonunda
göreceğiz). Boyutu belirtmek gerekirse $I_3$ yazılır:

$$
I_3 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

**Simetrik** matris köşegene göre aynadaki görüntüsüyle aynı. Uzaklık
tabloları simetrik: İstanbul–Ankara uzaklığı Ankara–İstanbul uzaklığına
eşit. İstatistik bölümlerinde göreceğimiz **kovaryans matrisi** de hep
simetrik.

## Eşitlik

İki matris **ancak ve ancak** aynı boyuttaysa ve karşılıklı bütün
elemanları eşitse eşittir.

$$
\begin{bmatrix} x & 3 \\ 1 & y \end{bmatrix} = \begin{bmatrix} 5 & 3 \\ 1 & -2 \end{bmatrix}
\;\Rightarrow\; x = 5,\; y = -2
$$

$\begin{bmatrix} 1 & 2 \end{bmatrix}$ ile $\begin{bmatrix} 1 \\ 2 \end{bmatrix}$
aynı sayıları içerse de eşit **değil**: biri $1 \times 2$, öteki
$2 \times 1$.

## Toplama ve çıkarma

Aynı boyuttaki iki matris **eleman eleman** toplanır; karşılıklı yerdeki
sayılar toplanıp aynı yere yazılır:

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\qquad
B = \begin{bmatrix} 5 & 0 \\ 1 & 2 \end{bmatrix}
$$

$$
A + B = \begin{bmatrix} 1 + 5 & 2 + 0 \\ 3 + 1 & 4 + 2 \end{bmatrix} = \begin{bmatrix} 6 & 2 \\ 4 & 6 \end{bmatrix}
$$

Çıkarma da aynı: $A - B = \begin{bmatrix} -4 & 2 \\ 2 & 2 \end{bmatrix}$.

Vektör toplamasının tıpatıp aynısı; matris yalnızca daha fazla bileşeni
olan bir vektör gibi davranıyor. Farklı boyutlu iki matris
**toplanamaz** ($2 \times 3$ ile $3 \times 2$ bile): bazı elemanların eşi
kalmaz.

Sayılardaki kurallar geçerli:

| Kural | Yazılış |
|---|---|
| Değişme | $A + B = B + A$ |
| Birleşme | $(A + B) + C = A + (B + C)$ |
| Sıfır matris | $A + O = A$ |
| Ters | $A + (-A) = O$ |

**Anlamı:** İki ayın satış tablosu (satır = mağaza, sütun = ürün)
toplanınca iki aylık toplam satış tablosu çıkıyor. İki fotoğrafın
ortalamasını almak da eleman eleman toplayıp ikiye bölmek.

## Skalerle çarpma

Bir matrisi bir sayıyla çarpmak her elemanı o sayıyla çarpmak demek:

$$
3A = 3 \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} = \begin{bmatrix} 3 & 6 \\ 9 & 12 \end{bmatrix}
$$

Yine vektördekiyle aynı. Fiyat tablosunun bütün elemanlarını $1.2$ ile
çarpmak her fiyata %20 zam yapmak. Kurallar:

| Kural | Yazılış |
|---|---|
| Dağılma | $c(A + B) = cA + cB$ |
| Dağılma | $(c + d)A = cA + dA$ |
| Birleşme | $c(dA) = (cd)A$ |

Toplama ve skalerle çarpma birlikte **doğrusal kombinasyon** kurar:
$2A - B$, $\tfrac{1}{2}(A + B)$ gibi.

## Devrik (transpoz)

Bir matrisin **devriği**, satırlarının sütun, sütunlarının satır olduğu
matristir. $A^\mathsf{T}$ diye yazılır ("A devrik").

<figure class="fig">
<svg viewBox="0 0 400 173" width="400"><rect class="box" x="30" y="62" width="38" height="38"/><text class="ink" x="49.0" y="86.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="68" y="62" width="38" height="38"/><text class="ink" x="87.0" y="86.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="106" y="62" width="38" height="38"/><text class="ink" x="125.0" y="86.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="30" y="100" width="38" height="38"/><text class="ink" x="49.0" y="124.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="68" y="100" width="38" height="38"/><text class="ink" x="87.0" y="124.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="106" y="100" width="38" height="38"/><text class="ink" x="125.0" y="124.0" font-size="15" text-anchor="middle">6</text><rect class="box" x="290" y="43" width="38" height="38"/><text class="ink" x="309.0" y="67.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="328" y="43" width="38" height="38"/><text class="ink" x="347.0" y="67.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="290" y="81" width="38" height="38"/><text class="ink" x="309.0" y="105.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="328" y="81" width="38" height="38"/><text class="ink" x="347.0" y="105.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="290" y="119" width="38" height="38"/><text class="ink" x="309.0" y="143.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="328" y="119" width="38" height="38"/><text class="ink" x="347.0" y="143.0" font-size="15" text-anchor="middle">6</text><rect class="curve" x="27" y="59" width="120" height="39" rx="4"/><rect class="curve2" x="27" y="102" width="120" height="39" rx="4"/><rect class="curve" x="287" y="40" width="39" height="120" rx="4"/><rect class="curve2" x="330" y="40" width="39" height="120" rx="4"/><text class="ink" x="87.0" y="46" font-size="13" text-anchor="middle">A  (2 × 3)</text><text class="ink" x="328" y="27" font-size="13" text-anchor="middle">Aᵀ  (3 × 2)</text><line class="curve3" x1="166" y1="100" x2="259" y2="100"/><polygon class="dim" points="268,100 257,95 257,105"/></svg>
  <figcaption>$A$'nın 1. satırı (mor) $A^\mathsf{T}$'nin 1. sütunu, 2. satırı (turuncu) 2. sütunu oluyor. $2 \times 3$ bir matrisin devriği $3 \times 2$.</figcaption>
</figure>

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\qquad
A^\mathsf{T} = \begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}
$$

Eleman diliyle: devrikte $i$. satır $j$. sütundaki eleman, asıl matrisin
$j$. satır $i$. sütunundaki eleman.

$$
(A^\mathsf{T})_{ij} = a_{ji}
$$

$m \times n$ bir matrisin devriği $n \times m$. Kare matriste devrik,
matrisi **köşegen etrafında aynalamak**: köşegen yerinde kalıyor, öteki
elemanlar karşı taraftaki eşleriyle yer değiştiriyor.

### Devriğin kuralları

| Kural | Yazılış |
|---|---|
| İki kez devrik | $(A^\mathsf{T})^\mathsf{T} = A$ |
| Toplam | $(A + B)^\mathsf{T} = A^\mathsf{T} + B^\mathsf{T}$ |
| Skaler | $(cA)^\mathsf{T} = c\,A^\mathsf{T}$ |
| Simetrik | $A$ simetrik $\iff A^\mathsf{T} = A$ |

**Sütun vektörünün devriği satır vektörü:**

$$
\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}^\mathsf{T} = \begin{bmatrix} 1 & 2 & 3 \end{bmatrix}
$$

Kitaplarda satır vektörünü ayrıca yazmak yerine $\mathbf{x}^\mathsf{T}$
yazılıyor. İki sütun vektörünün nokta çarpımı da bu yüzden sık sık
$\mathbf{a}^\mathsf{T} \mathbf{b}$ diye görünür: satır vektörü çarpı
sütun vektörü, sonuç tek bir sayı.

## Matris ile vektör çarpımı

Bir matrisi bir vektörle çarpmanın iki bakışı var. İkisi aynı sonucu
veriyor ama farklı şeyler anlatıyor.

### Boyut kuralı

$m \times n$ bir matris ancak **$n$ bileşenli** bir vektörle çarpılabilir
ve sonuç **$m$ bileşenli** bir vektör olur:

$$
\underbrace{A}_{m \times n}\;\underbrace{\mathbf{x}}_{n \times 1} = \underbrace{\mathbf{y}}_{m \times 1}
$$

Matrisin **sütun sayısı**, vektörün **bileşen sayısına** eşit olmalı.
Sonucun boyu matrisin **satır sayısı**.

### Satır bakışı: her satırla nokta çarpımı

Sonucun $i$. bileşeni, $A$'nın $i$. satırı ile $\mathbf{x}$'in nokta
çarpımıdır:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix}
= \begin{bmatrix} 1 \cdot 1 + 2 \cdot 0 + 3 \cdot (-1) \\ 4 \cdot 1 + 5 \cdot 0 + 6 \cdot (-1) \end{bmatrix}
= \begin{bmatrix} -2 \\ -2 \end{bmatrix}
$$

$2 \times 3$ matris, 3 bileşenli vektör, 2 bileşenli sonuç. Önceki
bölümün nokta çarpımı burada her satır için bir kez tekrarlanıyor.

### Sütun bakışı: sütunların doğrusal kombinasyonu

Aynı çarpım, $A$'nın **sütunlarının** $\mathbf{x}$'in bileşenleriyle
ağırlıklandırılmış toplamıdır:

$$
A\mathbf{x} = x_1\,\mathbf{a}_1 + x_2\,\mathbf{a}_2 + \cdots + x_n\,\mathbf{a}_n
$$

Burada $\mathbf{a}_j$, $A$'nın $j$. sütunu. Örnek:

$$
\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
\begin{bmatrix} 1 \\ 2 \end{bmatrix}
= 1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + 2 \begin{bmatrix} -1 \\ 1 \end{bmatrix}
= \begin{bmatrix} 0 \\ 3 \end{bmatrix}
$$

<figure class="fig">
<svg viewBox="0 0 252 252" width="252"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="grid" x1="66" y1="226" x2="66" y2="26"/><line class="line" x1="106" y1="226" x2="106" y2="26"/><line class="grid" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="26" y1="226" x2="226" y2="226"/><line class="line" x1="26" y1="186" x2="226" y2="186"/><line class="grid" x1="26" y1="146" x2="226" y2="146"/><line class="grid" x1="26" y1="106" x2="226" y2="106"/><line class="grid" x1="26" y1="66" x2="226" y2="66"/><line class="grid" x1="26" y1="26" x2="226" y2="26"/><text class="dim" x="26" y="200" font-size="10" text-anchor="middle">-2</text><text class="dim" x="66" y="200" font-size="10" text-anchor="middle">-1</text><text class="dim" x="146" y="200" font-size="10" text-anchor="middle">1</text><text class="dim" x="186" y="200" font-size="10" text-anchor="middle">2</text><text class="dim" x="226" y="200" font-size="10" text-anchor="middle">3</text><text class="dim" x="100" y="230" font-size="10" text-anchor="end">-1</text><text class="dim" x="100" y="150" font-size="10" text-anchor="end">1</text><text class="dim" x="100" y="110" font-size="10" text-anchor="end">2</text><text class="dim" x="100" y="70" font-size="10" text-anchor="end">3</text><text class="dim" x="100" y="30" font-size="10" text-anchor="end">4</text><line class="curve4" x1="106" y1="186" x2="106.0" y2="74.8"/><polygon class="dot3" points="106,66 110.5,76.0 101.5,76.0"/><line class="curve" x1="106" y1="186" x2="178.1" y2="149.9"/><polygon class="dot" points="186,146 179.0,154.5 175.0,146.5"/><line class="curve2" x1="186" y1="146" x2="112.2" y2="72.2"/><polygon class="dot2" points="106,66 116.3,69.9 109.9,76.3"/><text class="ink" x="194" y="152" font-size="13" text-anchor="start">1 · a₁</text><text class="ink" x="154" y="102" font-size="13" text-anchor="start">2 · a₂</text><text class="ink" x="116" y="58" font-size="14" text-anchor="start">Ax</text></svg>
  <figcaption>Önce 1. sütun $(2, 1)$ kadar (mor), sonra 2. sütunun iki katı $(-2, 2)$ kadar (turuncu) yürü. Vardığın nokta $A\mathbf{x} = (0, 3)$ (yeşil).</figcaption>
</figure>

Satır bakışıyla sağlama: $2 \cdot 1 + (-1) \cdot 2 = 0$ ve
$1 \cdot 1 + 1 \cdot 2 = 3$. ✓

Sütun bakışı çok önemli bir şey söylüyor: **$A\mathbf{x}$ her zaman
$A$'nın sütunlarından kurulabilen bir vektördür.** "Hangi $\mathbf{x}$ için
$A\mathbf{x} = \mathbf{b}$ olur?" sorusu, "$\mathbf{b}$'yi sütunlardan hangi
katsayılarla kurarım?" sorusuyla aynı. Vektörler bölümündeki "katsayıları
bul" problemi tam olarak buydu; Gauss eleme bölümünde bu soruyu düzenli
olarak çözeceğiz.

### Birim matrisle çarpma

$$
I\mathbf{x} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 7 \\ -3 \end{bmatrix}
= 7 \begin{bmatrix} 1 \\ 0 \end{bmatrix} - 3 \begin{bmatrix} 0 \\ 1 \end{bmatrix}
= \begin{bmatrix} 7 \\ -3 \end{bmatrix}
$$

Birim matrisin sütunları temel birim vektörler; onlardan $\mathbf{x}$'i
kurmak için katsayılar $\mathbf{x}$'in kendi bileşenleri. Bu yüzden
$I\mathbf{x} = \mathbf{x}$.

### Kurallar

| Kural | Yazılış |
|---|---|
| Vektörlere dağılma | $A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}$ |
| Skaler dışarı çıkar | $A(c\,\mathbf{x}) = c\,(A\mathbf{x})$ |
| Matrislere dağılma | $(A + B)\mathbf{x} = A\mathbf{x} + B\mathbf{x}$ |

İlk iki kural, matrisle çarpmanın **doğrusal** bir işlem olduğunu
söylüyor. "Doğrusal cebir" adı buradan geliyor.

## Makine öğrenmesinde matrisler

**Veri matrisi.** $n$ örnek ve $d$ özellik varsa veri $n \times d$ bir
matris: $X \in \mathbb{R}^{n \times d}$. Satır $i$, $i$. örneğin özellik
vektörü; sütun $j$, $j$. özelliğin bütün örneklerdeki değerleri.

**Bütün tahminler tek çarpımda.** Doğrusal bir modelin ağırlık vektörü
$\mathbf{w}$ ise, bir örneğin tahmini o örneğin satırıyla $\mathbf{w}$'nin
nokta çarpımı. Satır bakışına göre bu, $X\mathbf{w}$'nin tam olarak
yaptığı şey:

$$
X = \begin{bmatrix} 1.2 & 3 \\ 0.8 & 2 \\ 1.5 & 4 \end{bmatrix}
\qquad
\mathbf{w} = \begin{bmatrix} 100 \\ 20 \end{bmatrix}
\qquad
X\mathbf{w} = \begin{bmatrix} 180 \\ 120 \\ 230 \end{bmatrix}
$$

Birinci sütun yüz metrekare biriminde alan, ikinci sütun oda sayısı;
tahminler bin lira cinsinden fiyat. Birinci evin tahmini
$1.2 \cdot 100 + 3 \cdot 20 = 180$. Üç evin fiyatı tek bir matris–vektör çarpımıyla
bulundu. Bir milyon ev olsa da yazılış aynı: $\hat{\mathbf{y}} = X\mathbf{w}$.

**Görüntüler.** Gri tonlu bir fotoğraf, her pikselin parlaklığını tutan
bir matris. $28 \times 28$ piksellik bir el yazısı rakamı 784 sayılık bir
matris; renkli bir fotoğraf her renk kanalı (kırmızı, yeşil, mavi) için
bir tane olmak üzere üç matris.

<figure class="fig">
<svg viewBox="0 0 400 190" width="400"><rect class="box" x="20" y="20" width="30" height="30"/><rect class="ink" x="20" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="50" y="20" width="30" height="30"/><rect class="ink" x="50" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="80" y="20" width="30" height="30"/><rect class="ink" x="80" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="110" y="20" width="30" height="30"/><rect class="ink" x="110" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="140" y="20" width="30" height="30"/><rect class="ink" x="140" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="20" y="50" width="30" height="30"/><rect class="box" x="50" y="50" width="30" height="30"/><rect class="box" x="80" y="50" width="30" height="30"/><rect class="box" x="110" y="50" width="30" height="30"/><rect class="ink" x="110" y="50" width="30" height="30" opacity="0.78"/><rect class="box" x="140" y="50" width="30" height="30"/><rect class="ink" x="140" y="50" width="30" height="30" opacity="0.22"/><rect class="box" x="20" y="80" width="30" height="30"/><rect class="box" x="50" y="80" width="30" height="30"/><rect class="box" x="80" y="80" width="30" height="30"/><rect class="ink" x="80" y="80" width="30" height="30" opacity="0.67"/><rect class="box" x="110" y="80" width="30" height="30"/><rect class="ink" x="110" y="80" width="30" height="30" opacity="0.33"/><rect class="box" x="140" y="80" width="30" height="30"/><rect class="box" x="20" y="110" width="30" height="30"/><rect class="box" x="50" y="110" width="30" height="30"/><rect class="ink" x="50" y="110" width="30" height="30" opacity="0.56"/><rect class="box" x="80" y="110" width="30" height="30"/><rect class="ink" x="80" y="110" width="30" height="30" opacity="0.44"/><rect class="box" x="110" y="110" width="30" height="30"/><rect class="box" x="140" y="110" width="30" height="30"/><rect class="box" x="20" y="140" width="30" height="30"/><rect class="box" x="50" y="140" width="30" height="30"/><rect class="ink" x="50" y="140" width="30" height="30" opacity="1.0"/><rect class="box" x="80" y="140" width="30" height="30"/><rect class="box" x="110" y="140" width="30" height="30"/><rect class="box" x="140" y="140" width="30" height="30"/><rect class="box" x="230" y="20" width="30" height="30"/><text class="ink" x="245.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="260" y="20" width="30" height="30"/><text class="ink" x="275.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="290" y="20" width="30" height="30"/><text class="ink" x="305.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="320" y="20" width="30" height="30"/><text class="ink" x="335.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="350" y="20" width="30" height="30"/><text class="ink" x="365.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="230" y="50" width="30" height="30"/><text class="dim" x="245.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="50" width="30" height="30"/><text class="dim" x="275.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="290" y="50" width="30" height="30"/><text class="dim" x="305.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="320" y="50" width="30" height="30"/><text class="ink" x="335.0" y="70.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="350" y="50" width="30" height="30"/><text class="ink" x="365.0" y="70.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="230" y="80" width="30" height="30"/><text class="dim" x="245.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="80" width="30" height="30"/><text class="dim" x="275.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="290" y="80" width="30" height="30"/><text class="ink" x="305.0" y="100.0" font-size="14" text-anchor="middle">6</text><rect class="box" x="320" y="80" width="30" height="30"/><text class="ink" x="335.0" y="100.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="350" y="80" width="30" height="30"/><text class="dim" x="365.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="230" y="110" width="30" height="30"/><text class="dim" x="245.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="110" width="30" height="30"/><text class="ink" x="275.0" y="130.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="290" y="110" width="30" height="30"/><text class="ink" x="305.0" y="130.0" font-size="14" text-anchor="middle">4</text><rect class="box" x="320" y="110" width="30" height="30"/><text class="dim" x="335.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="350" y="110" width="30" height="30"/><text class="dim" x="365.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="230" y="140" width="30" height="30"/><text class="dim" x="245.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="140" width="30" height="30"/><text class="ink" x="275.0" y="160.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="290" y="140" width="30" height="30"/><text class="dim" x="305.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="320" y="140" width="30" height="30"/><text class="dim" x="335.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="350" y="140" width="30" height="30"/><text class="dim" x="365.0" y="160.0" font-size="14" text-anchor="middle">0</text><line class="curve3" x1="182" y1="95.0" x2="209" y2="95.0"/><polygon class="dim" points="218,95.0 207,90.0 207,100.0"/></svg>
  <figcaption>Solda $5 \times 5$ piksellik bir "7", sağda aynı görüntünün sayıları (0 boş, 9 en koyu). Bilgisayar görüntüyü sağdaki gibi görür.</figcaption>
</figure>

Fotoğrafı daha parlak yapmak skalerle çarpma, iki fotoğrafın ortalaması
toplama ve skalerle çarpma, fotoğrafı köşegen boyunca çevirmek devrik.

**Sinir ağı katmanı.** Bir katmandaki her nöron girdilerle kendi
ağırlıklarının nokta çarpımını hesaplıyor. Bütün nöronların ağırlıkları
bir matrisin satırlarına dizilince katmanın tamamı tek bir $W\mathbf{x}$
çarpımı oluyor.

## İz (trace)

Kare bir matrisin **izi**, köşegen elemanlarının toplamı:

$$
\operatorname{tr}\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix} = 4 + 3 = 7
$$

Şimdilik yalnızca bir tanım; özdeğerler bölümünde izin özdeğerlerin
toplamına eşit olduğunu göreceğiz.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$3 \times 4$: 3 sütun, 4 satır</p>
      <p>$a_{23}$: 2. sütun, 3. satır</p>
      <p>$2 \times 3$ ile $3 \times 2$ matris toplanır</p>
      <p>$2 \times 3$ matris çarpı 2 bileşenli vektör</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$3 \times 4$: 3 satır, 4 sütun</p>
      <p>$a_{23}$: 2. satır, 3. sütun</p>
      <p>Toplama için boyutlar birebir aynı olmalı</p>
      <p>$2 \times 3$ matris 3 bileşenli vektörle çarpılır</p>
    </div>
  </div>
  <figcaption>Boyutta ve alt simgede sıra hep aynı: önce satır, sonra sütun.</figcaption>
</figure>

- **Satır ile sütunu karıştırmak.** Boyut da eleman da önce satırı söyler.
- **Devriği yalnızca yer değiştirme sanmak.** $2 \times 3$ bir matrisin
  devriği yine $2 \times 3$ değil, $3 \times 2$.
- **Matris–vektör çarpımında boyutu kontrol etmemek.** Matrisin sütun
  sayısı vektörün bileşen sayısına eşit değilse çarpım tanımsız.
- **Sonucun boyunu karıştırmak.** Sonuç, matrisin satır sayısı kadar
  bileşenli.

## Özet

- Matris: satır ve sütunlara dizilmiş sayılar. Boyut $m \times n$, önce satır.
- $a_{ij}$: $i$. satır, $j$. sütun.
- Özel matrisler: kare, sıfır, köşegen, birim $I$, üçgen, simetrik.
- Toplama ve skalerle çarpma eleman eleman; toplama için boyutlar aynı olmalı.
- Devrik: satırlar sütun olur, $(A^\mathsf{T})_{ij} = a_{ji}$, boyut $n \times m$.
- $A\mathbf{x}$: satır bakışıyla her satırla nokta çarpımı; sütun bakışıyla sütunların doğrusal kombinasyonu.
- Boyut kuralı: $(m \times n)$ çarpı $n$ bileşen $=$ $m$ bileşen.
- ML: veri matrisi $X$, bütün tahminler $X\mathbf{w}$, görüntüler, sinir ağı katmanı $W\mathbf{x}$.
