# Denklem Sistemleri

İki bilinmeyen varsa tek bir denklem yetmez: $x + y = 10$'u sonsuz sayıda
$(x, y)$ çifti sağlar. İkinci bir koşul eklenince ($x - y = 4$) çözüm
tek bir çifte iner. Birden fazla denklemin **aynı anda** sağlanmasını
isteyen bu yapıya **denklem sistemi** denir. Bir doğruyu iki noktadan
geçirmek, bir karışımın oranlarını bulmak ya da bir modelin
parametrelerini veriden çıkarmak hep bir denklem sistemi çözmek demek.

Ön bilgi: Birinci Dereceden Denklemler.

## Sistem nedir?

$$
\begin{cases}
x + y = 10 \\
x - y = 4
\end{cases}
$$

Çözüm, **iki denklemi birden** sağlayan $(x, y)$ çifti. $(6, 4)$ birinci
denklemi sağlar ($6 + 4 = 10$) ama ikinciyi sağlamaz ($6 - 4 = 2$). $(7,
3)$ ikisini de sağlar: sistemin çözümü.

## Grafikte bir sistem

Her birinci dereceden denklem düzlemde bir doğru çizer. Doğru üzerindeki
her nokta o denklemi sağlar. İki denklemi birden sağlayan nokta, iki
doğrunun **kesiştiği** yer.

<figure class="fig">
<svg viewBox="0 0 400 458.0" width="400"><line class="grid" x1="50.0" y1="420.0" x2="50.0" y2="20.0"/><line class="grid" x1="75.0" y1="420.0" x2="75.0" y2="20.0"/><line class="grid" x1="100.0" y1="420.0" x2="100.0" y2="20.0"/><line class="grid" x1="125.0" y1="420.0" x2="125.0" y2="20.0"/><line class="grid" x1="150.0" y1="420.0" x2="150.0" y2="20.0"/><line class="grid" x1="175.0" y1="420.0" x2="175.0" y2="20.0"/><line class="grid" x1="200.0" y1="420.0" x2="200.0" y2="20.0"/><line class="grid" x1="225.0" y1="420.0" x2="225.0" y2="20.0"/><line class="grid" x1="250.0" y1="420.0" x2="250.0" y2="20.0"/><line class="grid" x1="275.0" y1="420.0" x2="275.0" y2="20.0"/><line class="grid" x1="300.0" y1="420.0" x2="300.0" y2="20.0"/><line class="grid" x1="325.0" y1="420.0" x2="325.0" y2="20.0"/><line class="grid" x1="350.0" y1="420.0" x2="350.0" y2="20.0"/><line class="grid" x1="50.0" y1="420.0" x2="350.0" y2="420.0"/><line class="grid" x1="50.0" y1="395.0" x2="350.0" y2="395.0"/><line class="grid" x1="50.0" y1="370.0" x2="350.0" y2="370.0"/><line class="grid" x1="50.0" y1="345.0" x2="350.0" y2="345.0"/><line class="grid" x1="50.0" y1="320.0" x2="350.0" y2="320.0"/><line class="grid" x1="50.0" y1="295.0" x2="350.0" y2="295.0"/><line class="grid" x1="50.0" y1="270.0" x2="350.0" y2="270.0"/><line class="grid" x1="50.0" y1="245.0" x2="350.0" y2="245.0"/><line class="grid" x1="50.0" y1="220.0" x2="350.0" y2="220.0"/><line class="grid" x1="50.0" y1="195.0" x2="350.0" y2="195.0"/><line class="grid" x1="50.0" y1="170.0" x2="350.0" y2="170.0"/><line class="grid" x1="50.0" y1="145.0" x2="350.0" y2="145.0"/><line class="grid" x1="50.0" y1="120.0" x2="350.0" y2="120.0"/><line class="grid" x1="50.0" y1="95.0" x2="350.0" y2="95.0"/><line class="grid" x1="50.0" y1="70.0" x2="350.0" y2="70.0"/><line class="grid" x1="50.0" y1="45.0" x2="350.0" y2="45.0"/><line class="grid" x1="50.0" y1="20.0" x2="350.0" y2="20.0"/><line class="line" x1="50.0" y1="295.0" x2="350.0" y2="295.0"/><line class="line" x1="75.0" y1="420.0" x2="75.0" y2="20.0"/><text class="dim" x="125.0" y="308.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="175.0" y="308.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="225.0" y="308.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="275.0" y="308.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="325.0" y="308.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="70.0" y="398.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="70.0" y="248.0" font-size="9" text-anchor="end">2</text><text class="dim" x="70.0" y="198.0" font-size="9" text-anchor="end">4</text><text class="dim" x="70.0" y="148.0" font-size="9" text-anchor="end">6</text><text class="dim" x="70.0" y="98.0" font-size="9" text-anchor="end">8</text><text class="dim" x="70.0" y="48.0" font-size="9" text-anchor="end">10</text><line class="curve" x1="50.0" y1="20.0" x2="350.0" y2="320.0"/><line class="curve2" x1="50.0" y1="420.0" x2="350.0" y2="120.0"/><text class="ink" x="90.0" y="29.0" font-size="12" text-anchor="start">x + y = 10</text><text class="ink" x="330.0" y="134.0" font-size="12" text-anchor="end">x − y = 4</text><circle class="dot3" cx="250.0" cy="220.0" r="6"/><text class="ink" x="260.0" y="238.0" font-size="12" text-anchor="start">kesişim (7, 3)</text><text class="dim" x="200" y="446.0" font-size="11" text-anchor="middle">iki denklemi birden sağlayan tek nokta</text></svg>
  <figcaption>$x + y = 10$ (mor) ve $x - y = 4$ (turuncu) doğruları $(7, 3)$'te kesişiyor. Mor doğru üzerindeki her nokta birinci denklemi, turuncu üzerindeki her nokta ikinciyi sağlıyor; ikisinde birden olan tek nokta kesişim.</figcaption>
</figure>

Grafik yöntemi fikri anlamak için iyi ama kesişim tam sayı değilse
okumak zor. Kesin sonuç için iki cebirsel yol var.

## Yerine koyma

Denklemlerden birinde bir bilinmeyeni yalnız bırak, öbür denklemde yerine
yaz. Tek bilinmeyenli bir denklem kalır.

$$
\begin{cases}
y = 2x - 1 \\
3x + y = 14
\end{cases}
$$

Birinci denklem $y$'yi zaten veriyor. İkincide $y$ yerine $2x - 1$ yaz:

$$
\begin{aligned}
3x + (2x - 1) &= 14 \\
5x &= 15 \\
x &= 3
\end{aligned}
$$

Sonra $y = 2 \cdot 3 - 1 = 5$. Çözüm $(3, 5)$.

**Sağlama:** İki denklemde de: $5 = 6 - 1$ ✓, $9 + 5 = 14$ ✓.

## Yok etme

Denklemleri alt alta toplayarak ya da çıkararak bir bilinmeyeni yok et.
Katsayılar zıtsa doğrudan topla:

$$
\begin{aligned}
2x + 3y &= 12 \\
4x - 3y &= 6
\end{aligned}
$$

Topla: $6x = 18$, $x = 3$. Birinci denklemden $6 + 3y = 12$, $y = 2$.

**Katsayılar uymuyorsa önce çarp.** Denklemi bir sayıyla çarpmak çözümünü
değiştirmez.

$$
\begin{aligned}
3x + 2y &= 16 &&\text{(} \times 2\text{)} \\
2x + 5y &= 18 &&\text{(} \times 3\text{)}
\end{aligned}
$$

$$
\begin{aligned}
6x + 4y &= 32 \\
6x + 15y &= 54
\end{aligned}
$$

İkinciden birinciyi çıkar: $11y = 22$, $y = 2$. Sonra $3x + 4 = 16$, $x =
4$. Çözüm $(4, 2)$.

**Hangisini seçmeli?** Bir bilinmeyen zaten yalnızsa ya da katsayısı $1$
ise yerine koyma; katsayılar kolay eşitlenebiliyorsa yok etme. İkisi de
aynı sonucu verir.

## Kaç çözüm olabilir?

<figure class="fig">
<svg viewBox="0 0 500 213.66666666666666" width="500"><line class="line" x1="20.0" y1="138.3" x2="150.0" y2="138.3"/><line class="line" x1="41.7" y1="181.7" x2="41.7" y2="30.0"/><line class="curve" x1="20.0" y1="127.5" x2="150.0" y2="62.5"/><line class="curve2" x1="20.0" y1="30.0" x2="150.0" y2="160.0"/><circle class="dot3" cx="85.0" cy="95.0" r="5"/><text class="ink" x="85" y="18" font-size="13" text-anchor="middle">tek çözüm</text><text class="dim" x="85" y="201.66666666666666" font-size="11" text-anchor="middle">doğrular kesişir</text><line class="line" x1="180.0" y1="138.3" x2="310.0" y2="138.3"/><line class="line" x1="201.7" y1="181.7" x2="201.7" y2="30.0"/><line class="curve" x1="180.0" y1="108.0" x2="310.0" y2="30.0"/><line class="curve2" x1="180.0" y1="173.0" x2="310.0" y2="95.0"/><text class="ink" x="245" y="18" font-size="13" text-anchor="middle">çözüm yok</text><text class="dim" x="245" y="201.66666666666666" font-size="11" text-anchor="middle">paralel doğrular</text><line class="line" x1="340.0" y1="138.3" x2="470.0" y2="138.3"/><line class="line" x1="361.7" y1="181.7" x2="361.7" y2="30.0"/><line class="curve" x1="340.0" y1="62.5" x2="470.0" y2="127.5"/><line class="curve2" stroke-dasharray="7 5" x1="340.0" y1="62.5" x2="470.0" y2="127.5"/><text class="ink" x="405" y="18" font-size="13" text-anchor="middle">sonsuz çözüm</text><text class="dim" x="405" y="201.66666666666666" font-size="11" text-anchor="middle">aynı doğru</text></svg>
  <figcaption>İki doğru ya bir noktada kesişir (tek çözüm), ya paraleldir ve hiç kesişmez (çözüm yok), ya da aynı doğrudur ve her noktası ortaktır (sonsuz çözüm).</figcaption>
</figure>

Cebirde bu durumlar yok etme sırasında görünür:

| Yok ettikten sonra | Anlamı | Örnek |
|---|---|---|
| $x = 3$ gibi bir değer | tek çözüm | yukarıdaki örnekler |
| $0 = 7$ gibi yanlış | çözüm yok (paralel) | $x + y = 2$ ve $x + y = 9$ |
| $0 = 0$ | sonsuz çözüm (aynı doğru) | $x + y = 2$ ve $2x + 2y = 4$ |

## Sözel problemleri sisteme çevirmek

İki bilinmeyen, iki bilgi: her bilgi bir denklem.

**Örnek:** Bir konsere $120$ bilet satıldı; tam bilet $50$, öğrenci $30$
lira; toplam gelir $5\,000$ lira. Kaç tam bilet satıldı?

$t$ = tam, $o$ = öğrenci.

$$
\begin{cases}
t + o = 120 \\
50t + 30o = 5\,000
\end{cases}
$$

Birinciden $o = 120 - t$; ikinciye koy: $50t + 3\,600 - 30t = 5\,000$,
$20t = 1\,400$, $t = 70$, $o = 50$.

## Makine öğrenmesinde denklem sistemleri

**İki noktadan geçen doğru.** $\hat{y} = wx + b$ modeli $(1, 5)$ ve $(3,
11)$ noktalarından geçsin:

$$
\begin{cases}
w + b = 5 \\
3w + b = 11
\end{cases}
$$

Çıkar: $2w = 6$, $w = 3$, $b = 2$. Model $\hat{y} = 3x + 2$.

**Veri çok, bilinmeyen az.** Gerçek veride yüzlerce nokta var ama doğrunun
yalnızca iki parametresi. Bütün noktalardan geçen bir doğru genelde yok:
sistemin tam çözümü yok. Doğrusal regresyon bunun yerine hatayı en küçük
yapan $w$ ve $b$'yi arar; bu da sonunda iki bilinmeyenli bir sistem
çözmeye iner. Çok bilinmeyenli sistemleri İleri Matematik'te (Gauss eleme)
göreceğiz.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>Yalnızca $x$'i bulup durmak</p>
      <p>Çıkarırken tek terimin işaretini değiştirmek</p>
      <p>$y$'yi bulduğun denkleme geri koymak</p>
      <p>Tek denklemde sağlamak</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Çözüm bir çift: $(x, y)$</p>
      <p>Bütün denklemi çıkar: her terimin işareti değişir</p>
      <p>$y$'yi <b>öbür</b> denkleme koy</p>
      <p>İki denklemde de sağla</p>
    </div>
  </div>
  <figcaption>Sistemin çözümü iki denklemi birden sağlamalı; sağlamayı ikisinde de yap.</figcaption>
</figure>

- **Aynı denklemde yerine koymak.** $y = 2x - 1$'i kendisine koyarsan $2x -
  1 = 2x - 1$ çıkar: hiçbir bilgi yok.
- **Çarparken bir terimi atlamak.** Bir denklemi çarparken **sağ taraf
  dahil** her terim çarpılır.

## Özet

- Denklem sistemi: birden fazla denklemin aynı anda sağlanması; çözüm bir $(x, y)$ çifti.
- Grafikte çözüm iki doğrunun kesişimi.
- Yerine koyma: bir bilinmeyeni yalnız bırak, öbür denklemde yerine yaz.
- Yok etme: katsayıları eşitle, topla ya da çıkar; bir bilinmeyen kaybolur.
- Tek çözüm (kesişen), çözüm yok (paralel, $0 = 7$), sonsuz çözüm (aynı doğru, $0 = 0$).
- Sözel problemde her bilgi bir denklem; iki bilinmeyen için iki bağımsız bilgi gerekir.
- İki noktadan geçen doğruyu bulmak iki bilinmeyenli bir sistem.
