# Bölünebilme, Asal Sayılar, EBOB ve EKOK

Bir sayının başka bir sayıya **tam** bölünüp bölünmediği, ilk bakışta
küçük bir soru. Ama kesirleri sadeleştirmek, bir işi eşit parçalara
ayırmak, iki olayın ne zaman yeniden çakışacağını bulmak hep bu soruya
dayanıyor. Bu bölümde bölünebilme kurallarını, sayıların yapı taşları
olan **asal sayıları** ve iki güçlü aracı göreceğiz: en büyük ortak
bölen (**EBOB**) ve en küçük ortak kat (**EKOK**).

Ön bilgi: Doğal Sayılar ve İşlem Önceliği bölümü (özellikle kalanlı
bölme).

## Bölen ve kat

$a$ ve $b$ doğal sayılar olsun. $b$'yi $a$'ya böldüğümüzde kalan $0$
çıkıyorsa, yani bir $k$ doğal sayısı için

$$
b = a \cdot k
$$

yazılabiliyorsa $a$, $b$'nin bir **böleni**, $b$ de $a$'nın bir
**katıdır**. Örneğin $12 = 3 \cdot 4$: $3$, $12$'nin böleni; $12$, $3$'ün
katı.

- $12$'nin bölenleri: $1, 2, 3, 4, 6, 12$. Sonlu sayıda.
- $12$'nin katları: $12, 24, 36, 48, \dots$ Sonsuz sayıda.

Bölenleri bulmanın düzenli yolu, **çift çift** aramak: $1 \cdot 12$,
$2 \cdot 6$, $3 \cdot 4$. Çarpanlar birbirine yaklaşınca durabilirsin;
$4 \cdot 3$ zaten bulundu.

## Bölünebilme kuralları

Büyük bir sayının küçük sayılara bölünüp bölünmediğini, bölme yapmadan
rakamlarına bakarak anlayabiliriz:

| Bölen | Kural | Örnek |
|---|---|---|
| $2$ | son rakam çift ($0, 2, 4, 6, 8$) | $3\,584$: son rakam $4$ ✓ |
| $3$ | rakamlar toplamı $3$'e bölünür | $2\,415$: $2+4+1+5 = 12$ ✓ |
| $4$ | son iki rakamın oluşturduğu sayı $4$'e bölünür | $7\,316$: $16$ ✓ |
| $5$ | son rakam $0$ ya da $5$ | $1\,235$ ✓ |
| $6$ | hem $2$'ye hem $3$'e bölünür | $474$: çift, $4+7+4 = 15$ ✓ |
| $8$ | son üç rakamın oluşturduğu sayı $8$'e bölünür | $5\,120$: $120 = 8 \cdot 15$ ✓ |
| $9$ | rakamlar toplamı $9$'a bölünür | $8\,127$: $8+1+2+7 = 18$ ✓ |
| $10$ | son rakam $0$ | $4\,930$ ✓ |
| $11$ | sağdan başlayıp rakamları $+, -, +, -$ ile toplayınca sonuç $11$'e bölünür | $9\,273$: $3 - 7 + 2 - 9 = -11$ ✓ |

### Rakam toplamı kuralı neden çalışıyor?

Anahtar şu: $10 = 9 + 1$, $100 = 99 + 1$, $1\,000 = 999 + 1$. Yani her
basamak değeri, **$9$'un bir katı artı $1$**. Üç basamaklı bir $abc$
sayısını açalım:

$$
\begin{aligned}
100a + 10b + c &= (99a + a) + (9b + b) + c \\
&= \underbrace{99a + 9b}_{9\text{'un katı}} + (a + b + c)
\end{aligned}
$$

İlk parça her zaman $9$'a (dolayısıyla $3$'e) bölünüyor. Geriye kalan
$a + b + c$, rakamların toplamı. Sayı $9$'a ancak rakam toplamı $9$'a
bölünüyorsa bölünür. Üstelik sayının $9$'a bölümünden kalan, rakam
toplamının $9$'a bölümünden kalanla aynı.

## Asal sayılar

$1$'den büyük olup yalnızca iki böleni ($1$ ve kendisi) olan sayılara
**asal sayı** denir: $2, 3, 5, 7, 11, 13, \dots$ Asal olmayan, birden
büyük sayılara da **bileşik** sayı denir: $4 = 2 \cdot 2$, $6 = 2 \cdot 3$.

- **$1$ asal değildir**: tek bir böleni var. Neden böyle tanımlandığını
  birazdan asal çarpanlara ayırmada göreceğiz.
- **$2$ tek çift asal**: ondan büyük her çift sayı $2$'ye bölündüğü için
  bileşik.

Asalları bulmanın eski ve güzel bir yolu **Eratosthenes eleği**: $2$'den
başla, her asalın katlarını listeden sil; silinmeden kalanlar asal.

<figure class="fig">
<svg viewBox="0 0 440 248" width="440"><text class="dim" x="40.0" y="39.0" font-size="14" text-anchor="middle">1</text><rect class="dot" opacity="0.28" x="62" y="16" width="36" height="36" rx="5"/><rect class="curve" x="62" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="80.0" y="39.0" font-size="14" text-anchor="middle">2</text><rect class="dot" opacity="0.28" x="102" y="16" width="36" height="36" rx="5"/><rect class="curve" x="102" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="39.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="142" y="16" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="39.0" font-size="13" text-anchor="middle">4</text><rect class="dot" opacity="0.28" x="182" y="16" width="36" height="36" rx="5"/><rect class="curve" x="182" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="200.0" y="39.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="222" y="16" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="39.0" font-size="13" text-anchor="middle">6</text><rect class="dot" opacity="0.28" x="262" y="16" width="36" height="36" rx="5"/><rect class="curve" x="262" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="39.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="302" y="16" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="39.0" font-size="13" text-anchor="middle">8</text><rect class="box" x="342" y="16" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="39.0" font-size="13" text-anchor="middle">9</text><rect class="box" x="382" y="16" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="39.0" font-size="13" text-anchor="middle">10</text><rect class="dot" opacity="0.28" x="22" y="56" width="36" height="36" rx="5"/><rect class="curve" x="22" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="79.0" font-size="14" text-anchor="middle">11</text><rect class="box" x="62" y="56" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="79.0" font-size="13" text-anchor="middle">12</text><rect class="dot" opacity="0.28" x="102" y="56" width="36" height="36" rx="5"/><rect class="curve" x="102" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="79.0" font-size="14" text-anchor="middle">13</text><rect class="box" x="142" y="56" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="79.0" font-size="13" text-anchor="middle">14</text><rect class="box" x="182" y="56" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="79.0" font-size="13" text-anchor="middle">15</text><rect class="box" x="222" y="56" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="79.0" font-size="13" text-anchor="middle">16</text><rect class="dot" opacity="0.28" x="262" y="56" width="36" height="36" rx="5"/><rect class="curve" x="262" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="79.0" font-size="14" text-anchor="middle">17</text><rect class="box" x="302" y="56" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="79.0" font-size="13" text-anchor="middle">18</text><rect class="dot" opacity="0.28" x="342" y="56" width="36" height="36" rx="5"/><rect class="curve" x="342" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="360.0" y="79.0" font-size="14" text-anchor="middle">19</text><rect class="box" x="382" y="56" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="79.0" font-size="13" text-anchor="middle">20</text><rect class="box" x="22" y="96" width="36" height="36" rx="5"/><text class="dim" x="40.0" y="119.0" font-size="13" text-anchor="middle">21</text><rect class="box" x="62" y="96" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="119.0" font-size="13" text-anchor="middle">22</text><rect class="dot" opacity="0.28" x="102" y="96" width="36" height="36" rx="5"/><rect class="curve" x="102" y="96" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="119.0" font-size="14" text-anchor="middle">23</text><rect class="box" x="142" y="96" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="119.0" font-size="13" text-anchor="middle">24</text><rect class="box" x="182" y="96" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="119.0" font-size="13" text-anchor="middle">25</text><rect class="box" x="222" y="96" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="119.0" font-size="13" text-anchor="middle">26</text><rect class="box" x="262" y="96" width="36" height="36" rx="5"/><text class="dim" x="280.0" y="119.0" font-size="13" text-anchor="middle">27</text><rect class="box" x="302" y="96" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="119.0" font-size="13" text-anchor="middle">28</text><rect class="dot" opacity="0.28" x="342" y="96" width="36" height="36" rx="5"/><rect class="curve" x="342" y="96" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="360.0" y="119.0" font-size="14" text-anchor="middle">29</text><rect class="box" x="382" y="96" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="119.0" font-size="13" text-anchor="middle">30</text><rect class="dot" opacity="0.28" x="22" y="136" width="36" height="36" rx="5"/><rect class="curve" x="22" y="136" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="159.0" font-size="14" text-anchor="middle">31</text><rect class="box" x="62" y="136" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="159.0" font-size="13" text-anchor="middle">32</text><rect class="box" x="102" y="136" width="36" height="36" rx="5"/><text class="dim" x="120.0" y="159.0" font-size="13" text-anchor="middle">33</text><rect class="box" x="142" y="136" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="159.0" font-size="13" text-anchor="middle">34</text><rect class="box" x="182" y="136" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="159.0" font-size="13" text-anchor="middle">35</text><rect class="box" x="222" y="136" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="159.0" font-size="13" text-anchor="middle">36</text><rect class="dot" opacity="0.28" x="262" y="136" width="36" height="36" rx="5"/><rect class="curve" x="262" y="136" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="159.0" font-size="14" text-anchor="middle">37</text><rect class="box" x="302" y="136" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="159.0" font-size="13" text-anchor="middle">38</text><rect class="box" x="342" y="136" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="159.0" font-size="13" text-anchor="middle">39</text><rect class="box" x="382" y="136" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="159.0" font-size="13" text-anchor="middle">40</text><rect class="dot" opacity="0.28" x="22" y="176" width="36" height="36" rx="5"/><rect class="curve" x="22" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="199.0" font-size="14" text-anchor="middle">41</text><rect class="box" x="62" y="176" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="199.0" font-size="13" text-anchor="middle">42</text><rect class="dot" opacity="0.28" x="102" y="176" width="36" height="36" rx="5"/><rect class="curve" x="102" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="199.0" font-size="14" text-anchor="middle">43</text><rect class="box" x="142" y="176" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="199.0" font-size="13" text-anchor="middle">44</text><rect class="box" x="182" y="176" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="199.0" font-size="13" text-anchor="middle">45</text><rect class="box" x="222" y="176" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="199.0" font-size="13" text-anchor="middle">46</text><rect class="dot" opacity="0.28" x="262" y="176" width="36" height="36" rx="5"/><rect class="curve" x="262" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="199.0" font-size="14" text-anchor="middle">47</text><rect class="box" x="302" y="176" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="199.0" font-size="13" text-anchor="middle">48</text><rect class="box" x="342" y="176" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="199.0" font-size="13" text-anchor="middle">49</text><rect class="box" x="382" y="176" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="199.0" font-size="13" text-anchor="middle">50</text><rect class="dot" opacity="0.28" x="30" y="225" width="14" height="14" rx="3"/><rect class="curve" x="30" y="225" width="14" height="14" rx="3" style="stroke-width:1.4"/><text class="ink" x="50" y="236" font-size="12" text-anchor="start">asal</text><rect class="box" x="140" y="225" width="14" height="14" rx="3"/><text class="ink" x="160" y="236" font-size="12" text-anchor="start">bileşik</text><text class="dim" x="270" y="236" font-size="12" text-anchor="start">1: ne asal ne bileşik</text></svg>
  <figcaption>$1$'den $50$'ye kadar sayılar. Önce $2$'nin katları, sonra $3$'ün, $5$'in ve $7$'nin katları elenince geriye $15$ asal kalıyor. $7 \cdot 7 = 49$ olduğu için $50$'ye kadar $7$'den sonra elemeye gerek yok.</figcaption>
</figure>

**Bir sayı asal mı?** $n$'yi, **karesi $n$'yi geçmeyen** asallara böl.
Hiçbiri bölmüyorsa $n$ asal. Neden yeter? $n = a \cdot b$ ise
çarpanlardan en az biri küçük tarafta kalır: ikisi de büyük olsaydı
çarpımları $n$'yi geçerdi. Örneğin $97$ için $2, 3, 5, 7$'ye bakmak
yeter ($11 \cdot 11 = 121 > 97$); hiçbiri bölmüyor, $97$ asal.

## Asal çarpanlara ayırma

Her bileşik sayı asalların çarpımı olarak yazılabilir. Bir **çarpan
ağacı** kur: sayıyı herhangi iki çarpana ayır, asal olmayan dalları
ayırmaya devam et.

<figure class="fig">
<svg viewBox="0 0 400 280" width="400"><line class="curve3" x1="200" y1="38" x2="120" y2="72"/><line class="curve3" x1="200" y1="38" x2="290" y2="72"/><line class="curve3" x1="120" y1="98" x2="70" y2="132"/><line class="curve3" x1="120" y1="98" x2="170" y2="132"/><line class="curve3" x1="290" y1="98" x2="255" y2="132"/><line class="curve3" x1="290" y1="98" x2="325" y2="132"/><line class="curve3" x1="70" y1="158" x2="40" y2="192"/><line class="curve3" x1="70" y1="158" x2="100" y2="192"/><line class="curve3" x1="170" y1="158" x2="145" y2="192"/><line class="curve3" x1="170" y1="158" x2="195" y2="192"/><rect class="box" x="177.5" y="12" width="45" height="28" rx="6"/><text class="ink" x="200" y="31" font-size="14" text-anchor="middle">360</text><rect class="box" x="102.0" y="72" width="36" height="28" rx="6"/><text class="ink" x="120" y="91" font-size="14" text-anchor="middle">36</text><rect class="box" x="272.0" y="72" width="36" height="28" rx="6"/><text class="ink" x="290" y="91" font-size="14" text-anchor="middle">10</text><rect class="box" x="56.5" y="132" width="27" height="28" rx="6"/><text class="ink" x="70" y="151" font-size="14" text-anchor="middle">4</text><rect class="box" x="156.5" y="132" width="27" height="28" rx="6"/><text class="ink" x="170" y="151" font-size="14" text-anchor="middle">9</text><circle class="dot" opacity="0.28" cx="255" cy="146" r="15"/><circle class="curve" cx="255" cy="146" r="15" style="stroke-width:1.6"/><text class="ink" x="255" y="151" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="325" cy="146" r="15"/><circle class="curve" cx="325" cy="146" r="15" style="stroke-width:1.6"/><text class="ink" x="325" y="151" font-size="14" text-anchor="middle">5</text><circle class="dot" opacity="0.28" cx="40" cy="206" r="15"/><circle class="curve" cx="40" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="40" y="211" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="100" cy="206" r="15"/><circle class="curve" cx="100" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="100" y="211" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="145" cy="206" r="15"/><circle class="curve" cx="145" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="145" y="211" font-size="14" text-anchor="middle">3</text><circle class="dot" opacity="0.28" cx="195" cy="206" r="15"/><circle class="curve" cx="195" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="195" y="211" font-size="14" text-anchor="middle">3</text><text class="ink" x="200" y="250" font-size="13" text-anchor="middle">360 = 2 · 2 · 2 · 3 · 3 · 5 = 2³ · 3² · 5</text><text class="dim" x="200" y="268" font-size="11" text-anchor="middle">yaprakların hepsi asal</text></svg>
  <figcaption>$360$'ı $36 \cdot 10$ diye ayırıp her dalı asallara inene kadar böldük. Başka bir yerden başlasaydık ($360 = 8 \cdot 45$ gibi) ağaç farklı görünürdü ama yapraklar yine üç tane $2$, iki tane $3$ ve bir $5$ olurdu.</figcaption>
</figure>

$$
360 = 2^3 \cdot 3^2 \cdot 5
$$

**Aritmetiğin temel teoremi:** Bu yazılış (çarpanların sırası dışında)
**tek**. Hangi yoldan gidersen git, aynı asallara varırsın. $1$'in asal
sayılmamasının sebebi bu: sayılsaydı $360 = 1 \cdot 2^3 \cdot 3^2 \cdot
5 = 1 \cdot 1 \cdot 2^3 \cdot \dots$ diye sonsuz yazılış olurdu.

Asal çarpanlar bir sayının "kimliği". Bölenleri de buradan okunur: $360$'ın
her böleni $2^a \cdot 3^b \cdot 5^c$ biçiminde, $a \in \{0,1,2,3\}$,
$b \in \{0,1,2\}$, $c \in \{0,1\}$. Seçim sayısı:

$$
(3 + 1)(2 + 1)(1 + 1) = 4 \cdot 3 \cdot 2 = 24
$$

$360$'ın $24$ böleni var. Kural: **üslerin birer fazlasını çarp**.

## EBOB: en büyük ortak bölen

İki sayıyı da bölen sayıların en büyüğü. $84$ ile $126$'yı düşünelim.

**Asal çarpanlarla:** Ortak asalları **küçük** üsleriyle al.

$$
84 = 2^2 \cdot 3 \cdot 7, \qquad 126 = 2 \cdot 3^2 \cdot 7
$$

Ortak asallar $2$, $3$, $7$; küçük üsler $2^1$, $3^1$, $7^1$:

$$
\text{EBOB}(84, 126) = 2 \cdot 3 \cdot 7 = 42
$$

**Öklid algoritması:** Büyük sayıyı küçüğe böl, kalanla devam et. Kalan
$0$ olunca son bölen EBOB.

$$
\begin{aligned}
126 &= 84 \cdot 1 + 42 \\
84 &= 42 \cdot 2 + 0
\end{aligned}
$$

EBOB $42$. Neden çalışıyor? $126$'yı ve $84$'ü bölen her sayı, farkları
olan $42$'yi de böler; yani $(126, 84)$ çiftinin ortak bölenleri
$(84, 42)$ çiftininkilerle aynı. Sayılar küçülür, EBOB değişmez. Büyük
sayılarda bu yol çarpanlara ayırmaktan çok daha hızlı; bilgisayarlar da
bunu kullanıyor.

EBOB'u $1$ olan sayılara **aralarında asal** denir: $8$ ile $15$ gibi.
İkisi de asal değil ama ortak asal çarpanları yok.

## EKOK: en küçük ortak kat

İki sayının da katı olan sayıların en küçüğü (sıfır hariç).

**Asal çarpanlarla:** Bütün asalları **büyük** üsleriyle al.

$$
\text{EKOK}(84, 126) = 2^2 \cdot 3^2 \cdot 7 = 252
$$

**Kontrol:** $252 = 84 \cdot 3 = 126 \cdot 2$ ✓.

İki sayı için güzel bir bağ var:

$$
\text{EBOB}(a, b) \cdot \text{EKOK}(a, b) = a \cdot b
$$

$42 \cdot 252 = 10\,584 = 84 \cdot 126$. Çünkü her asal için küçük üs ile
büyük üsün toplamı, iki sayıdaki üslerin toplamına eşit. EBOB'u
biliyorsan EKOK tek bölmeyle çıkıyor: $84 \cdot 126 \div 42 = 252$.

## Hangisini kullanmalı?

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h4>EBOB</h4>
      <p>Bir şeyi <b>eşit, en büyük parçalara</b> bölmek</p>
      <p>Bir zemini en büyük kare fayanslarla döşemek</p>
      <p>Bir kesri sadeleştirmek</p>
      <p>Cevap sayılardan <b>küçük</b> ya da eşit</p>
    </div>
    <div class="ok">
      <h4>EKOK</h4>
      <p>İki olayın <b>yeniden aynı anda</b> olması</p>
      <p>Farklı uzunluktaki döngülerin çakışması</p>
      <p>Kesirleri ortak paydaya getirmek</p>
      <p>Cevap sayılardan <b>büyük</b> ya da eşit</p>
    </div>
  </div>
  <figcaption>Soruda "bölmek, paylaştırmak, en büyük parça" varsa EBOB; "tekrar, çakışma, ilk ortak an" varsa EKOK.</figcaption>
</figure>

**Örnek (EKOK):** Bir otobüs $12$ dakikada, diğeri $18$ dakikada bir
kalkıyor. Saat $08{:}00$'de birlikte kalktılar. Birlikte kalkış her
iki sürenin de katında olur: $\text{EKOK}(12, 18) = 36$. Bir sonraki
birlikte kalkış $08{:}36$.

**Örnek (EBOB):** $24$ elma ve $36$ armut, her tabakta aynı sayıda elma
ve aynı sayıda armut olacak şekilde en çok kaç tabağa bölünür? Tabak
sayısı ikisini de bölmeli: $\text{EBOB}(24, 36) = 12$ tabak; her tabakta
$2$ elma, $3$ armut.

## Makine öğrenmesinde bölünebilme

**Yığın boyutu.** $1\,000$ örnekli bir veri setini eşit yığınlara bölmek
istiyorsan yığın boyutu $1\,000$'in bir böleni olmalı: $16$ bölmüyor
($1\,000 = 16 \cdot 62 + 8$, son yığın eksik kalır), $8$ ve $40$ bölüyor.

**Görüntüyü yamalara bölmek.** Bazı görüntü modelleri $224 \times 224$
piksellik bir resmi $16 \times 16$'lık kare yamalara ayırır. $224 = 16
\cdot 14$ olduğu için her kenarda $14$, toplam $14 \cdot 14 = 196$ yama
çıkıyor. Yama boyu kenarı bölmeseydi resmin kenarında artık kalırdı.

**Döngülerin çakışması.** Model her $12$ turda bir kaydediliyor, öğrenme
hızı her $18$ turda bir düşürülüyorsa ikisi ilk kez $36$. turda aynı anda
olur: EKOK.

## Sık yapılan hatalar

- **$1$'i asal saymak.** Asal sayının tam iki böleni olmalı; $1$'in bir
  tane var.
- **$6$ kuralını yalnızca rakam toplamıyla kontrol etmek.** $6$'ya
  bölünmek için sayı hem $3$'e (rakam toplamı) hem $2$'ye (çift) bölünmeli.
  $213$: rakam toplamı $6$ ama tek, $6$'ya bölünmez.
- **EBOB ile EKOK'u karıştırmak.** EBOB iki sayıdan büyük olamaz, EKOK
  küçük olamaz. Cevabın bu sınırlara uyup uymadığına bak.
- **Çarpan ağacında durmayı unutmak.** Yapraklarda bileşik sayı kalmamalı:
  $360 = 4 \cdot 9 \cdot 10$ bir çarpanlara ayırma ama **asal** çarpanlara
  ayırma değil.

## Özet

- $b = a \cdot k$ ise $a$, $b$'nin böleni; $b$, $a$'nın katı.
- Bölünebilme kuralları: $2, 5, 10$ son rakam; $4$ son iki; $8$ son üç; $3, 9$ rakam toplamı; $6$ = $2$ ve $3$; $11$ işaretli toplam.
- Asal: tam iki böleni var. $1$ asal değil, $2$ tek çift asal.
- Asallık testi: karesi sayıyı geçmeyen asallara bölmek yeter.
- Her sayının asal çarpanlara ayrılışı tek; bölen sayısı = üslerin birer fazlasının çarpımı.
- EBOB: ortak asallar, küçük üsler; ya da Öklid algoritması.
- EKOK: bütün asallar, büyük üsler; $\text{EBOB} \cdot \text{EKOK} = a \cdot b$.
- Bölmek, paylaştırmak → EBOB; çakışmak, yeniden aynı an → EKOK.
