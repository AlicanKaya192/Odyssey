# Özdeğerler ve Özvektörler

Bir matrisle çarpınca vektörlerin çoğu hem uzar ya da kısalır hem de
**yön değiştirir**. Ama çoğu matrisin, yönünü hiç değiştirmediği birkaç
özel vektörü vardır: matris onları yalnızca uzatır, kısaltır ya da ters
çevirir. Bu vektörlere **özvektör**, uzama miktarına **özdeğer** denir.

Neden bu kadar önemliler? Çünkü bir matrisin "iskeletini" gösteriyorlar.
Karmaşık görünen bir dönüşüm, özvektörlerin tabanında bakınca yalnızca
her yönde ayrı bir sayıyla çarpmaktan ibaret. Bu fikir makine
öğrenmesinde her yerde: PCA verinin en çok yayıldığı yönleri bir
matrisin özvektörleriyle buluyor, Google'ın PageRank'i web'in en önemli
sayfalarını bir özvektörle sıralıyor, bir modelin eğitiminin kararlı olup
olmayacağını özdeğerler söylüyor.

Ön bilgi: Determinant ve Ters Matris, Doğrusal Bağımsızlık ve Rank bölümleri.

## Tanım

Kare bir $A$ matrisi için, sıfır olmayan bir $\mathbf{v}$ vektörü ve bir
$\lambda$ sayısı

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

eşitliğini sağlıyorsa $\mathbf{v}$'ye $A$'nın bir **özvektörü**,
$\lambda$'ya (lambda) ona karşılık gelen **özdeğer** denir.

Sözle: $A$'yı $\mathbf{v}$'ye uygulamak, $\mathbf{v}$'yi bir sayıyla
çarpmakla aynı. Sonuç $\mathbf{v}$ ile **aynı doğru üzerinde** kalıyor.

- $\lambda > 1$: vektör uzuyor.
- $0 < \lambda < 1$: kısalıyor.
- $\lambda < 0$: ters yöne dönüyor (yine aynı doğru üzerinde).
- $\lambda = 0$: sıfıra gidiyor; $\mathbf{v}$ çekirdekte.

$\mathbf{v} = \mathbf{0}$ tanımın dışında: $A\mathbf{0} = \lambda\mathbf{0}$
her $\lambda$ için doğru, bir şey anlatmıyor.

### Bir örnek

$$
A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}
$$

Üç vektörü deneyelim:

$$
\begin{aligned}
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} &= \begin{bmatrix} 3 \\ 3 \end{bmatrix} = 3 \begin{bmatrix} 1 \\ 1 \end{bmatrix} \\
A \begin{bmatrix} 1 \\ -1 \end{bmatrix} &= \begin{bmatrix} 1 \\ -1 \end{bmatrix} = 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} \\
A \begin{bmatrix} 1 \\ 0 \end{bmatrix} &= \begin{bmatrix} 2 \\ 1 \end{bmatrix}
\end{aligned}
$$

$(1, 1)$ özvektör, özdeğeri $3$: üç katına uzuyor. $(1, -1)$ özvektör,
özdeğeri $1$: hiç değişmiyor. $(1, 0)$ özvektör **değil**: $(2, 1)$ onun
bir katı değil, yönü değişti.

<figure class="fig">
<svg viewBox="0 0 420 222" width="420"><line class="grid" x1="16" y1="194" x2="16" y2="14"/><line class="grid" x1="46" y1="194" x2="46" y2="14"/><line class="line" x1="76" y1="194" x2="76" y2="14"/><line class="grid" x1="106" y1="194" x2="106" y2="14"/><line class="grid" x1="136" y1="194" x2="136" y2="14"/><line class="grid" x1="166" y1="194" x2="166" y2="14"/><line class="grid" x1="196" y1="194" x2="196" y2="14"/><line class="grid" x1="16" y1="194" x2="196" y2="194"/><line class="grid" x1="16" y1="164" x2="196" y2="164"/><line class="line" x1="16" y1="134" x2="196" y2="134"/><line class="grid" x1="16" y1="104" x2="196" y2="104"/><line class="grid" x1="16" y1="74" x2="196" y2="74"/><line class="grid" x1="16" y1="44" x2="196" y2="44"/><line class="grid" x1="16" y1="14" x2="196" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="16.0" y1="194.0" x2="196.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" x1="16.0" y1="74.0" x2="136.0" y2="194.0"/><line class="curve" x1="76" y1="134" x2="100.9" y2="109.1"/><polygon class="dot" points="106,104 102.8,112.4 97.6,107.2"/><line class="curve2" x1="76" y1="134" x2="100.9" y2="158.9"/><polygon class="dot2" points="106,164 97.6,160.8 102.8,155.6"/><line class="curve4" x1="76" y1="134" x2="98.8" y2="134.0"/><polygon class="dot3" points="106,134 97.8,137.7 97.8,130.3"/><text class="ink" x="111" y="104" font-size="12" text-anchor="start">v₁</text><text class="ink" x="111" y="172" font-size="12" text-anchor="start">v₂</text><text class="ink" x="111" y="138" font-size="12" text-anchor="start">u</text><text class="ink" x="106.0" y="212" font-size="12" text-anchor="middle">Önce</text><line class="grid" x1="222" y1="194" x2="222" y2="14"/><line class="grid" x1="252" y1="194" x2="252" y2="14"/><line class="line" x1="282" y1="194" x2="282" y2="14"/><line class="grid" x1="312" y1="194" x2="312" y2="14"/><line class="grid" x1="342" y1="194" x2="342" y2="14"/><line class="grid" x1="372" y1="194" x2="372" y2="14"/><line class="grid" x1="402" y1="194" x2="402" y2="14"/><line class="grid" x1="222" y1="194" x2="402" y2="194"/><line class="grid" x1="222" y1="164" x2="402" y2="164"/><line class="line" x1="222" y1="134" x2="402" y2="134"/><line class="grid" x1="222" y1="104" x2="402" y2="104"/><line class="grid" x1="222" y1="74" x2="402" y2="74"/><line class="grid" x1="222" y1="44" x2="402" y2="44"/><line class="grid" x1="222" y1="14" x2="402" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="222.0" y1="194.0" x2="402.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" x1="222.0" y1="74.0" x2="342.0" y2="194.0"/><line class="curve" x1="282" y1="134" x2="366.9" y2="49.1"/><polygon class="dot" points="372,44 368.8,52.4 363.6,47.2"/><line class="curve2" x1="282" y1="134" x2="306.9" y2="158.9"/><polygon class="dot2" points="312,164 303.6,160.8 308.8,155.6"/><line class="curve4" x1="282" y1="134" x2="335.6" y2="107.2"/><polygon class="dot3" points="342,104 336.3,111.0 333.0,104.4"/><line class="curve3" stroke-dasharray="4 3" x1="282" y1="134" x2="304.8" y2="134.0"/><polygon class="dim" points="312,134 303.8,137.7 303.8,130.3"/><text class="ink" x="366" y="44" font-size="11" text-anchor="end">Av₁ = 3v₁</text><text class="ink" x="317" y="174" font-size="11" text-anchor="start">Av₂ = v₂</text><text class="ink" x="347" y="108" font-size="11" text-anchor="start">Au</text><text class="ink" x="312.0" y="212" font-size="12" text-anchor="middle">A = [2 1; 1 2] uygulandıktan sonra</text></svg>
  <figcaption>Kesikli çizgiler iki özvektörün doğruları. $A$ uygulanınca $\mathbf{v}_1 = (1, 1)$ (mor) kendi doğrusunda 3 katına uzuyor, $\mathbf{v}_2 = (1, -1)$ (turuncu) yerinde kalıyor. Sıradan bir vektör olan $\mathbf{u} = (1, 0)$ (yeşil) ise yönünü değiştirip $(2, 1)$'e gidiyor.</figcaption>
</figure>

Bir özvektörün her katı da özvektördür: $A(2\mathbf{v}) = 2A\mathbf{v} =
\lambda(2\mathbf{v})$. Bu yüzden özvektörden söz ederken aslında bir
**doğrultudan** söz ediyoruz; o doğrultudan herhangi bir temsilci (çoğu
zaman en basit tam sayılı olanı ya da birim uzunluklusu) seçilir.

## Özdeğerleri bulmak

$A\mathbf{v} = \lambda\mathbf{v}$'yi bir tarafa toplayalım. $\lambda\mathbf{v}
= \lambda I\mathbf{v}$ yazarsak:

$$
(A - \lambda I)\mathbf{v} = \mathbf{0}
$$

Bu denklemin **sıfır olmayan** bir çözümü olmasını istiyoruz. Önceki
bölümlerden: $B\mathbf{v} = \mathbf{0}$'ın sıfır olmayan çözümü ancak $B$
tekilse vardır, yani $\det B = 0$. Öyleyse özdeğerler

$$
\det(A - \lambda I) = 0
$$

denkleminin kökleri. Bu denkleme **karakteristik denklem**, sol taraftaki
$\lambda$ polinomuna **karakteristik polinom** denir.

### 2 × 2 için

$$
\det \begin{bmatrix} a - \lambda & b \\ c & d - \lambda \end{bmatrix} = (a - \lambda)(d - \lambda) - bc
$$

Açınca:

$$
\lambda^2 - (a + d)\,\lambda + (ad - bc) = 0
$$

$a + d$ köşegen toplamı yani **iz**, $ad - bc$ **determinant**. Kısaca:

$$
\lambda^2 - (\operatorname{tr} A)\,\lambda + \det A = 0
$$

Örneğimizde $\operatorname{tr} A = 4$, $\det A = 3$:

$$
\lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0
$$

Özdeğerler $\lambda_1 = 3$ ve $\lambda_2 = 1$; yukarıda denemeyle
bulduklarımızın aynısı.

## Özvektörleri bulmak

Her özdeğer için $(A - \lambda I)\mathbf{v} = \mathbf{0}$ sistemini çöz.
Matris tekil olduğu için sonsuz çözüm var (bir doğrultu); birini seçeriz.

**$\lambda = 3$:**

$$
A - 3I = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}
$$

İlk satır $-x + y = 0$, yani $y = x$. İkinci satır aynı bilgiyi veriyor
(tekil matrisin satırları bağımlı). $x = 1$ seçersek $\mathbf{v}_1 = (1, 1)$.

**$\lambda = 1$:**

$$
A - I = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
$$

$x + y = 0$, yani $y = -x$: $\mathbf{v}_2 = (1, -1)$.

**Sağlama her zaman kolay:** bulduğun vektörü $A$ ile çarp, $\lambda$ katı
çıkıyor mu bak.

### Simetrik olmayan bir örnek

$$
B = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}
$$

$\operatorname{tr} B = 7$, $\det B = 12 - 2 = 10$:

$$
\lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2) = 0
$$

$\lambda = 5$ için $B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}$:
$y = x$, $\mathbf{v} = (1, 1)$. $\lambda = 2$ için $B - 2I = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}$:
$2x + y = 0$, $\mathbf{v} = (1, -2)$.

Sağlama: $B(1, -2) = (4 - 2,\ 2 - 6) = (2, -4) = 2 \cdot (1, -2)$ ✓.

## Özdeğerlerin kuralları

$n \times n$ bir matrisin (karmaşık sayılar dahil sayılınca) $n$ özdeğeri
vardır ve şu kurallar geçerli:

| Kural | Yazılış |
|---|---|
| Toplam | $\lambda_1 + \cdots + \lambda_n = \operatorname{tr} A$ |
| Çarpım | $\lambda_1 \cdots \lambda_n = \det A$ |
| Üçgen matris | Özdeğerler köşegen elemanları |
| Kuvvet | $A^k$'nın özdeğerleri $\lambda^k$ (özvektörler aynı) |
| Ters | $A^{-1}$'in özdeğerleri $1/\lambda$ (özvektörler aynı) |
| Kaydırma | $A + cI$'nın özdeğerleri $\lambda + c$ |
| Tekil | $\det A = 0 \iff 0$ bir özdeğer |

Örneklerimizle: $A$ için $3 + 1 = 4 = \operatorname{tr} A$ ve $3 \cdot 1 = 3
= \det A$. $B$ için $5 + 2 = 7$, $5 \cdot 2 = 10$. ✓

**İz ve determinant kısayolu.** $2 \times 2$'de toplamı izi, çarpımı
determinantı veren iki sayı aramak çoğu zaman karakteristik denklemi
çözmekten hızlı.

**Kuvvet kuralı neden doğru?** $A\mathbf{v} = \lambda\mathbf{v}$ ise
$A^2\mathbf{v} = A(\lambda\mathbf{v}) = \lambda A\mathbf{v} =
\lambda^2\mathbf{v}$. Her çarpım bir $\lambda$ daha ekliyor.

### Gerçel özdeğer olmayabilir

$90°$ döndürme matrisi $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$:
$\operatorname{tr} R = 0$, $\det R = 1$, karakteristik denklem
$\lambda^2 + 1 = 0$. Gerçel çözümü yok. Geometrik olarak çok mantıklı:
döndürme **her** vektörün yönünü değiştiriyor, yönünü koruyan tek bir
vektör bile yok. (Karmaşık sayılarla özdeğerler $\pm i$; bu derste
gerçel özdeğerlerle çalışacağız.)

## Köşegenleştirme

$n \times n$ bir $A$'nın $n$ tane bağımsız özvektörü varsa, onları bir
tabana çevirebiliriz. Özvektörleri $P$'nin sütunları, özdeğerleri
köşegen bir $D$ matrisine yazınca:

$$
A = P D P^{-1}
$$

Neden? $AP$'nin her sütunu $A\mathbf{v}_i = \lambda_i\mathbf{v}_i$, yani
$AP = PD$. Sağdan $P^{-1}$ ile çarpınca eşitlik çıkıyor.

**Anlamı:** $A$'yı uygulamak üç adıma ayrılıyor:

1. $P^{-1}$: vektörü özvektör tabanındaki koordinatlarına çevir,
2. $D$: her koordinatı kendi özdeğeriyle çarp (en basit dönüşüm),
3. $P$: standart tabana geri dön.

Doğru tabanda $A$ yalnızca bir ölçekleme. Önceki bölümdeki "doğru tabanı
seçince problem basitleşir" fikrinin en güzel örneği bu.

### Kuvvet almak kolaylaşıyor

$$
A^k = P D^k P^{-1}
$$

Aradaki $P^{-1}P$'ler birbirini götürüyor ve köşegen bir matrisin kuvveti,
köşegen elemanların kuvveti. $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$
için:

$$
P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}
\qquad
D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}
$$

Pratikte $P^{-1}$ yazmak yerine vektörü özvektörlere ayırmak daha kısa:
$(3, 1) = 2 \cdot (1, 1) + 1 \cdot (1, -1)$. Her parça kendi özdeğeriyle
çarpılır:

$$
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \cdot 3^5 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \cdot 1^5 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 487 \\ 485 \end{bmatrix}
$$

Beş kez matris çarpmak yerine iki sayının kuvvetini aldık.

## Tekrarlı çarpım ve baskın özvektör

Bir vektörü aynı matrisle tekrar tekrar çarparsak ne olur? Vektörü
özvektörlere ayıralım: $\mathbf{x} = c_1\mathbf{v}_1 + c_2\mathbf{v}_2$.

$$
A^k\mathbf{x} = c_1\lambda_1^k\mathbf{v}_1 + c_2\lambda_2^k\mathbf{v}_2
$$

$|\lambda_1| > |\lambda_2|$ ise $\lambda_1^k$ çok daha hızlı büyür ve bir
süre sonra ikinci terim ona göre önemsiz kalır: $A^k\mathbf{x}$'in yönü
**baskın özvektöre** ($\mathbf{v}_1$) yaklaşır.

<figure class="fig">
<svg viewBox="0 0 350 278" width="350"><line class="line" x1="60" y1="244" x2="60" y2="14"/><line class="grid" x1="290" y1="244" x2="290" y2="14"/><line class="line" x1="60" y1="244" x2="290" y2="244"/><line class="grid" x1="60" y1="14" x2="290" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="60.0" y1="244.0" x2="290.0" y2="14.0"/><line opacity="0.35" class="curve" x1="60" y1="244" x2="271.3" y2="244.0"/><polygon opacity="0.35" class="dot" points="278.5,244.0 270.3,247.7 270.3,240.3"/><text class="ink" x="284.5" y="258.0" font-size="11" text-anchor="start">x</text><line opacity="0.51" class="curve" x1="60" y1="244" x2="249.0" y2="149.5"/><polygon opacity="0.51" class="dot" points="255.4,146.3 249.7,153.3 246.4,146.7"/><text class="ink" x="261.4" y="150.3" font-size="11" text-anchor="start">Ax</text><line opacity="0.68" class="curve" x1="60" y1="244" x2="225.0" y2="112.0"/><polygon opacity="0.68" class="dot" points="230.6,107.5 226.5,115.5 221.9,109.8"/><text class="ink" x="236.6" y="111.5" font-size="11" text-anchor="start">A²x</text><line opacity="0.84" class="curve" x1="60" y1="244" x2="214.8" y2="100.2"/><polygon opacity="0.84" class="dot" points="220.1,95.3 216.6,103.6 211.6,98.2"/><line opacity="1.00" class="curve" x1="60" y1="244" x2="211.2" y2="96.4"/><polygon opacity="1.00" class="dot" points="216.4,91.4 213.1,99.8 208.0,94.5"/><text class="ink" x="206.4" y="89.4" font-size="11" text-anchor="end">A³x, A⁴x</text><text class="ink" x="175" y="266" font-size="11" text-anchor="middle">Yön, kesikli özvektör doğrusuna yaklaşıyor</text></svg>
  <figcaption>$\mathbf{x} = (1, 0)$'dan başlayıp $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ ile tekrar tekrar çarpınca yönler $0°$, $27°$, $39°$, $43°$, $44°$: baskın özvektör $(1, 1)$'in $45°$'lik doğrultusuna yaklaşıyor (her ok birim uzunluğa indirildi).</figcaption>
</figure>

Bu, en büyük özdeğerin özvektörünü bulmanın en basit yolu: **kuvvet
yöntemi**. Rastgele bir vektörle başla, $A$ ile çarp, uzunluğunu 1'e
indir, tekrarla.

### Uzun vadede ne olur: Markov zinciri

Bir şehirde hava her gün ya güneşli ya yağmurlu. Güneşli bir günün
ertesi %90 güneşli, yağmurlu bir günün ertesi %50 güneşli olsun. Bunu bir
**geçiş matrisi** anlatıyor (sütun = bugün, satır = yarın):

$$
M = \begin{bmatrix} 0.9 & 0.5 \\ 0.1 & 0.5 \end{bmatrix}
$$

Bugünkü olasılıklar $\mathbf{p}$ ise yarınki $M\mathbf{p}$, bir hafta
sonraki $M^7\mathbf{p}$. Uzun vadede olasılıklar **değişmeyen** bir
$\mathbf{p}$'ye oturur: $M\mathbf{p} = \mathbf{p}$. Bu, özdeğeri $1$ olan
özvektör!

$$
M - I = \begin{bmatrix} -0.1 & 0.5 \\ 0.1 & -0.5 \end{bmatrix}
$$

$-0.1x + 0.5y = 0$, yani $x = 5y$: özvektör $(5, 1)$. Olasılıkların
toplamı 1 olmalı; $(5, 1)$'i toplamına bölünce $\left(\tfrac{5}{6},
\tfrac{1}{6}\right)$. Uzun vadede günlerin yaklaşık %83'ü güneşli,
bugünün havası ne olursa olsun.

Öteki özdeğer izden: $0.9 + 0.5 - 1 = 0.4$. $0.4^k$ hızla sıfıra gittiği
için başlangıcın etkisi birkaç haftada siliniyor.

## Simetrik matrisler

Makine öğrenmesinde en çok karşılaşılan matrisler **simetrik**
($A^\mathsf{T} = A$): kovaryans matrisleri, $X^\mathsf{T}X$, Hessian
matrisleri. Simetrik matrislerin çok güzel iki özelliği var
(**spektral teorem**):

1. **Bütün özdeğerleri gerçel.** Döndürme gibi "özdeğersiz" sürprizler
   yok.
2. **Farklı özdeğerlerin özvektörleri birbirine dik.** Örneğimizde
   $(1, 1) \cdot (1, -1) = 0$ ✓.

Özvektörleri birim uzunluğa indirince birbirine dik birim vektörlerden
oluşan bir taban çıkıyor. Böyle bir tabanın matrisi $Q$ için $Q^{-1} =
Q^\mathsf{T}$ (tersi bulmak için devrik almak yetiyor) ve

$$
A = Q \Lambda Q^\mathsf{T}
$$

$\Lambda$ özdeğerlerin köşegen matrisi. Simetrik bir matris, dik
eksenler boyunca ayrı ayrı esnetmekten başka bir şey yapmıyor.

Önceki simetrik olmayan $B$ örneğinde özvektörler $(1, 1)$ ve $(1, -2)$:
nokta çarpımları $1 - 2 = -1 \ne 0$, dik değiller.

## Makine öğrenmesinde özdeğerler

**PCA.** Verinin kovaryans matrisi simetrik. Onun en büyük özdeğerinin
özvektörü, verinin **en çok yayıldığı** yön; özdeğer, o yöndeki varyans.
PCA veriyi en büyük birkaç özdeğerin özvektörlerine izdüşürerek boyutu
indiriyor (PCA bölümünde ayrıntısıyla).

**PageRank.** Web'i sayfalar arası bir Markov zinciri olarak düşün: rastgele
gezen biri her sayfada bağlantılardan birine tıklıyor. Uzun vadede her
sayfada geçirilen zaman, geçiş matrisinin özdeğeri 1 olan özvektörü.
Google bu özvektörü kuvvet yöntemiyle hesaplayıp sayfaları sıraladı.

**Eğitimin kararlılığı.** Gradyan inişinde adım büyüklüğünün ne kadar
olabileceğini kayıp fonksiyonunun Hessian matrisinin en büyük özdeğeri
belirliyor. Tekrarlayan sinir ağlarında aynı ağırlık matrisiyle defalarca
çarpılıyor: özdeğerler 1'den büyükse değerler patlıyor, küçükse sönüyor
("patlayan / kaybolan gradyan").

**Spektral kümeleme.** Benzerlik grafiğinin matrisinin özvektörleri,
veriyi doğal gruplarına ayırmak için kullanılıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\mathbf{v} = \mathbf{0}$ bir özvektördür</p>
      <p>$\det(A - \lambda)$ ($I$ unutulmuş)</p>
      <p>Özvektör tektir</p>
      <p>$A^k$'nın özdeğerleri $k\lambda$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Özvektör sıfır olmayan bir vektör</p>
      <p>$\det(A - \lambda I)$: $\lambda$ yalnızca köşegenden çıkar</p>
      <p>Özvektörün her katı da özvektör</p>
      <p>$A^k$'nın özdeğerleri $\lambda^k$</p>
    </div>
  </div>
  <figcaption>Özvektör bir doğrultu; özdeğer o doğrultudaki uzama çarpanı.</figcaption>
</figure>

- **$\lambda$'yı bütün elemanlardan çıkarmak.** $A - \lambda I$'da
  $\lambda$ yalnızca köşegendeki elemanlardan çıkar.
- **Özvektörü bulurken tek bir çözüm beklemek.** $(A - \lambda I)$ tekil;
  sonsuz çözüm çıkar, birini seçersin. Çözüm yalnızca $\mathbf{0}$ çıkıyorsa
  özdeğeri yanlış hesaplamışsındır.
- **Sağlamayı atlamak.** $A\mathbf{v}$'yi hesapla ve $\lambda\mathbf{v}$'ye
  eşit mi bak; bir çarpım yeter.

## Özet

- $A\mathbf{v} = \lambda\mathbf{v}$, $\mathbf{v} \ne \mathbf{0}$: özvektör yönünü korur, özdeğer kadar uzar.
- Özdeğerler: $\det(A - \lambda I) = 0$. $2 \times 2$: $\lambda^2 - (\operatorname{tr} A)\lambda + \det A = 0$.
- Özvektörler: her $\lambda$ için $(A - \lambda I)\mathbf{v} = \mathbf{0}$'ı çöz; her katı da özvektör.
- $\sum \lambda_i = \operatorname{tr} A$, $\prod \lambda_i = \det A$; üçgen matriste köşegen; $A^k \to \lambda^k$, $A^{-1} \to 1/\lambda$.
- Döndürmenin gerçel özdeğeri yok.
- Köşegenleştirme: $A = PDP^{-1}$, $A^k = PD^kP^{-1}$.
- Tekrarlı çarpım baskın özvektöre yaklaşır (kuvvet yöntemi); Markov zincirinin uzun vadesi özdeğeri 1 olan özvektör.
- Simetrik matris: gerçel özdeğerler, dik özvektörler, $A = Q\Lambda Q^\mathsf{T}$.
- ML: PCA, PageRank, eğitimin kararlılığı, spektral kümeleme.
