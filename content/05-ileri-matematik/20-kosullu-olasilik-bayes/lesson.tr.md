# Koşullu Olasılık ve Bayes

Yeni bir bilgi geldiğinde bir şeye ne kadar inandığımız değişmeli: test
pozitif çıktıysa hasta olma olasılığı artar, e-postada "bedava" geçiyorsa
spam olma olasılığı artar. Ne kadar artacağını söyleyen kural **Bayes
kuralı**. Sezgi bu konuda sık yanılır: yüzde $99$ doğru bir test pozitif
çıktığında hasta olma olasılığı yüzde $99$ değil, çoğu zaman çok daha
düşüktür. Bu bölümde koşullu olasılığı, toplam olasılık kuralını, Bayes
kuralını, ardışık güncellemeyi ve Naive Bayes sınıflandırıcısını
göreceğiz.

Ön bilgi: MAT 1'deki Olasılığa Giriş ve Sayma bölümleri.

## Koşullu olasılık ve çarpım kuralı

"$A$ olduğu bilindiğine göre $B$" olasılığı, örnek uzayı $A$'ya daraltır:

$$
P(B \mid A) = \frac{P(A \cap B)}{P(A)}
$$

Aynı eşitlik ters yönden okununca **çarpım kuralı** olur: iki olayın
birlikte olma olasılığı, birinin olasılığı çarpı diğerinin ona bağlı
olasılığı.

$$
P(A \cap B) = P(A) \, P(B \mid A) = P(B) \, P(A \mid B)
$$

Olasılık ağacında dal boyunca çarpmak tam olarak bu. $A$ ile $B$
bağımsızsa $P(B \mid A) = P(B)$ ve kural $P(A)P(B)$'ye iner.

## Toplam olasılık kuralı

Örnek uzay birbirini dışlayan ve hepsini kapsayan parçalara bölünmüşse
($A_1, A_2, \dots$), bir olayın olasılığı parçalardaki payların toplamı:

$$
P(B) = \sum_{i} P(B \mid A_i) \, P(A_i)
$$

**Örnek.** Bir fabrikada ürünlerin yüzde $50$'sini A makinesi, yüzde
$30$'unu B, yüzde $20$'sini C yapıyor. Hatalı oranları sırasıyla yüzde $2$,
$3$ ve $5$. Rastgele bir ürünün hatalı olma olasılığı:

$$
0{,}5 \cdot 0{,}02 + 0{,}3 \cdot 0{,}03 + 0{,}2 \cdot 0{,}05 = 0{,}01 + 0{,}009 + 0{,}01 = 0{,}029
$$

## Bayes kuralı

Çarpım kuralının iki yazılışını eşitleyip $P(A \mid B)$'yi çekince:

$$
P(A \mid B) = \frac{P(B \mid A) \, P(A)}{P(B)}
$$

Parçaların adları, bir inancın güncellenmesini anlatır:

| Parça | Adı | Anlamı |
|---|---|---|
| $P(A)$ | önsel | kanıttan önceki inanç |
| $P(B \mid A)$ | olabilirlik | $A$ doğruysa bu kanıtı görme olasılığı |
| $P(B)$ | kanıt | kanıtın toplam olasılığı (toplam olasılık kuralıyla) |
| $P(A \mid B)$ | sonsal | kanıttan sonraki inanç |

Fabrika örneğinde hatalı bir ürün bulundu; C makinesinden gelmiş olma
olasılığı: $\frac{0{,}05 \cdot 0{,}2}{0{,}029} = \frac{0{,}01}{0{,}029}
\approx 0{,}345$. C yalnızca ürünlerin yüzde $20$'sini yapıyor ama
hatalıların yüzde $34{,}5$'i ondan geliyor.

## Test paradoksu

Bir hastalık nüfusun yüzde $1$'inde var. Test hastaların yüzde $99$'unda
pozitif çıkıyor (duyarlılık), sağlıklıların da yüzde $5$'inde yanlışlıkla
pozitif çıkıyor. Testi pozitif çıkan birinin hasta olma olasılığı nedir?

Sezgi "yüzde $99$" der. Hesap başka söylüyor. En kolayı doğal sıklıklarla
düşünmek: $10\,000$ kişi al.

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><line class="curve3" x1="220" y1="40" x2="110" y2="82"/><line class="curve3" x1="220" y1="40" x2="330" y2="82"/><line class="curve3" x1="110" y1="118" x2="55" y2="158"/><line class="curve3" x1="110" y1="118" x2="165" y2="158"/><line class="curve3" x1="330" y1="118" x2="275" y2="158"/><line class="curve3" x1="330" y1="118" x2="385" y2="158"/><rect class="box" x="165.0" y="12.0" width="110" height="28" rx="6"/><text class="ink" x="220" y="30.0" font-size="11" text-anchor="middle">10 000 kişi</text><rect class="box" x="65.0" y="82.0" width="90" height="36" rx="6"/><text class="ink" x="110" y="97.0" font-size="11" text-anchor="middle">hasta</text><text class="ink" x="110" y="111.0" font-size="11" text-anchor="middle">100</text><rect class="box" x="285.0" y="82.0" width="90" height="36" rx="6"/><text class="ink" x="330" y="97.0" font-size="11" text-anchor="middle">sağlıklı</text><text class="ink" x="330" y="111.0" font-size="11" text-anchor="middle">9900</text><rect class="box" x="12.0" y="158.0" width="86" height="36" rx="6"/><rect class="dot2" opacity="0.35" x="12.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="55" y="173.0" font-size="11" text-anchor="middle">test +</text><text class="ink" x="55" y="187.0" font-size="11" text-anchor="middle">99</text><rect class="box" x="122.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="165" y="173.0" font-size="11" text-anchor="middle">test −</text><text class="ink" x="165" y="187.0" font-size="11" text-anchor="middle">1</text><rect class="box" x="232.0" y="158.0" width="86" height="36" rx="6"/><rect class="dot2" opacity="0.35" x="232.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="275" y="173.0" font-size="11" text-anchor="middle">test +</text><text class="ink" x="275" y="187.0" font-size="11" text-anchor="middle">495</text><rect class="box" x="342.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="385" y="173.0" font-size="11" text-anchor="middle">test −</text><text class="ink" x="385" y="187.0" font-size="11" text-anchor="middle">9405</text><text class="ink" x="220" y="222" font-size="12" text-anchor="middle">pozitiflerin 99 / (99 + 495) = 1/6'sı hasta</text></svg>
  <figcaption>10 000 kişiden 100'ü hasta, 99'unun testi pozitif. 9900 sağlıklının yüzde 5'i, yani 495'inin testi de pozitif. Pozitif çıkan 594 kişiden yalnızca 99'u hasta.</figcaption>
</figure>

Pozitiflerin $\frac{99}{99 + 495} = \frac{99}{594} = \frac{1}{6} \approx
0{,}167$'si hasta. Bayes kuralıyla aynı hesap:

$$
P(H \mid +) = \frac{0{,}99 \cdot 0{,}01}{0{,}99 \cdot 0{,}01 + 0{,}05 \cdot 0{,}99} = \frac{0{,}0099}{0{,}0594} \approx 0{,}167
$$

<figure class="fig">
<svg viewBox="0 0 440 142" width="440"><rect class="dot2" opacity="0.6" x="20" y="40" width="66.7" height="46"/><rect class="dot" opacity="0.45" x="86.7" y="40" width="333.3" height="46"/><text class="dim" x="20" y="30" font-size="11" text-anchor="start">594 pozitif sonuç</text><text class="ink" x="53.333333333333336" y="104" font-size="11" text-anchor="middle">hasta: 99</text><text class="ink" x="253.33333333333331" y="68.0" font-size="12" text-anchor="middle">sağlıklı (yanlış alarm): 495</text><text class="ink" x="220.0" y="130" font-size="12" text-anchor="middle">pozitiflerin yalnızca 1/6'sı hasta</text></svg>
  <figcaption>Bütün pozitif sonuçlar tek çubukta, gerçek ölçüyle: 99'u hastalardan, 495'i sağlıklılardan. Hastaların neredeyse hepsi yakalanıyor, ama sağlıklılar o kadar kalabalık ki yüzde 5'lik yanlış alarm oranı bile beş kat fazla pozitif üretiyor.</figcaption>
</figure>

**Neden?** Hastalık nadir: yanlış alarmlar küçük bir oranın büyük bir
kalabalığa uygulanması, gerçek pozitifler büyük bir oranın küçük bir
gruba uygulanması. Önselin (yüzde $1$) etkisini görmezden gelmeye **taban
oranı yanılgısı** denir.

## Ardışık güncelleme

Bir testin sonsalı, bir sonraki testin önseli olur. Birinci test pozitif:
yüzde $16{,}7$. Aynı kişi bağımsız ikinci bir testte de pozitif çıkarsa:

$$
\frac{0{,}99 \cdot 0{,}167}{0{,}99 \cdot 0{,}167 + 0{,}05 \cdot 0{,}833} \approx 0{,}798
$$

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><line class="grid" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><line class="grid" x1="137.5" y1="210.0" x2="137.5" y2="20.0"/><line class="grid" x1="225.0" y1="210.0" x2="225.0" y2="20.0"/><line class="grid" x1="312.5" y1="210.0" x2="312.5" y2="20.0"/><line class="grid" x1="400.0" y1="210.0" x2="400.0" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="grid" x1="50.0" y1="162.5" x2="400.0" y2="162.5"/><line class="grid" x1="50.0" y1="115.0" x2="400.0" y2="115.0"/><line class="grid" x1="50.0" y1="67.5" x2="400.0" y2="67.5"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="line" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><text class="dim" x="45.0" y="165.5" font-size="9" text-anchor="end">25</text><text class="dim" x="45.0" y="118.0" font-size="9" text-anchor="end">50</text><text class="dim" x="45.0" y="70.5" font-size="9" text-anchor="end">75</text><text class="dim" x="45.0" y="23.0" font-size="9" text-anchor="end">100</text><rect class="dot" opacity="0.6" x="67.5" y="208.1" width="52.5" height="1.9"/><text class="ink" x="93.8" y="202.1" font-size="11" text-anchor="middle">1</text><text class="dim" x="93.8" y="226" font-size="10" text-anchor="middle">başta</text><rect class="dot" opacity="0.6" x="155.0" y="178.3" width="52.5" height="31.7"/><text class="ink" x="181.2" y="172.3" font-size="11" text-anchor="middle">16,7</text><text class="dim" x="181.2" y="226" font-size="10" text-anchor="middle">1. test +</text><rect class="dot" opacity="0.6" x="242.5" y="58.4" width="52.5" height="151.6"/><text class="ink" x="268.8" y="52.4" font-size="11" text-anchor="middle">79,8</text><text class="dim" x="268.8" y="226" font-size="10" text-anchor="middle">2. test +</text><rect class="dot" opacity="0.6" x="330.0" y="22.5" width="52.5" height="187.5"/><text class="ink" x="356.2" y="16.5" font-size="11" text-anchor="middle">98,7</text><text class="dim" x="356.2" y="226" font-size="10" text-anchor="middle">3. test +</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">hasta olma olasılığı (yüzde)</text></svg>
  <figcaption>Her pozitif test, bir öncekinin sonsalını önsel olarak kullanıyor: yüzde 1'den 16,7'ye, 79,8'e ve 98,7'ye. Tek bir test az şey söylüyor; bağımsız kanıtlar birikince inanç hızla netleşiyor.</figcaption>
</figure>

**Oran biçimi.** Olasılığı oranla yazınca Bayes bir çarpmaya dönüşür:

$$
\underbrace{\frac{P(H \mid +)}{P(S \mid +)}}_{\text{sonsal oran}} = \underbrace{\frac{P(H)}{P(S)}}_{\text{önsel oran}} \cdot \underbrace{\frac{P(+ \mid H)}{P(+ \mid S)}}_{\text{olabilirlik oranı}}
$$

Önsel oran $1 : 99$, olabilirlik oranı $\frac{0{,}99}{0{,}05} = 19{,}8$.
Sonsal oran $19{,}8 : 99 = 1 : 5$, yani olasılık $\frac{1}{6}$. Her yeni
bağımsız kanıt oranı bir kez daha $19{,}8$ ile çarpar.

## Koşullu bağımsızlık

İki olay, üçüncü bir şey bilindiğinde bağımsız olabilir:
$P(A \cap B \mid C) = P(A \mid C) \, P(B \mid C)$. Bir e-postada "bedava" ve
"kazan" kelimeleri birlikte sık geçer (bağımlı), ama e-postanın spam olduğu
biliniyorsa aralarındaki bağın çoğu açıklanmış olur. Naive Bayes bu
varsayımın üstüne kurulur.

## Makine öğrenmesinde Bayes

**Naive Bayes sınıflandırıcısı.** Her sınıf için "önsel çarpı kelimelerin
olabilirlikleri" hesaplanır, en büyüğü seçilir. $P(\text{spam}) = 0{,}3$;
"bedava" spamlerin yüzde $40$'ında, spam olmayanların yüzde $5$'inde;
"kazan" spamlerin yüzde $30$'unda, ötekilerin yüzde $2$'sinde geçiyor.
İkisini de içeren bir e-posta için:

$$
\begin{aligned}
\text{spam} &: 0{,}3 \cdot 0{,}4 \cdot 0{,}3 = 0{,}036 \\
\text{spam değil} &: 0{,}7 \cdot 0{,}05 \cdot 0{,}02 = 0{,}0007
\end{aligned}
$$

Normalleştirince $P(\text{spam} \mid \text{kelimeler}) = \frac{0{,}036}{0{,}0367}
\approx 0{,}98$. Payda (kanıt) iki sınıfta aynı olduğu için karşılaştırma
için gerekmez; yalnızca olasılığı $1$'e tamamlamak için hesaplanır.

**Kesinlik bir Bayes sorusu.** Bir modelin "pozitif" dediklerinin ne kadarı
gerçekten pozitif? Nadir sınıflarda (dolandırıcılık, arıza) iyi bir model
bile test paradoksuna düşer: yanlış alarmlar gerçek yakalamaları sayıca
geçebilir.

**Önsel bir varsayım.** Bayesçi yöntemler ağırlıklar hakkındaki önsel
inancı açıkça yazar; düzenlileştirme (küçük ağırlıkları tercih etmek) bir
önselin başka bir adıdır.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$P(H \mid +) = P(+ \mid H) = 0{,}99$</p>
      <p>önseli hesaba katmamak</p>
      <p>$P(B)$ için yalnızca bir dalı almak</p>
      <p>iki test = iki kat olasılık</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$P(H \mid +) \approx 0{,}167$</p>
      <p>taban oranı sonucu belirler</p>
      <p>toplam olasılık: bütün dalların toplamı</p>
      <p>sonsal, yeni önsel olur</p>
    </div>
  </div>
  <figcaption>Koşulun yönü önemli: "hastaysa pozitif" ile "pozitifse hasta" farklı sorular.</figcaption>
</figure>

- **Bağımsız olmayan kanıtları çarpmak.** Aynı testi aynı kişiye iki kez
  yapmak bağımsız iki kanıt sayılmayabilir; hata aynı sebepten tekrar
  edebilir.

## Özet

- $P(B \mid A) = \frac{P(A \cap B)}{P(A)}$; çarpım kuralı
  $P(A \cap B) = P(A) P(B \mid A)$.
- Toplam olasılık: $P(B) = \sum P(B \mid A_i) P(A_i)$.
- Bayes: $P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$; önsel, olabilirlik,
  kanıt, sonsal.
- Nadir olaylarda pozitif sonuç bile düşük sonsal verebilir (taban oranı).
- Sonsal bir sonraki adımın önseli; oran biçiminde her kanıt olabilirlik
  oranıyla çarpar.
- Naive Bayes koşullu bağımsızlıkla olabilirlikleri çarpar; kesinlik bir
  Bayes sorusudur.
