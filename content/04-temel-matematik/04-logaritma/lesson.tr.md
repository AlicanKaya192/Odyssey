# Logaritma

Makine öğrenmesinde logaritma her yerde: modelin kaybını ölçen formülde,
çarpık bir sütunu düzeltirken, algoritmaların hızını anlatırken, bir
olasılığın ne kadar "şaşırtıcı" olduğunu hesaplarken. Çoğu kişi onu okulda
kuralları ezberlenip unutulan bir konu olarak hatırlıyor.

Bu bölümde kuralları ezberlemeyeceğiz; **nereden çıktıklarını** göreceğiz.
Logaritmanın tek bir soruya verilen cevap olduğunu anladığında kuralların
hepsi o sorudan kendiliğinden çıkıyor.

Başlamadan önce bilmen gereken tek şey **üs**: $2^3 = 2 \cdot 2 \cdot 2 = 8$.
Üs kuralları bir önceki bölümde (Üsler ve Kökler) anlatıldı; burada
gerektikçe hatırlatacağım.

## Tek bir soru

Şu üç soruya bak:

- $2^3 = \;?$ — Cevap $8$. Tabanı ve üssü biliyorsun, **sonucu** arıyorsun.
- $?^3 = 8$ — Cevap $2$. Üssü ve sonucu biliyorsun, **tabanı** arıyorsun.
  Bu kök: $\sqrt[3]{8} = 2$.
- $2^{?} = 8$ — Cevap $3$. Tabanı ve sonucu biliyorsun, **üssü** arıyorsun.

Üçüncü sorunun bir adı var. **Logaritma**, "bu tabanı kaçıncı kuvvete
yükseltirsem bu sayıyı elde ederim?" sorusunun cevabı:

$$
\log_2 8 = 3 \quad\text{çünkü}\quad 2^3 = 8
$$

Okunuşu: "2 tabanında 8'in logaritması 3". Genel hâli:

$$
\log_b x = y \quad\Longleftrightarrow\quad b^y = x
$$

İki taraf **aynı cümlenin iki yazılışı**. Soldaki "üs kaç?" diye soruyor,
sağdaki "üs bu" diye cevap veriyor. Bir logaritma ifadesine takıldığında
yapacağın ilk şey onu sağdaki biçime çevirmek.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>$b$ — taban</span><span>Kuvveti alınan sayı. Pozitif olmalı ve 1 olmamalı.</span></div>
    <div class="anat-row"><span>$x$ — sayı (argüman)</span><span>Ulaşmak istediğin sonuç. Pozitif olmalı.</span></div>
    <div class="anat-row"><span>$y$ — logaritma</span><span>Aranan üs. Negatif, sıfır ya da ondalıklı olabilir.</span></div>
  </div>
  <figcaption>Logaritmanın üç parçası. Hesabın sonucu olan $y$ aslında bir üs.</figcaption>
</figure>

### Üç ters işlem

Matematikte her işlemin onu geri alan bir eşi var:

| İşlem | Geri alan | Örnek |
|---|---|---|
| Toplama | Çıkarma | $5 + 3 = 8$ → $8 - 3 = 5$ |
| Çarpma | Bölme | $5 \cdot 3 = 15$ → $15 / 3 = 5$ |
| Üs alma | Kök **ya da** logaritma | $2^3 = 8$ → $\sqrt[3]{8} = 2$ ve $\log_2 8 = 3$ |

Üs almanın **iki** tersi olmasının sebebi, toplama ve çarpmanın aksine
sıranın önemli olması: $2^3$ ile $3^2$ aynı şey değil. Tabanı geri almak
başka bir iş (kök), üssü geri almak başka bir iş (logaritma).

### Elle birkaç tane

Her birinde soruyu "taban kaçıncı kuvvette sayıyı verir?" diye çevir:

- $\log_{10} 1000$: $10^{?} = 1000$. $10^3 = 1000$, cevap $3$.
- $\log_3 81$: $3^{?} = 81$. $3 \cdot 3 \cdot 3 \cdot 3 = 81$, cevap $4$.
- $\log_2 1024$: $2^{10} = 1024$, cevap $10$.
- $\log_5 5$: $5^{?} = 5$. Her sayının birinci kuvveti kendisi, cevap $1$.
- $\log_7 1$: $7^{?} = 1$. Sıfırdan farklı her sayının sıfırıncı kuvveti $1$,
  cevap $0$.

## Negatif ve ondalıklı sonuçlar

Logaritmanın sonucu bir üs olduğu için üslerin alabildiği her değeri
alabiliyor.

**Negatif üs** "bölü" demek: $2^{-1} = \frac{1}{2}$, $2^{-3} = \frac{1}{8}$.
Öyleyse:

$$
\log_2 \tfrac{1}{8} = -3 \qquad \log_{10} 0.01 = -2
$$

Buradan önemli bir sonuç çıkıyor: **1'den küçük pozitif sayıların
logaritması negatif** (tabanı 1'den büyükken). Olasılıklar 0 ile 1 arasında
olduğu için bir olasılığın logaritması hep negatif çıkıyor. Makine
öğrenmesindeki kayıp formüllerinin başında bir eksi işareti görmenin sebebi
bu; ileride tekrar geleceğiz.

**Kesirli üs** kök demek: $4^{1/2} = \sqrt{4} = 2$. Öyleyse $\log_4 2 = \frac{1}{2}$.

Çoğu logaritma tam sayı çıkmıyor. $\log_2 3$ kaç? $2^1 = 2$ ile $2^2 = 4$
arasında bir yerde; yani cevap 1 ile 2 arasında. Hesap makinesi
$1.58496...$ diyor ve gerçekten $2^{1.58496} \approx 3$.

Bir logaritmayı **tahmin etmek** için iki komşu tam kuvvete bakmak çok işe
yarıyor. $\log_{10} 5000$? $10^3 = 1000$ ile $10^4 = 10000$ arasında, yani
3 ile 4 arasında — ve 5000, 10000'e 1000'den daha "yakın" olduğu için 3.7
civarı. (Gerçek değer $3.699$.)

## Neyin logaritması yok?

Tanımdan iki yasak çıkıyor. İkisini de "üs kaç?" sorusuyla görebilirsin:

- **Sıfırın logaritması yok.** $2^{?} = 0$ olacak bir üs yok. Üs küçüldükçe
  sonuç sıfıra **yaklaşıyor** ($2^{-10} \approx 0.001$, $2^{-100}$ çok daha
  küçük) ama hiçbir zaman sıfır olmuyor. Bu yüzden $\log x$, $x$ sıfıra
  yaklaştıkça eksi sonsuza gidiyor.
- **Negatif sayının logaritması yok.** Pozitif bir tabanın hangi kuvvetini
  alırsan al sonuç pozitif. $2^{?} = -8$ olamaz.

Tabanın kendisi için de iki şart var: pozitif olmalı ve 1 olmamalı. $1$'in
her kuvveti $1$; $\log_1 5$ sorusunun cevabı yok.

Bu yasaklar denklem çözerken sık karşına çıkacak: cebir bazen logaritmanın
içini negatif yapan bir "çözüm" üretiyor ve onu elemek gerekiyor. Aşağıda
bunun bir örneğini adım adım göreceğiz.

## Grafik: üssün aynası

$y = 2^x$ ile $y = \log_2 x$ fonksiyonlarını aynı eksene çizelim:

<figure class="fig">
<svg viewBox="0 0 380 320" width="380"><line class="grid" x1="67" y1="290" x2="67" y2="20"/><line class="grid" x1="30" y1="260" x2="360" y2="260"/><line class="grid" x1="103" y1="290" x2="103" y2="20"/><line class="grid" x1="30" y1="230" x2="360" y2="230"/><line class="grid" x1="177" y1="290" x2="177" y2="20"/><line class="grid" x1="30" y1="170" x2="360" y2="170"/><line class="grid" x1="213" y1="290" x2="213" y2="20"/><line class="grid" x1="30" y1="140" x2="360" y2="140"/><line class="grid" x1="250" y1="290" x2="250" y2="20"/><line class="grid" x1="30" y1="110" x2="360" y2="110"/><line class="grid" x1="287" y1="290" x2="287" y2="20"/><line class="grid" x1="30" y1="80" x2="360" y2="80"/><line class="grid" x1="323" y1="290" x2="323" y2="20"/><line class="grid" x1="30" y1="50" x2="360" y2="50"/><line class="line" x1="30" y1="200" x2="360" y2="200"/><line class="line" x1="140" y1="290" x2="140" y2="20"/><text class="dim" x="67" y="215" font-size="11" text-anchor="middle">-2</text><text class="dim" x="132" y="264" font-size="11" text-anchor="end">-2</text><text class="dim" x="103" y="215" font-size="11" text-anchor="middle">-1</text><text class="dim" x="132" y="234" font-size="11" text-anchor="end">-1</text><text class="dim" x="177" y="215" font-size="11" text-anchor="middle">1</text><text class="dim" x="132" y="174" font-size="11" text-anchor="end">1</text><text class="dim" x="213" y="215" font-size="11" text-anchor="middle">2</text><text class="dim" x="132" y="144" font-size="11" text-anchor="end">2</text><text class="dim" x="250" y="215" font-size="11" text-anchor="middle">3</text><text class="dim" x="132" y="114" font-size="11" text-anchor="end">3</text><text class="dim" x="287" y="215" font-size="11" text-anchor="middle">4</text><text class="dim" x="132" y="84" font-size="11" text-anchor="end">4</text><text class="dim" x="323" y="215" font-size="11" text-anchor="middle">5</text><text class="dim" x="132" y="54" font-size="11" text-anchor="end">5</text><path class="curve3" stroke-dasharray="5 5" d="M30,290 L360,20"/><path class="curve" d="M30,196 L38,196 L46,195 L54,194 L62,193 L69,192 L77,191 L85,189 L93,188 L101,186 L109,183 L117,181 L125,178 L132,174 L140,170 L148,165 L156,159 L164,153 L172,145 L180,137 L188,126 L195,115 L203,101 L211,85 L219,66 L227,45 L235,20"/><path class="curve2" d="M145,290 L153,245 L161,224 L169,210 L178,199 L186,190 L194,183 L203,177 L211,171 L219,167 L227,162 L236,158 L244,155 L252,152 L261,148 L269,146 L277,143 L285,140 L294,138 L302,136 L310,134 L319,131 L327,130 L335,128 L343,126 L352,124 L360,122"/><circle class="dot" cx="140" cy="170" r="4"/><circle class="dot2" cx="177" cy="200" r="4"/><circle class="dot" cx="213" cy="80" r="4"/><circle class="dot2" cx="287" cy="140" r="4"/><text class="ink" x="242" y="32" font-size="13">y = 2<tspan baseline-shift="super" font-size="9">x</tspan></text><text class="ink" x="298" y="118" font-size="13">y = log₂ x</text><text class="dim" x="309" y="41" font-size="12">y = x</text></svg>
  <figcaption>Mor $2^x$, turuncu $\log_2 x$. Kesik çizgi $y = x$ doğrusu; iki eğri ona göre birbirinin yansıması. $2^x$ eğrisindeki $(2, 4)$ noktası logaritmada $(4, 2)$ oluyor.</figcaption>
</figure>

Grafikten okunacak dört şey var:

1. **İki eğri $y = x$ doğrusuna göre ayna.** Ters fonksiyonların hepsinde
   böyle: birinin girdisi ötekinin çıktısı. $(0, 1)$ noktası $(1, 0)$'a,
   $(2, 4)$ noktası $(4, 2)$'ye yansıyor.
2. **Logaritma hep $(1, 0)$'dan geçiyor**, taban ne olursa olsun: $\log_b 1 = 0$.
3. **Sol tarafta duvar var.** Turuncu eğri $x = 0$'a hiç değmiyor, aşağı
   doğru sonsuza iniyor. Sıfırın ve negatiflerin logaritması olmadığını
   grafik de söylüyor.
4. **Logaritma çok yavaş büyüyor.** $x$ 1'den 4'e çıkınca $y$ 0'dan 2'ye
   çıkıyor; $x$ 4'ten 1024'e çıkınca $y$ yalnızca 2'den 10'a çıkıyor.
   Üstel fonksiyon ne kadar hızlı patlıyorsa logaritma o kadar ağır
   tırmanıyor.

Dördüncü madde logaritmanın en kullanışlı özelliği: **çok büyük sayıları
küçük, yönetilebilir sayılara çeviriyor.** Bir milyon $\log_{10}$ ile 6, bir
milyar 9 oluyor.

## Üç özel taban

Teoride her pozitif sayı (1 hariç) taban olabilir. Pratikte üç tanesi
kullanılıyor ve her birinin kendi yazılışı var.

### 10 tabanı: basamak sayacı

$\log_{10}$ ondalık sistemimizle birebir örtüşüyor. $\log_{10} 100 = 2$,
$\log_{10} 1000 = 3$: **logaritma, sayının kaç basamaklı olduğunun bir
eksiği.** Kesin hâli şöyle; $n$ pozitif bir tam sayıysa:

$$
\text{basamak sayısı} = \lfloor \log_{10} n \rfloor + 1
$$

$\lfloor \cdot \rfloor$ "aşağı yuvarla" demek. $\log_{10} 5000 = 3.699$,
aşağı yuvarlanınca 3, bir fazlası 4: 5000 dört basamaklı. Bu formülün gücü
sayıyı yazmadan basamağını bulabilmek: $2^{100}$ kaç basamaklı?

$$
\log_{10} 2^{100} = 100 \cdot \log_{10} 2 = 100 \cdot 0.30103 = 30.103
\quad\Rightarrow\quad 31 \text{ basamak}
$$

(İlk eşitlikte bir kural kullandık; birazdan göreceğiz.)

Bazı kaynaklar tabansız $\log x$ yazınca 10 tabanını kasteder. **Dikkat:**
makine öğrenmesi kaynaklarında tabansız $\log$ çoğu zaman bir sonraki
tabanı, yani $e$'yi kasteder.

### e tabanı: doğal logaritma

$e = 2.71828...$ matematiğin en önemli sabitlerinden biri. Nereden
çıktığını bir faiz hesabıyla görmek mümkün.

Bankaya 1 lira koyuyorsun, yıllık faiz %100. Yıl sonunda 2 liran oluyor.
Peki faizi yılda **iki kez** yarı yarıya işletirlerse? Altı ayda 1.5, yıl
sonunda $1.5 \cdot 1.5 = 2.25$. Faizi ne kadar sık işletirlerse sonuç o
kadar büyüyor:

| Yılda kaç kez | Hesap | Yıl sonu |
|---|---|---|
| 1 | $(1 + 1)^1$ | 2 |
| 12 (aylık) | $(1 + \frac{1}{12})^{12}$ | 2.613 |
| 365 (günlük) | $(1 + \frac{1}{365})^{365}$ | 2.7146 |
| 1 000 000 | $(1 + \frac{1}{10^6})^{10^6}$ | 2.71828 |

Sonuç sonsuza gitmiyor; **bir sayıya dayanıp duruyor.** O sayı $e$.
Sürekli büyüyen her şeyin (nüfus, radyoaktif bozunma, sürekli bileşik faiz)
doğal tabanı bu.

$e$ tabanındaki logaritmaya **doğal logaritma** deniyor ve $\ln$ yazılıyor:

$$
\ln x = \log_e x \qquad \ln e = 1 \qquad \ln 1 = 0
$$

Makine öğrenmesinde neredeyse bütün logaritmalar doğal logaritma. Sebebi
bir sonraki modülde (Kalkülüs) netleşecek: $e^x$'in türevi kendisi ve $\ln x$'in
türevi $\frac{1}{x}$. Başka hiçbir tabanda türevler bu kadar temiz çıkmıyor.

### 2 tabanı: bit ve yarıya bölme

$\log_2$ bilgisayar biliminin tabanı. İki soruya cevap veriyor:

- **Bir sayıyı kaç kez yarıya bölersen 1'e inersin?** $\log_2 1024 = 10$:
  1024 → 512 → ... → 1, on adım. Sıralı bir listede ikili arama bu yüzden
  bir milyon eleman arasında en fazla 20 adımda buluyor ($\log_2 10^6 \approx 19.93$).
  Algoritmalar patikasında $O(\log n)$ diye göreceğin şey bu.
- **Bir şeyi kaç bitle ayırt edersin?** 8 farklı değeri ayırt etmek için
  $\log_2 8 = 3$ bit yetiyor (000'dan 111'e). Entropi bölümünde bilginin
  birimi olarak geri gelecek.

## Kurallar ve nereden çıktıkları

Logaritmanın bütün kuralları üs kurallarının tersten okunması. Her birini
türeteceğim; ezberlemek yerine bu türetmeyi bir kez anlaman yeterli.

Üç üs kuralını hatırla:

$$
b^m \cdot b^n = b^{m+n} \qquad \frac{b^m}{b^n} = b^{m-n} \qquad (b^m)^k = b^{m \cdot k}
$$

### Kural 1: Çarpımın logaritması toplamdır

$$
\log_b (x \cdot y) = \log_b x + \log_b y
$$

**Neden:** $\log_b x = m$ ve $\log_b y = n$ diyelim. Tanım gereği
$x = b^m$ ve $y = b^n$. Çarpalım:

$$
x \cdot y = b^m \cdot b^n = b^{m+n}
$$

Son eşitlik "$x \cdot y$'yi elde etmek için $b$'yi $m + n$'inci kuvvete
yükselt" diyor. Yani $\log_b (xy) = m + n = \log_b x + \log_b y$.

**Örnek:** $\log_{10} 2 + \log_{10} 5 = \log_{10} 10 = 1$. Gerçekten de
$0.30103 + 0.69897 = 1$.

Bu kural logaritmanın **icat edilme sebebi**. 1600'lerde gökbilimciler
büyük sayıları elle çarpmak zorundaydı. Logaritma tablosuyla çarpma
toplamaya dönüşüyordu: iki sayının logaritmasını tablodan bul, topla,
sonucun karşılığını tablodan geri oku. Bugün aynı dönüşümü bilgisayar
sayılarının sınırını aşmamak için kullanıyoruz.

### Kural 2: Bölümün logaritması farktır

$$
\log_b \frac{x}{y} = \log_b x - \log_b y
$$

Türetme aynı: $\frac{x}{y} = \frac{b^m}{b^n} = b^{m-n}$.

Özel bir durumu: $\log_b \frac{1}{x} = \log_b 1 - \log_b x = -\log_b x$. Bir
sayının tersinin logaritması, logaritmasının eksi işaretlisi.

### Kural 3: Kuvvetin logaritması çarpımdır

$$
\log_b (x^k) = k \cdot \log_b x
$$

**Neden:** $x = b^m$ ise $x^k = (b^m)^k = b^{m \cdot k}$. Üs $k \cdot m$.

Basamak sayısı hesabında kullandığımız kural buydu: $\log_{10} 2^{100} =
100 \cdot \log_{10} 2$. Üssü öne alıp çarpan yapıyor; yani **bilinmeyeni
üsten indiriyor.** Denklem çözmenin anahtarı bu.

Kök de bir kuvvet olduğu için kural onu da kapsıyor:
$\log_b \sqrt{x} = \log_b x^{1/2} = \frac{1}{2}\log_b x$.

### Kural 4: Taban değiştirme

Hesap makinelerinde çoğu zaman yalnızca $\ln$ ile $\log_{10}$
var. $\log_2 3$'ü nasıl hesaplarsın?

$$
\log_b x = \frac{\log_k x}{\log_k b} \qquad \text{(k herhangi bir taban)}
$$

**Neden:** $\log_b x = y$ diyelim, yani $b^y = x$. İki tarafın da $k$
tabanında logaritmasını al: $\log_k (b^y) = \log_k x$. Kural 3 ile
$y \cdot \log_k b = \log_k x$. $y$'yi yalnız bırak:
$y = \frac{\log_k x}{\log_k b}$.

**Örnek:** $\log_2 3 = \frac{\ln 3}{\ln 2} = \frac{1.0986}{0.6931} = 1.585$.

Bu kuralın bir sonucu daha var: **iki tabandaki logaritma birbirinin sabit
katı.** $\log_2 x = \frac{\ln x}{\ln 2} = 1.4427 \cdot \ln x$. Hangi tabanı
seçersen seç eğrinin **şekli** aynı, yalnızca dikey olarak esniyor. Makine
öğrenmesinde tabanın çoğu zaman önemsenmemesinin sebebi bu: sıralama ve
en küçüğün yeri değişmiyor.

Bütün kurallar tek yerde:

| Kural | Ne yapıyor |
|---|---|
| $\log_b (xy) = \log_b x + \log_b y$ | Çarpım → toplam |
| $\log_b (x/y) = \log_b x - \log_b y$ | Bölüm → fark |
| $\log_b (x^k) = k \log_b x$ | Kuvvet → çarpan |
| $\log_b x = \dfrac{\ln x}{\ln b}$ | Taban değiştirme |
| $\log_b 1 = 0$ ve $\log_b b = 1$ | Her tabanda aynı |
| $b^{\log_b x} = x$ ve $\log_b (b^x) = x$ | Üs ile logaritma birbirini siler |

Hepsi $\log_b x = y \iff b^y = x$ tanımından çıkıyor.

## Sık yapılan hatalar

Kurallara çok benzeyen ama **yanlış** olan dört eşitlik var. Sınavlarda da
gerçek kodda da en çok bunlar karıştırılıyor.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\log (x + y) = \log x + \log y$</p>
      <p>$\log (x - y) = \log x - \log y$</p>
      <p>$\dfrac{\log x}{\log y} = \log \dfrac{x}{y}$</p>
      <p>$(\log x)^2 = 2 \log x$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$\log (x \cdot y) = \log x + \log y$</p>
      <p>$\log (x / y) = \log x - \log y$</p>
      <p>$\dfrac{\log x}{\log y} = \log_y x$ (taban değiştirme)</p>
      <p>$\log (x^2) = 2 \log x$</p>
    </div>
  </div>
  <figcaption>Logaritma çarpımı ve bölümü açar; toplamı ve farkı açamaz.</figcaption>
</figure>

İlkini sayılarla çürütmek kolay: $\log_{10} (10 + 10) = \log_{10} 20 = 1.301$,
ama $\log_{10} 10 + \log_{10} 10 = 2$. **Toplamın logaritmasının basit bir
açılımı yok.**

Dördüncüsünde parantezin yeri her şeyi değiştiriyor: $(\log x)^2$
logaritmanın karesi, $\log(x^2)$ karenin logaritması.

## Üstel denklemler

Logaritma, bilinmeyen **üsteyken** kullanılan araç. Tipik soru: yıllık %7
getirisi olan bir yatırım kaç yılda ikiye katlanır?

Her yıl para $1.07$ ile çarpılıyor. $t$ yıl sonra $1.07^t$ katına çıkıyor.
İki katı arıyoruz:

$$
1.07^t = 2
$$

Bilinmeyen üste. İki tarafın logaritmasını alıp Kural 3 ile aşağı indir:

$$
\ln (1.07^t) = \ln 2 \quad\Rightarrow\quad t \cdot \ln 1.07 = \ln 2
\quad\Rightarrow\quad t = \frac{\ln 2}{\ln 1.07} = \frac{0.6931}{0.0677} = 10.24
$$

Yaklaşık on yıl. (Finansçıların "72 kuralı" bu hesabın kestirmesi:
$72 / 7 \approx 10.3$.)

Genel yöntem her zaman aynı:

<figure class="fig">
  <div class="flow">
    <span class="node">Üslü terimi yalnız bırak</span>
    <span class="arrow">→</span>
    <span class="node">İki tarafın logaritmasını al</span>
    <span class="arrow">→</span>
    <span class="node">Üssü öne indir (Kural 3)</span>
    <span class="arrow">→</span>
    <span class="node ok">Bilinmeyeni çöz</span>
  </div>
  <figcaption>Bilinmeyen üsteyse dört adım. Hangi tabanda logaritma aldığın sonucu değiştirmez.</figcaption>
</figure>

Bu yöntemi üç farklı durumda adım adım uygulayalım.

### Önünde katsayı olan üs

**Soru:** 3000 liralık birikim yılda %4 büyüyor. Kaç yılda 4500 lira olur?

$$
3000 \cdot 1.04^t = 4500
$$

**1. Üslü terimi yalnız bırak.** İki tarafı 3000'e böl:

$$
1.04^t = \frac{4500}{3000} = 1.5
$$

**2. Logaritma al ve üssü indir:**

$$
t \cdot \ln 1.04 = \ln 1.5
\quad\Rightarrow\quad
t = \frac{\ln 1.5}{\ln 1.04} = \frac{0.4055}{0.0392} \approx 10.34 \text{ yıl}
$$

Birinci adımı atlayıp doğrudan logaritma almak da yanlış değil, yalnızca
daha uzun. Kural 1 çarpımı ayırıyor:

$$
\ln (3000 \cdot 1.04^t) = \ln 4500
\quad\Rightarrow\quad
\ln 3000 + t \ln 1.04 = \ln 4500
$$

$$
t = \frac{\ln 4500 - \ln 3000}{\ln 1.04} = \frac{8.4118 - 8.0064}{0.0392} \approx 10.34
$$

Aynı sonuç. **Sık yapılan hata** ise $\ln(3000 \cdot 1.04^t)$ ifadesini
$t \cdot \ln(3000 \cdot 1.04)$ diye açmak: kuvvet yalnızca $1.04$'ün üstünde,
3000'in değil.

### Azalan büyüklük

**Soru:** Bir makinenin değeri her yıl %20 düşüyor. Kaç yılda değeri yarıya
iner?

Her yıl değer $0.8$ ile çarpılıyor:

$$
0.8^t = 0.5
\quad\Rightarrow\quad
t = \frac{\ln 0.5}{\ln 0.8} = \frac{-0.6931}{-0.2231} \approx 3.11 \text{ yıl}
$$

İki logaritma da negatif, çünkü $0.5$ ve $0.8$ 1'den küçük. Bölünce
eksiler birbirini götürüyor ve süre pozitif çıkıyor. Sonuç negatif çıksaydı
bu bir uyarı olurdu: azalan bir şeyin büyümesini ya da büyüyen bir şeyin
küçülmesini beklemişsin demektir.

### İki tarafta farklı taban

**Soru:** $2^{x+1} = 5^x$ denklemini çöz.

Tabanlar farklı, birini ötekine çeviremiyoruz. İki tarafın da logaritmasını
al:

$$
\ln 2^{x+1} = \ln 5^x
\quad\Rightarrow\quad
(x + 1)\ln 2 = x \ln 5
$$

Artık üs kalmadı; sıradan bir birinci derece denklem. Parantezi aç ve $x$'li
terimleri bir tarafa topla:

$$
x \ln 2 + \ln 2 = x \ln 5
\quad\Rightarrow\quad
\ln 2 = x \ln 5 - x \ln 2 = x (\ln 5 - \ln 2)
$$

$$
x = \frac{\ln 2}{\ln 5 - \ln 2} = \frac{\ln 2}{\ln 2.5} = \frac{0.6931}{0.9163} \approx 0.7565
$$

**Sağlama:** $2^{1.7565} \approx 3.379$ ve $5^{0.7565} \approx 3.379$.
Paydada $\ln 5 - \ln 2 = \ln \frac{5}{2}$ yazabilmemiz Kural 2 sayesinde.

## Logaritmalı denklemler

Bu kez bilinmeyen logaritmanın **içinde**. Araç ters yönde çalışıyor:
logaritmayı tanım yardımıyla üsse çevirmek.

### Tek logaritma: tanıma çevir

$\log_3 (x - 1) = 2$ ise tanıma göre $3^2 = x - 1$, yani $x = 10$.

**Kontrol et:** $x - 1 = 9 > 0$, logaritma tanımlı. Cevap $x = 10$.

### Birden fazla logaritma: önce birleştir

**Soru:** $\log_2 x + \log_2 (x - 2) = 3$

**1. Kural 1 ile tek logaritmada topla:**

$$
\log_2 \big(x (x - 2)\big) = 3
$$

**2. Tanıma çevir:**

$$
x(x - 2) = 2^3 = 8
\quad\Rightarrow\quad
x^2 - 2x - 8 = 0
$$

**3. İkinci derece denklemi çöz.** Çarpımı $-8$, toplamı $-2$ olan iki sayı
$-4$ ve $2$:

$$
(x - 4)(x + 2) = 0
\quad\Rightarrow\quad
x = 4 \;\text{ ya da }\; x = -2
$$

**4. Her adayı orijinal denklemde kontrol et.**

- $x = 4$: $\log_2 4 + \log_2 2 = 2 + 1 = 3$. ✓
- $x = -2$: $\log_2 (-2)$ tanımsız. ✕

Cebir iki cevap üretti ama yalnızca biri geçerli: **$x = 4$.** Sahte çözüm,
birinci adımda iki logaritmayı birleştirirken ortaya çıktı. $x(x-2)$ çarpımı
$x = -2$ için pozitif ($(-2)(-4) = 8$), oysa tek tek $x$ ve $x - 2$ negatif.
Birleştirmek, orijinal denklemin koyduğu şartı gizledi.

### İki tarafta aynı tabanda logaritma

**Soru:** $\log_5 (2x + 3) = \log_5 (x + 7)$

Logaritma **bire birdir**: iki sayının logaritması eşitse sayıların
kendisi de eşittir. (Grafikteki eğri hep yükseliyor; aynı yüksekliğe iki
farklı noktadan çıkamıyor.)

$$
2x + 3 = x + 7 \quad\Rightarrow\quad x = 4
$$

**Kontrol:** $2 \cdot 4 + 3 = 11 > 0$ ve $4 + 7 = 11 > 0$. Geçerli.

### Kontrol neden şart?

Üstel denklemde sorun çıkmıyor: $b^x$ her $x$ için tanımlı. Logaritmalı
denklemde ise her logaritmanın içi pozitif olmalı ve kuralları uygularken
bu şart gözden kaçabiliyor. Alışkanlık edin: **bulduğun her cevabı orijinal
denklemdeki her logaritmanın içine koy ve pozitif mi diye bak.**

## Logaritmik ölçek

Bir büyüklük çok geniş bir aralığa yayılıyorsa (1'den milyona), düz bir
eksende küçük değerler sıfırın dibine sıkışıyor. Logaritmik ölçekte eksen
**eşit aralıklarla değil, eşit oranlarla** ilerliyor: 1, 10, 100, 1000
arasındaki mesafeler aynı.

Günlük hayatta sandığından sık karşına çıkıyor:

- **Deprem büyüklüğü:** 6 büyüklüğündeki deprem 5'ten 10 kat daha büyük
  genlikte.
- **Ses şiddeti (desibel):** 10 dB artış, ses gücünde 10 kat artış.
- **pH:** pH 3, pH 4'ten 10 kat daha asidik.

Hepsinde ortak fikir: **eşit farklar eşit oranları temsil ediyor.**
Logaritmik ölçekte "iki kat" her yerde aynı uzunlukta.

Bunun matematiksel sebebi Kural 2: $\log 100 - \log 10 = \log \frac{100}{10} = \log 10$
ve $\log 1000 - \log 100 = \log 10$. Farkı belirleyen yalnızca **oran**.

## Makine öğrenmesinde logaritma

Şimdiye kadar anlatılan her şey bu beş yere çıkıyor. İleride bu konuların
her biri kendi bölümünde ayrıntılı gelecek; burada logaritmanın hangi işi
gördüğünü görmek yeterli.

### 1. Çarpımı toplama çevirmek

Bir model 400 bağımsız olayın her birine $0.01$ olasılık veriyorsa, hepsinin
birlikte olma olasılığı çarpım:

$$
0.01^{400} = (10^{-2})^{400} = 10^{-800}
$$

Bilgisayarlar ondalık sayıları sınırlı bir hassasiyette tutuyor ve
yaklaşık $10^{-308}$'den küçük bir sayı **sıfıra yuvarlanıyor**. Sonuç sıfır
olunca iki modeli karşılaştırmak imkânsız: ikisi de "sıfır" diyor.

Çözüm Kural 1 ve Kural 3:

$$
\ln \prod_{i=1}^{400} p_i = \sum_{i=1}^{400} \ln p_i
\qquad\text{burada}\qquad
400 \cdot \ln 0.01 = 400 \cdot (-4.605) = -1842.07
$$

Aynı bilgi, sıradan bir sayı olarak. Logaritma artan bir fonksiyon olduğu
için büyük çarpımın logaritması da büyük; "hangisi daha olası" sorusunun
cevabı değişmiyor. İstatistikte buna **log-olabilirlik** deniyor ve model
eğitmenin büyük kısmı onu en büyük yapmaya çalışmak.

### 2. Kayıp fonksiyonu: log-loss

Sınıflandırma modelleri doğru sınıfa verdikleri olasılıkla
değerlendiriliyor. Doğru sınıfa $p$ olasılık veren bir tahminin cezası:

$$
\text{kayıp} = -\ln p
$$

| Doğru sınıfa verilen olasılık $p$ | $-\ln p$ |
|---|---|
| 0.9 | 0.105 |
| 0.5 | 0.693 |
| 0.1 | 2.303 |
| 0.01 | 4.605 |

Eksi işareti, olasılığın logaritması negatif olduğu için (0 ile 1 arası)
cezayı pozitif yapıyor. Asıl önemli olan tablonun şekli: model emin ve
haklıysa ceza neredeyse sıfır, **emin ve yanlışsa ceza patlıyor.** $p$
sıfıra giderken $-\ln p$ sonsuza gidiyor; "grafikteki sol duvar" burada
modeli kendinden fazla emin olmaktan caydırıyor.

### 3. Çarpık veriyi düzeltmek

Gelir, ev fiyatı, şehir nüfusu gibi büyüklüklerde değerlerin çoğu küçük,
birkaç tanesi devasa. Sekiz kişinin yıllık geliri:

| 18 000 | 22 000 | 25 000 | 31 000 | 40 000 | 55 000 | 90 000 | 2 500 000 |
|---|---|---|---|---|---|---|---|

Ortalama 347 625, medyan 35 500. Tek bir değer ortalamayı on kat yukarı
çekmiş; en büyük değer en küçüğün $\frac{2\,500\,000}{18\,000} \approx 139$ katı.

Her değerin $\log_{10}$'unu alalım:

| 4.255 | 4.342 | 4.398 | 4.491 | 4.602 | 4.740 | 4.954 | 6.398 |
|---|---|---|---|---|---|---|---|

Aradaki uçurum $6.398 - 4.255 = 2.14$ birime indi. Kural 2 bunun nedenini
söylüyor: logaritmada **oran farka dönüşüyor**, $\log_{10} 139 \approx 2.14$.
20 binden 40 bine çıkmak ile 1 milyondan 2 milyona çıkmak aynı mesafe
oluyor.

Değerlerde **sıfır** varsa $\log 0$ tanımsız. O zaman $\ln(1 + x)$
kullanılıyor: $x = 0$ için sonuç $\ln 1 = 0$.

### 4. Algoritmaların hızı

Her adımda problemi yarıya indiren bir yöntem $n$ elemanda $\log_2 n$ adımda
bitiyor. Bir milyar eleman için $\log_2 10^9 \approx 30$ adım. Sıralı bir
listede arama, karar ağaçları ve veritabanı dizinlerinin hızı bu
logaritmadan geliyor.

### 5. Bilgi ve entropi

Olasılığı $p$ olan bir olayın ne kadar "şaşırtıcı" olduğu $-\log_2 p$ bit
ile ölçülüyor: yazı-tura ($p = \frac{1}{2}$) tam $-\log_2 \frac{1}{2} = 1$
bit, olasılığı $\frac{1}{8}$ olan olay $3$ bit. Olay ne kadar
beklenmedikse bilgi o kadar fazla. Karar ağaçlarının hangi soruyu önce
soracağını seçerken kullandığı entropi bu fikirden çıkıyor.

## Kodda karşılığı

Bu bölümün konusu matematik; ama ileride kod yazarken bir farkı bilmen
işine yarar. **Programlama dillerinde tabansız `log` doğal logaritmadır**
($\ln$), okuldaki gibi 10 tabanı değil. 10 ve 2 tabanları için ayrı
fonksiyonlar var (`log10`, `log2`). Logaritmayı kodda kullanmayı Veri
Bilimi ve Makine Öğrenmesi patikalarında göreceksin.

## Özet

- $\log_b x = y$, "$b$'yi kaçıncı kuvvete yükseltirsem $x$ olur?" sorusunun
  cevabı; yani $b^y = x$. Takıldığında bu biçime çevir.
- Sonuç bir üs olduğu için negatif ya da ondalıklı olabilir; ama **argüman
  pozitif olmalı.** Sıfırın ve negatif sayının logaritması yok.
- 1'den küçük sayıların logaritması negatif; olasılıkların logaritması
  hep negatif.
- Üç taban: $\log_{10}$ (basamak), $\ln$ ($e$ tabanı, ML'deki varsayılan),
  $\log_2$ (yarıya bölme, bit).
- Kurallar üs kurallarının tersi: çarpım → toplam, bölüm → fark, kuvvet →
  çarpan. Toplamın logaritması açılmaz.
- **Üstel denklem:** üslü terimi yalnız bırak, iki tarafın logaritmasını al,
  üssü indir.
- **Logaritmalı denklem:** logaritmaları birleştir, tanıma çevir, çöz ve
  **her cevabı kontrol et.**
- ML'de: çarpımı toplama çevirmek, log-loss, çarpık değerleri sıkıştırmak,
  $\log_2 n$ hızı ve entropi.
