# Vektörler

Makine öğrenmesinde veri neredeyse her zaman **vektör** olarak durur. Bir
evin metrekaresi, oda sayısı ve yaşı üç sayıdır; bunları yan yana
yazınca tek bir nesne olur: $(120,\ 3,\ 10)$. Bir fotoğraf binlerce piksel
değerinden oluşan bir vektör, bir kelime yüzlerce sayılık bir vektör, bir
modelin öğrendiği ağırlıklar da bir vektör.

MAT 2'nin ilk konusu bu yüzden vektörler. Bu bölümde vektörün ne olduğunu,
nasıl yazıldığını, nasıl toplanıp ölçeklendiğini ve uzunluğunun nasıl
bulunduğunu göreceksin. Bir sonraki bölümde (Nokta Çarpımı) iki vektörün
birbirine ne kadar benzediğini ölçmeyi öğreneceğiz.

Başlamadan önce MAT 1'den üç şey gerekiyor: **koordinat düzlemi** (bir
noktanın $(x, y)$ ile yazılması), **Pisagor teoremi** ($a^2 + b^2 = c^2$)
ve **karekök**. Hepsini yeri geldikçe hatırlatacağım.

## Skaler ve vektör

Bazı büyüklükleri tek bir sayı anlatır. Oda sıcaklığı 22 derece, bir
kutunun kütlesi 3 kilogram, bir evin fiyatı 4 milyon lira. Bunlara
**skaler** denir: yalnızca bir **büyüklük** taşırlar.

Bazı büyüklükler için tek sayı yetmez. "Rüzgar saatte 20 kilometre hızla
esiyor" cümlesi eksik: **nereye** doğru? Kuzeye mi, doğuya mı? Hız, kuvvet,
yer değiştirme gibi büyüklüklerin hem bir **büyüklüğü** hem de bir **yönü**
vardır. Bunlara **vektör** denir.

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Skaler</h4>
      <p>Tek sayı. Yalnızca "ne kadar".</p>
      <p>Sıcaklık: 22°<br>Kütle: 3 kg<br>Fiyat: 4 milyon</p>
    </div>
    <div>
      <h4>Vektör</h4>
      <p>Sıralı sayılar. "Ne kadar" ve "nereye".</p>
      <p>Rüzgar: doğuya 3, kuzeye 4<br>Konum: $(2, 5)$<br>Ev: $(120, 3, 10)$</p>
    </div>
  </div>
  <figcaption>Skaler tek bir sayı; vektör sırası önemli olan bir sayı listesi.</figcaption>
</figure>

## Vektörü yazmak

Düzlemde bir vektör **iki sayıyla** yazılır: yatay yönde ne kadar gittiği
ve dikey yönde ne kadar gittiği. Bu sayılara vektörün **bileşenleri**
denir.

$$
\mathbf{v} = (3,\ 4)
$$

Burada birinci bileşen $v_1 = 3$ (sağa 3 birim), ikinci bileşen $v_2 = 4$
(yukarı 4 birim). Vektörleri sıradan sayılardan ayırmak için kalın harfle
($\mathbf{v}$) ya da üstüne ok koyarak ($\vec{v}$) yazarız. Kâğıtta elle
yazarken ok daha pratik.

Aynı vektör dikey olarak da yazılabilir; buna **sütun vektör** denir ve
MAT 2'nin ilerleyen bölümlerinde, matrislerle çalışırken bu yazılış
kullanılacak:

$$
\mathbf{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

İki yazılış aynı vektörü anlatıyor; fark yalnızca kâğıttaki yerleşim.

### Ok olarak çizmek

Vektör bir **ok** olarak çizilir. Ok başlangıç noktasından ($0, 0$) çıkar,
sağa 3 ve yukarı 4 gidip $(3, 4)$ noktasında biter:

<figure class="fig">
<svg viewBox="0 0 332 292" width="332"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="306" y1="266" x2="306" y2="26"/><line class="grid" x1="26" y1="266" x2="306" y2="266"/><line class="line" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="240" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve2" stroke-dasharray="5 4" x1="66" y1="226" x2="186" y2="226"/><line class="curve2" stroke-dasharray="5 4" x1="186" y1="226" x2="186" y2="66"/><line class="curve" x1="66" y1="226" x2="180.7" y2="73.0"/><polygon class="dot" points="186,66 183.6,76.7 176.4,71.3"/><text class="ink" x="126.0" y="220" font-size="13" text-anchor="middle">3</text><text class="ink" x="192" y="146" font-size="13" text-anchor="start">4</text><text class="ink" x="110.0" y="130.0" font-size="14" text-anchor="end">v = (3, 4)</text></svg>
  <figcaption>Mor ok $\mathbf{v} = (3, 4)$. Turuncu kesik çizgiler bileşenleri: önce sağa 3, sonra yukarı 4.</figcaption>
</figure>

Okun iki özelliği var:

- **Yönü:** okun gösterdiği taraf.
- **Uzunluğu (büyüklüğü):** okun boyu. Aşağıda Pisagor ile hesaplayacağız.

### Sıra önemlidir

$(3, 4)$ ile $(4, 3)$ **farklı** vektörlerdir: biri "sağa 3, yukarı 4",
öteki "sağa 4, yukarı 3". Vektör bir **küme** değil, **sıralı** bir
listedir. Ev örneğinde $(120, 3, 10)$ "120 metrekare, 3 oda, 10 yaşında"
demek; sırayı karıştırmak 3 metrekarelik, 120 odalı bir ev yaratır.

## Ok mu, liste mi?

Vektöre iki gözle bakılabilir ve ikisi de doğru:

1. **Geometrik bakış:** vektör bir ok; yönü ve uzunluğu var.
2. **Sayısal bakış:** vektör sıralı bir sayı listesi.

Düzlemde (2 boyut) ve uzayda (3 boyut) ikisi birbirine çevrilebilir: her
ok bir liste, her liste bir ok. Ama makine öğrenmesinde vektörler çoğu
zaman **çok daha fazla** sayı taşır:

- Bir ev: $(120,\ 3,\ 10,\ 2,\ 1)$ — metrekare, oda, yaş, kat, otopark. **5 boyut.**
- 28 × 28 piksellik siyah-beyaz bir resim: **784 boyut.**
- Bir dil modelindeki bir kelime: çoğu zaman **yüzlerce boyut.**

784 boyutlu bir oku çizemeyiz. Ama işin güzel yanı şu: bu bölümde
öğreneceğin **bütün kurallar** (toplama, ölçekleme, uzunluk) 2 boyutta
nasıl çalışıyorsa 784 boyutta da aynen öyle çalışıyor. 2 boyutta çizerek
anlıyoruz, sonra aynı hesabı istediğimiz kadar sayıya uyguluyoruz.

$n$ tane gerçek sayıdan oluşan vektörlerin kümesi $\mathbb{R}^n$ ile
gösterilir. $\mathbb{R}^2$ düzlem, $\mathbb{R}^3$ uzay; ev vektörü
$\mathbb{R}^5$'in bir elemanı.

## İki noktadan vektör

Başlangıcı orijin olmayan bir ok da bir vektördür. $A(1, 1)$ noktasından
$B(4, 5)$ noktasına giden ok, "sağa 3, yukarı 4" gidiyor. Bu vektör
$\overrightarrow{AB}$ ile yazılır ve **bitiş eksi başlangıç** ile bulunur:

$$
\overrightarrow{AB} = B - A = (4 - 1,\ 5 - 1) = (3,\ 4)
$$

<figure class="fig">
<svg viewBox="0 0 332 332" width="332"><line class="grid" x1="26" y1="306" x2="26" y2="26"/><line class="line" x1="66" y1="306" x2="66" y2="26"/><line class="grid" x1="106" y1="306" x2="106" y2="26"/><line class="grid" x1="146" y1="306" x2="146" y2="26"/><line class="grid" x1="186" y1="306" x2="186" y2="26"/><line class="grid" x1="226" y1="306" x2="226" y2="26"/><line class="grid" x1="266" y1="306" x2="266" y2="26"/><line class="grid" x1="306" y1="306" x2="306" y2="26"/><line class="grid" x1="26" y1="306" x2="306" y2="306"/><line class="line" x1="26" y1="266" x2="306" y2="266"/><line class="grid" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="280" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="280" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="280" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="280" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="280" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="280" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="280" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="310" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="230" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">5</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">6</text><line class="curve3" stroke-dasharray="5 4" x1="66" y1="266" x2="186" y2="106"/><circle class="dot2" cx="106" cy="226" r="4"/><circle class="dot2" cx="226" cy="66" r="4"/><line class="curve" x1="106" y1="226" x2="220.7" y2="73.0"/><polygon class="dot" points="226,66 223.6,76.7 216.4,71.3"/><text class="ink" x="114" y="240" font-size="13" text-anchor="start">A(1, 1)</text><text class="ink" x="234" y="70" font-size="13" text-anchor="start">B(4, 5)</text><text class="dim" x="122.0" y="162.0" font-size="12" text-anchor="end">(3, 4)</text></svg>
  <figcaption>$A$'dan $B$'ye giden mor ok ile orijinden çizilen kesik ok aynı vektör: ikisi de $(3, 4)$.</figcaption>
</figure>

Buradan önemli bir gerçek çıkıyor: **vektörün nerede durduğu önemli
değil.** Aynı yöne bakan, aynı uzunluktaki iki ok aynı vektördür. Bir
vektörü düzlemde kaydırırsan değişmez; yalnızca **yönü ve uzunluğu**
vektörü belirler.

Sıraya dikkat: $\overrightarrow{BA} = A - B = (-3, -4)$. Aynı uzunlukta ama
tam ters yönde bir ok. "Nereden nereye" sorusunun cevabı işaretleri
değiştiriyor.

## Toplama

İki vektör **bileşen bileşen** toplanır:

$$
\mathbf{v} + \mathbf{w} = (v_1 + w_1,\ v_2 + w_2)
$$

**Örnek:** $\mathbf{v} = (4, 1)$ ve $\mathbf{w} = (1, 3)$ ise
$\mathbf{v} + \mathbf{w} = (4 + 1,\ 1 + 3) = (5, 4)$.

Geometrik anlamı çok doğal: önce $\mathbf{v}$ kadar yürü, sonra
bulunduğun yerden $\mathbf{w}$ kadar yürü. Vardığın yer $\mathbf{v} + \mathbf{w}$.

<figure class="fig">
<svg viewBox="0 0 332 292" width="332"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="306" y1="266" x2="306" y2="26"/><line class="grid" x1="26" y1="266" x2="306" y2="266"/><line class="line" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="240" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve3" stroke-dasharray="5 4" x1="66" y1="226" x2="106" y2="106"/><line class="curve3" stroke-dasharray="5 4" x1="106" y1="106" x2="266" y2="66"/><line class="curve" x1="66" y1="226" x2="217.5" y2="188.1"/><polygon class="dot" points="226,186 217.3,192.8 215.2,184.1"/><line class="curve2" x1="226" y1="186" x2="263.2" y2="74.3"/><polygon class="dot2" points="266,66 267.1,76.9 258.6,74.1"/><line class="curve4" x1="66" y1="226" x2="259.1" y2="71.5"/><polygon class="dot3" points="266,66 261.0,75.8 255.4,68.8"/><text class="ink" x="154.0" y="220.0" font-size="14" text-anchor="middle">v</text><text class="ink" x="254.0" y="126.0" font-size="14" text-anchor="start">w</text><text class="ink" x="152.0" y="138.0" font-size="14" text-anchor="end">v + w</text></svg>
  <figcaption>Mor $\mathbf{v}$'nin ucundan turuncu $\mathbf{w}$ çiziliyor; yeşil ok başlangıçtan son noktaya gidiyor: $\mathbf{v} + \mathbf{w} = (5, 4)$. Kesik çizgiler ters sırayı gösteriyor (önce $\mathbf{w}$, sonra $\mathbf{v}$): aynı noktaya varılıyor.</figcaption>
</figure>

Buna **uç uca ekleme** (ya da üçgen kuralı) denir. Kesik çizgilerle
tamamlanan şekil bir **paralelkenar**; toplam vektör onun köşegeni.

Toplamanın özellikleri, sayılardaki toplamayla aynı:

- **Değişme:** $\mathbf{v} + \mathbf{w} = \mathbf{w} + \mathbf{v}$ (şekildeki iki yol aynı yere varıyor).
- **Birleşme:** $(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$.
- **Sıfır vektörü:** $\mathbf{0} = (0, 0)$; $\mathbf{v} + \mathbf{0} = \mathbf{v}$. Hiç yürümemek.

**Aynı boyuttaki vektörler toplanır.** $(1, 2)$ ile $(1, 2, 3)$'ü toplamak
tanımsız: üçüncü bileşenin eşi yok. Evi $(120, 3, 10)$ olarak yazıp bir
başkasını $(100, 4)$ olarak yazarsan toplayamazsın; ikisi farklı şeyleri
anlatıyor.

## Çıkarma

Çıkarma da bileşen bileşen:

$$
\mathbf{v} - \mathbf{w} = (v_1 - w_1,\ v_2 - w_2)
$$

$(4, 1) - (1, 3) = (3, -2)$.

Anlamı: $\mathbf{v} - \mathbf{w}$, **$\mathbf{w}$'nin ucundan
$\mathbf{v}$'nin ucuna** giden vektör. "İki nokta arasındaki vektör"
kuralının aynısı: bitiş eksi başlangıç.

Makine öğrenmesinde fark vektörü çok sık kullanılır: iki müşteri, iki ev
ya da iki resim arasındaki fark bir vektördür. Farkın **uzunluğu** da
ikisinin birbirine ne kadar uzak olduğunu söyler; birazdan göreceğiz.

## Skalerle çarpma

Bir vektörü bir sayıyla (skalerle) çarpmak, her bileşeni o sayıyla
çarpmak demektir:

$$
c \cdot \mathbf{v} = (c\, v_1,\ c\, v_2)
$$

<figure class="fig">
<svg viewBox="0 0 372 252" width="372"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="grid" x1="66" y1="226" x2="66" y2="26"/><line class="grid" x1="106" y1="226" x2="106" y2="26"/><line class="line" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="266" y1="226" x2="266" y2="26"/><line class="grid" x1="306" y1="226" x2="306" y2="26"/><line class="grid" x1="346" y1="226" x2="346" y2="26"/><line class="grid" x1="26" y1="226" x2="346" y2="226"/><line class="grid" x1="26" y1="186" x2="346" y2="186"/><line class="line" x1="26" y1="146" x2="346" y2="146"/><line class="grid" x1="26" y1="106" x2="346" y2="106"/><line class="grid" x1="26" y1="66" x2="346" y2="66"/><line class="grid" x1="26" y1="26" x2="346" y2="26"/><text class="dim" x="26" y="160" font-size="10" text-anchor="middle">-3</text><text class="dim" x="66" y="160" font-size="10" text-anchor="middle">-2</text><text class="dim" x="106" y="160" font-size="10" text-anchor="middle">-1</text><text class="dim" x="186" y="160" font-size="10" text-anchor="middle">1</text><text class="dim" x="226" y="160" font-size="10" text-anchor="middle">2</text><text class="dim" x="266" y="160" font-size="10" text-anchor="middle">3</text><text class="dim" x="306" y="160" font-size="10" text-anchor="middle">4</text><text class="dim" x="346" y="160" font-size="10" text-anchor="middle">5</text><text class="dim" x="140" y="230" font-size="10" text-anchor="end">-2</text><text class="dim" x="140" y="190" font-size="10" text-anchor="end">-1</text><text class="dim" x="140" y="110" font-size="10" text-anchor="end">1</text><text class="dim" x="140" y="70" font-size="10" text-anchor="end">2</text><text class="dim" x="140" y="30" font-size="10" text-anchor="end">3</text><line class="curve2" x1="146" y1="146" x2="298.1" y2="69.9"/><polygon class="dot2" points="306,66 299.0,74.5 295.0,66.5"/><line class="curve" x1="146" y1="146" x2="218.1" y2="109.9"/><polygon class="dot" points="226,106 219.0,114.5 215.0,106.5"/><line class="curve4" x1="146" y1="146" x2="73.9" y2="182.1"/><polygon class="dot3" points="66,186 73.0,177.5 77.0,185.5"/><text class="ink" x="230" y="98" font-size="14" text-anchor="start">v</text><text class="ink" x="310" y="60" font-size="14" text-anchor="start">2v</text><text class="ink" x="60" y="190" font-size="14" text-anchor="end">−v</text></svg>
  <figcaption>Mor $\mathbf{v} = (2, 1)$. Turuncu $2\mathbf{v} = (4, 2)$: aynı yön, iki kat uzun. Yeşil $-\mathbf{v} = (-2, -1)$: aynı uzunluk, ters yön.</figcaption>
</figure>

Skalerin değerine göre dört durum var:

| Skaler | Etkisi | Örnek ($\mathbf{v} = (2, 1)$) |
|---|---|---|
| $c > 1$ | Aynı yön, uzar | $2\mathbf{v} = (4, 2)$ |
| $0 < c < 1$ | Aynı yön, kısalır | $0.5\,\mathbf{v} = (1, 0.5)$ |
| $c = 0$ | Sıfır vektörü | $0\,\mathbf{v} = (0, 0)$ |
| $c < 0$ | **Yön tersine döner** | $-\mathbf{v} = (-2, -1)$ |

Skalerle çarpma **yönü değiştirmez**, yalnızca ya korur ya tam tersine
çevirir. Adı da buradan geliyor: "scale", ölçeklemek.

Çıkarma aslında toplama ile skalerle çarpmanın birleşimi:
$\mathbf{v} - \mathbf{w} = \mathbf{v} + (-1)\,\mathbf{w}$.

## Doğrusal kombinasyon

Toplama ile skalerle çarpmayı birleştirince vektör cebirinin en önemli
işlemi çıkıyor:

$$
a\,\mathbf{v} + b\,\mathbf{w}
$$

Buna $\mathbf{v}$ ile $\mathbf{w}$'nin **doğrusal kombinasyonu** denir.
$a$ ve $b$ sayılarına **katsayı** denir.

**Örnek:** $\mathbf{v} = (1, 2)$, $\mathbf{w} = (3, 1)$ ve $a = 2$, $b = -1$:

$$
2\,(1, 2) + (-1)\,(3, 1) = (2, 4) + (-3, -1) = (-1, 3)
$$

Günlük bir örnek: bir kafe iki tür karışım satıyor. Karışım A'nın bir
paketinde 1 birim kahve, 2 birim süt var: $(1, 2)$. Karışım B'de 3 birim
kahve, 1 birim süt: $(3, 1)$. 2 paket A ile 1 paket B aldığında toplam
kahve ve süt: $2(1, 2) + 1(3, 1) = (5, 5)$.

### Birim vektörlerle yazmak

Düzlemde iki özel vektör var:

$$
\mathbf{i} = (1, 0) \qquad \mathbf{j} = (0, 1)
$$

Biri sağa bir birim, öteki yukarı bir birim. **Her** vektör bunların
doğrusal kombinasyonu olarak yazılabilir:

$$
(3, 4) = 3\,(1, 0) + 4\,(0, 1) = 3\,\mathbf{i} + 4\,\mathbf{j}
$$

Bileşenler, aslında bu iki temel yönde kaç adım atıldığının sayısıdır.
MAT 2'nin ilerisinde (Doğrusal Bağımsızlık, Taban ve Rank) bu fikir
"taban" adıyla genelleşecek.

Makine öğrenmesinde doğrusal kombinasyon her yerde: bir doğrusal model
tahminini özelliklerin ağırlıklı toplamı olarak yapıyor. Ev fiyatı
$= w_1 \cdot \text{metrekare} + w_2 \cdot \text{oda} + w_3 \cdot \text{yaş} + b$.
Modelin öğrendiği şey, bu $w$ katsayıları.

## Uzunluk (büyüklük)

Bir vektörün uzunluğu **Pisagor teoremiyle** bulunur. $\mathbf{v} = (3, 4)$
okunu düşün: yatayda 3, dikeyde 4 giden bir dik üçgenin hipotenüsü.

$$
\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2} = \sqrt{3^2 + 4^2} = \sqrt{25} = 5
$$

$\|\mathbf{v}\|$ yazılışı "v'nin uzunluğu" (ya da **normu**) diye okunur.
Tek çizgiyle yazılan $|x|$ sayının mutlak değeriydi; çift çizgi vektörün
uzunluğu. Fikir aynı: "işaretten bağımsız olarak ne kadar büyük".

Üç boyutta bir bileşen daha ekleniyor:

$$
\|(2, -1, 2)\| = \sqrt{2^2 + (-1)^2 + 2^2} = \sqrt{9} = 3
$$

Genel formül, $n$ boyut için:

$$
\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2} = \sqrt{\sum_{i=1}^{n} v_i^2}
$$

Uzunluğun üç özelliği:

- **Hiç negatif değildir**; yalnızca sıfır vektörünün uzunluğu $0$.
- **Skaler dışarı çıkar:** $\|c\,\mathbf{v}\| = |c|\,\|\mathbf{v}\|$. $\|{-2}\,(3, 4)\| = 2 \cdot 5 = 10$.
- **Üçgen eşitsizliği:** $\|\mathbf{v} + \mathbf{w}\| \le \|\mathbf{v}\| + \|\mathbf{w}\|$. Toplamın uzunluğu, uzunlukların toplamından **büyük olamaz**.

Üçgen eşitsizliği şekilden okunuyor: toplama şeklindeki yeşil ok üçgenin
bir kenarı, $\mathbf{v}$ ve $\mathbf{w}$ öteki iki kenarı. Bir kenar
hiçbir zaman öteki ikisinin toplamından uzun olamaz. Sayılarla:
$\|(4, 1)\| + \|(1, 3)\| \approx 4.12 + 3.16 = 7.28$, ama
$\|(5, 4)\| \approx 6.40$.

## Birim vektör: yalnızca yön

Uzunluğu tam $1$ olan vektöre **birim vektör** denir. Herhangi bir
vektörü kendi uzunluğuna bölersen, aynı yönü gösteren birim vektörü
bulursun:

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}
$$

$\mathbf{v} = (3, 4)$ için $\|\mathbf{v}\| = 5$, dolayısıyla
$\hat{\mathbf{v}} = (3/5,\ 4/5) = (0.6,\ 0.8)$. Sağlama:
$\sqrt{0.6^2 + 0.8^2} = \sqrt{0.36 + 0.64} = 1$.

Bu işleme **normalleştirme** denir. Birim vektör "yalnızca yön" bilgisini
taşır; uzunluk bilgisini atar. Metin benzerliğinde iki belgeyi
karşılaştırırken bu çok işe yarar: uzun bir belge ile kısa bir belge aynı
konudan bahsediyorsa, uzunluklarını atıp yalnızca yönlerine bakmak
gerekir (bir sonraki bölümde).

Sıfır vektörünün birim vektörü **yoktur**: uzunluğu $0$ ve sıfıra
bölünemez. Zaten bir yönü de yok.

## İki nokta arasındaki uzaklık

İki nokta arasındaki uzaklık, aralarındaki fark vektörünün uzunluğudur:

$$
d(\mathbf{a}, \mathbf{b}) = \|\mathbf{b} - \mathbf{a}\|
$$

$P(2, 3)$ ile $Q(5, 7)$ arasında: $Q - P = (3, 4)$, uzunluğu $5$.

Buna **Öklid uzaklığı** denir ve makine öğrenmesinin en temel
araçlarından biridir. En yakın komşu (KNN) algoritması, yeni bir noktaya
en yakın örnekleri bu uzaklıkla bulur.

### Ölçek tuzağı

İki evi düşün: $\mathbf{a} = (120, 3, 10)$ ve $\mathbf{b} = (100, 4, 12)$
(metrekare, oda, yaş).

$$
\mathbf{a} - \mathbf{b} = (20, -1, -2) \qquad
\|\mathbf{a} - \mathbf{b}\| = \sqrt{400 + 1 + 4} = \sqrt{405} \approx 20.12
$$

Uzaklığın neredeyse tamamı metrekareden geliyor ($400$'ün yanında $1$ ve
$4$ önemsiz). Metrekare yüzlerle, oda sayısı birlerle ölçüldüğü için
metrekare uzaklığı **ezip geçiyor**. Metrekareyi yüz metrekare biriminde
yazsaydık ($1.20$ ve $1.00$) uzaklık $\approx 2.24$ olurdu ve oda ile yaş
farkı belirleyici hâle gelirdi.

Bu matematiksel bir gerçek: **uzaklık, bileşenlerin ölçeğine bağlıdır.**
Makine öğrenmesinde özellikleri ölçeklendirmenin (standartlaştırma)
sebebi tam olarak bu.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$\|\mathbf{v} + \mathbf{w}\| = \|\mathbf{v}\| + \|\mathbf{w}\|$</p>
      <p>$\|(3, 4)\| = 3 + 4 = 7$</p>
      <p>$\overrightarrow{AB} = A - B$</p>
      <p>$(1, 2) + 5 = (6, 7)$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>$\|\mathbf{v} + \mathbf{w}\| \le \|\mathbf{v}\| + \|\mathbf{w}\|$</p>
      <p>$\|(3, 4)\| = \sqrt{9 + 16} = 5$</p>
      <p>$\overrightarrow{AB} = B - A$</p>
      <p>Vektör ile sayı toplanmaz; $5\,(1, 2) = (5, 10)$ çarpılır</p>
    </div>
  </div>
  <figcaption>Uzunluk bileşenlerin toplamı değil, karelerinin toplamının karekökü.</figcaption>
</figure>

- **Uzunluğu bileşenleri toplayarak bulmak.** $(3, 4)$'ün uzunluğu $7$
  değil $5$: kuş uçuşu mesafe, önce sağa sonra yukarı yürünen yoldan kısa.
- **Negatif bileşenin karesini yanlış almak.** $(-3)^2 = 9$, $-9$ değil.
  Uzunluk bu yüzden hiç negatif çıkmıyor.
- **Farklı boyutlu vektörleri toplamak.** Tanımsız.
- **Vektöre sayı eklemek.** Vektörle sayı toplanmaz; ancak çarpılır.

## Özet

- Vektör, sırası önemli bir sayı listesi; aynı zamanda yönü ve uzunluğu
  olan bir ok. $\mathbb{R}^n$, $n$ sayılık vektörlerin kümesi.
- İki noktadan vektör: **bitiş eksi başlangıç**. Vektör kaydırılınca değişmez.
- Toplama ve çıkarma bileşen bileşen; geometride uç uca ekleme.
- Skalerle çarpma her bileşeni çarpar; yönü korur ya da (negatifse) ters çevirir.
- Doğrusal kombinasyon $a\,\mathbf{v} + b\,\mathbf{w}$: doğrusal modellerin temeli.
- Uzunluk $\|\mathbf{v}\| = \sqrt{\sum v_i^2}$ (Pisagor); birim vektör $\mathbf{v}/\|\mathbf{v}\|$.
- İki nokta arasındaki uzaklık fark vektörünün uzunluğu (Öklid uzaklığı);
  bileşenlerin ölçeğine bağlı.
