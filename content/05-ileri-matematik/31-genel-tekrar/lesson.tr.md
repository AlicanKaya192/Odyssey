# Genel Tekrar

MAT 2 burada bitiyor. Vektörlerle başladın; matrisler, özdeğerler ve SVD
ile veriyi geometrik bir nesne olarak gördün. Limit, türev, gradyan ve
geri yayılımla bir modelin nasıl öğrendiğini çıkardın. Olasılık,
dağılımlar, örnekleme ve kestirimle belirsizliği ölçtün; sonunda
regresyon, lojistik regresyon, entropi ve PCA'da üç kolun birleştiğini
gördün. Bu bölüm yeni bir konu öğretmiyor: parçaların nasıl bağlandığını
gösteriyor, hepsini tek bir problemde birlikte kullanıyor ve en sık
düşülen tuzakları tek listede topluyor. Sınav ve problemler bütün
modülden karışık.

## Parçalar nasıl bağlanıyor?

MAT 2 üç kolda ilerliyor ve üçü de makine öğrenmesinde buluşuyor.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Vektörler</b><br>nokta çarpımı, uzunluk</span>
    <span class="arrow">→</span>
    <span class="node"><b>Matrisler</b><br>çarpım, ters, sistemler</span>
    <span class="arrow">→</span>
    <span class="node"><b>Özdeğer ve SVD</b><br>matrisin iskeleti</span>
  </div>
  <figcaption>Doğrusal cebir kolu: veri bir matris, model bir matris çarpımı, verinin şekli özvektörlerde.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Limit ve türev</b><br>değişim hızı</span>
    <span class="arrow">→</span>
    <span class="node"><b>Gradyan</b><br>çok değişkenli eğim</span>
    <span class="arrow">→</span>
    <span class="node"><b>Gradyan inişi</b><br>adım adım en küçüğe</span>
    <span class="arrow">→</span>
    <span class="node"><b>Geri yayılım</b><br>zincir kuralı katman katman</span>
  </div>
  <figcaption>Kalkülüs kolu: bir modelin öğrenmesi, kaybın gradyanını hesaplayıp ters yönde adım atmaktır.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Olasılık</b><br>koşullu, Bayes</span>
    <span class="arrow">→</span>
    <span class="node"><b>Dağılımlar</b><br>beklenen değer, varyans</span>
    <span class="arrow">→</span>
    <span class="node"><b>Örnekleme</b><br>standart hata, test</span>
    <span class="arrow">→</span>
    <span class="node"><b>Kestirim</b><br>MLE, kayıp fonksiyonları</span>
  </div>
  <figcaption>Olasılık ve istatistik kolu: kayıp fonksiyonları olabilirlikten doğar; sonuçların güvenilirliği örneklemeyle ölçülür.</figcaption>
</figure>

Son bölümler üç kolu birleştiriyor: doğrusal regresyonda normal
denklemler (cebir), kayıp ve gradyan (kalkülüs) ve normal gürültü
(olasılık) aynı çözümü veriyor; PCA kovaryans matrisinin özvektörleri;
çapraz entropi hem bilgi kuramı hem olabilirlik.

## Baştan sona bir problem

Bir öneri ve sınıflandırma sistemi üzerinde çalışan bir mühendis düşün.
Sorular sırayla MAT 2'nin farklı köşelerinden geliyor.

### 1. Benzerlik: vektörler

İki kullanıcının üç filme verdiği puanlar $a = (4, 0, 3)$ ve
$b = (3, 1, 4)$. Nokta çarpımı $12 + 0 + 12 = 24$; uzunluklar
$\lVert a \rVert = 5$, $\lVert b \rVert = \sqrt{26} \approx 5{,}10$.

$$
\cos\theta = \frac{a \cdot b}{\lVert a \rVert \lVert b \rVert} \approx \frac{24}{25{,}50} \approx 0{,}94
$$

Zevkleri çok benzer; birinin sevdiği filmi ötekine önermek mantıklı.

### 2. Model ve kayıp: türev

Basit bir model $\hat{y} = wx$; veri $x = (1, 2, 3)$, $y = (1, 3, 5)$.
Kayıp $J(w) = \sum (y_i - wx_i)^2$ ve türevi:

$$
J'(w) = -2\sum x_i y_i + 2w\sum x_i^2 = -44 + 28w
$$

Türevi sıfır yapan nokta $w^* = \frac{22}{14} \approx 1{,}57$; bu, normal
denklemlerin tek boyutlu hâli $w = \frac{\sum xy}{\sum x^2}$.

### 3. Öğrenme: gradyan inişi

Veri çok büyük olsaydı formül yerine adım adım giderdik:
$w \leftarrow w - \eta J'(w)$, $\eta = 0{,}01$. $w_0 = 0$'dan
$w_1 = 0{,}44$, $w_2 \approx 0{,}76$, $w_3 \approx 0{,}98$…

<figure class="fig">
<svg viewBox="0 0 420 262" width="420"><line class="grid" x1="50.0" y1="226.0" x2="50.0" y2="26.0"/><line class="grid" x1="78.3" y1="226.0" x2="78.3" y2="26.0"/><line class="grid" x1="106.7" y1="226.0" x2="106.7" y2="26.0"/><line class="grid" x1="135.0" y1="226.0" x2="135.0" y2="26.0"/><line class="grid" x1="163.3" y1="226.0" x2="163.3" y2="26.0"/><line class="grid" x1="191.7" y1="226.0" x2="191.7" y2="26.0"/><line class="grid" x1="220.0" y1="226.0" x2="220.0" y2="26.0"/><line class="grid" x1="248.3" y1="226.0" x2="248.3" y2="26.0"/><line class="grid" x1="276.7" y1="226.0" x2="276.7" y2="26.0"/><line class="grid" x1="305.0" y1="226.0" x2="305.0" y2="26.0"/><line class="grid" x1="333.3" y1="226.0" x2="333.3" y2="26.0"/><line class="grid" x1="361.7" y1="226.0" x2="361.7" y2="26.0"/><line class="grid" x1="390.0" y1="226.0" x2="390.0" y2="26.0"/><line class="grid" x1="50.0" y1="226.0" x2="390.0" y2="226.0"/><line class="grid" x1="50.0" y1="201.0" x2="390.0" y2="201.0"/><line class="grid" x1="50.0" y1="176.0" x2="390.0" y2="176.0"/><line class="grid" x1="50.0" y1="151.0" x2="390.0" y2="151.0"/><line class="grid" x1="50.0" y1="126.0" x2="390.0" y2="126.0"/><line class="grid" x1="50.0" y1="101.0" x2="390.0" y2="101.0"/><line class="grid" x1="50.0" y1="76.0" x2="390.0" y2="76.0"/><line class="grid" x1="50.0" y1="51.0" x2="390.0" y2="51.0"/><line class="grid" x1="50.0" y1="26.0" x2="390.0" y2="26.0"/><line class="line" x1="50.0" y1="226.0" x2="390.0" y2="226.0"/><polyline class="curve" fill="none" points="61.3,23.6 62.8,26.0 64.2,28.3 65.6,30.6 67.0,33.0 68.4,35.3 69.8,37.5 71.2,39.8 72.7,42.1 74.1,44.3 75.5,46.6 76.9,48.8 78.3,51.0 79.8,53.2 81.2,55.4 82.6,57.5 84.0,59.7 85.4,61.8 86.8,63.9 88.2,66.1 89.7,68.2 91.1,70.2 92.5,72.3 93.9,74.4 95.3,76.4 96.8,78.4 98.2,80.4 99.6,82.4 101.0,84.4 102.4,86.4 103.8,88.3 105.2,90.3 106.7,92.2 108.1,94.1 109.5,96.0 110.9,97.9 112.3,99.8 113.8,101.6 115.2,103.5 116.6,105.3 118.0,107.1 119.4,108.9 120.8,110.7 122.3,112.5 123.7,114.2 125.1,116.0 126.5,117.7 127.9,119.4 129.3,121.1 130.8,122.8 132.2,124.5 133.6,126.2 135.0,127.8 136.4,129.4 137.8,131.1 139.2,132.7 140.7,134.2 142.1,135.8 143.5,137.4 144.9,138.9 146.3,140.5 147.8,142.0 149.2,143.5 150.6,145.0 152.0,146.5 153.4,147.9 154.8,149.4 156.2,150.8 157.7,152.2 159.1,153.7 160.5,155.1 161.9,156.4 163.3,157.8 164.8,159.2 166.2,160.5 167.6,161.8 169.0,163.1 170.4,164.4 171.8,165.7 173.2,167.0 174.7,168.2 176.1,169.5 177.5,170.7 178.9,171.9 180.3,173.1 181.8,174.3 183.2,175.5 184.6,176.6 186.0,177.8 187.4,178.9 188.8,180.0 190.2,181.1 191.7,182.2 193.1,183.3 194.5,184.3 195.9,185.4 197.3,186.4 198.7,187.4 200.2,188.4 201.6,189.4 203.0,190.4 204.4,191.4 205.8,192.3 207.2,193.2 208.7,194.2 210.1,195.1 211.5,195.9 212.9,196.8 214.3,197.7 215.8,198.5 217.2,199.4 218.6,200.2 220.0,201.0 221.4,201.8 222.8,202.6 224.2,203.3 225.7,204.1 227.1,204.8 228.5,205.5 229.9,206.3 231.3,207.0 232.8,207.6 234.2,208.3 235.6,209.0 237.0,209.6 238.4,210.2 239.8,210.8 241.2,211.4 242.7,212.0 244.1,212.6 245.5,213.1 246.9,213.7 248.3,214.2 249.8,214.7 251.2,215.2 252.6,215.7 254.0,216.2 255.4,216.6 256.8,217.1 258.2,217.5 259.7,217.9 261.1,218.3 262.5,218.7 263.9,219.1 265.3,219.4 266.8,219.8 268.2,220.1 269.6,220.4 271.0,220.7 272.4,221.0 273.8,221.3 275.2,221.6 276.7,221.8 278.1,222.0 279.5,222.3 280.9,222.5 282.3,222.6 283.8,222.8 285.2,223.0 286.6,223.1 288.0,223.3 289.4,223.4 290.8,223.5 292.2,223.6 293.7,223.7 295.1,223.7 296.5,223.8 297.9,223.8 299.3,223.8 300.8,223.9 302.2,223.9 303.6,223.8 305.0,223.8 306.4,223.8 307.8,223.7 309.2,223.6 310.7,223.5 312.1,223.4 313.5,223.3 314.9,223.2 316.3,223.0 317.8,222.9 319.2,222.7 320.6,222.5 322.0,222.3 323.4,222.1 324.8,221.9 326.2,221.6 327.7,221.4 329.1,221.1 330.5,220.8 331.9,220.5 333.3,220.2 334.8,219.9 336.2,219.5 337.6,219.2 339.0,218.8 340.4,218.4 341.8,218.0 343.2,217.6 344.7,217.2 346.1,216.8 347.5,216.3 348.9,215.8 350.3,215.4 351.8,214.9 353.2,214.3 354.6,213.8 356.0,213.3 357.4,212.7 358.8,212.2 360.2,211.6 361.7,211.0 363.1,210.4 364.5,209.8 365.9,209.1 367.3,208.5 368.8,207.8 370.2,207.1 371.6,206.5 373.0,205.8 374.4,205.0 375.8,204.3 377.2,203.6 378.7,202.8 380.1,202.0 381.5,201.2 382.9,200.4 384.3,199.6 385.8,198.8 387.2,197.9 388.6,197.1 390.0,196.2"/><line class="curve2" x1="78.3" y1="51.0" x2="136.9" y2="129.1"/><polygon class="dot2" points="140.7,134.2 133.7,130.3 138.9,126.4"/><line class="curve2" x1="140.7" y1="134.2" x2="180.9" y2="173.0"/><polygon class="dot2" points="185.5,177.4 178.0,174.7 182.5,170.0"/><line class="curve2" x1="185.5" y1="177.4" x2="212.6" y2="196.2"/><polygon class="dot2" points="217.9,199.8 210.0,198.3 213.7,193.0"/><line class="curve2" x1="217.9" y1="199.8" x2="235.4" y2="208.5"/><polygon class="dot2" points="241.1,211.4 233.1,211.1 236.0,205.2"/><line class="curve2" x1="241.1" y1="211.4" x2="251.9" y2="215.2"/><polygon class="dot2" points="257.9,217.4 249.9,218.0 252.1,211.9"/><line class="curve2" x1="257.9" y1="217.4" x2="263.7" y2="218.9"/><polygon class="dot2" points="269.9,220.5 262.0,221.8 263.6,215.5"/><circle class="dot2" cx="78.3" cy="51.0" r="3.6"/><circle class="dot2" cx="140.7" cy="134.2" r="3.6"/><circle class="dot2" cx="185.5" cy="177.4" r="3.6"/><circle class="dot2" cx="217.9" cy="199.8" r="3.6"/><circle class="dot2" cx="241.1" cy="211.4" r="3.6"/><circle class="dot2" cx="257.9" cy="217.4" r="3.6"/><circle class="dot2" cx="269.9" cy="220.5" r="3.6"/><line class="curve3" stroke-dasharray="5 4" x1="301.0" y1="226.0" x2="301.0" y2="223.9"/><circle class="dot3" cx="301.0" cy="223.9" r="4.5"/><text class="ink" x="86.3" y="55.0" font-size="10" text-anchor="start">w₀ = 0</text><text class="ink" x="148.7" y="138.2" font-size="10" text-anchor="start">w₁ = 0,44</text><text class="ink" x="301.0" y="240.0" font-size="10" text-anchor="middle">w* ≈ 1,57</text><text class="ink" x="382.9" y="166.0" font-size="11" text-anchor="end">J(w) = Σ(y − wx)²</text><text class="dim" x="248.3" y="66.0" font-size="10" text-anchor="middle">her adımda hata 0,72 katına iniyor</text><text class="dim" x="78.3" y="240.0" font-size="9" text-anchor="middle">0,0</text><text class="dim" x="149.2" y="240.0" font-size="9" text-anchor="middle">0,5</text><text class="dim" x="220.0" y="240.0" font-size="9" text-anchor="middle">1,0</text><text class="dim" x="361.7" y="240.0" font-size="9" text-anchor="middle">2,0</text><text class="dim" x="390.0" y="254.0" font-size="10" text-anchor="end">w</text></svg>
  <figcaption>Kayıp parabolü üzerinde gradyan inişi. Her adım en küçük noktaya olan uzaklığı 0,72 katına indiriyor; adımlar giderek kısalıyor çünkü eğim düzleşiyor.</figcaption>
</figure>

### 4. Sınıflandırma: lojistik regresyon

Başka bir model bir e-postanın spam olma olasılığını $p = \sigma(2x - 3)$
ile veriyor. $x = 2$ için $p = \sigma(1) \approx 0{,}731$. E-posta gerçekten
spamse ($y = 1$) log-loss $-\ln 0{,}731 \approx 0{,}313$; ağırlığın
gradyanı $(p - y)x \approx -0{,}269 \cdot 2 \approx -0{,}538$: ağırlık
artırılacak.

### 5. Kararın güvenilirliği: Bayes

E-postaların yüzde $20$'si spam. Model spamlerin yüzde $90$'ını, normal
e-postaların yüzde $5$'ini "spam" diye işaretliyor.
$P(\text{işaret}) = 0{,}18 + 0{,}04 = 0{,}22$ ve

$$
P(\text{spam} \mid \text{işaret}) = \frac{0{,}18}{0{,}22} \approx 0{,}82
$$

İşaretlenenlerin yaklaşık beşte biri aslında normal.

### 6. Değerlendirme: güven aralığı

Model $400$ test e-postasında yüzde $85$ doğruluk aldı.
$\text{SE} = \sqrt{\frac{0{,}85 \cdot 0{,}15}{400}} \approx 0{,}018$; yüzde
$95$ güven aralığı $0{,}85 \pm 0{,}035$, yani yaklaşık
$[0{,}815; \ 0{,}885]$. Başka bir modelin yüzde $86$'sı bu aralığın içinde:
fark için daha çok test verisi gerekir.

### 7. Özellikleri sıkıştırmak: PCA

İki özelliğin kovaryans matrisi $\begin{pmatrix} 5 & 4 \\ 4 & 5
\end{pmatrix}$. Özdeğerler $9$ ve $1$: tek bir bileşen varyansın yüzde
$90$'ını taşıyor, iki özellik yerine birini kullanmak yeterli olabilir.

Yedi adımda vektörler, türev, gradyan inişi, sigmoid ve log-loss, Bayes,
güven aralığı ve özdeğerler birlikte çalıştı. Bir makine öğrenmesi
sisteminin matematiği tam olarak bu parçalardan oluşur.

## Bölüm bölüm ne öğrendin?

| Konu | Anahtar fikir | Makine öğrenmesinde |
|---|---|---|
| Vektörler, nokta çarpımı | uzunluk, açı, kosinüs benzerliği | benzerlik araması |
| Matrisler ve çarpım | boyut kuralı, dönüşüm | katmanlar $Wx + b$ |
| Determinant, ters, sistemler | Gauss eleme, rank | normal denklemler |
| Özdeğer ve SVD | $Av = \lambda v$, $A = USV^\mathsf{T}$ | PCA, sıkıştırma |
| Limit ve süreklilik | yaklaşma | türevin temeli |
| Türev ve kuralları | eğim, zincir kuralı | geri yayılım |
| Türevin uygulamaları | $f' = 0$, ikinci türev | kaybın en küçüğü |
| Taylor | yerel polinom yaklaşımı | optimizasyon |
| İntegral | alan, birikim | olasılık yoğunluğu |
| Gradyan, Jacobian, Hessian | en dik yön, eğrilik | çok parametreli eğitim |
| Dışbükeylik, gradyan inişi | $w \leftarrow w - \eta\nabla J$ | eğitim döngüsü |
| Geri yayılım | zincir kuralı katman katman | sinir ağları |
| Koşullu olasılık, Bayes | $P(A \mid B)$, önsel ve sonsal | spam filtresi, tanı |
| Rastgele değişkenler, dağılımlar | $E$, $\operatorname{Var}$, binom, normal | modelleme |
| Örnekleme, test | $\text{SE} = \frac{\sigma}{\sqrt{n}}$, p değeri | A/B testi |
| Kovaryans, korelasyon | birlikte değişim | çoklu doğrusallık |
| En çok olabilirlik | veriyi en olası kılan parametre | kayıp fonksiyonları |
| Doğrusal ve lojistik regresyon | $X^\mathsf{T}Xw = X^\mathsf{T}y$; sigmoid, log-loss | temel modeller |
| Entropi, çapraz entropi, KL | bilgi ve fazladan bit | sınıflandırma kaybı |
| PCA | kovaryansın özvektörleri | boyut indirgeme |

## En sık düşülen tuzaklar

| Tuzak | Doğrusu |
|---|---|
| $AB = BA$ | matris çarpımı genelde değişmeli değil |
| $(AB)^{-1} = A^{-1}B^{-1}$ | $B^{-1}A^{-1}$ |
| $\det(A + B) = \det A + \det B$ | determinant toplamaya dağılmaz |
| $\frac{d}{dx}f(g(x)) = f'(g(x))$ | $\times\, g'(x)$ unutulmaz |
| türev sıfır, öyleyse en küçük | en büyük ya da eyer olabilir |
| büyük öğrenme oranı her zaman hızlı | ıraksayabilir |
| $P(A \mid B) = P(B \mid A)$ | Bayes ile çevrilir |
| $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y$ her zaman | $+ 2\operatorname{Cov}(X, Y)$ |
| $\text{SE} = \frac{\sigma}{n}$ | $\frac{\sigma}{\sqrt{n}}$ |
| p değeri $H_0$'ın olasılığı | veri hakkında bir olasılık |
| korelasyon nedensellik | deney gerekir |
| KL simetrik | $D(P \parallel Q) \neq D(Q \parallel P)$ |
| PCA'dan önce merkezlememek | önce ortalamayı çıkar |

## Bir sonraki adım

MAT 2 ile yapay zekanın matematik temeli tamamlandı. Buradan sonra:

- **Makine Öğrenmesi patikası:** burada türettiğin her formülün kodda nasıl
  kullanıldığını görürsün; doğrusal ve lojistik regresyon, karar ağaçları,
  kümeleme ve boyut indirgeme.
- **Kendin yaz:** gradyan inişini, lojistik regresyonu ya da PCA'yı
  yalnızca NumPy ile yazmak, matematiği pekiştirmenin en iyi yolu.
- **Derin öğrenme:** sinir ağları, geri yayılımın büyük ölçekli hâli;
  matris çarpımı, zincir kuralı, softmax ve çapraz entropi orada her
  satırda.

## Özet

- MAT 2'nin üç kolu: doğrusal cebir (veri ve modelin dili), kalkülüs
  (öğrenmenin mekanizması), olasılık ve istatistik (belirsizlik ve kayıp).
- Gerçek bir problemde üç kol birlikte çalışıyor: benzerlik vektörle,
  öğrenme gradyanla, karar olasılıkla, güvenilirlik örneklemeyle ölçülüyor.
- Regresyon, lojistik regresyon, entropi ve PCA üç kolun kesiştiği yerler.
- En sık hatalar değişmeli sanılan işlemlerden, unutulan zincir çarpanından,
  ters çevrilen koşullu olasılıktan ve karekök ile $n$ arasındaki
  karışıklıktan geliyor.
