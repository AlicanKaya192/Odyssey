# Entropi, Çapraz Entropi ve KL Iraksaması

Sınıflandırma modellerinin kaybına "çapraz entropi" diyoruz; karar
ağaçları "bilgi kazancına" bakarak bölünüyor; dil modellerinin başarısı
"şaşkınlık" (perplexity) ile ölçülüyor. Bu adların hepsi **bilgi
kuramından** geliyor. Bu bölümde üç temel sayıyı göreceğiz: bir
dağılımın belirsizliğini ölçen **entropi**, yanlış bir dağılımı
varsaymanın bedeli olan **çapraz entropi**, ve iki dağılım arasındaki
farkı ölçen **KL ıraksaması**.

Ön bilgi: Olasılık Dağılımları; En Çok Olabilirlik Kestirimi; Lojistik
Regresyon ve Log-Loss; Temel Matematik modülündeki Logaritma.

## Bilgi: bir sonucun şaşırtıcılığı

Olasılığı $p$ olan bir sonucu öğrenmenin getirdiği **bilgi**:

$$
I(x) = -\log_2 p(x) \quad \text{(bit)}
$$

- Kesin bir sonuç ($p = 1$) hiç bilgi vermez: $0$ bit.
- Adil paranın sonucu $1$ bit: tek bir evet–hayır sorusunun cevabı.
- Olasılığı $\frac{1}{8}$ olan bir sonuç $3$ bit.

Nadir olay daha şaşırtıcıdır, daha çok bilgi taşır. Bağımsız olayların
olasılıkları çarpılır, bilgileri toplanır; logaritma bunu sağlar.

## Entropi

Bir dağılımın **entropisi**, ortalama bilgidir, yani beklenen
şaşırtıcılık:

$$
H(P) = -\sum_{x} p(x)\log_2 p(x)
$$

($0 \log 0 = 0$ kabul edilir.) Doğal logaritmayla hesaplanırsa birim
**nat** olur; $1$ bit $= \ln 2 \approx 0{,}693$ nat.

**Örnekler.**

- Adil para: $H = 1$ bit.
- $0{,}9$ olasılıkla yazı gelen para: $-0{,}9\log_2 0{,}9 - 0{,}1\log_2 0{,}1
  \approx 0{,}137 + 0{,}332 = 0{,}469$ bit. Sonuç çoğunlukla tahmin
  edilebilir; belirsizlik az.
- $K$ eşit olasılıklı sonuç: $H = \log_2 K$. Bu, $K$ sonuçlu bir dağılımın
  alabileceği **en büyük** entropidir.

<figure class="fig">
<svg viewBox="0 0 420 260" width="420"><line class="grid" x1="50.0" y1="216.0" x2="50.0" y2="26.0"/><line class="grid" x1="84.0" y1="216.0" x2="84.0" y2="26.0"/><line class="grid" x1="118.0" y1="216.0" x2="118.0" y2="26.0"/><line class="grid" x1="152.0" y1="216.0" x2="152.0" y2="26.0"/><line class="grid" x1="186.0" y1="216.0" x2="186.0" y2="26.0"/><line class="grid" x1="220.0" y1="216.0" x2="220.0" y2="26.0"/><line class="grid" x1="254.0" y1="216.0" x2="254.0" y2="26.0"/><line class="grid" x1="288.0" y1="216.0" x2="288.0" y2="26.0"/><line class="grid" x1="322.0" y1="216.0" x2="322.0" y2="26.0"/><line class="grid" x1="356.0" y1="216.0" x2="356.0" y2="26.0"/><line class="grid" x1="390.0" y1="216.0" x2="390.0" y2="26.0"/><line class="grid" x1="50.0" y1="216.0" x2="390.0" y2="216.0"/><line class="grid" x1="50.0" y1="181.5" x2="390.0" y2="181.5"/><line class="grid" x1="50.0" y1="146.9" x2="390.0" y2="146.9"/><line class="grid" x1="50.0" y1="112.4" x2="390.0" y2="112.4"/><line class="grid" x1="50.0" y1="77.8" x2="390.0" y2="77.8"/><line class="grid" x1="50.0" y1="43.3" x2="390.0" y2="43.3"/><line class="line" x1="50.0" y1="216.0" x2="390.0" y2="216.0"/><line class="line" x1="50.0" y1="216.0" x2="50.0" y2="26.0"/><text class="dim" x="45.0" y="184.5" font-size="9" text-anchor="end">0.2</text><text class="dim" x="45.0" y="149.9" font-size="9" text-anchor="end">0.4</text><text class="dim" x="45.0" y="115.4" font-size="9" text-anchor="end">0.6</text><text class="dim" x="45.0" y="80.8" font-size="9" text-anchor="end">0.8</text><text class="dim" x="45.0" y="46.3" font-size="9" text-anchor="end">1</text><polyline class="curve" fill="none" points="50.0,216.0 51.4,209.3 52.8,204.0 54.2,199.3 55.7,194.9 57.1,190.8 58.5,186.9 59.9,183.1 61.3,179.6 62.8,176.2 64.2,172.8 65.6,169.6 67.0,166.5 68.4,163.5 69.8,160.6 71.2,157.7 72.7,155.0 74.1,152.3 75.5,149.6 76.9,147.0 78.3,144.5 79.8,142.1 81.2,139.7 82.6,137.3 84.0,135.0 85.4,132.7 86.8,130.5 88.2,128.4 89.7,126.2 91.1,124.2 92.5,122.1 93.9,120.1 95.3,118.1 96.8,116.2 98.2,114.3 99.6,112.5 101.0,110.7 102.4,108.9 103.8,107.1 105.2,105.4 106.7,103.7 108.1,102.1 109.5,100.4 110.9,98.8 112.3,97.3 113.8,95.7 115.2,94.2 116.6,92.8 118.0,91.3 119.4,89.9 120.8,88.5 122.2,87.1 123.7,85.8 125.1,84.4 126.5,83.1 127.9,81.9 129.3,80.6 130.8,79.4 132.2,78.2 133.6,77.0 135.0,75.9 136.4,74.7 137.8,73.6 139.2,72.6 140.7,71.5 142.1,70.5 143.5,69.4 144.9,68.4 146.3,67.5 147.8,66.5 149.2,65.6 150.6,64.7 152.0,63.8 153.4,62.9 154.8,62.1 156.2,61.2 157.7,60.4 159.1,59.6 160.5,58.9 161.9,58.1 163.3,57.4 164.8,56.7 166.2,56.0 167.6,55.3 169.0,54.7 170.4,54.0 171.8,53.4 173.2,52.8 174.7,52.2 176.1,51.7 177.5,51.1 178.9,50.6 180.3,50.1 181.8,49.6 183.2,49.2 184.6,48.7 186.0,48.3 187.4,47.9 188.8,47.5 190.2,47.1 191.7,46.7 193.1,46.4 194.5,46.1 195.9,45.8 197.3,45.5 198.8,45.2 200.2,45.0 201.6,44.7 203.0,44.5 204.4,44.3 205.8,44.1 207.2,44.0 208.7,43.8 210.1,43.7 211.5,43.6 212.9,43.5 214.3,43.4 215.8,43.4 217.2,43.3 218.6,43.3 220.0,43.3 221.4,43.3 222.8,43.3 224.2,43.4 225.7,43.4 227.1,43.5 228.5,43.6 229.9,43.7 231.3,43.8 232.8,44.0 234.2,44.1 235.6,44.3 237.0,44.5 238.4,44.7 239.8,45.0 241.2,45.2 242.7,45.5 244.1,45.8 245.5,46.1 246.9,46.4 248.3,46.7 249.8,47.1 251.2,47.5 252.6,47.9 254.0,48.3 255.4,48.7 256.8,49.2 258.2,49.6 259.7,50.1 261.1,50.6 262.5,51.1 263.9,51.7 265.3,52.2 266.8,52.8 268.2,53.4 269.6,54.0 271.0,54.7 272.4,55.3 273.8,56.0 275.2,56.7 276.7,57.4 278.1,58.1 279.5,58.9 280.9,59.6 282.3,60.4 283.8,61.2 285.2,62.1 286.6,62.9 288.0,63.8 289.4,64.7 290.8,65.6 292.2,66.5 293.7,67.5 295.1,68.4 296.5,69.4 297.9,70.5 299.3,71.5 300.8,72.6 302.2,73.6 303.6,74.7 305.0,75.9 306.4,77.0 307.8,78.2 309.2,79.4 310.7,80.6 312.1,81.9 313.5,83.1 314.9,84.4 316.3,85.8 317.8,87.1 319.2,88.5 320.6,89.9 322.0,91.3 323.4,92.8 324.8,94.2 326.2,95.7 327.7,97.3 329.1,98.8 330.5,100.4 331.9,102.1 333.3,103.7 334.8,105.4 336.2,107.1 337.6,108.9 339.0,110.7 340.4,112.5 341.8,114.3 343.2,116.2 344.7,118.1 346.1,120.1 347.5,122.1 348.9,124.2 350.3,126.2 351.8,128.4 353.2,130.5 354.6,132.7 356.0,135.0 357.4,137.3 358.8,139.7 360.2,142.1 361.7,144.5 363.1,147.0 364.5,149.6 365.9,152.3 367.3,155.0 368.8,157.7 370.2,160.6 371.6,163.5 373.0,166.5 374.4,169.6 375.8,172.8 377.2,176.2 378.7,179.6 380.1,183.1 381.5,186.9 382.9,190.8 384.3,194.9 385.8,199.3 387.2,204.0 388.6,209.3 390.0,216.0"/><circle class="dot2" cx="220.0" cy="43.3" r="5"/><circle class="dot2" cx="356.0" cy="135.0" r="5"/><circle class="dot3" cx="390.0" cy="216.0" r="5"/><text class="ink" x="220.0" y="33.3" font-size="11" text-anchor="middle">adil para: 1 bit</text><text class="ink" x="346.0" y="131.0" font-size="11" text-anchor="end">p = 0,9: 0,469 bit</text><text class="ink" x="384.0" y="206.0" font-size="10" text-anchor="end">kesin sonuç: 0 bit</text><text class="dim" x="50.0" y="230.0" font-size="9" text-anchor="middle">0,0</text><text class="dim" x="118.0" y="230.0" font-size="9" text-anchor="middle">0,2</text><text class="dim" x="186.0" y="230.0" font-size="9" text-anchor="middle">0,4</text><text class="dim" x="254.0" y="230.0" font-size="9" text-anchor="middle">0,6</text><text class="dim" x="322.0" y="230.0" font-size="9" text-anchor="middle">0,8</text><text class="dim" x="390.0" y="230.0" font-size="9" text-anchor="middle">1,0</text><text class="dim" x="390.0" y="244.0" font-size="10" text-anchor="end">yazı olasılığı p</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">H(p) (bit)</text></svg>
  <figcaption>İki sonuçlu bir dağılımın entropisi. En büyük değer, en belirsiz durum olan p = 0,5'te 1 bit. Sonuç kesinleştikçe (p → 0 ya da 1) entropi 0'a iner.</figcaption>
</figure>

## Entropi: soru sayısı

Dört sonuç olsun: A ($\frac{1}{2}$), B ($\frac{1}{4}$), C ($\frac{1}{8}$),
D ($\frac{1}{8}$). Hangisinin çıktığını evet–hayır sorularıyla bulmak
istiyoruz. Akıllıca yol, önce en olasıyı sormak:

<figure class="fig">
<svg viewBox="0 0 420 290" width="420"><line class="line" x1="90" y1="40" x2="40" y2="110"/><text class="dim" x="57.0" y="73.0" font-size="10" text-anchor="end">evet</text><line class="line" x1="90" y1="40" x2="200" y2="100"/><text class="dim" x="153.0" y="68.0" font-size="10" text-anchor="start">hayır</text><line class="line" x1="200" y1="100" x2="150" y2="170"/><text class="dim" x="167.0" y="133.0" font-size="10" text-anchor="end">evet</text><line class="line" x1="200" y1="100" x2="310" y2="160"/><text class="dim" x="263.0" y="128.0" font-size="10" text-anchor="start">hayır</text><line class="line" x1="310" y1="160" x2="260" y2="230"/><text class="dim" x="277.0" y="193.0" font-size="10" text-anchor="end">evet</text><line class="line" x1="310" y1="160" x2="360" y2="230"/><text class="dim" x="343.0" y="193.0" font-size="10" text-anchor="start">hayır</text><rect class="box" x="58" y="26" width="64" height="26" rx="8"/><text class="ink" x="90" y="44" font-size="11" text-anchor="middle">A mı?</text><rect class="box" x="168" y="86" width="64" height="26" rx="8"/><text class="ink" x="200" y="104" font-size="11" text-anchor="middle">B mi?</text><rect class="box" x="278" y="146" width="64" height="26" rx="8"/><text class="ink" x="310" y="164" font-size="11" text-anchor="middle">C mi?</text><circle class="box" cx="40" cy="110" r="15"/><text class="ink" x="40" y="115" font-size="13" text-anchor="middle">A</text><text class="ink" x="40" y="142" font-size="10" text-anchor="middle">p = 1/2</text><text class="dim" x="40" y="156" font-size="10" text-anchor="middle">0 · 1 soru</text><circle class="box" cx="150" cy="170" r="15"/><text class="ink" x="150" y="175" font-size="13" text-anchor="middle">B</text><text class="ink" x="150" y="202" font-size="10" text-anchor="middle">p = 1/4</text><text class="dim" x="150" y="216" font-size="10" text-anchor="middle">10 · 2 soru</text><circle class="box" cx="260" cy="230" r="15"/><text class="ink" x="260" y="235" font-size="13" text-anchor="middle">C</text><text class="ink" x="260" y="262" font-size="10" text-anchor="middle">p = 1/8</text><text class="dim" x="260" y="276" font-size="10" text-anchor="middle">110 · 3 soru</text><circle class="box" cx="360" cy="230" r="15"/><text class="ink" x="360" y="235" font-size="13" text-anchor="middle">D</text><text class="ink" x="360" y="262" font-size="10" text-anchor="middle">p = 1/8</text><text class="dim" x="360" y="276" font-size="10" text-anchor="middle">111 · 3 soru</text></svg>
  <figcaption>Önce "A mı?" diye sormak. A yarı yarıya olasılıkla tek soruda bulunuyor; C ve D üç soru istiyor. Her yaprağın altında ona giden cevap dizisi (0 evet, 1 hayır) ve soru sayısı.</figcaption>
</figure>

Ortalama soru sayısı $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 +
\frac{1}{8} \cdot 3 + \frac{1}{8} \cdot 3 = 1{,}75$. Entropi de tam
$1{,}75$ bit. Entropi, bir sonucu iletmek için gereken **en az ortalama
bit sayısıdır**; sık sonuca kısa, nadir sonuca uzun kod vermek bunu
sağlar (sıkıştırma algoritmalarının temeli). Olasılığı $p$ olan sonucun
kodu yaklaşık $-\log_2 p$ bit uzunluğundadır.

## Çapraz entropi

Veri gerçekte $P$'den geliyor ama biz $Q$ olduğunu varsayıp kodumuzu ona
göre kurduk. Ortalama kod uzunluğu:

$$
H(P, Q) = -\sum_{x} p(x)\log_2 q(x)
$$

Buna **çapraz entropi** denir. Her zaman $H(P, Q) \geq H(P)$: yanlış
varsayım ortalamada fazladan bit harcatır.

**Örnek.** Yukarıdaki $P$ için dört sonucu eşit olasılıklı sanıp ($Q$
düzgün) her birine $2$ bitlik kod verirsek ortalama $2$ bit harcarız:
$H(P, Q) = 2$. Doğru kodla $1{,}75$ yeterdi.

## KL ıraksaması

Fazladan harcanan bit sayısı **Kullback–Leibler ıraksamasıdır**:

$$
D_{\mathrm{KL}}(P \parallel Q) = \sum_{x} p(x)\log_2\frac{p(x)}{q(x)} = H(P, Q) - H(P)
$$

<figure class="fig">
<svg viewBox="0 0 470 250" width="470"><line class="grid" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><line class="grid" x1="105.0" y1="220.0" x2="105.0" y2="20.0"/><line class="grid" x1="170.0" y1="220.0" x2="170.0" y2="20.0"/><line class="grid" x1="235.0" y1="220.0" x2="235.0" y2="20.0"/><line class="grid" x1="300.0" y1="220.0" x2="300.0" y2="20.0"/><line class="grid" x1="40.0" y1="220.0" x2="300.0" y2="220.0"/><line class="grid" x1="40.0" y1="186.7" x2="300.0" y2="186.7"/><line class="grid" x1="40.0" y1="153.3" x2="300.0" y2="153.3"/><line class="grid" x1="40.0" y1="120.0" x2="300.0" y2="120.0"/><line class="grid" x1="40.0" y1="86.7" x2="300.0" y2="86.7"/><line class="grid" x1="40.0" y1="53.3" x2="300.0" y2="53.3"/><line class="grid" x1="40.0" y1="20.0" x2="300.0" y2="20.0"/><line class="line" x1="40.0" y1="220.0" x2="300.0" y2="220.0"/><rect class="dot" opacity="0.85" x="49.8" y="53.3" width="21.4" height="166.7"/><rect class="dot2" opacity="0.85" x="73.8" y="136.7" width="21.4" height="83.3"/><text class="ink" x="72.5" y="236.0" font-size="11" text-anchor="middle">A</text><rect class="dot" opacity="0.85" x="114.8" y="136.7" width="21.4" height="83.3"/><rect class="dot2" opacity="0.85" x="138.8" y="136.7" width="21.4" height="83.3"/><text class="ink" x="137.5" y="236.0" font-size="11" text-anchor="middle">B</text><rect class="dot" opacity="0.85" x="179.8" y="178.3" width="21.4" height="41.7"/><rect class="dot2" opacity="0.85" x="203.8" y="136.7" width="21.4" height="83.3"/><text class="ink" x="202.5" y="236.0" font-size="11" text-anchor="middle">C</text><rect class="dot" opacity="0.85" x="244.8" y="178.3" width="21.4" height="41.7"/><rect class="dot2" opacity="0.85" x="268.8" y="136.7" width="21.4" height="83.3"/><text class="ink" x="267.5" y="236.0" font-size="11" text-anchor="middle">D</text><text class="dim" x="36.0" y="181.3" font-size="9" text-anchor="end">0,125</text><text class="dim" x="36.0" y="139.7" font-size="9" text-anchor="end">0,25</text><text class="dim" x="36.0" y="56.3" font-size="9" text-anchor="end">0,5</text><rect class="dot" x="320" y="40" width="14" height="14"/><rect class="dot2" x="320" y="62" width="14" height="14"/><text class="ink" x="340" y="52" font-size="11" text-anchor="start">P (gerçek)</text><text class="ink" x="340" y="74" font-size="11" text-anchor="start">Q (varsayılan)</text><text class="ink" x="320" y="120" font-size="11" text-anchor="start">H(P) = 1,75 bit</text><text class="ink" x="320" y="142" font-size="11" text-anchor="start">H(P, Q) = 2 bit</text><text class="ink" x="320" y="164" font-size="11" text-anchor="start">KL(P ‖ Q) = 0,25 bit</text></svg>
  <figcaption>Gerçek dağılım P ve varsayılan düzgün dağılım Q. Q ile kodlamak ortalamada 2 bit harcatıyor; P'nin kendi entropisi 1,75 bit. Aradaki 0,25 bit KL ıraksaması.</figcaption>
</figure>

- $D_{\mathrm{KL}} \geq 0$; yalnızca $P = Q$ iken $0$.
- **Simetrik değildir**: $D_{\mathrm{KL}}(P \parallel Q) \neq
  D_{\mathrm{KL}}(Q \parallel P)$ olabilir. Bu yüzden "uzaklık" değil
  "ıraksama" denir.
- $p(x) > 0$ iken $q(x) = 0$ ise sonsuzdur: gerçekte olabilen bir şeye
  sıfır olasılık vermenin bedeli sınırsız.

**Asimetri örneği.** $P = (0{,}9; \ 0{,}1)$, $Q = (0{,}5; \ 0{,}5)$.
$D_{\mathrm{KL}}(P \parallel Q) \approx 0{,}531$ bit, ama
$D_{\mathrm{KL}}(Q \parallel P) \approx 0{,}737$ bit.

## Makine öğrenmesinde

**Çapraz entropi kaybı.** Sınıflandırmada gerçek etiket tek-sıcak bir
dağılım $P$: doğru sınıfa $1$, ötekilere $0$. Modelin olasılıkları $Q$.
O zaman

$$
H(P, Q) = -\log q_{\text{doğru}}
$$

yani Lojistik Regresyon bölümündeki log-loss. $H(P) = 0$ olduğu için
çapraz entropiyi en küçük yapmak KL'yi en küçük yapmakla aynıdır; bu da
En Çok Olabilirlik ile aynı: üç bakış, tek bir kayıp. (Kayıplarda genellikle
doğal logaritma, yani nat kullanılır.)

**Karar ağaçlarında bilgi kazancı.** Bir düğümdeki sınıf dağılımının
entropisi, düğümün ne kadar "karışık" olduğunu ölçer. Bir bölmenin **bilgi
kazancı**, ebeveyn entropisinden çocukların ağırlıklı ortalama entropisinin
çıkarılmasıdır. Örnek: $4$ spam $4$ normal ($H = 1$); bölme $(3, 1)$ ve
$(1, 3)$ verirse çocukların entropisi $0{,}811$, kazanç $0{,}189$ bit.

**Şaşkınlık.** Dil modelleri $2^{H}$ (ya da $e^{H}$) ile değerlendirilir:
model her adımda ortalama kaç seçenek arasında kararsız kalıyormuş gibi
davranıyor.

**KL başka yerlerde.** Varyasyonel otokodlayıcılar gizli dağılımı bir
önsele KL cezasıyla yaklaştırır; bilgi damıtmada küçük model, büyük
modelin olasılıklarına KL (ya da çapraz entropi) ile yaklaştırılır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>KL(P ‖ Q) = KL(Q ‖ P)</p>
      <p>çapraz entropi entropiden küçük olabilir</p>
      <p>bir kayıpta bit, ötekinde nat, sonra karşılaştırmak</p>
      <p>modelin bir sınıfa tam 0 olasılık vermesi zararsız</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>KL simetrik değil; hangi dağılımın gerçek olduğu önemli</p>
      <p>H(P, Q) ≥ H(P); fark KL</p>
      <p>log tabanını sabit tut; 1 bit = 0,693 nat</p>
      <p>gerçekte olabilen sonuca q = 0: kayıp sonsuz</p>
    </div>
  </div>
  <figcaption>Entropi bir dağılım hakkında, çapraz entropi ve KL iki dağılım hakkında.</figcaption>
</figure>

- **$0 \log 0$'ı tanımsız saymak.** Olasılığı $0$ olan sonuç entropiye
  katkı vermez; $p\log p \to 0$.

## Özet

- Bilgi $I(x) = -\log_2 p(x)$; nadir olay daha çok bilgi taşır.
- Entropi $H(P) = -\sum p\log p$: ortalama bilgi, en az ortalama kod
  uzunluğu; $K$ sonuçta en fazla $\log_2 K$.
- Çapraz entropi $H(P, Q) = -\sum p\log q \geq H(P)$.
- KL $= H(P, Q) - H(P) = \sum p\log\frac{p}{q} \geq 0$; simetrik değil.
- Sınıflandırmada çapraz entropi kaybı $= -\log q_{\text{doğru}}$ =
  log-loss; en küçük yapmak MLE ile aynı.
- Karar ağaçları bilgi kazancıyla böler; dil modelleri şaşkınlıkla ölçülür.
