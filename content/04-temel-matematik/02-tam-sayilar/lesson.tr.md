# Tam Sayılar ve Negatif Sayılar

Doğal sayılarla $5 - 8$ işlemini yapamıyorduk: $5$'ten $8$ çıkarınca
sonuç doğal sayı değil. Ama hayatta böyle durumlar hep var: sıcaklık
sıfırın altına düşer, bir hesap eksiye geçer, bir asansör zemin katın
altına iner. Bunları anlatmak için sayıları **sıfırın soluna** da
uzatıyoruz: negatif sayılar.

Bu bölümde tam sayıları sayı doğrusunda göreceğiz, mutlak değeri
tanımlayacağız ve dört işlemin işaret kurallarını **neden** öyle
olduklarıyla birlikte öğreneceğiz. Makine öğrenmesinde hata, eğim ve
ağırlıklar sürekli negatif değerler alıyor; bu kuralları otomatik
uygulayabilmek önemli.

Ön bilgi: Doğal Sayılar ve İşlem Önceliği bölümü.

## Tam sayılar ve sayı doğrusu

**Tam sayılar**, doğal sayılar ile onların negatiflerinden oluşur:

$$
\mathbb{Z} = \{\dots, -3, -2, -1, 0, 1, 2, 3, \dots\}
$$

$\mathbb{Z}$ harfi Almanca "sayılar" anlamındaki *Zahlen*'den geliyor.
Sıfır ne pozitif ne negatif; iki tarafın sınırı.

<figure class="fig">
<svg viewBox="0 0 460 138" width="460"><path class="curve2" d="M 230 66 L 230 44 L 110 44 L 110 66"/><text class="ink" x="170.0" y="36" font-size="12" text-anchor="middle">|−4| = 4</text><path class="curve" d="M 230 66 L 230 44 L 350 44 L 350 66"/><text class="ink" x="290.0" y="36" font-size="12" text-anchor="middle">|4| = 4</text><line class="line" x1="10" y1="78" x2="450" y2="78"/><line class="line" x1="20" y1="72" x2="20" y2="84"/><text class="dim" x="20" y="102" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="72" x2="50" y2="84"/><text class="dim" x="50" y="102" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="72" x2="80" y2="84"/><text class="dim" x="80" y="102" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="72" x2="110" y2="84"/><text class="dim" x="110" y="102" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="72" x2="140" y2="84"/><text class="dim" x="140" y="102" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="72" x2="170" y2="84"/><text class="dim" x="170" y="102" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="72" x2="200" y2="84"/><text class="dim" x="200" y="102" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="69" x2="230" y2="87"/><text class="ink" x="230" y="102" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="72" x2="260" y2="84"/><text class="dim" x="260" y="102" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="72" x2="290" y2="84"/><text class="dim" x="290" y="102" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="72" x2="320" y2="84"/><text class="dim" x="320" y="102" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="72" x2="350" y2="84"/><text class="dim" x="350" y="102" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="72" x2="380" y2="84"/><text class="dim" x="380" y="102" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="72" x2="410" y2="84"/><text class="dim" x="410" y="102" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="72" x2="440" y2="84"/><text class="dim" x="440" y="102" font-size="11" text-anchor="middle">7</text><circle class="dot2" cx="110" cy="78" r="5"/><circle class="dot" cx="350" cy="78" r="5"/><text class="dim" x="65.0" y="126" font-size="11" text-anchor="middle">← negatifler</text><text class="dim" x="395.0" y="126" font-size="11" text-anchor="middle">pozitifler →</text><text class="ink" x="230" y="126" font-size="12" text-anchor="middle">zıt sayılar: −4 ve 4</text></svg>
  <figcaption>Sayı doğrusunda sıfırın sağı pozitif, solu negatif. $-4$ ile $4$ sıfıra eşit uzaklıkta ama zıt yönde: bunlara zıt sayılar denir. İkisinin de sıfıra uzaklığı, yani mutlak değeri $4$.</figcaption>
</figure>

**Sıralama:** Sayı doğrusunda sağdaki sayı daha büyük. Bu yüzden

$$
-5 < -2 < 0 < 3
$$

Negatiflerde sezgi ters çalışabilir: $-5$, $-2$'den **küçük**, çünkü daha
solda. Sıcaklıkla düşün: $-5$ derece, $-2$ dereceden daha soğuk.

## Zıt sayı ve mutlak değer

Bir sayının **zıttı**, sayı doğrusunda sıfıra göre öbür taraftaki
sayıdır: $3$'ün zıttı $-3$, $-7$'nin zıttı $7$. Bir sayı ile zıttının
toplamı her zaman $0$:

$$
a + (-a) = 0
$$

Eksi işareti "zıttını al" anlamına da geliyor. Bu yüzden

$$
-(-5) = 5
$$

"$-5$'in zıttı" $5$. İki eksi yan yana gelince birbirini götürüyor.

**Mutlak değer** $|a|$, bir sayının sıfıra **uzaklığı**. Uzaklık negatif
olamaz:

$$
|7| = 7, \qquad \lvert -7 \rvert = 7, \qquad |0| = 0
$$

İki sayı arasındaki uzaklık da mutlak değerle yazılır: $a$ ile $b$
arasındaki uzaklık $|a - b|$. Örneğin $-3$ ile $5$ arası $\lvert -3 - 5 \rvert =
\lvert -8 \rvert = 8$ birim.

## Toplama

Sayı doğrusunda toplama bir **yürüyüş**: $a + b$ için $a$'dan başla,
$b$ pozitifse sağa, negatifse sola $|b|$ adım at.

<figure class="fig">
<svg viewBox="0 0 460 216" width="460"><text class="ink" x="230" y="18" font-size="13" text-anchor="middle">−3 + 5 = 2</text><text class="dim" x="230" y="34" font-size="11" text-anchor="middle">önce −3'e git, sonra 5 adım sağa</text><line class="curve2" x1="230" y1="46" x2="147" y2="46"/><polygon class="dot2" points="140,46 150,41 150,51"/><line class="curve" x1="140" y1="58" x2="283" y2="58"/><polygon class="dot" points="290,58 280,53 280,63"/><line class="line" x1="10" y1="70" x2="450" y2="70"/><line class="line" x1="20" y1="64" x2="20" y2="76"/><text class="dim" x="20" y="94" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="64" x2="50" y2="76"/><text class="dim" x="50" y="94" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="64" x2="80" y2="76"/><text class="dim" x="80" y="94" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="64" x2="110" y2="76"/><text class="dim" x="110" y="94" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="64" x2="140" y2="76"/><text class="dim" x="140" y="94" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="64" x2="170" y2="76"/><text class="dim" x="170" y="94" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="64" x2="200" y2="76"/><text class="dim" x="200" y="94" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="61" x2="230" y2="79"/><text class="ink" x="230" y="94" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="64" x2="260" y2="76"/><text class="dim" x="260" y="94" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="64" x2="290" y2="76"/><text class="dim" x="290" y="94" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="64" x2="320" y2="76"/><text class="dim" x="320" y="94" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="64" x2="350" y2="76"/><text class="dim" x="350" y="94" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="64" x2="380" y2="76"/><text class="dim" x="380" y="94" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="64" x2="410" y2="76"/><text class="dim" x="410" y="94" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="64" x2="440" y2="76"/><text class="dim" x="440" y="94" font-size="11" text-anchor="middle">7</text><circle class="dot3" cx="290" cy="70" r="5"/><text class="ink" x="230" y="128" font-size="13" text-anchor="middle">2 − 6 = 2 + (−6) = −4</text><text class="dim" x="230" y="144" font-size="11" text-anchor="middle">önce 2'ye git, sonra 6 adım sola</text><line class="curve" x1="230" y1="156" x2="283" y2="156"/><polygon class="dot" points="290,156 280,151 280,161"/><line class="curve2" x1="290" y1="168" x2="117" y2="168"/><polygon class="dot2" points="110,168 120,163 120,173"/><line class="line" x1="10" y1="180" x2="450" y2="180"/><line class="line" x1="20" y1="174" x2="20" y2="186"/><text class="dim" x="20" y="204" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="174" x2="50" y2="186"/><text class="dim" x="50" y="204" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="174" x2="80" y2="186"/><text class="dim" x="80" y="204" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="174" x2="110" y2="186"/><text class="dim" x="110" y="204" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="174" x2="140" y2="186"/><text class="dim" x="140" y="204" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="174" x2="170" y2="186"/><text class="dim" x="170" y="204" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="174" x2="200" y2="186"/><text class="dim" x="200" y="204" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="171" x2="230" y2="189"/><text class="ink" x="230" y="204" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="174" x2="260" y2="186"/><text class="dim" x="260" y="204" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="174" x2="290" y2="186"/><text class="dim" x="290" y="204" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="174" x2="320" y2="186"/><text class="dim" x="320" y="204" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="174" x2="350" y2="186"/><text class="dim" x="350" y="204" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="174" x2="380" y2="186"/><text class="dim" x="380" y="204" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="174" x2="410" y2="186"/><text class="dim" x="410" y="204" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="174" x2="440" y2="186"/><text class="dim" x="440" y="204" font-size="11" text-anchor="middle">7</text><circle class="dot3" cx="110" cy="180" r="5"/></svg>
  <figcaption>Toplama sayı doğrusunda yürümektir. $-3 + 5$: $-3$'ten başlayıp $5$ adım sağa giderek $2$'ye varıyoruz. Çıkarma, zıttını eklemek: $2 - 6$, $2$'den $6$ adım sola gitmek ve $-4$'e varmak.</figcaption>
</figure>

Bu yürüyüş iki kurala dönüşüyor:

| Durum | Kural | Örnek |
|---|---|---|
| İşaretler aynı | mutlak değerleri topla, ortak işareti koy | $-4 + (-6) = -10$ |
| İşaretler farklı | büyük mutlak değerden küçüğü çıkar, büyüğün işaretini koy | $-9 + 4 = -5$ |

İkinci satırda $\lvert -9 \rvert = 9$ büyük, $9 - 4 = 5$ ve sonuç $-9$'un işaretini
alıyor. Borç benzetmesi işe yarar: $9$ lira borcun var, $4$ lira
ödedin; hâlâ $5$ lira borçlusun.

## Çıkarma: zıttını eklemek

Tam sayılarda çıkarmayı ayrı bir işlem gibi ezberlemek yerine **toplamaya
çeviriyoruz**:

$$
a - b = a + (-b)
$$

Böylece her çıkarma bir toplama olur ve yukarıdaki iki kural yeter:

$$
\begin{aligned}
3 - 8 &= 3 + (-8) = -5 \\
-2 - 6 &= -2 + (-6) = -8 \\
5 - (-4) &= 5 + 4 = 9 \\
-7 - (-10) &= -7 + 10 = 3
\end{aligned}
$$

**Negatif bir sayıyı çıkarmak, pozitifini eklemektir.** Sıcaklık
$-3$ dereceden $5$ dereceye çıktıysa fark $5 - (-3) = 8$ derece.

## Çarpma ve bölme: işaret kuralları

Önce mutlak değerleri çarp ya da böl, sonra işareti belirle:

| | pozitif | negatif |
|---|---|---|
| **pozitif** | $+$ | $-$ |
| **negatif** | $-$ | $+$ |

**Aynı işaretler pozitif, farklı işaretler negatif** verir:

$$
(-3) \cdot 4 = -12, \qquad (-3) \cdot (-4) = 12, \qquad (-20) \div 5 = -4, \qquad (-20) \div (-5) = 4
$$

Bölme için kural aynı, çünkü bölme çarpmanın tersi: $(-20) \div (-5) =
4$, çünkü $4 \cdot (-5) = -20$.

### Neden eksi çarpı eksi artı?

Bir örüntüyle görelim. $-3$'ü sırayla $3, 2, 1, 0$ ile çarpalım:

$$
\begin{aligned}
(-3) \cdot 3 &= -9 \\
(-3) \cdot 2 &= -6 \\
(-3) \cdot 1 &= -3 \\
(-3) \cdot 0 &= 0
\end{aligned}
$$

Çarpan her $1$ azaldığında sonuç $3$ **artıyor**. Örüntü devam ederse
$(-3) \cdot (-1) = 3$, $(-3) \cdot (-2) = 6$ olmalı. Başka bir cevap,
dağılma özelliğini bozardı: $(-3) \cdot (2 + (-2)) = (-3) \cdot 0 = 0$
olmalı, bu da ancak $(-3)(-2) = 6$ ise tutar.

**Çok çarpanlı işlemlerde** eksileri say: çift sayıda eksi varsa sonuç
pozitif, tek sayıda eksi varsa negatif.

$$
(-1) \cdot (-2) \cdot (-3) = -6, \qquad (-1) \cdot (-2) \cdot (-3) \cdot (-4) = 24
$$

## Negatif sayıların kuvvetleri

Burada parantez her şey:

$$
(-2)^2 = (-2) \cdot (-2) = 4, \qquad -2^2 = -(2 \cdot 2) = -4
$$

$-2^2$ yazısında üs yalnızca $2$'ye ait; eksi en son uygulanıyor (üs,
işlem önceliğinde önce gelir). Negatif bir sayının:

- **çift** kuvveti pozitif: $(-2)^4 = 16$,
- **tek** kuvveti negatif: $(-2)^3 = -8$.

$(-1)^n$ bu yüzden $n$ çiftse $1$, tekse $-1$; işaretleri sırayla
değiştirmek için matematikte sık kullanılıyor.

## İşlem önceliği negatiflerle

Kural değişmiyor; yalnızca işaretlere dikkat:

$$
\begin{aligned}
-8 + 3 \cdot (-2) - (-5) &= -8 + (-6) + 5 \\
&= -14 + 5 = -9
\end{aligned}
$$

Adımlar: çarpma ($3 \cdot (-2) = -6$), eksi bir negatifi çıkarmayı
toplamaya çevir ($-(-5) = +5$), sonra soldan sağa topla.

## Makine öğrenmesinde negatif sayılar

**Hata.** Bir modelin hatası çoğu zaman gerçek değer eksi tahmin:
$e = y - \hat{y}$. Model fazla tahmin ettiyse hata negatif, az tahmin
ettiyse pozitif. Gerçek $20$, tahmin $23$ ise $e = 20 - 23 = -3$.

**Hatalar birbirini götürebilir.** Hataları $-3, 2, 4, -3$ olan bir
modelin hata toplamı $0$; ama model hiçbir tahmini doğru yapmamış! Bu
yüzden hatalar ya mutlak değerle ($|{-3}| + |2| + |4| + |{-3}| = 12$) ya
da karesiyle toplanır. Negatif bir sayının karesi pozitif olduğu için
kareler de birbirini götürmez.

**Yön.** Model eğitiminde "eğim negatifse ağırlığı artır, pozitifse
azalt" gibi kurallar var: bir sayının işareti bir **yön** bilgisi taşıyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$-5 > -2$</p>
      <p>$-2^2 = 4$</p>
      <p>$5 - (-3) = 2$</p>
      <p>$(-4)(-5) = -20$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$-5 < -2$ (daha solda)</p>
      <p>$-2^2 = -4$, ama $(-2)^2 = 4$</p>
      <p>$5 - (-3) = 5 + 3 = 8$</p>
      <p>$(-4)(-5) = 20$</p>
    </div>
  </div>
  <figcaption>Negatiflerde hataların çoğu işaretten ve parantezden çıkıyor.</figcaption>
</figure>

- **"İki eksi artı yapar" kuralını toplamaya uygulamak.** $-3 + (-4)$
  $7$ değil, $-7$: aynı işaretli iki sayı toplanınca işaret korunur.
  "Eksi çarpı eksi artı" yalnızca çarpma ve bölme için.
- **Mutlak değeri "eksiyi silmek" sanıp ifadenin içine uygulamak.**
  $|3 - 8| = \lvert -5 \rvert = 5$; önce içini hesapla, sonra mutlak değer al.
  $|3| - |8| = -5$ başka bir şey.

## Özet

- Tam sayılar: $\dots, -2, -1, 0, 1, 2, \dots$; sayı doğrusunda sağdaki büyük.
- Zıt sayı: $a + (-a) = 0$; $-(-a) = a$.
- Mutlak değer sıfıra uzaklık: $|a| \ge 0$; $a$ ile $b$ arası uzaklık $|a - b|$.
- Toplama: aynı işaret → topla, işareti koru; farklı işaret → çıkar, büyüğün işareti.
- Çıkarma, zıttını eklemek: $a - b = a + (-b)$.
- Çarpma ve bölme: aynı işaret $+$, farklı işaret $-$; çok çarpanda eksileri say.
- $(-2)^2 = 4$ ama $-2^2 = -4$; negatifin çift kuvveti pozitif, tek kuvveti negatif.
- Hatalar işaretli; toplarken birbirini götürmesin diye mutlak değer ya da kare alınır.
