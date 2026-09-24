# Cebirsel İfadeler ve Özdeşlikler

Şimdiye kadar hep belli sayılarla hesap yaptık. Cebir, sayının yerine
bir **harf** koyup "hangi sayı olursa olsun" doğru olan kuralları yazmayı
sağlıyor. Bir makine öğrenmesi modeli de böyle yazılır: $\hat{y} = wx +
b$ ifadesinde $x$ her örnekte değişen girdi, $w$ ve $b$ modelin öğrendiği
sayılar. Bu bölümde cebirsel ifadeleri okumayı, sadeleştirmeyi,
çarpmayı ve her zaman doğru olan eşitlikleri, yani **özdeşlikleri**
göreceğiz.

Ön bilgi: Matematiği Okumak, Tam Sayılar ve Üslü Sayılar bölümleri.

## İfadenin parçaları

$$
3x^2 - 5x + 7
$$

| Parça | Bu ifadede |
|---|---|
| **Değişken** | $x$: değeri değişebilen harf |
| **Terim** | $3x^2$, $-5x$, $7$: $+$ ve $-$ ile ayrılan parçalar |
| **Katsayı** | $3$ ve $-5$: harfin önündeki sayı (işaretiyle) |
| **Sabit terim** | $7$: harfsiz terim |
| **Derece** | $2$: en büyük üs |

Terimin işareti kendisine ait: $-5x$ teriminin katsayısı $5$ değil $-5$.
Harfin önünde sayı yoksa katsayı $1$: $x = 1 \cdot x$, $-x = -1 \cdot x$.

## Değer hesaplamak

Bir ifadenin değerini bulmak için harfin yerine sayıyı **parantez içinde**
koy. $x = -2$ için

$$
3x^2 - 5x + 7 = 3(-2)^2 - 5(-2) + 7 = 12 + 10 + 7 = 29
$$

Parantezsiz yazmak ($3 \cdot -2^2$) hem işareti hem üssü karıştırır.

## Benzer terimler

Harfleri ve üsleri **tamamen aynı** olan terimlere **benzer terim** denir.
Yalnızca benzer terimler toplanır; katsayıları toplanır, harf kısmı
aynen kalır:

$$
3x + 5y - x + 2y = (3 - 1)x + (5 + 2)y = 2x + 7y
$$

Neden? $3x - x$ "üç tane $x$'ten bir tane $x$ çıkar" demek: dağılma
özelliği tersten, $3x - 1x = (3 - 1)x$.

- $2x$ ile $2x^2$ benzer değil (üsler farklı).
- $xy$ ile $yx$ benzer (çarpmada sıra önemsiz).
- $3x + 2y$ daha fazla sadeleşmez; $5xy$ **değildir**.

## Dağılma: parantezi açmak

Parantezin önündeki çarpan içerideki **her** terimle çarpılır:

$$
3(2x - 5) = 6x - 15
$$

**Eksi işareti de bir çarpan:** $-(x - 4) = -1 \cdot (x - 4) = -x + 4$.
İçerideki her terimin işareti değişir.

$$
\begin{aligned}
3(2x - 5) - 2(x - 4) &= 6x - 15 - 2x + 8 \\
&= 4x - 7
\end{aligned}
$$

## Çarpma

**Tek terimliler:** katsayılar çarpılır, aynı harflerin üsleri toplanır.

$$
(3x^2)(4x^3) = 12x^5, \qquad (-2ab)(5a) = -10a^2 b
$$

**İki terimli çarpı iki terimli:** her terim öbürünün her terimiyle
çarpılır; dört çarpım çıkar.

<figure class="fig">
<svg viewBox="0 0 440 250" width="440"><rect class="dot" opacity="0.35" x="120" y="34" width="120" height="120"/><rect class="curve3" x="120" y="34" width="120" height="120"/><text class="ink" x="180.0" y="99.0" font-size="16" text-anchor="middle">x²</text><rect class="dot2" opacity="0.35" x="240" y="34" width="78" height="120"/><rect class="curve3" x="240" y="34" width="78" height="120"/><text class="ink" x="279.0" y="99.0" font-size="14" text-anchor="middle">3x</text><rect class="dot2" opacity="0.35" x="120" y="154" width="120" height="52"/><rect class="curve3" x="120" y="154" width="120" height="52"/><text class="ink" x="180.0" y="185.0" font-size="14" text-anchor="middle">2x</text><rect class="dot3" opacity="0.35" x="240" y="154" width="78" height="52"/><rect class="curve3" x="240" y="154" width="78" height="52"/><text class="ink" x="279.0" y="185.0" font-size="14" text-anchor="middle">6</text><text class="ink" x="180.0" y="24" font-size="14" text-anchor="middle">x</text><text class="ink" x="279.0" y="24" font-size="14" text-anchor="middle">3</text><text class="ink" x="108" y="99.0" font-size="14" text-anchor="middle">x</text><text class="ink" x="108" y="185" font-size="14" text-anchor="middle">2</text><text class="ink" x="220" y="236" font-size="13" text-anchor="middle">(x + 3)(x + 2) = x² + 3x + 2x + 6 = x² + 5x + 6</text></svg>
  <figcaption>Kenarları $x + 3$ ve $x + 2$ olan dikdörtgenin alanı dört parçanın toplamı: bir $x^2$, iki tane $x$ çarpı sayı ($3x$ ve $2x$) ve bir sabit ($6$). Çarpmada hiçbir parça atlanmıyor.</figcaption>
</figure>

$$
(x + 3)(x + 2) = x \cdot x + x \cdot 2 + 3 \cdot x + 3 \cdot 2 = x^2 + 5x + 6
$$

İşaretlere dikkat:

$$
(2x + 3)(x - 4) = 2x^2 - 8x + 3x - 12 = 2x^2 - 5x - 12
$$

## Özdeşlikler

Bazı çarpımlar o kadar sık çıkar ki sonuçları ezberlemeye değer:

| Özdeşlik | Örnek |
|---|---|
| $(a + b)^2 = a^2 + 2ab + b^2$ | $(x + 5)^2 = x^2 + 10x + 25$ |
| $(a - b)^2 = a^2 - 2ab + b^2$ | $(2x - 3)^2 = 4x^2 - 12x + 9$ |
| $(a + b)(a - b) = a^2 - b^2$ | $(x + 4)(x - 4) = x^2 - 16$ |

<figure class="fig">
<svg viewBox="0 0 490 278" width="490"><rect class="dot" opacity="0.35" x="150" y="30" width="130" height="130"/><rect class="curve3" x="150" y="30" width="130" height="130"/><text class="ink" x="215.0" y="100.0" font-size="16" text-anchor="middle">a²</text><rect class="dot2" opacity="0.35" x="280" y="30" width="60" height="130"/><rect class="curve3" x="280" y="30" width="60" height="130"/><text class="ink" x="310.0" y="100.0" font-size="14" text-anchor="middle">ab</text><rect class="dot2" opacity="0.35" x="150" y="160" width="130" height="60"/><rect class="curve3" x="150" y="160" width="130" height="60"/><text class="ink" x="215.0" y="195.0" font-size="14" text-anchor="middle">ab</text><rect class="dot3" opacity="0.35" x="280" y="160" width="60" height="60"/><rect class="curve3" x="280" y="160" width="60" height="60"/><text class="ink" x="310.0" y="195.0" font-size="14" text-anchor="middle">b²</text><text class="ink" x="215.0" y="20" font-size="14" text-anchor="middle">a</text><text class="ink" x="310.0" y="20" font-size="14" text-anchor="middle">b</text><text class="ink" x="138" y="100.0" font-size="14" text-anchor="middle">a</text><text class="ink" x="138" y="195.0" font-size="14" text-anchor="middle">b</text><text class="ink" x="245.0" y="248" font-size="13" text-anchor="middle">(a + b)² = a² + ab + ab + b² = a² + 2ab + b²</text><text class="dim" x="245.0" y="266" font-size="11" text-anchor="middle">iki tane ab dikdörtgeni unutulmamalı</text></svg>
  <figcaption>Kenarı $a + b$ olan karenin alanı dört parçadan oluşuyor: $a^2$, $b^2$ ve <b>iki tane</b> $ab$. $(a + b)^2 = a^2 + b^2$ yazmak iki dikdörtgeni unutmak demek.</figcaption>
</figure>

**Özdeşlik ile denklem farkı.** $(a + b)^2 = a^2 + 2ab + b^2$ **her** $a$
ve $b$ için doğru; buna özdeşlik denir. $2x + 1 = 7$ ise yalnızca $x = 3$
için doğru; bu bir denklem.

**Hızlı sınama:** Bir eşitliğin özdeşlik olup olmadığından emin değilsen
bir sayı koy. $(a + b)^2 = a^2 + b^2$ için $a = 1$, $b = 2$: sol $9$, sağ
$5$. Tek bir karşı örnek yeter: özdeşlik değil. (Ama birkaç sayıda tutması
özdeşlik olduğunu **kanıtlamaz**; kanıt için açıp sadeleştirmek gerekir.)

### Özdeşliklerle zihinden hesap

$$
\begin{aligned}
99^2 &= (100 - 1)^2 = 10\,000 - 200 + 1 = 9\,801 \\
51 \cdot 49 &= (50 + 1)(50 - 1) = 2\,500 - 1 = 2\,499
\end{aligned}
$$

## Makine öğrenmesinde cebirsel ifadeler

**Doğrusal model.** İki girdili bir model $\hat{y} = w_1 x_1 + w_2 x_2 +
b$. Girdiler $x_1 = 3$, $x_2 = -1$, ağırlıklar $w_1 = 2$, $w_2 = 5$, $b =
1$ ise $\hat{y} = 6 - 5 + 1 = 2$: ifadeye değer koymak.

**Kare hatayı açmak.** Tek bir örnek için hata $(y - wx)^2$. Özdeşlikle
açılınca

$$
(y - wx)^2 = y^2 - 2wxy + w^2 x^2
$$

ağırlık $w$'ye göre ikinci dereceden bir ifade çıkıyor. Modelin en iyi
$w$'yi nasıl bulduğunu anlamanın ilk adımı bu açılım.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$(a + b)^2 = a^2 + b^2$</p>
      <p>$-(x - 4) = -x - 4$</p>
      <p>$3x + 2y = 5xy$</p>
      <p>$x^2 + x^2 = x^4$</p>
      <p>$2x \cdot 3x = 6x$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$(a + b)^2 = a^2 + 2ab + b^2$</p>
      <p>$-(x - 4) = -x + 4$</p>
      <p>$3x + 2y$ sadeleşmez</p>
      <p>$x^2 + x^2 = 2x^2$</p>
      <p>$2x \cdot 3x = 6x^2$</p>
    </div>
  </div>
  <figcaption>Toplamada yalnızca benzer terimler birleşir ve üs değişmez; çarpmada üsler toplanır.</figcaption>
</figure>

- **Eksiyi yalnızca ilk terime dağıtmak.** $-(x - 4)$'te eksi her terime
  gider.
- **Toplamada üsleri toplamak.** $x^2 + x^2$ iki tane $x^2$: $2x^2$.
  Üsler yalnızca çarpmada toplanır.
- **Değer koyarken parantezi unutmak.** $x = -3$ için $x^2 = (-3)^2 = 9$.

## Özet

- İfade terimlerden oluşur; her terimin katsayısı (işaretiyle) ve harf kısmı var.
- Değer koyarken sayıyı parantez içinde yaz.
- Yalnızca benzer terimler (aynı harf, aynı üs) toplanır: katsayıları toplanır.
- Dağılma: $a(b + c) = ab + ac$; $-(b - c) = -b + c$.
- İki terimli çarpımda dört çarpım: $(a + b)(c + d) = ac + ad + bc + bd$.
- $(a \pm b)^2 = a^2 \pm 2ab + b^2$; $(a + b)(a - b) = a^2 - b^2$.
- Özdeşlik her değerde doğru; tek bir karşı örnek özdeşlik olmadığını gösterir.
