# Boyut İndirgeme: PCA'nın Matematiği

Bir veri kümesinde yüzlerce özellik olabilir; ama çoğu zaman bunlar
birbirine bağlıdır ve gerçekte çok daha az "yönde" değişirler. **Temel
bileşenler analizi** (PCA), verinin en çok yayıldığı yönleri bulur ve
veriyi o birkaç yöne izdüşürerek boyutu indirir. Bu bölüm İleri Matematik modülünün iki
yarısını birleştiriyor: kovaryans matrisi (istatistik), özdeğer ve
özvektörler, SVD ve dik izdüşüm (doğrusal cebir).

Ön bilgi: Özdeğerler ve Özvektörler; Tekil Değer Ayrışımı (SVD); Kovaryans
ve Korelasyon; Doğrusal Regresyonun Matematiği (dik izdüşüm).

## Fikir: en çok yayılan yön

<figure class="fig">
<svg viewBox="0 0 420 322" width="420"><line class="grid" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><line class="grid" x1="74.0" y1="292.0" x2="74.0" y2="20.0"/><line class="grid" x1="108.0" y1="292.0" x2="108.0" y2="20.0"/><line class="grid" x1="142.0" y1="292.0" x2="142.0" y2="20.0"/><line class="grid" x1="176.0" y1="292.0" x2="176.0" y2="20.0"/><line class="grid" x1="210.0" y1="292.0" x2="210.0" y2="20.0"/><line class="grid" x1="244.0" y1="292.0" x2="244.0" y2="20.0"/><line class="grid" x1="278.0" y1="292.0" x2="278.0" y2="20.0"/><line class="grid" x1="312.0" y1="292.0" x2="312.0" y2="20.0"/><line class="grid" x1="346.0" y1="292.0" x2="346.0" y2="20.0"/><line class="grid" x1="380.0" y1="292.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="grid" x1="40.0" y1="258.0" x2="380.0" y2="258.0"/><line class="grid" x1="40.0" y1="224.0" x2="380.0" y2="224.0"/><line class="grid" x1="40.0" y1="190.0" x2="380.0" y2="190.0"/><line class="grid" x1="40.0" y1="156.0" x2="380.0" y2="156.0"/><line class="grid" x1="40.0" y1="122.0" x2="380.0" y2="122.0"/><line class="grid" x1="40.0" y1="88.0" x2="380.0" y2="88.0"/><line class="grid" x1="40.0" y1="54.0" x2="380.0" y2="54.0"/><line class="grid" x1="40.0" y1="20.0" x2="380.0" y2="20.0"/><line class="line" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="line" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><text class="dim" x="108.0" y="305.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="176.0" y="305.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="244.0" y="305.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="312.0" y="305.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="35.0" y="227.0" font-size="9" text-anchor="end">2</text><text class="dim" x="35.0" y="159.0" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="91.0" font-size="9" text-anchor="end">6</text><circle class="dot" cx="166.8" cy="170.4" r="3.2"/><circle class="dot" cx="143.6" cy="186.8" r="3.2"/><circle class="dot" cx="204.3" cy="171.4" r="3.2"/><circle class="dot" cx="229.4" cy="143.8" r="3.2"/><circle class="dot" cx="248.8" cy="103.6" r="3.2"/><circle class="dot" cx="218.4" cy="157.5" r="3.2"/><circle class="dot" cx="183.7" cy="170.9" r="3.2"/><circle class="dot" cx="175.2" cy="180.8" r="3.2"/><circle class="dot" cx="238.0" cy="125.0" r="3.2"/><circle class="dot" cx="286.1" cy="109.6" r="3.2"/><circle class="dot" cx="223.5" cy="149.4" r="3.2"/><circle class="dot" cx="152.9" cy="191.4" r="3.2"/><circle class="dot" cx="166.4" cy="184.6" r="3.2"/><circle class="dot" cx="288.9" cy="116.9" r="3.2"/><circle class="dot" cx="211.2" cy="138.4" r="3.2"/><circle class="dot" cx="144.2" cy="226.3" r="3.2"/><circle class="dot" cx="216.8" cy="173.7" r="3.2"/><circle class="dot" cx="169.4" cy="208.4" r="3.2"/><circle class="dot" cx="173.5" cy="163.5" r="3.2"/><circle class="dot" cx="191.4" cy="175.7" r="3.2"/><circle class="dot" cx="186.7" cy="190.4" r="3.2"/><circle class="dot" cx="244.6" cy="153.0" r="3.2"/><circle class="dot" cx="203.5" cy="152.7" r="3.2"/><circle class="dot" cx="193.0" cy="187.6" r="3.2"/><circle class="dot" cx="239.4" cy="159.2" r="3.2"/><circle class="dot" cx="241.6" cy="122.4" r="3.2"/><circle class="dot" cx="147.3" cy="222.3" r="3.2"/><circle class="dot" cx="201.4" cy="168.1" r="3.2"/><circle class="dot" cx="166.4" cy="186.7" r="3.2"/><circle class="dot" cx="206.2" cy="167.0" r="3.2"/><circle class="dot" cx="153.0" cy="196.9" r="3.2"/><circle class="dot" cx="199.2" cy="138.6" r="3.2"/><circle class="dot" cx="212.8" cy="163.7" r="3.2"/><circle class="dot" cx="207.5" cy="181.3" r="3.2"/><circle class="dot" cx="179.4" cy="211.7" r="3.2"/><circle class="dot" cx="194.1" cy="170.9" r="3.2"/><circle class="dot" cx="164.5" cy="194.5" r="3.2"/><circle class="dot" cx="147.3" cy="195.0" r="3.2"/><circle class="dot" cx="224.1" cy="154.8" r="3.2"/><circle class="dot" cx="164.8" cy="196.6" r="3.2"/><circle class="dot" cx="268.5" cy="128.5" r="3.2"/><circle class="dot" cx="246.5" cy="140.2" r="3.2"/><circle class="dot" cx="119.6" cy="216.3" r="3.2"/><circle class="dot" cx="225.5" cy="152.3" r="3.2"/><circle class="dot" cx="160.0" cy="189.1" r="3.2"/><circle class="dot" cx="194.8" cy="131.1" r="3.2"/><circle class="dot" cx="207.7" cy="148.6" r="3.2"/><circle class="dot" cx="135.2" cy="237.8" r="3.2"/><circle class="dot" cx="184.4" cy="141.6" r="3.2"/><circle class="dot" cx="195.5" cy="159.6" r="3.2"/><circle class="dot" cx="261.1" cy="137.8" r="3.2"/><circle class="dot" cx="149.4" cy="181.5" r="3.2"/><circle class="dot" cx="242.7" cy="132.7" r="3.2"/><circle class="dot" cx="166.4" cy="198.0" r="3.2"/><circle class="dot" cx="200.8" cy="174.3" r="3.2"/><circle class="dot" cx="181.3" cy="194.7" r="3.2"/><circle class="dot" cx="274.1" cy="110.2" r="3.2"/><circle class="dot" cx="225.9" cy="124.9" r="3.2"/><circle class="dot" cx="321.2" cy="84.2" r="3.2"/><circle class="dot" cx="234.9" cy="130.7" r="3.2"/><line class="curve2" x1="201.7" y1="164.6" x2="277.5" y2="107.6"/><polygon class="dot2" points="284.5,102.3 279.2,111.9 273.8,104.8"/><line class="curve2" x1="60" y1="34" x2="86" y2="34"/><text class="ink" x="92" y="38" font-size="11" text-anchor="start">1. bileşen</text><line class="curve4" x1="201.7" y1="164.6" x2="191.9" y2="151.5"/><polygon class="dot3" points="186.6,144.5 196.2,149.8 189.0,155.2"/><line class="curve4" x1="60" y1="54" x2="86" y2="54"/><text class="ink" x="92" y="58" font-size="11" text-anchor="start">2. bileşen</text><circle class="dot3" cx="201.7" cy="164.6" r="4.5"/><text class="dim" x="380.0" y="320.0" font-size="10" text-anchor="end">x₁</text><text class="dim" x="32.0" y="24.0" font-size="10" text-anchor="end">x₂</text></svg>
  <figcaption>İki özellikli, birbirine bağlı 60 nokta. Turuncu ok verinin en çok yayıldığı yön (1. bileşen), yeşil ok ona dik olan 2. bileşen; ok uzunlukları o yöndeki standart sapmayla orantılı. Bu veride 1. bileşen toplam varyansın yaklaşık yüzde 94'ünü taşıyor.</figcaption>
</figure>

Noktalar neredeyse tek bir doğru boyunca uzanıyor. Her noktayı iki sayı
yerine "doğru üzerindeki konumu" ile, yani tek bir sayıyla anlatsak çok az
bilgi kaybederiz. PCA bu doğruyu (genelde de en iyi $k$ boyutlu alt uzayı)
bulur.

## Adım 0: merkezlemek

Önce her özelliğin ortalaması çıkarılır: $x \leftarrow x - \bar{x}$.
Özellikler farklı birimlerdeyse (metre ve lira gibi) standart sapmaya da
bölünür; yoksa büyük ölçekli özellik varyansa hâkim olur ve PCA yalnızca
onu görür.

## Bir yöndeki varyans

Birim vektör $u$ yönündeki izdüşüm $u^\mathsf{T}x$ bir sayıdır. Kovaryans
bölümündeki kurala göre varyansı:

$$
\operatorname{Var}(u^\mathsf{T}x) = u^\mathsf{T}\Sigma u
$$

Problem: $\lVert u \rVert = 1$ koşuluyla $u^\mathsf{T}\Sigma u$'yu en büyük
yapmak. Lagrange çarpanıyla türevi sıfıra eşitleyince:

$$
\Sigma u = \lambda u
$$

Yani $u$, kovaryans matrisinin bir **özvektörü**; o yöndeki varyans
$u^\mathsf{T}\Sigma u = \lambda$, yani **özdeğer**. En çok yayılan yön en
büyük özdeğerin özvektörüdür.

- **1. temel bileşen:** en büyük özdeğerin özvektörü.
- **2. temel bileşen:** birinciye dik yönler arasında varyansı en büyük
  olan; ikinci büyük özdeğerin özvektörü. $\Sigma$ simetrik olduğu için
  özvektörleri zaten birbirine dik.
- Özdeğerlerin toplamı ($\Sigma$'nın izi) toplam varyanstır.

**Örnek.**

$$
\Sigma = \begin{pmatrix} 5 & 4 \\ 4 & 5 \end{pmatrix}
$$

Karakteristik denklem $(5 - \lambda)^2 - 16 = 0$: $\lambda_1 = 9$,
$\lambda_2 = 1$. Özvektörler $\frac{1}{\sqrt{2}}(1, 1)$ ve
$\frac{1}{\sqrt{2}}(1, -1)$. Birinci bileşen toplam varyansın
$\frac{9}{10}$'unu, yani yüzde $90$'ını açıklıyor.

## İzdüşüm ve geri çatma

İlk $k$ özvektörü sütun olarak yan yana koyalım: $U_k$ ($d \times k$).

$$
z = U_k^\mathsf{T}(x - \bar{x}) \qquad \hat{x} = \bar{x} + U_k z
$$

- $z$: noktanın yeni, $k$ boyutlu koordinatları (**bileşen skorları**).
- $\hat{x}$: bu $k$ sayıdan geri çatılan nokta; alt uzaya dik izdüşüm.

<figure class="fig">
<svg viewBox="0 0 420 312" width="420"><line class="grid" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><line class="grid" x1="74.0" y1="292.0" x2="74.0" y2="20.0"/><line class="grid" x1="108.0" y1="292.0" x2="108.0" y2="20.0"/><line class="grid" x1="142.0" y1="292.0" x2="142.0" y2="20.0"/><line class="grid" x1="176.0" y1="292.0" x2="176.0" y2="20.0"/><line class="grid" x1="210.0" y1="292.0" x2="210.0" y2="20.0"/><line class="grid" x1="244.0" y1="292.0" x2="244.0" y2="20.0"/><line class="grid" x1="278.0" y1="292.0" x2="278.0" y2="20.0"/><line class="grid" x1="312.0" y1="292.0" x2="312.0" y2="20.0"/><line class="grid" x1="346.0" y1="292.0" x2="346.0" y2="20.0"/><line class="grid" x1="380.0" y1="292.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="grid" x1="40.0" y1="258.0" x2="380.0" y2="258.0"/><line class="grid" x1="40.0" y1="224.0" x2="380.0" y2="224.0"/><line class="grid" x1="40.0" y1="190.0" x2="380.0" y2="190.0"/><line class="grid" x1="40.0" y1="156.0" x2="380.0" y2="156.0"/><line class="grid" x1="40.0" y1="122.0" x2="380.0" y2="122.0"/><line class="grid" x1="40.0" y1="88.0" x2="380.0" y2="88.0"/><line class="grid" x1="40.0" y1="54.0" x2="380.0" y2="54.0"/><line class="grid" x1="40.0" y1="20.0" x2="380.0" y2="20.0"/><line class="curve" x1="38.7" y1="287.2" x2="364.8" y2="42.0"/><line class="curve2" stroke-width="1.6" x1="166.8" y1="170.4" x2="176.6" y2="183.5"/><line class="curve2" stroke-width="1.6" x1="143.6" y1="186.8" x2="153.9" y2="200.5"/><line class="curve2" stroke-width="1.6" x1="204.3" y1="171.4" x2="200.1" y2="165.8"/><line class="curve2" stroke-width="1.6" x1="229.4" y1="143.8" x2="229.4" y2="143.8"/><line class="curve2" stroke-width="1.6" x1="248.8" y1="103.6" x2="261.1" y2="120.0"/><line class="curve2" stroke-width="1.6" x1="218.4" y1="157.5" x2="215.7" y2="154.1"/><line class="curve2" stroke-width="1.6" x1="183.7" y1="170.9" x2="187.2" y2="175.5"/><line class="curve2" stroke-width="1.6" x1="175.2" y1="180.8" x2="177.0" y2="183.2"/><line class="curve2" stroke-width="1.6" x1="238.0" y1="125.0" x2="243.9" y2="132.9"/><line class="curve2" stroke-width="1.6" x1="286.1" y1="109.6" x2="282.0" y2="104.2"/><line class="curve2" stroke-width="1.6" x1="223.5" y1="149.4" x2="222.9" y2="148.7"/><line class="curve2" stroke-width="1.6" x1="152.9" y1="191.4" x2="157.6" y2="197.7"/><line class="curve2" stroke-width="1.6" x1="166.4" y1="184.6" x2="169.5" y2="188.8"/><line class="curve2" stroke-width="1.6" x1="288.9" y1="116.9" x2="280.3" y2="105.5"/><circle class="dot" cx="166.8" cy="170.4" r="4"/><circle class="dot3" cx="176.6" cy="183.5" r="3.4"/><circle class="dot" cx="143.6" cy="186.8" r="4"/><circle class="dot3" cx="153.9" cy="200.5" r="3.4"/><circle class="dot" cx="204.3" cy="171.4" r="4"/><circle class="dot3" cx="200.1" cy="165.8" r="3.4"/><circle class="dot" cx="229.4" cy="143.8" r="4"/><circle class="dot3" cx="229.4" cy="143.8" r="3.4"/><circle class="dot" cx="248.8" cy="103.6" r="4"/><circle class="dot3" cx="261.1" cy="120.0" r="3.4"/><circle class="dot" cx="218.4" cy="157.5" r="4"/><circle class="dot3" cx="215.7" cy="154.1" r="3.4"/><circle class="dot" cx="183.7" cy="170.9" r="4"/><circle class="dot3" cx="187.2" cy="175.5" r="3.4"/><circle class="dot" cx="175.2" cy="180.8" r="4"/><circle class="dot3" cx="177.0" cy="183.2" r="3.4"/><circle class="dot" cx="238.0" cy="125.0" r="4"/><circle class="dot3" cx="243.9" cy="132.9" r="3.4"/><circle class="dot" cx="286.1" cy="109.6" r="4"/><circle class="dot3" cx="282.0" cy="104.2" r="3.4"/><circle class="dot" cx="223.5" cy="149.4" r="4"/><circle class="dot3" cx="222.9" cy="148.7" r="3.4"/><circle class="dot" cx="152.9" cy="191.4" r="4"/><circle class="dot3" cx="157.6" cy="197.7" r="3.4"/><circle class="dot" cx="166.4" cy="184.6" r="4"/><circle class="dot3" cx="169.5" cy="188.8" r="3.4"/><circle class="dot" cx="288.9" cy="116.9" r="4"/><circle class="dot3" cx="280.3" cy="105.5" r="3.4"/><text class="ink" x="60" y="36" font-size="11" text-anchor="start">1. bileşen doğrusu</text><line class="curve" x1="60" y1="46" x2="86" y2="46"/><circle class="dot3" cx="66" cy="62" r="3.4"/><text class="ink" x="76" y="66" font-size="11" text-anchor="start">izdüşüm</text><line class="curve2" x1="60" y1="80" x2="86" y2="80"/><text class="ink" x="92" y="84" font-size="11" text-anchor="start">hata (atılan bilgi)</text></svg>
  <figcaption>Noktalar (mor) 1. bileşen doğrusuna dik olarak izdüşürülüyor; izdüşümler yeşil. Turuncu parçalar izdüşümde kaybolan kısım. PCA'nın seçtiği doğru, bu parçaların karelerinin toplamını en küçük yapan doğru.</figcaption>
</figure>

**Örnek.** Yukarıdaki $\Sigma$, $\bar{x} = (2, 3)$, $x = (5, 4)$ ve $k = 1$.
Merkezlenmiş nokta $(3, 1)$; $z = \frac{3 + 1}{\sqrt{2}} \approx 2{,}83$.
Geri çatma $\hat{x} = (2, 3) + 2{,}83 \cdot \frac{1}{\sqrt{2}}(1, 1) =
(4, 5)$. Hata $(1, -1)$, karesi $2$.

**İki bakış, tek cevap.** Varyansı en büyük yapmak ile geri çatma hatasını
en küçük yapmak aynı yönü verir. Pisagor: $\lVert x - \bar{x} \rVert^2 =
\lVert\text{izdüşüm}\rVert^2 + \lVert\text{hata}\rVert^2$; sol taraf sabit,
biri büyürken öteki küçülür. Ortalama kare geri çatma hatası, atılan
bileşenlerin özdeğerlerinin toplamıdır (örneklem kovaryansının $n - 1$
kuralıyla).

Not: Bu, regresyondan farklıdır. Regresyon $y$ yönündeki **dikey**
hataları küçültür; PCA doğruya **dik** uzaklıkları küçültür ve hedef
değişken diye bir şey yoktur.

## Kaç bileşen?

Her bileşenin **açıklanan varyans payı**
$\frac{\lambda_j}{\sum_i \lambda_i}$. Birikimli pay istenen düzeye (örneğin
yüzde $95$) ulaşana kadar bileşen eklenir.

<figure class="fig">
<svg viewBox="0 0 420 262" width="420"><line class="grid" x1="91.5" y1="216.0" x2="91.5" y2="26.0"/><line class="grid" x1="150.7" y1="216.0" x2="150.7" y2="26.0"/><line class="grid" x1="210.0" y1="216.0" x2="210.0" y2="26.0"/><line class="grid" x1="269.3" y1="216.0" x2="269.3" y2="26.0"/><line class="grid" x1="328.5" y1="216.0" x2="328.5" y2="26.0"/><line class="grid" x1="50.0" y1="216.0" x2="370.0" y2="216.0"/><line class="grid" x1="50.0" y1="179.8" x2="370.0" y2="179.8"/><line class="grid" x1="50.0" y1="143.6" x2="370.0" y2="143.6"/><line class="grid" x1="50.0" y1="107.4" x2="370.0" y2="107.4"/><line class="grid" x1="50.0" y1="71.2" x2="370.0" y2="71.2"/><line class="grid" x1="50.0" y1="35.0" x2="370.0" y2="35.0"/><line class="line" x1="50.0" y1="216.0" x2="370.0" y2="216.0"/><line class="curve3" stroke-dasharray="5 4" x1="50.0" y1="44.1" x2="370.0" y2="44.1"/><text class="dim" x="115.2" y="40.1" font-size="9" text-anchor="start">yüzde 95</text><rect class="dot" opacity="0.8" x="73.7" y="107.4" width="35.6" height="108.6"/><text class="ink" x="91.5" y="101.4" font-size="10" text-anchor="middle">0,60</text><text class="dim" x="91.5" y="230.0" font-size="10" text-anchor="middle">1</text><rect class="dot" opacity="0.8" x="133.0" y="170.8" width="35.5" height="45.2"/><text class="ink" x="150.7" y="164.8" font-size="10" text-anchor="middle">0,25</text><text class="dim" x="150.7" y="230.0" font-size="10" text-anchor="middle">2</text><rect class="dot" opacity="0.8" x="192.2" y="201.5" width="35.6" height="14.5"/><text class="ink" x="210.0" y="195.5" font-size="10" text-anchor="middle">0,08</text><text class="dim" x="210.0" y="230.0" font-size="10" text-anchor="middle">3</text><rect class="dot" opacity="0.8" x="251.5" y="208.8" width="35.5" height="7.2"/><text class="ink" x="269.3" y="202.8" font-size="10" text-anchor="middle">0,04</text><text class="dim" x="269.3" y="230.0" font-size="10" text-anchor="middle">4</text><rect class="dot" opacity="0.8" x="310.7" y="210.6" width="35.6" height="5.4"/><text class="ink" x="328.5" y="204.6" font-size="10" text-anchor="middle">0,03</text><text class="dim" x="328.5" y="230.0" font-size="10" text-anchor="middle">5</text><line class="curve2" x1="91.5" y1="107.4" x2="150.7" y2="62.2"/><line class="curve2" x1="150.7" y1="62.2" x2="210.0" y2="47.7"/><line class="curve2" x1="210.0" y1="47.7" x2="269.3" y2="40.5"/><line class="curve2" x1="269.3" y1="40.5" x2="328.5" y2="35.0"/><circle class="dot2" cx="91.5" cy="107.4" r="4"/><circle class="dot2" cx="150.7" cy="62.2" r="4"/><circle class="dot2" cx="210.0" cy="47.7" r="4"/><circle class="dot2" cx="269.3" cy="40.5" r="4"/><circle class="dot2" cx="328.5" cy="35.0" r="4"/><text class="ink" x="158.7" y="76.2" font-size="10" text-anchor="start">birikimli 0,85</text><text class="dim" x="46.0" y="182.8" font-size="9" text-anchor="end">0,2</text><text class="dim" x="46.0" y="146.6" font-size="9" text-anchor="end">0,4</text><text class="dim" x="46.0" y="110.4" font-size="9" text-anchor="end">0,6</text><text class="dim" x="46.0" y="74.2" font-size="9" text-anchor="end">0,8</text><text class="dim" x="46.0" y="38.0" font-size="9" text-anchor="end">1,0</text><text class="dim" x="370.0" y="244.0" font-size="10" text-anchor="end">bileşen</text><text class="dim" x="54.0" y="20.0" font-size="10" text-anchor="start">açıklanan varyans payı</text></svg>
  <figcaption>Özdeğerleri 6; 2,5; 0,8; 0,4; 0,3 olan beş özellikli bir veri. İlk iki bileşen varyansın yüzde 85'ini açıklıyor; yüzde 95'i geçmek için dört bileşen gerekiyor. Çubukların birden düştüğü "dirsek" de bir seçim ölçütü.</figcaption>
</figure>

## SVD ile hesaplamak

Merkezlenmiş veri matrisi $X$ ($n \times d$) için SVD bölümünde gördüğümüz
$X = U S V^\mathsf{T}$ ayrışımı doğrudan PCA'yı verir:

- $V$'nin sütunları temel bileşen yönleri.
- Özdeğerler $\lambda_j = \frac{s_j^2}{n - 1}$ ($s_j$ tekil değerler).
- Bileşen skorları $XV = US$.

Kütüphaneler kovaryans matrisini hiç kurmadan SVD kullanır; hem daha
kararlı hem de $d$ çok büyükken daha ucuz.

## Makine öğrenmesinde

- **Görselleştirme:** yüksek boyutlu veriyi ilk iki bileşene izdüşürüp
  çizmek.
- **Ön işleme:** çok sayıda ilişkili özelliği birkaç ilişkisiz bileşene
  indirmek; çoklu doğrusallığı giderir, eğitimi hızlandırır.
- **Sıkıştırma ve gürültü:** küçük özdeğerli bileşenler çoğu zaman
  gürültüdür; atmak veriyi temizler. Yüz görüntülerinin "özyüzler" ile
  anlatılması bunun ünlü bir örneği.
- **Beyazlatma:** skorları $\sqrt{\lambda_j}$'ye bölmek, birim varyanslı ve
  ilişkisiz özellikler üretir.

**Sınırları.** PCA doğrusaldır: veri eğri bir yüzey üzerindeyse doğrusal
yönler onu iyi anlatamaz (t-SNE, UMAP, otokodlayıcılar gibi doğrusal
olmayan yöntemler bu yüzden var). PCA hedefi görmez: en çok varyans taşıyan
yön, tahmin için en yararlı yön olmayabilir. Aykırı değerler kovaryansı,
dolayısıyla bileşenleri çarpıtır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>ortalamayı çıkarmadan PCA</p>
      <p>metre ve lira aynı tabloda, ölçeklemeden</p>
      <p>PCA regresyon doğrusunu bulur</p>
      <p>en büyük varyans = en önemli özellik</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>önce merkezle; gerekirse standartlaştır</p>
      <p>farklı birimlerde korelasyon matrisiyle çalış</p>
      <p>PCA dik uzaklıkları küçültür; hedef yok</p>
      <p>varyans, hedef için önem demek değil</p>
    </div>
  </div>
  <figcaption>PCA verinin kendi şeklini özetler; neyi tahmin edeceğimizi bilmez.</figcaption>
</figure>

- **Bileşenleri özellik gibi yorumlamak.** Her bileşen bütün özelliklerin
  bir karışımı; "1. bileşen = boy" demek çoğu zaman yanlıştır. Özvektörün
  elemanlarına (yüklere) bakmak gerekir.

## Özet

- Veriyi merkezle (gerekirse standartlaştır); kovaryans matrisi $\Sigma$.
- $u$ yönündeki varyans $u^\mathsf{T}\Sigma u$; en büyük yapan $u$, en büyük
  özdeğerin özvektörü.
- Temel bileşenler $\Sigma$'nın dik özvektörleri; varyansları özdeğerler.
- $z = U_k^\mathsf{T}(x - \bar{x})$, $\hat{x} = \bar{x} + U_k z$; varyansı en
  büyük yapmak = geri çatma hatasını en küçük yapmak.
- Açıklanan varyans payı $\frac{\lambda_j}{\sum\lambda_i}$; birikimli paya
  göre $k$ seçilir.
- SVD: yönler $V$'nin sütunları, $\lambda_j = \frac{s_j^2}{n - 1}$.
