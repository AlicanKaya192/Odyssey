# Eşitsizlikler ve Mutlak Değer

Denklem tek bir değeri sorar: "hangi $x$ için eşit?" **Eşitsizlik** ise
bir aralık sorar: "hangi $x$'ler için küçük?" Günlük hayatın çoğu sınırı
böyle: hız sınırı, bütçe, yaş aralığı. Makine öğrenmesinde de eşikler
("olasılık $0{,}5$'ten büyükse evet de"), hata toleransları ("hata en fazla
$0{,}1$") ve kırpmalar hep eşitsizliklerle yazılıyor. Bu bölümde
eşitsizlikleri çözmeyi, çözümleri sayı doğrusunda göstermeyi ve mutlak
değerle "uzaklık" koşullarını yazmayı göreceğiz.

Ön bilgi: Tam Sayılar (mutlak değer), Birinci Dereceden Denklemler.

## Eşitsizlik işaretleri

| İşaret | Okunuşu | Örnek |
|---|---|---|
| $<$ | küçüktür | $2 < 5$ |
| $>$ | büyüktür | $-1 > -4$ |
| $\le$ | küçük ya da eşittir | $x \le 3$: $3$ de dahil |
| $\ge$ | büyük ya da eşittir | $x \ge 0$: negatif olmayanlar |

Bir eşitsizliğin çözümü genellikle tek sayı değil, bir **aralık**: $x > 2$
ifadesini $2$'den büyük **bütün** sayılar sağlar.

<figure class="fig">
<svg viewBox="0 0 500 160" width="500"><text class="ink" x="247.0" y="22" font-size="12" text-anchor="middle">x > 2: 2 dahil değil (boş daire)</text><line class="line" x1="18" y1="44" x2="476" y2="44"/><line class="line" x1="26" y1="39" x2="26" y2="49"/><text class="dim" x="26" y="64" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="39" x2="60" y2="49"/><text class="dim" x="60" y="64" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="39" x2="94" y2="49"/><text class="dim" x="94" y="64" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="39" x2="128" y2="49"/><text class="dim" x="128" y="64" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="39" x2="162" y2="49"/><text class="dim" x="162" y="64" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="39" x2="196" y2="49"/><text class="dim" x="196" y="64" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="39" x2="230" y2="49"/><text class="ink" x="230" y="64" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="39" x2="264" y2="49"/><text class="dim" x="264" y="64" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="39" x2="298" y2="49"/><text class="dim" x="298" y="64" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="39" x2="332" y2="49"/><text class="dim" x="332" y="64" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="39" x2="366" y2="49"/><text class="dim" x="366" y="64" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="39" x2="400" y2="49"/><text class="dim" x="400" y="64" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="39" x2="434" y2="49"/><text class="dim" x="434" y="64" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="39" x2="468" y2="49"/><text class="dim" x="468" y="64" font-size="10" text-anchor="middle">7</text><line class="curve" x1="298" y1="44" x2="474.8" y2="44" style="stroke-width:5"/><polygon class="dot" points="484,44 472,37 472,51"/><circle class="box" cx="298" cy="44" r="6" style="stroke-width:2.5"/><circle class="curve" cx="298" cy="44" r="6" style="stroke-width:2.5"/><text class="ink" x="247.0" y="106" font-size="12" text-anchor="middle">−1 ≤ x < 3: −1 dahil (dolu), 3 değil (boş)</text><line class="line" x1="18" y1="128" x2="476" y2="128"/><line class="line" x1="26" y1="123" x2="26" y2="133"/><text class="dim" x="26" y="148" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="123" x2="60" y2="133"/><text class="dim" x="60" y="148" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="123" x2="94" y2="133"/><text class="dim" x="94" y="148" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="123" x2="128" y2="133"/><text class="dim" x="128" y="148" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="123" x2="162" y2="133"/><text class="dim" x="162" y="148" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="123" x2="196" y2="133"/><text class="dim" x="196" y="148" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="123" x2="230" y2="133"/><text class="ink" x="230" y="148" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="123" x2="264" y2="133"/><text class="dim" x="264" y="148" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="123" x2="298" y2="133"/><text class="dim" x="298" y="148" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="123" x2="332" y2="133"/><text class="dim" x="332" y="148" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="123" x2="366" y2="133"/><text class="dim" x="366" y="148" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="123" x2="400" y2="133"/><text class="dim" x="400" y="148" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="123" x2="434" y2="133"/><text class="dim" x="434" y="148" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="123" x2="468" y2="133"/><text class="dim" x="468" y="148" font-size="10" text-anchor="middle">7</text><line class="curve" x1="196" y1="128" x2="332" y2="128" style="stroke-width:5"/><circle class="dot" cx="196" cy="128" r="6"/><circle class="box" cx="332" cy="128" r="6" style="stroke-width:2.5"/><circle class="curve" cx="332" cy="128" r="6" style="stroke-width:2.5"/></svg>
  <figcaption>Sayı doğrusunda çözüm kümesi: boş daire o sayının dahil olmadığını ($<$, $>$), dolu daire dahil olduğunu ($\le$, $\ge$) gösteriyor. Üstte $2$'den büyük bütün sayılar; altta $-1$ ile $3$ arası, $-1$ dahil, $3$ hariç.</figcaption>
</figure>

**Aralık gösterimi:** Köşeli parantez dahil, normal parantez hariç demek.

| Eşitsizlik | Aralık |
|---|---|
| $x > 2$ | $(2, \infty)$ |
| $x \le 3$ | $(-\infty, 3]$ |
| $-1 \le x < 3$ | $[-1, 3)$ |

Sonsuz hiçbir zaman "dahil" olmaz; yanında hep normal parantez.

## Eşitsizlik çözmek

Denklem kuralları geçerli, **tek bir farkla**: iki tarafı **negatif** bir
sayıyla çarpar ya da bölersen eşitsizliğin yönü **döner**.

Neden? $2 < 5$ doğru. İki tarafı $-1$ ile çarp: $-2$ ve $-5$. Ama $-2 >
-5$; sayı doğrusunda negatife geçince sıra tersine dönüyor.

$$
\begin{aligned}
-3x + 5 &\ge 14 \\
-3x &\ge 9 &&\text{(iki taraftan } 5 \text{ çıkar)} \\
x &\le -3 &&\text{(} -3\text{'e böl, yön döner)}
\end{aligned}
$$

**Sağlama:** Sınırdaki ve içerideki bir değeri dene. $x = -3$: $9 + 5 = 14
\ge 14$ ✓. $x = -4$: $12 + 5 = 17 \ge 14$ ✓. Dışarıdan $x = 0$: $5 \ge 14$
değil ✓.

**Yönü değiştirmeden çözmek de mümkün:** bilinmeyeni katsayısı pozitif
kalacak tarafa topla. $-3x + 5 \ge 14 \Rightarrow 5 - 14 \ge 3x \Rightarrow
-9 \ge 3x \Rightarrow -3 \ge x$. Aynı sonuç.

### Çift eşitsizlik

$-1 \le 2x + 3 < 9$ gibi bir eşitsizlikte üç parçaya da aynı işlem yapılır:

$$
\begin{aligned}
-1 &\le 2x + 3 < 9 \\
-4 &\le 2x < 6 &&\text{(üç parçadan } 3 \text{ çıkar)} \\
-2 &\le x < 3 &&\text{(üç parçayı } 2\text{'ye böl)}
\end{aligned}
$$

## Mutlak değer: uzaklık

Tam Sayılar bölümünden: $|a|$, $a$'nın sıfıra uzaklığı; $|a - b|$, $a$ ile
$b$ arasındaki uzaklık. Mutlak değerli denklem ve eşitsizlikleri çözmenin
anahtarı bu "uzaklık" okuması.

**Mutlak değerli denklem.** $|x| = 3$: sıfıra uzaklığı $3$ olan sayılar,
$x = 3$ ya da $x = -3$. Genel olarak

$$
|A| = r \quad (r \ge 0) \quad\Longleftrightarrow\quad A = r \text{ ya da } A = -r
$$

$|x - 2| = 5$: $x - 2 = 5$ ya da $x - 2 = -5$, yani $x = 7$ ya da $x = -3$.
Sayı doğrusunda $2$'den $5$ birim sağ ve sol.

$r$ negatifse ($|x| = -1$ gibi) çözüm yok: uzaklık negatif olamaz.

## Mutlak değerli eşitsizlikler

<figure class="fig">
<svg viewBox="0 0 500 152" width="500"><text class="ink" x="247.0" y="20" font-size="12" text-anchor="middle">|x − 2| ≤ 3: 2'ye uzaklığı en fazla 3 olan sayılar</text><line class="line" x1="18" y1="86" x2="476" y2="86"/><line class="line" x1="26" y1="81" x2="26" y2="91"/><text class="dim" x="26" y="106" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="81" x2="60" y2="91"/><text class="dim" x="60" y="106" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="81" x2="94" y2="91"/><text class="dim" x="94" y="106" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="81" x2="128" y2="91"/><text class="dim" x="128" y="106" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="81" x2="162" y2="91"/><text class="dim" x="162" y="106" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="81" x2="196" y2="91"/><text class="dim" x="196" y="106" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="81" x2="230" y2="91"/><text class="ink" x="230" y="106" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="81" x2="264" y2="91"/><text class="dim" x="264" y="106" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="81" x2="298" y2="91"/><text class="dim" x="298" y="106" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="81" x2="332" y2="91"/><text class="dim" x="332" y="106" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="81" x2="366" y2="91"/><text class="dim" x="366" y="106" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="81" x2="400" y2="91"/><text class="dim" x="400" y="106" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="81" x2="434" y2="91"/><text class="dim" x="434" y="106" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="81" x2="468" y2="91"/><text class="dim" x="468" y="106" font-size="10" text-anchor="middle">7</text><line class="curve" x1="196" y1="86" x2="400" y2="86" style="stroke-width:5"/><circle class="dot" cx="196" cy="86" r="6"/><circle class="dot" cx="400" cy="86" r="6"/><circle class="dot2" cx="298" cy="86" r="5"/><line class="curve2" x1="298" y1="60" x2="204" y2="60"/><polygon class="dot2" points="196,60 205,55 205,65"/><text class="ink" x="247.0" y="53" font-size="12" text-anchor="middle">3</text><line class="curve2" x1="298" y1="60" x2="392" y2="60"/><polygon class="dot2" points="400,60 391,55 391,65"/><text class="ink" x="349.0" y="53" font-size="12" text-anchor="middle">3</text><line class="curve3" stroke-dasharray="3 3" x1="298" y1="52" x2="298" y2="86"/><text class="dim" x="298" y="122" font-size="11" text-anchor="middle">merkez 2</text><text class="ink" x="298" y="140" font-size="13" text-anchor="middle">−1 ≤ x ≤ 5</text></svg>
  <figcaption>$|x - 2| \le 3$, $x$'in $2$'ye uzaklığının en fazla $3$ olduğunu söylüyor: $2$'nin iki yanında $3$'er birimlik bir bölge. Merkez $2$, yarıçap $3$; çözüm $-1 \le x \le 5$.</figcaption>
</figure>

| Koşul | Anlamı | Çözüm |
|---|---|---|
| $\lvert x - a \rvert \le r$ | $a$'ya uzaklık en fazla $r$ | $a - r \le x \le a + r$ |
| $\lvert x - a \rvert \ge r$ | $a$'ya uzaklık en az $r$ | $x \le a - r$ ya da $x \ge a + r$ |

"Küçük" bir **aralık** (içeride), "büyük" **iki ayrı parça** (dışarıda) verir.

**Örnek:** $|2x - 1| \le 5$.

$$
\begin{aligned}
-5 &\le 2x - 1 \le 5 \\
-4 &\le 2x \le 6 \\
-2 &\le x \le 3
\end{aligned}
$$

**Örnek:** $|x + 1| > 4$. $x + 1 > 4$ ya da $x + 1 < -4$: $x > 3$ ya da $x < -5$.

## Makine öğrenmesinde eşitsizlikler

**Eşik.** Bir sınıflandırıcı olasılık $p \ge 0{,}5$ ise "evet" der.
Eşiği $0{,}8$'e çıkarmak daha temkinli bir model demek: "evet" için daha
çok emin olmak gerekiyor.

**Tolerans.** "Tahmin gerçeğe en fazla $0{,}5$ yakın olsun" koşulu
$|\hat{y} - y| \le 0{,}5$ diye yazılır. Gerçek değer $12$ ise kabul edilen
tahminler $11{,}5 \le \hat{y} \le 12{,}5$.

**Kırpma.** Eğitimde çok büyük adımları önlemek için bir değer $[-1, 1]$
aralığına kırpılır: $-1$'den küçükse $-1$, $1$'den büyükse $1$ yapılır.
Bu, değerin $|g| \le 1$ koşulunu sağlamasını zorlamak demek.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$-2x < 6 \Rightarrow x < -3$</p>
      <p>$|x| < 3 \Rightarrow x < 3$</p>
      <p>$|x - 2| \ge 3 \Rightarrow -1 \ge x \ge 5$</p>
      <p>$x > 2$: $2$'de dolu daire</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$-2x < 6 \Rightarrow x > -3$ (yön döner)</p>
      <p>$|x| < 3 \Rightarrow -3 < x < 3$</p>
      <p>$x \le -1$ ya da $x \ge 5$ (iki parça)</p>
      <p>$x > 2$: $2$'de boş daire</p>
    </div>
  </div>
  <figcaption>Negatifle çarpıp bölünce yön döner; mutlak değer iki tarafı birden sınırlar.</figcaption>
</figure>

- **Yönü döndürmeyi unutmak.** Emin değilsen sınırın iki yanından birer
  sayı dene.
- **"Ya da"yı tek eşitsizliğe sıkıştırmak.** $x \le -1$ ya da $x \ge 5$
  kümesi $-1 \ge x \ge 5$ diye yazılamaz; böyle bir sayı yok.
- **Mutlak değerin negatif çıkabileceğini sanmak.** $|x - 3| < -2$'nin
  çözümü yok.

## Özet

- Eşitsizliğin çözümü bir aralık; sayı doğrusunda boş daire hariç, dolu daire dahil.
- Aralık gösterimi: $[\ ]$ dahil, $(\ )$ hariç; $\infty$ hep $($ ile.
- Denklem kuralları geçerli; negatifle çarpıp bölünce eşitsizlik yön değiştirir.
- Çift eşitsizlikte üç parçaya da aynı işlem.
- $|A| = r$: $A = r$ ya da $A = -r$ ($r \ge 0$).
- $|x - a| \le r$: $a - r \le x \le a + r$ (içeride); $|x - a| \ge r$: $x \le a - r$ ya da $x \ge a + r$ (dışarıda).
- Eşikler, toleranslar ve kırpmalar eşitsizliklerle yazılır.
