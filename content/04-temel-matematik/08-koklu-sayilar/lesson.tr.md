# Köklü Sayılar

Kare almak bir sayıyı kendisiyle çarpmaktı: $7^2 = 49$. **Karekök** bunun
tersini soruyor: karesi $49$ olan sayı hangisi? Kökler uzaklıklarda,
alanlardan kenar bulmada ve istatistikte her yerde: bir vektörün uzunluğu,
standart sapma ve bir modelin ortalama hatası (RMSE) hep bir karekökle
hesaplanıyor. Bu bölümde karekökü, kök kurallarını, sadeleştirmeyi ve
kesirli üsleri göreceğiz.

Ön bilgi: Üslü Sayılar bölümü.

## Karekök nedir?

$a \ge 0$ için $\sqrt{a}$, **karesi $a$ olan negatif olmayan sayıdır**:

$$
\sqrt{49} = 7 \quad\text{çünkü}\quad 7^2 = 49 \text{ ve } 7 \ge 0
$$

$(-7)^2$ de $49$ ama $\sqrt{49}$ tek bir sayıyı gösterir: pozitif olanı.
"Karesi $49$ olan sayılar" sorulursa cevap iki tane: $x^2 = 49$ ise $x = 7$
ya da $x = -7$, kısaca $x = \pm 7$.

**Negatif sayının karekökü** gerçek sayılarda yok: hiçbir gerçek sayının
karesi negatif değil. $\sqrt{-4}$ tanımsız.

Karekökün geometrik anlamı: **alanı $a$ olan karenin kenarı**.

<figure class="fig">
<svg viewBox="0 0 420 176" width="420"><line class="grid" x1="40" y1="20" x2="40" y2="160"/><line class="grid" x1="40" y1="20" x2="180" y2="20"/><line class="grid" x1="110" y1="20" x2="110" y2="160"/><line class="grid" x1="40" y1="90" x2="180" y2="90"/><line class="grid" x1="180" y1="20" x2="180" y2="160"/><line class="grid" x1="40" y1="160" x2="180" y2="160"/><rect class="curve3" x="40" y="20" width="140" height="140"/><polygon class="dot" opacity="0.35" points="40,90 110,20 180,90 110,160"/><polygon class="curve" points="40,90 110,20 180,90 110,160"/><polygon class="dot2" opacity="0.35" points="40,90 40,20 110,20"/><polygon class="dot2" opacity="0.35" points="110,20 180,20 180,90"/><polygon class="dot2" opacity="0.35" points="180,90 180,160 110,160"/><polygon class="dot2" opacity="0.35" points="110,160 40,160 40,90"/><text class="ink" x="91.0" y="73.0" font-size="15" text-anchor="middle">√2</text><rect class="curve3" x="204" y="42" width="14" height="14"/><text class="ink" x="226" y="54" font-size="12" text-anchor="start">alan 4, kenar 2</text><rect class="dot" opacity="0.35" x="204" y="72" width="14" height="14"/><text class="ink" x="226" y="84" font-size="12" text-anchor="start">alan 2, kenar √2</text><rect class="dot2" opacity="0.35" x="204" y="102" width="14" height="14"/><text class="ink" x="226" y="114" font-size="12" text-anchor="start">4 × köşe üçgeni = 2</text><text class="dim" x="226" y="144" font-size="11" text-anchor="start">büyük karenin yarısı</text></svg>
  <figcaption>$2 \times 2$'lik karenin alanı $4$. Kenarların orta noktalarını birleştiren eğik kare, büyük karenin tam yarısı: dört turuncu köşe üçgeni birleşince bir tane daha eğik kare ediyor. Eğik karenin alanı $2$, yani kenarı $\sqrt{2}$.</figcaption>
</figure>

### Tam kareler

| $n$ | $n^2$ | $n$ | $n^2$ | $n$ | $n^2$ |
|---|---|---|---|---|---|
| $1$ | $1$ | $6$ | $36$ | $11$ | $121$ |
| $2$ | $4$ | $7$ | $49$ | $12$ | $144$ |
| $3$ | $9$ | $8$ | $64$ | $13$ | $169$ |
| $4$ | $16$ | $9$ | $81$ | $14$ | $196$ |
| $5$ | $25$ | $10$ | $100$ | $15$ | $225$ |

Bu tabloyu bilmek, köklerle hızlı çalışmanın yarısı.

## Tam çıkmayan kökler

$\sqrt{2}$ hangi sayı? $1^2 = 1 < 2 < 4 = 2^2$, yani $1$ ile $2$ arasında.
$1{,}4^2 = 1{,}96$ ve $1{,}5^2 = 2{,}25$: $1{,}4$ ile $1{,}5$ arasında.
Daraltmaya devam edersek $\sqrt{2} = 1{,}414\,21\dots$

$\sqrt{2}$'nin ondalık yazılışı ne biter ne de devreder; hiçbir kesre eşit
değildir. Böyle sayılara **irrasyonel** denir. Tam kare olmayan her doğal
sayının karekökü irrasyoneldir.

<figure class="fig">
<svg viewBox="0 0 460 140" width="460"><line class="line" x1="20" y1="88" x2="440" y2="88"/><line class="line" x1="30" y1="80" x2="30" y2="96"/><text class="ink" x="30" y="112" font-size="13" text-anchor="middle">0</text><text class="dim" x="30" y="128" font-size="11" text-anchor="middle">√0</text><line class="line" x1="110" y1="80" x2="110" y2="96"/><text class="ink" x="110" y="112" font-size="13" text-anchor="middle">1</text><text class="dim" x="110" y="128" font-size="11" text-anchor="middle">√1</text><line class="line" x1="190" y1="80" x2="190" y2="96"/><text class="ink" x="190" y="112" font-size="13" text-anchor="middle">2</text><text class="dim" x="190" y="128" font-size="11" text-anchor="middle">√4</text><line class="line" x1="270" y1="80" x2="270" y2="96"/><text class="ink" x="270" y="112" font-size="13" text-anchor="middle">3</text><text class="dim" x="270" y="128" font-size="11" text-anchor="middle">√9</text><line class="line" x1="350" y1="80" x2="350" y2="96"/><text class="ink" x="350" y="112" font-size="13" text-anchor="middle">4</text><text class="dim" x="350" y="128" font-size="11" text-anchor="middle">√16</text><line class="line" x1="430" y1="80" x2="430" y2="96"/><text class="ink" x="430" y="112" font-size="13" text-anchor="middle">5</text><text class="dim" x="430" y="128" font-size="11" text-anchor="middle">√25</text><line class="curve3" x1="143.1" y1="82" x2="143.1" y2="74"/><circle class="dot" cx="143.1" cy="88" r="5"/><text class="ink" x="143.1" y="54" font-size="13" text-anchor="middle">√2</text><text class="dim" x="143.1" y="68" font-size="10" text-anchor="middle">≈ 1,414</text><line class="curve3" x1="168.6" y1="82" x2="168.6" y2="48"/><circle class="dot" cx="168.6" cy="88" r="5"/><text class="ink" x="168.6" y="28" font-size="13" text-anchor="middle">√3</text><text class="dim" x="168.6" y="42" font-size="10" text-anchor="middle">≈ 1,732</text><line class="curve3" x1="208.9" y1="82" x2="208.9" y2="74"/><circle class="dot" cx="208.9" cy="88" r="5"/><text class="ink" x="208.9" y="54" font-size="13" text-anchor="middle">√5</text><text class="dim" x="208.9" y="68" font-size="10" text-anchor="middle">≈ 2,236</text><line class="curve3" x1="283.0" y1="82" x2="283.0" y2="48"/><circle class="dot" cx="283.0" cy="88" r="5"/><text class="ink" x="283.0" y="28" font-size="13" text-anchor="middle">√10</text><text class="dim" x="283.0" y="42" font-size="10" text-anchor="middle">≈ 3,162</text><line class="curve3" x1="387.8" y1="82" x2="387.8" y2="74"/><circle class="dot" cx="387.8" cy="88" r="5"/><text class="ink" x="387.8" y="54" font-size="13" text-anchor="middle">√20</text><text class="dim" x="387.8" y="68" font-size="10" text-anchor="middle">≈ 4,472</text></svg>
  <figcaption>Tam karelerin kökleri tam sayılara denk geliyor ($\sqrt{4} = 2$, $\sqrt{9} = 3$). Aradaki köklerin yeri tam kareler arasında: $\sqrt{10}$, $\sqrt{9} = 3$'ün hemen sağında; $\sqrt{20}$ ise $\sqrt{16} = 4$ ile $\sqrt{25} = 5$ arasında, $4$'e daha yakın.</figcaption>
</figure>

**Tahmin:** $\sqrt{200}$ kaç? $14^2 = 196$ ve $15^2 = 225$; $200$, $196$'ya
çok yakın, yani $\sqrt{200}$, $14$'ün biraz üstünde: $14{,}14\dots$

## Kök kuralları

Kökler çarpmaya ve bölmeye dağılır:

$$
\sqrt{a \cdot b} = \sqrt{a} \cdot \sqrt{b}, \qquad \sqrt{\frac{a}{b}} = \frac{\sqrt{a}}{\sqrt{b}} \qquad (a, b \ge 0,\; b \neq 0)
$$

$$
\sqrt{4 \cdot 9} = \sqrt{36} = 6 = 2 \cdot 3 = \sqrt{4} \cdot \sqrt{9}
$$

Ama **toplamaya dağılmaz**:

$$
\sqrt{9 + 16} = \sqrt{25} = 5, \qquad \sqrt{9} + \sqrt{16} = 3 + 4 = 7
$$

Bu, $(a + b)^2 \neq a^2 + b^2$ hatasının öbür yüzü.

**Kök ve kare birbirini götürür:** $(\sqrt{a})^2 = a$ ($a \ge 0$). Ters
sırada dikkat: $\sqrt{x^2} = |x|$. Örneğin $\sqrt{(-5)^2} = \sqrt{25} = 5$,
$-5$ değil.

## Kökleri sadeleştirmek

Kökün içindeki sayıyı **en büyük tam kare çarpanla** ayır, tam kareyi
dışarı çıkar:

$$
\sqrt{50} = \sqrt{25 \cdot 2} = \sqrt{25} \cdot \sqrt{2} = 5\sqrt{2}
$$

$$
\sqrt{72} = \sqrt{36 \cdot 2} = 6\sqrt{2}, \qquad \sqrt{48} = \sqrt{16 \cdot 3} = 4\sqrt{3}
$$

Asal çarpanlardan da gidebilirsin: $72 = 2^3 \cdot 3^2 = (2 \cdot 3)^2 \cdot
2$; her çift bir çarpan olarak dışarı çıkar.

**Toplama ve çıkarma:** Yalnızca **aynı kökler** birleşir; tıpkı $5x + 3x
= 8x$ gibi.

$$
5\sqrt{2} + 3\sqrt{2} = 8\sqrt{2}, \qquad \sqrt{2} + \sqrt{3} \text{ birleşmez}
$$

Önce sadeleştirmek gizli benzerlikleri ortaya çıkarır:
$\sqrt{50} + \sqrt{8} = 5\sqrt{2} + 2\sqrt{2} = 7\sqrt{2}$.

**Çarpma:** Katsayılar katsayılarla, kökler köklerle çarpılır:

$$
2\sqrt{3} \cdot 4\sqrt{3} = (2 \cdot 4) \cdot (\sqrt{3} \cdot \sqrt{3}) = 8 \cdot 3 = 24
$$

## Paydayı kökten kurtarmak

$\dfrac{6}{\sqrt{3}}$ gibi bir sayıda paydada kök kalmasın isteriz. Payı
ve paydayı $\sqrt{3}$ ile çarp (değer değişmez, $\frac{\sqrt{3}}{\sqrt{3}}
= 1$):

$$
\frac{6}{\sqrt{3}} = \frac{6 \cdot \sqrt{3}}{\sqrt{3} \cdot \sqrt{3}} = \frac{6\sqrt{3}}{3} = 2\sqrt{3}
$$

Sonuç aynı sayı ama karşılaştırması ve toplaması daha kolay.

## Başka kökler ve kesirli üsler

**Küpkök:** $\sqrt[3]{a}$, küpü $a$ olan sayı. $\sqrt[3]{8} = 2$,
$\sqrt[3]{125} = 5$. Tek dereceli köklerde negatif sayıların da kökü var:
$\sqrt[3]{-27} = -3$, çünkü $(-3)^3 = -27$.

Genel olarak $\sqrt[n]{a}$, $n$'inci kuvveti $a$ olan sayı: $\sqrt[4]{16} =
2$, $\sqrt[5]{32} = 2$.

**Kesirli üs:** Üs kurallarının bozulmaması için $a^{1/2}$ ne olmalı?
$(a^{1/2})^2 = a^{1/2 \cdot 2} = a^1 = a$. Karesi $a$ olan sayı: $\sqrt{a}$.

$$
a^{1/n} = \sqrt[n]{a}, \qquad a^{m/n} = \left(\sqrt[n]{a}\right)^m
$$

$$
8^{2/3} = \left(\sqrt[3]{8}\right)^2 = 2^2 = 4, \qquad 16^{-1/2} = \frac{1}{\sqrt{16}} = \frac{1}{4}
$$

Kesirli üste payda kökün derecesini, pay kuvveti söyler. Önce kökü almak
sayıları küçük tutar.

## Makine öğrenmesinde kökler

**Uzunluk ve uzaklık.** $(3, 4)$ vektörünün uzunluğu $\sqrt{3^2 + 4^2} =
\sqrt{25} = 5$. İki nokta arasındaki uzaklık, en yakın komşu gibi
yöntemlerin temeli.

**RMSE.** Hataların karelerinin ortalamasının karekökü: hataları kare
alarak işaretten kurtarır, sonra kök alarak birimi geri getirir. Hatalar
$3, -1, 2, -2$ ise

$$
\sqrt{\frac{9 + 1 + 4 + 4}{4}} = \sqrt{4{,}5} \approx 2{,}12
$$

**Ölçekleme.** Dikkat mekanizmasında skorlar $\sqrt{d}$'ye bölünür; $d =
64$ ise $\sqrt{64} = 8$'e.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\sqrt{9 + 16} = 3 + 4$</p>
      <p>$\sqrt{49} = \pm 7$</p>
      <p>$\sqrt{2} + \sqrt{3} = \sqrt{5}$</p>
      <p>$\sqrt{(-5)^2} = -5$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$\sqrt{25} = 5$</p>
      <p>$\sqrt{49} = 7$; ama $x^2 = 49 \Rightarrow x = \pm 7$</p>
      <p>Birleşmez: $\sqrt{2} + \sqrt{3} \approx 3{,}15$, $\sqrt{5} \approx 2{,}24$</p>
      <p>$\sqrt{(-5)^2} = \lvert -5 \rvert = 5$</p>
    </div>
  </div>
  <figcaption>Kök çarpmaya ve bölmeye dağılır, toplamaya dağılmaz; $\sqrt{\;}$ işareti her zaman negatif olmayan kökü gösterir.</figcaption>
</figure>

- **Kökü toplamaya dağıtmak.** $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$.
- **$\sqrt{\;}$ işaretine iki değer vermek.** $\sqrt{49}$ yalnızca $7$;
  $\pm$ işareti denklem çözerken çıkar.
- **Sadeleştirmeyi yarım bırakmak.** $\sqrt{72} = 2\sqrt{18}$ doğru ama
  bitmedi; en büyük tam kare çarpanı ($36$) kullan: $6\sqrt{2}$.

## Özet

- $\sqrt{a}$: karesi $a$ olan negatif olmayan sayı ($a \ge 0$). $x^2 = a$ ise $x = \pm\sqrt{a}$.
- Geometride alanı $a$ olan karenin kenarı. Tam kare olmayan sayıların kökleri irrasyonel.
- $\sqrt{ab} = \sqrt{a}\sqrt{b}$, $\sqrt{a/b} = \sqrt{a}/\sqrt{b}$; ama $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$.
- $(\sqrt{a})^2 = a$, $\sqrt{x^2} = |x|$.
- Sadeleştirme: en büyük tam kare çarpanı dışarı çıkar. Yalnızca aynı kökler toplanır.
- Paydadaki kökü, pay ve paydayı o kökle çarparak yok et.
- $a^{1/n} = \sqrt[n]{a}$, $a^{m/n} = (\sqrt[n]{a})^m$.
- RMSE, standart sapma, vektör uzunluğu: hepsi bir karekök.
