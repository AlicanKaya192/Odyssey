# Genel Tekrar

Yirmi iki bölüm boyunca tek tek araçlar öğrendin: tarih okumak, yeniden
örneklemek, ayrıştırmak, tahmin etmek, aralık vermek, anomali yakalamak. Bu
bölümde yeni bir araç yok. Hepsini **tek bir işte**, baştan sona kullanıyorsun.

İş şu: bir şehrin bisiklet kiralama sistemi, üç yıllık günlük kiralama dökümünü
veriyor ve soruyor: **önümüzdeki 28 günde her gün kaç bisiklet kiralanacak?**

## Akış

<figure class="fig">
<div class="flow">
<span class="node">Ham döküm</span><span class="arrow">→</span>
<span class="node">Düzenli seri</span><span class="arrow">→</span>
<span class="node">Tanı</span><span class="arrow">→</span>
<span class="node">Taban çizgi</span><span class="arrow">→</span>
<span class="node">Düzenek</span><span class="arrow">→</span>
<span class="node">Model</span><span class="arrow">→</span>
<span class="node">Aralık</span><span class="arrow">→</span>
<span class="node acc">İzleme</span>
</div>
<figcaption>Her zaman serisi işi bu sırayla ilerler. Adımları atlamak cazip; en pahalı hatalar atlanan adımlardan çıkar.</figcaption>
</figure>

## 1. Ham dökümden düzenli seriye

Döküm (`bike_raw.csv`) gerçek hayattaki gibi geliyor: tarihler `29.01.2022`
biçiminde, satırlar sırasız, bazı günler iki kez yazılmış, bazıları hiç yok.

```python
import pandas as pd

raw = pd.read_csv("bike_raw.csv")
raw["date"] = pd.to_datetime(raw["date"], format="%d.%m.%Y")     # Bolum 02

print(len(raw), int(raw.duplicated().sum()))                     # 1093 6

rentals = raw.drop_duplicates().set_index("date")["rentals"]
rentals = rentals.sort_index().asfreq("D")                       # Bolum 03

print(int(rentals.isna().sum()))                                 # 9
```

Üç karar, üçü de önceki bölümlerden:

- **Biçimi açıkça yaz** (`format=`). Yazılmasaydı `03.04.2022` Mart mı Nisan mı,
  pandas'ın tahminine kalırdı.
- **`asfreq("D")` eksikleri görünür kılar.** Dokuz gün eksik; en uzun boşluk
  dört gün. `asfreq` çağrılmasaydı bu günler sessizce atlanır, `shift(7)` "yedi
  satır önce"yi "yedi gün önce" sanırdı.
- **Aykırı değere bak.** En düşük değer 16 Temmuz 2024'te 9 kiralama; bir hafta
  önce 600, bir hafta sonra 311. Sistem arızası: gerçek talep değil, eksik
  sayılır.

Eksik günler ve arıza günü, bir hafta öncesi ile sonrasının ortalamasıyla
dolduruldu (Bölüm 13). Sonuç: 1096 günlük, boşluksuz bir seri.

## 2. Seriyi tanı

Model kurmadan önce seriye bak (Bölüm 05–12):

| Soru | Araç | Bulgu |
|---|---|---|
| Büyüyor mu? | `resample("YS").sum()` | Yılda +%14.8, +%11.5 |
| Haftalık desen? | `groupby(dayofweek).mean()` | Cumartesi, pazartesinin 1.35 katı |
| Yıllık desen? | `groupby(month).mean()` | Temmuz, Ocak'ın 2.4 katı |
| Durağan mı? | `adfuller` | Düzeyde p = 0.33 (değil); farkı alınınca 0.00 |
| Dış etken? | Hava verisiyle birleştir | Yağmurlu gün, kuru günün 0.55'i |

Üç şey öğrenildi: iki mevsimsellik var (haftalık ve yıllık), salınım düzeyle
birlikte büyüyor (çarpımsal: **logaritma**), ve seriyi en çok oynatan şey
**yağmur**. Sonuncusu işin geri kalanını belirleyecek.

## 3. Taban çizgi ve düzenek

Önce yenilmesi gereken sayı (Bölüm 14), sonra onu ölçecek düzenek (Bölüm 15):
2024 boyunca 13 başlangıç, her birinde 28 günlük tahmin.

| Yöntem | MAE | En kötü deney |
|---|---|---|
| Naif (son değer) | 112.2 | 234.9 |
| Mevsimsel naif (geçen hafta) | 98.6 | 199.1 |
| Son dört haftanın gün ortalaması | 86.9 | 129.7 |

Günlük ortalama kiralama 410 civarında; mevsimsel naif dörtte bir yanılıyor.
Dikkat: bu seride mevsimsel naif zayıf bir taban, çünkü "geçen hafta aynı gün"
yağmurlu olabilir. Dört haftanın ortalaması gürültüyü düzlüyor ve daha iyi.
**Taban çizgiyi de seriye göre seçersin.**

## 4. Model

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.0" x2="666" y2="210.0"/><text class="dim" x="38" y="213.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="172.8" x2="666" y2="172.8"/><text class="dim" x="38" y="176.3" font-size="10.5" text-anchor="end">25</text><line class="grid" x1="44" y1="135.6" x2="666" y2="135.6"/><text class="dim" x="38" y="139.1" font-size="10.5" text-anchor="end">50</text><line class="grid" x1="44" y1="98.4" x2="666" y2="98.4"/><text class="dim" x="38" y="101.9" font-size="10.5" text-anchor="end">75</text><line class="grid" x1="44" y1="61.2" x2="666" y2="61.2"/><text class="dim" x="38" y="64.7" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="24.0" x2="666" y2="24.0"/><text class="dim" x="38" y="27.5" font-size="10.5" text-anchor="end">125</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="104.2" y1="210" x2="104.2" y2="214"/><text class="dim" x="104.2" y="226" font-size="10.5" text-anchor="middle">naif</text><line class="line" x1="204.5" y1="210" x2="204.5" y2="214"/><text class="dim" x="204.5" y="226" font-size="10.5" text-anchor="middle">mevsimsel naif</text><line class="line" x1="304.8" y1="210" x2="304.8" y2="214"/><text class="dim" x="304.8" y="226" font-size="10.5" text-anchor="middle">4 hafta ort.</text><line class="line" x1="405.2" y1="210" x2="405.2" y2="214"/><text class="dim" x="405.2" y="226" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="505.5" y1="210" x2="505.5" y2="214"/><text class="dim" x="505.5" y="226" font-size="10.5" text-anchor="middle">takvim</text><line class="line" x1="605.8" y1="210" x2="605.8" y2="214"/><text class="dim" x="605.8" y="226" font-size="10.5" text-anchor="middle">takvim + gerçek hava</text><rect class="dim" x="73.1" y="43.0" width="62.2" height="167.0" rx="3" opacity="0.9"/><rect class="dim" x="173.4" y="63.3" width="62.2" height="146.7" rx="3" opacity="0.9"/><rect class="dim" x="273.7" y="80.7" width="62.2" height="129.3" rx="3" opacity="0.9"/><rect class="dot2" x="374.1" y="91.4" width="62.2" height="118.6" rx="3" opacity="0.9"/><rect class="dot" x="474.4" y="113.1" width="62.2" height="96.9" rx="3" opacity="0.9"/><rect class="dot3" x="574.7" y="178.9" width="62.2" height="31.1" rx="3" opacity="0.9"/><text class="ink" x="104.2" y="37.8" font-size="11.5" text-anchor="middle">112.2</text><text class="ink" x="204.5" y="58.1" font-size="11.5" text-anchor="middle">98.6</text><text class="ink" x="304.8" y="75.5" font-size="11.5" text-anchor="middle">86.9</text><text class="ink" x="405.2" y="86.2" font-size="11.5" text-anchor="middle">79.7</text><text class="ink" x="505.5" y="107.9" font-size="11.5" text-anchor="middle">65.1</text><text class="ink" x="605.8" y="173.7" font-size="11.5" text-anchor="middle">20.9</text></svg>
  <figcaption>13 deneyin ortalama MAE'si. Gri: taban çizgiler. Turuncu: Holt–Winters. Mor: gelecekte bilinenlerle kurulabilen en iyi model. Yeşil çubuk bir model değil, bir <b>sınır</b>: hava önceden bilinseydi ne olurdu.</figcaption>
</figure>

| Yöntem | MAE | Bölüm |
|---|---|---|
| Holt–Winters (haftalık mevsim) | 79.7 | 16 |
| Takvim modeli: logaritma üzerinde doğrusal; gün, trend, yıllık Fourier, tatil | **65.1** | 18–19 |
| Takvim + hava (mevsim normalleriyle) | 66.2 | 18 |
| Takvim + hava (**gerçekleşen** hava) | 20.9 | — |

Dört satır, dört ders:

**Holt–Winters yalnızca haftayı biliyor.** 28 günlük ufukta yılın hangi
döneminde olunduğu önemli; yıllık deseni bilen takvim modeli %18 daha iyi.

**Logaritma işe yarıyor.** Aynı model düzey üzerinde kurulunca 67.6. Etkiler
çarpımsal (yağmur kiralamayı 40 azaltmıyor, %38 azaltıyor); logaritma bunu
toplamsal yapıyor.

**Mevsim normali bilgi değildir.** Hava sütunları gelecekte bilinmiyor.
Yerlerine mevsim normali konunca (o günün ortalama sıcaklığı, o ayın yağmur
oranı) hata düşmüyor: normal zaten Fourier terimlerinin içinde. Bölüm 18'in
kuralı: gelecekte **bilmediğin** değişken, modeli iyileştirmez.

**Kalan hata modelin değil, bilginin eksiği.** Hava gerçekten bilinseydi hata
65'ten 21'e inerdi. Daha karmaşık bir model (ağaçlar, ARIMA) bu farkı kapatamaz;
çünkü eksik olan yöntem değil, **yağmurun yağıp yağmayacağı**. Bir ay sonrasının
yağmurunu kimse bilemez.

Bu, patikanın en önemli dersi: modeli değiştirmeden önce **hatanın nereden
geldiğini** sor.

## 5. Belirsizliği söyle

Nokta tahmini %16 yanılıyor ve nedenini biliyorsun. Dürüst olan, bunu aralıkla
söylemek (Bölüm 20). 13 deneyin oransal hatalarından:

| | Değer |
|---|---|
| Ortalama oransal hata | +%0.3 (yansız) |
| %10 yüzdeliği | −%31 |
| %90 yüzdeliği | +%26 |
| %80 aralığın kapsaması (her deney, öbür 12 deneyin hatalarıyla) | 0.80 |

Aralık geniş ve **simetrik değil**: aşağı doğru daha uzun. Nedeni yine yağmur:
modelin hatası yağmurlu günlerde ortalama −%28, kuru günlerde +%11. Model her
gün için "ortalama bir gün" tahmin ediyor; gerçek günler ya kuru ya yağmurlu.

Ocak 2025'in ilk 28 günü için tahmin:

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="219.3" x2="666" y2="219.3"/><text class="dim" x="38" y="222.8" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="188.0" x2="666" y2="188.0"/><text class="dim" x="38" y="191.5" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="156.6" x2="666" y2="156.6"/><text class="dim" x="38" y="160.1" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="125.3" x2="666" y2="125.3"/><text class="dim" x="38" y="128.8" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="94.0" x2="666" y2="94.0"/><text class="dim" x="38" y="97.5" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="62.6" x2="666" y2="62.6"/><text class="dim" x="38" y="66.1" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="31.3" x2="666" y2="31.3"/><text class="dim" x="38" y="34.8" font-size="10.5" text-anchor="end">600</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="89.1" y1="230" x2="89.1" y2="234"/><text class="dim" x="89.1" y="246" font-size="10.5" text-anchor="middle">25 Kas</text><line class="line" x1="215.3" y1="230" x2="215.3" y2="234"/><text class="dim" x="215.3" y="246" font-size="10.5" text-anchor="middle">9 Ara</text><line class="line" x1="341.5" y1="230" x2="341.5" y2="234"/><text class="dim" x="341.5" y="246" font-size="10.5" text-anchor="middle">23 Ara</text><line class="line" x1="467.7" y1="230" x2="467.7" y2="234"/><text class="dim" x="467.7" y="246" font-size="10.5" text-anchor="middle">6 Oca</text><line class="line" x1="593.9" y1="230" x2="593.9" y2="234"/><text class="dim" x="593.9" y="246" font-size="10.5" text-anchor="middle">20 Oca</text><polygon class="dot" opacity="0.2" style="stroke:none" points="422.6,118.7 431.6,116.0 440.6,112.9 449.7,89.2 458.7,108.2 467.7,123.9 476.7,119.1 485.7,119.7 494.7,117.0 503.7,113.9 512.8,90.2 521.8,109.0 530.8,124.5 539.8,119.6 548.8,120.2 557.8,117.3 566.8,114.1 575.9,90.5 584.9,109.1 593.9,124.5 602.9,119.5 611.9,120.0 620.9,117.1 629.9,113.8 639.0,89.9 648.0,108.5 657.0,123.9 666.0,118.8 666.0,164.0 657.0,166.9 648.0,158.4 639.0,148.2 629.9,161.3 620.9,163.1 611.9,164.7 602.9,164.5 593.9,167.2 584.9,158.7 575.9,148.5 566.8,161.5 557.8,163.3 548.8,164.8 539.8,164.5 530.8,167.2 521.8,158.7 512.8,148.4 503.7,161.3 494.7,163.1 485.7,164.6 476.7,164.2 467.7,166.9 458.7,158.2 449.7,147.8 440.6,160.8 431.6,162.5 422.6,164.0"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,100.9 53.0,82.7 62.0,74.5 71.0,70.2 80.1,91.2 89.1,145.7 98.1,104.0 107.1,115.0 116.1,114.6 125.1,152.6 134.1,81.8 143.2,144.1 152.2,155.1 161.2,119.3 170.2,101.5 179.2,102.4 188.2,85.5 197.2,119.0 206.3,92.1 215.3,129.4 224.3,126.2 233.3,142.5 242.3,114.0 251.3,162.3 260.3,81.8 269.4,124.4 278.4,131.6 287.4,130.6 296.4,131.9 305.4,136.0 314.4,155.4 323.4,104.0 332.5,151.0 341.5,129.7 350.5,163.5 359.5,126.6 368.5,158.8 377.5,153.8 386.6,137.2 395.6,102.7 404.6,126.6 413.6,162.0"/><polyline class="curve" style="stroke-width:2.2" points="422.6,139.3 431.6,137.1 440.6,134.7 449.7,115.8 458.7,130.9 467.7,143.5 476.7,139.6 485.7,140.1 494.7,137.9 503.7,135.5 512.8,116.7 521.8,131.6 530.8,143.9 539.8,140.0 548.8,140.5 557.8,138.2 566.8,135.7 575.9,116.9 584.9,131.7 593.9,143.9 602.9,140.0 611.9,140.3 620.9,138.0 629.9,135.4 639.0,116.4 648.0,131.2 657.0,143.4 666.0,139.4"/><line class="curve3" stroke-dasharray="4 4" x1="418.1" y1="30" x2="418.1" y2="230"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">gerçekleşen</text><line class="curve" x1="177" y1="38" x2="195" y2="38"/><text class="ink" x="201" y="42" font-size="11">tahmin</text><rect class="dot" x="265" y="33" width="18" height="10" opacity="0.3"/><text class="ink" x="289" y="42" font-size="11">%80 aralık</text></svg>
  <figcaption>2024'ün son altı haftası ve Ocak 2025'in ilk 28 günü. Geçmişteki sert inişler yağmurlu günler; tahmin onları bilemediği için düz bir haftalık desen çiziyor ve belirsizliği bantla söylüyor.</figcaption>
</figure>

Toplam 7541 kiralama. 1 Ocak için 255, %80 aralık 177–321. Kaç bisikletin
hazır tutulacağı sorusunun cevabı nokta tahmini değil, bir **yüzdelik**:
bisikletsiz kalmak pahalıysa üst uç.

## 6. Teslimden sonra: izle

Tahmin teslim edilince iş bitmez (Bölüm 21):

- **Her gün** gerçekleşeni aralıkla karşılaştır. %80 aralığın dışına beş günde
  bir düşülmesi beklenir; art arda aynı yönde düşülüyorsa bir şey değişmiştir.
- **Hatayı biriktir** (CUSUM): küçük ama kalıcı bir sapma, düzey kaymasıdır.
- **Anomalileri işaretle, eğitimden önce onar**; düzey kaymasından sonra modeli
  yeniden kur.
- **Düzenli yeniden eğit.** Trend yılda %13; bir yıl önceki katsayılar eskir.
- **Kısa ufukta daha iyisini yap.** Yarın için hava tahmini vardır; 28 günlük
  tahmin ile yarınki tahmin aynı model olmak zorunda değil.

## Bölüm bölüm

| Bölüm | Akılda kalacak tek şey |
|---|---|
| 00 Zaman Serisi Nedir? | Sıra bilgidir; satırları karıştıramazsın |
| 01 Tarih ve Saat | `datetime` bir an, `timedelta` bir süre |
| 02 pandas'ta Tarihler | Biçimi açıkça yaz; bozuk tarihi `errors="coerce"` ile gör |
| 03 Zaman İndeksi | İndeks tarih olunca dilimleme, hizalama, `asfreq` gelir |
| 04 Periyotlar ve Takvimler | An ile dönem farklı; iş günü ve tatil takvimi |
| 05 Yeniden Örnekleme | Sıklık değişince **nasıl özetlediğin** sonucu belirler |
| 06 Kaydırma ve Farklar | `shift` geçmişi bugüne taşır; `diff` değişimi verir |
| 07 Hareketli Pencereler | Pencere gürültüyü düzler; ortalanmış pencere geleceği görür |
| 08 Birden Çok Seri | Uzun ve geniş biçim; indekste hizalama |
| 09 Görselleştirme | Önce çiz; her soru için ayrı grafik |
| 10 Bileşenler ve Ayrıştırma | Trend + mevsim + kalıntı; toplamsal mı çarpımsal mı |
| 11 Durağanlık | Logaritma varyansı, fark trendi giderir |
| 12 Otokorelasyon | Seri kendi geçmişine ne kadar benziyor; kalıntı beyaz gürültü mü |
| 13 Eksik Veri ve Aykırı Değerler | Önce görünür kıl; satırı silme, değeri onar |
| 14 Temel Tahminler | Taban çizgiyi yenemeyen model işe yaramaz |
| 15 Tahmini Doğrulamak | Zamana göre böl; tek ayrıma güvenme |
| 16 Üstel Düzleştirme | Yakın geçmişe daha çok ağırlık: düzey, trend, mevsim |
| 17 ARIMA | Fark al, otokorelasyonu modelle; kalıntıyı denetle |
| 18 Dışsal Değişkenler | Yalnızca gelecekte bilinen değişken işe yarar |
| 19 Makine Öğrenmesiyle Tahmin | Özellikler geçmişten; ağaç düzeyi uzatamaz |
| 20 Tahmin Aralıkları | Tek sayı yetmez; aralığı da sına |
| 21 Anomali ve Değişim Noktası | Geçici olanı işaretle, kalıcı olana göre yeniden kur |

## Patikanın on kuralı

1. **Önce çiz.** Hiçbir istatistik, grafiğin bir bakışta gösterdiğini söylemez.
2. **Düzenli indeks kur.** Eksik gün, görünmeyen bir hatadır.
3. **Geleceği kullanma.** Özellikte, doldurmada, ölçeklemede, doğrulamada:
   her yerde yalnızca geçmiş.
4. **Taban çizgiyle başla.** Mevsimsel naifi yenemeyen model karmaşıklıktan
   ibarettir.
5. **Tek ayrıma güvenme.** Kayan başlangıç, birden çok deney, en kötü deney.
6. **Ölçüyü işe göre seç.** MAE, RMSE, MASE, pinball: her biri başka bir soruya
   cevap verir.
7. **Kazanç bilgiden gelir.** Bu patikada her büyük iyileşme yeni bir yöntemden
   değil, yeni bir bilgiden geldi: takvim, tatil, kampanya.
8. **Kalıntıya bak.** Kalıntıda desen varsa model bir şeyi kaçırıyor.
9. **Belirsizliği söyle ve sına.** Aralık vermeyen tahmin yarım tahmindir.
10. **Teslimden sonra izle.** Seri değişir; model eskir.

## Neyi yapabiliyorsun

- Dağınık bir tarih sütununu düzenli, boşluksuz bir seriye çevirmek.
- Bir serinin trendini, mevsimini, otokorelasyonunu ölçmek ve çizmek.
- Eksik ve aykırı değerleri bulup gerekçesiyle onarmak.
- Bir tahmini zamana saygılı bir düzenekle, taban çizgiye karşı sınamak.
- Üstel düzleştirme, ARIMA, dış değişkenli regresyon ve ağaç modelleriyle
  tahmin kurmak; hangisinin ne zaman işe yaradığını ölçerek söylemek.
- Tahmine aralık eklemek ve aralığın dürüst olup olmadığını ölçmek.
- Anomaliyi değişim noktasından ayırmak.

## Neyi henüz yapamıyorsun

- **Çok serili tahmin.** Bin mağazayı tek modelle tahmin etmek (küresel
  modeller, hiyerarşik uzlaştırma).
- **Çok değişkenli modeller.** Serilerin birbirini etkilediği durumlar (VAR).
- **Oynaklık modelleri.** Finansal serilerde değişen varyans (GARCH).
- **Derin öğrenme.** Çok uzun ve çok sayıda seride sinir ağları.
- **Nedensellik.** "Kampanya satışı artırdı mı?" sorusu tahminden farklı bir
  sorudur ve farklı araçlar ister.

Bunların hepsi bu patikanın temeline oturur: düzenli indeks, zamana saygılı
doğrulama, taban çizgi, kalıntı.

## Son söz

Bisiklet örneğinde en iyi model, hatasının üçte ikisinin kaynağı olan
**yağmuru** bilmiyordu ve bilemezdi. Yine de iş yapıldı: taban çizgiden üçte bir daha iyi
bir tahmin, dürüst bir aralık ve hatanın kaynağının açık bir açıklaması.

Zaman serisi tahmini geleceği bilmek değildir. **Bilineni sonuna kadar
kullanmak, bilinmeyenin boyunu söylemek** ve ikisini birbirinden ayırmaktır.
