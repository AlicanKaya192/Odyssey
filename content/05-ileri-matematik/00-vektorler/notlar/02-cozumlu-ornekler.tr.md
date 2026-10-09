Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. İki noktadan vektör ve ters yönü

**Soru:** $A(-2, 5)$ ve $B(3, -1)$ için $\overrightarrow{AB}$ ve $\overrightarrow{BA}$ nedir?

Bitiş eksi başlangıç:

$$
\overrightarrow{AB} = B - A = \big(3 - (-2),\ -1 - 5\big) = (5,\ -6)
$$

$$
\overrightarrow{BA} = A - B = (-2 - 3,\ 5 - (-1)) = (-5,\ 6)
$$

İkisi birbirinin eksi işaretlisi: aynı uzunluk, ters yön. Eksi bir sayıyı
çıkarırken işarete dikkat: $3 - (-2) = 5$.

## 2. Üç boyutta doğrusal kombinasyon

**Soru:** $3\,(2, -1, 0) - 2\,(1, 1, 4)$ nedir?

Önce her vektörü kendi skaleriyle çarp, sonra bileşen bileşen çıkar:

$$
(6, -3, 0) - (2, 2, 8) = (6 - 2,\ -3 - 2,\ 0 - 8) = (4,\ -5,\ -8)
$$

Boyut kaç olursa olsun yöntem aynı.

## 3. Eksik katsayıyı bulmak

**Soru:** $a\,(2, 1) + b\,(-1, 3) = (0, 7)$ ise $a$ ve $b$ kaçtır?

Sol tarafı bileşenlerine aç:

$$
(2a - b,\ a + 3b) = (0,\ 7)
$$

İki vektör eşitse bileşenleri tek tek eşittir. İki denklem çıkıyor:

$$
2a - b = 0 \qquad a + 3b = 7
$$

Birinciden $b = 2a$. İkinciye koy: $a + 6a = 7$, yani $a = 1$ ve $b = 2$.

**Sağlama:** $1\,(2, 1) + 2\,(-1, 3) = (2, 1) + (-2, 6) = (0, 7)$. ✓

Bir vektörü başka vektörlerin doğrusal kombinasyonu olarak yazmak her
zaman bir **denklem sistemi** çözmektir. İleri Matematik modülünün Doğrusal Sistemler
bölümü bunu büyük ölçekte yapıyor.

## 4. Uzunluk ve birim vektör

**Soru:** $\mathbf{v} = (5, -12)$ için $\|\mathbf{v}\|$ ve birim vektör nedir?

$$
\|\mathbf{v}\| = \sqrt{5^2 + (-12)^2} = \sqrt{25 + 144} = \sqrt{169} = 13
$$

$$
\hat{\mathbf{v}} = \left(\frac{5}{13},\ \frac{-12}{13}\right) \approx (0.385,\ -0.923)
$$

$(5, 12, 13)$ bir Pisagor üçlüsü; negatif işaret uzunluğu değiştirmiyor.

## 5. Orta nokta ve ortalama vektör

**Soru:** $A(1, 1)$ ile $B(5, 7)$'nin tam ortasındaki nokta nedir?

Orta nokta iki vektörün ortalaması:

$$
M = \frac{A + B}{2} = \frac{(6, 8)}{2} = (3, 4)
$$

Aynı fikir çok nokta için de çalışır. Üç kişinin (boy, kilo) vektörleri
$(160, 55)$, $(170, 65)$ ve $(180, 75)$ ise ortalama vektör:

$$
\frac{(160, 55) + (170, 65) + (180, 75)}{3} = \frac{(510, 195)}{3} = (170,\ 65)
$$

Kümeleme algoritmaları (k-ortalamalar) her kümenin merkezini tam olarak
böyle buluyor.

## 6. Doğru üzerinde bir nokta

**Soru:** $A(2, 1)$'den $B(8, 10)$'a giden yolun üçte birindeki nokta nedir?

$A$'dan başla, $\overrightarrow{AB}$'nin üçte biri kadar yürü:

$$
\overrightarrow{AB} = (6, 9) \qquad
A + \tfrac{1}{3}\,\overrightarrow{AB} = (2, 1) + (2, 3) = (4,\ 4)
$$

Genel hâli $A + t\,\overrightarrow{AB}$: $t = 0$ ise $A$, $t = 1$ ise $B$,
aradaki her $t$ doğru parçası üzerinde bir nokta.

## 7. En yakın komşu

**Soru:** $P(2, 3)$ noktasına $Q(5, 7)$ mi daha yakın, $R(7, 1)$ mi?

$$
\|Q - P\| = \|(3, 4)\| = 5
\qquad
\|R - P\| = \|(5, -2)\| = \sqrt{25 + 4} = \sqrt{29} \approx 5.39
$$

$Q$ daha yakın. Karekök almadan da karşılaştırabilirdin: $25 < 29$.
Uzunlukların karelerini karşılaştırmak aynı sonucu verir ve hesap
makinesi gerektirmez.
