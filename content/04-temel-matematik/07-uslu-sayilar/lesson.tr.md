# Üslü Sayılar

Çarpma tekrarlı toplamaydı. **Üs** de tekrarlı çarpma: $2 \cdot 2 \cdot 2
\cdot 2 \cdot 2$ yerine kısaca $2^5$ yazıyoruz. Üsler çok büyük ve çok
küçük sayıları yazmanın, "her adımda iki katına çıkan" büyümeyi
anlatmanın dili. Bir dil modelinin $10^{11}$ parametresi, bir öğrenme
hızının $10^{-3}$ olması, bir bilgisayar baytının $2^8 = 256$ değer
alabilmesi hep üslerle anlatılıyor.

Ön bilgi: Tam Sayılar ve Kesirler bölümleri.

## Üs nedir?

$n$ pozitif bir tam sayıysa

$$
a^n = \underbrace{a \cdot a \cdot \ldots \cdot a}_{n \text{ tane}}
$$

$a$'ya **taban**, $n$'ye **üs** denir; $a^n$ "$a$'nın $n$'inci kuvveti"
diye okunur. $a^2$ "$a$'nın karesi", $a^3$ "$a$'nın küpü".

$$
2^5 = 32, \qquad 10^3 = 1\,000, \qquad \left(\frac{2}{3}\right)^2 = \frac{4}{9}, \qquad (-3)^3 = -27
$$

### Üslü büyüme çok hızlıdır

<figure class="fig">
<svg viewBox="0 0 440 228" width="440"><rect class="dot" opacity="0.5" x="40" y="198.8" width="34" height="1.2" rx="3"/><text class="ink" x="57.0" y="192.8" font-size="11" text-anchor="middle">1</text><text class="dim" x="57.0" y="216" font-size="11" text-anchor="middle">0</text><circle class="dot2" cx="57.0" cy="200.0" r="4"/><rect class="dot" opacity="0.5" x="88" y="197.5" width="34" height="2.5" rx="3"/><text class="ink" x="105.0" y="191.5" font-size="11" text-anchor="middle">2</text><text class="dim" x="105.0" y="216" font-size="11" text-anchor="middle">1</text><circle class="dot2" cx="105.0" cy="197.5" r="4"/><rect class="dot" opacity="0.5" x="136" y="195.0" width="34" height="5.0" rx="3"/><text class="ink" x="153.0" y="189.0" font-size="11" text-anchor="middle">4</text><text class="dim" x="153.0" y="216" font-size="11" text-anchor="middle">2</text><circle class="dot2" cx="153.0" cy="195.0" r="4"/><rect class="dot" opacity="0.5" x="184" y="190.0" width="34" height="10.0" rx="3"/><text class="ink" x="201.0" y="184.0" font-size="11" text-anchor="middle">8</text><text class="dim" x="201.0" y="216" font-size="11" text-anchor="middle">3</text><circle class="dot2" cx="201.0" cy="192.5" r="4"/><rect class="dot" opacity="0.5" x="232" y="180.0" width="34" height="20.0" rx="3"/><text class="ink" x="249.0" y="174.0" font-size="11" text-anchor="middle">16</text><text class="dim" x="249.0" y="216" font-size="11" text-anchor="middle">4</text><circle class="dot2" cx="249.0" cy="190.0" r="4"/><rect class="dot" opacity="0.5" x="280" y="160.0" width="34" height="40.0" rx="3"/><text class="ink" x="297.0" y="154.0" font-size="11" text-anchor="middle">32</text><text class="dim" x="297.0" y="216" font-size="11" text-anchor="middle">5</text><circle class="dot2" cx="297.0" cy="187.5" r="4"/><rect class="dot" opacity="0.5" x="328" y="120.0" width="34" height="80.0" rx="3"/><text class="ink" x="345.0" y="114.0" font-size="11" text-anchor="middle">64</text><text class="dim" x="345.0" y="216" font-size="11" text-anchor="middle">6</text><circle class="dot2" cx="345.0" cy="185.0" r="4"/><rect class="dot" opacity="0.5" x="376" y="40.0" width="34" height="160.0" rx="3"/><text class="ink" x="393.0" y="34.0" font-size="11" text-anchor="middle">128</text><text class="dim" x="393.0" y="216" font-size="11" text-anchor="middle">7</text><circle class="dot2" cx="393.0" cy="182.5" r="4"/><polyline class="curve2" fill="none" points="57.0,200.0 105.0,197.5 153.0,195.0 201.0,192.5 249.0,190.0 297.0,187.5 345.0,185.0 393.0,182.5"/><line class="line" x1="32" y1="200" x2="424" y2="200"/><text class="dim" x="428" y="216" font-size="11" text-anchor="start">n</text><rect class="dot" opacity="0.5" x="40" y="14" width="12" height="12" rx="2"/><text class="ink" x="58" y="24" font-size="12" text-anchor="start">2ⁿ: her adımda iki katı</text><circle class="dot2" cx="46" cy="42" r="4"/><text class="ink" x="58" y="46" font-size="12" text-anchor="start">2n: her adımda 2 fazlası</text></svg>
  <figcaption>Mor çubuklar $2^n$: her adımda iki katına çıkıyor. Turuncu çizgi $2n$: her adımda $2$ artıyor. $n = 7$'de biri $128$, öbürü $14$. Başta farkı yok gibi, ama iki katına çıkmak kısa sürede her toplamayı geride bırakıyor.</figcaption>
</figure>

$2^{10} = 1\,024 \approx 10^3$. Bu yüzden bilgisayarda $1$ kilobayt kabaca
$1\,000$ bayt. $2^{20} \approx 10^6$, $2^{30} \approx 10^9$.

## Üs kuralları

Kuralları ezberlemek yerine her birini açarak görebilirsin; hepsi
tanımdan çıkıyor.

**Aynı tabanlı çarpma: üsler toplanır.**

$$
a^m \cdot a^n = a^{m + n} \qquad 2^3 \cdot 2^4 = (2 \cdot 2 \cdot 2)(2 \cdot 2 \cdot 2 \cdot 2) = 2^7
$$

**Aynı tabanlı bölme: üsler çıkarılır.**

$$
\frac{a^m}{a^n} = a^{m - n} \qquad \frac{2^5}{2^2} = \frac{2 \cdot 2 \cdot 2 \cdot \cancel{2} \cdot \cancel{2}}{\cancel{2} \cdot \cancel{2}} = 2^3
$$

**Kuvvetin kuvveti: üsler çarpılır.**

$$
(a^m)^n = a^{m \cdot n} \qquad (2^3)^2 = 2^3 \cdot 2^3 = 2^6
$$

**Çarpımın ve bölümün kuvveti: her çarpana dağılır.**

$$
(ab)^n = a^n b^n, \qquad \left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}
$$

$(2 \cdot 5)^3 = 2^3 \cdot 5^3 = 8 \cdot 125 = 1\,000$; gerçekten de $10^3$.

**Toplamın kuvveti dağılmaz!** $(a + b)^2 \neq a^2 + b^2$. Örneğin
$(1 + 2)^2 = 9$ ama $1^2 + 2^2 = 5$. Kural yalnızca çarpma ve bölme için.

## Sıfır ve negatif üsler

Üs yalnızca "kaç kez çarptık" olsaydı $2^0$ ya da $2^{-1}$ anlamsız
olurdu. Ama kuralların bozulmaması için bu üslerin değeri **kendiliğinden**
belirleniyor.

<figure class="fig">
<svg viewBox="0 0 542 126" width="542"><rect class="box" x="14" y="30" width="58" height="58" rx="6"/><text class="ink" x="43.0" y="54" font-size="16" text-anchor="middle">2³</text><text class="ink" x="43.0" y="76" font-size="14" text-anchor="middle">8</text><text class="dim" x="87.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="87.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="102" y="30" width="58" height="58" rx="6"/><text class="ink" x="131.0" y="54" font-size="16" text-anchor="middle">2²</text><text class="ink" x="131.0" y="76" font-size="14" text-anchor="middle">4</text><text class="dim" x="175.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="175.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="190" y="30" width="58" height="58" rx="6"/><text class="ink" x="219.0" y="54" font-size="16" text-anchor="middle">2¹</text><text class="ink" x="219.0" y="76" font-size="14" text-anchor="middle">2</text><text class="dim" x="263.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="263.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="278" y="30" width="58" height="58" rx="6"/><rect class="curve" x="278" y="30" width="58" height="58" rx="6"/><text class="ink" x="307.0" y="54" font-size="16" text-anchor="middle">2⁰</text><text class="ink" x="307.0" y="76" font-size="14" text-anchor="middle">1</text><text class="dim" x="351.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="351.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="366" y="30" width="58" height="58" rx="6"/><text class="ink" x="395.0" y="54" font-size="16" text-anchor="middle">2⁻¹</text><text class="ink" x="395.0" y="76" font-size="14" text-anchor="middle">1/2</text><text class="dim" x="439.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="439.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="454" y="30" width="58" height="58" rx="6"/><text class="ink" x="483.0" y="54" font-size="16" text-anchor="middle">2⁻²</text><text class="ink" x="483.0" y="76" font-size="14" text-anchor="middle">1/4</text><text class="ink" x="263.0" y="114" font-size="12" text-anchor="middle">üs 1 azalınca değer yarıya iner</text></svg>
  <figcaption>Üs her $1$ azaldığında değer yarıya iniyor. Bu örüntüyü sürdürünce $2^0 = 1$, $2^{-1} = \tfrac{1}{2}$, $2^{-2} = \tfrac{1}{4}$ çıkıyor. Tanımlar keyfi değil; örüntünün devamı.</figcaption>
</figure>

**Sıfırıncı kuvvet.** Bölme kuralından: $\dfrac{a^n}{a^n} = a^{n - n} =
a^0$. Ama bir sayının kendine bölümü $1$. Demek ki

$$
a^0 = 1 \qquad (a \neq 0)
$$

**Negatif üs.** Yine bölme kuralından: $\dfrac{a^0}{a^n} = a^{0 - n} =
a^{-n}$, ve bu $\dfrac{1}{a^n}$:

$$
a^{-n} = \frac{1}{a^n} \qquad 2^{-3} = \frac{1}{8}, \qquad 10^{-2} = \frac{1}{100} = 0{,}01
$$

**Negatif üs sayıyı negatif yapmaz;** tersini alır. $2^{-3}$ pozitif bir
sayı: $\tfrac{1}{8}$.

Kesirlerde negatif üs kesri ters çevirir:

$$
\left(\frac{2}{3}\right)^{-2} = \left(\frac{3}{2}\right)^2 = \frac{9}{4}
$$

Bütün kurallar sıfır ve negatif üslerde de geçerli:

$$
\frac{2^3 \cdot 2^5}{2^{10}} = \frac{2^8}{2^{10}} = 2^{-2} = \frac{1}{4}
$$

## Farklı tabanları eşitlemek

Tabanlar farklıysa kurallar doğrudan uygulanamaz: $2^3 \cdot 3^2$
birleşmez. Ama tabanlar aynı sayının kuvvetleriyse, önce aynı tabana
çevir:

$$
\frac{4^3 \cdot 8^2}{2^{10}} = \frac{(2^2)^3 \cdot (2^3)^2}{2^{10}} = \frac{2^6 \cdot 2^6}{2^{10}} = 2^{2} = 4
$$

**Basit üslü denklemler** de böyle çözülür: $2^x = 32$ ise $32 = 2^5$
yazıp $x = 5$. Tabanlar aynıysa üsler eşit olmalı.

## Negatif taban ve parantez

Tam Sayılar bölümünden hatırla: parantez tabanı belirler.

$$
(-2)^4 = 16, \qquad -2^4 = -16, \qquad (-2)^3 = -8
$$

Negatif tabanın çift kuvveti pozitif, tek kuvveti negatif.

## Bilimsel gösterim

Çok büyük ve çok küçük sayılar $a \times 10^n$ biçiminde yazılır; burada
$1 \le a < 10$ ve $n$ bir tam sayı.

| Sayı | Bilimsel gösterim |
|---|---|
| $300\,000$ | $3 \times 10^5$ |
| $175\,000\,000\,000$ | $1{,}75 \times 10^{11}$ |
| $0{,}004$ | $4 \times 10^{-3}$ |
| $0{,}000\,025$ | $2{,}5 \times 10^{-5}$ |

$n$, virgülün kaç basamak kaydığını söyler: pozitifse sayı büyük, negatifse
$1$'den küçük.

**Bilimsel gösterimde çarpma ve bölme:** Katsayıları ayrı, $10$'un
kuvvetlerini ayrı işle.

$$
(3 \times 10^4)(2 \times 10^{-7}) = (3 \cdot 2) \times 10^{4 + (-7)} = 6 \times 10^{-3}
$$

Katsayı $10$'u geçerse düzelt: $(5 \times 10^3)(4 \times 10^2) = 20 \times
10^5 = 2 \times 10^6$.

**Bilgisayarda** $6 \times 10^{-3}$ genelde `6e-3` diye yazılır; Python'da
`0.006 == 6e-3` doğrudur.

## Makine öğrenmesinde üsler

**Öğrenme hızı** gibi küçük değerler çoğunlukla $10$'un negatif
kuvvetleriyle seçilir: $10^{-2}$, $10^{-3}$, $10^{-4}$. Bunları denerken
her adımda değer $10$ kat küçülür.

**Model büyüklüğü** bilimsel gösterimle anlatılır: $1{,}75 \times 10^{11}$
parametre, yani $175$ milyar.

**İkilik sistem.** $8$ bit $2^8 = 256$ farklı değer tutabilir; bir resmin
her pikseli çoğu zaman $0$ ile $255$ arasında bir sayıdır.

**Deneme sayısı.** $5$ ayarın her biri için $3$ değer deneyip bütün
birleşimleri eğitmek $3^5 = 243$ model eğitmek demek. Ayar sayısı $10$'a
çıkınca $3^{10} = 59\,049$ olur; bu yüzden her birleşimi denemek çoğu
zaman mümkün değil.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$2^3 \cdot 2^4 = 4^7$</p>
      <p>$(2^3)^2 = 2^9$</p>
      <p>$2^{-3} = -8$</p>
      <p>$(a + b)^2 = a^2 + b^2$</p>
      <p>$3^0 = 0$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$2^3 \cdot 2^4 = 2^7$ (taban aynı kalır)</p>
      <p>$(2^3)^2 = 2^6$ (üsler çarpılır)</p>
      <p>$2^{-3} = \dfrac{1}{8}$</p>
      <p>$(1 + 2)^2 = 9 \neq 5$</p>
      <p>$3^0 = 1$</p>
    </div>
  </div>
  <figcaption>Çarpmada üsler toplanır, taban değişmez; kuvvetin kuvvetinde üsler çarpılır.</figcaption>
</figure>

- **Tabanları çarpmak.** $2^3 \cdot 2^4$'te taban $2$ kalır; tabanlar
  çarpılmaz.
- **Toplamada üs kuralı uygulamak.** $2^3 + 2^4 \neq 2^7$: $8 + 16 = 24$.
  Kurallar yalnızca çarpma ve bölme için. (Ama $2^3 + 2^3 = 2 \cdot 2^3 =
  2^4$, çünkü aynı şeyi iki kez topluyoruz.)
- **Negatif üssü negatif sayı sanmak.** Negatif üs tersini alır.

## Özet

- $a^n$: $a$'yı $n$ kez çarp. Taban $a$, üs $n$.
- $a^m a^n = a^{m+n}$, $\dfrac{a^m}{a^n} = a^{m-n}$, $(a^m)^n = a^{mn}$, $(ab)^n = a^n b^n$.
- $a^0 = 1$, $a^{-n} = \dfrac{1}{a^n}$ ($a \neq 0$); negatif üs tersini alır, işareti değiştirmez.
- Toplamın kuvveti dağılmaz: $(a + b)^2 \neq a^2 + b^2$.
- Farklı tabanları mümkünse aynı tabana çevir: $4 = 2^2$, $8 = 2^3$.
- Bilimsel gösterim: $a \times 10^n$, $1 \le a < 10$; katsayıları ve $10$'un kuvvetlerini ayrı işle.
- $2^{10} \approx 10^3$; üslü büyüme her doğrusal büyümeyi kısa sürede geçer.
