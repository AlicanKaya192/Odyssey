# Sayma: Permütasyon ve Kombinasyon

"Kaç farklı yolu var?" sorusu olasılığın temeli: bir olayın olasılığı
çoğu zaman "istenen durum sayısı bölü bütün durumların sayısı". Durumları
tek tek yazmak birkaç taneden sonra imkânsızlaşır; bu bölümde onları
yazmadan saymayı öğreneceğiz. Makine öğrenmesinde de sayma her yerde:
hiperparametre aramasında kaç model eğitileceği, $20$ özellikten kaç
farklı alt küme seçilebileceği, bir veri setinde kaç çift karşılaştırma
yapılacağı birer sayma sorusu. Çarpma ilkesini, faktöriyeli, permütasyonu,
kombinasyonu ve hangisinin ne zaman kullanılacağını göreceğiz.

Ön bilgi: Doğal Sayılar ve İşlem Önceliği, Üslü Sayılar, Kümeler ve
Mantık.

## Toplama ilkesi

Seçenekler **ayrı gruplardan** geliyorsa ve yalnızca birini seçiyorsan
sayılar toplanır. Menüde $3$ tatlı ve $4$ meyve varsa bir tatlı **ya da**
bir meyve seçmenin $3 + 4 = 7$ yolu var.

Koşul, grupların ortak elemanı olmaması. Ortak eleman varsa iki kez
sayılır; Kümeler bölümündeki $s(A \cup B) = s(A) + s(B) - s(A \cap B)$
bunu düzeltir.

## Çarpma ilkesi

Bir iş **adım adım** yapılıyorsa ve her adımın seçenek sayısı öncekilere
bağlı değilse, sayılar **çarpılır**. $2$ gömlek ve $3$ pantolonla
$2 \cdot 3 = 6$ farklı kombin yapılır: her gömleğin yanına üç pantolon
gelir.

<figure class="fig">
<svg viewBox="0 0 470 264" width="470"><rect class="box" x="22.0" y="117.0" width="56" height="26" rx="6"/><text class="ink" x="50" y="134" font-size="11" text-anchor="middle">başla</text><line class="curve3" x1="78" y1="130" x2="134" y2="70"/><rect class="box" x="134.0" y="57.0" width="72" height="26" rx="6"/><text class="ink" x="170" y="74" font-size="11" text-anchor="middle">gömlek 1</text><line class="curve3" x1="206" y1="70" x2="266" y2="30"/><rect class="box" x="266.0" y="17.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="34" font-size="11" text-anchor="middle">kot</text><line class="curve3" x1="206" y1="70" x2="266" y2="70"/><rect class="box" x="266.0" y="57.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="74" font-size="11" text-anchor="middle">kumaş</text><line class="curve3" x1="206" y1="70" x2="266" y2="110"/><rect class="box" x="266.0" y="97.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="114" font-size="11" text-anchor="middle">şort</text><line class="curve3" x1="78" y1="130" x2="134" y2="190"/><rect class="box" x="134.0" y="177.0" width="72" height="26" rx="6"/><text class="ink" x="170" y="194" font-size="11" text-anchor="middle">gömlek 2</text><line class="curve3" x1="206" y1="190" x2="266" y2="150"/><rect class="box" x="266.0" y="137.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="154" font-size="11" text-anchor="middle">kot</text><line class="curve3" x1="206" y1="190" x2="266" y2="190"/><rect class="box" x="266.0" y="177.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="194" font-size="11" text-anchor="middle">kumaş</text><line class="curve3" x1="206" y1="190" x2="266" y2="230"/><rect class="box" x="266.0" y="217.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="234" font-size="11" text-anchor="middle">şort</text><text class="ink" x="400" y="134" font-size="12" text-anchor="middle">2 · 3 = 6 kombin</text></svg>
  <figcaption>Seçim ağacı: ilk adımda 2 dal, her dalın ucunda 3 dal daha. Yapraklar bütün kombinler; 2 · 3 = 6 tane.</figcaption>
</figure>

- $4$ haneli bir PIN kodu: her hane $10$ seçenek, $10^4 = 10\,000$ kod.
- Her soruda $4$ şık olan $10$ soruluk test: $4^{10} = 1\,048\,576$ farklı
  cevap kâğıdı.
- $3$ öğrenme oranı, $4$ ağaç derinliği ve $5$ ağaç sayısı: $3 \cdot 4 \cdot 5
  = 60$ farklı ayar.

**Tekrarlı sıralı seçim.** $n$ seçenekten $k$ kez, her seferinde yine
bütün seçenekler açıkken seçilirse sonuç $n^k$.

## Faktöriyel

$n$ farklı nesne kaç farklı sırada dizilir? İlk yere $n$, ikinciye
$n - 1$, … sonuncuya $1$ seçenek kalır:

$$
n! = n \cdot (n - 1) \cdot (n - 2) \cdots 2 \cdot 1
$$

"$n$ faktöriyel" diye okunur. $3! = 6$, $5! = 120$, $10! = 3\,628\,800$.
Faktöriyel üstelden bile hızlı büyür: $52$ kartlık bir destenin
dizilişlerinin sayısı $52!$, yaklaşık $8 \cdot 10^{67}$.

**$0! = 1$.** Hiç nesneyi dizmenin tek bir yolu var: hiçbir şey yapmamak.
Formüllerin de tutarlı çalışması için bu tanım gerekir.

## Permütasyon: sıra önemli

$n$ nesneden $k$ tanesini **sıralı** seçmek (dizmek). Çarpma ilkesiyle
$n \cdot (n - 1) \cdots (n - k + 1)$; bu, $n!$'in son $n - k$ çarpanı
atılmış hâli:

$$
P(n, k) = \frac{n!}{(n - k)!}
$$

$8$ koşucudan birinci, ikinci ve üçüncü kaç farklı şekilde çıkar?
$P(8, 3) = 8 \cdot 7 \cdot 6 = 336$.

**Tekrarlı nesneler.** Bazı nesneler birbirinin aynısıysa aralarındaki
yer değiştirmeler yeni bir diziliş vermez; o yüzden bölünür. "KAYAK"
kelimesinin harfleri: $5$ harf, iki K, iki A:

$$
\frac{5!}{2! \cdot 2!} = \frac{120}{4} = 30
$$

## Kombinasyon: sıra önemsiz

$n$ nesneden $k$ tanesini **sırasız** seçmek (bir grup oluşturmak). Her
grup, $k!$ farklı sırayla dizilebilir; permütasyon her grubu $k!$ kez
saymış olur. Bu yüzden:

$$
C(n, k) = \binom{n}{k} = \frac{n!}{k! \, (n - k)!}
$$

<figure class="fig">
<svg viewBox="0 0 440 186" width="440"><text class="ink" x="110" y="22" font-size="12" text-anchor="middle">sıra önemli: 3 · 2 = 6</text><text class="dim" x="110" y="40" font-size="11" text-anchor="middle">başkan–yardımcı</text><text class="ink" x="330" y="22" font-size="12" text-anchor="middle">sıra önemsiz: 6 / 2 = 3</text><text class="dim" x="330" y="40" font-size="11" text-anchor="middle">iki kişilik ekip</text><rect class="box" x="56.0" y="59.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="76" font-size="11" text-anchor="middle">AB</text><rect class="box" x="116.0" y="59.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="76" font-size="11" text-anchor="middle">BA</text><line class="curve2" x1="172" y1="72" x2="282" y2="72" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="59.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="76" font-size="11" text-anchor="middle">{A, B}</text><rect class="box" x="56.0" y="101.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="118" font-size="11" text-anchor="middle">AC</text><rect class="box" x="116.0" y="101.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="118" font-size="11" text-anchor="middle">CA</text><line class="curve2" x1="172" y1="114" x2="282" y2="114" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="101.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="118" font-size="11" text-anchor="middle">{A, C}</text><rect class="box" x="56.0" y="143.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="160" font-size="11" text-anchor="middle">BC</text><rect class="box" x="116.0" y="143.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="160" font-size="11" text-anchor="middle">CB</text><line class="curve2" x1="172" y1="156" x2="282" y2="156" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="143.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="160" font-size="11" text-anchor="middle">{B, C}</text></svg>
  <figcaption>A, B, C'den iki kişi. Başkan ve yardımcı seçiliyorsa AB ile BA farklı: 6 yol. İki kişilik ekipte ikisi aynı ekip: her çift bir kez sayılır, 6 / 2! = 3 yol.</figcaption>
</figure>

$10$ kişiden $3$ kişilik komite: $\binom{10}{3} = \frac{10 \cdot 9 \cdot
8}{3 \cdot 2 \cdot 1} = 120$. Başkan, yardımcı ve sekreter seçilseydi
$P(10, 3) = 720 = 120 \cdot 3!$ olurdu.

**Simetri.** $k$ kişiyi seçmek, geride kalacak $n - k$ kişiyi seçmekle
aynı: $\binom{n}{k} = \binom{n}{n - k}$. $\binom{10}{7} = \binom{10}{3}
= 120$.

**Pascal üçgeni.** $\binom{n}{k}$ sayıları bir üçgende dizilince her sayı
üstündeki iki sayının toplamı çıkar:
$\binom{n}{k} = \binom{n - 1}{k - 1} + \binom{n - 1}{k}$. Sebep: belli bir
kişi ya gruptadır (öteki $k - 1$ kişi $n - 1$ kişiden seçilir) ya da
değildir ($k$ kişinin hepsi $n - 1$ kişiden).

<figure class="fig">
<svg viewBox="0 0 440 270" width="440"><circle class="box" cx="220.0" cy="26" r="14"/><text class="ink" x="220.0" y="30" font-size="11" text-anchor="middle">1</text><circle class="box" cx="202.0" cy="58" r="14"/><text class="ink" x="202.0" y="62" font-size="11" text-anchor="middle">1</text><circle class="box" cx="238.0" cy="58" r="14"/><text class="ink" x="238.0" y="62" font-size="11" text-anchor="middle">1</text><circle class="box" cx="184.0" cy="90" r="14"/><text class="ink" x="184.0" y="94" font-size="11" text-anchor="middle">1</text><circle class="box" cx="220.0" cy="90" r="14"/><text class="ink" x="220.0" y="94" font-size="11" text-anchor="middle">2</text><circle class="box" cx="256.0" cy="90" r="14"/><text class="ink" x="256.0" y="94" font-size="11" text-anchor="middle">1</text><circle class="box" cx="166.0" cy="122" r="14"/><text class="ink" x="166.0" y="126" font-size="11" text-anchor="middle">1</text><circle class="dot2" opacity="0.55" cx="202.0" cy="122" r="14"/><text class="ink" x="202.0" y="126" font-size="11" text-anchor="middle">3</text><circle class="dot2" opacity="0.55" cx="238.0" cy="122" r="14"/><text class="ink" x="238.0" y="126" font-size="11" text-anchor="middle">3</text><circle class="box" cx="274.0" cy="122" r="14"/><text class="ink" x="274.0" y="126" font-size="11" text-anchor="middle">1</text><circle class="box" cx="148.0" cy="154" r="14"/><text class="ink" x="148.0" y="158" font-size="11" text-anchor="middle">1</text><circle class="box" cx="184.0" cy="154" r="14"/><text class="ink" x="184.0" y="158" font-size="11" text-anchor="middle">4</text><circle class="dot3" opacity="0.55" cx="220.0" cy="154" r="14"/><text class="ink" x="220.0" y="158" font-size="11" text-anchor="middle">6</text><circle class="box" cx="256.0" cy="154" r="14"/><text class="ink" x="256.0" y="158" font-size="11" text-anchor="middle">4</text><circle class="box" cx="292.0" cy="154" r="14"/><text class="ink" x="292.0" y="158" font-size="11" text-anchor="middle">1</text><circle class="box" cx="130.0" cy="186" r="14"/><text class="ink" x="130.0" y="190" font-size="11" text-anchor="middle">1</text><circle class="box" cx="166.0" cy="186" r="14"/><text class="ink" x="166.0" y="190" font-size="11" text-anchor="middle">5</text><circle class="box" cx="202.0" cy="186" r="14"/><text class="ink" x="202.0" y="190" font-size="11" text-anchor="middle">10</text><circle class="box" cx="238.0" cy="186" r="14"/><text class="ink" x="238.0" y="190" font-size="11" text-anchor="middle">10</text><circle class="box" cx="274.0" cy="186" r="14"/><text class="ink" x="274.0" y="190" font-size="11" text-anchor="middle">5</text><circle class="box" cx="310.0" cy="186" r="14"/><text class="ink" x="310.0" y="190" font-size="11" text-anchor="middle">1</text><circle class="box" cx="112.0" cy="218" r="14"/><text class="ink" x="112.0" y="222" font-size="11" text-anchor="middle">1</text><circle class="box" cx="148.0" cy="218" r="14"/><text class="ink" x="148.0" y="222" font-size="11" text-anchor="middle">6</text><circle class="box" cx="184.0" cy="218" r="14"/><text class="ink" x="184.0" y="222" font-size="11" text-anchor="middle">15</text><circle class="box" cx="220.0" cy="218" r="14"/><text class="ink" x="220.0" y="222" font-size="11" text-anchor="middle">20</text><circle class="box" cx="256.0" cy="218" r="14"/><text class="ink" x="256.0" y="222" font-size="11" text-anchor="middle">15</text><circle class="box" cx="292.0" cy="218" r="14"/><text class="ink" x="292.0" y="222" font-size="11" text-anchor="middle">6</text><circle class="box" cx="328.0" cy="218" r="14"/><text class="ink" x="328.0" y="222" font-size="11" text-anchor="middle">1</text><text class="dim" x="22" y="30" font-size="10" text-anchor="start">n = 0</text><text class="dim" x="22" y="62" font-size="10" text-anchor="start">n = 1</text><text class="dim" x="22" y="94" font-size="10" text-anchor="start">n = 2</text><text class="dim" x="22" y="126" font-size="10" text-anchor="start">n = 3</text><text class="dim" x="22" y="158" font-size="10" text-anchor="start">n = 4</text><text class="dim" x="22" y="190" font-size="10" text-anchor="start">n = 5</text><text class="dim" x="22" y="222" font-size="10" text-anchor="start">n = 6</text><text class="ink" x="220" y="256" font-size="11" text-anchor="middle">her sayı üstündeki iki sayının toplamı; 4. satırda 2. sıradaki C(4, 2) = 6</text></svg>
  <figcaption>Pascal üçgeninin ilk yedi satırı. Yeşil 6, üstündeki iki turuncu 3'ün toplamı. n. satırın sayıları C(n, 0), C(n, 1), …, C(n, n); toplamları 2ⁿ.</figcaption>
</figure>

**Alt küme sayısı.** $n$ elemanlı bir kümenin $2^n$ alt kümesi var: her
eleman için "al" ya da "alma" diye iki seçenek. Pascal üçgeninin bir
satırının toplamı bu yüzden $2^n$.

## Hangi formül?

Dört soruyu sırayla sor: kaç nesneden seçiliyor ($n$), kaç tane
seçiliyor ($k$), **sıra önemli mi**, **aynı nesne tekrar seçilebilir mi**?

| Sıra önemli mi? | Tekrar var mı? | Sayı | Örnek |
|---|---|---|---|
| evet | evet | $n^k$ | PIN kodu |
| evet | hayır | $P(n, k) = \dfrac{n!}{(n - k)!}$ | yarışta ilk üç |
| hayır | hayır | $\binom{n}{k}$ | komite |
| hayır | evet | $\binom{n + k - 1}{k}$ | $3$ çeşitten $5$ dondurma topu |

Son satır daha az karşılaşılan durum: $3$ çeşitten tekrar serbest $5$ top
seçmek $\binom{7}{5} = 21$ yol.

**Sıra önemli mi testi:** seçilenlerin yerini değiştir. Sonuç değişiyorsa
(birinci ile ikinci yer değişti) sıra önemli; değişmiyorsa (ekip aynı
ekip) önemsiz.

## Olasılığa köprü

Bütün sonuçlar eşit olasılıklıysa:

$$
P(\text{olay}) = \frac{\text{olaya uyan sonuç sayısı}}{\text{bütün sonuçların sayısı}}
$$

Torbada $3$ kırmızı ve $2$ mavi top var; rastgele $2$ top çekiliyor. İkisinin
de kırmızı olma olasılığı $\frac{\binom{3}{2}}{\binom{5}{2}} =
\frac{3}{10}$. $49$ sayıdan $6$'sını seçen bir lotoda büyük ikramiye olasılığı
$\frac{1}{\binom{49}{6}} = \frac{1}{13\,983\,816}$. Bir sonraki bölüm
Olasılığa Giriş bu köprüden başlar.

## Makine öğrenmesinde sayma

**Izgara araması.** Hiperparametrelerin bütün birleşimlerini denemek
çarpma ilkesi: $3 \cdot 4 \cdot 5 = 60$ ayar. $5$ katlı çapraz doğrulamayla
her ayar $5$ kez eğitilir: $300$ eğitim. Her yeni hiperparametre sayıyı
çarpar; bu yüzden büyük aramalarda rastgele arama tercih edilir.

**Özellik seçimi.** $20$ özellikten en iyi alt kümeyi bulmak için hepsini
denemek $2^{20} \approx 10^6$ model demek; $50$ özellikte $2^{50} \approx
10^{15}$, imkânsız. Adım adım ekleyen ya da çıkaran açgözlü yöntemler bu
yüzden var.

**Çift karşılaştırma.** $n$ örneğin hepsini birbiriyle karşılaştırmak
$\binom{n}{2} = \frac{n(n - 1)}{2}$ karşılaştırma. $1000$ örnek için
$499\,500$; örnek sayısı iki katına çıkınca iş dört katına çıkar.

**Karıştırma.** Her dönemde veri yeniden karıştırılır; $1000$ örneğin
$1000!$ farklı sırası var, iki dönemin aynı sırayı görme olasılığı
pratikte sıfır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>komite için $P(10, 3) = 720$</p>
      <p>$0! = 0$</p>
      <p>"KAYAK" için $5! = 120$</p>
      <p>$\binom{n}{k} = \dfrac{n!}{k!}$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>sıra önemsiz: $\binom{10}{3} = 120$</p>
      <p>$0! = 1$</p>
      <p>tekrarlı harfler için böl: $30$</p>
      <p>$\dfrac{n!}{k! \, (n - k)!}$</p>
    </div>
  </div>
  <figcaption>Önce sıranın önemli olup olmadığına karar ver; aynı nesneler varsa kendi aralarındaki yer değiştirmelere böl.</figcaption>
</figure>

- **Toplama ile çarpmayı karıştırmak.** "Ya o ya bu" toplanır, "önce o
  sonra bu" çarpılır.
- **Aynı durumu iki kez saymak.** Ağaç çizip küçük bir örnekte elle say;
  formülün verdiğiyle karşılaştır.

## Özet

- Ayrı gruplardan biri: topla. Adım adım: çarp.
- $n! = n \cdot (n - 1) \cdots 1$, $0! = 1$.
- Sıralı seçim $P(n, k) = \frac{n!}{(n - k)!}$; tekrarlı sıralı $n^k$.
- Sırasız seçim $\binom{n}{k} = \frac{n!}{k!(n - k)!}$; $P(n, k) =
  \binom{n}{k} \cdot k!$.
- $\binom{n}{k} = \binom{n}{n - k}$; Pascal üçgeni; $n$ elemanlı kümenin
  $2^n$ alt kümesi.
- Aynı nesneler varsa kendi aralarındaki dizilişlere böl.
- Olasılık = uyan / bütün; ızgara araması, özellik seçimi ve çift
  karşılaştırma birer sayma sorusu.
