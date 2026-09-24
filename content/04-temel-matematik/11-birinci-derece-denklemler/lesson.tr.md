# Birinci Dereceden Denklemler

Bir **ifade** ($3x + 4$) bir değer anlatır; bir **denklem** ($3x + 4 =
19$) bir soru sorar: $x$ hangi sayı olursa iki taraf eşit olur? Birinci
dereceden denklemlerde bilinmeyen en fazla birinci kuvvetle geçer ($x$
var, $x^2$ yok). Bunlar matematiğin en sık çözülen denklemleri: bir
formülden bilinmeyeni çekmek, iki fiyat planının ne zaman eşitlendiğini
bulmak ya da bir modelin karar sınırını hesaplamak hep bu işe varıyor.

Ön bilgi: Cebirsel İfadeler ve Özdeşlikler, Kesirler.

## Denklem bir terazidir

<figure class="fig">
<svg viewBox="0 0 480 278" width="480"><polygon class="dot" opacity="0.5" points="240,190 222,220 258,220"/><line class="line" x1="240" y1="40" x2="240" y2="190" style="stroke-width:3"/><line class="line" x1="110" y1="40" x2="370" y2="40" style="stroke-width:4"/><line class="curve3" x1="110" y1="40" x2="35.0" y2="150"/><line class="curve3" x1="110" y1="40" x2="185.0" y2="150"/><line class="line" x1="29.0" y1="150" x2="191.0" y2="150" style="stroke-width:3"/><line class="curve3" x1="370" y1="40" x2="295.0" y2="150"/><line class="curve3" x1="370" y1="40" x2="445.0" y2="150"/><line class="line" x1="289.0" y1="150" x2="451.0" y2="150" style="stroke-width:3"/><rect class="dot" opacity="0.55" x="52" y="120" width="26" height="28" rx="3"/><text class="ink" x="65" y="139" font-size="13" text-anchor="middle">x</text><rect class="dot" opacity="0.55" x="82" y="120" width="26" height="28" rx="3"/><text class="ink" x="95" y="139" font-size="13" text-anchor="middle">x</text><rect class="dot" opacity="0.55" x="112" y="120" width="26" height="28" rx="3"/><text class="ink" x="125" y="139" font-size="13" text-anchor="middle">x</text><circle class="dot3" opacity="0.8" cx="146" cy="128" r="6"/><circle class="dot3" opacity="0.8" cx="160" cy="128" r="6"/><circle class="dot3" opacity="0.8" cx="146" cy="142" r="6"/><circle class="dot3" opacity="0.8" cx="160" cy="142" r="6"/><circle class="dot3" opacity="0.8" cx="322" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="337" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="352" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="367" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="382" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="397" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="412" cy="144" r="6"/><circle class="dot3" opacity="0.8" cx="322" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="337" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="352" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="367" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="382" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="397" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="412" cy="130" r="6"/><circle class="dot3" opacity="0.8" cx="322" cy="116" r="6"/><circle class="dot3" opacity="0.8" cx="337" cy="116" r="6"/><circle class="dot3" opacity="0.8" cx="352" cy="116" r="6"/><circle class="dot3" opacity="0.8" cx="367" cy="116" r="6"/><circle class="dot3" opacity="0.8" cx="382" cy="116" r="6"/><text class="dim" x="110" y="172" font-size="11" text-anchor="middle">3 kutu + 4 birim</text><text class="dim" x="370" y="172" font-size="11" text-anchor="middle">19 birim</text><text class="ink" x="240" y="248" font-size="13" text-anchor="middle">iki kefe dengede: 3x + 4 = 19</text><text class="dim" x="240" y="266" font-size="11" text-anchor="middle">her kutuda x birim var</text></svg>
  <figcaption>Sol kefede üç kutu ve dört birim, sağda on dokuz birim; terazi dengede. Her iki kefeden aynı şeyi alırsak ya da her ikisini aynı sayıya bölersek denge bozulmaz. Önce iki taraftan $4$ birim al: $3x = 15$. Sonra ikisini de $3$'e böl: $x = 5$.</figcaption>
</figure>

**Temel kural:** Denklemin iki tarafına **aynı işlemi** uygularsan eşitlik
korunur. Ekleme, çıkarma, sıfırdan farklı bir sayıyla çarpma ya da bölme.

$$
\begin{aligned}
3x + 4 &= 19 \\
3x &= 15 &&\text{(iki taraftan } 4 \text{ çıkar)} \\
x &= 5 &&\text{(iki tarafı } 3\text{'e böl)}
\end{aligned}
$$

**Sağlama:** $3 \cdot 5 + 4 = 19$ ✓. Her çözümün sonunda bulduğun sayıyı
**asıl** denkleme koy.

"Karşıya atınca işaret değişir" kısayolu da bu kuraldan geliyor: $3x + 4 =
19$'da $4$'ü "karşıya atmak", iki taraftan $4$ çıkarmak demek.

## Genel yol

1. Parantezleri aç, her tarafı ayrı ayrı sadeleştir.
2. Kesir varsa iki tarafı paydaların EKOK'uyla çarp.
3. Bilinmeyenli terimleri bir tarafa, sayıları öbür tarafa topla.
4. Bilinmeyenin katsayısına böl.
5. Asıl denkleme koyarak sağla.

**Bilinmeyen iki tarafta:**

$$
\begin{aligned}
5x - 7 &= 2x + 8 \\
3x - 7 &= 8 &&\text{(iki taraftan } 2x \text{ çıkar)} \\
3x &= 15 \\
x &= 5
\end{aligned}
$$

**Parantezli:**

$$
\begin{aligned}
2(x - 3) &= 4 - (x + 1) \\
2x - 6 &= 3 - x \\
3x &= 9 \\
x &= 3
\end{aligned}
$$

Sağdaki eksi **iki** terimin işaretini değiştirdi: $-(x + 1) = -x - 1$.

**Kesirli:** Paydaların EKOK'uyla çarpınca kesirler kaybolur. **Her** terim
çarpılmalı.

$$
\begin{aligned}
\frac{x}{3} + \frac{x}{4} &= 7 \\
4x + 3x &= 84 &&\text{(iki tarafı } 12 \text{ ile çarp)} \\
7x &= 84 \\
x &= 12
\end{aligned}
$$

## Çözümü olmayan ve sonsuz çözümlü denklemler

Bilinmeyen sadeleşip kaybolursa iki durum var:

| Denklem | Sadeleşince | Anlamı |
|---|---|---|
| $2x + 1 = 2x + 5$ | $1 = 5$ | hiçbir $x$ sağlamaz: **çözüm yok** |
| $2(x + 1) = 2x + 2$ | $2 = 2$ | her $x$ sağlar: bu bir **özdeşlik** |

## Grafikte bir denklem

<figure class="fig">
<svg viewBox="0 0 450 274" width="450"><line class="grid" x1="50.0" y1="230.0" x2="50.0" y2="30.0"/><text class="dim" x="50.0" y="245" font-size="10" text-anchor="middle">0</text><line class="grid" x1="92.9" y1="230.0" x2="92.9" y2="30.0"/><text class="dim" x="92.9" y="245" font-size="10" text-anchor="middle">1</text><line class="grid" x1="135.7" y1="230.0" x2="135.7" y2="30.0"/><text class="dim" x="135.7" y="245" font-size="10" text-anchor="middle">2</text><line class="grid" x1="178.6" y1="230.0" x2="178.6" y2="30.0"/><text class="dim" x="178.6" y="245" font-size="10" text-anchor="middle">3</text><line class="grid" x1="221.4" y1="230.0" x2="221.4" y2="30.0"/><text class="dim" x="221.4" y="245" font-size="10" text-anchor="middle">4</text><line class="grid" x1="264.3" y1="230.0" x2="264.3" y2="30.0"/><text class="dim" x="264.3" y="245" font-size="10" text-anchor="middle">5</text><line class="grid" x1="307.1" y1="230.0" x2="307.1" y2="30.0"/><text class="dim" x="307.1" y="245" font-size="10" text-anchor="middle">6</text><line class="grid" x1="350.0" y1="230.0" x2="350.0" y2="30.0"/><text class="dim" x="350.0" y="245" font-size="10" text-anchor="middle">7</text><line class="grid" x1="50.0" y1="230.0" x2="350.0" y2="230.0"/><text class="dim" x="44" y="233.0" font-size="10" text-anchor="end">0</text><line class="grid" x1="50.0" y1="201.4" x2="350.0" y2="201.4"/><text class="dim" x="44" y="204.4" font-size="10" text-anchor="end">4</text><line class="grid" x1="50.0" y1="172.9" x2="350.0" y2="172.9"/><text class="dim" x="44" y="175.9" font-size="10" text-anchor="end">8</text><line class="grid" x1="50.0" y1="144.3" x2="350.0" y2="144.3"/><text class="dim" x="44" y="147.3" font-size="10" text-anchor="end">12</text><line class="grid" x1="50.0" y1="115.7" x2="350.0" y2="115.7"/><text class="dim" x="44" y="118.7" font-size="10" text-anchor="end">16</text><line class="grid" x1="50.0" y1="87.1" x2="350.0" y2="87.1"/><text class="dim" x="44" y="90.1" font-size="10" text-anchor="end">20</text><line class="grid" x1="50.0" y1="58.6" x2="350.0" y2="58.6"/><text class="dim" x="44" y="61.6" font-size="10" text-anchor="end">24</text><line class="grid" x1="50.0" y1="30.0" x2="350.0" y2="30.0"/><text class="dim" x="44" y="33.0" font-size="10" text-anchor="end">28</text><line class="line" x1="50.0" y1="230.0" x2="350.0" y2="230.0"/><line class="line" x1="50.0" y1="230.0" x2="50.0" y2="30.0"/><text class="dim" x="360.0" y="234" font-size="12" text-anchor="start">x</text><text class="dim" x="50" y="22.0" font-size="12" text-anchor="middle">y</text><line class="curve" x1="50.0" y1="201.4" x2="350.0" y2="51.4"/><line class="curve2" x1="50.0" y1="94.3" x2="350.0" y2="94.3"/><line class="curve3" stroke-dasharray="4 3" x1="264.3" y1="94.3" x2="264.3" y2="230.0"/><circle class="dot" cx="264.3" cy="94.3" r="5"/><text class="ink" x="356.0" y="55.4" font-size="12" text-anchor="start">y = 3x + 4</text><text class="ink" x="356.0" y="98.3" font-size="12" text-anchor="start">y = 19</text><text class="ink" x="256.3" y="82.3" font-size="12" text-anchor="end">kesişim: x = 5</text><text class="dim" x="264.3" y="262" font-size="11" text-anchor="middle">denklemin çözümü</text></svg>
  <figcaption>$3x + 4 = 19$ denklemi, $y = 3x + 4$ doğrusunun $y = 19$ yüksekliğine ulaştığı yeri soruyor. İki çizgi $x = 5$'te kesişiyor: denklemin çözümü bu kesişimin $x$'i.</figcaption>
</figure>

Her birinci dereceden denklem, iki doğrunun kesiştiği yeri bulmak demek.
Koordinat Düzlemi bölümünde bu bakış açısına geri döneceğiz.

## Formülden bilinmeyeni çekmek

Aynı kurallar harflerle de işliyor. Hız formülü $v = \dfrac{d}{t}$'den
süreyi çekelim:

$$
v = \frac{d}{t} \quad\Rightarrow\quad vt = d \quad\Rightarrow\quad t = \frac{d}{v}
$$

Sıcaklık: $F = \dfrac{9}{5}C + 32$ ise

$$
F - 32 = \frac{9}{5}C \quad\Rightarrow\quad C = \frac{5}{9}(F - 32)
$$

$F = 212$ için $C = \frac{5}{9} \cdot 180 = 100$ ✓ (suyun kaynama noktası).

## Sözel problemleri denkleme çevirmek

1. Bilinmeyene bir harf ver ve ne olduğunu **yaz**.
2. Cümleleri tek tek matematiğe çevir.
3. Çöz ve sonucun soruya cevap olup olmadığına bak.

**Örnek:** Bir telefon planı ayda $40$ lira artı her GB için $2$ lira;
öbürü $25$ lira artı her GB için $5$ lira. Kaç GB'de iki plan eşit?

$x$ = GB sayısı. $40 + 2x = 25 + 5x \Rightarrow 15 = 3x \Rightarrow x = 5$.
$5$ GB'den az kullanan için ikinci plan, fazla kullanan için birinci plan
ucuz.

## Makine öğrenmesinde doğrusal denklemler

**Karar sınırı.** Bir sınıflandırıcı $0{,}8x - 2$ pozitifse "evet",
negatifse "hayır" diyor. Sınır, ifadenin sıfır olduğu yer:

$$
0{,}8x - 2 = 0 \quad\Rightarrow\quad x = 2{,}5
$$

**Ölçeklemeyi geri almak.** Veriler çoğu zaman $z = \dfrac{x - \mu}{\sigma}$
ile ölçeklenir ($\mu$ ortalama, $\sigma$ yayılım). Modelin çıktısını
gerçek birime çevirmek için $x$'i çekeriz: $x = \mu + z\sigma$.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$3x + 4 = 19 \Rightarrow 3x = 23$</p>
      <p>$2x + 6 = 10 \Rightarrow x + 6 = 5$</p>
      <p>$\dfrac{x}{3} + 1 = 5 \Rightarrow x + 1 = 15$</p>
      <p>$5 - (x - 2) = 1 \Rightarrow 5 - x - 2 = 1$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$3x = 19 - 4 = 15$</p>
      <p>$x + 3 = 5$ (her terim $2$'ye bölünür)</p>
      <p>$x + 3 = 15$ (her terim $3$ ile çarpılır)</p>
      <p>$5 - x + 2 = 1$</p>
    </div>
  </div>
  <figcaption>İki tarafa yapılan işlem, iki taraftaki <b>her terime</b> uygulanır.</figcaption>
</figure>

- **Karşıya atarken işaret değiştirmemek.** Kısayolu unutup kurala dön:
  iki taraftan aynı şeyi çıkar.
- **Bilinmeyenle bölmek.** $x^2 = 3x$'i $x$'e bölmek $x = 0$ çözümünü
  kaybettirir. Birinci dereceden denklemlerde buna gerek yok, ama alışkanlık
  edinme.
- **Sağlamayı atlamak.** Özellikle kesirli denklemlerde hesap hatası
  kolay; bulduğun sayıyı asıl denkleme koy.

## Özet

- Denklem, iki tarafı eşit yapan değeri soran bir soru.
- İki tarafa aynı işlemi uygula: ekle, çıkar, sıfır olmayan sayıyla çarp ya da böl.
- Sıra: parantez aç, kesirleri EKOK'la temizle, terimleri topla, katsayıya böl, sağla.
- Bilinmeyen kaybolursa: $1 = 5$ gibi yanlışsa çözüm yok; $2 = 2$ gibi doğruysa her sayı çözüm.
- Grafikte çözüm, iki doğrunun kesiştiği yerin $x$'i.
- Formüllerde de aynı kurallar: $v = \dfrac{d}{t} \Rightarrow t = \dfrac{d}{v}$.
