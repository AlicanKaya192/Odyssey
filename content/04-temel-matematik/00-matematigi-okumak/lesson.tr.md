# Matematiği Okumak: Semboller ve Terimler

Matematik bir dil. Kendi harfleri (sayılar, değişkenler), kendi
sözcükleri (işlem sembolleri) ve kendi dilbilgisi (işlem önceliği, parantez)
var. Çoğu insanın matematikten korkmasının sebebi aslında işlemler değil,
bu dili okuyamamak: bir formüle bakınca ne dediği anlaşılmıyor ve
"bu bana göre değil" deniyor.

Bu bölüm bir sözlük gibi. Sonraki bütün bölümlerde karşına çıkacak
sembolleri ve terimleri tek tek tanıtıyor, her birinin **nasıl
okunduğunu** ve **ne anlama geldiğini** söylüyor. Burada hiçbir şeyi
ezberlemen gerekmiyor; takıldığında geri dönüp bakacağın bir yer
olarak düşün.

Ön bilgi: yok. Bu, patikanın ilk bölümü.

## Sayılar ve sayı kümeleri

Matematikte sayılar, özelliklerine göre **kümelere** ayrılır. Her küme
bir öncekini içine alır ve yeni bir şeye izin verir.

| Sembol | Adı | İçindekiler | Yeni ne getiriyor? |
|---|---|---|---|
| $\mathbb{N}$ | Doğal sayılar | $0, 1, 2, 3, \dots$ | Saymak |
| $\mathbb{Z}$ | Tam sayılar | $\dots, -2, -1, 0, 1, 2, \dots$ | Negatif sayılar (borç, sıfırın altı) |
| $\mathbb{Q}$ | Rasyonel sayılar | $\tfrac{1}{2}$, $-\tfrac{3}{4}$, $0.75$ … | Kesirler: iki tam sayının oranı |
| $\mathbb{R}$ | Gerçel sayılar | $\sqrt{2}$, $\pi$ … ve öncekilerin hepsi | Sayı doğrusundaki her nokta |

<figure class="fig">
<svg viewBox="0 0 420 230" width="420"><rect class="curve3" x="8" y="8" width="404" height="214" rx="16"/><text class="ink" x="20" y="28" font-size="12" text-anchor="start">ℝ  Gerçel</text><rect class="curve4" x="26" y="34" width="290" height="170" rx="16"/><text class="ink" x="38" y="54" font-size="12" text-anchor="start">ℚ  Rasyonel</text><rect class="curve2" x="44" y="60" width="182" height="126" rx="16"/><text class="ink" x="56" y="80" font-size="12" text-anchor="start">ℤ  Tam</text><rect class="curve" x="62" y="86" width="84" height="82" rx="16"/><text class="ink" x="74" y="106" font-size="12" text-anchor="start">ℕ  Doğal</text><text class="ink" x="84" y="136" font-size="14" text-anchor="middle">0</text><text class="ink" x="104" y="150" font-size="14" text-anchor="middle">1</text><text class="ink" x="124" y="136" font-size="14" text-anchor="middle">7</text><text class="ink" x="170" y="120" font-size="14" text-anchor="middle">−3</text><text class="ink" x="170" y="156" font-size="14" text-anchor="middle">−1</text><text class="ink" x="258" y="104" font-size="14" text-anchor="middle">1/2</text><text class="ink" x="262" y="150" font-size="14" text-anchor="middle">−0.75</text><text class="ink" x="258" y="184" font-size="14" text-anchor="middle">2/3</text><text class="ink" x="358" y="90" font-size="14" text-anchor="middle">√2</text><text class="ink" x="360" y="136" font-size="14" text-anchor="middle">π</text><text class="ink" x="356" y="182" font-size="14" text-anchor="middle">−√5</text></svg>
  <figcaption>Sayı kümeleri iç içe: her doğal sayı bir tam sayı, her tam sayı bir rasyonel sayı, her rasyonel sayı bir gerçel sayı. $\sqrt{2}$ ve $\pi$ gibi sayılar gerçel ama rasyonel değil: hiçbir kesirle tam olarak yazılamıyorlar.</figcaption>
</figure>

$\sqrt{2}$ ya da $\pi$ gibi, gerçel olup kesir olarak yazılamayan sayılara
**irrasyonel** sayılar denir. Ondalık yazılışları hiç bitmez ve tekrar
etmez: $\pi = 3.14159265\dots$

**Not:** Bazı kitaplar doğal sayıları $1$'den başlatır ve $0$'ı dahil
etmez. Türkiye'deki müfredatta $0$ doğal sayıdır; $1, 2, 3, \dots$'e
**sayma sayıları** denir.

### Küme sembolleri

| Sembol | Okunuşu | Örnek |
|---|---|---|
| $\in$ | "elemanıdır" | $3 \in \mathbb{N}$: 3 bir doğal sayıdır |
| $\notin$ | "elemanı değildir" | $-3 \notin \mathbb{N}$ |
| $\subset$ | "alt kümesidir" | $\mathbb{N} \subset \mathbb{Z}$ |
| $\{\ \}$ | küme parantezi | $\{1, 2, 3\}$: 1, 2 ve 3'ten oluşan küme |

Kümeleri ayrıntısıyla Kümeler ve Mantık bölümünde göreceğiz; şimdilik
okuyabilmek yeterli.

## Değişkenler ve sabitler

Bir sayının değerini bilmediğimizde ya da **her** sayı için geçerli bir
şey söylemek istediğimizde onun yerine bir harf yazarız. Bu harfe
**değişken** denir.

- "Bir sayının 3 fazlası" yerine $x + 3$.
- "Her sayı için, sayıyı 0 ile toplamak onu değiştirmez" yerine
  $a + 0 = a$.

Değeri sabit kalan harflere **sabit** denir: $\pi \approx 3.14159$ hiç
değişmez. Bir problemde "$a$ bir sabit" dendiğinde, $a$'nın belirli ama
bize söylenmemiş bir sayı olduğu anlaşılır.

Harflerin seçimi keyfî ama gelenekler var:

| Harfler | Genelde ne için? |
|---|---|
| $x, y, z$ | Bilinmeyenler, değişkenler |
| $a, b, c$ | Sabitler, katsayılar |
| $n, m, k$ | Tam sayılar, sayaçlar ("$n$ tane") |
| $i, j$ | Sıra numaraları (1., 2., 3. eleman) |
| $f, g, h$ | Fonksiyonlar |
| $t$ | Zaman |

### Yunan harfleri

Latin harfleri yetmediğinde Yunan alfabesi kullanılır. Makine
öğrenmesinde en sık karşına çıkacaklar:

| Harf | Okunuşu | Tipik kullanımı |
|---|---|---|
| $\alpha$ | alfa | Öğrenme oranı, açı |
| $\beta$ | beta | Katsayılar, ağırlıklar |
| $\gamma$ | gama | İndirim oranı |
| $\delta$, $\Delta$ | delta | Küçük değişim, fark ($\Delta x$: "$x$'teki değişim") |
| $\varepsilon$ | epsilon | Çok küçük bir sayı, hata |
| $\theta$ | teta | Açı, bir modelin parametreleri |
| $\lambda$ | lambda | Düzenlileştirme katsayısı, özdeğer |
| $\mu$ | mü | Ortalama |
| $\pi$ | pi | $3.14159\dots$ (çemberin çevresi / çapı) |
| $\sigma$, $\Sigma$ | sigma | Standart sapma; büyük hâli toplam sembolü |
| $\varphi$ | fi | Açı, özel fonksiyonlar |

Aynı harfin küçük ve büyük hâli çoğu zaman farklı şeyler anlatır: $\sigma$
standart sapma, $\Sigma$ ise toplam sembolü.

## İşlem sembolleri

| Sembol | Okunuşu | Örnek |
|---|---|---|
| $+$ | artı | $5 + 3 = 8$ |
| $-$ | eksi | $5 - 3 = 2$ |
| $\times$, $\cdot$ | çarpı | $5 \times 3 = 5 \cdot 3 = 15$ |
| $\div$, $/$, kesir çizgisi | bölü | $15 \div 3 = 15/3 = \tfrac{15}{3} = 5$ |
| $a^n$ | "$a$ üssü $n$", "$a$'nın $n$. kuvveti" | $2^3 = 2 \cdot 2 \cdot 2 = 8$ |
| $\sqrt{a}$ | "karekök $a$" | $\sqrt{9} = 3$ |
| $\lvert a \rvert$ | "$a$'nın mutlak değeri" | $\lvert -4 \rvert = 4$ |

### Yan yana yazmak çarpmak demek

Harflerle çalışırken çarpma işareti çoğu zaman yazılmaz:

$$
2x = 2 \cdot x
\qquad
ab = a \cdot b
\qquad
3(x + 1) = 3 \cdot (x + 1)
$$

**Dikkat:** Bu kural yalnızca harflerle geçerli. $23$, "2 çarpı 3" değil
yirmi üç sayısı. $2x$ ise "2 çarpı $x$"; $x = 5$ ise $2x = 10$, $25$
değil.

$\times$ işareti harf $x$ ile karışmasın diye cebirde nokta ($\cdot$)
tercih edilir.

### Kesir çizgisi bir parantezdir

$$
\frac{6 + 4}{2} = \frac{10}{2} = 5
$$

Kesir çizgisinin üstündeki ve altındaki her şey önce kendi içinde
hesaplanır. Aynı ifadeyi tek satırda yazarken parantez şart:
$(6 + 4) / 2 = 5$, ama $6 + 4 / 2 = 6 + 2 = 8$.

### Parantezler

$(\ )$, $[\ ]$ ve $\{\ \}$ gruplamak için kullanılır; iç içe
parantezlerde okumayı kolaylaştırmak için farklı türler seçilir:

$$
2 \cdot [3 + (4 - 1)] = 2 \cdot [3 + 3] = 2 \cdot 6 = 12
$$

İçteki parantezden dışarı doğru çözülür. Hangi işlemin önce yapıldığını
bir sonraki bölümde (İşlem Önceliği) ayrıntısıyla göreceğiz.

## İlişki sembolleri

Bu semboller iki şeyin **birbirine göre nasıl olduğunu** söyler; sonuç
bir sayı değil, doğru ya da yanlış bir cümledir.

| Sembol | Okunuşu | Örnek |
|---|---|---|
| $=$ | eşittir | $2 + 3 = 5$ |
| $\ne$ | eşit değildir | $2 + 3 \ne 6$ |
| $<$ | küçüktür | $3 < 5$ |
| $>$ | büyüktür | $5 > 3$ |
| $\le$ | küçük ya da eşittir | $x \le 10$: $x$ en fazla 10 |
| $\ge$ | büyük ya da eşittir | $x \ge 0$: $x$ negatif değil |
| $\approx$ | yaklaşık eşittir | $\pi \approx 3.14$ |
| $\Rightarrow$ | ise, gerektirir | $x = 2 \Rightarrow x^2 = 4$ |
| $\iff$ | ancak ve ancak | $x + 1 = 3 \iff x = 2$ |

**$<$ ile $>$'yi karıştırmamak için:** Sembolün açık ağzı her zaman
**büyük** sayıya bakar. $3 < 5$'te ağız 5'e açılıyor.

**Zincir eşitsizlik:** $-2 < x \le 3$, "$x$, $-2$'den büyük ve $3$'ten
küçük ya da ona eşit" demek. Tam sayılardan bu koşulu sağlayanlar
$-1, 0, 1, 2, 3$.

**$\Rightarrow$ tek yönlüdür.** $x = 2 \Rightarrow x^2 = 4$ doğru, ama
tersi değil: $x^2 = 4$ iken $x = -2$ de olabilir.

## İfade, terim, katsayı: bir formülün parçaları

<figure class="fig">
<svg viewBox="0 0 400 176" width="400"><text class="ink" x="85" y="118" font-size="34" text-anchor="middle">3</text><text class="ink" x="110" y="118" font-size="34" text-anchor="middle">x</text><text class="ink" x="165" y="118" font-size="34" text-anchor="middle">−</text><text class="ink" x="205" y="118" font-size="34" text-anchor="middle">5</text><text class="ink" x="230" y="118" font-size="34" text-anchor="middle">x</text><text class="ink" x="275" y="118" font-size="34" text-anchor="middle">+</text><text class="ink" x="320" y="118" font-size="34" text-anchor="middle">7</text><text class="ink" x="130" y="100" font-size="18" text-anchor="middle">2</text><line class="curve" x1="85" y1="58" x2="85" y2="84"/><text class="ink" x="85" y="50" font-size="12" text-anchor="middle">katsayı</text><line class="curve2" x1="130" y1="38" x2="130" y2="80"/><text class="ink" x="130" y="30" font-size="12" text-anchor="middle">üs</text><line class="curve4" x1="230" y1="58" x2="230" y2="90"/><text class="ink" x="230" y="50" font-size="12" text-anchor="middle">değişken</text><path class="curve3" d="M68,132 v8 H142 v-8" fill="none"/><text class="ink" x="105.0" y="162" font-size="12" text-anchor="middle">1. terim</text><path class="curve3" d="M152,132 v8 H248 v-8" fill="none"/><text class="ink" x="200.0" y="162" font-size="12" text-anchor="middle">2. terim</text><path class="curve3" d="M262,132 v8 H338 v-8" fill="none"/><text class="ink" x="300.0" y="162" font-size="12" text-anchor="middle">sabit terim</text></svg>
  <figcaption>$3x^2 - 5x + 7$ ifadesi üç terimden oluşuyor. Bir terimde harfin önündeki sayı katsayı (mor), harfin sağ üstündeki küçük sayı üs (turuncu). Harf içermeyen terime sabit terim denir.</figcaption>
</figure>

| Terim | Anlamı | Örnek |
|---|---|---|
| **İfade** | Sayı, harf ve işlemlerden oluşan bir yazı; eşittir işareti yok | $3x^2 - 5x + 7$ |
| **Terim** | İfadenin $+$ ve $-$ ile ayrılan parçaları | $3x^2$, $-5x$, $7$ |
| **Katsayı** | Bir terimde harfle çarpılan sayı | $3x^2$'de $3$; $-5x$'te $-5$ |
| **Sabit terim** | Harf içermeyen terim | $7$ |
| **Denklem** | İki ifadenin eşit olduğunu söyleyen cümle | $2x + 1 = 7$ |
| **Eşitsizlik** | Birinin ötekinden büyük ya da küçük olduğunu söyleyen cümle | $2x + 1 < 7$ |
| **Formül** | Bir niceliği başka niceliklerle hesaplayan eşitlik | Dikdörtgenin alanı $A = a \cdot b$ |
| **Özdeşlik** | Her değer için doğru olan eşitlik | $a + b = b + a$ |

**Katsayının işareti terime aittir:** $3x^2 - 5x + 7$'de $x$'in katsayısı
$5$ değil $-5$. İfadeyi $3x^2 + (-5x) + 7$ diye düşün.

**$x$'in katsayısı 1:** $x$ yazıldığında önünde görünmeyen bir $1$ vardır;
$-x$'in katsayısı $-1$.

### Değer yerine koymak

Bir ifadenin değerini bulmak için harfin yerine sayıyı yazarız. $x = 2$
için:

$$
\begin{aligned}
3x^2 - 5x + 7 &= 3 \cdot 2^2 - 5 \cdot 2 + 7 \\
&= 3 \cdot 4 - 10 + 7 \\
&= 12 - 10 + 7 = 9
\end{aligned}
$$

Negatif bir sayı koyarken **parantez kullan**: $x = -2$ için
$3 \cdot (-2)^2 - 5 \cdot (-2) + 7 = 12 + 10 + 7 = 29$.

### İfade ile denklem arasındaki fark

İfade bir **isim** gibidir: bir şeyi anlatır ama bir iddiada bulunmaz.
Denklem ise bir **cümledir**: "bu ikisi eşittir" der ve bu doğru ya da
yanlış olabilir. $2x + 1$ bir ifade; $2x + 1 = 7$ bir denklem ve yalnızca
$x = 3$ iken doğru. İfadeyi **sadeleştirir** ya da **hesaplarız**;
denklemi **çözeriz**.

## Alt simge ve üst simge

Harfin **sağ üstündeki** küçük sayı üstür, **sağ altındaki** küçük sayı
**alt simge** (indis):

| Yazılış | Okunuşu | Anlamı |
|---|---|---|
| $x^2$ | "$x$ kare" | $x \cdot x$ |
| $x_2$ | "$x$ iki", "$x$ alt iki" | $x$ adlı değişkenlerden **ikincisi** |
| $x_i$ | "$x$ alt $i$" | $i$. eleman |
| $a_{ij}$ | "$a$ alt $i$ $j$" | bir tablonun $i$. satır, $j$. sütundaki elemanı |

Alt simge bir işlem yapmaz, yalnızca bir **ad**dır. Beş evin fiyatını
$x_1, x_2, x_3, x_4, x_5$ diye adlandırabiliriz; $x_3$ üçüncü evin
fiyatı. Çok sayıda eleman olduğunda "ve böyle devam eder" üç noktayla
söylenir: $x_1, x_2, \dots, x_n$ "$x_1$'den $x_n$'ye kadar, $n$ tane".

## Toplam sembolü Σ

Çok sayıda terimi toplamak için büyük sigma kullanılır:

$$
\sum_{i=1}^{4} x_i = x_1 + x_2 + x_3 + x_4
$$

Okunuşu: "$i$, 1'den 4'e kadar, $x_i$'lerin toplamı". Altındaki $i = 1$
nereden başladığını, üstündeki $4$ nerede bittiğini söyler. Bir örnek:

$$
\sum_{i=1}^{4} i = 1 + 2 + 3 + 4 = 10
$$

Makine öğrenmesinde bu sembol her yerde; ayrıntısını Diziler ve Seriler
bölümünde göreceğiz.

## Fonksiyon gösterimi

$f(x) = 2x + 1$ şunu söyler: "$f$ adında bir kural var; ona bir $x$ ver,
sana $2x + 1$ versin". $f(3)$, kurala $3$ vermek demek:

$$
f(3) = 2 \cdot 3 + 1 = 7
$$

**Dikkat:** $f(x)$, "$f$ çarpı $x$" **değil**. Parantez burada kurala
verilen girdiyi gösteriyor. Fonksiyonları kendi bölümünde ayrıntısıyla
göreceğiz.

## Formülleri sesli okumak

Bir formülü anlamanın en iyi yolu onu sesli okumaktır.

| Formül | Okunuşu |
|---|---|
| $x^2 + y^2 = r^2$ | "$x$ kare artı $y$ kare eşittir $r$ kare" |
| $\frac{a + b}{2}$ | "$a$ artı $b$'nin yarısı" (ya da "bölü iki") |
| $\lvert x - 3 \rvert \le 1$ | "$x$ eksi 3'ün mutlak değeri 1'den küçük ya da eşit" |
| $x_1 + x_2 + \cdots + x_n$ | "$x$ bir artı $x$ iki artı … artı $x$ $n$" |
| $f(x) = 3x - 1$ | "$f$ $x$ eşittir 3 $x$ eksi 1" |

## Makine öğrenmesinde bir formül okumak

Doğrusal bir modelin tahmini:

$$
\hat{y} = w_1 x_1 + w_2 x_2 + b
$$

Parça parça:

- $\hat{y}$ ("$y$ şapka"): modelin **tahmini**. Şapka "tahmin edilen"
  demek; gerçek değer şapkasız $y$.
- $x_1, x_2$: evin özellikleri, örneğin metrekare ve oda sayısı.
- $w_1, w_2$: her özelliğin **ağırlığı** (weight): o özelliğin tahmine
  ne kadar katkı yaptığı.
- $b$: sabit terim (bias).

$w_1 = 2$, $w_2 = 10$, $b = 5$ ve bir ev için $x_1 = 100$, $x_2 = 3$ ise:

$$
\hat{y} = 2 \cdot 100 + 10 \cdot 3 + 5 = 200 + 30 + 5 = 235
$$

Bir de hata ölçüsü: **ortalama kare hata**

$$
\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

"1 bölü $n$ çarpı, $i$ 1'den $n$'ye kadar, $y_i$ eksi $\hat{y}_i$'nin
karelerinin toplamı". Yani: her örnekte gerçek değerle tahmin arasındaki
farkı al, karesini al, hepsini topla, örnek sayısına böl. Bu cümleyi
okuyabiliyorsan formülü de okuyabiliyorsun.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$x^2$ ile $x_2$ aynı şey</p>
      <p>$x = 5$ iken $2x = 25$</p>
      <p>$f(x)$ = $f$ çarpı $x$</p>
      <p>$3x^2 - 5x$'te $x$'in katsayısı $5$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$x^2 = x \cdot x$; $x_2$ ikinci $x$</p>
      <p>$2x = 2 \cdot 5 = 10$</p>
      <p>$f(x)$: $f$ kuralına $x$ verilince çıkan değer</p>
      <p>Katsayı işaretiyle birlikte: $-5$</p>
    </div>
  </div>
  <figcaption>Semboller küçük ama farkları büyük: üst simge işlem, alt simge ad.</figcaption>
</figure>

- **Negatif sayıyı parantezsiz koymak.** $x = -3$ için $x^2$, $(-3)^2 = 9$;
  $-3^2$ yazarsan $-9$ okunur.
- **$=$ işaretini "sonra" anlamında kullanmak.** $2 + 3 = 5 \cdot 2 = 10$
  yanlış bir yazı, çünkü $2 + 3 \ne 10$. Her $=$'in iki yanı gerçekten eşit
  olmalı; ara sonuçları ayrı satırlara yaz.
- **$<$ ve $>$'yi ters okumak.** Açık ağız büyük sayıya bakar.

## Özet

- Sayı kümeleri iç içe: $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$; $\sqrt{2}$, $\pi$ irrasyonel.
- Değişken: değeri bilinmeyen ya da her değeri alabilen harf; sabit: değişmeyen.
- Yan yana yazmak çarpmak: $2x = 2 \cdot x$, $3(x + 1) = 3 \cdot (x + 1)$.
- Kesir çizgisi parantez gibi davranır.
- İlişki sembolleri ($=, \ne, <, >, \le, \ge, \approx$) doğru ya da yanlış bir cümle kurar.
- İfade: terimlerden oluşur; terimde katsayı (işaretiyle), değişken ve üs var. Denklem: iki ifadenin eşitliği.
- Üst simge işlemdir ($x^2$), alt simge addır ($x_2$).
- $\sum_{i=1}^{n} x_i$: $x_1$'den $x_n$'ye kadar topla. $f(x)$: $f$ kuralına $x$ ver.
- ML formüllerini parça parça ve sesli oku: $\hat{y} = w_1x_1 + w_2x_2 + b$.
