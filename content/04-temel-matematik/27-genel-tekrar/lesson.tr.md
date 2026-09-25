# Genel Tekrar

MAT 1 burada bitiyor. Sayıları okumaktan başladın; kesirler, üsler ve
köklerle hesap yaptın, cebirle denklem kurdun, fonksiyonlarla ilişkileri
çizdin, geometri ve trigonometriyle şekilleri ölçtün, sayma, olasılık ve
istatistikle belirsizliği sayılara döktün. Bu bölüm yeni bir konu
öğretmiyor: parçaların birbirine nasıl bağlandığını gösteriyor, hepsini
tek bir problemde birlikte kullanıyor ve en sık düşülen tuzakları tek
listede topluyor. Sınav ve problemler de bütün modülden karışık.

## Parçalar nasıl bağlanıyor?

MAT 1'in konuları dört kolda ilerliyor ve hepsi MAT 2'ye akıyor.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Sayılar</b><br>işlem önceliği, kesir, ondalık</span>
    <span class="arrow">→</span>
    <span class="node"><b>Üs ve kök</b><br>kuvvet kuralları</span>
    <span class="arrow">→</span>
    <span class="node"><b>Cebir</b><br>ifade, çarpanlar, denklem</span>
    <span class="arrow">→</span>
    <span class="node"><b>Fonksiyonlar</b><br>doğru, polinom, üstel, logaritma</span>
  </div>
  <figcaption>Hesap kolu: her adım bir öncekinin dilini kullanıyor. Fonksiyonlar bölümü, sonraki her konunun konuştuğu dil.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Koordinat</b><br>nokta, uzaklık, eğim</span>
    <span class="arrow">→</span>
    <span class="node"><b>Geometri</b><br>açı, Pisagor, alan</span>
    <span class="arrow">→</span>
    <span class="node"><b>Trigonometri</b><br>sin, cos, birim çember</span>
  </div>
  <figcaption>Şekil kolu: Pisagor uzaklık formülünü, dik üçgen trigonometriyi doğuruyor. MAT 2'de vektörler bu kolun devamı.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Kümeler</b><br>birleşim, kesişim</span>
    <span class="arrow">→</span>
    <span class="node"><b>Sayma</b><br>permütasyon, kombinasyon</span>
    <span class="arrow">→</span>
    <span class="node"><b>Olasılık</b><br>olay, bağımsızlık</span>
    <span class="arrow">→</span>
    <span class="node"><b>İstatistik</b><br>ortalama, yayılım</span>
  </div>
  <figcaption>Belirsizlik kolu: olaylar küme, olasılık sayma, istatistik de verinin olasılık diliyle özeti.</figcaption>
</figure>

Dördüncü kol Diziler ve Σ gösterimi: ortalamadan hata fonksiyonuna kadar
her toplam onunla yazılıyor ve üç kolun hepsinde kullanılıyor.

## Baştan sona bir problem

Bir öğrenme uygulamasının verisine bakan bir analist düşün. Sorular
sırayla MAT 1'in farklı köşelerinden geliyor.

### 1. Büyüme: üstel fonksiyon

Uygulamanın $2000$ kullanıcısı var ve kullanıcı sayısı her ay yüzde $10$
artıyor. $t$ ay sonra:

$$
N(t) = 2000 \cdot 1{,}1^t
$$

$6$ ay sonra $2000 \cdot 1{,}1^6 \approx 2000 \cdot 1{,}7716 \approx 3543$.
Yüzdeler toplanmıyor: altı ayda yüzde $60$ değil, yaklaşık yüzde $77$
artış.

### 2. Ne zaman? Logaritma

Kullanıcı sayısı kaç ayda iki katına çıkar? $1{,}1^t = 2$; iki tarafın
logaritmasını al:

$$
t = \frac{\ln 2}{\ln 1{,}1} \approx \frac{0{,}6931}{0{,}0953} \approx 7{,}27
$$

$10\,000$'e ne zaman ulaşır? $1{,}1^t = 5$, $t = \frac{\ln 5}{\ln 1{,}1}
\approx 16{,}9$; yani $17.$ ayın sonunda geçer.

<figure class="fig">
<svg viewBox="0 0 440 254" width="440"><line class="grid" x1="55.0" y1="240.0" x2="55.0" y2="20.0"/><line class="grid" x1="91.8" y1="240.0" x2="91.8" y2="20.0"/><line class="grid" x1="128.7" y1="240.0" x2="128.7" y2="20.0"/><line class="grid" x1="165.5" y1="240.0" x2="165.5" y2="20.0"/><line class="grid" x1="202.4" y1="240.0" x2="202.4" y2="20.0"/><line class="grid" x1="239.2" y1="240.0" x2="239.2" y2="20.0"/><line class="grid" x1="276.1" y1="240.0" x2="276.1" y2="20.0"/><line class="grid" x1="312.9" y1="240.0" x2="312.9" y2="20.0"/><line class="grid" x1="349.7" y1="240.0" x2="349.7" y2="20.0"/><line class="grid" x1="386.6" y1="240.0" x2="386.6" y2="20.0"/><line class="grid" x1="55.0" y1="240.0" x2="405.0" y2="240.0"/><line class="grid" x1="55.0" y1="203.3" x2="405.0" y2="203.3"/><line class="grid" x1="55.0" y1="166.7" x2="405.0" y2="166.7"/><line class="grid" x1="55.0" y1="130.0" x2="405.0" y2="130.0"/><line class="grid" x1="55.0" y1="93.3" x2="405.0" y2="93.3"/><line class="grid" x1="55.0" y1="56.7" x2="405.0" y2="56.7"/><line class="grid" x1="55.0" y1="20.0" x2="405.0" y2="20.0"/><line class="line" x1="55.0" y1="240.0" x2="405.0" y2="240.0"/><line class="line" x1="55.0" y1="240.0" x2="55.0" y2="20.0"/><text class="dim" x="91.8" y="253.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="128.7" y="253.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="165.5" y="253.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="202.4" y="253.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="239.2" y="253.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="276.1" y="253.0" font-size="9" text-anchor="middle">12</text><text class="dim" x="312.9" y="253.0" font-size="9" text-anchor="middle">14</text><text class="dim" x="349.7" y="253.0" font-size="9" text-anchor="middle">16</text><text class="dim" x="386.6" y="253.0" font-size="9" text-anchor="middle">18</text><text class="dim" x="50.0" y="206.3" font-size="9" text-anchor="end">2000</text><text class="dim" x="50.0" y="169.7" font-size="9" text-anchor="end">4000</text><text class="dim" x="50.0" y="133.0" font-size="9" text-anchor="end">6000</text><text class="dim" x="50.0" y="96.3" font-size="9" text-anchor="end">8000</text><text class="dim" x="50.0" y="59.7" font-size="9" text-anchor="end">10000</text><text class="dim" x="50.0" y="23.0" font-size="9" text-anchor="end">12000</text><line class="curve3" stroke-dasharray="5 4" x1="55.0" y1="56.7" x2="405.0" y2="56.7"/><line class="curve3" stroke-dasharray="5 4" x1="55.0" y1="166.7" x2="189.0" y2="166.7"/><polyline class="curve" fill="none" points="55.0,203.3 56.5,203.1 57.9,202.8 59.4,202.5 60.8,202.2 62.3,201.9 63.8,201.6 65.2,201.3 66.7,201.1 68.1,200.8 69.6,200.5 71.0,200.2 72.5,199.9 74.0,199.6 75.4,199.2 76.9,198.9 78.3,198.6 79.8,198.3 81.2,198.0 82.7,197.7 84.2,197.4 85.6,197.0 87.1,196.7 88.5,196.4 90.0,196.1 91.5,195.7 92.9,195.4 94.4,195.0 95.8,194.7 97.3,194.4 98.8,194.0 100.2,193.7 101.7,193.3 103.1,193.0 104.6,192.6 106.0,192.3 107.5,191.9 109.0,191.5 110.4,191.2 111.9,190.8 113.3,190.4 114.8,190.0 116.2,189.7 117.7,189.3 119.2,188.9 120.6,188.5 122.1,188.1 123.5,187.7 125.0,187.3 126.5,186.9 127.9,186.5 129.4,186.1 130.8,185.7 132.3,185.3 133.8,184.9 135.2,184.5 136.7,184.1 138.1,183.6 139.6,183.2 141.0,182.8 142.5,182.3 144.0,181.9 145.4,181.5 146.9,181.0 148.3,180.6 149.8,180.1 151.2,179.7 152.7,179.2 154.2,178.8 155.6,178.3 157.1,177.8 158.5,177.3 160.0,176.9 161.5,176.4 162.9,175.9 164.4,175.4 165.8,174.9 167.3,174.4 168.8,174.0 170.2,173.4 171.7,172.9 173.1,172.4 174.6,171.9 176.0,171.4 177.5,170.9 179.0,170.4 180.4,169.8 181.9,169.3 183.3,168.8 184.8,168.2 186.2,167.7 187.7,167.1 189.2,166.6 190.6,166.0 192.1,165.5 193.5,164.9 195.0,164.3 196.5,163.8 197.9,163.2 199.4,162.6 200.8,162.0 202.3,161.4 203.8,160.8 205.2,160.2 206.7,159.6 208.1,159.0 209.6,158.4 211.0,157.8 212.5,157.2 214.0,156.5 215.4,155.9 216.9,155.3 218.3,154.6 219.8,154.0 221.2,153.3 222.7,152.7 224.2,152.0 225.6,151.4 227.1,150.7 228.5,150.0 230.0,149.3 231.5,148.6 232.9,147.9 234.4,147.2 235.8,146.5 237.3,145.8 238.8,145.1 240.2,144.4 241.7,143.7 243.1,143.0 244.6,142.2 246.0,141.5 247.5,140.7 249.0,140.0 250.4,139.2 251.9,138.5 253.3,137.7 254.8,136.9 256.2,136.1 257.7,135.3 259.2,134.6 260.6,133.8 262.1,132.9 263.5,132.1 265.0,131.3 266.5,130.5 267.9,129.7 269.4,128.8 270.8,128.0 272.3,127.1 273.8,126.3 275.2,125.4 276.7,124.6 278.1,123.7 279.6,122.8 281.0,121.9 282.5,121.0 284.0,120.1 285.4,119.2 286.9,118.3 288.3,117.4 289.8,116.4 291.2,115.5 292.7,114.6 294.2,113.6 295.6,112.7 297.1,111.7 298.5,110.7 300.0,109.7 301.5,108.8 302.9,107.8 304.4,106.8 305.8,105.8 307.3,104.7 308.8,103.7 310.2,102.7 311.7,101.6 313.1,100.6 314.6,99.5 316.0,98.5 317.5,97.4 319.0,96.3 320.4,95.2 321.9,94.1 323.3,93.0 324.8,91.9 326.2,90.8 327.7,89.7 329.2,88.5 330.6,87.4 332.1,86.2 333.5,85.1 335.0,83.9 336.5,82.7 337.9,81.5 339.4,80.3 340.8,79.1 342.3,77.9 343.8,76.7 345.2,75.4 346.7,74.2 348.1,72.9 349.6,71.7 351.0,70.4 352.5,69.1 354.0,67.8 355.4,66.5 356.9,65.2 358.3,63.9 359.8,62.5 361.2,61.2 362.7,59.8 364.2,58.5 365.6,57.1 367.1,55.7 368.5,54.3 370.0,52.9 371.5,51.5 372.9,50.0 374.4,48.6 375.8,47.2 377.3,45.7 378.8,44.2 380.2,42.7 381.7,41.3 383.1,39.7 384.6,38.2 386.0,36.7 387.5,35.2 389.0,33.6 390.4,32.0 391.9,30.5 393.3,28.9 394.8,27.3 396.2,25.7 397.7,24.1 399.2,22.4 400.6,20.8 402.1,19.1 403.5,17.4 405.0,15.8"/><circle class="dot2" cx="165.5" cy="175.0" r="4.5"/><circle class="dot3" cx="189.0" cy="166.7" r="4.5"/><circle class="dot2" cx="368.2" cy="54.7" r="4.5"/><text class="ink" x="173.5" y="187.0" font-size="11" text-anchor="start">6. ay ≈ 3543</text><text class="ink" x="181.0" y="158.7" font-size="11" text-anchor="end">iki katı: ≈ 7,3 ay</text><text class="ink" x="358.2" y="50.7" font-size="11" text-anchor="end">10 000'i geçtiği ay: 17</text><text class="dim" x="405.0" y="234.0" font-size="10" text-anchor="end">ay</text><text class="dim" x="61.0" y="30.0" font-size="10" text-anchor="start">kullanıcı</text></svg>
  <figcaption>Aylık yüzde 10 büyüme. Sayı 7,3 ayda iki katına çıkıyor ve 17. ayda 10 000'i geçiyor; eğri her ay bir öncekinden daha hızlı yükseliyor.</figcaption>
</figure>

### 3. Reklam ve yeni kullanıcı: doğru

İki ayın verisi: $1000$ TL reklamla $150$, $3000$ TL reklamla $350$ yeni
kullanıcı. Aralarında doğrusal bir ilişki varsayalım. Eğim:

$$
m = \frac{350 - 150}{3000 - 1000} = \frac{200}{2000} = 0{,}1
$$

Her $10$ TL bir kullanıcı getiriyor. $150 = 0{,}1 \cdot 1000 + b$, yani
$b = 50$: $y = 0{,}1x + 50$. $5000$ TL için tahmin $550$. Gerçekte $520$
gelirse hata $520 - 550 = -30$, karesi $900$.

### 4. Kullanım süresi: istatistik

Beş kullanıcının günlük kullanım süresi (dakika): $12, 15, 18, 20, 35$.
Ortalama $20$, ortanca $18$. Sapmalar $-8, -5, -2, 0, 15$; kareleri
toplamı $318$; varyans $63{,}6$, standart sapma $\approx 7{,}97$. $35$
dakikanın z puanı $\frac{15}{7{,}97} \approx 1{,}88$: ortalamanın neredeyse
iki standart sapma üstünde, göze çarpan ama inanılmaz olmayan bir
kullanıcı.

### 5. Premium üyeler: olasılık

Kullanıcıların yüzde $30$'u premium. Rastgele ve birbirinden bağımsız $3$
kullanıcıdan en az birinin premium olma olasılığı tümleyenle:
$1 - 0{,}7^3 = 1 - 0{,}343 = 0{,}657$.

Beş adımda üstel fonksiyon, logaritma, doğru denklemi, Σ ile yazılmış
istatistikler ve olasılık kuralları birlikte çalıştı. Bir makine öğrenmesi
projesinin ilk günü tam olarak böyle görünür.

## Bölüm bölüm ne öğrendin?

| Konu | Anahtar fikir | Makine öğrenmesinde |
|---|---|---|
| Sayılar, işlem önceliği | Önce parantez, sonra üs, sonra çarpma ve bölme | her formül |
| Kesir, ondalık, yüzde | Oran bir bölme; yüzdeler çarpılarak birikir | doğruluk, olasılık |
| Üs ve kök | $a^m a^n = a^{m+n}$, $a^{-n} = \frac{1}{a^n}$ | öğrenme oranı, ölçekler |
| Cebir ve çarpanlar | Özdeşlikler, iki tarafa aynı işlem | model denklemleri |
| Denklemler ve eşitsizlikler | Bilinmeyeni yalnız bırak; negatifle çarpınca yön döner | kısıtlar |
| Denklem sistemleri | İki bilinmeyen, iki denklem | ağırlıkları çözmek |
| İkinci derece | $\Delta$, kökler, parabol | kayıp eğrileri |
| Kümeler ve mantık | Birleşim, kesişim, "ve", "veya" | filtreler, olaylar |
| Fonksiyonlar | Girdi → çıktı, bileşke, ters | model = fonksiyon |
| Koordinat ve doğru | Eğim, $y = mx + b$, uzaklık | doğrusal regresyon |
| Polinomlar | Derece, kökler, bölme | polinom regresyonu |
| Üstel ve logaritma | Oran sabit; logaritma üssü bulur | sigmoid, log-kayıp |
| Diziler ve Σ | Aritmetik, geometrik, toplam formülleri | her ortalama ve kayıp |
| Geometri | Pisagor, alan, benzerlik | uzaklık, IoU |
| Trigonometri | sin, cos, radyan, birim çember | kosinüs benzerliği |
| Sayma | Çarpma ilkesi, $P$, $\binom{n}{k}$ | arama uzayı |
| Olasılık | Tümleyen, birleşim, bağımsızlık, koşullu | sınıf olasılıkları |
| İstatistik | Ortalama, ortanca, standart sapma, z | ölçekleme, aykırı değer |

## En sık düşülen tuzaklar

MAT 1 boyunca defalarca karşına çıkan hatalar, tek listede:

| Tuzak | Doğrusu |
|---|---|
| $-3^2 = 9$ | $-3^2 = -9$; $(-3)^2 = 9$ |
| $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$ | ortak payda: $\frac{5}{6}$ |
| $(a + b)^2 = a^2 + b^2$ | $a^2 + 2ab + b^2$ |
| $\sqrt{a + b} = \sqrt{a} + \sqrt{b}$ | kök toplama dağılmaz |
| $\log(a + b) = \log a + \log b$ | $\log(ab) = \log a + \log b$ |
| eşitsizliği negatifle çarpıp yönü korumak | yön döner |
| üç kez yüzde $10$ = yüzde $30$ | $1{,}1^3 = 1{,}331$ |
| $a_n = a_1 + nd$ | $a_1 + (n - 1)d$ |
| hesap makinesi radyandayken $\sin 30$ | açının birimine bak |
| sıra önemsizken permütasyon | $\binom{n}{k}$ |
| $P(A \cup B) = P(A) + P(B)$ | ortak kısmı çıkar |
| çarpık veride ortalamayı "tipik" saymak | ortancaya bak |

## Bir sonraki adım

MAT 2 — Yapay Zekanın Matematiği üç kolla devam ediyor:

- **Doğrusal cebir:** vektörler ve matrisler. Koordinat düzlemi ve
  trigonometri buraya taşınıyor; bir veri satırı bir vektör, bir veri
  seti bir matris.
- **Kalkülüs:** limit, türev, integral ve gradyan. Fonksiyonlar, polinomlar,
  üstel ve logaritma burada "değişim hızı" sorusuyla yeniden ele alınıyor;
  modellerin nasıl öğrendiği (gradyan inişi) buradan çıkıyor.
- **Olasılık ve istatistik:** koşullu olasılık, Bayes, dağılımlar,
  regresyonun ve entropinin matematiği. Bu bölümdeki olasılık ve
  istatistik temelinin üstüne kuruluyor.

## Özet

- MAT 1'in dört kolu: hesap (sayılardan fonksiyonlara), şekil (koordinattan
  trigonometriye), belirsizlik (kümelerden istatistiğe) ve hepsini bağlayan
  Σ gösterimi.
- Gerçek bir problemde bu kollar birlikte çalışıyor: büyüme üstel,
  "ne zaman" logaritma, ilişki doğru, özet istatistik, risk olasılık.
- En sık hatalar dağılmayan işlemlerden (kare, kök, logaritma), işaret ve
  yönden, yüzdelerin toplanmasından ve birimlerden geliyor.
- Sırada MAT 2: doğrusal cebir, kalkülüs ve olasılık–istatistik.
