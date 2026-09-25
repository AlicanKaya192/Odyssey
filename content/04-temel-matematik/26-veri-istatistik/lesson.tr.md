# Veri ve Temel İstatistik

İstatistik, bir yığın sayıyı birkaç anlamlı sayıya indirmenin yolu. Bin
öğrencinin notunu tek tek okumak yerine "ortalama $68$, çoğu $55$ ile $80$
arasında, birkaç tane çok düşük not var" demek, verinin neye benzediğini
anlatır. Makine öğrenmesinde her proje buradan başlar: bir sütunun
ortalamasına, yayılımına, aykırı değerlerine bakmadan model kurulmaz;
özellikleri aynı ölçeğe getirmek için de ortalama ve standart sapma
kullanılır. Bu bölümde veri türlerini, tablo ve grafiklerle özetlemeyi,
merkez ölçülerini (ortalama, ortanca, tepe değer), yayılım ölçülerini
(açıklık, çeyrekler, varyans, standart sapma), aykırı değerleri ve
standartlaştırmayı göreceğiz.

Ön bilgi: Ondalık Sayılar ve Yuvarlama, Köklü Sayılar, Diziler, Seriler ve
Σ Gösterimi.

## Veri türleri

| Tür | Anlamı | Örnek |
|---|---|---|
| sayısal, sürekli | ölçülür, her değeri alabilir | boy, sıcaklık, fiyat |
| sayısal, kesikli | sayılır, tam sayı | çocuk sayısı, tıklama |
| kategorik, sırasız | etiket, sırası yok | renk, şehir |
| kategorik, sıralı | etiket, sırası var | eğitim düzeyi, beden (S, M, L) |

Türü bilmek hangi özetin anlamlı olduğunu söyler: şehirlerin ortalaması
alınmaz ama en sık görüleni sayılır. Makine öğrenmesinde kategorik
sütunlar modele verilmeden önce sayıya çevrilir (Veri Bilimi patikasında
göreceğin kodlama işlemleri).

## Tablolar ve histogram

**Sıklık tablosu** her değerin ya da her aralığın kaç kez geçtiğini
gösterir. Sayısal veri aralıklara bölünüp çubuklarla çizilince
**histogram** olur.

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="67.5" y1="220.0" x2="67.5" y2="20.0"/><line class="grid" x1="111.2" y1="220.0" x2="111.2" y2="20.0"/><line class="grid" x1="155.0" y1="220.0" x2="155.0" y2="20.0"/><line class="grid" x1="198.8" y1="220.0" x2="198.8" y2="20.0"/><line class="grid" x1="242.5" y1="220.0" x2="242.5" y2="20.0"/><line class="grid" x1="286.2" y1="220.0" x2="286.2" y2="20.0"/><line class="grid" x1="330.0" y1="220.0" x2="330.0" y2="20.0"/><line class="grid" x1="373.8" y1="220.0" x2="373.8" y2="20.0"/><line class="grid" x1="50.0" y1="220.0" x2="400.0" y2="220.0"/><line class="grid" x1="50.0" y1="191.4" x2="400.0" y2="191.4"/><line class="grid" x1="50.0" y1="162.9" x2="400.0" y2="162.9"/><line class="grid" x1="50.0" y1="134.3" x2="400.0" y2="134.3"/><line class="grid" x1="50.0" y1="105.7" x2="400.0" y2="105.7"/><line class="grid" x1="50.0" y1="77.1" x2="400.0" y2="77.1"/><line class="grid" x1="50.0" y1="48.6" x2="400.0" y2="48.6"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="220.0" x2="400.0" y2="220.0"/><line class="line" x1="50.0" y1="220.0" x2="50.0" y2="20.0"/><text class="dim" x="67.5" y="233.0" font-size="9" text-anchor="middle">150</text><text class="dim" x="111.2" y="233.0" font-size="9" text-anchor="middle">155</text><text class="dim" x="155.0" y="233.0" font-size="9" text-anchor="middle">160</text><text class="dim" x="198.8" y="233.0" font-size="9" text-anchor="middle">165</text><text class="dim" x="242.5" y="233.0" font-size="9" text-anchor="middle">170</text><text class="dim" x="286.2" y="233.0" font-size="9" text-anchor="middle">175</text><text class="dim" x="330.0" y="233.0" font-size="9" text-anchor="middle">180</text><text class="dim" x="373.8" y="233.0" font-size="9" text-anchor="middle">185</text><text class="dim" x="45.0" y="194.4" font-size="9" text-anchor="end">2</text><text class="dim" x="45.0" y="137.3" font-size="9" text-anchor="end">6</text><text class="dim" x="45.0" y="80.1" font-size="9" text-anchor="end">10</text><text class="dim" x="45.0" y="23.0" font-size="9" text-anchor="end">14</text><rect class="dot" opacity="0.6" x="70.1" y="191.4" width="38.5" height="28.6"/><text class="ink" x="89.4" y="187.4" font-size="10" text-anchor="middle">2</text><rect class="dot" opacity="0.6" x="113.9" y="148.6" width="38.5" height="71.4"/><text class="ink" x="133.1" y="144.6" font-size="10" text-anchor="middle">5</text><rect class="dot" opacity="0.6" x="157.6" y="91.4" width="38.5" height="128.6"/><text class="ink" x="176.9" y="87.4" font-size="10" text-anchor="middle">9</text><rect class="dot" opacity="0.6" x="201.4" y="48.6" width="38.5" height="171.4"/><text class="ink" x="220.6" y="44.6" font-size="10" text-anchor="middle">12</text><rect class="dot" opacity="0.6" x="245.1" y="77.1" width="38.5" height="142.9"/><text class="ink" x="264.4" y="73.1" font-size="10" text-anchor="middle">10</text><rect class="dot" opacity="0.6" x="288.9" y="134.3" width="38.5" height="85.7"/><text class="ink" x="308.1" y="130.3" font-size="10" text-anchor="middle">6</text><rect class="dot" opacity="0.6" x="332.6" y="177.1" width="38.5" height="42.9"/><text class="ink" x="351.9" y="173.1" font-size="10" text-anchor="middle">3</text><text class="dim" x="400.0" y="214.0" font-size="10" text-anchor="end">boy (cm)</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">öğrenci sayısı</text></svg>
  <figcaption>47 öğrencinin boyu 5 cm'lik aralıklarda. En kalabalık aralık 165–170 (12 öğrenci); uçlara doğru sayı azalıyor ve şekil kabaca simetrik bir tepe.</figcaption>
</figure>

Histogramdan üç şey okunur: **merkez** (değerler nerede toplanmış),
**yayılım** (ne kadar geniş alana dağılmış) ve **şekil** (simetrik mi, bir
yana mı çarpık, birden çok tepesi var mı).

## Merkez ölçüleri

**Ortalama** bütün değerlerin toplamı bölü değer sayısı:

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

**Ortanca (medyan)** değerler sıralanınca tam ortadaki değer; değer sayısı
çiftse ortadaki iki değerin ortalaması. **Tepe değer (mod)** en sık geçen
değer.

Bir şirkette $7$ çalışanın aylık maaşı (bin TL): $20, 22, 25, 25, 28, 30,
150$. Ortalama $\frac{300}{7} \approx 42{,}9$; ortanca $25$ (dördüncü
değer); tepe değer $25$.

<figure class="fig">
<svg viewBox="0 0 440 172" width="440"><line class="grid" x1="30.0" y1="140.0" x2="30.0" y2="30.0"/><line class="grid" x1="77.5" y1="140.0" x2="77.5" y2="30.0"/><line class="grid" x1="125.0" y1="140.0" x2="125.0" y2="30.0"/><line class="grid" x1="172.5" y1="140.0" x2="172.5" y2="30.0"/><line class="grid" x1="220.0" y1="140.0" x2="220.0" y2="30.0"/><line class="grid" x1="267.5" y1="140.0" x2="267.5" y2="30.0"/><line class="grid" x1="315.0" y1="140.0" x2="315.0" y2="30.0"/><line class="grid" x1="362.5" y1="140.0" x2="362.5" y2="30.0"/><line class="grid" x1="410.0" y1="140.0" x2="410.0" y2="30.0"/><line class="grid" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="30.0" y2="30.0"/><text class="dim" x="77.5" y="153.0" font-size="9" text-anchor="middle">20</text><text class="dim" x="125.0" y="153.0" font-size="9" text-anchor="middle">40</text><text class="dim" x="172.5" y="153.0" font-size="9" text-anchor="middle">60</text><text class="dim" x="220.0" y="153.0" font-size="9" text-anchor="middle">80</text><text class="dim" x="267.5" y="153.0" font-size="9" text-anchor="middle">100</text><text class="dim" x="315.0" y="153.0" font-size="9" text-anchor="middle">120</text><text class="dim" x="362.5" y="153.0" font-size="9" text-anchor="middle">140</text><text class="dim" x="410.0" y="153.0" font-size="9" text-anchor="middle">160</text><circle class="dot" cx="77.5" cy="121.7" r="6"/><circle class="dot" cx="82.2" cy="121.7" r="6"/><circle class="dot" cx="89.4" cy="121.7" r="6"/><circle class="dot" cx="89.4" cy="101.5" r="6"/><circle class="dot" cx="96.5" cy="121.7" r="6"/><circle class="dot" cx="101.2" cy="121.7" r="6"/><circle class="dot" cx="386.2" cy="121.7" r="6"/><line class="curve4" stroke-dasharray="5 4" x1="89.4" y1="140.0" x2="89.4" y2="44.7"/><line class="curve2" stroke-dasharray="5 4" x1="131.8" y1="140.0" x2="131.8" y2="44.7"/><text class="ink" x="85.4" y="40.7" font-size="11" text-anchor="end">ortanca 25</text><text class="ink" x="135.8" y="40.7" font-size="11" text-anchor="start">ortalama ≈ 42,9</text><text class="dim" x="410.0" y="168.0" font-size="10" text-anchor="end">maaş (bin TL)</text></svg>
  <figcaption>Altı maaş 20 ile 30 arasında, biri 150. Ortalama tek aykırı değerin etkisiyle 42,9'a çekiliyor; çalışanların hiçbiri bu kadar kazanmıyor. Ortanca 25'te kalıyor.</figcaption>
</figure>

**Hangisi ne zaman?** Ortalama her değeri hesaba katar, bu yüzden aykırı
değerlere duyarlıdır. Ortanca yalnızca sıraya bakar ve aykırı değerden
etkilenmez. Maaş, ev fiyatı gibi bir yana çarpık verilerde "tipik değer"
için ortanca daha dürüsttür. Tepe değer kategorik verinin tek merkez
ölçüsüdür.

## Yayılım ölçüleri

Aynı ortalamalı iki veri çok farklı olabilir.

<figure class="fig">
<svg viewBox="0 0 440 182" width="440"><line class="grid" x1="30.0" y1="140.0" x2="30.0" y2="20.0"/><line class="grid" x1="68.0" y1="140.0" x2="68.0" y2="20.0"/><line class="grid" x1="106.0" y1="140.0" x2="106.0" y2="20.0"/><line class="grid" x1="144.0" y1="140.0" x2="144.0" y2="20.0"/><line class="grid" x1="182.0" y1="140.0" x2="182.0" y2="20.0"/><line class="grid" x1="220.0" y1="140.0" x2="220.0" y2="20.0"/><line class="grid" x1="258.0" y1="140.0" x2="258.0" y2="20.0"/><line class="grid" x1="296.0" y1="140.0" x2="296.0" y2="20.0"/><line class="grid" x1="334.0" y1="140.0" x2="334.0" y2="20.0"/><line class="grid" x1="372.0" y1="140.0" x2="372.0" y2="20.0"/><line class="grid" x1="410.0" y1="140.0" x2="410.0" y2="20.0"/><line class="grid" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="410.0" y2="140.0"/><line class="line" x1="30.0" y1="140.0" x2="30.0" y2="20.0"/><text class="dim" x="68.0" y="153.0" font-size="9" text-anchor="middle">30</text><text class="dim" x="144.0" y="153.0" font-size="9" text-anchor="middle">40</text><text class="dim" x="220.0" y="153.0" font-size="9" text-anchor="middle">50</text><text class="dim" x="296.0" y="153.0" font-size="9" text-anchor="middle">60</text><text class="dim" x="372.0" y="153.0" font-size="9" text-anchor="middle">70</text><line class="curve3" stroke-dasharray="5 4" x1="220.0" y1="140.0" x2="220.0" y2="20.0"/><circle class="dot" cx="204.8" cy="56.0" r="6"/><circle class="dot" cx="212.4" cy="56.0" r="6"/><circle class="dot" cx="220.0" cy="56.0" r="6"/><circle class="dot" cx="227.6" cy="56.0" r="6"/><circle class="dot" cx="235.2" cy="56.0" r="6"/><circle class="dot2" cx="68.0" cy="104.0" r="6"/><circle class="dot2" cx="144.0" cy="104.0" r="6"/><circle class="dot2" cx="220.0" cy="104.0" r="6"/><circle class="dot2" cx="296.0" cy="104.0" r="6"/><circle class="dot2" cx="372.0" cy="104.0" r="6"/><text class="ink" x="34.0" y="44.0" font-size="11" text-anchor="start">A: standart sapma ≈ 1,4</text><text class="ink" x="34.0" y="92.0" font-size="11" text-anchor="start">B: standart sapma ≈ 14,1</text><text class="ink" x="220" y="170" font-size="12" text-anchor="middle">ikisinin de ortalaması 50</text></svg>
  <figcaption>A kümesi 48 ile 52 arasında sıkışık, B kümesi 30 ile 70 arasında dağınık. İkisinin ortalaması da 50; farkı yalnızca yayılım ölçüsü gösteriyor.</figcaption>
</figure>

**Açıklık** en büyük eksi en küçük. Basit ama yalnızca iki uç değere bakar;
tek bir aykırı değer onu büyütür.

**Varyans** değerlerin ortalamadan sapmalarının karelerinin ortalaması:

$$
\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2
$$

**Standart sapma** varyansın karekökü, $\sigma$; verinin kendi biriminde
"değerler ortalamadan tipik olarak ne kadar uzak" sorusunun cevabı.

**Örnek.** $2, 4, 4, 4, 5, 5, 7, 9$: ortalama $\frac{40}{8} = 5$.

| $x_i$ | $2$ | $4$ | $4$ | $4$ | $5$ | $5$ | $7$ | $9$ |
|---|---|---|---|---|---|---|---|---|
| $x_i - \bar{x}$ | $-3$ | $-1$ | $-1$ | $-1$ | $0$ | $0$ | $2$ | $4$ |
| $(x_i - \bar{x})^2$ | $9$ | $1$ | $1$ | $1$ | $0$ | $0$ | $4$ | $16$ |

Karelerin toplamı $32$; varyans $\frac{32}{8} = 4$, standart sapma $2$.

**Neden kare?** Sapmaların kendisini toplamak her zaman $0$ verir:
ortalamanın üstündekiler altındakileri tam götürür. Kare, işareti yok
eder. Karesi alındığı için birim de karelenir; karekök birimi geri getirir.

**Örneklem için $n - 1$.** Veri bütün topluluk değil de ondan alınmış bir
örneklemse varyans $\frac{1}{n - 1} \sum (x_i - \bar{x})^2$ ile
hesaplanır: $\frac{32}{7} \approx 4{,}57$. Örneklemin ortalaması
verilere topluluğun ortalamasından daha yakın düştüğü için bölen biraz
küçültülüp düzeltilir. Veri büyüdükçe fark önemsizleşir; nedenini MAT
2'deki Örnekleme bölümü anlatır.

## Çeyrekler ve kutu grafiği

Sıralı veriyi dört eşit parçaya bölen üç sayı: **birinci çeyrek** Ç1,
**ortanca** ve **üçüncü çeyrek** Ç3. Bu bölümde çeyrekleri şöyle
buluyoruz: ortanca veriyi iki yarıya böler; Ç1 alt yarının, Ç3 üst yarının
ortancasıdır. (Programlar biraz farklı yöntemler kullanabilir; sonuçlar
birbirine yakın çıkar.)

**Çeyrekler açıklığı** $\text{ÇAA} = \text{Ç3} - \text{Ç1}$: verinin ortadaki
yarısının genişliği. Açıklık gibi uçlara bakmadığı için aykırı değerden
etkilenmez.

**Örnek.** $3, 5, 7, 8, 9, 11, 13, 15, 20, 40$: ortanca
$\frac{9 + 11}{2} = 10$; alt yarı $3, 5, 7, 8, 9$, Ç1 $= 7$; üst yarı
$11, 13, 15, 20, 40$, Ç3 $= 15$. $\text{ÇAA} = 8$.

**Aykırı değer kuralı.** Ç1'in $1{,}5 \cdot \text{ÇAA}$ altı ya da Ç3'ün
$1{,}5 \cdot \text{ÇAA}$ üstü aykırı sayılır. Burada üst sınır
$15 + 12 = 27$, alt sınır $7 - 12 = -5$: $40$ aykırı.

<figure class="fig">
<svg viewBox="0 0 440 146" width="440"><line class="grid" x1="30.0" y1="130.0" x2="30.0" y2="30.0"/><line class="grid" x1="73.2" y1="130.0" x2="73.2" y2="30.0"/><line class="grid" x1="116.4" y1="130.0" x2="116.4" y2="30.0"/><line class="grid" x1="159.5" y1="130.0" x2="159.5" y2="30.0"/><line class="grid" x1="202.7" y1="130.0" x2="202.7" y2="30.0"/><line class="grid" x1="245.9" y1="130.0" x2="245.9" y2="30.0"/><line class="grid" x1="289.1" y1="130.0" x2="289.1" y2="30.0"/><line class="grid" x1="332.3" y1="130.0" x2="332.3" y2="30.0"/><line class="grid" x1="375.5" y1="130.0" x2="375.5" y2="30.0"/><line class="grid" x1="30.0" y1="130.0" x2="410.0" y2="130.0"/><line class="line" x1="30.0" y1="130.0" x2="410.0" y2="130.0"/><line class="line" x1="30.0" y1="130.0" x2="30.0" y2="30.0"/><text class="dim" x="73.2" y="143.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="116.4" y="143.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="159.5" y="143.0" font-size="9" text-anchor="middle">15</text><text class="dim" x="202.7" y="143.0" font-size="9" text-anchor="middle">20</text><text class="dim" x="245.9" y="143.0" font-size="9" text-anchor="middle">25</text><text class="dim" x="289.1" y="143.0" font-size="9" text-anchor="middle">30</text><text class="dim" x="332.3" y="143.0" font-size="9" text-anchor="middle">35</text><text class="dim" x="375.5" y="143.0" font-size="9" text-anchor="middle">40</text><rect class="dot" opacity="0.35" x="90.5" y="62.5" width="69.0" height="35.0"/><rect class="curve" fill="none" x="90.5" y="62.5" width="69.0" height="35.0"/><line class="curve2" stroke-width="3" x1="116.4" y1="97.5" x2="116.4" y2="62.5"/><line class="curve" x1="55.9" y1="80.0" x2="90.5" y2="80.0"/><line class="curve" x1="159.5" y1="80.0" x2="202.7" y2="80.0"/><line class="curve" x1="55.9" y1="90.0" x2="55.9" y2="70.0"/><line class="curve" x1="202.7" y1="90.0" x2="202.7" y2="70.0"/><line class="curve3" stroke-dasharray="5 4" x1="263.2" y1="110.0" x2="263.2" y2="50.0"/><circle class="dot2" cx="375.5" cy="80.0" r="6"/><text class="dim" x="55.9" y="62.0" font-size="10" text-anchor="middle">en küçük</text><text class="ink" x="90.5" y="113.5" font-size="10" text-anchor="middle">Ç1 = 7</text><text class="ink" x="116.4" y="54.5" font-size="10" text-anchor="middle">ortanca 10</text><text class="ink" x="159.5" y="113.5" font-size="10" text-anchor="middle">Ç3 = 15</text><text class="dim" x="263.2" y="44.0" font-size="10" text-anchor="middle">sınır 27</text><text class="ink" x="375.5" y="68.0" font-size="10" text-anchor="middle">aykırı 40</text><text class="dim" x="125.0" y="37.5" font-size="10" text-anchor="middle">ÇAA = 8</text></svg>
  <figcaption>Kutu Ç1'den Ç3'e uzanıyor, içindeki çizgi ortanca. Bıyıklar sınırın içindeki en uç değerlere (3 ve 20) kadar gidiyor. 40, 27'deki sınırın dışında; ayrı bir nokta olarak çiziliyor.</figcaption>
</figure>

## Standartlaştırma

Farklı ölçeklerdeki sayıları karşılaştırmak için her değer, ortalamadan
kaç standart sapma uzakta olduğuyla yazılır. Buna **z puanı** denir:

$$
z = \frac{x - \bar{x}}{\sigma}
$$

Ortalaması $70$, standart sapması $10$ olan bir sınavda $85$ alan kişinin
z puanı $1{,}5$. Ortalaması $60$, standart sapması $5$ olan başka bir
sınavda $70$ alanınki $2$: ikinci sınavda daha iyi, çünkü kendi sınıfının
daha üstünde.

Standartlaştırılmış bir sütunun ortalaması $0$, standart sapması $1$ olur.

**Min–maks ölçekleme** değerleri $0$ ile $1$ arasına sıkıştırır:
$x' = \frac{x - \min}{\max - \min}$.

## Makine öğrenmesinde istatistik

**Veriyi tanımak.** Veri Bilimi patikasında göreceğin `describe` benzeri
özetler her sütun için sayıyı, ortalamayı, standart sapmayı, en küçüğü,
çeyrekleri ve en büyüğü verir; bu bölümdeki her sayı orada.

**Ölçekleme.** Metrekaresi yüzlerle, oda sayısı birlerle ölçülen iki
özellik uzaklık hesaplayan yöntemlerde (k en yakın komşu, k-means) ve
gradyan inişinde dengesiz davranır. Z puanıyla standartlaştırma ya da
min–maks ölçekleme bunu düzeltir. Ortalama ve standart sapma **yalnızca
eğitim verisinden** hesaplanır ve test verisine aynen uygulanır; yoksa
test verisinden bilgi sızar.

**Aykırı değerler.** Ortalama kare hata (MSE) sapmaların karesini aldığı
için aykırı değerlere çok duyarlıdır, ortanca gibi davranan ortalama mutlak
hata (MAE) daha az. Aykırı değer bir ölçüm hatasıysa temizlenir, gerçekse
modele öğretilmesi gereken bir durumdur.

**Dengesiz sınıflar.** Örneklerin yüzde $98$'i "normal" olan bir veride
her şeye "normal" diyen model yüzde $98$ doğruluk alır ama hiçbir şey
öğrenmemiştir. Sınıfların sıklık tablosuna bakmak bunu önceden gösterir.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>çarpık veride tipik değer = ortalama</p>
      <p>ortancayı sıralamadan almak</p>
      <p>$\sigma = \sum (x_i - \bar{x}) / n$</p>
      <p>ölçeklemeyi bütün veriyle hesaplamak</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>çarpık veride ortanca daha temsilî</p>
      <p>önce sırala, sonra ortadakini al</p>
      <p>sapmaların karesi, sonra karekök</p>
      <p>yalnızca eğitim verisinden hesapla</p>
    </div>
  </div>
  <figcaption>Aykırı değer ortalamayı ve standart sapmayı çeker, ortancayı ve çeyrekler açıklığını çekmez.</figcaption>
</figure>

- **Kategorik veriye ortalama almak.** Şehir kodlarının ortalaması bir şey
  anlatmaz; tepe değer ya da sıklık tablosu kullanılır.
- **Standart sapmayı varyansla karıştırmak.** Varyansın birimi karelenmiş
  birim; standart sapma verinin kendi biriminde.

## Özet

- Veri sayısal (sürekli, kesikli) ya da kategorik (sırasız, sıralı).
- Histogram merkezi, yayılımı ve şekli gösterir.
- Ortalama $\bar{x} = \frac{1}{n} \sum x_i$; ortanca sıralı verinin ortası;
  tepe değer en sık değer. Aykırı değer ortalamayı çeker, ortancayı çekmez.
- Varyans $\frac{1}{n} \sum (x_i - \bar{x})^2$, standart sapma karekökü;
  örneklemde $n - 1$.
- Çeyrekler ve ÇAA; $1{,}5 \cdot \text{ÇAA}$ kuralı aykırıları gösterir;
  kutu grafiği bunları çizer.
- $z = \frac{x - \bar{x}}{\sigma}$ ölçekleri eşitler; ölçekleme eğitim
  verisinden hesaplanır.
