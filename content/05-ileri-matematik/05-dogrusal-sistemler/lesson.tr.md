# Doğrusal Sistemler ve Gauss Eleme

Bir önceki bölümde $A\mathbf{x} = \mathbf{b}$ denklemini ters matrisle
çözdük: $\mathbf{x} = A^{-1}\mathbf{b}$. Güzel bir formül, ama iki sorunu
var. Birincisi, ters matris hesaplamak büyük matrislerde yavaş. İkincisi,
determinant sıfır olunca formül hiçbir şey söylemiyor: sistemin **hiç**
çözümü mü yok, yoksa **sonsuz** çözümü mü var?

Bu bölümde her iki soruya da cevap veren yöntemi öğreneceğiz: **Gauss
eleme**. Ortaokulda iki denklemi toplayıp bir bilinmeyeni yok ettiğin
yöntemin düzenli, her boyutta çalışan hâli. Bilgisayarların doğrusal
sistemleri çözerken kullandığı yöntem de bu.

Ön bilgi: Determinant ve Ters Matris bölümü.

## Doğrusal sistem nedir?

Bilinmeyenlerin yalnızca birinci kuvvetle geçtiği ve birbirleriyle
çarpılmadığı denklemlere **doğrusal** denklem denir. Birkaç doğrusal
denklem bir arada **doğrusal sistem** oluşturur:

$$
\begin{aligned}
x + y + z &= 6 \\
2x + 3y - z &= 5 \\
x - y + 2z &= 5
\end{aligned}
$$

$x^2$, $xy$, $\sin x$ gibi terimler olsaydı sistem doğrusal olmazdı.

### Matris biçimi ve artırılmış matris

Katsayılar bir matrise, bilinmeyenler bir vektöre, sağ taraflar başka bir
vektöre gider: $A\mathbf{x} = \mathbf{b}$.

$$
\begin{bmatrix} 1 & 1 & 1 \\ 2 & 3 & -1 \\ 1 & -1 & 2 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix}
= \begin{bmatrix} 6 \\ 5 \\ 5 \end{bmatrix}
$$

Elle çözerken $x, y, z$ harflerini her satırda tekrar yazmaya gerek yok.
Katsayı matrisinin yanına sağ tarafı bir çizgiyle ekleyince **artırılmış
matris** çıkıyor:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & -1 & 5 \\ 1 & -1 & 2 & 5 \end{array}\right]
$$

Her satır bir denklem, çizginin solundaki her sütun bir bilinmeyenin
katsayıları, sağdaki sütun sağ taraf.

## Üç olasılık

İki bilinmeyenli bir denklem düzlemde bir doğru. İki denklemli bir
sistemin çözümü, iki doğrunun **ortak noktaları**. İki doğru üç farklı
şekilde durabilir:

<figure class="fig">
<svg viewBox="0 0 420 192" width="420"><line class="grid" x1="14" y1="134" x2="14" y2="14"/><line class="line" x1="38" y1="134" x2="38" y2="14"/><line class="grid" x1="62" y1="134" x2="62" y2="14"/><line class="grid" x1="86" y1="134" x2="86" y2="14"/><line class="grid" x1="110" y1="134" x2="110" y2="14"/><line class="grid" x1="134" y1="134" x2="134" y2="14"/><line class="grid" x1="14" y1="134" x2="134" y2="134"/><line class="line" x1="14" y1="110" x2="134" y2="110"/><line class="grid" x1="14" y1="86" x2="134" y2="86"/><line class="grid" x1="14" y1="62" x2="134" y2="62"/><line class="grid" x1="14" y1="38" x2="134" y2="38"/><line class="grid" x1="14" y1="14" x2="134" y2="14"/><line class="curve" x1="14" y1="14.0" x2="134" y2="134.0"/><line class="curve2" x1="38.0" y1="134" x2="134" y2="38.0"/><circle class="dot3" cx="86" cy="86" r="4.5"/><text class="ink" x="74.0" y="152" font-size="12" text-anchor="middle">Tek çözüm</text><text class="dim" x="74.0" y="168" font-size="11" text-anchor="middle">x + y = 3</text><text class="dim" x="74.0" y="182" font-size="11" text-anchor="middle">x − y = 1</text><line class="grid" x1="152" y1="134" x2="152" y2="14"/><line class="line" x1="176" y1="134" x2="176" y2="14"/><line class="grid" x1="200" y1="134" x2="200" y2="14"/><line class="grid" x1="224" y1="134" x2="224" y2="14"/><line class="grid" x1="248" y1="134" x2="248" y2="14"/><line class="grid" x1="272" y1="134" x2="272" y2="14"/><line class="grid" x1="152" y1="134" x2="272" y2="134"/><line class="line" x1="152" y1="110" x2="272" y2="110"/><line class="grid" x1="152" y1="86" x2="272" y2="86"/><line class="grid" x1="152" y1="62" x2="272" y2="62"/><line class="grid" x1="152" y1="38" x2="272" y2="38"/><line class="grid" x1="152" y1="14" x2="272" y2="14"/><line class="curve" x1="152" y1="14.0" x2="272" y2="134.0"/><line class="curve2" x1="152" y1="62.0" x2="224.0" y2="134"/><text class="ink" x="212.0" y="152" font-size="12" text-anchor="middle">Çözüm yok</text><text class="dim" x="212.0" y="168" font-size="11" text-anchor="middle">x + y = 3</text><text class="dim" x="212.0" y="182" font-size="11" text-anchor="middle">x + y = 1</text><line class="grid" x1="290" y1="134" x2="290" y2="14"/><line class="line" x1="314" y1="134" x2="314" y2="14"/><line class="grid" x1="338" y1="134" x2="338" y2="14"/><line class="grid" x1="362" y1="134" x2="362" y2="14"/><line class="grid" x1="386" y1="134" x2="386" y2="14"/><line class="grid" x1="410" y1="134" x2="410" y2="14"/><line class="grid" x1="290" y1="134" x2="410" y2="134"/><line class="line" x1="290" y1="110" x2="410" y2="110"/><line class="grid" x1="290" y1="86" x2="410" y2="86"/><line class="grid" x1="290" y1="62" x2="410" y2="62"/><line class="grid" x1="290" y1="38" x2="410" y2="38"/><line class="grid" x1="290" y1="14" x2="410" y2="14"/><line class="curve" x1="290" y1="38.0" x2="386.0" y2="134"/><line class="curve2" stroke-dasharray="6 5" x1="290" y1="38.0" x2="386.0" y2="134"/><text class="ink" x="350.0" y="152" font-size="12" text-anchor="middle">Sonsuz çözüm</text><text class="dim" x="350.0" y="168" font-size="11" text-anchor="middle">x + y = 2</text><text class="dim" x="350.0" y="182" font-size="11" text-anchor="middle">2x + 2y = 4</text></svg>
  <figcaption>Solda doğrular tek bir noktada kesişiyor: $(2, 1)$. Ortada paraleller, hiç kesişmiyorlar. Sağda iki denklem aynı doğruyu anlatıyor (ikincisi birincinin 2 katı): doğru üzerindeki her nokta bir çözüm.</figcaption>
</figure>

| Durum | Geometri | Çözüm sayısı |
|---|---|---|
| Doğrular kesişiyor | tek ortak nokta | **1** |
| Doğrular paralel | ortak nokta yok | **0** |
| Doğrular çakışık | bütün noktalar ortak | **sonsuz** |

Üç bilinmeyende her denklem bir **düzlem** ve aynı üç durum geçerli:
düzlemler tek bir noktada buluşur, hiç ortak noktaları olmaz ya da bir
doğru (veya düzlem) boyunca buluşurlar. Bu kural her boyutta doğru:
**doğrusal bir sistemin ya 0, ya 1 ya da sonsuz çözümü vardır.** Tam iki
çözümü olan bir doğrusal sistem yoktur.

Determinant ile bağı: kare bir sistemde $\det A \ne 0$ ise tek çözüm var.
$\det A = 0$ ise ya hiç çözüm yok ya da sonsuz çözüm var; hangisi olduğunu
Gauss eleme söyleyecek.

## Satır işlemleri

Gauss eleme, sistemi **çözümünü değiştirmeden** daha kolay bir sisteme
dönüştürür. Bunun için üç işlem serbest:

| İşlem | Yazılış | Neden çözümü değiştirmez? |
|---|---|---|
| Yer değiştirme | $R_i \leftrightarrow R_j$ | Denklemlerin sırası önemli değil |
| Ölçekleme | $R_i \to c\,R_i$ ($c \ne 0$) | Bir denklemin iki tarafını aynı sayıyla çarpmak |
| Ekleme | $R_i \to R_i + c\,R_j$ | Bir denkleme başka bir denklemin katını eklemek |

$R_i$, $i$. satır (row) demek. Üçüncü işlem en çok kullanılanı: bir
bilinmeyeni yok etmek için bir satırdan başka bir satırın uygun katını
çıkarıyoruz.

**Kural:** İşlem, artırılmış matrisin **bütün satırına** uygulanır;
çizginin sağındaki sayı da dahil. Yalnızca sol tarafı değiştirmek
denklemi bozar.

## Gauss eleme: iki aşama

### 1. aşama: ileri eleme

Amaç, köşegenin **altını sıfırlamak**. Böylece matris basamak biçimine
gelir: her satır bir öncekinden daha az bilinmeyen içerir.

<figure class="fig">
<svg viewBox="0 0 400 186" width="400"><rect class="box" x="26" y="40" width="34" height="34"/><text class="ink" x="43.0" y="62.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="60" y="40" width="34" height="34"/><text class="ink" x="77.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="94" y="40" width="34" height="34"/><text class="ink" x="111.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="128" y="40" width="34" height="34"/><text class="ink" x="145.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="26" y="74" width="34" height="34"/><text class="ink" x="43.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="60" y="74" width="34" height="34"/><text class="ink" x="77.0" y="96.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="94" y="74" width="34" height="34"/><text class="ink" x="111.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="128" y="74" width="34" height="34"/><text class="ink" x="145.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="26" y="108" width="34" height="34"/><text class="ink" x="43.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="60" y="108" width="34" height="34"/><text class="ink" x="77.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="94" y="108" width="34" height="34"/><text class="ink" x="111.0" y="130.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="128" y="108" width="34" height="34"/><text class="ink" x="145.0" y="130.0" font-size="15" text-anchor="middle">∗</text><rect class="curve" x="29" y="43" width="28" height="28" rx="4"/><rect class="curve" x="63" y="77" width="28" height="28" rx="4"/><rect class="curve" x="97" y="111" width="28" height="28" rx="4"/><line class="curve3" x1="128" y1="36" x2="128" y2="146" stroke-dasharray="4 3"/><path class="curve2" d="M26,74 H60 V108 H94 V142" fill="none"/><text class="ink" x="94" y="26" font-size="12" text-anchor="middle">Basamak biçimi</text><rect class="box" x="226" y="40" width="34" height="34"/><text class="ink" x="243.0" y="62.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="260" y="40" width="34" height="34"/><text class="ink" x="277.0" y="62.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="294" y="40" width="34" height="34"/><text class="ink" x="311.0" y="62.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="328" y="40" width="34" height="34"/><text class="ink" x="345.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="226" y="74" width="34" height="34"/><text class="ink" x="243.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="260" y="74" width="34" height="34"/><text class="ink" x="277.0" y="96.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="294" y="74" width="34" height="34"/><text class="ink" x="311.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="328" y="74" width="34" height="34"/><text class="ink" x="345.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="226" y="108" width="34" height="34"/><text class="ink" x="243.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="260" y="108" width="34" height="34"/><text class="ink" x="277.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="294" y="108" width="34" height="34"/><text class="ink" x="311.0" y="130.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="328" y="108" width="34" height="34"/><text class="ink" x="345.0" y="130.0" font-size="15" text-anchor="middle">∗</text><rect class="curve" x="229" y="43" width="28" height="28" rx="4"/><rect class="curve" x="263" y="77" width="28" height="28" rx="4"/><rect class="curve" x="297" y="111" width="28" height="28" rx="4"/><line class="curve3" x1="328" y1="36" x2="328" y2="146" stroke-dasharray="4 3"/><path class="curve2" d="M226,74 H260 V108 H294 V142" fill="none"/><text class="ink" x="294" y="26" font-size="12" text-anchor="middle">İndirgenmiş basamak biçimi</text><text class="dim" x="200" y="172" font-size="12" text-anchor="middle">■ pivot (sıfır değil), ∗ herhangi bir sayı</text></svg>
  <figcaption>Solda ileri elemenin varacağı basamak biçimi: her satırın ilk sıfır olmayan elemanı (pivot, çerçeveli) bir üstündekinin sağında ve pivotların altı sıfır. Sağda Gauss–Jordan'ın varacağı indirgenmiş biçim: pivotlar 1, pivot sütunlarının geri kalanı 0.</figcaption>
</figure>

Her sütunda sırayla:

1. **Pivot seç:** o sütunda, üzerinde çalıştığın satırdaki eleman. Sıfırsa
   aşağıdaki sıfır olmayan bir satırla yer değiştir.
2. **Altını sıfırla:** pivotun altındaki her satırdan, pivot satırının
   uygun katını çıkar. Kat $=$ (sıfırlanacak eleman) $/$ (pivot).

Bölümün başındaki sistemi çözelim.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & -1 & 5 \\ 1 & -1 & 2 & 5 \end{array}\right]
$$

**1. sütun.** Pivot sol üstteki $1$. Altındaki $2$'yi sıfırlamak için
$R_2 \to R_2 - 2R_1$, altındaki $1$ için $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -3 & -7 \\ 0 & -2 & 1 & -1 \end{array}\right]
$$

Hesabı bir satırda görelim: $R_2 - 2R_1 = (2 - 2,\ 3 - 2,\ -1 - 2 \mid 5 - 12) = (0,\ 1,\ -3 \mid -7)$.

**2. sütun.** Pivot artık 2. satırdaki $1$. Altındaki $-2$'yi sıfırlamak
için $R_3 \to R_3 + 2R_2$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -3 & -7 \\ 0 & 0 & -5 & -15 \end{array}\right]
$$

Köşegenin altı sıfır: basamak biçimi. Son satır artık tek bilinmeyenli
bir denklem.

### 2. aşama: geri yerine koyma

En alttan başlayıp yukarı çıkıyoruz:

$$
\begin{aligned}
-5z &= -15 &\Rightarrow\quad z &= 3 \\
y - 3z &= -7 &\Rightarrow\quad y &= -7 + 9 = 2 \\
x + y + z &= 6 &\Rightarrow\quad x &= 6 - 2 - 3 = 1
\end{aligned}
$$

**Sağlama:** $(1, 2, 3)$'ü orijinal üç denkleme koy: $1 + 2 + 3 = 6$ ✓,
$2 + 6 - 3 = 5$ ✓, $1 - 2 + 6 = 5$ ✓.

## Çözüm yok ve sonsuz çözüm

Eleme bitince son satırlara bakmak sistemin türünü söyler.

**Çözüm yok.** Bir satır $\left[\begin{array}{ccc|c} 0 & 0 & 0 & c \end{array}\right]$
($c \ne 0$) hâline gelirse o satır $0 = c$ diyor: imkânsız. Örnek:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 1 & 2 & 3 & 5 \\ 2 & 3 & 4 & 8 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 0 & 1 & 2 & 3 \\ 0 & 1 & 2 & 4 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 0 & 1 \end{array}\right]
$$

($R_2 - R_1$, $R_3 - 2R_1$, sonra $R_3 - R_2$.) Son satır $0 = 1$: sistem
**tutarsız**, hiç çözüm yok. Geometrik olarak üç düzlemin üçünün birden
geçtiği nokta yok.

**Sonsuz çözüm.** Aynı sistemde son sağ tarafı $8$ yerine $7$ yapalım.
Eleme sonunda son satır $\left[\begin{array}{ccc|c} 0 & 0 & 0 & 0 \end{array}\right]$
olur: $0 = 0$, her zaman doğru, hiçbir şey söylemiyor. Geriye üç
bilinmeyenli **iki** denklem kalıyor:

$$
\begin{aligned}
x + y + z &= 2 \\
y + 2z &= 3
\end{aligned}
$$

Pivotu olmayan sütunun bilinmeyeni ($z$) **serbest değişken**: ona
istediğimiz değeri verebiliriz. $z = t$ dersek:

$$
\begin{aligned}
y &= 3 - 2t \\
x &= 2 - y - z = 2 - (3 - 2t) - t = -1 + t
\end{aligned}
$$

Çözüm kümesi $(x, y, z) = (-1 + t,\ 3 - 2t,\ t)$; her $t$ sayısı için bir
çözüm. $t = 0$ için $(-1, 3, 0)$, $t = 1$ için $(0, 1, 1)$. Geometrik
olarak bu bir **doğru**: üç düzlem bir doğru boyunca kesişiyor.

| Eleme sonunda | Anlamı |
|---|---|
| Her sütunda pivot var | tek çözüm |
| $0 = c$ ($c \ne 0$) satırı var | çözüm yok |
| $0 = c$ satırı yok ama pivotsuz sütun var | sonsuz çözüm (serbest değişken sayısı kadar parametre) |

## Gauss–Jordan: tersi bulmak

Elemeyi bir adım daha ileri götürebiliriz: pivotları $1$ yapıp
(satırı pivota bölerek) pivotların **üstünü de** sıfırlarsak geri yerine
koymaya gerek kalmaz, çözüm doğrudan son sütunda okunur. Buna
**Gauss–Jordan eleme** denir ve sonuç **indirgenmiş basamak biçimi**.

Aynı yöntem ters matrisi de bulur: $A$'nın yanına $I$'yı yazıp sol tarafı
$I$'ya çevirirsen, sağ taraf $A^{-1}$ olur.

$$
[\,A \mid I\,] \;\longrightarrow\; [\,I \mid A^{-1}\,]
$$

Neden? Satır işlemlerinin hepsi aynı anda iki tarafa uygulanıyor.
$A$'yı $I$'ya çeviren işlemler dizisi, matris olarak $A^{-1}$ ile soldan
çarpmakla aynı; aynı dizi $I$'yı $A^{-1}I = A^{-1}$'e çeviriyor.

Örnek: $A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}$.

$$
\left[\begin{array}{cc|cc} 2 & 1 & 1 & 0 \\ 5 & 3 & 0 & 1 \end{array}\right]
\xrightarrow{R_1 / 2}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 5 & 3 & 0 & 1 \end{array}\right]
$$

$$
\xrightarrow{R_2 - 5R_1}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 0 & 0.5 & -2.5 & 1 \end{array}\right]
\xrightarrow{2R_2}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 0 & 1 & -5 & 2 \end{array}\right]
$$

$$
\xrightarrow{R_1 - 0.5R_2}
\left[\begin{array}{cc|cc} 1 & 0 & 3 & -1 \\ 0 & 1 & -5 & 2 \end{array}\right]
$$

$A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$; önceki bölümdeki
formülle bulunanın aynısı. Farkı şu: bu yöntem $3 \times 3$'te, $100 \times
100$'de de aynı şekilde çalışıyor. Sol taraf $I$'ya çevrilemiyorsa
(sıfır satır çıkıyorsa) matrisin tersi yok.

## Determinantı elemeyle bulmak

Satır işlemlerinin determinanta etkisini önceki bölümde görmüştük:
**ekleme** değiştirmiyor, **yer değiştirme** işaretini çeviriyor. Yalnızca
ekleme (ve gerekirse yer değiştirme) kullanarak basamak biçimine
gelirsek, basamak biçimi üçgen olduğu için determinant köşegen çarpımı:

$$
\det A = (\pm 1) \cdot (\text{pivotların çarpımı})
$$

Bölümün başındaki örnekte yer değiştirme yapmadık ve pivotlar $1, 1, -5$:
$\det A = 1 \cdot 1 \cdot (-5) = -5$. $3 \times 3$ açılımıyla da aynısı çıkar;
ama $10 \times 10$ bir matriste açılım 3,6 milyon terim demek, eleme ise
birkaç yüz işlem.

## Neden bilgisayarlar Gauss eleme kullanır?

$n \times n$ bir sistem için eleme yaklaşık $\tfrac{n^3}{3}$ çarpma
yapıyor. $n = 1000$ için yaklaşık 330 milyon işlem; bugünkü bir
bilgisayar için bir saniyenin küçük bir kesri. Tersi hesaplayıp çarpmak
yaklaşık üç kat daha fazla iş ve yuvarlama hatalarına daha açık.

Kütüphanelerin "sistem çöz" fonksiyonları (NumPy'da `solve`) elemeyi
**LU ayrışımı** adıyla yapıyor: ileri elemenin çarpanlarını bir alt üçgen
matriste ($L$), sonucu bir üst üçgen matriste ($U$) saklayıp $A = LU$
yazıyor. Aynı $A$ ile birçok farklı $\mathbf{b}$ için çözüm gerektiğinde
eleme bir kez yapılıyor.

**Kısmi pivotlama:** Bilgisayar her sütunda pivot olarak mutlak değeri
**en büyük** elemanı seçiyor (gerekirse satır değiştirerek). Çok küçük bir
sayıya bölmek yuvarlama hatalarını büyütüyor; en büyüğü seçmek bunu
önlüyor.

## Makine öğrenmesinde doğrusal sistemler

**Modelin parametrelerini bulmak.** Üç noktadan geçen parabolü
($y = a + bx + cx^2$) bulmak üç bilinmeyenli bir doğrusal sistem:
bilinmeyenler $a, b, c$ ve her nokta bir denklem. $x^2$ geçmesine rağmen
sistem **$a, b, c$'de** doğrusal. Doğrusal regresyon da aynı fikre
dayanıyor: ağırlıklar bir doğrusal sistemin (normal denklemlerin)
çözümü.

**Veri, bilinmeyenden az olunca.** 3 örnek ve 10 özellik varsa 3 denklem
ve 10 bilinmeyen var: sonsuz çözüm. Model veriyi mükemmel açıklayan
sonsuz sayıda ağırlık bulabilir ama hangisinin gerçekten doğru olduğunu
bilemez. Bu, aşırı öğrenmenin (overfitting) doğrusal cebirdeki görüntüsü.
Düzenlileştirme bu sonsuz çözüm arasından "en küçük ağırlıklı" olanı
seçer.

**Veri, bilinmeyenden çok olunca.** 1000 ev ve 3 özellik varsa 1000
denklem ve 3 bilinmeyen var; gürültülü veride bütün denklemleri aynı anda
sağlayan bir çözüm neredeyse hiç yok (tutarsız sistem). Regresyon o
zaman "tam çözüm" yerine **hatayı en küçük** yapan çözümü arar: en küçük
kareler. Onu Doğrusal Regresyonun Matematiği bölümünde göreceğiz.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>İşlemi yalnızca çizginin soluna uygulamak</p>
      <p>$R_2 - 2R_1$'de $R_1$'i de değiştirmek</p>
      <p>Sıfır pivota bölmeye çalışmak</p>
      <p>$0 = 0$ satırını "çözüm yok" sanmak</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Satırın tamamına, sağ taraf dahil</p>
      <p>Yalnızca $R_2$ değişir, $R_1$ aynı kalır</p>
      <p>Önce alttaki bir satırla yer değiştir</p>
      <p>$0 = 0$ sonsuz çözüm; $0 = c \ne 0$ çözüm yok</p>
    </div>
  </div>
  <figcaption>Eleme mekanik bir iş; hataların çoğu işaret ve sağ taraf unutmaktan çıkıyor.</figcaption>
</figure>

- **İşaret hataları.** $R_3 \to R_3 - (-2)R_2$ ile $R_3 + 2R_2$ aynı şey;
  bir kez yaz, sonra hesapla.
- **Sağlamayı atlamak.** Bulduğun çözümü **orijinal** denklemlere koy;
  eleme sırasında yapılan bir hata ancak böyle yakalanır.
- **Serbest değişkeni sayı sanmak.** Sonsuz çözümlü sistemde cevap tek
  bir nokta değil, bir parametreye bağlı bir küme.

## Özet

- Doğrusal sistem: $A\mathbf{x} = \mathbf{b}$; elle çözerken artırılmış matris $[A \mid \mathbf{b}]$.
- Çözüm sayısı her zaman 0, 1 ya da sonsuz (doğrular: kesişen, paralel, çakışık).
- Satır işlemleri: yer değiştirme, sıfır olmayan sayıyla ölçekleme, bir satıra başka satırın katını ekleme.
- İleri eleme: pivotun altını sıfırla $\Rightarrow$ basamak biçimi; sonra geri yerine koyma.
- $0 = c \ne 0$ satırı: çözüm yok. Pivotsuz sütun: serbest değişken, sonsuz çözüm.
- Gauss–Jordan: $[A \mid I] \to [I \mid A^{-1}]$.
- $\det A$ = (yer değiştirme sayısına göre $\pm$) pivotların çarpımı.
- Bilgisayar: yaklaşık $n^3/3$ işlem, LU ayrışımı, kısmi pivotlama.
- ML: parametreleri bulmak bir sistem çözmek; az veri $\Rightarrow$ sonsuz çözüm, çok gürültülü veri $\Rightarrow$ tutarsız sistem ve en küçük kareler.
