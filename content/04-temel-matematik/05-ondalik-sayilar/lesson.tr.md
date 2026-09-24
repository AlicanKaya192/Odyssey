# Ondalık Sayılar ve Yuvarlama

Kesirler bir bütünün parçasını anlatıyordu. **Ondalık sayılar** aynı işi
basamak değeriyle yapıyor: $\dfrac{3}{4}$ yerine $0{,}75$ yazıyoruz. Ölçümler,
paralar, olasılıklar ve bir bilgisayarın hesapladığı neredeyse her sayı
ondalık. Bu bölümde ondalık sayıları kesirlerle ilişkilendirecek, dört
işlemi yapacak ve **yuvarlamayı** doğru öğreneceğiz.

Ön bilgi: Kesirler bölümü.

## Virgülden sonraki basamaklar

Doğal sayılarda her basamak sağındakinin $10$ katıydı. Virgülden sonra
bu örüntü devam ediyor: her basamak solundakinin **onda biri**.

<figure class="fig">
<svg viewBox="0 0 400 156" width="400"><rect class="box" x="40" y="44" width="70" height="50"/><text class="ink" x="75.0" y="78" font-size="24" text-anchor="middle">3</text><text class="dim" x="75.0" y="36" font-size="11" text-anchor="middle">birler</text><text class="ink" x="121" y="82" font-size="28" text-anchor="middle">,</text><rect class="box" x="132" y="44" width="70" height="50"/><text class="ink" x="167.0" y="78" font-size="24" text-anchor="middle">7</text><text class="dim" x="167.0" y="22" font-size="11" text-anchor="middle">onda</text><text class="dim" x="167.0" y="36" font-size="11" text-anchor="middle">birler</text><rect class="box" x="202" y="44" width="70" height="50"/><text class="ink" x="237.0" y="78" font-size="24" text-anchor="middle">5</text><text class="dim" x="237.0" y="22" font-size="11" text-anchor="middle">yüzde</text><text class="dim" x="237.0" y="36" font-size="11" text-anchor="middle">birler</text><rect class="box" x="272" y="44" width="70" height="50"/><text class="ink" x="307.0" y="78" font-size="24" text-anchor="middle">2</text><text class="dim" x="307.0" y="22" font-size="11" text-anchor="middle">binde</text><text class="dim" x="307.0" y="36" font-size="11" text-anchor="middle">birler</text><rect class="curve" x="129" y="41" width="216" height="56" rx="4"/><text class="dim" x="237.0" y="120" font-size="11" text-anchor="middle">×1/10 · ×1/100 · ×1/1000</text><text class="ink" x="191" y="144" font-size="13" text-anchor="middle">3,752 = 3 + 7/10 + 5/100 + 2/1000</text></svg>
  <figcaption>$3{,}752$'de $3$ birler, $7$ onda birler, $5$ yüzde birler, $2$ binde birler basamağında. Virgülün sağındaki her basamak, bir öncekinin onda biri değerinde.</figcaption>
</figure>

$$
3{,}752 = 3 + \frac{7}{10} + \frac{5}{100} + \frac{2}{1\,000}
$$

**Virgül mü nokta mı?** Türkçede ondalık ayıracı virgül: $3{,}75$.
İngilizcede ve **bütün programlama dillerinde** nokta: `3.75`. Python'a
`3,75` yazarsan iki ayrı sayı ($3$ ve $75$) anlar. Bu derste Türkçe
metinde virgül kullanıyoruz; cevap kutularına ikisini de yazabilirsin.

**Sağdaki sıfırlar değeri değiştirmez:** $0{,}5 = 0{,}50 = 0{,}500$. Çünkü
$\dfrac{5}{10} = \dfrac{50}{100}$.

## Ondalık ve kesir arasında çeviri

**Ondalıktan kesre:** Virgülden sonraki basamak sayısı kadar sıfırlı bir
payda yaz, sonra sadeleştir.

$$
0{,}36 = \frac{36}{100} = \frac{9}{25}, \qquad 2{,}125 = \frac{2\,125}{1\,000} = \frac{17}{8}
$$

**Kesirden ondalığa:** Payı paydaya böl. $\dfrac{7}{8}$ için:

$$
7 \div 8 = 0{,}875
$$

Uzun bölmede $7$'nin yanına sıfırlar ekleyerek devam ederiz: $70 \div 8 =
8$ kalan $6$; $60 \div 8 = 7$ kalan $4$; $40 \div 8 = 5$ kalan $0$.

Paydası $10$'un bir çarpanına kolayca genişletilebiliyorsa bölmeye gerek
yok: $\dfrac{3}{25} = \dfrac{12}{100} = 0{,}12$.

### Biten ve devreden ondalıklar

$\dfrac{1}{3} = 0{,}333\dots$ hiç bitmiyor: $1$'i $3$'e bölerken kalan hep
$1$. Böyle sayılara **devirli ondalık** denir ve devreden kısım üstüne
çizgi çekilerek yazılır: $0{,}\overline{3}$.

Bir kesrin ondalık yazılışı ne zaman biter? En sade hâlinde **paydanın
asal çarpanları yalnızca $2$ ve $5$ ise**, çünkü $10 = 2 \cdot 5$ ve payda
$10$'un bir kuvvetine genişletilebilir. $\dfrac{7}{8}$ biter ($8 = 2^3$),
$\dfrac{1}{3}$, $\dfrac{5}{6}$ ve $\dfrac{2}{7}$ bitmez.

**Devirli ondalığı kesre çevirmek:** $x = 0{,}\overline{4} = 0{,}444\dots$
olsun. $10$ ile çarpınca devreden kısım aynı kalır:

$$
\begin{aligned}
10x &= 4{,}444\dots \\
x &= 0{,}444\dots
\end{aligned}
$$

Alt alta çıkarınca sonsuz kuyruklar birbirini götürür: $9x = 4$, yani $x =
\dfrac{4}{9}$. Sonuç ilginç: $0{,}\overline{9} = \dfrac{9}{9} = 1$.

## Karşılaştırma

Virgülden sonraki basamak sayılarını sağa sıfır ekleyerek eşitle, sonra
tam sayı gibi karşılaştır:

$$
0{,}5 \;\;?\;\; 0{,}45 \quad\Rightarrow\quad 0{,}50 > 0{,}45
$$

**Uzun olan büyük değildir.** $0{,}45$'te daha çok basamak var ama
$0{,}5$ daha büyük: beş onda bir, dört onda birden fazla.

## Dört işlem

**Toplama ve çıkarma:** Virgülleri alt alta hizala; eksik basamaklara
sıfır koy.

$$
12{,}45 + 8{,}9 = 12{,}45 + 8{,}90 = 21{,}35
$$

**Çarpma:** Virgülleri yok sayıp tam sayı gibi çarp; sonuçta virgülden
sonraki basamak sayısı, çarpanlardakilerin **toplamı** kadar olsun.

$$
3{,}75 \cdot 0{,}4: \quad 375 \cdot 4 = 1\,500, \quad 2 + 1 = 3 \text{ basamak} \quad\Rightarrow\quad 1{,}500 = 1{,}5
$$

Neden? $3{,}75 = \dfrac{375}{100}$ ve $0{,}4 = \dfrac{4}{10}$; çarpımın
paydası $1\,000$.

**Bölme:** Böleni tam sayı yapacak kadar **iki sayının da** virgülünü aynı
miktarda sağa kaydır. Bu, bölüneni ve böleni aynı sayıyla ($10$, $100$, …)
çarpmak demek; bölüm değişmez.

$$
1{,}2 \div 0{,}05 = 120 \div 5 = 24
$$

**$10$, $100$, $1\,000$ ile çarpmak ve bölmek:** Virgülü sıfır sayısı
kadar kaydırmak yeter. $3{,}752 \cdot 100 = 375{,}2$ ve $3{,}752 \div 100
= 0{,}03752$.

## Yuvarlama

Bir sayıyı belirli bir basamağa yuvarlamak, o basamaktaki **en yakın**
sayıyı seçmek demek.

<figure class="fig">
<svg viewBox="0 0 420 206" width="420"><line class="line" x1="32" y1="70" x2="388" y2="70"/><line class="line" x1="40" y1="60" x2="40" y2="80"/><line class="line" x1="74" y1="65" x2="74" y2="75"/><line class="line" x1="108" y1="65" x2="108" y2="75"/><line class="line" x1="142" y1="65" x2="142" y2="75"/><line class="line" x1="176" y1="65" x2="176" y2="75"/><line class="line" x1="210" y1="65" x2="210" y2="75"/><line class="line" x1="244" y1="65" x2="244" y2="75"/><line class="line" x1="278" y1="65" x2="278" y2="75"/><line class="line" x1="312" y1="65" x2="312" y2="75"/><line class="line" x1="346" y1="65" x2="346" y2="75"/><line class="line" x1="380" y1="60" x2="380" y2="80"/><text class="ink" x="40" y="98" font-size="13" text-anchor="middle">2,71</text><text class="ink" x="380" y="98" font-size="13" text-anchor="middle">2,72</text><line class="curve3" stroke-dasharray="4 3" x1="210" y1="40" x2="210" y2="82"/><text class="dim" x="210" y="98" font-size="11" text-anchor="middle">2,715</text><text class="dim" x="210" y="34" font-size="11" text-anchor="middle">orta nokta</text><circle class="dot" cx="312" cy="70" r="6"/><text class="ink" x="312" y="54" font-size="13" text-anchor="middle">2,718</text><line class="curve2" x1="312" y1="116" x2="374" y2="116"/><polygon class="dot2" points="380,116 371,111 371,121"/><text class="ink" x="346" y="134" font-size="11" text-anchor="middle">0,002</text><line class="curve3" x1="312" y1="150" x2="46" y2="150"/><polygon class="dim" points="40,150 49,145 49,155"/><text class="dim" x="176" y="168" font-size="11" text-anchor="middle">0,008</text><text class="ink" x="210" y="194" font-size="13" text-anchor="middle">2,718, 2,72'ye daha yakın</text></svg>
  <figcaption>$2{,}718$, $2{,}71$ ile $2{,}72$ arasında. $2{,}72$'ye $0{,}002$, $2{,}71$'e $0{,}008$ uzaklıkta; iki basamağa yuvarlanınca $2{,}72$ olur. Orta noktayı ($2{,}715$) geçen her sayı yukarı yuvarlanır.</figcaption>
</figure>

**Kural:** Yuvarlanacak basamağın hemen sağındaki rakama bak. $5$ ya da
büyükse yukarı, küçükse aşağı yuvarla; sağdaki rakamları at.

| Sayı | Bir basamak | İki basamak | Üç basamak |
|---|---|---|---|
| $2{,}718\,28$ | $2{,}7$ | $2{,}72$ | $2{,}718$ |
| $0{,}654\,9$ | $0{,}7$ | $0{,}65$ | $0{,}655$ |
| $9{,}996$ | $10{,}0$ | $10{,}00$ | $9{,}996$ |

Son satırdaki gibi yuvarlama bir sonraki basamağa taşabilir: $9{,}996$'yı
iki basamağa yuvarlarken $9{,}99 + 0{,}01 = 10{,}00$.

**Yuvarlamayı en sona bırak.** Ara adımlarda yuvarlarsan hatalar birikir.
$2{,}449$'u bir basamağa yuvarlarken önce $2{,}45$'e, sonra $2{,}5$'e
gitmek yanlış; doğrudan bakınca onda birlerden sonraki rakam $4$: $2{,}4$.

**Atmak ile yuvarlamak farklı.** $2{,}718$'i iki basamağa **kesmek**
(fazlasını atmak) $2{,}71$ verir; yuvarlamak $2{,}72$.

## Makine öğrenmesinde ondalıklar

**Bilgisayar her ondalığı tam tutamaz.** Python'da `0.1 + 0.2` yazınca
`0.30000000000000004` çıkar. Bilgisayar sayıları ikilik sistemde tutuyor
ve $0{,}1$ ikilik sistemde, $\dfrac{1}{3}$'ün onluk sistemdeki gibi,
devirli: sonsuz basamak gerekir, bir yerde kesilir. Bu yüzden ondalık
sayıları `==` ile karşılaştırmak yerine "yeterince yakın mı?" diye
bakılır.

**Metrikleri raporlamak.** Doğruluk $0{,}873\,46$ çıktıysa genelde $0{,}873$
ya da $\%87{,}3$ diye yuvarlanarak yazılır. Ama hesap sürerken tam değer
kullanılır; yuvarlama yalnızca göstermek için.

**Küçük sayılar.** Öğrenme hızı gibi değerler $0{,}001$ ya da $0{,}000\,1$
olabilir; virgülden sonraki sıfırları saymak önemli, çünkü her sıfır
değeri on kat değiştiriyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$0{,}45 > 0{,}5$</p>
      <p>$0{,}3 \cdot 0{,}2 = 0{,}6$</p>
      <p>$1{,}2 \div 0{,}05 = 0{,}24$</p>
      <p>$2{,}449 \to 2{,}45 \to 2{,}5$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$0{,}50 > 0{,}45$</p>
      <p>$0{,}3 \cdot 0{,}2 = 0{,}06$</p>
      <p>$1{,}2 \div 0{,}05 = 120 \div 5 = 24$</p>
      <p>$2{,}449 \to 2{,}4$</p>
    </div>
  </div>
  <figcaption>Basamak sayısına dikkat: çarpımda basamaklar toplanır, bölmede iki sayının da virgülü kaydırılır.</figcaption>
</figure>

- **Basamak çok diye büyük sanmak.** Basamakları sıfırla eşitleyip
  karşılaştır.
- **Çarpımda virgülü yanlış koymak.** $0{,}3 \cdot 0{,}2$: $3 \cdot 2 = 6$
  ve toplam $2$ basamak, $0{,}06$. Kontrol: iki sayı da $1$'den küçük,
  çarpım ikisinden de küçük olmalı.
- **Zincirleme yuvarlamak.** Yuvarlama tek seferde, istenen basamağa
  bakarak yapılır.

## Özet

- Virgülden sonraki basamaklar: onda birler, yüzde birler, binde birler; her biri solundakinin onda biri.
- Türkçede virgül, programlamada nokta: $3{,}75$ ile `3.75` aynı sayı.
- Ondalık → kesir: $10$'un kuvveti paydaya yaz, sadeleştir. Kesir → ondalık: payı paydaya böl.
- Payda (en sade hâlde) yalnızca $2$ ve $5$ içeriyorsa ondalık biter; yoksa devreder.
- $0{,}\overline{4} = \dfrac{4}{9}$: $10x - x$ ile devreden kısmı götür.
- Karşılaştırmada basamakları eşitle; uzun olan büyük değildir.
- Çarpma: basamak sayıları toplanır. Bölme: iki sayının da virgülünü aynı miktar kaydır.
- Yuvarlama: sağdaki rakam $5$ ya da büyükse yukarı; en sonda ve tek seferde yuvarla.
