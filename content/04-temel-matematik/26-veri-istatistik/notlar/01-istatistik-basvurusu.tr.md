Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Veri türleri

| Tür | Örnek | Anlamlı özet |
|---|---|---|
| sürekli | boy, fiyat | ortalama, ortanca, standart sapma |
| kesikli | çocuk sayısı | ortalama, ortanca, tepe değer |
| sırasız kategorik | şehir | tepe değer, sıklık tablosu |
| sıralı kategorik | beden | ortanca, tepe değer |

## Merkez

| Ölçü | Nasıl | Aykırıya duyarlı mı? |
|---|---|---|
| ortalama | $\bar{x} = \frac{1}{n} \sum x_i$ | evet |
| ortanca | sırala, ortadaki (çiftse iki ortadakinin ortalaması) | hayır |
| tepe değer | en sık değer | hayır |

## Yayılım

| Ölçü | Formül |
|---|---|
| açıklık | en büyük $-$ en küçük |
| varyans (topluluk) | $\sigma^2 = \frac{1}{n} \sum (x_i - \bar{x})^2$ |
| varyans (örneklem) | $s^2 = \frac{1}{n - 1} \sum (x_i - \bar{x})^2$ |
| standart sapma | varyansın karekökü |
| ÇAA | Ç3 $-$ Ç1 |

Çeyrekler (bu bölümdeki yöntem): ortanca veriyi ikiye böler; Ç1 alt
yarının, Ç3 üst yarının ortancası.

## Aykırı değer

Ç1 $- 1{,}5 \cdot$ ÇAA'dan küçük ya da Ç3 $+ 1{,}5 \cdot$ ÇAA'dan büyük
değerler aykırı.

## Ölçekleme

| Yöntem | Formül | Sonuç |
|---|---|---|
| z puanı | $z = \dfrac{x - \bar{x}}{\sigma}$ | ortalama $0$, standart sapma $1$ |
| min–maks | $x' = \dfrac{x - \min}{\max - \min}$ | $0$ ile $1$ arası |

Ölçekleme değerleri yalnızca eğitim verisinden hesaplanır.

## Pratik ipuçları

- Ortancadan önce mutlaka sırala.
- Sapmaların toplamı hep $0$: hesabını sınamak için kullan.
- Çarpık veride (maaş, fiyat) tipik değer için ortancaya bak.
- Standart sapma verinin biriminde; varyans birimin karesinde.
