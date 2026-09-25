# Rastgele Değişkenler, Beklenen Değer ve Varyans

Olasılık şimdiye kadar olaylarla konuştu: "tura gelir mi?", "hasta mı?".
Çoğu soru ise bir sayıyla ilgili: kaç tura geldi, müşteri ne kadar
harcadı, model ne kadar hata yaptı. **Rastgele değişken**, bir deneyin
sonucunu bir sayıya çevirir. İki özet onu anlatmaya çoğu zaman yeter:
**beklenen değer** (uzun vadede ortalama ne çıkar) ve **varyans** (ne kadar
yayılır). Makine öğrenmesinde eğitim bir beklenen değeri (beklenen kaybı)
küçültmek demek; stokastik gradyan bir beklenen değerin tahmini,
dropout'taki ölçekleme bir beklenen değeri korumak için. Bu bölümde kesikli
ve sürekli rastgele değişkenleri, beklenen değeri, varyansı ve bunların
hesap kurallarını göreceğiz.

Ön bilgi: Koşullu Olasılık ve Bayes, İntegral ve Alan, MAT 1'deki Veri ve
Temel İstatistik bölümleri.

## Rastgele değişken

Rastgele değişken, her sonuca bir sayı atayan bir fonksiyon. Üç kez yazı
tura atalım; $X$ tura sayısı olsun. Sekiz eşit olasılıklı sonuç var:

| Sonuç | YYY | YYT, YTY, TYY | YTT, TYT, TTY | TTT |
|---|---|---|---|---|
| $X$ | $0$ | $1$ | $2$ | $3$ |
| $P(X = x)$ | $\frac{1}{8}$ | $\frac{3}{8}$ | $\frac{3}{8}$ | $\frac{1}{8}$ |

Değerleri sayılabilen (ayrık) değişkenlere **kesikli**, bir aralıktaki her
değeri alabilenlere **sürekli** denir. Tura sayısı kesikli, bir kişinin
boyu sürekli.

## Olasılık dağılımı

Kesikli bir değişkenin her değerine olasılığını veren tabloya **olasılık
kütle fonksiyonu** $p(x) = P(X = x)$ denir. İki kuralı var: her $p(x) \geq 0$
ve $\sum_x p(x) = 1$.

<figure class="fig">
<svg viewBox="0 0 440 242" width="440"><line class="grid" x1="98.6" y1="210.0" x2="98.6" y2="20.0"/><line class="grid" x1="179.5" y1="210.0" x2="179.5" y2="20.0"/><line class="grid" x1="260.5" y1="210.0" x2="260.5" y2="20.0"/><line class="grid" x1="341.4" y1="210.0" x2="341.4" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="grid" x1="50.0" y1="157.2" x2="390.0" y2="157.2"/><line class="grid" x1="50.0" y1="104.4" x2="390.0" y2="104.4"/><line class="grid" x1="50.0" y1="51.7" x2="390.0" y2="51.7"/><line class="line" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="line" x1="98.6" y1="210.0" x2="98.6" y2="20.0"/><text class="dim" x="98.6" y="223.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="179.5" y="223.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="260.5" y="223.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="341.4" y="223.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="93.6" y="107.4" font-size="9" text-anchor="end">0.25</text><text class="dim" x="93.6" y="54.7" font-size="9" text-anchor="end">0.375</text><rect class="dot" opacity="0.6" x="74.3" y="157.2" width="48.6" height="52.8"/><text class="ink" x="98.6" y="151.2" font-size="11" text-anchor="middle">1/8</text><rect class="dot" opacity="0.6" x="155.2" y="51.7" width="48.6" height="158.3"/><text class="ink" x="179.5" y="45.7" font-size="11" text-anchor="middle">3/8</text><rect class="dot" opacity="0.6" x="236.2" y="51.7" width="48.6" height="158.3"/><text class="ink" x="260.5" y="45.7" font-size="11" text-anchor="middle">3/8</text><rect class="dot" opacity="0.6" x="317.1" y="157.2" width="48.6" height="52.8"/><text class="ink" x="341.4" y="151.2" font-size="11" text-anchor="middle">1/8</text><line class="curve2" stroke-dasharray="5 4" x1="220.0" y1="210.0" x2="220.0" y2="28.4"/><text class="ink" x="220.0" y="24.4" font-size="11" text-anchor="middle">E[X] = 1,5</text><text class="dim" x="390.0" y="238.0" font-size="10" text-anchor="end">tura sayısı x</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">P(X = x)</text></svg>
  <figcaption>Üç atışta tura sayısının dağılımı: 0 ve 3 birer yolla (1/8), 1 ve 2 üçer yolla (3/8). Dağılım 1,5'e göre simetrik; beklenen değer tam ortada.</figcaption>
</figure>

**Birikimli dağılım** $F(x) = P(X \leq x)$: $x$'e kadar olan olasılıkların
toplamı. Burada $F(1) = \frac{1}{8} + \frac{3}{8} = \frac{1}{2}$.

## Beklenen değer

Beklenen değer, her değerin olasılığıyla ağırlıklandırılmış ortalaması:

$$
E[X] = \mu = \sum_x x \, p(x)
$$

Tura sayısı: $0 \cdot \frac{1}{8} + 1 \cdot \frac{3}{8} + 2 \cdot \frac{3}{8} +
3 \cdot \frac{1}{8} = \frac{12}{8} = 1{,}5$.

Zar: $\frac{1 + 2 + 3 + 4 + 5 + 6}{6} = 3{,}5$. Beklenen değerin bir sonuç
olması gerekmez; zar hiç $3{,}5$ göstermez. Anlamı: çok sayıda atışın
ortalaması $3{,}5$'e yaklaşır (büyük sayılar yasası).

**Bir oyun.** $10$ lira verip zar atıyorsun; $6$ gelirse $50$ lira
kazanıyorsun, gelmezse hiçbir şey. Net kazanç $X$: $40$ ($\frac{1}{6}$) ya
da $-10$ ($\frac{5}{6}$).

$$
E[X] = 40 \cdot \tfrac{1}{6} - 10 \cdot \tfrac{5}{6} = \frac{40 - 50}{6} \approx -1{,}67
$$

Her oyunda ortalama $1{,}67$ lira kaybedilir. Kumarhaneler beklenen değeri
kendi lehlerine olan oyunlar kurar.

**Bir fonksiyonun beklenen değeri.** $E[g(X)] = \sum_x g(x) \, p(x)$.
Zarda $E[X^2] = \frac{1 + 4 + 9 + 16 + 25 + 36}{6} = \frac{91}{6}$.
Dikkat: $E[X^2] \neq (E[X])^2 = 12{,}25$.

## Doğrusallık

Beklenen değerin en kullanışlı özelliği:

$$
E[aX + b] = a \, E[X] + b \qquad E[X + Y] = E[X] + E[Y]
$$

İkinci eşitlik $X$ ile $Y$ bağımlı olsa bile doğru. $10$ zarın toplamının
beklenen değeri $10 \cdot 3{,}5 = 35$; toplamın dağılımını hiç
hesaplamadan.

## Varyans

Varyans, değerlerin beklenen değerden sapmalarının karesinin beklenen
değeri:

$$
\operatorname{Var}(X) = E\big[(X - \mu)^2\big] = E[X^2] - \mu^2
$$

Standart sapma $\sigma = \sqrt{\operatorname{Var}(X)}$. İkinci biçim hesap
için kolay. Zar: $\frac{91}{6} - 3{,}5^2 = \frac{182 - 147}{12} =
\frac{35}{12} \approx 2{,}92$; $\sigma \approx 1{,}71$.

<figure class="fig">
<svg viewBox="0 0 440 212" width="440"><line class="grid" x1="35.8" y1="170.0" x2="35.8" y2="30.0"/><line class="grid" x1="62.2" y1="170.0" x2="62.2" y2="30.0"/><line class="grid" x1="88.6" y1="170.0" x2="88.6" y2="30.0"/><line class="grid" x1="115.0" y1="170.0" x2="115.0" y2="30.0"/><line class="grid" x1="141.4" y1="170.0" x2="141.4" y2="30.0"/><line class="grid" x1="167.8" y1="170.0" x2="167.8" y2="30.0"/><line class="grid" x1="194.2" y1="170.0" x2="194.2" y2="30.0"/><line class="grid" x1="20.0" y1="170.0" x2="210.0" y2="170.0"/><line class="grid" x1="20.0" y1="106.4" x2="210.0" y2="106.4"/><line class="grid" x1="20.0" y1="42.7" x2="210.0" y2="42.7"/><line class="line" x1="20.0" y1="170.0" x2="210.0" y2="170.0"/><line class="line" x1="35.8" y1="170.0" x2="35.8" y2="30.0"/><text class="dim" x="35.8" y="183.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="62.2" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="88.6" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="115.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="141.4" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="167.8" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="194.2" y="183.0" font-size="9" text-anchor="middle">6</text><rect class="dot" opacity="0.6" x="80.7" y="106.4" width="15.8" height="63.6"/><rect class="dot" opacity="0.6" x="107.1" y="42.7" width="15.8" height="127.3"/><rect class="dot" opacity="0.6" x="133.5" y="106.4" width="15.8" height="63.6"/><line class="curve3" stroke-dasharray="5 4" x1="115.0" y1="170.0" x2="115.0" y2="30.0"/><text class="ink" x="115" y="20" font-size="12" text-anchor="middle">A: Var = 0,5</text><line class="grid" x1="250.8" y1="170.0" x2="250.8" y2="30.0"/><line class="grid" x1="277.2" y1="170.0" x2="277.2" y2="30.0"/><line class="grid" x1="303.6" y1="170.0" x2="303.6" y2="30.0"/><line class="grid" x1="330.0" y1="170.0" x2="330.0" y2="30.0"/><line class="grid" x1="356.4" y1="170.0" x2="356.4" y2="30.0"/><line class="grid" x1="382.8" y1="170.0" x2="382.8" y2="30.0"/><line class="grid" x1="409.2" y1="170.0" x2="409.2" y2="30.0"/><line class="grid" x1="235.0" y1="170.0" x2="425.0" y2="170.0"/><line class="grid" x1="235.0" y1="106.4" x2="425.0" y2="106.4"/><line class="grid" x1="235.0" y1="42.7" x2="425.0" y2="42.7"/><line class="line" x1="235.0" y1="170.0" x2="425.0" y2="170.0"/><line class="line" x1="250.8" y1="170.0" x2="250.8" y2="30.0"/><text class="dim" x="250.8" y="183.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="277.2" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="303.6" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="330.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="356.4" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="382.8" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="409.2" y="183.0" font-size="9" text-anchor="middle">6</text><rect class="dot2" opacity="0.6" x="242.9" y="119.1" width="15.9" height="50.9"/><rect class="dot2" opacity="0.6" x="269.3" y="144.5" width="15.8" height="25.5"/><rect class="dot2" opacity="0.6" x="322.1" y="68.2" width="15.8" height="101.8"/><rect class="dot2" opacity="0.6" x="374.9" y="144.5" width="15.8" height="25.5"/><rect class="dot2" opacity="0.6" x="401.2" y="119.1" width="15.9" height="50.9"/><line class="curve3" stroke-dasharray="5 4" x1="330.0" y1="170.0" x2="330.0" y2="30.0"/><text class="ink" x="330" y="20" font-size="12" text-anchor="middle">B: Var = 4,4</text><text class="ink" x="220" y="200" font-size="12" text-anchor="middle">ikisinde de E[X] = 3</text></svg>
  <figcaption>İki dağılımın da beklenen değeri 3. A'nın olasılığı 2 ile 4 arasında toplanmış, varyansı 0,5. B'nin olasılığı uçlara yayılmış, varyansı 4,4. Beklenen değer merkezi, varyans yayılımı anlatıyor.</figcaption>
</figure>

**Kurallar.**

| Kural | Neden |
|---|---|
| $\operatorname{Var}(X + b) = \operatorname{Var}(X)$ | kaydırmak yayılımı değiştirmez |
| $\operatorname{Var}(aX) = a^2 \operatorname{Var}(X)$ | sapmalar $a$ katı, kareleri $a^2$ katı |
| bağımsızsa $\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)$ | ortak dalgalanma yok |

**Ortalamanın varyansı.** $n$ bağımsız ve aynı dağılımlı değişkenin
ortalaması $\bar{X}$ için $E[\bar{X}] = \mu$ ve
$\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$. Ortalama almak merkezi
korur, yayılımı küçültür; standart sapma $\frac{\sigma}{\sqrt{n}}$ ile
azalır. Örnekleme ve Merkezi Limit Teoremi bölümü bunun üstüne kurulu.

## Sürekli rastgele değişkenler

Sürekli bir değişkenin tek bir değeri alma olasılığı $0$'dır; olasılık
aralıklara verilir. Bunu bir **olasılık yoğunluk fonksiyonu** $f(x)$
anlatır: bir aralığın olasılığı eğrinin altındaki alan.

$$
P(a \leq X \leq b) = \int_a^b f(x) \, dx \qquad \int_{-\infty}^{\infty} f(x) \, dx = 1
$$

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="76.2" y1="220.0" x2="76.2" y2="20.0"/><line class="grid" x1="141.5" y1="220.0" x2="141.5" y2="20.0"/><line class="grid" x1="206.9" y1="220.0" x2="206.9" y2="20.0"/><line class="grid" x1="272.3" y1="220.0" x2="272.3" y2="20.0"/><line class="grid" x1="337.7" y1="220.0" x2="337.7" y2="20.0"/><line class="grid" x1="50.0" y1="220.0" x2="390.0" y2="220.0"/><line class="grid" x1="50.0" y1="176.5" x2="390.0" y2="176.5"/><line class="grid" x1="50.0" y1="133.0" x2="390.0" y2="133.0"/><line class="grid" x1="50.0" y1="89.6" x2="390.0" y2="89.6"/><line class="grid" x1="50.0" y1="46.1" x2="390.0" y2="46.1"/><line class="line" x1="50.0" y1="220.0" x2="390.0" y2="220.0"/><line class="line" x1="76.2" y1="220.0" x2="76.2" y2="20.0"/><text class="dim" x="206.9" y="233.0" font-size="9" text-anchor="middle">0.5</text><text class="dim" x="337.7" y="233.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="71.2" y="136.0" font-size="9" text-anchor="end">1</text><text class="dim" x="71.2" y="49.1" font-size="9" text-anchor="end">2</text><polygon class="dot" opacity="0.35" points="206.9,220.0 206.9,133.0 208.0,132.3 209.1,131.6 210.2,130.9 211.3,130.1 212.4,129.4 213.5,128.7 214.6,128.0 215.6,127.2 216.7,126.5 217.8,125.8 218.9,125.1 220.0,124.3 221.1,123.6 222.2,122.9 223.3,122.2 224.4,121.4 225.4,120.7 226.5,120.0 227.6,119.3 228.7,118.6 229.8,117.8 230.9,117.1 232.0,116.4 233.1,115.7 234.2,114.9 235.3,114.2 236.3,113.5 237.4,112.8 238.5,112.0 239.6,111.3 240.7,110.6 241.8,109.9 242.9,109.1 244.0,108.4 245.1,107.7 246.2,107.0 247.2,106.2 248.3,105.5 249.4,104.8 250.5,104.1 251.6,103.3 252.7,102.6 253.8,101.9 254.9,101.2 256.0,100.4 257.1,99.7 258.1,99.0 259.2,98.3 260.3,97.5 261.4,96.8 262.5,96.1 263.6,95.4 264.7,94.6 265.8,93.9 266.9,93.2 267.9,92.5 269.0,91.7 270.1,91.0 271.2,90.3 272.3,89.6 273.4,88.8 274.5,88.1 275.6,87.4 276.7,86.7 277.8,85.9 278.8,85.2 279.9,84.5 281.0,83.8 282.1,83.0 283.2,82.3 284.3,81.6 285.4,80.9 286.5,80.1 287.6,79.4 288.7,78.7 289.7,78.0 290.8,77.2 291.9,76.5 293.0,75.8 294.1,75.1 295.2,74.3 296.3,73.6 297.4,72.9 298.5,72.2 299.6,71.4 300.6,70.7 301.7,70.0 302.8,69.3 303.9,68.6 305.0,67.8 306.1,67.1 307.2,66.4 308.3,65.7 309.4,64.9 310.4,64.2 311.5,63.5 312.6,62.8 313.7,62.0 314.8,61.3 315.9,60.6 317.0,59.9 318.1,59.1 319.2,58.4 320.3,57.7 321.3,57.0 322.4,56.2 323.5,55.5 324.6,54.8 325.7,54.1 326.8,53.3 327.9,52.6 329.0,51.9 330.1,51.2 331.2,50.4 332.2,49.7 333.3,49.0 334.4,48.3 335.5,47.5 336.6,46.8 337.7,46.1 337.7,220.0"/><polyline class="curve" fill="none" points="76.2,220.0 77.2,219.3 78.3,218.6 79.4,217.8 80.5,217.1 81.6,216.4 82.7,215.7 83.8,214.9 84.9,214.2 86.0,213.5 87.1,212.8 88.1,212.0 89.2,211.3 90.3,210.6 91.4,209.9 92.5,209.1 93.6,208.4 94.7,207.7 95.8,207.0 96.9,206.2 97.9,205.5 99.0,204.8 100.1,204.1 101.2,203.3 102.3,202.6 103.4,201.9 104.5,201.2 105.6,200.4 106.7,199.7 107.8,199.0 108.8,198.3 109.9,197.5 111.0,196.8 112.1,196.1 113.2,195.4 114.3,194.6 115.4,193.9 116.5,193.2 117.6,192.5 118.7,191.7 119.7,191.0 120.8,190.3 121.9,189.6 123.0,188.8 124.1,188.1 125.2,187.4 126.3,186.7 127.4,185.9 128.5,185.2 129.6,184.5 130.6,183.8 131.7,183.0 132.8,182.3 133.9,181.6 135.0,180.9 136.1,180.1 137.2,179.4 138.3,178.7 139.4,178.0 140.4,177.2 141.5,176.5 142.6,175.8 143.7,175.1 144.8,174.3 145.9,173.6 147.0,172.9 148.1,172.2 149.2,171.4 150.3,170.7 151.3,170.0 152.4,169.3 153.5,168.6 154.6,167.8 155.7,167.1 156.8,166.4 157.9,165.7 159.0,164.9 160.1,164.2 161.2,163.5 162.2,162.8 163.3,162.0 164.4,161.3 165.5,160.6 166.6,159.9 167.7,159.1 168.8,158.4 169.9,157.7 171.0,157.0 172.1,156.2 173.1,155.5 174.2,154.8 175.3,154.1 176.4,153.3 177.5,152.6 178.6,151.9 179.7,151.2 180.8,150.4 181.9,149.7 182.9,149.0 184.0,148.3 185.1,147.5 186.2,146.8 187.3,146.1 188.4,145.4 189.5,144.6 190.6,143.9 191.7,143.2 192.8,142.5 193.8,141.7 194.9,141.0 196.0,140.3 197.1,139.6 198.2,138.8 199.3,138.1 200.4,137.4 201.5,136.7 202.6,135.9 203.7,135.2 204.7,134.5 205.8,133.8 206.9,133.0 208.0,132.3 209.1,131.6 210.2,130.9 211.3,130.1 212.4,129.4 213.5,128.7 214.6,128.0 215.6,127.2 216.7,126.5 217.8,125.8 218.9,125.1 220.0,124.3 221.1,123.6 222.2,122.9 223.3,122.2 224.4,121.4 225.4,120.7 226.5,120.0 227.6,119.3 228.7,118.6 229.8,117.8 230.9,117.1 232.0,116.4 233.1,115.7 234.2,114.9 235.3,114.2 236.3,113.5 237.4,112.8 238.5,112.0 239.6,111.3 240.7,110.6 241.8,109.9 242.9,109.1 244.0,108.4 245.1,107.7 246.2,107.0 247.2,106.2 248.3,105.5 249.4,104.8 250.5,104.1 251.6,103.3 252.7,102.6 253.8,101.9 254.9,101.2 256.0,100.4 257.1,99.7 258.1,99.0 259.2,98.3 260.3,97.5 261.4,96.8 262.5,96.1 263.6,95.4 264.7,94.6 265.8,93.9 266.9,93.2 267.9,92.5 269.0,91.7 270.1,91.0 271.2,90.3 272.3,89.6 273.4,88.8 274.5,88.1 275.6,87.4 276.7,86.7 277.8,85.9 278.8,85.2 279.9,84.5 281.0,83.8 282.1,83.0 283.2,82.3 284.3,81.6 285.4,80.9 286.5,80.1 287.6,79.4 288.7,78.7 289.7,78.0 290.8,77.2 291.9,76.5 293.0,75.8 294.1,75.1 295.2,74.3 296.3,73.6 297.4,72.9 298.5,72.2 299.6,71.4 300.6,70.7 301.7,70.0 302.8,69.3 303.9,68.6 305.0,67.8 306.1,67.1 307.2,66.4 308.3,65.7 309.4,64.9 310.4,64.2 311.5,63.5 312.6,62.8 313.7,62.0 314.8,61.3 315.9,60.6 317.0,59.9 318.1,59.1 319.2,58.4 320.3,57.7 321.3,57.0 322.4,56.2 323.5,55.5 324.6,54.8 325.7,54.1 326.8,53.3 327.9,52.6 329.0,51.9 330.1,51.2 331.2,50.4 332.2,49.7 333.3,49.0 334.4,48.3 335.5,47.5 336.6,46.8 337.7,46.1"/><line class="curve3" stroke-dasharray="5 4" x1="337.7" y1="220.0" x2="337.7" y2="46.1"/><text class="ink" x="193.8" y="120.0" font-size="12" text-anchor="end">f(x) = 2x</text><text class="ink" x="264.5" y="189.6" font-size="10" text-anchor="middle">P(0,5 ≤ X ≤ 1) = 0,75</text><text class="dim" x="89.2" y="33.0" font-size="10" text-anchor="start">toplam alan 1</text></svg>
  <figcaption>[0, 1] aralığında f(x) = 2x yoğunluğu: büyük değerler daha olası. Eğrinin altındaki toplam alan 1 (bir üçgen: ½ · 1 · 2). 0,5 ile 1 arasındaki gölgeli alan 0,75.</figcaption>
</figure>

$P(0{,}5 \leq X \leq 1) = \int_{0{,}5}^{1} 2x \, dx = \big[x^2\big]_{0{,}5}^{1} = 1 - 0{,}25 = 0{,}75$.

Beklenen değer ve varyans toplam yerine integralle yazılır:

$$
E[X] = \int x \, f(x) \, dx \qquad \operatorname{Var}(X) = \int x^2 f(x) \, dx - \mu^2
$$

$f(x) = 2x$ için $E[X] = \int_0^1 2x^2 \, dx = \frac{2}{3}$,
$E[X^2] = \int_0^1 2x^3 \, dx = \frac{1}{2}$, varyans
$\frac{1}{2} - \frac{4}{9} = \frac{1}{18}$.

**Tekdüze dağılım.** $[0, 1]$'de her yere eşit yoğunluk, $f(x) = 1$:
$E[X] = \frac{1}{2}$, $\operatorname{Var}(X) = \frac{1}{3} - \frac{1}{4} =
\frac{1}{12}$. Bilgisayarların "rastgele sayı" üreticisi budur.

**Yoğunluk olasılık değil.** $f(x)$ $1$'den büyük olabilir ($f(1) = 2$);
olasılık yalnızca alan olarak okunur.

## Makine öğrenmesinde beklenen değer

**Beklenen kayıp.** Bir modelin gerçek başarısı, bütün olası veriler
üzerindeki **beklenen kayıp** (risk). Onu bilemediğimiz için eğitim
verisindeki ortalama kaybı küçültürüz; bu, beklenen değerin örneklem
ortalamasıyla tahmini.

**Stokastik gradyan.** Mini-yığından hesaplanan gradyan rastgele bir
değişken; beklenen değeri bütün verinin gradyanına eşit (yansız tahmin).
Yığın büyüdükçe varyansı $\frac{1}{n}$ ile azalır: büyük yığın daha düzgün
adım, küçük yığın daha gürültülü ama ucuz adım.

**Dropout.** Eğitimde her nöron $p$ olasılıkla açık tutulur ve açıksa
çıkışı $\frac{1}{p}$ ile büyütülür. Çıkış $a$ ise beklenen değer
$p \cdot \frac{a}{p} + (1 - p) \cdot 0 = a$: test sırasında hiçbir şey
kapatılmadığında ölçek bozulmaz.

**Yanlılık ve varyans.** Bir modelin hatası iki kaynaktan gelir: tahminin
beklenen değerinin gerçekten uzaklığı (yanlılık) ve farklı eğitim
verilerinde tahminin dalgalanması (varyans). Basit modeller yanlı, karmaşık
modeller değişken olur.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$E[X^2] = (E[X])^2$</p>
      <p>$\operatorname{Var}(2X) = 2 \operatorname{Var}(X)$</p>
      <p>$\operatorname{Var}(X - Y) = \operatorname{Var}(X) - \operatorname{Var}(Y)$</p>
      <p>$f(x)$ bir olasılıktır</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>aradaki fark varyans: $E[X^2] - \mu^2$</p>
      <p>$\operatorname{Var}(2X) = 4 \operatorname{Var}(X)$</p>
      <p>bağımsızsa $\operatorname{Var}(X) + \operatorname{Var}(Y)$</p>
      <p>olasılık alan: $\int_a^b f(x) \, dx$</p>
    </div>
  </div>
  <figcaption>Beklenen değer doğrusal; varyans karelerle çalıştığı için çarpanın karesini alır ve farkta bile toplanır.</figcaption>
</figure>

- **Beklenen değeri "en olası değer" sanmak.** Zarın beklenen değeri
  $3{,}5$ ama zar onu hiç göstermez.
- **Bağımlı değişkenlerin varyansını toplamak.** Kural yalnızca
  bağımsızlıkta geçerli; aksi hâlde kovaryans terimi eklenir (Kovaryans ve
  Korelasyon bölümü).

## Özet

- Rastgele değişken sonucu sayıya çevirir; kesikli ya da sürekli.
- Kesikli: $p(x)$, $\sum p(x) = 1$; sürekli: $f(x)$, olasılık alan.
- $E[X] = \sum x p(x)$ ya da $\int x f(x) dx$; uzun vadeli ortalama.
- $E[aX + b] = aE[X] + b$, $E[X + Y] = E[X] + E[Y]$ her zaman.
- $\operatorname{Var}(X) = E[X^2] - \mu^2$; $\operatorname{Var}(aX + b) =
  a^2 \operatorname{Var}(X)$; bağımsızsa varyanslar toplanır.
- $n$ gözlemin ortalamasının varyansı $\frac{\sigma^2}{n}$.
- Beklenen kayıp, stokastik gradyan, dropout ve yanlılık–varyans birer
  beklenen değer hikâyesi.
