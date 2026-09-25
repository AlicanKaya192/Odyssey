Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kavramlar

| Kavram | Anlamı |
|---|---|
| topluluk | ilgilenilen bütün birimler |
| örneklem | topluluktan seçilen $n$ birim |
| parametre | topluluğun sayısı ($\mu$, $\sigma$, $p$); bilinmez |
| istatistik | örneklemden hesaplanan ($\bar{x}$, $s$, $\hat{p}$) |
| örneklem dağılımı | bir istatistiğin örneklemden örnekleme dağılımı |
| standart hata | istatistiğin standart sapması |
| yansız | $E[\text{tahmin}] = \text{parametre}$ |

## Formüller

| Ne | Formül |
|---|---|
| ortalamanın beklenen değeri | $E[\bar{X}] = \mu$ |
| ortalamanın standart hatası | $\frac{\sigma}{\sqrt{n}}$ ($\sigma$ bilinmiyorsa $\frac{s}{\sqrt{n}}$) |
| oranın standart hatası | $\sqrt{\frac{p(1 - p)}{n}}$ |
| toplamın standart sapması | $\sigma\sqrt{n}$ |
| standartlaştırma | $Z = \dfrac{\bar{X} - \mu}{\sigma / \sqrt{n}}$ |

## Merkezi Limit Teoremi

$n$ büyükse (kabaca $n \geq 30$) $\bar{X} \approx \mathcal{N}\!\left(\mu,
\frac{\sigma^2}{n}\right)$; topluluğun biçimi önemli değil. Gözlemler
bağımsız olmalı.

## Pratik ipuçları

- Tek gözlem mi, ortalama mı soruluyor? Ortalamaysa standart sapmayı
  $\sqrt{n}$'ye böl.
- Hatayı $k$ kat küçültmek için $k^2$ kat veri.
- Yanlı örneklemde büyüklük işe yaramaz; önce seçim yöntemine bak.
- Toplam soruluyorsa ortalama $n\mu$, standart sapma $\sigma\sqrt{n}$.
