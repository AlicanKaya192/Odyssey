# Determinant ve Ters Matris

Önceki bölümde matrisin bir **dönüşüm** olduğunu gördük: düzlemi
döndürüyor, esnetiyor, yansıtıyor. Bu bölümde iki soru soracağız:

1. Bir matris alanları **kaç katına** çıkarıyor? Bu sorunun cevabı tek bir
   sayı: **determinant**.
2. Bir dönüşümü **geri alabilir miyiz?** Döndürdüğümüz bir şekli eski
   yerine getiren matrise **ters matris** denir.

İki soru birbirine bağlı: determinant sıfırsa dönüşüm geri alınamaz. Bu
bağ, doğrusal denklem sistemlerinin çözümünün var olup olmadığını da
belirliyor. Makine öğrenmesinde doğrusal regresyonun formülü, bir
matrisin tersini içeriyor ve bu tersin olmadığı durum gerçek verilerde
sık karşılaşılan bir sorun.

Ön bilgi: Matris Çarpımı ve Dönüşümler bölümü.

## 2 × 2 determinant

Kare bir matrisin determinantı, o matristen hesaplanan tek bir sayı.
$\det A$ ya da $|A|$ diye yazılır. $2 \times 2$ için formül:

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

**Ana köşegenin çarpımı eksi öteki köşegenin çarpımı.** Örnek:

$$
\det \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} = 3 \cdot 2 - 1 \cdot 1 = 5
$$

Determinant yalnızca **kare** matrisler için tanımlı. $2 \times 3$ bir
matrisin determinantı yok.

## Determinant ne anlatır: alan çarpanı

Formül ezberlemek yerine anlamına bakalım. Önceki bölümde bir matrisin
sütunlarının, $\mathbf{e}_1$ ile $\mathbf{e}_2$'nin gittiği yer olduğunu
gördük. Birim kare (alanı 1) de bu iki sütunun kurduğu bir
**paralelkenara** dönüşüyor.

<figure class="fig">
<svg viewBox="0 0 320 204" width="320"><line class="grid" x1="40" y1="192" x2="40" y2="16"/><line class="line" x1="84" y1="192" x2="84" y2="16"/><line class="grid" x1="128" y1="192" x2="128" y2="16"/><line class="grid" x1="172" y1="192" x2="172" y2="16"/><line class="grid" x1="216" y1="192" x2="216" y2="16"/><line class="grid" x1="260" y1="192" x2="260" y2="16"/><line class="grid" x1="40" y1="192" x2="260" y2="192"/><line class="line" x1="40" y1="148" x2="260" y2="148"/><line class="grid" x1="40" y1="104" x2="260" y2="104"/><line class="grid" x1="40" y1="60" x2="260" y2="60"/><line class="grid" x1="40" y1="16" x2="260" y2="16"/><text class="dim" x="40" y="161" font-size="9" text-anchor="middle">-1</text><text class="dim" x="128" y="161" font-size="9" text-anchor="middle">1</text><text class="dim" x="172" y="161" font-size="9" text-anchor="middle">2</text><text class="dim" x="216" y="161" font-size="9" text-anchor="middle">3</text><text class="dim" x="260" y="161" font-size="9" text-anchor="middle">4</text><text class="dim" x="79" y="195" font-size="9" text-anchor="end">-1</text><text class="dim" x="79" y="107" font-size="9" text-anchor="end">1</text><text class="dim" x="79" y="63" font-size="9" text-anchor="end">2</text><text class="dim" x="79" y="19" font-size="9" text-anchor="end">3</text><polygon class="dot" opacity="0.16" points="84,148 216,104 260,16 128,60"/><polygon class="curve3" points="84,148 216,104 260,16 128,60"/><polygon class="dot2" opacity="0.16" points="84,148 128,148 128,104 84,104"/><polygon class="curve3" stroke-dasharray="4 3" points="84,148 128,148 128,104 84,104"/><line class="curve" x1="84" y1="148" x2="209.2" y2="106.3"/><polygon class="dot" points="216,104 209.4,110.1 207.0,103.1"/><line class="curve2" x1="84" y1="148" x2="124.8" y2="66.4"/><polygon class="dot2" points="128,60 127.6,69.0 121.0,65.7"/><text class="ink" x="106.0" y="130.0" font-size="11" text-anchor="middle">alan 1</text><text class="ink" x="176.4" y="71.0" font-size="13" text-anchor="middle">alan |det A| = 5</text><text class="ink" x="222" y="116" font-size="11" text-anchor="start">(3, 1)</text><text class="ink" x="122" y="56" font-size="11" text-anchor="end">(1, 2)</text></svg>
  <figcaption>$A = \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}$ birim kareyi (turuncu, alan 1) sütunları $(3, 1)$ ve $(1, 2)$ olan paralelkenara (mor) götürüyor. Paralelkenarın alanı $\det A = 5$.</figcaption>
</figure>

**Determinant, matrisin alanları kaç katına çıkardığını söyler.** Birim
kare alanı 5 olan bir paralelkenara dönüştüyse, düzlemdeki **her** şeklin
alanı 5 katına çıkar: alanı 2 olan bir üçgen, alanı 10 olan bir üçgene
dönüşür. Çünkü her şekil küçük karelerden kurulabilir ve her küçük kare
aynı oranda büyür.

Tanıdık dönüşümlerle kontrol edelim:

| Matris | Dönüşüm | $\det$ | Anlamı |
|---|---|---|---|
| $\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ | Ölçekleme | $6$ | Genişlik 2, yükseklik 3 kat: alan 6 kat |
| $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | $90°$ döndürme | $1$ | Döndürme alanı değiştirmez |
| $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ | Kaydırma | $1$ | Kare eğilir ama alanı aynı kalır |
| $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | İzdüşüm | $0$ | Kare bir doğru parçasına ezilir |

Kaydırmanın alanı değiştirmemesi ilginç: kare bir paralelkenara dönüşüyor
ama tabanı da yüksekliği de aynı kalıyor. Alan = taban × yükseklik.

### İşaret: yön değişti mi?

Determinant **negatif** de olabilir. Mutlak değeri yine alan çarpanı; eksi
işaret ise düzlemin **ters çevrildiğini** (aynadaki görüntüsüne döndüğünü)
söylüyor.

<figure class="fig">
<svg viewBox="0 0 400 208" width="400"><line class="grid" x1="20" y1="176" x2="20" y2="16"/><line class="line" x1="60" y1="176" x2="60" y2="16"/><line class="grid" x1="100" y1="176" x2="100" y2="16"/><line class="grid" x1="140" y1="176" x2="140" y2="16"/><line class="grid" x1="180" y1="176" x2="180" y2="16"/><line class="grid" x1="20" y1="176" x2="180" y2="176"/><line class="line" x1="20" y1="136" x2="180" y2="136"/><line class="grid" x1="20" y1="96" x2="180" y2="96"/><line class="grid" x1="20" y1="56" x2="180" y2="56"/><line class="grid" x1="20" y1="16" x2="180" y2="16"/><polygon class="dot" opacity="0.16" points="60,136 100,136 100,96 60,96"/><polygon class="curve3" points="60,136 100,136 100,96 60,96"/><line class="curve" x1="60" y1="136" x2="92.8" y2="136.0"/><polygon class="dot" points="100,136 91.8,139.7 91.8,132.3"/><line class="curve2" x1="60" y1="136" x2="60.0" y2="103.2"/><polygon class="dot2" points="60,96 63.7,104.2 56.3,104.2"/><text class="ink" x="104" y="150" font-size="12" text-anchor="start">e₁</text><text class="ink" x="55" y="96" font-size="12" text-anchor="end">e₂</text><text class="ink" x="100.0" y="196" font-size="12" text-anchor="middle">Önce: e₂, e₁'in solunda</text><line class="grid" x1="220" y1="176" x2="220" y2="16"/><line class="line" x1="260" y1="176" x2="260" y2="16"/><line class="grid" x1="300" y1="176" x2="300" y2="16"/><line class="grid" x1="340" y1="176" x2="340" y2="16"/><line class="grid" x1="380" y1="176" x2="380" y2="16"/><line class="grid" x1="220" y1="176" x2="380" y2="176"/><line class="line" x1="220" y1="136" x2="380" y2="136"/><line class="grid" x1="220" y1="96" x2="380" y2="96"/><line class="grid" x1="220" y1="56" x2="380" y2="56"/><line class="grid" x1="220" y1="16" x2="380" y2="16"/><polygon class="dot" opacity="0.16" points="260,136 300,56 380,16 340,96"/><polygon class="curve3" points="260,136 300,56 380,16 340,96"/><line class="curve" x1="260" y1="136" x2="296.8" y2="62.4"/><polygon class="dot" points="300,56 299.6,65.0 293.0,61.7"/><line class="curve2" x1="260" y1="136" x2="333.6" y2="99.2"/><polygon class="dot2" points="340,96 334.3,103.0 331.0,96.4"/><text class="ink" x="295" y="56" font-size="12" text-anchor="end">Be₁</text><text class="ink" x="345" y="108" font-size="12" text-anchor="start">Be₂</text><text class="ink" x="300.0" y="196" font-size="12" text-anchor="middle">Sonra: yön ters, det = −3</text></svg>
  <figcaption>Solda $\mathbf{e}_2$, $\mathbf{e}_1$'in solunda (saat yönünün tersinde). $B = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$ uygulandıktan sonra $B\mathbf{e}_2$, $B\mathbf{e}_1$'in sağında kalıyor: düzlem ters dönmüş. $\det B = 1 - 4 = -3$: alan 3 kat, yön ters.</figcaption>
</figure>

Yansımanın determinantı bu yüzden $-1$: alan aynı, yön ters.

$$
\det \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = 1 \cdot (-1) - 0 \cdot 0 = -1
$$

### Sıfır determinant: düzlem eziliyor

$\det A = 0$ ise birim kare **alanı sıfır** olan bir şekle dönüşüyor:
bir doğru parçasına ya da tek bir noktaya. Bu, iki sütunun **aynı doğru
üzerinde** olduğu anlamına geliyor.

<figure class="fig">
<svg viewBox="0 0 310 200" width="310"><line class="grid" x1="30" y1="166" x2="30" y2="16"/><line class="line" x1="80" y1="166" x2="80" y2="16"/><line class="grid" x1="130" y1="166" x2="130" y2="16"/><line class="grid" x1="180" y1="166" x2="180" y2="16"/><line class="grid" x1="230" y1="166" x2="230" y2="16"/><line class="grid" x1="280" y1="166" x2="280" y2="16"/><line class="grid" x1="30" y1="166" x2="280" y2="166"/><line class="line" x1="30" y1="116" x2="280" y2="116"/><line class="grid" x1="30" y1="66" x2="280" y2="66"/><line class="grid" x1="30" y1="16" x2="280" y2="16"/><text class="dim" x="30" y="129" font-size="9" text-anchor="middle">-1</text><text class="dim" x="130" y="129" font-size="9" text-anchor="middle">1</text><text class="dim" x="180" y="129" font-size="9" text-anchor="middle">2</text><text class="dim" x="230" y="129" font-size="9" text-anchor="middle">3</text><text class="dim" x="280" y="129" font-size="9" text-anchor="middle">4</text><text class="dim" x="75" y="169" font-size="9" text-anchor="end">-1</text><text class="dim" x="75" y="69" font-size="9" text-anchor="end">1</text><text class="dim" x="75" y="19" font-size="9" text-anchor="end">2</text><polygon class="dot2" opacity="0.16" points="80,116 130,116 130,66 80,66"/><polygon class="curve3" stroke-dasharray="4 3" points="80,116 130,116 130,66 80,66"/><line class="curve3" stroke-dasharray="4 3" x1="30" y1="141.0" x2="280" y2="16"/><line class="curve4" x1="80" y1="116" x2="230" y2="41.0"/><line class="curve2" x1="80" y1="116" x2="173.6" y2="69.2"/><polygon class="dot2" points="180,66 174.3,73.0 171.0,66.4"/><line class="curve" x1="80" y1="116" x2="123.6" y2="94.2"/><polygon class="dot" points="130,91.0 124.3,98.0 121.0,91.4"/><circle class="dot3" cx="230" cy="41.0" r="3.5"/><text class="ink" x="155.0" y="188" font-size="12" text-anchor="middle">det = 0: bütün düzlem tek bir doğruya eziliyor</text></svg>
  <figcaption>$\begin{bmatrix} 1 & 2 \\ 0.5 & 1 \end{bmatrix}$'nin sütunları $(1, 0.5)$ ve $(2, 1)$ aynı doğru üzerinde. Birim kare yeşil doğru parçasına eziliyor; düzlemin tamamı kesikli doğrunun üstüne düşüyor.</figcaption>
</figure>

$$
\det \begin{bmatrix} 1 & 2 \\ 0.5 & 1 \end{bmatrix} = 1 \cdot 1 - 2 \cdot 0.5 = 0
$$

Burada bilgi **kayboluyor**: düzlemin bütün noktaları tek bir doğruya
iniyor. Farklı pek çok nokta aynı yere gidiyor; örneğin $(2, 0)$ ve
$(0, 1)$'in ikisi de $(2, 1)$'e gidiyor. Sonuca bakıp "hangi noktadan
geldi?" sorusunu cevaplamak artık imkânsız. Birazdan göreceğimiz gibi bu
matrisin tersi yok.

Determinantı sıfır olan matrise **tekil** (singular) matris denir.

## 3 × 3 determinant

Üç boyutta determinant, birim küpün **hacmini** kaç katına çıkardığını
söyler. Hesaplamanın en yaygın yolu **ilk satır boyunca açmak**:

$$
\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= a \begin{vmatrix} e & f \\ h & i \end{vmatrix}
- b \begin{vmatrix} d & f \\ g & i \end{vmatrix}
+ c \begin{vmatrix} d & e \\ g & h \end{vmatrix}
$$

Her ilk satır elemanı, **kendi satırı ve sütunu silinince kalan**
$2 \times 2$ matrisin determinantıyla çarpılıyor. İşaretler sırayla
$+, -, +$. Örnek:

$$
A = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 1 \end{bmatrix}
$$

$$
\begin{aligned}
\det A &= 1 \cdot (1 \cdot 1 - 2 \cdot 1) - 2 \cdot (3 \cdot 1 - 2 \cdot 0) + 0 \cdot (\dots) \\
&= 1 \cdot (-1) - 2 \cdot 3 + 0 \\
&= -7
\end{aligned}
$$

Sıfır olan bir elemanın terimi hesaplanmıyor bile. Bu yüzden açılım için
**en çok sıfır içeren satır ya da sütun** seçilir (işaret deseni
satranç tahtası gibi: $+ - +$, $- + -$, $+ - +$).

**Sarrus kuralı** (yalnızca $3 \times 3$ için): ilk iki sütunu sağa bir
kez daha yaz; soldan sağa inen üç köşegenin çarpımlarını topla, sağdan sola
inen üç köşegenin çarpımlarını çıkar. Aynı örnekte:

$$
(1 \cdot 1 \cdot 1 + 2 \cdot 2 \cdot 0 + 0 \cdot 3 \cdot 1) - (0 \cdot 1 \cdot 0 + 1 \cdot 2 \cdot 1 + 2 \cdot 3 \cdot 1) = 1 - 8 = -7
$$

### Üçgen matrisin determinantı

Köşegenin altı (ya da üstü) tamamen sıfırsa determinant **köşegen
elemanlarının çarpımı**:

$$
\det \begin{bmatrix} 2 & 5 & 1 \\ 0 & 3 & 4 \\ 0 & 0 & -1 \end{bmatrix} = 2 \cdot 3 \cdot (-1) = -6
$$

İlk sütun boyunca açınca her adımda tek bir terim kalıyor. Bir sonraki
bölümdeki Gauss eleme, büyük matrisleri önce üçgen biçime getirip
determinantı böyle hesaplıyor.

## Determinantın kuralları

| Kural | Yazılış | Anlamı |
|---|---|---|
| Çarpım | $\det(AB) = \det A \cdot \det B$ | Art arda dönüşümde alan çarpanları çarpılır |
| Devrik | $\det(A^\mathsf{T}) = \det A$ | Satırlar ve sütunlar eşit haklı |
| Birim | $\det I = 1$ | Hiçbir şey değişmiyor |
| Skaler | $\det(cA) = c^n \det A$ | $n \times n$ matriste her boyut $c$ kat |
| Satır değiştirme | işaret değişir | İki satırın yeri değişince yön ters döner |
| Satır ekleme | değişmez | Bir satıra başka bir satırın katını eklemek bir kaydırma |
| Aynı iki satır | $\det = 0$ | Satırlar aynı doğruda |

**Çarpım kuralı** geometriden geliyor: önce $B$ alanı 2 katına, sonra $A$
5 katına çıkarıyorsa toplam 10 kat. Örnek:

$$
\det \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} = 5
\qquad
\det \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix} = 2
$$

$$
\det \left( \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix} \right) = \det \begin{bmatrix} 3 & 5 \\ 1 & 5 \end{bmatrix} = 15 - 5 = 10
$$

**Skaler kuralına dikkat:** $2 \times 2$ bir matrisi 2 ile çarpmak her
iki yönü 2 katına çıkarıyor, alan 4 katına çıkıyor: $\det(2A) = 4 \det A$,
$2 \det A$ değil. $3 \times 3$'te $2^3 = 8$ kat.

**Toplama kuralı yok:** $\det(A + B) \ne \det A + \det B$ (genelde).

## Ters matris

Bir sayının tersi, onunla çarpınca 1 veren sayı: $5 \cdot \tfrac{1}{5} = 1$.
Matrislerde 1'in karşılığı birim matris $I$. Kare bir $A$ matrisinin
**tersi** $A^{-1}$, şu eşitliği sağlayan matris:

$$
A A^{-1} = A^{-1} A = I
$$

Dönüşüm diliyle: $A^{-1}$, $A$'nın yaptığını **geri alan** dönüşüm. $A$
bir noktayı götürdüyse $A^{-1}$ onu eski yerine getirir:
$A^{-1}(A\mathbf{x}) = \mathbf{x}$.

### 2 × 2 tersin formülü

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Üç hareket: **köşegendeki iki elemanın yerini değiştir, öteki ikisinin
işaretini çevir, determinanta böl.** Örnek:

$$
A = \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}
\qquad
\det A = 5
$$

$$
A^{-1} = \frac{1}{5} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} = \begin{bmatrix} 0.4 & -0.2 \\ -0.2 & 0.6 \end{bmatrix}
$$

**Her zaman sağlama yap:** $AA^{-1}$ gerçekten $I$ mi?

$$
\begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} = \begin{bmatrix} 6 - 1 & -3 + 3 \\ 2 - 2 & -1 + 6 \end{bmatrix} = \begin{bmatrix} 5 & 0 \\ 0 & 5 \end{bmatrix}
$$

$5$'e bölününce $I$. ✓ (Bölmeyi sona bırakınca kesirlerle uğraşmak
gerekmiyor.)

### Ne zaman ters yok?

Formülde determinanta bölüyoruz. **$\det A = 0$ ise ters yok.** Geometrik
nedeni yukarıda gördük: determinant sıfırsa düzlem bir doğruya eziliyor,
birçok nokta aynı yere gidiyor ve hangisinin nereden geldiği
bilinemiyor. Ezilmiş bir şeyi eski hâline döndüren bir dönüşüm olamaz.

$$
A^{-1} \text{ vardır} \iff \det A \ne 0
$$

Tersi olan matrise **tersinir** (invertible) ya da **tekil olmayan**
matris denir.

### Dönüşümlerin tersleri

Geometrik olarak düşününce çoğu tersi hesap yapmadan yazabilirsin:

| Dönüşüm | Tersi |
|---|---|
| $\theta$ kadar döndürme | $-\theta$ kadar döndürme |
| $x$'i 2 katına çıkarma | $x$'i yarıya indirme |
| $k$ kadar kaydırma | $-k$ kadar kaydırma |
| Yansıma | Kendisi (iki kez yansıtınca eski yerine döner) |
| İzdüşüm | **Yok** (yükseklik bilgisi kayboldu) |

### Tersin kuralları

| Kural | Yazılış |
|---|---|
| Tersin tersi | $(A^{-1})^{-1} = A$ |
| Çarpımın tersi | $(AB)^{-1} = B^{-1} A^{-1}$ |
| Devriğin tersi | $(A^\mathsf{T})^{-1} = (A^{-1})^\mathsf{T}$ |
| Determinant | $\det(A^{-1}) = \dfrac{1}{\det A}$ |

**Çarpımın tersinde sıra ters döner**, tıpkı devrikte olduğu gibi. Sabah
önce çorap sonra ayakkabı giyersin; akşam önce ayakkabıyı sonra çorabı
çıkarırsın. $AB$ "önce $B$, sonra $A$" demekse, geri almak için önce
$A$'yı, sonra $B$'yi geri alman gerekir: $B^{-1} A^{-1}$.

## Ters matrisle denklem çözmek

Bir denklem sistemi matris biçiminde yazılabilir:

$$
\begin{aligned}
3x + y &= 5 \\
x + 2y &= 5
\end{aligned}
\qquad \Longleftrightarrow \qquad
\begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 5 \\ 5 \end{bmatrix}
$$

Sayılarda $3x = 5$ denklemini iki tarafı 3'e bölerek çözeriz. Matrislerde
bölme yok, ama iki tarafı **soldan** $A^{-1}$ ile çarpabiliriz:

$$
A\mathbf{x} = \mathbf{b} \quad \Rightarrow \quad A^{-1} A \mathbf{x} = A^{-1}\mathbf{b} \quad \Rightarrow \quad \mathbf{x} = A^{-1}\mathbf{b}
$$

Bizim örnekte $A^{-1}$'i zaten bulduk:

$$
\mathbf{x} = \frac{1}{5} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} \begin{bmatrix} 5 \\ 5 \end{bmatrix} = \frac{1}{5} \begin{bmatrix} 5 \\ 10 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
$$

Sağlama: $3 \cdot 1 + 2 = 5$ ve $1 + 2 \cdot 2 = 5$. ✓

**Soldan çarpmak şart.** $A\mathbf{x}$'in sağından $A^{-1}$ ile çarpmak
($A\mathbf{x}A^{-1}$) boyut bakımından bile tanımsız; matris çarpımı
değişmeli olmadığı için hangi taraftan çarptığın önemli.

**Determinant ve çözüm sayısı.** $\det A \ne 0$ ise sistemin **tam bir**
çözümü var: $\mathbf{x} = A^{-1}\mathbf{b}$. $\det A = 0$ ise ya hiç
çözüm yok ya da sonsuz çözüm var; bu durumları bir sonraki bölümde Gauss
eleme ile inceleyeceğiz.

**Uygulamada:** Bilgisayar büyük sistemleri çözerken tersi hesaplamaz;
Gauss eleme (bir sonraki bölüm) hem daha hızlı hem de yuvarlama
hatalarına karşı daha sağlam. Ters matris daha çok **formül yazarken**
kullanılıyor: $\mathbf{x} = A^{-1}\mathbf{b}$ "çözüm budur" demenin kısa
yolu.

## Makine öğrenmesinde determinant ve ters

**Doğrusal regresyonun kapalı formülü.** Veri matrisi $X$ ve hedefler
$\mathbf{y}$ için en iyi ağırlıklar:

$$
\mathbf{w} = (X^\mathsf{T} X)^{-1} X^\mathsf{T} \mathbf{y}
$$

Bu formülün nereden geldiğini Doğrusal Regresyonun Matematiği bölümünde
göreceğiz. Şimdilik önemli olan şu: içinde bir **ters** var ve
$X^\mathsf{T} X$ tekilse formül çalışmıyor.

**Tekrarlanan özellik sorunu.** Veride bir özellik ötekinin katıysa
(metrekare ile "yüz metrekare" aynı tabloda iki sütun olarak duruyorsa)
$X$'in sütunları aynı doğru üzerinde olur ve $\det(X^\mathsf{T} X) = 0$
çıkar. Model iki sütunun etkisini birbirinden ayıramaz. Bu soruna
**çoklu doğrusal bağlantı** (multicollinearity) denir. Neredeyse aynı
sütunlarda determinant sıfıra çok yakın çıkar ve ağırlıklar kararsız,
çok büyük sayılara kaçar.

**Ridge düzenlileştirmesi** bunu çözmek için köşegene küçük bir sayı
ekler: $(X^\mathsf{T} X + \lambda I)^{-1}$. $\lambda > 0$ eklenince
matris her zaman tersinir olur.

**Çok değişkenli normal dağılım** (olasılık bölümleri): formülünde
kovaryans matrisinin determinantı ve tersi geçiyor. Determinant verinin
ne kadar "yayıldığını" (hacim), ters ise uzaklığın hangi yönlerde daha
önemli olduğunu anlatıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\det(A + B) = \det A + \det B$</p>
      <p>$\det(2A) = 2 \det A$ ($2 \times 2$)</p>
      <p>$(AB)^{-1} = A^{-1} B^{-1}$</p>
      <p>Tersi: her elemanın tersi $1/a_{ij}$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Toplam için kural yok; $\det(AB) = \det A \det B$</p>
      <p>$\det(2A) = 4 \det A$</p>
      <p>$(AB)^{-1} = B^{-1} A^{-1}$</p>
      <p>$\frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$</p>
    </div>
  </div>
  <figcaption>Determinant çarpımla uyumlu, toplamla değil. Ters matris elemanların tersi değil.</figcaption>
</figure>

- **Tersin formülünde yerleri karıştırmak.** Köşegendeki $a$ ile $d$ yer
  değiştirir; $b$ ile $c$ **yerinde kalır**, yalnızca işaretleri değişir.
- **Determinantı hesaplamadan tersi yazmak.** Önce $\det$'e bak; sıfırsa
  ters yok, formülü uygulamaya çalışma.
- **$3 \times 3$ açılımda işaretleri unutmak.** İlk satırda $+, -, +$.
- **Sağlamayı atlamak.** $AA^{-1} = I$ çıkıyor mu, bir kez çarp.

## Özet

- $\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$; yalnızca kare matriste.
- $|\det A|$ alan (3 boyutta hacim) çarpanı; eksi işaret yönün ters döndüğünü söyler.
- $\det A = 0$: düzlem eziliyor, bilgi kayboluyor, matris tekil.
- $3 \times 3$: ilk satır boyunca açılım ($+, -, +$) ya da Sarrus; üçgen matriste köşegen çarpımı.
- $\det(AB) = \det A \det B$, $\det(A^\mathsf{T}) = \det A$, $\det(cA) = c^n \det A$.
- $A A^{-1} = I$; $2 \times 2$: yer değiştir, işaret çevir, determinanta böl.
- Ters var $\iff$ $\det A \ne 0$. $(AB)^{-1} = B^{-1}A^{-1}$.
- $A\mathbf{x} = \mathbf{b}$ ise $\mathbf{x} = A^{-1}\mathbf{b}$ (soldan çarp).
- ML: $(X^\mathsf{T}X)^{-1}$, tekrarlanan özellik $\Rightarrow$ tekil matris, ridge $+\lambda I$.
