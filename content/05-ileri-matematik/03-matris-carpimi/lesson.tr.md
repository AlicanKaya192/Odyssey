# Matris Çarpımı ve Dönüşümler

Önceki bölümde bir matrisi bir vektörle çarptık: ev tablosu $X$ ile ağırlık
vektörü $\mathbf{w}$'nin çarpımı, bütün evlerin fiyat tahminini tek seferde
verdi. Şimdi bir adım ileri gidelim. Elimizde **iki farklı model** olsun:
biri fiyatı, öteki kira getirisini tahmin etsin. İki ağırlık vektörünü yan
yana koyunca bir matris çıkıyor ve soru şu oluyor: **bir matrisi başka bir
matrisle nasıl çarparız?**

Matris çarpımı, doğrusal cebirin en çok kullanılan işlemi. Bir sinir ağının
her katmanı, bir fotoğrafı döndürmek, bir veri tablosunun bütün
satırlarını aynı anda dönüştürmek; hepsi matris çarpımı. Bu bölümde:

- İki matrisin nasıl çarpıldığını ve boyut kuralını,
- Çarpımın neden **sıraya bağlı** olduğunu,
- Bir matrisin düzlemi nasıl **döndürdüğünü, esnettiğini ve yansıttığını**,
- İki dönüşümü art arda yapmanın neden matris çarpımı olduğunu

göreceğiz.

Ön bilgi: Matrisler bölümü (özellikle matris–vektör çarpımı).

## Boyut kuralı

İki matris ancak **soldakinin sütun sayısı sağdakinin satır sayısına
eşitse** çarpılabilir. Sonuç, soldakinin satır sayısı kadar satırlı,
sağdakinin sütun sayısı kadar sütunlu olur:

$$
\underbrace{A}_{m \times n}\;\underbrace{B}_{n \times p} = \underbrace{C}_{m \times p}
$$

Boyutları yan yana yazınca kural kendiliğinden okunuyor: $(m \times
\boxed{n})(\boxed{n} \times p)$. **İçteki iki sayı eşit olmalı, dıştaki
iki sayı sonucun boyutu.**

| $A$ | $B$ | $AB$ |
|---|---|---|
| $2 \times 3$ | $3 \times 4$ | $2 \times 4$ |
| $3 \times 3$ | $3 \times 1$ | $3 \times 1$ (matris–vektör çarpımı) |
| $1 \times 3$ | $3 \times 1$ | $1 \times 1$ (tek sayı: nokta çarpımı) |
| $3 \times 1$ | $1 \times 3$ | $3 \times 3$ |
| $2 \times 3$ | $2 \times 3$ | tanımsız ($3 \ne 2$) |

Tablonun ikinci ve üçüncü satırına dikkat: önceki bölümlerde gördüğümüz
matris–vektör çarpımı ve nokta çarpımı, matris çarpımının **özel
hâlleri**. Yeni bir işlem öğrenmiyoruz, bildiğimiz işlemi genişletiyoruz.

## Eleman kuralı: satır çarpı sütun

$C = AB$'nin $i$. satır, $j$. sütunundaki elemanı, **$A$'nın $i$. satırı
ile $B$'nin $j$. sütununun nokta çarpımı**:

$$
c_{ij} = a_{i1} b_{1j} + a_{i2} b_{2j} + \cdots + a_{in} b_{nj}
$$

Boyut kuralının sebebi de bu: nokta çarpımı yapabilmek için $A$'nın bir
satırının uzunluğu ($n$) ile $B$'nin bir sütununun uzunluğu ($n$) aynı
olmalı.

<figure class="fig">
<svg viewBox="0 0 400 228" width="400"><rect class="box" x="20" y="70" width="34" height="34"/><text class="ink" x="37.0" y="92.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="54" y="70" width="34" height="34"/><text class="ink" x="71.0" y="92.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="88" y="70" width="34" height="34"/><text class="ink" x="105.0" y="92.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="20" y="104" width="34" height="34"/><text class="ink" x="37.0" y="126.0" font-size="14" text-anchor="middle">4</text><rect class="box" x="54" y="104" width="34" height="34"/><text class="ink" x="71.0" y="126.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="88" y="104" width="34" height="34"/><text class="ink" x="105.0" y="126.0" font-size="14" text-anchor="middle">6</text><rect class="box" x="162" y="53" width="34" height="34"/><text class="ink" x="179.0" y="75.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="196" y="53" width="34" height="34"/><text class="ink" x="213.0" y="75.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="162" y="87" width="34" height="34"/><text class="ink" x="179.0" y="109.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="196" y="87" width="34" height="34"/><text class="ink" x="213.0" y="109.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="162" y="121" width="34" height="34"/><text class="ink" x="179.0" y="143.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="196" y="121" width="34" height="34"/><text class="ink" x="213.0" y="143.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="270" y="70" width="34" height="34"/><text class="ink" x="287.0" y="92.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="304" y="70" width="34" height="34"/><text class="ink" x="321.0" y="92.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="270" y="104" width="34" height="34"/><text class="ink" x="287.0" y="126.0" font-size="14" text-anchor="middle">16</text><rect class="box" x="304" y="104" width="34" height="34"/><text class="ink" x="321.0" y="126.0" font-size="14" text-anchor="middle">11</text><rect class="curve" x="17" y="67" width="108" height="40" rx="4"/><rect class="curve2" x="193" y="50" width="40" height="108" rx="4"/><rect class="curve4" x="301" y="67" width="40" height="40" rx="4"/><text class="ink" x="71.0" y="56" font-size="12" text-anchor="middle">A  (2 × 3)</text><text class="ink" x="196" y="39" font-size="12" text-anchor="middle">B  (3 × 2)</text><text class="ink" x="304" y="56" font-size="12" text-anchor="middle">AB  (2 × 2)</text><text class="ink" x="142" y="109" font-size="20" text-anchor="middle">·</text><text class="ink" x="250" y="109" font-size="18" text-anchor="middle">=</text><text class="ink" x="71.0" y="160" font-size="12" text-anchor="middle">1. satır</text><text class="ink" x="213.0" y="175" font-size="12" text-anchor="middle">2. sütun</text><text class="ink" x="200" y="212" font-size="14" text-anchor="middle">c₁₂ = 1 · 0 + 2 · 1 + 3 · 1 = 5</text></svg>
  <figcaption>$A$'nın 1. satırı (mor) ile $B$'nin 2. sütunu (turuncu) çarpılıp toplanınca $AB$'nin 1. satır 2. sütundaki elemanı (yeşil) çıkıyor.</figcaption>
</figure>

Bir örnekle bütün elemanları hesaplayalım:

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
\qquad
B = \begin{bmatrix} 1 & 4 \\ 2 & -1 \end{bmatrix}
$$

Her eleman için bir satır ve bir sütun seçiyoruz:

$$
\begin{aligned}
c_{11} &= (2, 1) \cdot (1, 2) = 2 + 2 = 4 \\
c_{12} &= (2, 1) \cdot (4, -1) = 8 - 1 = 7 \\
c_{21} &= (0, 3) \cdot (1, 2) = 0 + 6 = 6 \\
c_{22} &= (0, 3) \cdot (4, -1) = 0 - 3 = -3
\end{aligned}
$$

$$
AB = \begin{bmatrix} 4 & 7 \\ 6 & -3 \end{bmatrix}
$$

**Pratik düzen:** $c_{ij}$'yi hesaplarken sol elinin parmağını $A$'nın
$i$. satırında soldan sağa, sağ elininkini $B$'nin $j$. sütununda yukarıdan
aşağıya gezdir; parmakların durduğu sayıları çarp ve topla.

## Sütun bakışı: $B$'nin her sütunu ayrı bir matris–vektör çarpımı

$B$'yi sütunlarına ayırırsak, $AB$'nin her sütunu $A$ ile $B$'nin o
sütununun çarpımı:

$$
AB = A \begin{bmatrix} \mathbf{b}_1 & \mathbf{b}_2 \end{bmatrix} = \begin{bmatrix} A\mathbf{b}_1 & A\mathbf{b}_2 \end{bmatrix}
$$

Yukarıdaki örnekte:

$$
A\mathbf{b}_1 = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}
$$

Bu, $AB$'nin 1. sütunu. Matris çarpımı demek, **aynı $A$'yı birçok
vektöre birden uygulamak** demek. Bir veri matrisinin bütün satırlarını
aynı ağırlıklarla çarpmak ya da bir fotoğrafın bütün noktalarını aynı
şekilde döndürmek tam olarak bu.

## Çarpım sıraya bağlıdır

Sayılarda $3 \cdot 5 = 5 \cdot 3$. Matrislerde bu **genellikle doğru
değil**. Aynı $A$ ve $B$ için $BA$'yı hesaplayalım:

$$
BA = \begin{bmatrix} 1 & 4 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} = \begin{bmatrix} 2 & 13 \\ 4 & -1 \end{bmatrix}
$$

$AB = \begin{bmatrix} 4 & 7 \\ 6 & -3 \end{bmatrix}$ idi. İkisi farklı:
$AB \ne BA$. Üstelik bazen biri tanımlıyken öteki tanımsız bile olabilir:
$A$ $2 \times 3$ ve $B$ $3 \times 4$ ise $AB$ var ($2 \times 4$), $BA$ yok
($4 \ne 2$).

Bu yüzden matris çarpımında "soldan çarpmak" ile "sağdan çarpmak" ayrı
şeyler. Bir eşitliğin iki tarafını bir matrisle çarparken **aynı taraftan**
çarpmak gerekiyor.

**Neden böyle?** Birazdan göreceğimiz gibi matris bir **dönüşüm** ve
çarpım iki dönüşümü art arda yapmak. Önce ayakkabı sonra çorap giymek, önce
çorap sonra ayakkabı giymekle aynı sonucu vermez; dönüşümlerde de sıra
önemli.

## Çarpımın kuralları

Sıra dışında sayılardaki kuralların çoğu geçerli:

| Kural | Yazılış |
|---|---|
| Birleşme | $(AB)C = A(BC)$ |
| Soldan dağılma | $A(B + C) = AB + AC$ |
| Sağdan dağılma | $(A + B)C = AC + BC$ |
| Skaler | $(cA)B = c(AB) = A(cB)$ |
| Birim matris | $AI = IA = A$ |
| Devrik | $(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$ |
| Değişme | **genelde yok:** $AB \ne BA$ |

**Birleşme** çok işe yarıyor: $(AB)C$ ile $A(BC)$ aynı, parantezi istediğin
yere koyabilirsin (ama sırayı değiştiremezsin). Üç dönüşümü art arda yapmak
için hangi ikisini önce birleştirdiğin fark etmez.

**Devriğin kuralı sırayı ters çevirir:** $(AB)^\mathsf{T} = B^\mathsf{T}
A^\mathsf{T}$, $A^\mathsf{T} B^\mathsf{T}$ değil. Örneğimizde:

$$
(AB)^\mathsf{T} = \begin{bmatrix} 4 & 6 \\ 7 & -3 \end{bmatrix}
= \begin{bmatrix} 1 & 2 \\ 4 & -1 \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}
= B^\mathsf{T} A^\mathsf{T}
$$

Boyutlara bakınca da mantıklı: $A$ $2 \times 3$, $B$ $3 \times 4$ ise
$(AB)^\mathsf{T}$ $4 \times 2$; $B^\mathsf{T}$ ($4 \times 3$) çarpı
$A^\mathsf{T}$ ($3 \times 2$) de $4 \times 2$. Öteki sıra çarpılamaz bile.

### Kuvvetler

Kare bir matris kendisiyle çarpılabilir: $A^2 = AA$, $A^3 = AAA$.

$$
A^2 = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} = \begin{bmatrix} 4 & 5 \\ 0 & 9 \end{bmatrix}
$$

**Dikkat:** $A^2$, elemanların karesini almak **değil**. Elemanların
karesi $\begin{bmatrix} 4 & 1 \\ 0 & 9 \end{bmatrix}$ olurdu; sağ üstteki
$5$ ile $1$ farklı.

## Matris bir dönüşümdür

Şimdi bölümün ikinci ve belki en önemli fikri. $2 \times 2$ bir matrisi
bir vektörle çarpınca yeni bir vektör çıkıyor. Yani matris, düzlemin her
noktasını başka bir noktaya **götüren** bir kural: bir **dönüşüm**.

### Sütunlar her şeyi söyler

Bir matrisin ne yaptığını anlamanın kısa yolu, iki temel birim vektörün
nereye gittiğine bakmak: $\mathbf{e}_1 = (1, 0)$ ve $\mathbf{e}_2 = (0, 1)$.

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} a \\ c \end{bmatrix}
\qquad
\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} b \\ d \end{bmatrix}
$$

**$\mathbf{e}_1$ matrisin 1. sütununa, $\mathbf{e}_2$ 2. sütununa gidiyor.**
Başka her vektör $\mathbf{e}_1$ ile $\mathbf{e}_2$'den kurulduğu için
($(x, y) = x\,\mathbf{e}_1 + y\,\mathbf{e}_2$), onların nereye gittiğini
bilmek her şeyin nereye gittiğini bilmek demek. Bu, matris–vektör
çarpımının sütun bakışının geometrideki karşılığı.

Tersinden de düşünebiliriz: "düzlemi şöyle dönüştürmek istiyorum" dediğinde
matrisini yazmak için $\mathbf{e}_1$'in ve $\mathbf{e}_2$'nin gitmesini
istediğin yerleri sütun olarak yan yana koyman yeterli.

### Dört temel dönüşüm

<figure class="fig">
<svg viewBox="0 0 400 444" width="400"><line class="grid" x1="26" y1="152" x2="26" y2="16"/><line class="grid" x1="60" y1="152" x2="60" y2="16"/><line class="line" x1="94" y1="152" x2="94" y2="16"/><line class="grid" x1="128" y1="152" x2="128" y2="16"/><line class="grid" x1="162" y1="152" x2="162" y2="16"/><line class="grid" x1="26" y1="152" x2="162" y2="152"/><line class="grid" x1="26" y1="118" x2="162" y2="118"/><line class="line" x1="26" y1="84" x2="162" y2="84"/><line class="grid" x1="26" y1="50" x2="162" y2="50"/><line class="grid" x1="26" y1="16" x2="162" y2="16"/><polygon class="curve3" stroke-dasharray="4 3" points="94,84 128,84 128,50 94,50"/><polygon class="dot" opacity="0.16" points="94,84 162,84 162,50 94,50"/><polygon class="curve3" points="94,84 162,84 162,50 94,50"/><line class="curve" x1="94" y1="84" x2="154.8" y2="84.0"/><polygon class="dot" points="162,84 153.8,87.7 153.8,80.3"/><line class="curve2" x1="94" y1="84" x2="94.0" y2="57.2"/><polygon class="dot2" points="94,50 97.7,58.2 90.3,58.2"/><text class="ink" x="94.0" y="170" font-size="12" text-anchor="middle">Ölçekleme</text><text class="dim" x="94.0" y="185" font-size="11" text-anchor="middle">[2 0; 0 1]</text><line class="grid" x1="222" y1="152" x2="222" y2="16"/><line class="grid" x1="256" y1="152" x2="256" y2="16"/><line class="line" x1="290" y1="152" x2="290" y2="16"/><line class="grid" x1="324" y1="152" x2="324" y2="16"/><line class="grid" x1="358" y1="152" x2="358" y2="16"/><line class="grid" x1="222" y1="152" x2="358" y2="152"/><line class="grid" x1="222" y1="118" x2="358" y2="118"/><line class="line" x1="222" y1="84" x2="358" y2="84"/><line class="grid" x1="222" y1="50" x2="358" y2="50"/><line class="grid" x1="222" y1="16" x2="358" y2="16"/><polygon class="curve3" stroke-dasharray="4 3" points="290,84 324,84 324,50 290,50"/><polygon class="dot" opacity="0.16" points="290,84 290,50 256,50 256,84"/><polygon class="curve3" points="290,84 290,50 256,50 256,84"/><line class="curve" x1="290" y1="84" x2="290.0" y2="57.2"/><polygon class="dot" points="290,50 293.7,58.2 286.3,58.2"/><line class="curve2" x1="290" y1="84" x2="263.2" y2="84.0"/><polygon class="dot2" points="256,84 264.2,80.3 264.2,87.7"/><text class="ink" x="290.0" y="170" font-size="12" text-anchor="middle">90° döndürme</text><text class="dim" x="290.0" y="185" font-size="11" text-anchor="middle">[0 −1; 1 0]</text><line class="grid" x1="26" y1="366" x2="26" y2="230"/><line class="grid" x1="60" y1="366" x2="60" y2="230"/><line class="line" x1="94" y1="366" x2="94" y2="230"/><line class="grid" x1="128" y1="366" x2="128" y2="230"/><line class="grid" x1="162" y1="366" x2="162" y2="230"/><line class="grid" x1="26" y1="366" x2="162" y2="366"/><line class="grid" x1="26" y1="332" x2="162" y2="332"/><line class="line" x1="26" y1="298" x2="162" y2="298"/><line class="grid" x1="26" y1="264" x2="162" y2="264"/><line class="grid" x1="26" y1="230" x2="162" y2="230"/><polygon class="curve3" stroke-dasharray="4 3" points="94,298 128,298 128,264 94,264"/><polygon class="dot" opacity="0.16" points="94,298 128,298 128,332 94,332"/><polygon class="curve3" points="94,298 128,298 128,332 94,332"/><line class="curve" x1="94" y1="298" x2="120.8" y2="298.0"/><polygon class="dot" points="128,298 119.8,301.7 119.8,294.3"/><line class="curve2" x1="94" y1="298" x2="94.0" y2="324.8"/><polygon class="dot2" points="94,332 90.3,323.8 97.7,323.8"/><text class="ink" x="94.0" y="384" font-size="12" text-anchor="middle">x eksenine yansıma</text><text class="dim" x="94.0" y="399" font-size="11" text-anchor="middle">[1 0; 0 −1]</text><line class="grid" x1="222" y1="366" x2="222" y2="230"/><line class="grid" x1="256" y1="366" x2="256" y2="230"/><line class="line" x1="290" y1="366" x2="290" y2="230"/><line class="grid" x1="324" y1="366" x2="324" y2="230"/><line class="grid" x1="358" y1="366" x2="358" y2="230"/><line class="grid" x1="222" y1="366" x2="358" y2="366"/><line class="grid" x1="222" y1="332" x2="358" y2="332"/><line class="line" x1="222" y1="298" x2="358" y2="298"/><line class="grid" x1="222" y1="264" x2="358" y2="264"/><line class="grid" x1="222" y1="230" x2="358" y2="230"/><polygon class="curve3" stroke-dasharray="4 3" points="290,298 324,298 324,264 290,264"/><polygon class="dot" opacity="0.16" points="290,298 324,298 358,264 324,264"/><polygon class="curve3" points="290,298 324,298 358,264 324,264"/><line class="curve" x1="290" y1="298" x2="316.8" y2="298.0"/><polygon class="dot" points="324,298 315.8,301.7 315.8,294.3"/><line class="curve2" x1="290" y1="298" x2="318.9" y2="269.1"/><polygon class="dot2" points="324,264 320.8,272.4 315.6,267.2"/><text class="ink" x="290.0" y="384" font-size="12" text-anchor="middle">Kaydırma</text><text class="dim" x="290.0" y="399" font-size="11" text-anchor="middle">[1 1; 0 1]</text></svg>
  <figcaption>Kesikli kare dönüşümden önceki birim kare, dolu şekil sonrası. Mor ok $\mathbf{e}_1$'in, turuncu ok $\mathbf{e}_2$'nin gittiği yer: matrisin 1. ve 2. sütunu.</figcaption>
</figure>

| Dönüşüm | Matris | Ne yapıyor? |
|---|---|---|
| Ölçekleme | $\begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$ | $x$'i 2 katına çıkarıyor, $y$'ye dokunmuyor |
| 90° döndürme | $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | Her şeyi saat yönünün tersine 90° çeviriyor |
| Yansıma | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | $x$ eksenine göre ayna: $(x, y) \to (x, -y)$ |
| Kaydırma | $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ | Yukarıdaki noktaları sağa kaydırıyor: $(x, y) \to (x + y, y)$ |
| İzdüşüm | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | Her noktayı $x$ eksenine indiriyor: $(x, y) \to (x, 0)$ |

Bir örnekle döndürmeyi kontrol edelim. $(3, 1)$ noktasını 90° döndürelim:

$$
\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \cdot 3 + (-1) \cdot 1 \\ 1 \cdot 3 + 0 \cdot 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 3 \end{bmatrix}
$$

$(3, 1)$ sağda ve biraz yukarıdaydı, $(-1, 3)$ yukarıda ve biraz solda:
gerçekten çeyrek tur dönmüş. Uzunluk da değişmedi: $\sqrt{9 + 1} =
\sqrt{1 + 9}$.

### Herhangi bir açıyla döndürme

Saat yönünün tersine $\theta$ açısıyla döndürme:

$$
R_\theta = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
$$

Sütun kuralıyla okuyalım: $\mathbf{e}_1 = (1, 0)$, birim çember üzerinde
$\theta$ kadar dönünce $(\cos\theta, \sin\theta)$'ya varıyor (1. sütun).
$\mathbf{e}_2$ de ondan $90°$ ileride, $(-\sin\theta, \cos\theta)$'da (2.
sütun). $\theta = 90°$ koyunca $\cos 90° = 0$, $\sin 90° = 1$ ve yukarıdaki
matris çıkıyor.

### Doğrusal dönüşüm ne demek?

Matrisle yapılan her dönüşümün iki özelliği var (Matrisler bölümündeki
kurallar):

$$
A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}
\qquad
A(c\,\mathbf{x}) = c\,A\mathbf{x}
$$

Geometrik anlamı: **başlangıç noktası yerinde kalır, doğrular doğru
kalır, paralel doğrular paralel kalır ve ızgara çizgileri eşit aralıklı
kalır.** Kare paralelkenara dönüşebilir ama asla eğriye dönüşmez. Bu
özelliklere sahip dönüşümlere **doğrusal dönüşüm** denir ve her doğrusal
dönüşüm bir matrisle yazılabilir.

Öteleme (her noktayı $(1, 0)$ kadar kaydırmak) bu anlamda doğrusal
**değil**: başlangıç noktasını yerinden oynatıyor, o yüzden tek bir
$2 \times 2$ matrisle yazılamıyor.

## Art arda iki dönüşüm = matris çarpımı

Bir vektöre önce $B$'yi, sonra $A$'yı uygulayalım:

$$
A(B\mathbf{x}) = (AB)\mathbf{x}
$$

Bu eşitlik birleşme kuralından geliyor ve çok şey söylüyor: **iki
dönüşümü art arda yapmak, çarpımları olan tek bir dönüşümü yapmakla
aynı.** Bin noktayı önce döndürüp sonra ölçeklemek yerine, iki matrisi bir
kez çarpıp tek matrisi bin noktaya uygulayabilirsin.

**Okuma sırası sağdan sola.** $AB\mathbf{x}$'te vektöre en yakın matris
($B$) önce uygulanıyor. $AB$ "önce $B$, sonra $A$" demek. Fonksiyonlarda
$f(g(x))$'te önce $g$'nin uygulanmasıyla aynı.

### Sıra neden önemli: bir örnek

$R$ 90° döndürme, $S$ $x$ eksenine yansıma olsun. $\mathbf{v} = (2, 1)$
vektörüne ikisini iki farklı sırada uygulayalım.

<figure class="fig">
<svg viewBox="0 0 420 212" width="420"><line class="grid" x1="30" y1="176" x2="30" y2="16"/><line class="grid" x1="70" y1="176" x2="70" y2="16"/><line class="line" x1="110" y1="176" x2="110" y2="16"/><line class="grid" x1="150" y1="176" x2="150" y2="16"/><line class="grid" x1="190" y1="176" x2="190" y2="16"/><line class="grid" x1="30" y1="176" x2="190" y2="176"/><line class="grid" x1="30" y1="136" x2="190" y2="136"/><line class="line" x1="30" y1="96" x2="190" y2="96"/><line class="grid" x1="30" y1="56" x2="190" y2="56"/><line class="grid" x1="30" y1="16" x2="190" y2="16"/><text class="dim" x="30" y="109" font-size="9" text-anchor="middle">-2</text><text class="dim" x="70" y="109" font-size="9" text-anchor="middle">-1</text><text class="dim" x="150" y="109" font-size="9" text-anchor="middle">1</text><text class="dim" x="190" y="109" font-size="9" text-anchor="middle">2</text><text class="dim" x="105" y="179" font-size="9" text-anchor="end">-2</text><text class="dim" x="105" y="139" font-size="9" text-anchor="end">-1</text><text class="dim" x="105" y="59" font-size="9" text-anchor="end">1</text><text class="dim" x="105" y="19" font-size="9" text-anchor="end">2</text><line class="curve4" x1="110" y1="96" x2="183.6" y2="59.2"/><polygon class="dot3" points="190,56 184.3,63.0 181.0,56.4"/><line class="curve3" stroke-dasharray="4 3" x1="110" y1="96" x2="73.2" y2="22.4"/><polygon class="dim" points="70,16 77.0,21.7 70.4,25.0"/><line class="curve" x1="110" y1="96" x2="73.2" y2="169.6"/><polygon class="dot" points="70,176 70.4,167.0 77.0,170.3"/><text class="ink" x="195" y="52" font-size="12" text-anchor="start">v</text><text class="ink" x="63" y="180" font-size="11" text-anchor="end">(-1, -2)</text><text class="ink" x="110.0" y="200" font-size="12" text-anchor="middle">Önce döndür, sonra yansıt: SRv</text><line class="grid" x1="240" y1="176" x2="240" y2="16"/><line class="grid" x1="280" y1="176" x2="280" y2="16"/><line class="line" x1="320" y1="176" x2="320" y2="16"/><line class="grid" x1="360" y1="176" x2="360" y2="16"/><line class="grid" x1="400" y1="176" x2="400" y2="16"/><line class="grid" x1="240" y1="176" x2="400" y2="176"/><line class="grid" x1="240" y1="136" x2="400" y2="136"/><line class="line" x1="240" y1="96" x2="400" y2="96"/><line class="grid" x1="240" y1="56" x2="400" y2="56"/><line class="grid" x1="240" y1="16" x2="400" y2="16"/><text class="dim" x="240" y="109" font-size="9" text-anchor="middle">-2</text><text class="dim" x="280" y="109" font-size="9" text-anchor="middle">-1</text><text class="dim" x="360" y="109" font-size="9" text-anchor="middle">1</text><text class="dim" x="400" y="109" font-size="9" text-anchor="middle">2</text><text class="dim" x="315" y="179" font-size="9" text-anchor="end">-2</text><text class="dim" x="315" y="139" font-size="9" text-anchor="end">-1</text><text class="dim" x="315" y="59" font-size="9" text-anchor="end">1</text><text class="dim" x="315" y="19" font-size="9" text-anchor="end">2</text><line class="curve4" x1="320" y1="96" x2="393.6" y2="59.2"/><polygon class="dot3" points="400,56 394.3,63.0 391.0,56.4"/><line class="curve3" stroke-dasharray="4 3" x1="320" y1="96" x2="393.6" y2="132.8"/><polygon class="dim" points="400,136 391.0,135.6 394.3,129.0"/><line class="curve2" x1="320" y1="96" x2="356.8" y2="22.4"/><polygon class="dot2" points="360,16 359.6,25.0 353.0,21.7"/><text class="ink" x="405" y="52" font-size="12" text-anchor="start">v</text><text class="ink" x="367" y="20" font-size="11" text-anchor="start">(1, 2)</text><text class="ink" x="320.0" y="200" font-size="12" text-anchor="middle">Önce yansıt, sonra döndür: RSv</text></svg>
  <figcaption>Yeşil ok $\mathbf{v} = (2, 1)$, kesikli ok ilk dönüşümden sonraki ara durum. Aynı iki dönüşüm, sıra değişince farklı yere varıyor.</figcaption>
</figure>

**Önce döndür, sonra yansıt** ($SR\mathbf{v}$): döndürünce $(-1, 2)$,
sonra yansıtınca $(-1, -2)$.

**Önce yansıt, sonra döndür** ($RS\mathbf{v}$): yansıtınca $(2, -1)$,
sonra döndürünce $(1, 2)$.

İki sonuç farklı. Matrisleri çarparak da görebiliriz:

$$
SR = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}
$$

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

$SR \ne RS$. "Matris çarpımı değişmeli değil" kuralının geometrideki
karşılığı bu.

### Bazı dönüşümler sırayı umursamaz

İki döndürmeyi art arda yapmak, açıları toplanmış tek bir döndürme:
$R_\alpha R_\beta = R_{\alpha + \beta} = R_\beta R_\alpha$. İki ölçekleme de
sırayı umursamaz. Ama bu istisna; genel kural olarak sıra önemli kabul
edilir.

## Makine öğrenmesinde matris çarpımı

**Bir veri matrisinin bütün satırları, bütün modeller.** $X$ $n \times d$
bir veri matrisi (satır = örnek), $W$ $d \times k$ bir ağırlık matrisi
(sütun = bir model) olsun. $XW$ $n \times k$: her örnek için $k$ modelin
tahmini, tek çarpımda. Önceki bölümde tek bir $\mathbf{w}$ ile yaptığımızın
genelleşmiş hâli.

**Sinir ağı katmanları.** Bir katman girdiyi $W_1\mathbf{x}$ ile
dönüştürüyor, sonraki katman sonucu $W_2$ ile. Aradaki doğrusal olmayan
bir işlem (etkinleştirme fonksiyonu) olmasaydı iki katman tek bir katmana
eşit olurdu:

$$
W_2(W_1\mathbf{x}) = (W_2 W_1)\mathbf{x}
$$

Yüz katman da üst üste konsa, doğrusal kaldıkça tek bir matris kadar güçlü.
Sinir ağlarının katmanlar arasına ReLU gibi eğri fonksiyonlar koymasının
sebebi tam olarak bu.

**Görüntü işleme.** Bir fotoğrafı döndürmek, büyütmek ya da aynalamak,
her pikselin koordinatını bir matrisle çarpmak. Veri çoğaltma (aynı
fotoğrafın döndürülmüş, aynalanmış kopyalarıyla modeli eğitmek) bu
dönüşümlerle yapılıyor.

**Hesap maliyeti.** $(m \times n)(n \times p)$ çarpımında her eleman için
$n$ çarpma, toplam $m \cdot n \cdot p$ çarpma var. İki $1000 \times 1000$
matris için bir milyar çarpma. Ekran kartları (GPU) bu tür çok sayıda
bağımsız çarpma–toplamayı aynı anda yapmak için tasarlandığı için derin
öğrenmede kullanılıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$AB = BA$</p>
      <p>$(AB)^\mathsf{T} = A^\mathsf{T} B^\mathsf{T}$</p>
      <p>$A^2$ = elemanların karesi</p>
      <p>$AB$'yi eleman eleman çarpmak</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Genelde $AB \ne BA$</p>
      <p>$(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$</p>
      <p>$A^2 = AA$, satır çarpı sütun</p>
      <p>$c_{ij}$ = $i$. satır · $j$. sütun</p>
    </div>
  </div>
  <figcaption>Matris çarpımı sayı çarpımına benziyor ama sıra ve eleman kuralı farklı.</figcaption>
</figure>

- **Boyutu kontrol etmeden çarpmaya başlamak.** Önce içteki iki sayı eşit
  mi bak, sonra sonucun boyutunu (dıştaki iki sayı) yaz.
- **Eleman eleman çarpmak.** $\begin{bmatrix} 1 & 2 \\ 3 & 4
  \end{bmatrix}$ ile $\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$'nin
  çarpımı $\begin{bmatrix} 5 & 12 \\ 21 & 32 \end{bmatrix}$ değil. Eleman
  eleman çarpmanın da bir adı var (Hadamard çarpımı, $\odot$) ama matris
  çarpımı o değil.
- **Dönüşüm sırasını ters okumak.** $AB\mathbf{x}$'te önce $B$ uygulanır.
- **Devrikte sırayı unutmak.** $(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$.

## Özet

- Boyut: $(m \times n)(n \times p) = m \times p$; içteki sayılar eşit olmalı.
- Eleman: $c_{ij}$ = $A$'nın $i$. satırı · $B$'nin $j$. sütunu.
- Sütun bakışı: $AB$'nin $j$. sütunu $A\mathbf{b}_j$.
- Genelde $AB \ne BA$; birleşme ve dağılma geçerli; $AI = IA = A$.
- $(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$; $A^2 = AA$.
- $2 \times 2$ matris bir dönüşüm: sütunları $\mathbf{e}_1$ ile $\mathbf{e}_2$'nin gittiği yer.
- Ölçekleme, döndürme ($R_\theta$), yansıma, kaydırma, izdüşüm.
- $A(B\mathbf{x}) = (AB)\mathbf{x}$: art arda dönüşüm = çarpım, sağdan sola okunur.
- ML: $XW$ ile bütün örnekler ve modeller; doğrusal katmanlar tek matrise çöker.
