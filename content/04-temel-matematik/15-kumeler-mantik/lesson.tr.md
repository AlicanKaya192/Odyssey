# Kümeler ve Mantık

Matematiğin iki temel dili: **kümeler** nesneleri gruplamayı, **mantık** da
doğru–yanlış cümlelerle akıl yürütmeyi anlatıyor. Bir veri setindeki
satırları süzmek, eğitim ve test verisinin çakışmadığından emin olmak ya
da bir modelin ne kadar isabetli olduğunu ölçmek hep bu iki dille yapılıyor.
pandas'ta `&`, `|`, `~` ile yazdığın her süzgeç, bu bölümdeki işlemlerin
kendisi.

Ön bilgi: Matematiği Okumak.

## Küme ve eleman

**Küme**, iyi tanımlanmış nesnelerin topluluğu. Elemanları süslü parantez
içinde yazılır; sıra ve tekrar önemli değildir:

$$
A = \{1, 2, 3\} = \{3, 1, 2\} = \{1, 1, 2, 3\}
$$

| Gösterim | Anlamı | Örnek |
|---|---|---|
| $x \in A$ | $x$, $A$'nın elemanı | $2 \in \{1, 2, 3\}$ |
| $x \notin A$ | $x$, $A$'nın elemanı değil | $5 \notin \{1, 2, 3\}$ |
| $\emptyset$ | boş küme | $\{\}$ |
| $s(A)$ ya da $\lvert A \rvert$ | eleman sayısı | $s(\{1, 2, 3\}) = 3$ |
| $A \subseteq B$ | $A$'nın her elemanı $B$'de | $\{1, 2\} \subseteq \{1, 2, 3\}$ |

Kümeler bir **kuralla** da yazılabilir: $\{x \mid x \text{ çift ve } 0 < x <
10\} = \{2, 4, 6, 8\}$. "$\mid$" işareti "öyle ki" diye okunur.

### Sayı kümeleri

<figure class="fig">
<svg viewBox="0 0 480 260" width="480"><ellipse class="curve3" cx="240" cy="130" rx="215" ry="115"/><text class="ink" x="240" y="31" font-size="12" text-anchor="middle">ℝ gerçek</text><ellipse class="dot2" opacity="0.18" cx="240" cy="130" rx="160" ry="88"/><ellipse class="curve2" cx="240" cy="130" rx="160" ry="88"/><text class="ink" x="240" y="58" font-size="12" text-anchor="middle">ℚ rasyonel</text><ellipse class="dot" opacity="0.18" cx="240" cy="130" rx="108" ry="62"/><ellipse class="curve" cx="240" cy="130" rx="108" ry="62"/><text class="ink" x="240" y="84" font-size="12" text-anchor="middle">ℤ tam</text><ellipse class="dot3" opacity="0.18" cx="240" cy="130" rx="58" ry="36"/><ellipse class="curve4" cx="240" cy="130" rx="58" ry="36"/><text class="ink" x="240" y="110" font-size="12" text-anchor="middle">ℕ doğal</text><text class="ink" x="226" y="140" font-size="13" text-anchor="middle">0</text><text class="ink" x="254" y="140" font-size="13" text-anchor="middle">5</text><text class="ink" x="320" y="136" font-size="13" text-anchor="middle">−3</text><text class="ink" x="108" y="136" font-size="13" text-anchor="middle">1/2</text><text class="ink" x="372" y="136" font-size="13" text-anchor="middle">0,75</text><text class="ink" x="52" y="136" font-size="13" text-anchor="middle">√2</text><text class="ink" x="428" y="136" font-size="13" text-anchor="middle">π</text></svg>
  <figcaption>Şimdiye kadarki sayılar iç içe kümeler: her doğal sayı bir tam sayı, her tam sayı bir rasyonel sayı (kesir), her rasyonel sayı bir gerçek sayı. $\sqrt{2}$ ve $\pi$ gerçek ama rasyonel değil.</figcaption>
</figure>

$$
\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}
$$

## Küme işlemleri

<figure class="fig">
<svg viewBox="0 0 460 262" width="460"><rect class="box" x="20" y="20" width="420" height="230" rx="8"/><text class="dim" x="36" y="42" font-size="11" text-anchor="start">U: 30 öğrenci</text><circle class="dot" opacity="0.25" cx="180" cy="140" r="85"/><circle class="dot2" opacity="0.25" cx="280" cy="140" r="85"/><circle class="curve" cx="180" cy="140" r="85"/><circle class="curve2" cx="280" cy="140" r="85"/><text class="ink" x="160" y="47" font-size="12" text-anchor="middle">Python (18)</text><text class="ink" x="300" y="47" font-size="12" text-anchor="middle">SQL (12)</text><text class="ink" x="140" y="144" font-size="20" text-anchor="middle">11</text><text class="dim" x="140" y="162" font-size="10" text-anchor="middle">yalnız Python</text><text class="ink" x="230.0" y="144" font-size="20" text-anchor="middle">7</text><text class="dim" x="230.0" y="162" font-size="10" text-anchor="middle">ikisi</text><text class="ink" x="320" y="144" font-size="20" text-anchor="middle">5</text><text class="dim" x="320" y="162" font-size="10" text-anchor="middle">yalnız SQL</text><text class="ink" x="400" y="230" font-size="18" text-anchor="middle">7</text><text class="dim" x="400" y="244" font-size="10" text-anchor="middle">hiçbiri</text></svg>
  <figcaption>$30$ öğrencinin $18$'i Python, $12$'si SQL biliyor, $7$'si ikisini de. Venn şemasında dört bölge var: yalnız Python ($11$), ikisi ($7$), yalnız SQL ($5$) ve hiçbiri ($7$). Toplam $11 + 7 + 5 + 7 = 30$.</figcaption>
</figure>

| İşlem | Gösterim | Anlamı |
|---|---|---|
| Birleşim | $A \cup B$ | $A$'da **ya da** $B$'de (ya da ikisinde) |
| Kesişim | $A \cap B$ | hem $A$'da **hem** $B$'de |
| Fark | $A \setminus B$ | $A$'da olup $B$'de olmayan |
| Tümleyen | $A'$ | evrensel kümede olup $A$'da olmayan |

$A = \{1, 2, 3, 4\}$, $B = \{3, 4, 5\}$ için:

$$
A \cup B = \{1, 2, 3, 4, 5\}, \quad A \cap B = \{3, 4\}, \quad A \setminus B = \{1, 2\}
$$

Kesişimi boş olan kümelere **ayrık** denir: $A \cap B = \emptyset$.

### Birleşimin eleman sayısı

İki kümenin elemanlarını toplarken ortak elemanlar **iki kez** sayılır; bir
kez çıkarmak gerekir:

$$
s(A \cup B) = s(A) + s(B) - s(A \cap B)
$$

Şekildeki örnekte: $18 + 12 - 7 = 23$ öğrenci en az birini biliyor, $30 -
23 = 7$ öğrenci hiçbirini bilmiyor.

## Mantık: önermeler

**Önerme**, doğru ya da yanlış olan bir cümle. "$3 > 2$" doğru, "$2 + 2 =
5$" yanlış. "Bu soru zor" gibi kişiye göre değişen cümleler önerme değil.

Önermeler bağlaçlarla birleşir. $p$ ve $q$ iki önerme olsun ($1$ doğru,
$0$ yanlış):

| $p$ | $q$ | $p \wedge q$ (ve) | $p \vee q$ (veya) | $\neg p$ (değil) | $p \Rightarrow q$ (ise) |
|---|---|---|---|---|---|
| $1$ | $1$ | $1$ | $1$ | $0$ | $1$ |
| $1$ | $0$ | $0$ | $1$ | $0$ | $0$ |
| $0$ | $1$ | $0$ | $1$ | $1$ | $1$ |
| $0$ | $0$ | $0$ | $0$ | $1$ | $1$ |

- **ve** ($\wedge$): ikisi de doğruysa doğru.
- **veya** ($\vee$): en az biri doğruysa doğru. Matematikte "veya" **kapsayıcı**:
  ikisi birden doğruysa da doğru.
- **ise** ($\Rightarrow$): yalnızca "öncül doğru, sonuç yanlış" durumunda
  yanlış. "Yağmur yağarsa yer ıslanır" sözü, yağmur yağmadığı bir günde
  çiğnenmiş olmaz.

**Tersi aynı şey değil.** $p \Rightarrow q$ doğru olsa da $q \Rightarrow
p$ yanlış olabilir: "sayı $4$'e bölünüyorsa çifttir" doğru, "sayı çiftse
$4$'e bölünür" yanlış ($6$).

## Kümeler ile mantık aynı dil

| Mantık | Küme |
|---|---|
| ve ($\wedge$) | kesişim ($\cap$) |
| veya ($\vee$) | birleşim ($\cup$) |
| değil ($\neg$) | tümleyen ($'$) |
| ise ($\Rightarrow$) | alt küme ($\subseteq$) |

**De Morgan kuralları:** "ve"nin değili, değillerin "veya"sı:

$$
\neg(p \wedge q) = \neg p \vee \neg q, \qquad (A \cap B)' = A' \cup B'
$$

$$
\neg(p \vee q) = \neg p \wedge \neg q, \qquad (A \cup B)' = A' \cap B'
$$

"Hem Python hem SQL biliyor" cümlesinin değili "Python bilmiyor **veya**
SQL bilmiyor"; "ikisini de bilmiyor" değil.

## Makine öğrenmesinde kümeler ve mantık

**Veri süzmek.** pandas'ta `df[(df["yas"] > 30) & (df["sehir"] == "Ankara")]`
iki koşulun kesişimini, `|` birleşimini, `~` tümleyenini alır. Parantezler
şart: `&`, karşılaştırmadan önce işlenir.

**Eğitim ve test ayrık olmalı.** Eğitim kümesi ile test kümesinin kesişimi
boş değilse model sınavdan önce soruları görmüş olur; ölçülen başarı
gerçeği yansıtmaz. Buna **veri sızıntısı** denir.

**İsabet ölçüleri.** "Modelin spam dediği" küme $T$, "gerçekten spam olan"
küme $G$ ise:

$$
\text{kesinlik} = \frac{s(T \cap G)}{s(T)}, \qquad \text{duyarlılık} = \frac{s(T \cap G)}{s(G)}
$$

Kesinlik, "spam dediklerimin ne kadarı gerçekten spam?"; duyarlılık,
"gerçek spamlerin ne kadarını yakaladım?" sorusunun cevabı.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$s(A \cup B) = s(A) + s(B)$</p>
      <p>$\neg(p \wedge q) = \neg p \wedge \neg q$</p>
      <p>$p \Rightarrow q$ ise $q \Rightarrow p$</p>
      <p>"veya" = biri ama ikisi değil</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$s(A) + s(B) - s(A \cap B)$</p>
      <p>$\neg p \vee \neg q$</p>
      <p>Tersi ayrıca kanıtlanmalı</p>
      <p>"veya" ikisini birden de kapsar</p>
    </div>
  </div>
  <figcaption>Kesişim iki kez sayılır; "değil" bir bağlacın içine girerken "ve"yi "veya"ya çevirir.</figcaption>
</figure>

- **Tekrarlı eleman saymak.** $\{1, 1, 2\}$'nin eleman sayısı $2$.
- **$\in$ ile $\subseteq$'yi karıştırmak.** $2 \in \{1, 2\}$ ama $\{2\}
  \subseteq \{1, 2\}$; eleman ile küme farklı şeyler.

## Özet

- Küme: sıra ve tekrarın önemsiz olduğu topluluk; $\in$, $\notin$, $\emptyset$, $\subseteq$.
- $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.
- Birleşim "veya", kesişim "ve", fark "ama değil", tümleyen "değil".
- $s(A \cup B) = s(A) + s(B) - s(A \cap B)$.
- Önerme doğru ya da yanlış; $\wedge$, $\vee$, $\neg$, $\Rightarrow$ doğruluk tablosuyla tanımlı.
- $p \Rightarrow q$ yalnızca $p$ doğru, $q$ yanlışken yanlış; tersi ayrı bir önerme.
- De Morgan: $\neg(p \wedge q) = \neg p \vee \neg q$, $(A \cup B)' = A' \cap B'$.
- Veri süzgeçleri, veri sızıntısı ve kesinlik–duyarlılık küme diliyle yazılır.
