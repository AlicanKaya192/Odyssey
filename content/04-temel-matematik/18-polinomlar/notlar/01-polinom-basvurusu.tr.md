Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Parçalar

$P(x) = a_n x^n + \dots + a_1 x + a_0$

| Ad | Ne | $3x^4 - 2x^2 + x - 5$ |
|---|---|---|
| derece | en büyük kuvvet | $4$ |
| baş katsayı | $a_n$ | $3$ |
| sabit terim | $a_0 = P(0)$ | $-5$ |
| katsayılar toplamı | $P(1)$ | $-3$ |

Kuvvetler yalnızca $0, 1, 2, \dots$; $\frac{1}{x}$ ve $\sqrt{x}$ polinom
değil.

## İşlemler

| İşlem | Kural |
|---|---|
| toplama, çıkarma | benzer terimler; çıkarmada her işaret değişir |
| çarpma | her terim her terimle; $x^m \cdot x^n = x^{m+n}$ |
| çarpımın derecesi | derecelerin toplamı |
| toplamın derecesi | en fazla büyük olanınki |

## Bölme

$$
P(x) = B(x) \cdot Q(x) + K(x), \qquad \operatorname{der} K < \operatorname{der} B
$$

- Uzun bölme: baş terimi böl, bölenle çarp, çıkar, tekrarla.
- Eksik terimlere $0$ katsayı yaz.
- Sentetik bölme: bölen $(x - a)$; ilk katsayıyı indir, $a$ ile çarp,
  sonrakine ekle. Son sayı kalan.

## İki teorem

| Teorem | Söylediği |
|---|---|
| kalan | $(x - a)$'ya bölümden kalan $P(a)$ |
| çarpan | $P(a) = 0 \iff (x - a)$ çarpan |

$(x + 3)$ için $a = -3$.

## Kökler ve grafik

- $n$. derecenin en fazla $n$ gerçek kökü var.
- Tam sayı kök adayları: sabit terimin bölenleri (baş katsayı $1$ ise).
  Genelde $\pm \frac{p}{q}$: $p$ sabit terimi, $q$ baş katsayıyı böler.
- Tek derece: uçlar zıt yönde, en az bir kök kesin.
- Çift derece: uçlar aynı yönde.
- Tek katlı kök: eğri keser. Çift katlı kök: değip döner.

## Pratik ipuçları

- Önce standart biçime diz: derece ve baş katsayı ondan sonra okunur.
- Yalnızca kalan soruluyorsa bölme; $P(a)$'yı hesapla.
- Bir kök bulunca $(x - a)$'ya böl, kalan ikinci dereceyi çarpanlara ayır.
- Sonucu bir sayı koyarak sına: $x = 1$ ya da $x = 0$ en kolayları.
