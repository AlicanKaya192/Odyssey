Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Basamaklar

| Basamak | Değeri | Örnek ($3{,}752$) |
|---|---|---|
| birler | $1$ | $3$ |
| onda birler | $\dfrac{1}{10}$ | $7$ |
| yüzde birler | $\dfrac{1}{100}$ | $5$ |
| binde birler | $\dfrac{1}{1\,000}$ | $2$ |

Türkçede ondalık ayıracı virgül ($3{,}75$), programlamada nokta (`3.75`).

## Sık kullanılan çeviriler

| Kesir | Ondalık |
|---|---|
| $\dfrac{1}{2}$ | $0{,}5$ |
| $\dfrac{1}{4}$ | $0{,}25$ |
| $\dfrac{3}{4}$ | $0{,}75$ |
| $\dfrac{1}{5}$ | $0{,}2$ |
| $\dfrac{1}{8}$ | $0{,}125$ |
| $\dfrac{1}{3}$ | $0{,}\overline{3}$ |
| $\dfrac{2}{3}$ | $0{,}\overline{6}$ |
| $\dfrac{1}{9}$ | $0{,}\overline{1}$ |

## Biter mi, devreder mi?

En sade kesrin paydası yalnızca $2$ ve $5$ çarpanlarından oluşuyorsa
ondalık biter; başka bir asal çarpan varsa devreder.

**Devirli → kesir:** $x = 0{,}\overline{ab}$ ise $100x - x = ab$, yani
$x = \dfrac{ab}{99}$. Bir basamak devrediyorsa $10x - x$ ve payda $9$.

## İşlemler

| İşlem | Kural |
|---|---|
| Toplama, çıkarma | virgülleri hizala |
| Çarpma | tam sayı gibi çarp; virgülden sonraki basamak sayılarını topla |
| Bölme | iki sayının virgülünü aynı miktar kaydır, bölen tam sayı olsun |
| $\cdot 10^k$ | virgül $k$ basamak sağa |
| $\div 10^k$ | virgül $k$ basamak sola |

## Yuvarlama

Yuvarlanacak basamağın sağındaki rakam:

- $0$–$4$ → aşağı (rakam aynı kalır)
- $5$–$9$ → yukarı (rakam $1$ artar, gerekirse taşır)

Tek seferde ve en sonda yuvarla.

## Pratik ipuçları

- Karşılaştırırken sağa sıfır ekleyerek basamakları eşitle.
- Çarpımın sonucunu kabaca kontrol et: $3{,}75 \cdot 0{,}4 \approx 4 \cdot 0{,}4 = 1{,}6$.
- $1$'den küçük bir sayıyla çarpmak küçültür, bölmek büyütür.
- Bilgisayarda ondalıkları `==` ile değil, farkın çok küçük olup olmadığıyla karşılaştır.
