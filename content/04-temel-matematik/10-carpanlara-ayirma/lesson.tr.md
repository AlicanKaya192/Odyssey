# Çarpanlara Ayırma

Önceki bölümde çarpımları açtık: $(x + 2)(x + 3) = x^2 + 5x + 6$. Çarpanlara
ayırma bunun **tersi**: bir toplamı, çarpılınca onu veren çarpanlar olarak
yazmak. Neden isteriz? Çünkü çarpım biçimi çok daha fazla şey söylüyor:
bir ifadenin ne zaman sıfır olduğu, bir kesrin nasıl sadeleştiği ve bir
hesabın nasıl kısaltılabileceği hep çarpanlardan okunuyor. İkinci dereceden
denklemleri çözmenin en hızlı yolu da bu.

Ön bilgi: Cebirsel İfadeler ve Özdeşlikler, Bölünebilme (EBOB).

## Ortak çarpan parantezi

Her terimde ortak olan çarpanı dışarı al. Katsayılar için **EBOB**, harfler
için **en küçük üs**:

$$
6x^2 + 9x = 3x(2x + 3)
$$

$6$ ile $9$'un EBOB'u $3$; $x^2$ ile $x$'in ortağı $x$. Parantezin içi,
her terimin $3x$'e bölümü: $6x^2 \div 3x = 2x$, $9x \div 3x = 3$.

**Tamamını çıkar:** $6x^2 + 9x = 3(2x^2 + 3x)$ doğru ama bitmemiş;
parantezin içinde hâlâ ortak bir $x$ var.

**Sağlama her zaman kolay:** parantezi geri aç, başa dönmelisin.

### Gruplama

Dört terimde ortak çarpan tek seferde yoksa ikişer ikişer grupla:

$$
\begin{aligned}
ax + ay + bx + by &= a(x + y) + b(x + y) \\
&= (a + b)(x + y)
\end{aligned}
$$

İkinci satırda $(x + y)$ iki terimin **ortak çarpanı** oldu ve dışarı
alındı.

## Özdeşliklerden gelen kalıplar

Cebirsel İfadeler bölümündeki özdeşlikler tersten okununca çarpanlara ayırma
kalıbı oluyor:

| Kalıp | Çarpanlar | Örnek |
|---|---|---|
| $a^2 - b^2$ | $(a - b)(a + b)$ | $x^2 - 49 = (x - 7)(x + 7)$ |
| $a^2 + 2ab + b^2$ | $(a + b)^2$ | $x^2 + 10x + 25 = (x + 5)^2$ |
| $a^2 - 2ab + b^2$ | $(a - b)^2$ | $9x^2 - 12x + 4 = (3x - 2)^2$ |

**İki kare farkını tanı:** iki terim, ikisi de tam kare, aralarında eksi.
$4x^2 - 25 = (2x)^2 - 5^2 = (2x - 5)(2x + 5)$.

**İki kare toplamı** ($x^2 + 9$ gibi) gerçek sayılarla çarpanlara ayrılmaz.
$(x + 3)^2 = x^2 + 6x + 9$, ortada $6x$ var.

## Üç terimliler: x² + bx + c

$(x + p)(x + q)$'yu açınca

$$
(x + p)(x + q) = x^2 + (p + q)x + pq
$$

çıkıyor. Demek ki $x^2 + bx + c$'yi ayırmak için **çarpımı $c$, toplamı
$b$** olan iki sayı $p$ ve $q$ aranır.

<figure class="fig">
<svg viewBox="0 0 480 206" width="480"><line class="curve3" x1="58" y1="38" x2="182" y2="162"/><line class="curve3" x1="182" y1="38" x2="58" y2="162"/><text class="ink" x="120" y="60" font-size="16" text-anchor="middle">6</text><text class="dim" x="120" y="76" font-size="10" text-anchor="middle">çarpım</text><text class="ink" x="120" y="146" font-size="16" text-anchor="middle">5</text><text class="dim" x="120" y="160" font-size="10" text-anchor="middle">toplam</text><circle class="dot" opacity="0.3" cx="76" cy="100" r="18"/><text class="ink" x="76" y="106" font-size="16" text-anchor="middle">2</text><circle class="dot" opacity="0.3" cx="164" cy="100" r="18"/><text class="ink" x="164" y="106" font-size="16" text-anchor="middle">3</text><text class="ink" x="120" y="192" font-size="12" text-anchor="middle">x² + 5x + 6 = (x + 2)(x + 3)</text><line class="curve3" x1="298" y1="38" x2="422" y2="162"/><line class="curve3" x1="422" y1="38" x2="298" y2="162"/><text class="ink" x="360" y="60" font-size="16" text-anchor="middle">−12</text><text class="dim" x="360" y="76" font-size="10" text-anchor="middle">çarpım</text><text class="ink" x="360" y="146" font-size="16" text-anchor="middle">−1</text><text class="dim" x="360" y="160" font-size="10" text-anchor="middle">toplam</text><circle class="dot" opacity="0.3" cx="316" cy="100" r="18"/><text class="ink" x="316" y="106" font-size="16" text-anchor="middle">−4</text><circle class="dot" opacity="0.3" cx="404" cy="100" r="18"/><text class="ink" x="404" y="106" font-size="16" text-anchor="middle">3</text><text class="ink" x="360" y="192" font-size="12" text-anchor="middle">x² − x − 12 = (x − 4)(x + 3)</text></svg>
  <figcaption>Elmas yöntemi: üste çarpımı ($c$), alta toplamı ($b$) yaz; iki yana, çarpımı üsttekini, toplamı alttakini veren sayıları bul. Solda $2 \cdot 3 = 6$, $2 + 3 = 5$. Sağda $(-4) \cdot 3 = -12$, $-4 + 3 = -1$.</figcaption>
</figure>

**Örnek:** $x^2 + 5x + 6$. Çarpımı $6$ olan tam sayı çiftleri: $1 \cdot
6$, $2 \cdot 3$ (ve negatifleri). Toplamı $5$ olan: $2$ ve $3$.

$$
x^2 + 5x + 6 = (x + 2)(x + 3)
$$

<figure class="fig">
<svg viewBox="0 0 420 266" width="420"><rect class="dot" opacity="0.35" x="130" y="48" width="110" height="110"/><rect class="curve3" x="130" y="48" width="110" height="110"/><text class="ink" x="185.0" y="108.0" font-size="16" text-anchor="middle">x²</text><rect class="dot2" opacity="0.35" x="240" y="48" width="24" height="110"/><rect class="curve3" x="240" y="48" width="24" height="110"/><text class="ink" x="252.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="264" y="48" width="24" height="110"/><rect class="curve3" x="264" y="48" width="24" height="110"/><text class="ink" x="276.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="288" y="48" width="24" height="110"/><rect class="curve3" x="288" y="48" width="24" height="110"/><text class="ink" x="300.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="130" y="158" width="110" height="24"/><rect class="curve3" x="130" y="158" width="110" height="24"/><text class="ink" x="185.0" y="175.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="130" y="182" width="110" height="24"/><rect class="curve3" x="130" y="182" width="110" height="24"/><text class="ink" x="185.0" y="199.0" font-size="13" text-anchor="middle">x</text><rect class="dot3" opacity="0.35" x="240" y="158" width="24" height="24"/><rect class="curve3" x="240" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="264" y="158" width="24" height="24"/><rect class="curve3" x="264" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="288" y="158" width="24" height="24"/><rect class="curve3" x="288" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="240" y="182" width="24" height="24"/><rect class="curve3" x="240" y="182" width="24" height="24"/><rect class="dot3" opacity="0.35" x="264" y="182" width="24" height="24"/><rect class="curve3" x="264" y="182" width="24" height="24"/><rect class="dot3" opacity="0.35" x="288" y="182" width="24" height="24"/><rect class="curve3" x="288" y="182" width="24" height="24"/><line class="curve" x1="130" y1="34" x2="312" y2="34"/><text class="ink" x="221.0" y="26" font-size="14" text-anchor="middle">x + 3</text><line class="curve" x1="116" y1="48" x2="116" y2="206"/><text class="ink" x="108" y="132.0" font-size="14" text-anchor="end">x + 2</text><text class="dim" x="221.0" y="234" font-size="11" text-anchor="middle">parçalar: bir x², beş x, altı birim</text><text class="ink" x="221.0" y="254" font-size="13" text-anchor="middle">x² + 5x + 6 = (x + 3)(x + 2)</text></svg>
  <figcaption>Aynı iş alanla: bir $x^2$ karesi, beş $x$ şeridi ve altı birim kareyi boşluksuz bir dikdörtgene dizince kenarlar $x + 3$ ve $x + 2$ çıkıyor. Çarpanlara ayırmak, alanı bilinen dikdörtgenin kenarlarını bulmak.</figcaption>
</figure>

**İşaretler için ipucu:**

| $c$ | $b$ | $p$ ve $q$ |
|---|---|---|
| pozitif | pozitif | ikisi de pozitif |
| pozitif | negatif | ikisi de negatif |
| negatif | herhangi | işaretleri farklı; büyüğü $b$'nin işaretini alır |

$x^2 - x - 12$: çarpım $-12$ (işaretler farklı), toplam $-1$ (büyük olan
negatif). $-4$ ve $3$: $(x - 4)(x + 3)$.

## Üç terimliler: ax² + bx + c

$x^2$'nin katsayısı $1$ değilse **$ac$ yöntemi**: çarpımı $a \cdot c$,
toplamı $b$ olan iki sayı bul, ortadaki terimi onlarla ikiye böl, sonra
gruplama yap.

$$
2x^2 + 7x + 3
$$

$a \cdot c = 6$, toplam $7$: $6$ ve $1$.

$$
\begin{aligned}
2x^2 + 7x + 3 &= 2x^2 + 6x + x + 3 \\
&= 2x(x + 3) + 1(x + 3) \\
&= (2x + 1)(x + 3)
\end{aligned}
$$

**Sağlama:** $(2x + 1)(x + 3) = 2x^2 + 6x + x + 3$ ✓.

## Nereden başlamalı?

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1. Ortak çarpan</b><br>var mı?</span>
    <span class="arrow">→</span>
    <span class="node"><b>2. Kalıp</b><br>özdeşlikler</span>
    <span class="arrow">→</span>
    <span class="node"><b>3. Üç terimli</b><br>çarpım–toplam</span>
    <span class="arrow">→</span>
    <span class="node"><b>4. Kontrol</b><br>geri aç</span>
  </div>
  <figcaption>Her zaman önce ortak çarpanı çıkar; geriye kalan çoğu zaman bir kalıba ya da basit bir üç terimliye dönüşüyor. Sonunda çarpanları açıp başa döndüğünü gör.</figcaption>
</figure>

$$
\begin{aligned}
3x^3 - 12x &= 3x(x^2 - 4) \\
&= 3x(x - 2)(x + 2)
\end{aligned}
$$

## Kesirleri sadeleştirmek

Kesirlerde sadeleştirme yalnızca **çarpanlar** arasında yapılır. Önce pay
ve paydayı çarpanlarına ayır:

$$
\frac{x^2 - 9}{x^2 + 5x + 6} = \frac{(x - 3)(x + 3)}{(x + 2)(x + 3)} = \frac{x - 3}{x + 2}
$$

Bu eşitlik $x = -3$ ve $x = -2$ dışında geçerli: o değerlerde asıl kesrin
paydası sıfır.

## Çarpım sıfırsa

İki sayının çarpımı sıfırsa en az biri sıfırdır. Bu yüzden çarpanlara
ayrılmış bir ifadenin sıfır olduğu yerler hemen okunur:

$$
(x - 2)(x + 5) = 0 \quad\Rightarrow\quad x = 2 \text{ ya da } x = -5
$$

İkinci Dereceden Denklemler bölümünde bu fikri ana yöntem olarak
kullanacağız.

## Makine öğrenmesinde çarpanlara ayırma

**Daha az işlem.** $w x_1 + w x_2 + w x_3$ üç çarpma ve iki toplama;
$w(x_1 + x_2 + x_3)$ ise iki toplama ve **bir** çarpma. Milyonlarca kez
tekrarlanan hesaplarda ortak çarpanı dışarı almak ciddi zaman kazandırıyor.

**Sıfır yerleri.** Bir modelin davranışını değiştirdiği noktalar çoğu
zaman bir ifadenin sıfır olduğu yerler. Çarpanlarına ayrılmış bir ifadede
bu yerler hesap yapmadan görünür.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$x^2 - 9 = (x - 3)^2$</p>
      <p>$x^2 + 9 = (x + 3)^2$</p>
      <p>$\dfrac{x + 3}{3} = x$</p>
      <p>$6x^2 + 9x = 3(2x^2 + 3x)$ (bitti)</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$x^2 - 9 = (x - 3)(x + 3)$</p>
      <p>$x^2 + 9$ ayrılmaz</p>
      <p>$\dfrac{x + 3}{3}$ sadeleşmez; $3$ bir terim</p>
      <p>$6x^2 + 9x = 3x(2x + 3)$</p>
    </div>
  </div>
  <figcaption>Çarpanları geri açarak her sonucu sına; sadeleştirmeyi yalnızca çarpanlar arasında yap.</figcaption>
</figure>

- **İşaret hatası.** $x^2 - x - 12$'yi $(x + 4)(x - 3)$ diye ayırmak
  ortadaki terimi $+x$ yapar. Geri açmak bunu hemen yakalar.
- **Toplamdaki terimi sadeleştirmek.** $\dfrac{x + 3}{x + 5}$'te $x$'ler
  sadeleşmez; ikisi de terim.

## Özet

- Çarpanlara ayırma, açmanın tersi; sonucu geri açarak sına.
- Önce ortak çarpan: katsayılarda EBOB, harflerde en küçük üs; tamamını çıkar.
- Dört terimde gruplama: $ax + ay + bx + by = (a + b)(x + y)$.
- $a^2 - b^2 = (a - b)(a + b)$; $a^2 \pm 2ab + b^2 = (a \pm b)^2$; $a^2 + b^2$ ayrılmaz.
- $x^2 + bx + c$: çarpımı $c$, toplamı $b$ olan iki sayı.
- $ax^2 + bx + c$: çarpımı $ac$, toplamı $b$ olan sayılarla ortadaki terimi böl, grupla.
- Kesirde sadeleştirme yalnızca çarpanlar arasında; paydayı sıfır yapan değerler dışarıda.
- $AB = 0$ ise $A = 0$ ya da $B = 0$.
