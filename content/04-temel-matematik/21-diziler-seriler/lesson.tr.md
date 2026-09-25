# Diziler, Seriler ve Σ Gösterimi

Bir **dizi**, sırayla dizilmiş sayılardır: $2, 4, 6, 8, \dots$ Bir
**seri**, bu sayıların toplamıdır: $2 + 4 + 6 + 8 + \dots$ Uzun toplamları
kısaca yazmak için büyük sigma harfi $\Sigma$ kullanılır. Makine öğrenmesi
formülleri Σ ile dolu: ortalama, hata fonksiyonu, iki vektörün çarpımı,
softmax'in paydası hep birer toplam. Bu bölümde dizileri, iki önemli dizi
türünü (aritmetik ve geometrik), Σ gösterimini okuyup yazmayı ve toplamların
kısa yoldan nasıl hesaplandığını göreceğiz. Sonsuz tane sayının toplamının
bile sonlu bir sayı olabildiğini de göreceğiz.

Ön bilgi: Doğal Sayılar ve İşlem Önceliği, Fonksiyonlar, Üstel
Fonksiyonlar ve Büyüme.

## Dizi nedir?

Dizi, her doğal sayıya bir sayı eşleyen bir fonksiyondur: $1.$ terim,
$2.$ terim, $3.$ terim… $n.$ terim $a_n$ diye yazılır; küçük $n$'ye
**indis** denir.

Dizi iki yolla verilebilir:

- **Genel terimle:** $a_n = 2n + 1$ ise $a_1 = 3$, $a_2 = 5$, $a_{10} = 21$.
  Herhangi bir terime doğrudan gidilir.
- **Bir öncekinden (özyinelemeli):** $a_1 = 3$ ve $a_{n+1} = a_n + 2$. Aynı
  dizi, ama $a_{10}$ için önceki dokuz terimi bilmek gerekir.

Ünlü bir özyinelemeli dizi **Fibonacci**: $F_1 = F_2 = 1$ ve her terim
önceki ikisinin toplamı, $F_{n+2} = F_{n+1} + F_n$. Terimler $1, 1, 2, 3,
5, 8, 13, 21, \dots$

## Aritmetik dizi

Her terim bir öncekine **aynı sayıyı ekleyerek** bulunur. Bu sayıya
**ortak fark** denir ve $d$ ile gösterilir.

$$
a_n = a_1 + (n - 1) d
$$

$5, 8, 11, 14, \dots$ dizisinde $a_1 = 5$ ve $d = 3$. Yirminci terim:
$a_{20} = 5 + 19 \cdot 3 = 62$. Birinci terimden yirminciye $19$ adım var,
$20$ değil; formüldeki $(n - 1)$ bu yüzden.

**İki terimden.** $a_4 = 17$ ve $a_{10} = 41$ ise aradaki $6$ adımda $24$
artmış: $d = \frac{24}{6} = 4$. Geriye doğru $a_1 = 17 - 3 \cdot 4 = 5$.

Aritmetik dizi, Koordinat Düzlemi bölümündeki **doğrunun** tam sayılardaki
değerleri: $a_n = dn + (a_1 - d)$; eğim $d$.

## Geometrik dizi

Her terim bir öncekini **aynı sayıyla çarparak** bulunur. Bu sayıya
**ortak oran** denir ve $r$ ile gösterilir.

$$
a_n = a_1 \cdot r^{n - 1}
$$

$3, 6, 12, 24, \dots$ dizisinde $a_1 = 3$ ve $r = 2$. Sekizinci terim:
$a_8 = 3 \cdot 2^7 = 384$. Geometrik dizi, bir önceki bölümdeki **üstel
fonksiyonun** tam sayılardaki değerleri.

<figure class="fig">
<svg viewBox="0 0 440 244" width="440"><line class="grid" x1="40.0" y1="230.0" x2="40.0" y2="20.0"/><line class="grid" x1="80.0" y1="230.0" x2="80.0" y2="20.0"/><line class="grid" x1="120.0" y1="230.0" x2="120.0" y2="20.0"/><line class="grid" x1="160.0" y1="230.0" x2="160.0" y2="20.0"/><line class="grid" x1="200.0" y1="230.0" x2="200.0" y2="20.0"/><line class="grid" x1="240.0" y1="230.0" x2="240.0" y2="20.0"/><line class="grid" x1="280.0" y1="230.0" x2="280.0" y2="20.0"/><line class="grid" x1="320.0" y1="230.0" x2="320.0" y2="20.0"/><line class="grid" x1="360.0" y1="230.0" x2="360.0" y2="20.0"/><line class="grid" x1="400.0" y1="230.0" x2="400.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="400.0" y2="230.0"/><line class="grid" x1="40.0" y1="206.7" x2="400.0" y2="206.7"/><line class="grid" x1="40.0" y1="183.3" x2="400.0" y2="183.3"/><line class="grid" x1="40.0" y1="160.0" x2="400.0" y2="160.0"/><line class="grid" x1="40.0" y1="136.7" x2="400.0" y2="136.7"/><line class="grid" x1="40.0" y1="113.3" x2="400.0" y2="113.3"/><line class="grid" x1="40.0" y1="90.0" x2="400.0" y2="90.0"/><line class="grid" x1="40.0" y1="66.7" x2="400.0" y2="66.7"/><line class="grid" x1="40.0" y1="43.3" x2="400.0" y2="43.3"/><line class="grid" x1="40.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="40.0" y1="230.0" x2="400.0" y2="230.0"/><line class="line" x1="40.0" y1="230.0" x2="40.0" y2="20.0"/><text class="dim" x="80.0" y="243.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="120.0" y="243.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="160.0" y="243.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="200.0" y="243.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="240.0" y="243.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="280.0" y="243.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="320.0" y="243.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="360.0" y="243.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="35.0" y="186.3" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="139.7" font-size="9" text-anchor="end">8</text><text class="dim" x="35.0" y="93.0" font-size="9" text-anchor="end">12</text><text class="dim" x="35.0" y="46.3" font-size="9" text-anchor="end">16</text><circle class="dot2" cx="80.0" cy="206.7" r="4.5"/><circle class="dot" cx="80.0" cy="218.3" r="4.5"/><circle class="dot2" cx="120.0" cy="183.3" r="4.5"/><circle class="dot" cx="120.0" cy="212.5" r="4.5"/><circle class="dot2" cx="160.0" cy="160.0" r="4.5"/><circle class="dot" cx="160.0" cy="203.8" r="4.5"/><circle class="dot2" cx="200.0" cy="136.7" r="4.5"/><circle class="dot" cx="200.0" cy="190.6" r="4.5"/><circle class="dot2" cx="240.0" cy="113.3" r="4.5"/><circle class="dot" cx="240.0" cy="170.9" r="4.5"/><circle class="dot2" cx="280.0" cy="90.0" r="4.5"/><circle class="dot" cx="280.0" cy="141.4" r="4.5"/><circle class="dot2" cx="320.0" cy="66.7" r="4.5"/><circle class="dot" cx="320.0" cy="97.1" r="4.5"/><circle class="dot2" cx="360.0" cy="43.3" r="4.5"/><circle class="dot" cx="360.0" cy="30.7" r="4.5"/><line class="curve2" x1="56.0" y1="34.0" x2="76.0" y2="34.0"/><text class="ink" x="80.0" y="38.0" font-size="11" text-anchor="start">aritmetik: 2, 4, 6, … (her adımda +2)</text><line class="curve" x1="56.0" y1="57.3" x2="76.0" y2="57.3"/><text class="ink" x="80.0" y="61.3" font-size="11" text-anchor="start">geometrik: 1; 1,5; 2,25; … (her adımda ×1,5)</text><text class="dim" x="400.0" y="224.0" font-size="11" text-anchor="end">n</text></svg>
  <figcaption>Aritmetik dizi her adımda aynı miktar yükseliyor, noktaları bir doğru üstünde. Geometrik dizi her adımda aynı oranda büyüyor; başta geride, sonra hızlanıyor.</figcaption>
</figure>

$r$ negatifse işaretler sırayla değişir ($1, -2, 4, -8, \dots$); $0 < r < 1$
ise terimler küçülür: $80, 40, 20, 10, \dots$

## Σ gösterimi

Uzun bir toplamı kısaca yazmanın yolu:

$$
\sum_{i=1}^{n} a_i = a_1 + a_2 + \dots + a_n
$$

Okunuşu: "$i$, $1$'den $n$'ye kadar, $a_i$'lerin toplamı".

| Parça | Anlamı |
|---|---|
| $\Sigma$ | topla |
| $i$ | sayaç (indis) |
| alttaki $i = 1$ | sayaç buradan başlar |
| üstteki $n$ | sayaç burada biter (dahil) |
| $a_i$ | her adımda eklenen terim |

**Açarak oku.** Sayaca sırayla değer ver, terimleri yaz, topla:

$$
\sum_{i=1}^{4} i^2 = 1 + 4 + 9 + 16 = 30
\qquad
\sum_{k=0}^{3} 2^k = 1 + 2 + 4 + 8 = 15
$$

**Terim sayısı** üst sınır eksi alt sınır artı bir: $\sum_{k=0}^{3}$
dört terimli, $\sum_{i=3}^{7}$ beş terimli.

**Sayacın adı önemsiz.** $\sum_{i=1}^{4} i^2$ ile $\sum_{k=1}^{4} k^2$ aynı
toplam; sayaç yalnızca toplamın içinde yaşar.

**Kurallar.** Bunlar toplamayı ve dağılma özelliğini tekrar yazmaktan
ibaret:

| Kural | Neden |
|---|---|
| $\sum (a_i + b_i) = \sum a_i + \sum b_i$ | terimler istenen sırayla toplanabilir |
| $\sum c \cdot a_i = c \sum a_i$ | ortak çarpan dışarı alınır |
| $\sum_{i=1}^{n} c = n \cdot c$ | $n$ kez $c$ eklenir |

**Dikkat:** Çarpım içeri girmez: $\sum a_i b_i \neq \left( \sum a_i \right)
\left( \sum b_i \right)$. $a = (1, 2)$, $b = (3, 4)$ için sol taraf
$3 + 8 = 11$, sağ taraf $3 \cdot 7 = 21$.

## Aritmetik serinin toplamı

Söylentiye göre Gauss okulda $1 + 2 + \dots + 100$ toplamını bir dakikada
bulmuş: baştan ve sondan eşleştir, $1 + 100 = 2 + 99 = \dots = 101$; $50$
çift var, toplam $50 \cdot 101 = 5050$.

<figure class="fig">
<svg viewBox="0 0 440 240" width="440"><rect class="dot" opacity="0.55" x="130" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="160" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="190" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="20" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="50" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="190" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="50" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="220" y="110" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="110" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="220" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="250" y="140" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="20" y="186" width="14" height="14" rx="2"/><text class="ink" x="40" y="197" font-size="12" text-anchor="start">1 + 2 + 3 + 4 + 5</text><rect class="dot2" opacity="0.55" x="220" y="186" width="14" height="14" rx="2"/><text class="ink" x="240" y="197" font-size="12" text-anchor="start">aynısı ters çevrilmiş</text><text class="ink" x="220" y="226" font-size="13" text-anchor="middle">2 · S = 5 · 6 = 30, yani S = 15</text><text class="dim" x="120" y="39" font-size="11" text-anchor="end">1</text><text class="dim" x="120" y="69" font-size="11" text-anchor="end">2</text><text class="dim" x="120" y="99" font-size="11" text-anchor="end">3</text><text class="dim" x="120" y="129" font-size="11" text-anchor="end">4</text><text class="dim" x="120" y="159" font-size="11" text-anchor="end">5</text></svg>
  <figcaption>Mor kareler 1 + 2 + 3 + 4 + 5. Aynı merdiven ters çevrilip yanına konunca (turuncu) 5 satır ve 6 sütunluk bir dikdörtgen çıkıyor. Dikdörtgen toplamın iki katı.</figcaption>
</figure>

Aynı fikir her aritmetik seriye uyar: toplamı iki kez yaz, biri ters
sırayla; her sütun $a_1 + a_n$ eder ve $n$ sütun var.

$$
S_n = \frac{n \, (a_1 + a_n)}{2}
$$

Özel hâl, ilk $n$ doğal sayının toplamı:

$$
\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}
$$

$5, 8, 11, \dots, 62$ ($20$ terim) toplamı $\frac{20 \cdot 67}{2} = 670$.

İlk $n$ karenin toplamının da bir formülü var:
$\sum_{i=1}^{n} i^2 = \frac{n(n + 1)(2n + 1)}{6}$. $n = 4$ için
$\frac{4 \cdot 5 \cdot 9}{6} = 30$; yukarıda açarak bulduğumuz sayı.

## Geometrik serinin toplamı

$S = a_1 + a_1 r + a_1 r^2 + \dots + a_1 r^{n-1}$. Her iki tarafı $r$ ile
çarpınca terimler bir basamak kayar; $S$'den $rS$'yi çıkarınca ortadaki
bütün terimler birbirini götürür:

$$
\begin{aligned}
S - rS &= a_1 - a_1 r^n \\
S &= a_1 \cdot \frac{1 - r^n}{1 - r} \qquad (r \neq 1)
\end{aligned}
$$

$1 + 2 + 4 + \dots + 2^9$: $a_1 = 1$, $r = 2$, $n = 10$ terim;
$\frac{1 - 2^{10}}{1 - 2} = \frac{-1023}{-1} = 1023$. İkilik sistemde on
tane $1$ yan yana, $1111111111_2 = 1023$.

$3, 6, 12, \dots, 384$ ($8$ terim) toplamı $3 \cdot \frac{1 - 2^8}{1 - 2} =
3 \cdot 255 = 765$.

## Sonsuz geometrik seri

$\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots$ sonsuz terimli, ama
toplamı sonsuz değil.

<figure class="fig">
<svg viewBox="0 0 440 114" width="440"><rect class="box" x="20" y="30" width="400" height="44"/><rect class="dot" opacity="0.6" x="20" y="30" width="198.5" height="44" rx="2"/><text class="ink" x="120.0" y="57.0" font-size="13" text-anchor="middle">½</text><rect class="dot2" opacity="0.6" x="220.0" y="30" width="98.5" height="44" rx="2"/><text class="ink" x="270.0" y="57.0" font-size="13" text-anchor="middle">¼</text><rect class="dot" opacity="0.6" x="320.0" y="30" width="48.5" height="44" rx="2"/><text class="ink" x="345.0" y="57.0" font-size="13" text-anchor="middle">⅛</text><rect class="dot2" opacity="0.6" x="370.0" y="30" width="23.5" height="44" rx="2"/><text class="ink" x="382.5" y="57.0" font-size="10" text-anchor="middle">1/16</text><rect class="dot" opacity="0.6" x="395.0" y="30" width="11.0" height="44" rx="2"/><rect class="dot2" opacity="0.6" x="407.5" y="30" width="4.8" height="44" rx="2"/><rect class="dot" opacity="0.6" x="413.8" y="30" width="1.6" height="44" rx="2"/><text class="dim" x="20" y="22" font-size="11" text-anchor="start">0</text><text class="dim" x="420" y="22" font-size="11" text-anchor="end">1</text><text class="ink" x="220.0" y="100" font-size="12" text-anchor="middle">toplam 1'e yaklaşır ama geçmez</text></svg>
  <figcaption>1 uzunluğundaki şeridin yarısı, sonra kalanın yarısı, sonra onun da yarısı… Her adımda kalan boşluk yarıya iniyor; parçalar şeridi dolduruyor ama taşmıyor.</figcaption>
</figure>

İlk $n$ terimin toplamına **kısmi toplam** denir: $S_n = 1 -
\left( \frac{1}{2} \right)^n$. $n$ büyüdükçe $\left( \frac{1}{2}
\right)^n$ sıfıra gider ve $S_n$, $1$'e yaklaşır.

<figure class="fig">
<svg viewBox="0 0 440 224" width="440"><line class="grid" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><line class="grid" x1="88.9" y1="210.0" x2="88.9" y2="20.0"/><line class="grid" x1="127.8" y1="210.0" x2="127.8" y2="20.0"/><line class="grid" x1="166.7" y1="210.0" x2="166.7" y2="20.0"/><line class="grid" x1="205.6" y1="210.0" x2="205.6" y2="20.0"/><line class="grid" x1="244.4" y1="210.0" x2="244.4" y2="20.0"/><line class="grid" x1="283.3" y1="210.0" x2="283.3" y2="20.0"/><line class="grid" x1="322.2" y1="210.0" x2="322.2" y2="20.0"/><line class="grid" x1="361.1" y1="210.0" x2="361.1" y2="20.0"/><line class="grid" x1="400.0" y1="210.0" x2="400.0" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="grid" x1="50.0" y1="166.8" x2="400.0" y2="166.8"/><line class="grid" x1="50.0" y1="123.6" x2="400.0" y2="123.6"/><line class="grid" x1="50.0" y1="80.5" x2="400.0" y2="80.5"/><line class="grid" x1="50.0" y1="37.3" x2="400.0" y2="37.3"/><line class="line" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="line" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><text class="dim" x="88.9" y="223.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="127.8" y="223.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="166.7" y="223.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="205.6" y="223.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="244.4" y="223.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="283.3" y="223.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="322.2" y="223.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="361.1" y="223.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="45.0" y="169.8" font-size="9" text-anchor="end">0.25</text><text class="dim" x="45.0" y="126.6" font-size="9" text-anchor="end">0.5</text><text class="dim" x="45.0" y="83.5" font-size="9" text-anchor="end">0.75</text><text class="dim" x="45.0" y="40.3" font-size="9" text-anchor="end">1</text><line class="curve3" stroke-dasharray="5 4" x1="50.0" y1="37.3" x2="400.0" y2="37.3"/><rect class="dot" opacity="0.75" x="80.3" y="123.6" width="17.1" height="86.4"/><rect class="dot" opacity="0.75" x="119.2" y="80.5" width="17.1" height="129.5"/><rect class="dot" opacity="0.75" x="158.1" y="58.9" width="17.1" height="151.1"/><rect class="dot" opacity="0.75" x="197.0" y="48.1" width="17.1" height="161.9"/><rect class="dot" opacity="0.75" x="235.9" y="42.7" width="17.1" height="167.3"/><rect class="dot" opacity="0.75" x="274.8" y="40.0" width="17.1" height="170.0"/><rect class="dot" opacity="0.75" x="313.7" y="38.6" width="17.1" height="171.4"/><rect class="dot" opacity="0.75" x="352.6" y="37.9" width="17.1" height="172.1"/><text class="ink" x="400.0" y="31.3" font-size="11" text-anchor="end">sınır: 1</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">kısmi toplam Sₙ</text><text class="dim" x="400.0" y="204.0" font-size="11" text-anchor="end">n</text></svg>
  <figcaption>Kısmi toplamlar 0,5; 0,75; 0,875; 0,9375… Her çubuk bir öncekiyle 1 arasındaki boşluğun yarısını kapatıyor. Sınır 1.</figcaption>
</figure>

Genel kural: $-1 < r < 1$ ise $r^n \to 0$ ve formüldeki $r^n$ düşer:

$$
\sum_{k=0}^{\infty} a_1 r^k = \frac{a_1}{1 - r} \qquad (-1 < r < 1)
$$

- $\frac{1}{2} + \frac{1}{4} + \dots = \frac{1/2}{1 - 1/2} = 1$.
- $0{,}333\dots = \frac{3}{10} + \frac{3}{100} + \dots =
  \frac{3/10}{1 - 1/10} = \frac{1}{3}$.
- $r \geq 1$ ya da $r \leq -1$ ise terimler küçülmez ve toplam bir sayıya
  yerleşmez: $1 + 2 + 4 + \dots$ sınırsız büyür. Aritmetik seri de ($d \neq 0$
  ise) hep sınırsız büyür.

## Makine öğrenmesinde Σ

**Ortalama.** $n$ sayının ortalaması

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

**Hata fonksiyonu.** Ortalama kare hata (MSE), gerçek değerler $y_i$ ve
tahminler $\hat{y}_i$ için:

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

$y = (3, 5, 8)$ ve $\hat{y} = (2, 5, 10)$ için farklar $1, 0, -2$; kareleri
$1, 0, 4$; $\text{MSE} = \frac{5}{3}$.

**Ağırlıklı toplam.** Bir nöronun girdisi $\sum_{i} w_i x_i + b$: her
özellik kendi ağırlığıyla çarpılıp toplanıyor. Doğrusal Cebir'deki nokta
çarpımı tam olarak bu.

**Gelecek ödülleri.** Pekiştirmeli öğrenmede her adımda $1$ ödül alan bir
ajanın gelecekteki ödülleri $\gamma = 0{,}9$ ile indirgenir:
$1 + 0{,}9 + 0{,}9^2 + \dots = \frac{1}{1 - 0{,}9} = 10$. Sonsuz geometrik
seri, sonsuz bir geleceğe sonlu bir değer veriyor.

**Hareketli ortalama.** Momentum ve Adam gibi yöntemler eski gradyanları
$(1 - \beta), (1 - \beta)\beta, (1 - \beta)\beta^2, \dots$ ağırlıklarıyla
toplar. Bu ağırlıklar bir geometrik seri ve toplamları
$\frac{1 - \beta}{1 - \beta} = 1$.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$a_{20} = a_1 + 20d$</p>
      <p>$\sum_{i=3}^{7}$: $4$ terim</p>
      <p>$\sum a_i b_i = \sum a_i \cdot \sum b_i$</p>
      <p>$1 + 2 + 4 + \dots = \dfrac{1}{1 - 2} = -1$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$a_{20} = a_1 + 19d$</p>
      <p>$7 - 3 + 1 = 5$ terim</p>
      <p>çarpım toplamın içine girmez</p>
      <p>$r = 2$: toplam sınırsız büyür</p>
    </div>
  </div>
  <figcaption>Terim sayısında ve adım sayısında bir fark var; sonsuz toplam formülü yalnızca −1 &lt; r &lt; 1 iken geçerli.</figcaption>
</figure>

- **Oranı ters almak.** Ortak oran sonraki bölü önceki: $80, 40, 20$
  dizisinde $r = \frac{40}{80} = \frac{1}{2}$, $2$ değil.
- **Σ'nin önündeki çarpanı unutmak.** $\frac{1}{n} \sum$ yazıldıysa bölme
  bütün toplamadan sonra yapılır.

## Özet

- Dizi sıralı sayılar $a_n$; genel terimle ya da bir öncekinden
  tanımlanır.
- Aritmetik: $a_n = a_1 + (n - 1)d$, toplam $\frac{n(a_1 + a_n)}{2}$.
- Geometrik: $a_n = a_1 r^{n-1}$, toplam $a_1 \frac{1 - r^n}{1 - r}$.
- $\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$.
- Σ'de sayaç alt sınırdan üst sınıra; toplam ve sabit çarpan kuralları
  var, çarpım içeri girmez.
- $-1 < r < 1$ ise sonsuz geometrik seri $\frac{a_1}{1 - r}$.
- Ortalama, MSE, ağırlıklı toplam, indirgenmiş ödül ve hareketli ortalama
  hep birer Σ.
