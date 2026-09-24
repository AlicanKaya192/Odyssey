# Kesirler

Bir pizzanın dörtte üçü, bir sınıfın beşte ikisi, bir veri setinin
yüzde sekseni… Bütünün bir **parçasını** anlatmak için kesirleri
kullanıyoruz. Olasılıklar, oranlar, ortalamalar ve makine öğrenmesindeki
pek çok sayı aslında birer kesir. Bu bölümde kesrin ne olduğunu, denk
kesirleri, sadeleştirmeyi ve dört işlemi **neden** öyle yapıldığıyla
birlikte göreceğiz.

Ön bilgi: Bölünebilme, Asal Sayılar, EBOB ve EKOK bölümü.

## Kesir nedir?

$\dfrac{a}{b}$ kesri, bir bütünü $b$ eşit parçaya bölüp bunlardan $a$
tanesini almak demek. Üstteki sayı **pay**, alttaki **payda**:

$$
\frac{3}{4} \quad \leftarrow \quad \begin{aligned} &\text{pay: kaç parça alındı} \\ &\text{payda: bütün kaç parçaya bölündü} \end{aligned}
$$

Kesir aynı zamanda bir **bölmedir**: $\dfrac{3}{4} = 3 \div 4$. Bu yüzden
payda **sıfır olamaz**; sıfıra bölme tanımsızdı.

**Kesir çeşitleri:**

| Çeşit | Anlamı | Örnek |
|---|---|---|
| Basit kesir | pay paydadan küçük, değeri $1$'den az | $\dfrac{3}{4}$ |
| Bileşik kesir | pay paydaya eşit ya da büyük | $\dfrac{7}{3}$ |
| Tam sayılı kesir | bir tam sayı ile bir basit kesir | $2\tfrac{1}{3}$ |

Bileşik kesirle tam sayılı kesir aynı sayının iki yazılışı. $7 \div 3 =
2$, kalan $1$: yani $\dfrac{7}{3} = 2\tfrac{1}{3}$. Geri çevirmek için
$2\tfrac{1}{3} = \dfrac{2 \cdot 3 + 1}{3} = \dfrac{7}{3}$.

Her tam sayı paydası $1$ olan bir kesir: $5 = \dfrac{5}{1}$.

## Denk kesirler ve sadeleştirme

<figure class="fig">
<svg viewBox="0 0 520 158" width="520"><rect class="dot" opacity="0.55" x="70.0" y="16" width="75.0" height="34"/><rect class="curve3" x="70.0" y="16" width="75.0" height="34"/><rect class="dot" opacity="0.55" x="145.0" y="16" width="75.0" height="34"/><rect class="curve3" x="145.0" y="16" width="75.0" height="34"/><rect class="dot" opacity="0.55" x="220.0" y="16" width="75.0" height="34"/><rect class="curve3" x="220.0" y="16" width="75.0" height="34"/><rect class="curve3" x="295.0" y="16" width="75.0" height="34"/><text class="ink" x="56" y="39.0" font-size="15" text-anchor="end">3/4</text><text class="dim" x="380" y="38.0" font-size="11" text-anchor="start">4 eşit parçadan 3'ü</text><rect class="dot" opacity="0.55" x="70.0" y="76" width="37.5" height="34"/><rect class="curve3" x="70.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="107.5" y="76" width="37.5" height="34"/><rect class="curve3" x="107.5" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="145.0" y="76" width="37.5" height="34"/><rect class="curve3" x="145.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="182.5" y="76" width="37.5" height="34"/><rect class="curve3" x="182.5" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="220.0" y="76" width="37.5" height="34"/><rect class="curve3" x="220.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="257.5" y="76" width="37.5" height="34"/><rect class="curve3" x="257.5" y="76" width="37.5" height="34"/><rect class="curve3" x="295.0" y="76" width="37.5" height="34"/><rect class="curve3" x="332.5" y="76" width="37.5" height="34"/><text class="ink" x="56" y="99.0" font-size="15" text-anchor="end">6/8</text><text class="dim" x="380" y="98.0" font-size="11" text-anchor="start">8 eşit parçadan 6'sı</text><line class="curve2" stroke-dasharray="4 3" x1="295.0" y1="8" x2="295.0" y2="118"/><text class="ink" x="220.0" y="146" font-size="13" text-anchor="middle">aynı uzunluk: 3/4 = 6/8</text></svg>
  <figcaption>Üstteki çubuk $4$ parçaya bölünmüş, $3$'ü boyalı; alttaki $8$ parçaya bölünmüş, $6$'sı boyalı. Boyalı uzunluk aynı: $\tfrac{3}{4}$ ile $\tfrac{6}{8}$ aynı sayı. Her parçayı ikiye bölmek hem payı hem paydayı ikiyle çarptı.</figcaption>
</figure>

Pay ve paydayı **aynı sayıyla** (sıfır hariç) çarpmak ya da bölmek
kesrin değerini değiştirmez:

$$
\frac{a}{b} = \frac{a \cdot k}{b \cdot k}
$$

Genişletmek (çarpmak) kesirleri ortak paydaya getirmek için,
**sadeleştirmek** (bölmek) sayıları küçültmek için kullanılır. En sade
hâl için pay ve paydayı **EBOB'larına** böl:

$$
\frac{84}{126} = \frac{84 \div 42}{126 \div 42} = \frac{2}{3}
$$

EBOB'u hemen göremiyorsan adım adım da sadeleştirebilirsin: önce $2$'ye,
sonra $3$'e, sonra $7$'ye. Sonuç aynı.

## Kesirleri karşılaştırmak

- **Paydalar aynıysa** payı büyük olan büyük: $\dfrac{5}{8} > \dfrac{3}{8}$.
- **Paylar aynıysa** paydası küçük olan büyük: $\dfrac{3}{4} >
  \dfrac{3}{5}$ (bütünü daha az parçaya bölünce her parça daha büyük).
- **Genel yol:** ortak paydaya getir ya da **çapraz çarp**.

$$
\frac{5}{7} \;\; ? \;\; \frac{2}{3} \qquad 5 \cdot 3 = 15, \quad 2 \cdot 7 = 14 \qquad 15 > 14 \;\Rightarrow\; \frac{5}{7} > \frac{2}{3}
$$

Çapraz çarpma aslında ortak payda $21$'e getirmek: $\dfrac{15}{21}$ ile
$\dfrac{14}{21}$'i karşılaştırıyoruz.

## Toplama ve çıkarma

Paydalar aynıysa payları topla, paydayı koru: $\dfrac{2}{7} + \dfrac{3}{7}
= \dfrac{5}{7}$. Aynı büyüklükteki parçaları sayıyoruz.

Paydalar farklıysa parçalar farklı büyüklükte; önce **ortak paydaya**
getirmek gerekiyor.

<figure class="fig">
<svg viewBox="0 0 480 282" width="480"><rect class="dot" opacity="0.55" x="70.0" y="14" width="150.0" height="34"/><rect class="curve3" x="70.0" y="14" width="150.0" height="34"/><rect class="curve3" x="220.0" y="14" width="150.0" height="34"/><text class="ink" x="56" y="37.0" font-size="15" text-anchor="end">1/2</text><rect class="dot2" opacity="0.55" x="70.0" y="60" width="100.0" height="34"/><rect class="curve3" x="70.0" y="60" width="100.0" height="34"/><rect class="curve3" x="170.0" y="60" width="100.0" height="34"/><rect class="curve3" x="270.0" y="60" width="100.0" height="34"/><text class="ink" x="56" y="83.0" font-size="15" text-anchor="end">1/3</text><text class="dim" x="220.0" y="118" font-size="12" text-anchor="middle">↓ altıda birlere böl</text><rect class="dot" opacity="0.55" x="70.0" y="132" width="50.0" height="34"/><rect class="curve3" x="70.0" y="132" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="120.0" y="132" width="50.0" height="34"/><rect class="curve3" x="120.0" y="132" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="170.0" y="132" width="50.0" height="34"/><rect class="curve3" x="170.0" y="132" width="50.0" height="34"/><rect class="curve3" x="220.0" y="132" width="50.0" height="34"/><rect class="curve3" x="270.0" y="132" width="50.0" height="34"/><rect class="curve3" x="320.0" y="132" width="50.0" height="34"/><text class="ink" x="56" y="155.0" font-size="15" text-anchor="end">3/6</text><rect class="dot2" opacity="0.55" x="70.0" y="178" width="50.0" height="34"/><rect class="curve3" x="70.0" y="178" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="120.0" y="178" width="50.0" height="34"/><rect class="curve3" x="120.0" y="178" width="50.0" height="34"/><rect class="curve3" x="170.0" y="178" width="50.0" height="34"/><rect class="curve3" x="220.0" y="178" width="50.0" height="34"/><rect class="curve3" x="270.0" y="178" width="50.0" height="34"/><rect class="curve3" x="320.0" y="178" width="50.0" height="34"/><text class="ink" x="56" y="201.0" font-size="15" text-anchor="end">2/6</text><rect class="dot" opacity="0.55" x="70.0" y="236" width="50.0" height="34"/><rect class="curve3" x="70.0" y="236" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="120.0" y="236" width="50.0" height="34"/><rect class="curve3" x="120.0" y="236" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="170.0" y="236" width="50.0" height="34"/><rect class="curve3" x="170.0" y="236" width="50.0" height="34"/><rect class="curve3" x="220.0" y="236" width="50.0" height="34"/><rect class="curve3" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="320.0" y="236" width="50.0" height="34"/><rect class="curve3" x="70.0" y="236" width="50.0" height="34"/><rect class="curve3" x="120.0" y="236" width="50.0" height="34"/><rect class="curve3" x="170.0" y="236" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="220.0" y="236" width="50.0" height="34"/><rect class="curve3" x="220.0" y="236" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="320.0" y="236" width="50.0" height="34"/><text class="ink" x="56" y="259.0" font-size="15" text-anchor="end">5/6</text><text class="dim" x="382" y="258.0" font-size="12" text-anchor="start">= 3/6 + 2/6</text></svg>
  <figcaption>Yarım ile üçte bir doğrudan toplanamaz, parçalar farklı büyüklükte. İkisini de altıda birlere bölünce yarım $3$, üçte bir $2$ parça ediyor; toplam $5$ altıda bir.</figcaption>
</figure>

$$
\frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} = \frac{5}{6}
$$

En uygun ortak payda, paydaların **EKOK'u**. $\dfrac{5}{12} + \dfrac{7}{18}$
için $\text{EKOK}(12, 18) = 36$:

$$
\frac{5}{12} + \frac{7}{18} = \frac{15}{36} + \frac{14}{36} = \frac{29}{36}
$$

Paydaları çarpmak ($12 \cdot 18 = 216$) da doğru sonuç verir ama sayılar
büyür ve sonunda sadeleştirmen gerekir.

**Tam sayılı kesirlerde** ya bileşik kesre çevir ya tam kısımları ve
kesir kısımları ayrı topla: $2\tfrac{1}{3} + 1\tfrac{1}{2} = 3 +
\tfrac{5}{6} = 3\tfrac{5}{6}$.

## Çarpma

Payları çarp, paydaları çarp:

$$
\frac{a}{b} \cdot \frac{c}{d} = \frac{a \cdot c}{b \cdot d}
$$

$\dfrac{2}{3} \cdot \dfrac{3}{4}$: "dörtte üçün üçte ikisi". Bir kareyi
yatayda $4$'e, dikeyde $3$'e bölünce $12$ küçük parça çıkar; $3$ sütunun
$2$ satırı $6$ parça: $\dfrac{6}{12} = \dfrac{1}{2}$.

**Önce sadeleştir, sonra çarp.** Çarpmadan önce bir paydaki ve bir
paydadaki ortak çarpanları sadeleştirmek hesabı küçültür:

$$
\frac{2}{3} \cdot \frac{3}{4} = \frac{2 \cdot \cancel{3}}{\cancel{3} \cdot 4} = \frac{2}{4} = \frac{1}{2}
$$

**"Kesri" = "çarpı".** "$12$'nin $\dfrac{2}{3}$'ü" demek $\dfrac{2}{3}
\cdot 12 = 8$ demek: $12$'yi $3$'e böl ($4$), $2$ tanesini al ($8$).

## Bölme

Bir kesre bölmek, onun **tersiyle** çarpmaktır:

$$
\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c}
$$

Neden? $3 \div \dfrac{1}{4}$ sorusu "$3$'ün içinde kaç tane çeyrek var?"
Her bütünde $4$ çeyrek, $3$ bütünde $12$: $3 \div \dfrac{1}{4} = 3 \cdot 4
= 12$. Küçük bir sayıya bölmek sonucu **büyütür**.

$$
\frac{3}{4} \div \frac{9}{8} = \frac{3}{4} \cdot \frac{8}{9} = \frac{24}{36} = \frac{2}{3}
$$

**Sağlama:** $\dfrac{2}{3} \cdot \dfrac{9}{8} = \dfrac{18}{24} =
\dfrac{3}{4}$ ✓. Bölme çarpmanın tersiydi.

## Kesirlerde işlem önceliği

Kurallar değişmiyor: parantez, üs, çarpma ve bölme, toplama ve çıkarma.
Kesir çizgisi bir parantez gibi davranır: üstü ve altı ayrı ayrı
hesaplanır.

$$
\begin{aligned}
\frac{1}{2} + \frac{2}{3} \cdot \frac{9}{4} &= \frac{1}{2} + \frac{3}{2} \\
&= \frac{4}{2} = 2
\end{aligned}
$$

Önce çarpma ($\tfrac{2}{3} \cdot \tfrac{9}{4} = \tfrac{18}{12} = \tfrac{3}{2}$), sonra toplama.

## Makine öğrenmesinde kesirler

**Doğruluk.** $60$ örneğin $45$'ini doğru tahmin eden bir modelin
doğruluğu $\dfrac{45}{60} = \dfrac{3}{4}$.

**Olasılıklar.** Bir sınıflandırıcı üç sınıf için $\dfrac{1}{2}$,
$\dfrac{1}{3}$ ve $\dfrac{1}{6}$ olasılık verebilir. Olasılıkların
toplamı $1$ olmalı: $\dfrac{3}{6} + \dfrac{2}{6} + \dfrac{1}{6} = 1$ ✓.

**Veri bölme.** Verinin $\dfrac{4}{5}$'i eğitime, $\dfrac{1}{5}$'i teste
ayrılır. $1\,000$ örnekte $800$ eğitim, $200$ test.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{2}{5}$</p>
      <p>$\dfrac{2 + 3}{2 + 5} = \dfrac{3}{5}$</p>
      <p>$\dfrac{3}{4} \div \dfrac{1}{2} = \dfrac{3}{8}$</p>
      <p>$2\tfrac{1}{3} = \dfrac{2}{3}$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{5}{6}$</p>
      <p>$\dfrac{2 + 3}{2 + 5} = \dfrac{5}{7}$</p>
      <p>$\dfrac{3}{4} \div \dfrac{1}{2} = \dfrac{3}{4} \cdot 2 = \dfrac{3}{2}$</p>
      <p>$2\tfrac{1}{3} = \dfrac{7}{3}$</p>
    </div>
  </div>
  <figcaption>Toplamada paylar ve paydalar ayrı ayrı toplanmaz; sadeleştirme yalnızca çarpanlar arasında yapılır.</figcaption>
</figure>

- **Payları ve paydaları toplamak.** $\dfrac{1}{2} + \dfrac{1}{3}$,
  $\dfrac{2}{5}$ olamaz: $\dfrac{2}{5}$, $\dfrac{1}{2}$'den bile küçük!
- **Toplamdaki terimleri sadeleştirmek.** $\dfrac{2 + 3}{2 + 5}$'te
  $2$'ler sadeleşmez; $2$ bir terim, çarpan değil. Önce üstü ve altı
  hesapla.
- **Bölmede yanlış kesri ters çevirmek.** Ters çevrilen **bölen**
  (ikinci kesir), bölünen değil.

## Özet

- $\dfrac{a}{b}$: bütünü $b$ parçaya bölüp $a$ tanesini almak; $a \div b$; $b \ne 0$.
- Pay ve paydayı aynı sayıyla çarpmak ya da bölmek değeri değiştirmez; en sade hâl için EBOB'a böl.
- Karşılaştırma: ortak payda ya da çapraz çarpma.
- Toplama ve çıkarma: ortak paydaya getir (EKOK), payları topla.
- Çarpma: payları çarp, paydaları çarp; önce sadeleştir.
- Bölme: bölenin tersiyle çarp.
- Tam sayılı kesir: $2\tfrac{1}{3} = \dfrac{7}{3}$.
- Sadeleştirme yalnızca çarpanlar arasında; toplamın içindeki terimler sadeleşmez.
