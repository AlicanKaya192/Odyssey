# ARIMA

Üstel düzleştirme seriyi **bileşenleriyle** anlatıyordu: düzey, eğim, mevsim.
ARIMA başka bir yoldan gidiyor: seriyi **kendi geçmişiyle** anlatıyor. "Bugün,
dünün şu kadarı artı geçen haftanın sürprizinin bu kadarı."

Bunun için gereken her şeyi zaten biliyorsun. Bölüm 11'de seriyi
durağanlaştırdın; Bölüm 12'de hafızasını ACF ve PACF ile okudun ve AR ile MA'nın
parmak izlerini tanıdın. ARIMA bu iki bölümün bir modele dönüşmüş hâli.

## 1. Üç harf, üç sayı

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>AR · p</span><span>Otoregresif: bugün, son <code>p</code> değerin ağırlıklı toplamına bağlı.</span></div>
<div class="anat-row"><span>I · d</span><span>Fark: model seriyi <code>d</code> kez fark alarak durağanlaştırır, tahmini düzeye kendisi geri çevirir.</span></div>
<div class="anat-row"><span>MA · q</span><span>Hareketli ortalama: bugün, son <code>q</code> sürprizin (tahmin hatasının) ağırlıklı toplamına bağlı.</span></div>
</div>
<figcaption>Model <code>ARIMA(p, d, q)</code> diye yazılır. Üç sayıyı sen seçersin; katsayıları model bulur.</figcaption>
</figure>

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(train, order=(1, 0, 0)).fit()
```

## 2. AR: seri kendini hatırlıyor

En basit hâli AR(1): $y_t = c + \phi\,(y_{t-1} - c) + e_t$. Bugün, dünün
ortalamadan sapmasının `φ` katını taşıyor.

Sıcaklığın mevsim normalinden sapmasında (Bölüm 12'de PACF'si tek çubuktu):

```python
fit = ARIMA(anomaly, order=(1, 0, 0)).fit()
print(fit.params.round(3).to_dict())
# {'const': -0.005, 'ar.L1': 0.724, 'sigma2': 2.06}
```

`φ = 0.724`: bugünkü sapmanın %72'si yarına kalıyor. Son gün sapma +1.32
derece; tahmin:

```python
print(fit.forecast(5).round(2).tolist())     # [0.95, 0.69, 0.5, 0.36, 0.26]
```

Her gün 0.724 ile çarpılarak **ortalamaya dönüyor**: 1.32 × 0.724 = 0.95,
0.95 × 0.724 = 0.69...

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="212.8" x2="666" y2="212.8"/><text class="dim" x="38" y="216.3" font-size="10.5" text-anchor="end">−4</text><line class="grid" x1="44" y1="195.4" x2="666" y2="195.4"/><text class="dim" x="38" y="198.9" font-size="10.5" text-anchor="end">−3</text><line class="grid" x1="44" y1="178.0" x2="666" y2="178.0"/><text class="dim" x="38" y="181.5" font-size="10.5" text-anchor="end">−2</text><line class="grid" x1="44" y1="160.6" x2="666" y2="160.6"/><text class="dim" x="38" y="164.1" font-size="10.5" text-anchor="end">−1</text><line class="line" x1="44" y1="143.2" x2="666" y2="143.2"/><text class="dim" x="38" y="146.7" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="125.9" x2="666" y2="125.9"/><text class="dim" x="38" y="129.4" font-size="10.5" text-anchor="end">1</text><line class="grid" x1="44" y1="108.5" x2="666" y2="108.5"/><text class="dim" x="38" y="112.0" font-size="10.5" text-anchor="end">2</text><line class="grid" x1="44" y1="91.1" x2="666" y2="91.1"/><text class="dim" x="38" y="94.6" font-size="10.5" text-anchor="end">3</text><line class="grid" x1="44" y1="73.7" x2="666" y2="73.7"/><text class="dim" x="38" y="77.2" font-size="10.5" text-anchor="end">4</text><line class="grid" x1="44" y1="56.3" x2="666" y2="56.3"/><text class="dim" x="38" y="59.8" font-size="10.5" text-anchor="end">5</text><line class="grid" x1="44" y1="38.9" x2="666" y2="38.9"/><text class="dim" x="38" y="42.4" font-size="10.5" text-anchor="end">6</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="74.3" y1="220" x2="74.3" y2="224"/><text class="dim" x="74.3" y="236" font-size="10.5" text-anchor="middle">5 Kas</text><line class="line" x1="180.5" y1="220" x2="180.5" y2="224"/><text class="dim" x="180.5" y="236" font-size="10.5" text-anchor="middle">12 Kas</text><line class="line" x1="286.7" y1="220" x2="286.7" y2="224"/><text class="dim" x="286.7" y="236" font-size="10.5" text-anchor="middle">19 Kas</text><line class="line" x1="392.9" y1="220" x2="392.9" y2="224"/><text class="dim" x="392.9" y="236" font-size="10.5" text-anchor="middle">26 Kas</text><line class="line" x1="499.1" y1="220" x2="499.1" y2="224"/><text class="dim" x="499.1" y="236" font-size="10.5" text-anchor="middle">3 Ara</text><line class="line" x1="605.3" y1="220" x2="605.3" y2="224"/><text class="dim" x="605.3" y="236" font-size="10.5" text-anchor="middle">10 Ara</text><rect class="box" x="461.2" y="32" width="204.8" height="188" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,162.7 59.2,121.5 74.3,154.8 89.5,157.7 104.7,177.5 119.9,204.7 135.0,197.5 150.2,175.1 165.4,133.7 180.5,106.7 195.7,110.5 210.9,145.9 226.0,106.4 241.2,123.0 256.4,140.4 271.6,156.0 286.7,143.5 301.9,102.4 317.1,86.4 332.2,66.7 347.4,62.9 362.6,109.9 377.8,105.0 392.9,93.1 408.1,92.5 423.3,113.4 438.4,150.2 453.6,120.3"/><polyline class="curve2" stroke-dasharray="5 4" style="stroke-width:2" points="453.6,120.3 468.8,120.3 484.0,120.3 499.1,120.3 514.3,120.3 529.5,120.3 544.6,120.3 559.8,120.3 575.0,120.3 590.1,120.3 605.3,120.3 620.5,120.3 635.7,120.3 650.8,120.3 666.0,120.3"/><polyline class="curve" style="stroke-width:2.4" points="453.6,120.3 468.8,126.7 484.0,131.3 499.1,134.6 514.3,137.0 529.5,138.8 544.6,140.0 559.8,140.9 575.0,141.6 590.1,142.1 605.3,142.4 620.5,142.7 635.7,142.9 650.8,143.0 666.0,143.1"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">sapma (°C)</text><line class="curve2" x1="170" y1="40" x2="188" y2="40"/><text class="ink" x="194" y="44" font-size="11">naif</text><line class="curve" x1="244" y1="40" x2="262" y2="40"/><text class="ink" x="268" y="44" font-size="11">AR(1) tahmini</text></svg>
  <figcaption>Gölgeli bölge 14 günlük tahmin. Naif son sapmayı olduğu gibi taşıyor; AR(1) her gün 0.724 ile çarpıp sıfıra, yani mevsim normaline yaklaştırıyor.</figcaption>
</figure>

Bu, iki temel yöntemin arasında duran bir tahmin. Naif "sapma olduğu gibi
kalır" diyor; ortalama "yarın normale döner" diyor; AR(1) "yavaş yavaş döner"
diyor. 2024'ün bir gün sonrası tahminlerinde hata:

| Ortalama (sapma = 0) | Naif | AR(1) |
|---|---|---|
| 1.63 | 1.26 | **1.14** |

## 3. MA: sürprizin yankısı

MA(1): $y_t = c + e_t + \theta\,e_{t-1}$. Bugün, dünkü **sürprizin** `θ` katını
taşıyor; iki gün önceki sürpriz tamamen unutulmuş.

Bölüm 12'deki iki yapay seriyi hatırla: `x` AR(1), `y` MA(1) ile üretilmişti,
ikisi de katsayı 0.7 ile. Model onları geri buluyor:

```python
print(ARIMA(w["x"], order=(1, 0, 0)).fit().params["ar.L1"].round(3))   # 0.691
print(ARIMA(w["y"], order=(0, 0, 1)).fit().params["ma.L1"].round(3))   # 0.7
```

Yanlış türü denersen ne olur? Bunu **AIC** söyler:

| | AR(1) | MA(1) |
|---|---|---|
| `x` serisi | **1622.9** | 1744.9 |
| `y` serisi | 1722.5 | **1625.2** |

**AIC** (Akaike bilgi ölçütü) modelin veriye uyumunu ödüllendirir, katsayı
sayısını cezalandırır. **Küçük olan daha iyi.** Yalnızca farkı anlamlıdır:
birkaç puanlık fark önemsiz, yüz puanlık fark açık.

## 4. I: fark

Bölüm 11'in dersi: AR ve MA **durağan** seride anlamlı. Seri durağan değilse
önce fark alınır. `d`, kaç kez.

ARIMA farkı senin yerine alıyor ve tahmini düzeye geri çeviriyor; `diff` ve
`cumsum` ile uğraşmıyorsun.

En yalın örnek `ARIMA(0, 1, 0)`: fark al, başka hiçbir şey yapma. Bu, **rastgele
yürüyüş**; tahmini naif. Hisse fiyatında daha fazlasına gerek var mı?

| Model | AIC | Katsayılar |
|---|---|---|
| (0, 1, 0) | 3503.1 | |
| (1, 1, 0) | 3503.8 | AR 0.04 |
| (0, 1, 1) | 3503.9 | MA 0.04 |
| (1, 1, 1) | 3503.1 | AR 0.63, MA −0.57 |

Hiçbiri yalın modeli geçemiyor: farkların hafızası yok (Bölüm 12'de Ljung–Box
bunu söylemişti). Son satıra dikkat: AR 0.63 ve MA −0.57 **birbirini götürüyor**.
Birbirine yakın, ters işaretli AR ve MA katsayısı, modelin gereksiz iki terimle
hiçbir şey anlatmadığının işareti.

## 5. Mertebeyi seçmek

<figure class="fig">
<div class="flow">
<span class="node">Durağanlaştır<br><code>d</code></span><span class="arrow">→</span>
<span class="node">ACF ve PACF'ye bak<br>aday <code>p</code>, <code>q</code></span><span class="arrow">→</span>
<span class="node">Adayları kur<br>AIC'yi karşılaştır</span><span class="arrow">→</span>
<span class="node">Kalıntıyı denetle<br>Ljung–Box</span><span class="arrow">→</span>
<span class="node acc">Örnek dışı sına</span>
</div>
<figcaption>Hiçbir adım tek başına karar vermez. AIC aday eler; son sözü kayan başlangıç söyler.</figcaption>
</figure>

1. **`d`:** Bölüm 11'deki gibi. Çoğu seride 0 ya da 1.
2. **Adaylar:** farkı alınmış serinin ACF ve PACF'si (Bölüm 12). PACF `p`.
   gecikmeden sonra kesiliyorsa AR(p); ACF `q`. gecikmeden sonra kesiliyorsa
   MA(q). Gerçek veride şekiller temiz değildir: **iki üç aday** çıkar.
3. **AIC:** adaylar arasında en küçüğü. Yalnızca **aynı veri ve aynı `d`** ile
   kurulan modeller karşılaştırılır.
4. **Kalıntı:** Ljung–Box p-değeri büyük olmalı (hafıza kalmamış).
5. **Sınama:** Bölüm 15'in düzeneği. Çıtayı geçmeyen model, AIC'si ne olursa
   olsun işe yaramaz.

Küçük tut: `p` ve `q` nadiren 2'yi geçer. Çok terimli model eğitimi ezberler.

## 6. Mevsimsel ARIMA

Mevsim için aynı üç fikir, **mevsim boyu kadar geriden**:

$$\text{ARIMA}(p, d, q)(P, D, Q)_m$$

- `D`: mevsimsel fark sayısı (`diff(m)`).
- `P`: mevsimsel AR: bir mevsim önceki **değer**.
- `Q`: mevsimsel MA: bir mevsim önceki **sürpriz**.
- `m`: mevsimin boyu.

```python
fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
```

**Yolcu serisi.** Bölüm 11'in reçetesi: dalgalar büyüyor (logaritma), yıllık
mevsim var (`D = 1`), trend var (`d = 1`). Dönüştürülmüş serinin ACF'si:

| Gecikme | 1 | 2 | 3 | 12 |
|---|---|---|---|---|
| ACF | −0.54 | 0.05 | 0.01 | −0.38 |

Birinci gecikmede tek çubuk, sonra kesiliyor: `q = 1`. 12. gecikmede tek çubuk:
`Q = 1`. Bölüm 12'de tanıdığın iki parmak izi. Sonuç, bu tür serilerin klasiği:

```python
import numpy as np

fit = ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
forecast = np.exp(fit.forecast(12))
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Oca 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Tem 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Oca 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Tem 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Oca 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Tem 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve" style="stroke-width:2.4" points="470.5,176.5 488.3,183.5 506.1,156.7 523.8,149.3 541.6,136.9 559.4,107.5 577.1,76.3 594.9,70.2 612.7,117.6 630.5,141.1 648.2,164.0 666.0,143.6"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">log + (0,1,1)(0,1,1)₁₂</text></svg>
  <figcaption>2024'ün tahmini. İki katsayılı bir model on iki ayın hepsinde gerçeğin yanından gidiyor; ortalama hata %1.6.</figcaption>
</figure>

| Model | MAE | Yüzde hata | AIC | Ljung–Box p |
|---|---|---|---|---|
| Mevsimsel naif × büyüme | 11.11 | %2.8 | | |
| Holt–Winters (çarpımsal) | 6.53 | %1.7 | | |
| (0,1,0)(0,1,0)₁₂ | 10.67 | %2.7 | −485.0 | 0.000 |
| (1,1,0)(0,1,1)₁₂ | 6.59 | %1.7 | −579.0 | 0.016 |
| **(0,1,1)(0,1,1)₁₂** | **6.14** | **%1.6** | **−613.0** | 0.988 |
| (1,1,1)(0,1,1)₁₂ | 6.19 | %1.6 | −611.4 | 0.987 |

Dört ölçüt aynı modeli gösteriyor: en küçük AIC, temiz kalıntı, en küçük test
hatası. Fazladan AR terimi eklemek (son satır) hiçbir şey kazandırmıyor.

Logaritmayı atlasaydın aynı modelin hatası 11.05 olurdu: dönüşüm modelin
parçası.

## 7. Özeti okumak

```python
print(fit.summary().tables[1])
```

```text
                 coef    std err          z      P>|z|      [0.025      0.975]
ma.L1         -0.9435      0.047    -19.942      0.000      -1.036      -0.851
ma.S.L12      -0.9511      0.380     -2.504      0.012      -1.695      -0.207
sigma2         0.0003   9.56e-05      2.693      0.007       7e-05       0.000
```

- **coef:** katsayı. `ma.L1` kısa dönem, `ma.S.L12` mevsimsel MA terimi.
- **P>|z|:** katsayının sıfırdan ayırt edilebilirliği. 0.05'in üstündeyse o
  terim büyük olasılıkla gereksiz.
- **[0.025, 0.975]:** katsayının güven aralığı. Sıfırı içeriyorsa aynı sonuç.
- **sigma2:** kalıntının varyansı.

## 8. Günlük satış

Mevsimsel farkın (`diff(7)`) ACF'sinde 1. gecikme 0.16, 7. gecikme −0.43
(Bölüm 12). Adaylar, tek ayrımda (5 Kasım):

| Model | AIC | Ljung–Box p | MAE |
|---|---|---|---|
| (0,0,0)(0,1,0)₇ | 8782.5 | 0.000 | 11.64 |
| (1,0,0)(0,1,1)₇ | 8423.1 | 0.000 | 14.90 |
| (0,1,1)(0,1,1)₇ | 8265.8 | 0.035 | 10.48 |
| (1,1,1)(0,1,1)₇ | 8258.7 | 0.311 | 10.44 |

İlk satır tanıdık: yalnızca mevsimsel fark, başka terim yok. Bu, **mevsimsel
naifin ta kendisi** (MAE 11.64). Temel yöntemler ARIMA ailesinin en yalın
üyeleri.

İkinci satır bir uyarı: AIC'si ilkinden çok iyi ama test hatası **daha kötü**
ve kalıntısında hafıza kalmış. `d = 0` ile seviye kaymasını izleyemiyor.
AIC tek başına yetmez.

Son iki model hem AIC'de hem kalıntıda hem testte iyi.

## 9. Sınama

Bölüm 15'in düzeneği: 13 başlangıç, 28 günlük ufuk.

| Yöntem | Ortalama MAE | En kötü deney |
|---|---|---|
| Mevsimsel naif | 17.95 | 41.3 |
| Holt–Winters | 15.91 | 38.6 |
| ARIMA (0,1,1)(0,1,1)₇ | 15.94 | 52.2 |
| ARIMA (1,1,1)(0,1,1)₇ | 15.87 | 52.7 |

ARIMA mevsimsel naifi 13 deneyin 11'inde geçiyor. Holt–Winters'a karşı ise
fark −0.02, deneyler arası oynaklığı 5.1: **tam bir beraberlik.**

Bu sonuç önemli. Bambaşka iki model (biri bileşenleri, öteki hafızayı
modelliyor) aynı hataya varıyor. Demek ki sınır modelde değil, **veride**:
bu serinin geçmişi, 28 gün ilerisi hakkında ancak bu kadarını söylüyor. Daha
ileri gitmek için daha karmaşık bir model değil, **yeni bilgi** gerekiyor:
takvim, tatiller, kampanyalar. Bölüm 18 tam olarak bu.

ARIMA'nın en kötü deneyi Holt–Winters'ınkinden belirgin biçimde kötü (52'ye
karşı 39): `d = 1`, yıl sonu düzeyini Ocak'a taşıyor. Ortalama hata aynıyken
en kötü durum farklıysa, riskten kaçınan seçim belli.

## 10. Hangisi ne zaman?

| | Üstel düzleştirme | ARIMA |
|---|---|---|
| Seriyi nasıl anlatır | Düzey, eğim, mevsim | Geçmiş değerler ve sürprizler |
| Güçlü olduğu yer | Belirgin trend ve mevsim | Kısa dönem hafıza; sensör, sapma serileri |
| Çarpımsal yapı | Doğrudan (`"mul"`) | Logaritmayla |
| Ayar | Bileşen seçimi | `p, d, q, P, D, Q` seçimi |
| Dış değişken | Alamaz | Alabilir (Bölüm 18) |

Pratikte ikisini de kur, aynı düzenekte sına, berabereyse basit olanı seç.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Durağan olmayan seriye `d = 0` | Kalıntıda hafıza, kayan tahmin | Bölüm 11'deki reçeteyle `d` ve `D` |
| Gereğinden çok fark | Oynaklık artar, MA katsayısı −1'e yapışır | En az fark |
| Büyük `p` ve `q` | Ezber; birbirini götüren katsayılar | Küçük tut; AIC ve p-değerine bak |
| Farklı `d` ile AIC karşılaştırmak | Anlamsız | Yalnızca aynı veri, aynı fark |
| Yalnızca AIC'ye güvenmek | Örnek dışında kötü model | Kalıntı ve kayan başlangıç |
| Çarpımsal seride logaritmayı unutmak | Hata iki katı | `np.log` → model → `np.exp` |
| `seasonal_order`'da `m`'yi unutmak | Mevsim modellenmez | `(P, D, Q, m)` |
| Kalıntının ilk değerlerini denetime katmak | Başlangıç etkisi testi bozar | İlk `d + D × m` değeri at |

## Özet

- **AR(p)**: geçmiş değerler. **MA(q)**: geçmiş sürprizler. **I(d)**: fark.
- AR(1) tahmini ortalamaya `φ` hızıyla döner; MA(1)'in etkisi bir adımda biter;
  `ARIMA(0,1,0)` rastgele yürüyüştür.
- Mevsimsel sürüm `(p,d,q)(P,D,Q)ₘ`: aynı fikirler bir mevsim geriden.
- Mertebe: `d` durağanlıktan, adaylar ACF/PACF'den, eleme **AIC**'den,
  onay **kalıntıdan** (Ljung–Box) ve **kayan başlangıçtan**.
- `ARIMA(train, order=..., seasonal_order=...).fit()`; `.params`,
  `.summary()`, `.forecast(h)`, `.resid`, `.aic`.
- Yolcu serisinde `log` + (0,1,1)(0,1,1)₁₂ hatayı %1.6'ya indiriyor.
- Günlük satışta ARIMA ile Holt–Winters **berabere**: sınır modelde değil,
  veride.

Sıradaki bölüm o sınırı aşıyor: modele serinin kendi geçmişinden başka bilgi
veriyorsun. Tatiller, kampanyalar, hava durumu.
