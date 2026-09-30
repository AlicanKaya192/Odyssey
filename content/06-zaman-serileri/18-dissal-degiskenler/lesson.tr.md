# Dışsal Değişkenler

Bölüm 17 bir sınırla bitti: çok farklı iki model aynı hataya vardı, çünkü
ikisi de yalnızca **serinin kendi geçmişine** bakıyordu. Geçmiş, yarın bir
kampanya olacağını bilmez. Önümüzdeki perşembenin resmi tatil olduğunu bilmez.
Haftaya havanın ısınacağını bilmez.

Sen biliyorsun. Bu bilgiyi modele vermenin yolu **dışsal değişkenler**: serinin
dışından gelen ve onu etkileyen sütunlar. Bu bölümde onları kuruyor, modele
veriyor ve en önemli soruyu soruyorsun: **tahmin anında bu bilgi elimde olacak
mı?**

## 1. Üç tür dış bilgi

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Takvim</span><span>Tatil, hafta sonu, ayın günü, okul dönemi. Geleceği <b>kesin</b> biliniyor.</span></div>
<div class="anat-row"><span>Planlanan</span><span>Kampanya, fiyat, reklam bütçesi, açılış saati. Geleceğini <b>sen belirliyorsun</b>.</span></div>
<div class="anat-row"><span>Ölçülen</span><span>Hava sıcaklığı, döviz kuru, rakibin fiyatı. Geleceği <b>bilinmiyor</b>; onun da tahmini gerekir.</span></div>
</div>
<figcaption>İlk ikisi tahmin anında hazır. Üçüncüsü bölümün zor kısmı.</figcaption>
</figure>

Bu bölümün verisi bir iş merkezindeki kafe (`cafe_daily.csv`), üç türden de
birer değişkeni var:

```python
import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
print(c.head(3))
```

```text
            sales  temp_c  promo  holiday
date
2022-01-01     46     7.1      0        1
2022-01-02     86     6.1      0        0
2022-01-03    205     8.6      0        0
```

`promo` ve `holiday` **kukla değişken**: olay varsa 1, yoksa 0. Üç yılda 84
kampanya günü ve 41 resmi tatil var.

## 2. Etkiyi kabaca ölçmek ve tuzağı

Kampanya ne kadar satış getiriyor? İlk akla gelen:

```python
print(round(c.loc[c["promo"] == 1, "sales"].mean(), 1))     # 284.0
print(round(c.loc[c["promo"] == 0, "sales"].mean(), 1))     # 227.1
```

Fark 57. Ama bu karşılaştırma **adil değil**: kampanyalar hep perşembe–cumartesi
yapılıyor ve o günlerin satışı zaten ortalamadan farklı. Haftanın günü, araya
giren bir **karıştırıcı**.

Daha adil bir karşılaştırma: her kampanya gününü, bir hafta önceki ve sonraki
**aynı günle** karşılaştır.

| | Kaba fark | Aynı günün komşularıyla |
|---|---|---|
| Kampanya | +57.0 | +50.8 |
| Tatil | −67.3 | −76.2 |

Tatilin etkisi kabaca ölçülünce olduğundan **küçük** görünüyor: tatillerin çoğu
bahar ve yazda, yani satışın zaten yüksek olduğu sıcak aylarda. Sıcaklık ikinci
bir karıştırıcı.

Bütün etkileri **aynı anda** ayırmak için model gerekiyor.

## 3. Dışsal değişkenli ARIMA

ARIMA'ya `exog` ile bir tablo verirsin. Model iki işi birlikte yapar: dış
değişkenlerin etkisini bir regresyonla tahmin eder ve **geriye kalanı** ARIMA
ile modeller.

```python
from statsmodels.tsa.arima.model import ARIMA

train = c.loc[:"2024-10-31"]
columns = ["promo", "holiday", "temp_c"]

fit = ARIMA(
    train["sales"], exog=train[columns],
    order=(1, 0, 0), seasonal_order=(0, 1, 1, 7),
).fit()
print(fit.summary().tables[1])
```

```text
                 coef    std err          z      P>|z|      [0.025      0.975]
promo         49.3391      1.636     30.163      0.000      46.133      52.545
holiday      -75.2347      1.403    -53.612      0.000     -77.985     -72.484
temp_c         5.5143      0.089     61.619      0.000       5.339       5.690
ar.L1          0.5077      0.027     18.896      0.000       0.455       0.560
ma.S.L7       -0.9139      0.014    -64.185      0.000      -0.942      -0.886
```

İlk üç satır doğrudan okunuyor:

- **Kampanya günü +49 satış.** (Kaba hesap 57 demişti.)
- **Resmi tatilde −75 satış.** İş merkezi boşalıyor.
- **Her 1 derece için +5.5 satış.** Yazın kalabalık olmasının nedeni bu.

Son iki satır tanıdık ARIMA terimleri: dış değişkenlerin açıklayamadığı kısımda
kalan kısa hafıza ve haftalık desen.

AIC 9464'ten 7569'a düştü: neredeyse iki bin puan. Bölüm 17'de "birkaç puan"
için uğraşıyordun; yeni bilgi, mertebe ayarının yapamadığını yapıyor.

## 4. Tahmin: gelecekteki değişkenler de gerekli

Dış değişkenli bir modelden tahmin istemek için **gelecekteki** değerlerini de
vermen gerekir:

```python
test = c.loc["2024-11-01":"2024-11-28"]
forecast = fit.forecast(28, exog=test[columns])
```

Satır sayısı ufukla, sütunlar eğitimdekiyle aynı sırada olmalı. Model bu
tabloyu alıp "14–16 Kasım'da kampanya var, +49 ekle" diyebiliyor.

Ama bir sorun var: bu kodda `test[columns]` içinde Kasım'ın **gerçek
sıcaklıkları** duruyor. 31 Ekim'de onları bilemezdin.

## 5. Gelecekte bilinen ve bilinmeyen

<figure class="fig">
<div class="versus">
<div class="ok"><h4>Tahmin anında hazır</h4><p>Takvim: tatil listesi yıllar öncesinden belli.</p><p>Plan: kampanya takvimi, fiyat listesi.</p><p>Doğrudan gelecekteki değerlerini yazarsın.</p></div>
<div class="no"><h4>Tahmin anında bilinmiyor</h4><p>Hava, kur, rakip, talep.</p><p>Geleceği için <b>ayrı bir tahmin</b> gerekir.</p><p>O tahminin hatası senin tahminine eklenir.</p></div>
</div>
<figcaption>Bir değişkeni modele koymadan önce sor: bu sayı, tahmin yaptığım gün elimde olacak mı?</figcaption>
</figure>

Sıcaklık için üç seçenek ve hepsinin 13 deneydeki sonucu (28 günlük ufuk):

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="216.0" x2="666" y2="216.0"/><text class="dim" x="38" y="219.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="164.6" x2="666" y2="164.6"/><text class="dim" x="38" y="168.1" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="113.3" x2="666" y2="113.3"/><text class="dim" x="38" y="116.8" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="61.9" x2="666" y2="61.9"/><text class="dim" x="38" y="65.4" font-size="10.5" text-anchor="end">30</text><line class="line" x1="44" y1="216" x2="666" y2="216"/><line class="line" x1="95.8" y1="216" x2="95.8" y2="220"/><text class="dim" x="95.8" y="232" font-size="10.5" text-anchor="middle">mevsimsel naif</text><line class="line" x1="182.2" y1="216" x2="182.2" y2="220"/><text class="dim" x="182.2" y="232" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="268.6" y1="216" x2="268.6" y2="220"/><text class="dim" x="268.6" y="232" font-size="10.5" text-anchor="middle">ARIMA</text><line class="line" x1="355.0" y1="216" x2="355.0" y2="220"/><text class="dim" x="355.0" y="232" font-size="10.5" text-anchor="middle">+ takvim</text><line class="line" x1="441.4" y1="216" x2="441.4" y2="220"/><text class="dim" x="441.4" y="232" font-size="10.5" text-anchor="middle">+ son sıcaklık</text><line class="line" x1="527.8" y1="216" x2="527.8" y2="220"/><text class="dim" x="527.8" y="232" font-size="10.5" text-anchor="middle">+ mevsim normali</text><line class="line" x1="614.2" y1="216" x2="614.2" y2="220"/><text class="dim" x="614.2" y="232" font-size="10.5" text-anchor="middle">+ gerçek sıcaklık</text><rect class="dot2" x="69.1" y="51.4" width="53.5" height="164.6" rx="3" opacity="0.9"/><rect class="dot2" x="155.4" y="65.7" width="53.6" height="150.3" rx="3" opacity="0.9"/><rect class="dot2" x="241.8" y="65.7" width="53.6" height="150.3" rx="3" opacity="0.9"/><rect class="dot" x="328.2" y="91.2" width="53.6" height="124.8" rx="3" opacity="0.9"/><rect class="dot" x="414.6" y="125.3" width="53.6" height="90.7" rx="3" opacity="0.9"/><rect class="dot" x="501.0" y="138.9" width="53.6" height="77.1" rx="3" opacity="0.9"/><rect class="dim" x="587.4" y="167.7" width="53.5" height="48.3" rx="3" opacity="0.9"/><text class="ink" x="95.8" y="45.2" font-size="11.5" text-anchor="middle">32.1</text><text class="ink" x="182.2" y="59.6" font-size="11.5" text-anchor="middle">29.3</text><text class="ink" x="268.6" y="59.6" font-size="11.5" text-anchor="middle">29.3</text><text class="ink" x="355.0" y="85.1" font-size="11.5" text-anchor="middle">24.3</text><text class="ink" x="441.4" y="119.1" font-size="11.5" text-anchor="middle">17.7</text><text class="ink" x="527.8" y="132.8" font-size="11.5" text-anchor="middle">15.0</text><text class="ink" x="614.2" y="161.6" font-size="11.5" text-anchor="middle">9.4</text></svg>
  <figcaption>13 deneyin ortalama MAE'si. Turuncu: yalnızca serinin geçmişi. Mor: dış değişkenler, tahmin anında bilinenle. Gri: gelecekteki gerçek sıcaklıkla; ulaşılabilir değil, bir tavan.</figcaption>
</figure>

| Yöntem | Ortalama MAE | En kötü deney |
|---|---|---|
| Mevsimsel naif | 32.06 | 54.1 |
| Holt–Winters | 29.26 | 76.5 |
| ARIMA, dış değişkensiz | 29.26 | 75.6 |
| + takvim (kampanya, tatil) | 24.30 | 38.7 |
| + sıcaklık: son bilinen değer | 17.67 | 31.5 |
| + sıcaklık: mevsim normali | **15.01** | 18.8 |
| + sıcaklık: gerçek değer (hile) | 9.40 | 11.4 |

Tablodan üç sonuç:

**Yeni bilgi çok şey değiştiriyor.** Dış değişkensiz üç model 29–32 arasında
sıkışmıştı; takvim ve mevsim normaliyle hata yarıya iniyor ve en kötü deney
76'dan 19'a düşüyor.

**Bilinmeyen değişken için makul bir vekil yeter.** Sıcaklığın 28 gün sonrasını
kimse bilemez, ama o takvim gününün geçmiş yıllardaki ortalaması (mevsim
normali) iyi bir tahmin:

```python
normal = train["temp_c"].groupby(train.index.dayofyear).mean()
future["temp_c"] = [normal[day] for day in future.index.dayofyear]
```

"Son bilinen sıcaklık" daha kötü: 28 gün boyunca aynı sayıyı taşıyor ve mevsim
dönerken yanılıyor.

**Son satır bir tahmin değil, bir tavan.** Gerçek sıcaklıkla 9.40: bu, kusursuz
bir hava tahminin olsaydı varabileceğin yer. Onu başarın diye raporlamak
**sızıntı**: gelecekteki bir ölçümü kullanmış olursun. Yararı başka: 15.01 ile
9.40 arasındaki fark, daha iyi bir hava tahmininin sana en fazla ne
kazandıracağını söylüyor.

## 6. Uzun mevsim: Fourier terimleri

Mevsimsel ARIMA ve Holt–Winters tek ve kısa bir mevsim alıyordu. Günlük veride
haftalık deseni aldın; **yıllık** deseni (365 günlük mevsim) alamadın. Kafede
bu işi sıcaklık gördü. Sıcaklık gibi bir değişkenin yoksa?

Düzgün bir yıllık dalga, birkaç sinüs ve kosinüsün toplamıyla anlatılabilir.
Bunlar da birer dışsal değişken:

```python
import numpy as np


def fourier(index, K, period=365.25):
    day = index.dayofyear.to_numpy()
    columns = {}
    for k in range(1, K + 1):
        columns[f"sin{k}"] = np.sin(2 * np.pi * k * day / period)
        columns[f"cos{k}"] = np.cos(2 * np.pi * k * day / period)
    return pd.DataFrame(columns, index=index)
```

`K = 1` tek bir yumuşak dalga (bir tepe, bir çukur); `K = 2` yılda iki kez
kıvrılabilen bir şekil. Her `K` iki sütun ekler. Takvime bağlı oldukları için
geleceği **kesin biliniyor**: `fourier(future_index, K)`.

Bölüm 17'deki günlük mağaza satışına dön. Orada ARIMA'nın en kötü deneyleri yıl
dönümündeydi. İki takvim bilgisi ekle: yıllık dalga (Fourier, `K = 2`) ve
Aralık ayındaki yılbaşı tırmanışı (ayın günü ilerledikçe büyüyen bir sütun).

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="220.0" x2="666" y2="220.0"/><text class="dim" x="38" y="223.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="187.2" x2="666" y2="187.2"/><text class="dim" x="38" y="190.7" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="154.5" x2="666" y2="154.5"/><text class="dim" x="38" y="158.0" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="121.7" x2="666" y2="121.7"/><text class="dim" x="38" y="125.2" font-size="10.5" text-anchor="end">30</text><line class="grid" x1="44" y1="89.0" x2="666" y2="89.0"/><text class="dim" x="38" y="92.5" font-size="10.5" text-anchor="end">40</text><line class="grid" x1="44" y1="56.2" x2="666" y2="56.2"/><text class="dim" x="38" y="59.7" font-size="10.5" text-anchor="end">50</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="76.5" y1="220" x2="76.5" y2="224"/><text class="dim" x="76.5" y="236" font-size="10.5" text-anchor="middle">2 Oca</text><line class="line" x1="169.3" y1="220" x2="169.3" y2="224"/><text class="dim" x="169.3" y="236" font-size="10.5" text-anchor="middle">27 Şub</text><line class="line" x1="262.2" y1="220" x2="262.2" y2="224"/><text class="dim" x="262.2" y="236" font-size="10.5" text-anchor="middle">23 Nis</text><line class="line" x1="355.0" y1="220" x2="355.0" y2="224"/><text class="dim" x="355.0" y="236" font-size="10.5" text-anchor="middle">18 Haz</text><line class="line" x1="447.8" y1="220" x2="447.8" y2="224"/><text class="dim" x="447.8" y="236" font-size="10.5" text-anchor="middle">13 Ağu</text><line class="line" x1="540.7" y1="220" x2="540.7" y2="224"/><text class="dim" x="540.7" y="236" font-size="10.5" text-anchor="middle">8 Eki</text><line class="line" x1="633.5" y1="220" x2="633.5" y2="224"/><text class="dim" x="633.5" y="236" font-size="10.5" text-anchor="middle">3 Ara</text><rect class="dot2" x="58.9" y="49.0" width="16.7" height="171.0" rx="3" opacity="0.9"/><rect class="dot2" x="105.3" y="186.1" width="16.7" height="33.9" rx="3" opacity="0.9"/><rect class="dot2" x="151.7" y="179.5" width="16.7" height="40.5" rx="3" opacity="0.9"/><rect class="dot2" x="198.1" y="187.6" width="16.7" height="32.4" rx="3" opacity="0.9"/><rect class="dot2" x="244.5" y="181.0" width="16.7" height="39.0" rx="3" opacity="0.9"/><rect class="dot2" x="290.9" y="181.9" width="16.8" height="38.1" rx="3" opacity="0.9"/><rect class="dot2" x="337.4" y="190.9" width="16.7" height="29.1" rx="3" opacity="0.9"/><rect class="dot2" x="383.8" y="191.6" width="16.7" height="28.4" rx="3" opacity="0.9"/><rect class="dot2" x="430.2" y="152.2" width="16.7" height="67.8" rx="3" opacity="0.9"/><rect class="dot2" x="476.6" y="192.9" width="16.7" height="27.1" rx="3" opacity="0.9"/><rect class="dot2" x="523.0" y="185.7" width="16.7" height="34.3" rx="3" opacity="0.9"/><rect class="dot2" x="569.5" y="185.7" width="16.7" height="34.3" rx="3" opacity="0.9"/><rect class="dot2" x="615.9" y="117.3" width="16.7" height="102.7" rx="3" opacity="0.9"/><rect class="dot" x="77.4" y="191.3" width="16.7" height="28.7" rx="3" opacity="0.9"/><rect class="dot" x="123.8" y="189.0" width="16.7" height="31.0" rx="3" opacity="0.9"/><rect class="dot" x="170.3" y="179.8" width="16.7" height="40.2" rx="3" opacity="0.9"/><rect class="dot" x="216.7" y="191.2" width="16.7" height="28.8" rx="3" opacity="0.9"/><rect class="dot" x="263.1" y="186.5" width="16.7" height="33.5" rx="3" opacity="0.9"/><rect class="dot" x="309.5" y="182.8" width="16.7" height="37.2" rx="3" opacity="0.9"/><rect class="dot" x="355.9" y="192.7" width="16.7" height="27.3" rx="3" opacity="0.9"/><rect class="dot" x="402.3" y="190.9" width="16.8" height="29.1" rx="3" opacity="0.9"/><rect class="dot" x="448.8" y="179.0" width="16.7" height="41.0" rx="3" opacity="0.9"/><rect class="dot" x="495.2" y="194.6" width="16.7" height="25.4" rx="3" opacity="0.9"/><rect class="dot" x="541.6" y="189.8" width="16.7" height="30.2" rx="3" opacity="0.9"/><rect class="dot" x="588.0" y="183.5" width="16.7" height="36.5" rx="3" opacity="0.9"/><rect class="dot" x="634.4" y="173.0" width="16.7" height="47.0" rx="3" opacity="0.9"/><line class="curve2" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">ARIMA</text><line class="curve" x1="135" y1="38" x2="153" y2="38"/><text class="ink" x="159" y="42" font-size="11">ARIMA + takvim</text></svg>
  <figcaption>Günlük mağaza satışı, 13 deneyin MAE'si; yatay eksen eğitimin bittiği gün. Takvim bilgisi sıradan dönemlerde az şey değiştiriyor, yıl dönümündeki iki dev hatayı ise ortadan kaldırıyor.</figcaption>
</figure>

| Model | Ortalama MAE | En kötü deney |
|---|---|---|
| ARIMA (0,1,1)(0,1,1)₇ | 15.94 | 52.2 |
| + trend + Fourier (`K = 2`) | 13.16 | 33.0 |
| + Fourier + Aralık tırmanışı | **10.23** | 14.4 |

Bölüm 17'de "sınır veride" demiştik. Modele verinin söylemediğini (yılın
neresinde olduğumuzu) söyleyince sınır yer değiştirdi: ortalama hata üçte bir
azaldı, en kötü deney 52'den 14'e indi.

Aralık sütununu nereden bildik? Bölüm 15'te en kötü deneylerin **hep yıl
dönümünde** olduğunu görmüştün. Kötü deneylerin takvimdeki yeri, hangi
değişkenin eksik olduğunu söyler.

## 7. Tuzaklar

**Sızıntı.** Dış değişkenin tahmin ettiğin günle **aynı güne** ait değeri,
tahmin anında bilinmiyorsa kullanılamaz. "O günkü müşteri sayısı" satışı çok iyi
açıklar, ama yarının müşteri sayısını bugün bilmiyorsun. Böyle değişkenleri
ancak **gecikmeli** kullanabilirsin: `visitors.shift(1)`.

**Karıştırıcılar.** Katsayı, "öteki değişkenler sabitken" etkidir. Önemli bir
değişkeni dışarıda bırakırsan etkisi komşularına yapışır: sıcaklığı çıkarınca
kampanya katsayısı 49'dan 53'e kayıyor.

**Eğitimde hiç görülmemiş değerler.** Model −5 derecede ya da üç gün süren bir
kampanya yerine üç haftalık bir kampanyada ne olacağını bilmiyor; doğrusal
etkiyi olduğu gibi uzatıyor.

**Az örnek.** Yılda bir kez olan bir olayın (yılbaşı) etkisi üç yıllık veride üç
gözlemden tahmin ediliyor. Katsayının güven aralığına bak.

**Etki sabit değil.** Aynı kampanya beşinci kez yapıldığında aynı etkiyi
yapmayabilir. Modeli düzenli olarak yeniden kur ve katsayıları izle.

**Çok değişken.** Her sütun bir katsayı; azı karar, çoğu ezber. Etkisini
açıklayabildiğin değişkenleri koy.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `forecast`'e `exog` vermemek | Hata: gelecekteki değişkenler eksik | `fit.forecast(h, exog=future)` |
| Gelecek tablosunda sütun sırası ya da sayısı farklı | Hata ya da yanlış katsayıyla çarpım | Eğitimdeki sütunlar, aynı sırada |
| Test dönemindeki gerçek ölçümleri kullanmak | Sızıntı; inanılmaz iyi sonuç | Bilinmeyen değişkeni de tahmin et |
| "Gerçek değerle" sonucu başarı diye raporlamak | Üretimde çöken model | Tavan olarak göster, ayrı raporla |
| Aynı günün bilinmeyen değişkeni | Sızıntı | `shift` ile gecikmeli |
| Kaba ortalama farkını etki saymak | Karıştırıcılar yüzünden yanlı | Model, ya da benzer günlerle karşılaştırma |
| Haftalık mevsim varken 7 kukla + mevsimsel fark | Aynı bilgi iki kez; model kurulamaz | Birini seç |
| Çok büyük `K` | Dalga gürültüyü ezberler | `K` 1–3; kayan başlangıçla seç |

## Özet

- **Dışsal değişken**, serinin kendi geçmişi dışındaki bilgi: takvim, plan,
  ölçüm.
- `ARIMA(y, exog=X, ...)` etkileri regresyonla, kalanı ARIMA ile modeller.
  Katsayılar doğrudan okunur: "kampanya +49".
- Tahmin için **gelecekteki** `X` gerekir: `fit.forecast(h, exog=X_future)`.
- Takvim ve plan değişkenlerinin geleceği bellidir. **Ölçülen** değişkenin
  geleceği bilinmez: mevsim normali gibi bir vekil kullan; gerçek değerle
  bulunan sonuç tavandır, başarı değil.
- **Fourier terimleri** uzun mevsimi (yıllık) birkaç sütunla anlatır.
- Kötü deneylerin takvimdeki yeri, eksik değişkeni gösterir.
- Kafede hata 29'dan 15'e, mağazada 16'dan 10'a indi: kazanç modelden değil,
  **yeni bilgiden** geldi.

Dış değişkenler bir tablo: her satır bir gün, her sütun bir bilgi. Bu, makine
öğrenmesinin ana dili. Sıradaki bölümde tahmini bir tablo problemine çeviriyor
ve Makine Öğrenmesi patikasındaki araçları kullanıyorsun.
