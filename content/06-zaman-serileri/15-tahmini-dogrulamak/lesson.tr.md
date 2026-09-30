# Tahmini Doğrulamak

Bölüm 14'te mevsimsel naifin hatasını ölçtün: 28 günlük ufukta 11.6. Bu sayıya
ne kadar güvenebilirsin?

Aynı deneyi 2024 boyunca **on üç farklı başlangıçtan** tekrarlayınca ortalama
hata 17.9 çıkıyor; en iyi dönemde 9.4, en kötüsünde 41.3. İlk ölçtüğün 11.6
yanlış değildi, ama **şanslı bir dönemin** sayısıydı.

Bu bölüm bir tahmini dürüstçe ölçmeyi öğretiyor: hangi hata ölçüsü, kaç deney,
hangi veriyle. Bundan sonraki her modelin (üstel düzleştirme, ARIMA, makine
öğrenmesi) notunu burada kuracağın düzenek verecek.

## 1. Hata ölçüleri

Hata her zaman aynı: **gerçek − tahmin**. Fark, o hataları tek sayıya nasıl
indirdiğinde.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>MAE</span><span>Mutlak hataların ortalaması. Serinin biriminde, okuması en kolay.</span></div>
<div class="anat-row"><span>RMSE</span><span>Hataların karesinin ortalamasının karekökü. Büyük hataları ağır cezalandırır.</span></div>
<div class="anat-row"><span>MAPE</span><span>Mutlak yüzde hataların ortalaması. Birimsiz; sıfıra yakın değerlerde bozulur.</span></div>
<div class="anat-row"><span>MASE</span><span>MAE'nin, naif yöntemin eğitimdeki hatasına oranı. Birimsiz ve sağlam; 1'in altı naiften iyi.</span></div>
<div class="anat-row"><span>Yanlılık</span><span>Hataların ortalaması. Büyüklüğü değil, <b>yönü</b> gösterir.</span></div>
</div>
<figcaption>Hiçbiri "en doğrusu" değil; her biri başka bir soruyu cevaplıyor.</figcaption>
</figure>

```python
import numpy as np


def mae(actual, forecast):
    return np.mean(np.abs(actual - forecast))


def rmse(actual, forecast):
    return np.sqrt(np.mean((actual - forecast) ** 2))


def mape(actual, forecast):
    return np.mean(np.abs(actual - forecast) / np.abs(actual)) * 100
```

Bölüm 14'teki deneyde (eğitim 5 Kasım'a kadar, 28 gün, mevsimsel naif):

| MAE | RMSE | MAPE | Yanlılık |
|---|---|---|---|
| 11.64 | 13.98 | %3.46 | +6.79 |

## 2. MAE mi, RMSE mi?

RMSE her zaman MAE'den büyük ya da ona eşit. Aradaki **fark** bilgi taşıyor:
hatalar birbirine yakınsa ikisi yakın çıkar; birkaç büyük hata varsa RMSE açılır.

Web trafiğinde mevsimsel naifin tek adımlı hatası:

| | MAE | RMSE | RMSE / MAE |
|---|---|---|---|
| Bütün yıl | 307.2 | 728.6 | 2.37 |
| Üç aykırı günün etkilediği 6 gün çıkarılınca | 225.3 | 303.3 | 1.35 |

366 günün 6'sı MAE'yi %36, RMSE'yi **%140** şişiriyor. (Üç aykırı gün altı hata
üretiyor: gün gelince tahmin kaçırıyor, bir hafta sonra o günü kopyaladığı için
yine kaçırıyor.)

Hangisini seçeceğin **büyük hatanın bedeline** bağlı:

- Büyük hata, küçük hatanın katlarınca pahalıysa (stok tükenmesi, enerji
  kesintisi): **RMSE**. Büyük ıskayı affetmez.
- Her birimlik hata aynı maliyetteyse ve veride aykırı günler varsa: **MAE**.
  Birkaç kötü gün bütün notu belirlemez.

## 3. MAPE ve tuzakları

Yüzde hata cazip: "yüzde 3.5 yanılıyoruz" herkesin anladığı bir cümle ve farklı
ölçekteki serileri karşılaştırmaya izin veriyor. Ama üç tuzağı var.

**Sıfırda patlar.** Gerçek değer sıfırsa bölme tanımsız. Pazarları kapalı olan
C mağazasında naif tahminin MAPE'si `inf`: 52 pazar gününde payda sıfır.

**Küçük değerlerde şişer.** Gerçek 2, tahmin 4 ise hata %100. Günde birkaç tane
satılan bir üründe MAPE anlamsız büyür.

**Simetrik değil.** Aynı 50 birimlik ıska, yönüne göre farklı cezalandırılır:

| Gerçek | Tahmin | Yüzde hata |
|---|---|---|
| 100 | 150 | %50 |
| 150 | 100 | %33 |

Yüksek tahmin düşük tahminden ağır cezalandırılıyor; MAPE'ye göre seçilen model
**düşük tahmin etmeye** meyleder.

MAPE'yi değerleri sıfırdan uzak, hep artı serilerde kullan. Ötekilerde MASE.

## 4. MASE: ölçekten bağımsız ve sağlam

Fikir: hatayı, **naif yöntemin aynı serideki tipik hatasına** böl.

$$\text{MASE} = \frac{\text{MAE}_{\text{tahmin}}}{\text{eğitimde mevsimsel naifin tek adımlı MAE'si}}$$

```python
def mase(actual, forecast, train, m):
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return mae(actual, forecast) / scale
```

`train[m:] - train[:-m]` her değerin bir mevsim öncekinden farkı. Payda
eğitim verisinden geliyor; test verisine dokunmuyor ve seride sıfır olsa bile
sıfır çıkmıyor.

Üç farklı seride aynı tablo:

| Seri ve yöntem | MAE | MAPE | MASE |
|---|---|---|---|
| Günlük satış, mevsimsel naif | 11.6 | %3.5 | 0.88 |
| Aylık yolcu, mevsimsel naif | 40.4 | %10.3 | 1.82 |
| Aylık yolcu, büyümeli | 11.1 | %2.8 | 0.50 |
| Hisse, naif (40 gün) | 18.8 | %11.5 | 10.36 |

MAE'ler karşılaştırılamaz (birimler farklı). MASE karşılaştırılır: **1'in altı**,
"tek adımlı naiften daha az yanılıyor" demek. Hisse satırındaki 10.36 şunu
söylüyor: 40 gün ilerisini tahmin etmek, yarını tahmin etmekten on kat zor.

## 5. Tek ayrım yetmez: kayan başlangıç

Tek bir eğitim/test ayrımı tek bir deney. Sonucu, o 28 günün kolay ya da zor
olmasına bağlı. Çözüm deneyi tekrarlamak: başlangıcı geçmişte ileri doğru
kaydır, her durakta yeniden tahmin et ve ölç. Buna **geriye dönük sınama**
(backtesting) ya da **kayan başlangıç** deniyor.

<figure class="fig">
  <svg viewBox="0 0 680 228" width="680" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="86" y="48" font-size="11.5" text-anchor="end">deney 1</text><rect class="dot" x="96.0" y="34" width="236.7" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="334.7" y="34" width="64.2" height="20" rx="4"/><text class="dim" x="86" y="80" font-size="11.5" text-anchor="end">deney 2</text><rect class="dot" x="96.0" y="66" width="302.9" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="400.9" y="66" width="64.3" height="20" rx="4"/><text class="dim" x="86" y="112" font-size="11.5" text-anchor="end">deney 3</text><rect class="dot" x="96.0" y="98" width="369.2" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="467.2" y="98" width="64.3" height="20" rx="4"/><text class="dim" x="86" y="144" font-size="11.5" text-anchor="end">deney 4</text><rect class="dot" x="96.0" y="130" width="435.5" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="533.5" y="130" width="64.2" height="20" rx="4"/><text class="dim" x="86" y="176" font-size="11.5" text-anchor="end">deney 5</text><rect class="dot" x="96.0" y="162" width="501.7" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="599.7" y="162" width="64.3" height="20" rx="4"/><rect class="dot" x="96" y="5" width="22" height="10" rx="3" opacity="0.28"/><text class="ink" x="124" y="14" font-size="11.5">eğitim</text><rect class="dot2" x="196" y="5" width="22" height="10" rx="3"/><text class="ink" x="224" y="14" font-size="11.5">test</text><line class="line" x1="96" y1="202" x2="658" y2="202"/><polygon class="ink" points="664,202 656,198 656,206"/><text class="dim" x="664" y="218" font-size="11" text-anchor="end">zaman</text></svg>
  <figcaption>Kayan başlangıç, genişleyen pencere. Her deneyde eğitim biraz daha uzuyor, test onun hemen ardından geliyor. Test hiçbir zaman eğitimin içinde değil.</figcaption>
</figure>

```python
def backtest(y, forecast, first, step, h, count):
    scores = []
    for i in range(count):
        cut = pd.Timestamp(first) + pd.Timedelta(days=step * i)
        train = y.loc[:cut]
        test = y.loc[cut + pd.Timedelta(days=1):].iloc[:h]
        scores.append(mae(test.to_numpy(), forecast(train, h)))
    return scores
```

`forecast` bir fonksiyon: eğitim verisini ve ufku alıp `h` tahmin döndürüyor.
Her turda yalnızca o ana kadarki veriyi görüyor.

2 Ocak 2024'ten başlayıp 28'er gün kaydırarak 13 deney:

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.0" x2="666" y2="210.0"/><text class="dim" x="38" y="213.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="170.0" x2="666" y2="170.0"/><text class="dim" x="38" y="173.5" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="130.0" x2="666" y2="130.0"/><text class="dim" x="38" y="133.5" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="90.0" x2="666" y2="90.0"/><text class="dim" x="38" y="93.5" font-size="10.5" text-anchor="end">30</text><line class="grid" x1="44" y1="50.0" x2="666" y2="50.0"/><text class="dim" x="38" y="53.5" font-size="10.5" text-anchor="end">40</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="72.3" y1="210" x2="72.3" y2="214"/><text class="dim" x="72.3" y="226" font-size="10.5" text-anchor="middle">2 Oca</text><line class="line" x1="166.5" y1="210" x2="166.5" y2="214"/><text class="dim" x="166.5" y="226" font-size="10.5" text-anchor="middle">27 Şub</text><line class="line" x1="260.8" y1="210" x2="260.8" y2="214"/><text class="dim" x="260.8" y="226" font-size="10.5" text-anchor="middle">23 Nis</text><line class="line" x1="355.0" y1="210" x2="355.0" y2="214"/><text class="dim" x="355.0" y="226" font-size="10.5" text-anchor="middle">18 Haz</text><line class="line" x1="449.2" y1="210" x2="449.2" y2="214"/><text class="dim" x="449.2" y="226" font-size="10.5" text-anchor="middle">13 Ağu</text><line class="line" x1="543.5" y1="210" x2="543.5" y2="214"/><text class="dim" x="543.5" y="226" font-size="10.5" text-anchor="middle">8 Eki</text><line class="line" x1="637.7" y1="210" x2="637.7" y2="214"/><text class="dim" x="637.7" y="226" font-size="10.5" text-anchor="middle">3 Ara</text><rect class="dot" x="57.7" y="44.9" width="29.2" height="165.1" rx="3" opacity="0.9"/><rect class="dot" x="104.8" y="166.0" width="29.2" height="44.0" rx="3" opacity="0.9"/><rect class="dot" x="151.9" y="146.7" width="29.2" height="63.3" rx="3" opacity="0.9"/><rect class="dot" x="199.0" y="139.4" width="29.2" height="70.6" rx="3" opacity="0.9"/><rect class="dot" x="246.2" y="169.1" width="29.2" height="40.9" rx="3" opacity="0.9"/><rect class="dot" x="293.3" y="157.0" width="29.2" height="53.0" rx="3" opacity="0.9"/><rect class="dot" x="340.4" y="172.4" width="29.2" height="37.6" rx="3" opacity="0.9"/><rect class="dot" x="387.5" y="169.7" width="29.2" height="40.3" rx="3" opacity="0.9"/><rect class="dot" x="434.6" y="110.3" width="29.3" height="99.7" rx="3" opacity="0.9"/><rect class="dot" x="481.8" y="159.9" width="29.2" height="50.1" rx="3" opacity="0.9"/><rect class="dot" x="528.9" y="148.6" width="29.2" height="61.4" rx="3" opacity="0.9"/><rect class="dot" x="576.0" y="163.4" width="29.2" height="46.6" rx="3" opacity="0.9"/><rect class="dot" x="623.1" y="49.0" width="29.2" height="161.0" rx="3" opacity="0.9"/><line class="curve2" stroke-dasharray="4 4" x1="44" y1="138.2" x2="666" y2="138.2"/><text class="ink" x="378.6" y="129.4" font-size="11.5" text-anchor="middle">ortalama 18.0</text><text class="ink" x="72.3" y="38.9" font-size="11" text-anchor="middle">41.3</text><text class="ink" x="637.7" y="43.0" font-size="11" text-anchor="middle">40.2</text></svg>
  <figcaption>Mevsimsel naifin 28 günlük hatası, 13 farklı başlangıçtan. Yatay eksen eğitimin bittiği gün. İlk ve son deney ötekilerin üç katı: yıl dönümü.</figcaption>
</figure>

| | MAE |
|---|---|
| 13 deneyin ortalaması | 17.95 |
| Standart sapması | 10.94 |
| En iyi deney | 9.39 |
| En kötü deney | 41.29 |
| Bölüm 14'teki tek deney | 11.64 |

Doğru cevap "11.6" değil, "**ortalama 18, döneme göre 9 ile 41 arasında**". İki
kötü deney yılın başında ve sonunda: yıl sonu tırmanışı ve ardından gelen
düşüş. Bu da bir bulgu: temel yöntem en çok yıl dönümünde zorlanıyor.

## 6. İki yöntemi adilce karşılaştırmak

Mevsimsel naif mi, son dört haftanın ortalaması mı?

| Deney düzeni | Mevsimsel naif | Dört hafta ortalaması |
|---|---|---|
| Tek ayrım (5 Kasım) | **11.64** | 14.84 |
| 13 başlangıç, 28 gün arayla | 17.95 | **17.20** |
| 48 başlangıç, 7 gün arayla | **15.05** | 15.42 |

Üç düzen, üç farklı "kazanan". 13 deneyin 5'inde mevsimsel naif, 8'inde öteki
önde. Aradaki fark (0.4–0.8), deneyler arası oynaklığın (11) yanında çok küçük.

Dürüst sonuç: **ikisi berabere.** Tek ayrıma baksaydın "mevsimsel naif %22 daha
iyi" derdin ve yanılırdın.

Bir yöntemin ötekinden iyi olduğunu söylemek için fark **deneylerin çoğunda
aynı yönde** olmalı ve deneyler arası oynaklığa göre küçük kalmamalı.

## 7. Ufka göre hata

Geriye dönük sınama bir şey daha veriyor: her ufuk için ayrı hata. 13 deneyin
hatalarını ufkun haftasına göre ortala:

| Ufuk | 1. hafta | 2. hafta | 3. hafta | 4. hafta |
|---|---|---|---|---|
| Mevsimsel naif MAE | 15.9 | 17.0 | 18.2 | 20.7 |

Kararın hangi ufka bağlıysa o satıra bak. Yarınki vardiyayı planlayan için 1.
hafta, gelecek ayın siparişini veren için 4. hafta önemli; ikisi için en iyi
model aynı olmayabilir.

## 8. Genişleyen ve kayan pencere

Her deneyde eğitim verisi ne kadar geriye gitsin?

<figure class="fig">
<div class="versus">
<div><h4>Genişleyen pencere</h4><p>Eğitim hep en baştan başlar; her deneyde uzar.</p><p>Artısı: bütün veriyi kullanır.</p><p>Eksisi: eski dönemler bugünü temsil etmiyorsa tahmini geriye çeker.</p></div>
<div><h4>Kayan pencere</h4><p>Eğitim sabit uzunlukta; başı da ilerler.</p><p>Artısı: değişen seriye çabuk uyar.</p><p>Eksisi: daha az veri; uzun desenleri göremez.</p></div>
</div>
<figcaption>Yukarıdaki <code>backtest</code> genişleyen pencere. Kayan pencere için <code>train = y.loc[:cut].iloc[-n:]</code>.</figcaption>
</figure>

Ortalama tahmininde fark belirgin: bütün geçmişin ortalaması 53.1, son 56 günün
ortalaması 43.3. Seri büyüdüğü için üç yıl önceki günler bugünün düzeyini
aşağı çekiyor.

## 9. Doğrulama ve test

Bir ayarı (pencere boyu, model türü, katsayı) **hataya bakarak** seçtiğin anda
o hata artık dürüst bir ölçüm değil: en iyi görüneni seçtin, biraz da şansını
seçtin.

Bu yüzden veri üçe bölünür:

<figure class="fig">
<div class="flow">
<span class="node">Eğitim<br>model öğrenir</span><span class="arrow">→</span>
<span class="node">Doğrulama<br>ayarı seçersin</span><span class="arrow">→</span>
<span class="node acc">Test<br>bir kez, sonda ölçersin</span>
</div>
<figcaption>Test verisine göre hiçbir karar verilmez. Verildiği anda test, doğrulamaya dönüşür.</figcaption>
</figure>

Örnek: "son `k` haftanın ortalaması" yönteminde `k` kaç olsun? 13 deneyin ilk
10'u doğrulama, son 3'ü test:

| `k` | Doğrulama MAE | Test MAE |
|---|---|---|
| 1 | 16.61 | **22.42** |
| 2 | 15.84 | 22.50 |
| 3 | **15.16** | 22.97 |
| 5 | 15.40 | 25.13 |
| 8 | 16.17 | 29.76 |

Doğrulamaya göre `k = 3` seçilir. Raporlanacak sayı doğrulamadaki 15.16 değil,
testteki **22.97**. Test tablosuna bakıp "aslında `k = 1` daha iyiymiş" diyerek
22.42'yi raporlamak hile: o kararı test verisini görerek verdin.

(Test neden bu kadar kötü? Son üç deney yılın son çeyreği, yani en zor dönem.
Doğrulama ile testin zorluğu aynı olmak zorunda değil; bu da raporda yazılır.)

## 10. Sızıntı denetimi

Doğrulamadaki en tehlikeli hata, modelin tahmin anında bilemeyeceği bir şeyi
görmesi. Sonuç inanılmaz iyi çıkar ve gerçek kullanımda çöker.

1. **Ayrım zamana göre mi?** Rastgele karıştırma yok.
2. **Her sayı yalnızca eğitimden mi?** Ortalama, ölçek, büyüme oranı, mevsim
   çarpanı: hepsi her deneyde `train` üzerinden yeniden hesaplanır.
3. **Özellikler geriye mi bakıyor?** `shift(1)` önce, sonra `rolling`.
   `center=True`, `shift(-k)`, `interpolate`, `bfill` yok.
4. **Ön işleme deneyin içinde mi?** Aykırı değer düzeltme, doldurma,
   ayrıştırma bütün seriye bir kez uygulanmışsa gelecek sızmıştır.
5. **Ufuk gerçekçi mi?** 28 gün ilerisini tahmin edeceksen dünkü değeri
   kullanan bir özellik tahmin anında elinde olmayacak.

scikit-learn aynı bölmeyi hazır veriyor:

```python
from sklearn.model_selection import TimeSeriesSplit

splitter = TimeSeriesSplit(n_splits=5, test_size=28)
for train_idx, test_idx in splitter.split(s):
    train, test = s.iloc[train_idx], s.iloc[test_idx]
```

Test blokları art arda, sondan geriye doğru diziliyor; eğitim her seferinde
testten önceki her şey. Bölüm 19'da makine öğrenmesi modellerini bununla
sınayacaksın.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Tek bir ayrıma güvenmek | Şanslı ya da şanssız dönemin sayısı | Kayan başlangıçla çok deney |
| Yalnızca ortalamayı raporlamak | Oynaklık gizlenir | Ortalama, yayılım, en kötü deney |
| Küçük farkla "kazanan" ilan etmek | Gürültüyü bulgu sanmak | Fark deneylerin çoğunda aynı yönde mi? |
| Sıfır içeren seride MAPE | `inf` ya da sessizce atlanan günler | MAE ya da MASE |
| Farklı ölçekteki serilerde MAE karşılaştırmak | Anlamsız | MASE |
| Testte ayar seçmek | İyimser, tekrarlanamaz sonuç | Ayar doğrulamada, rapor testte |
| Ön işlemeyi bütün seriye bir kez uygulamak | Sızıntı | Her deneyde yalnızca eğitim verisine |
| Tek adımlı hatayı çok adımlı kullanım için raporlamak | Gerçekte çok daha kötü | Kullanılacak ufukta ölç |

## Özet

- **MAE** okunaklı ve dayanıklı; **RMSE** büyük hatayı cezalandırır; **MAPE**
  birimsiz ama sıfırda ve küçük değerlerde bozulur; **MASE** birimsiz ve
  sağlam, 1'in altı naiften iyi. **Yanlılık** yönü gösterir.
- Tek ayrım bir deneydir. **Kayan başlangıç** çok deney yapar; ortalamayı,
  yayılımı ve en kötü durumu birlikte raporla.
- İki yöntem arasındaki fark, deneyler arası oynaklıktan küçükse **berabere**.
- Hata **ufka göre** ayrı ayrı bakılır.
- **Genişleyen** pencere bütün veriyi, **kayan** pencere yalnızca yakın geçmişi
  kullanır.
- Ayar **doğrulamada** seçilir, sonuç **testte** bir kez ölçülür.
- İnanılmaz iyi sonuç = önce **sızıntı** ara.

Düzenek hazır. Bölüm 16'da ilk gerçek modelini kuruyorsun: düzeyi, trendi ve
mevsimi birlikte izleyen üstel düzleştirme. Notunu bu bölümün araçları verecek.
