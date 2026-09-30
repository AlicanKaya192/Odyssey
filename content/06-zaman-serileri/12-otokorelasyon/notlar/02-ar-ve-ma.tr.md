Bölüm 17'deki ARIMA'nın iki yapı taşı. Burada yalnızca **sezgiyi** kuruyoruz:
her biri bir şoku nasıl taşıyor ve korelogramda nasıl görünüyor.

## Şok

İkisi de aynı ham maddeden yapılıyor: **beyaz gürültü** `e`. Her gün bağımsız,
öngörülemeyen bir sürpriz. AR ve MA, bu sürprizin sonraki günlere nasıl
yayıldığını anlatan iki farklı kural.

## AR: seri kendini hatırlıyor

$$y_t = \phi\, y_{t-1} + e_t$$

Bugün = dünün `φ` katı + bugünün şoku. `φ = 0.7` ile bir şokun izi:

| Gün | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Etki | 1 | 0.7 | 0.49 | 0.34 | 0.24 | 0.17 |

Hiçbir zaman tam sıfır olmuyor, ama her gün küçülüyor. ACF'nin şekli de bu:
$\rho_k = \phi^k$.

Örnekler: sıcaklık sapması (bugün sıcaksa yarın da büyük olasılıkla sıcak),
stok düzeyi, bir kuyruktaki bekleyen sayısı. **Durumun kendisi** taşınıyor.

`φ`'nin değeri:

- 0'a yakın: hafıza yok denecek kadar kısa.
- 1'e yakın: çok uzun hafıza; şoklar çok yavaş sönüyor.
- Tam 1: rastgele yürüyüş. Şok hiç sönmüyor; seri durağan değil.
- Eksi: seri bir yukarı bir aşağı gidiyor; ACF işaret değiştirerek sönüyor.

## MA: şok yankılanıyor

$$y_t = e_t + \theta\, e_{t-1}$$

Bugün = bugünün şoku + dünkü şokun `θ` katı. `θ = 0.7` ile bir şokun izi:

| Gün | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Etki | 1 | 0.7 | 0 | 0 |

Bir gün sonra hâlâ hissediliyor, iki gün sonra **tamamen** yok. ACF de 1.
gecikmeden sonra kesiliyor. 1. gecikmenin değeri:

$$\rho_1 = \frac{\theta}{1 + \theta^2} = \frac{0.7}{1.49} = 0.47$$

Örnekler: bir kampanyanın ertesi güne sarkan etkisi, bir teslimat gecikmesinin
ertesi günkü telafisi, ölçüm hatasının düzeltilmesi. **Olayın kendisi**
yankılanıyor, durum taşınmıyor.

## Üretip görmek

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
e = rng.normal(0, 1, 650)

ar = np.zeros(650)
for i in range(1, 650):
    ar[i] = 0.7 * ar[i - 1] + e[i]

ma = e[1:] + 0.7 * e[:-1]
```

İlk 50 değeri atmak iyi bir alışkanlık: AR serisi sıfırdan başladığı için
dengeye oturması zaman alıyor.

## Parmak izleri

| Süreç | ACF | PACF |
|---|---|---|
| AR(1), `φ > 0` | Artı, üstel sönüş | 1. gecikmede tek çubuk |
| AR(1), `φ < 0` | İşaret değiştirerek sönüş | 1. gecikmede tek eksi çubuk |
| AR(2) | Sönüş ya da sönen dalga | İlk iki gecikmede çubuk |
| MA(1), `θ > 0` | 1. gecikmede tek artı çubuk | İşaret değiştirerek sönüş |
| MA(1), `θ < 0` | 1. gecikmede tek eksi çubuk | Eksi, üstel sönüş |
| MA(2) | İlk iki gecikmede çubuk | Sönüş |
| ARMA(1, 1) | 1. gecikmeden sonra sönüş | 1. gecikmeden sonra sönüş |

## Neden ayna görüntüsü?

- AR'da bugün **yalnızca dünle** doğrudan bağlı (PACF tek çubuk), ama dün de
  evvelsi günle bağlı olduğu için zincir uzuyor (ACF uzun kuyruk).
- MA'da bugün ile iki gün öncesi **hiçbir ortak şok** paylaşmıyor (ACF
  kesiliyor). Ama seriyi kendi geçmiş değerleriyle açıklamaya çalışırsan çok
  sayıda gecikmeye ihtiyaç duyarsın (PACF uzun kuyruk).

## Mevsimsel yankı

Aynı iki fikir mevsim boyunda da geçerli. Günlük satışın mevsimsel farkında
7. gecikmede tek bir eksi çubuk (−0.41) vardı ve 14'te yoktu: bu, **mevsimsel
MA(1)** parmak izi. Geçen haftanın aynı günündeki sürpriz bu haftayı etkiliyor,
iki hafta öncesi etkilemiyor.

Bölüm 17'de bu dört sayıyı seçeceksin: `p` (AR), `q` (MA), `P` (mevsimsel AR),
`Q` (mevsimsel MA). Hepsini ACF ve PACF'den okuyacaksın.

## Hangisi "daha iyi"?

İkisi de aynı amaca hizmet ediyor: kısa dönem hafızayı birkaç sayıyla anlatmak.
Aynı seri çoğu zaman ikisiyle de yaklaşık olarak anlatılabilir (uzun bir AR,
kısa bir MA'ya benzer; tersi de). Seçim, **en az parametreyle** kalıntıyı beyaz
gürültüye çeviren model lehine yapılır.
