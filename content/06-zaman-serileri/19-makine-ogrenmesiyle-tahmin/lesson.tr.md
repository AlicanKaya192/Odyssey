# Makine Öğrenmesiyle Tahmin

Bölüm 18'in sonunda elinde bir tablo vardı: her satır bir gün, her sütun o gün
hakkında bir bilgi. Makine Öğrenmesi patikasındaki bütün modeller tam olarak
böyle bir tabloyla çalışır.

Bu bölümde tahmini bir **tablo problemine** çeviriyorsun. İyi haber: doğrusal
regresyondan gradyan artırmaya bildiğin her model kullanılabilir. Kötü haber:
zaman serisine özgü üç tuzak var ve üçü de sessiz. Sonuçlar da beklediğin gibi
çıkmayabilir: bu bölümün en önemli dersi, **kazancın modelden değil
özelliklerden geldiği**.

## 1. Seriyi tabloya çevirmek

Bir zaman serisi tek sütundur. Modelin öğrenebilmesi için her günün yanına, o
günü **tahmin ederken elinde olacak** bilgileri yazarsın.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Gecikmeler</span><span>Serinin geçmiş değerleri: dün, geçen hafta aynı gün. <code>shift(k)</code></span></div>
<div class="anat-row"><span>Pencereler</span><span>Yakın geçmişin özeti: son 7 günün ortalaması. <code>shift(1).rolling(n)</code></span></div>
<div class="anat-row"><span>Takvim</span><span>Haftanın günü, ay, tatil, Fourier terimleri. Geleceği belli.</span></div>
<div class="anat-row"><span>Dış değişkenler</span><span>Kampanya, fiyat, sıcaklık (Bölüm 18).</span></div>
</div>
<figcaption>Dört özellik ailesi. Hedef sütun, o günün değeri.</figcaption>
</figure>

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    X = pd.DataFrame(index=y.index)
    for k in (1, 2, 7, 14):
        X[f"lag{k}"] = y.shift(k)
    X["mean7"] = y.shift(1).rolling(7).mean()
    X["mean28"] = y.shift(1).rolling(28).mean()
    X["dow"] = y.index.dayofweek
    X["month"] = y.index.month
    return X


table = features(s).join(s.rename("y")).dropna()
print(table.shape, table.index[0].date())      # (1068, 9) 2022-01-29
```

İlk 28 satır gitti: `mean28` için geçmiş yetmiyor. Her gecikme ve pencere
başta satır kaybettirir.

`mean7`'de **önce `shift(1)`, sonra `rolling`**: Bölüm 07 ve 14'teki kural.
Yoksa "son 7 günün ortalaması" tahmin edilecek günü de içerir.

## 2. İlk model

Tablo hazır olunca gerisi tanıdık. Eğitim 2023 sonuna kadar, test 2024; her
gün **bir gün sonrası** tahmin ediliyor:

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression

train, test = table.loc[:"2023"], table.loc["2024"]
columns = [c for c in table.columns if c != "y"]

model = LinearRegression().fit(train[columns], train["y"])
predicted = model.predict(test[columns])
```

| Yöntem | Test MAE | Eğitim MAE |
|---|---|---|
| Naif | 41.10 | |
| Mevsimsel naif | 13.87 | |
| Doğrusal regresyon | **11.51** | 10.89 |
| Rastgele orman | 12.87 | 4.31 |
| Gradyan artırma | 14.63 | 4.79 |

Üç gözlem:

- Doğrusal model mevsimsel naifi %17 geçiyor.
- **En basit model en iyisi.** Ağaç tabanlı iki model doğrusal regresyonun
  gerisinde; gradyan artırma mevsimsel naifi bile geçemiyor.
- Ağaçların eğitim hatası (4–5) test hatasının üçte biri: **ezber**. 700
  satırlık bir tablo, binlerce yaprağı olan bir modeli beslemeye yetmiyor.

Bu sonuç bir kaza değil; bir sonraki kısım nedenini gösteriyor.

## 3. Ağaçlar düzeyi uzatamaz

Bir karar ağacı, tahmin olarak **eğitimde gördüğü değerlerin ortalamasını**
verir. Eğitimde gördüğü en yüksek değerden daha yükseğini söyleyemez.

Mağaza büyüyor. Eğitim verisindeki en yüksek satış 462; Aralık 2024'te 503'e
çıkılıyor.

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="234.6" x2="666" y2="234.6"/><text class="dim" x="38" y="238.1" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="202.5" x2="666" y2="202.5"/><text class="dim" x="38" y="206.0" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="170.4" x2="666" y2="170.4"/><text class="dim" x="38" y="173.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="138.2" x2="666" y2="138.2"/><text class="dim" x="38" y="141.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="106.1" x2="666" y2="106.1"/><text class="dim" x="38" y="109.6" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="74.0" x2="666" y2="74.0"/><text class="dim" x="38" y="77.5" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="41.9" x2="666" y2="41.9"/><text class="dim" x="38" y="45.4" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">18 Kas</text><line class="line" x1="145.3" y1="240" x2="145.3" y2="244"/><text class="dim" x="145.3" y="256" font-size="10.5" text-anchor="middle">25 Kas</text><line class="line" x1="246.5" y1="240" x2="246.5" y2="244"/><text class="dim" x="246.5" y="256" font-size="10.5" text-anchor="middle">2 Ara</text><line class="line" x1="347.8" y1="240" x2="347.8" y2="244"/><text class="dim" x="347.8" y="256" font-size="10.5" text-anchor="middle">9 Ara</text><line class="line" x1="449.0" y1="240" x2="449.0" y2="244"/><text class="dim" x="449.0" y="256" font-size="10.5" text-anchor="middle">16 Ara</text><line class="line" x1="550.3" y1="240" x2="550.3" y2="244"/><text class="dim" x="550.3" y="256" font-size="10.5" text-anchor="middle">23 Ara</text><line class="line" x1="651.5" y1="240" x2="651.5" y2="244"/><text class="dim" x="651.5" y="256" font-size="10.5" text-anchor="middle">30 Ara</text><line class="curve3" stroke-dasharray="4 4" x1="44" y1="98.4" x2="666" y2="98.4"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,219.9 58.5,215.4 72.9,215.4 87.4,192.9 101.9,159.5 116.3,127.3 130.8,149.2 145.3,222.4 159.7,210.9 174.2,204.4 188.7,204.4 203.1,179.4 217.6,117.7 232.0,142.7 246.5,222.4 261.0,208.9 275.4,196.7 289.9,193.5 304.4,165.9 318.8,106.8 333.3,131.8 347.8,206.4 362.2,191.6 376.7,201.9 391.2,163.3 405.6,145.3 420.1,96.5 434.6,116.4 449.0,201.9 463.5,197.4 478.0,187.7 492.4,189.7 506.9,132.5 521.3,81.1 535.8,119.0 550.3,198.7 564.7,174.2 579.2,176.8 593.7,166.5 608.1,122.8 622.6,72.1 637.1,110.0 651.5,177.4 666.0,172.3"/><polyline class="curve" style="stroke-width:2" points="44.0,212.2 58.5,217.9 72.9,201.2 87.4,193.8 101.9,159.8 116.3,121.9 130.8,143.3 145.3,212.5 159.7,214.5 174.2,201.8 188.7,190.7 203.1,156.2 217.6,130.5 232.0,139.4 246.5,213.8 261.0,208.8 275.4,202.7 289.9,191.2 304.4,164.7 318.8,122.0 333.3,138.2 347.8,213.5 362.2,204.2 376.7,192.6 391.2,190.8 405.6,164.4 420.1,111.0 434.6,129.0 449.0,204.3 463.5,194.5 478.0,190.6 492.4,171.0 506.9,150.9 521.3,100.5 535.8,116.8 550.3,195.9 564.7,189.2 579.2,185.2 593.7,168.5 608.1,134.3 622.6,88.2 637.1,109.8 651.5,190.9 666.0,179.3"/><polyline class="curve2" style="stroke-width:2" points="44.0,206.2 58.5,208.3 72.9,204.7 87.4,198.5 101.9,149.9 116.3,137.3 130.8,139.5 145.3,209.0 159.7,205.6 174.2,199.5 188.7,188.4 203.1,149.7 217.6,140.7 232.0,130.1 246.5,207.3 261.0,206.1 275.4,204.7 289.9,195.0 304.4,156.5 318.8,128.1 333.3,132.2 347.8,207.3 362.2,207.3 376.7,193.3 391.2,186.6 405.6,147.3 420.1,132.2 434.6,132.2 449.0,206.2 463.5,190.0 478.0,196.5 492.4,165.2 506.9,142.4 521.3,130.1 535.8,132.2 550.3,204.0 564.7,191.4 579.2,185.5 593.7,164.8 608.1,135.9 622.6,132.2 637.1,132.2 651.5,193.9 666.0,184.6"/><text class="dim" x="48.3" y="94.6" font-size="11" text-anchor="start">eğitimdeki en yüksek değer: 462</text><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">doğrusal regresyon</text><line class="curve2" x1="314" y1="40" x2="332" y2="40"/><text class="ink" x="338" y="44" font-size="11">gradyan artırma</text></svg>
  <figcaption>Aralık 2024, bir gün sonrası tahminleri. Kesik çizgi eğitim verisindeki en yüksek satış. Gradyan artırma o çizginin epey altında kalıyor; cumartesi tepelerini doğrusal model izliyor, ağaç izleyemiyor.</figcaption>
</figure>

| | En yüksek değer | Aralık 2024 MAE |
|---|---|---|
| Gerçek (Aralık 2024) | 503 | |
| Doğrusal regresyon tahmini | 478 | 14.52 |
| Gradyan artırma tahmini | 416 | 22.47 |

Gradyan artırmanın tahmini 416'da **tavana vuruyor**. En yüksek 20 günde
ortalama 27 birim düşük kalıyor. Doğrusal model ise `lag7` büyüdükçe tahminini
de büyütebiliyor.

Bu, trendli her seride ağaç tabanlı modellerin temel sorunu. Çözüm Bölüm 11'den
tanıdık: **düzeyi değil, değişimi tahmin et.**

```python
target = table["y"] - table["lag7"]          # gecen haftaya gore degisim
# model bu farki ogrenir; tahmin = model ciktisi + lag7
```

Hedef fark olunca gradyan artırmanın test hatası 14.63'ten 11.74'e, Aralık
hatası 22.47'den 10.87'ye iniyor. Fark durağan; ağacın uzatması gereken bir
düzey kalmıyor.

## 4. Doğrulama: karıştırma yok

scikit-learn'ün varsayılan çapraz doğrulaması satırları **karıştırır**. Zaman
serisinde bu, modelin 15 Mart'ı tahmin ederken 14 ve 16 Mart'ı eğitimde görmesi
demek.

```python
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score

model = HistGradientBoostingRegressor(random_state=0)
for cv in (KFold(5, shuffle=True, random_state=0), TimeSeriesSplit(5)):
    scores = -cross_val_score(model, table[columns], table["y"], cv=cv,
                              scoring="neg_mean_absolute_error")
    print(round(scores.mean(), 2))
# 11.88   15.78
```

Aynı model, aynı veri: karıştırılmış doğrulama 11.88, zamana göre doğrulama
15.78. Birincisi modelin **geçmişteki boşlukları doldurma** becerisini ölçüyor;
ikincisi **geleceği tahmin etme** becerisini. Senin işin ikincisi.

`TimeSeriesSplit` Bölüm 15'teki kayan başlangıcın hazır hâli: her parçada
eğitim testten önce.

## 5. Sızıntı: tek satırlık hata

```python
X["mean7"] = y.rolling(7).mean()              # shift(1) unutuldu
```

Bu tek satırla doğrusal modelin test hatası 11.51'den 10.55'e "iyileşiyor".
Hiçbir uyarı yok, kod çalışıyor, sonuç daha iyi. Oysa özellik, tahmin edilecek
günün kendisini içeriyor.

Her özellik için tek bir soru: **bu sayıyı, tahmini yaptığım anda
hesaplayabilir miydim?** Beklenmedik bir iyileşme gördüğünde önce bunu sor.

## 6. Çok adımlı tahmin: üç yol

Buraya kadar hep yarını tahmin ettin. 28 gün ilerisi için `lag1` elinde yok:
27 gün sonrasının dünü henüz yaşanmadı.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Özyinelemeli</span><span>Yarını tahmin et, tahmini veri say, öbür günü tahmin et. Tek model; hatalar <b>birikir</b>.</span></div>
<div class="anat-row"><span>Doğrudan, güvenli özellikler</span><span>Yalnızca ufuk kadar eski bilgileri kullan: <code>lag28</code>, <code>lag35</code>, takvim. Tek model; hata birikmez.</span></div>
<div class="anat-row"><span>Doğrudan, ufuk başına model</span><span>Her ufuk için ayrı model: 1 gün, 2 gün, ..., 28 gün. En esnek; en pahalı.</span></div>
</div>
<figcaption>28 günlük ufukta "güvenli" özellik: en az 28 gün eski olan her şey ve takvim.</figcaption>
</figure>

İkinci yol en yalını. Özellikler:

```python
def safe_features(full):
    X = pd.DataFrame(index=full.index)
    for k in (28, 35, 42, 56):
        X[f"lag{k}"] = full.shift(k)
    X["level28"] = full.shift(28).rolling(28).mean()
    X["dow"] = X.index.dayofweek
    # + takvim: gun sayaci, Aralik tirmanisi, Fourier terimleri (Bolum 18)
    return X
```

`lag28`, tahmin edilecek günle **aynı haftanın günü**: 28, 7'nin katı. Haftalık
desen bu yüzden korunuyor.

## 7. Sınama: hepsi bir arada

Bölüm 15'in düzeneği: 13 başlangıç, 28 günlük ufuk.

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="206.0" x2="666" y2="206.0"/><text class="dim" x="38" y="209.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="163.1" x2="666" y2="163.1"/><text class="dim" x="38" y="166.6" font-size="10.5" text-anchor="end">5</text><line class="grid" x1="44" y1="120.3" x2="666" y2="120.3"/><text class="dim" x="38" y="123.8" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="77.4" x2="666" y2="77.4"/><text class="dim" x="38" y="80.9" font-size="10.5" text-anchor="end">15</text><line class="grid" x1="44" y1="34.6" x2="666" y2="34.6"/><text class="dim" x="38" y="38.1" font-size="10.5" text-anchor="end">20</text><line class="line" x1="44" y1="206" x2="666" y2="206"/><line class="line" x1="104.2" y1="206" x2="104.2" y2="210"/><text class="dim" x="104.2" y="222" font-size="10.5" text-anchor="middle">mevsimsel naif</text><line class="line" x1="204.5" y1="206" x2="204.5" y2="210"/><text class="dim" x="204.5" y="222" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="304.8" y1="206" x2="304.8" y2="210"/><text class="dim" x="304.8" y="222" font-size="10.5" text-anchor="middle">ARIMA</text><line class="line" x1="405.2" y1="206" x2="405.2" y2="210"/><text class="dim" x="405.2" y="222" font-size="10.5" text-anchor="middle">gradyan art. + takvim</text><line class="line" x1="505.5" y1="206" x2="505.5" y2="210"/><text class="dim" x="505.5" y="222" font-size="10.5" text-anchor="middle">doğrusal + takvim</text><line class="line" x1="605.8" y1="206" x2="605.8" y2="210"/><text class="dim" x="605.8" y="222" font-size="10.5" text-anchor="middle">ARIMA + takvim</text><rect class="dot2" x="73.1" y="52.1" width="62.2" height="153.9" rx="3" opacity="0.9"/><rect class="dot2" x="173.4" y="69.6" width="62.2" height="136.4" rx="3" opacity="0.9"/><rect class="dot2" x="273.7" y="69.4" width="62.2" height="136.6" rx="3" opacity="0.9"/><rect class="dot" x="374.1" y="87.7" width="62.2" height="118.3" rx="3" opacity="0.9"/><rect class="dot" x="474.4" y="114.8" width="62.2" height="91.2" rx="3" opacity="0.9"/><rect class="dot" x="574.7" y="118.3" width="62.2" height="87.7" rx="3" opacity="0.9"/><text class="ink" x="104.2" y="46.1" font-size="11.5" text-anchor="middle">17.9</text><text class="ink" x="204.5" y="63.6" font-size="11.5" text-anchor="middle">15.9</text><text class="ink" x="304.8" y="63.4" font-size="11.5" text-anchor="middle">15.9</text><text class="ink" x="405.2" y="81.7" font-size="11.5" text-anchor="middle">13.8</text><text class="ink" x="505.5" y="108.8" font-size="11.5" text-anchor="middle">10.6</text><text class="ink" x="605.8" y="112.3" font-size="11.5" text-anchor="middle">10.2</text></svg>
  <figcaption>13 deneyin ortalama MAE'si, 28 günlük ufuk. Turuncu: yalnızca serinin geçmişi. Mor: takvim bilgisiyle. Basamağı model türü değil, bilgi atlatıyor.</figcaption>
</figure>

| Yöntem | Ortalama MAE | En kötü deney |
|---|---|---|
| Mevsimsel naif | 17.95 | 41.3 |
| Holt–Winters | 15.91 | 38.6 |
| ARIMA | 15.94 | 52.2 |
| ARIMA + takvim | 10.23 | 14.4 |
| Özyinelemeli doğrusal (takvimsiz) | 16.66 | 45.4 |
| Doğrudan doğrusal, **takvimsiz** | 18.98 | 41.4 |
| Doğrudan gradyan artırma, **takvimsiz** | 27.09 | 63.6 |
| Doğrudan gradyan artırma + takvim | 13.80 | 21.1 |
| **Doğrudan doğrusal + takvim** | **10.64** | 16.9 |

Tabloyu dikkatle oku:

**Özellikler modelden önemli.** Aynı doğrusal model takvimsiz 18.98, takvimle
10.64. Aynı gradyan artırma 27.09 ve 13.80. Model değiştirmek en fazla 3 puan
oynatıyor; özellik eklemek 8–13 puan.

**Makine öğrenmesi mucize değil.** En iyi makine öğrenmesi sonucu (10.64),
aynı takvim bilgisini alan ARIMA ile (10.23) başa baş. Takvimsiz hâlleri
mevsimsel naiften **kötü**.

**Karmaşık model bu veride kaybediyor.** Tek bir seri, bin satır, belirgin bir
trend: gradyan artırmanın güçlü olduğu koşullar bunlar değil.

## 8. Peki ne zaman makine öğrenmesi?

| Durum | Neden |
|---|---|
| **Çok sayıda seri** (yüzlerce ürün, mağaza) | Tek model hepsinden öğrenir; her seriye ayrı ARIMA kurulmaz |
| **Çok sayıda dış değişken** | Ağaçlar onlarca sütunu ve aralarındaki etkileşimi kendisi bulur |
| **Doğrusal olmayan etkiler** | "Sıcaklık 25'i geçince satış düşer" gibi eşikler |
| **Kısa geçmişli yeni seriler** | Benzer serilerden öğrenilen desen aktarılır |
| **Uzun, zengin veri** | On binlerce satır ezberi zorlaştırır |

Tek, kısa, düzenli bir seride klasik yöntemler (Bölüm 16–18) çoğu zaman yeter
ve daha az bakım ister. Sıra hep aynı: **temel yöntem → klasik model → gerekirse
makine öğrenmesi**, hepsi aynı düzenekte.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `rolling`'den önce `shift` unutmak | Sızıntı; sahte iyileşme | `y.shift(1).rolling(n)` |
| Karıştırılmış çapraz doğrulama | İyimser hata | `TimeSeriesSplit` |
| Ufuktan kısa gecikmeler | Tahmin anında olmayan bilgi | `h` adım için en az `h` gecikme |
| Trendli seride ağaçla düzeyi tahmin etmek | Tahmin tavana vurur | Hedefi fark ya da oran yap |
| Ölçekleyiciyi bütün veride kurmak | Test bilgisi eğitime sızar | Yalnızca eğitimde `fit` |
| Eğitim hatasına bakıp sevinmek | Ezber | Örnek dışı hata, kayan başlangıç |
| Temel yöntemle karşılaştırmamak | Kazanç sanılan kayıp | Aynı düzenekte mevsimsel naif |
| Yalnızca modeli değiştirip durmak | Küçük oynamalar | Önce özellikleri zenginleştir |

## Özet

- Tahmin bir **tablo problemine** çevrilir: gecikmeler, pencereler, takvim, dış
  değişkenler; hedef o günün değeri.
- Her özellik tahmin anında **hesaplanabilir** olmalı: `shift` önce, gecikme en
  az ufuk kadar.
- **Ağaçlar düzeyi uzatamaz**; trendli seride hedefi farka çevir.
- Doğrulama **zamana göre**: `TimeSeriesSplit`, kayan başlangıç.
- Çok adımlı tahmin: özyinelemeli (hata birikir), güvenli özelliklerle doğrudan,
  ya da ufuk başına model.
- Bu seride en iyi sonuç **doğrusal model + takvim**: 10.64. Gradyan artırma
  geride; takvimsiz her model mevsimsel naiften kötü.
- **Kazanç özelliklerden gelir.** Makine öğrenmesi çok serili, çok değişkenli
  problemlerde öne çıkar.

Şimdiye kadar her tahmin tek bir sayıydı. Oysa "yarın 310 satılacak" demek
yetmez; "280 ile 340 arasında" demek gerekir. Sıradaki bölüm belirsizliği ölçüyor.
