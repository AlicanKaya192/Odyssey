# Yeniden Örnekleme

Veri çoğu zaman ihtiyacın olan sıklıkta gelmiyor. Satış günlük kaydedilmiş,
rapor haftalık isteniyor. Sensör dakikada birkaç kez ölçüm gönderiyor, sana
saatlik ortalama yeter. Bütçe aylık verilmiş, karşılaştırma günlük yapılacak.

Bir serinin sıklığını değiştirmeye **yeniden örnekleme** (resampling) deniyor.
İki yönü var ve ikisi çok farklı işler:

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Seyreltmek (downsampling)</h4><p>Sık veriden seyrek veriye.<br>günlük → haftalık, saatlik → günlük<br>Birçok değer <b>tek sayıya iniyor</b>: topla, ortala, sonuncuyu al.</p></div>
    <div class="no"><h4>Sıklaştırmak (upsampling)</h4><p>Seyrek veriden sık veriye.<br>aylık → günlük, günlük → saatlik<br>Aradaki değerler <b>yok</b>: doldurman, yani tahmin etmen gerekiyor.</p></div>
  </div>
  <figcaption>Seyreltirken bilgi kaybediyorsun ama uydurmuyorsun. Sıklaştırırken satır kazanıyorsun ama bilgi kazanmıyorsun.</figcaption>
</figure>

Seyreltmek kolay ve güvenli: elinde fazlası var, özetliyorsun. Sıklaştırmak
tehlikeli: elinde olmayan bilgiyi üretmen gerekiyor.

## Günlükten haftalığa

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

weekly = s.resample("W").sum()
print(weekly.head(3))
```

```text
date
2022-01-02     582
2022-01-09    1606
2022-01-16    1604
Freq: W-SUN, Name: sales, dtype: int64
```

`resample("W")` günleri haftalık **kovalara** ayırıyor; `.sum()` her kovanın
içindekileri topluyor. Yazım `groupby` ile aynı mantıkta: önce nasıl
gruplayacağını, sonra ne hesaplayacağını söylüyorsun.

Üç şeye dikkat:

- **Etiket haftanın son günü.** `2022-01-09` o tarihte biten haftayı (3–9
  Ocak, pazartesiden pazara) temsil ediyor.
- **İlk kova eksik.** 2022, cumartesi günü başlıyor; ilk haftada yalnızca iki
  gün var. 582, kötü bir hafta değil, **yarım** bir hafta.
- Son kova da öyle: 2024, salı günü bitiyor.

```python
counts = s.resample("W").count()
print(counts.head(2).tolist(), counts.tail(2).tolist())   # [2, 7] [7, 2]

full = weekly[counts == 7]
print(len(weekly), len(full))                # 158 156
print(full.idxmax().date(), full.max())      # 2024-12-29 2717
print(full.idxmin().date(), full.min())      # 2022-07-03 1357
```

**Kovanın kaç gözlem içerdiğine her zaman bak.** Uçlardaki yarım kovaları
atmadan "en kötü hafta" sorusunu sorarsan cevap hep ilk ya da son hafta
çıkıyor.

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="206.6" x2="666" y2="206.6"/><text class="dim" x="38" y="210.1" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="146.7" x2="666" y2="146.7"/><text class="dim" x="38" y="150.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="86.7" x2="666" y2="86.7"/><text class="dim" x="38" y="90.2" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="26.8" x2="666" y2="26.8"/><text class="dim" x="38" y="30.3" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="199.1" y1="220" x2="199.1" y2="224"/><text class="dim" x="199.1" y="236" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="354.1" y1="220" x2="354.1" y2="224"/><text class="dim" x="354.1" y="236" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="510.9" y1="220" x2="510.9" y2="224"/><text class="dim" x="510.9" y="236" font-size="10.5" text-anchor="middle">Eki</text><polyline class="curve3" style="stroke-width:1.1" points="44.0,167.6 45.7,176.0 47.4,174.8 49.1,164.6 50.8,126.9 52.5,89.1 54.2,121.5 55.9,184.4 57.6,176.6 59.3,167.6 61.0,155.6 62.7,137.7 64.4,84.9 66.2,122.7 67.9,168.8 69.6,183.2 71.3,164.0 73.0,162.2 74.7,149.1 76.4,89.7 78.1,125.7 79.8,170.6 81.5,182.0 83.2,169.4 84.9,158.0 86.6,147.3 88.3,97.5 90.0,119.1 91.7,183.8 93.4,179.6 95.1,164.0 96.8,143.1 98.5,141.9 100.2,93.3 101.9,128.1 103.6,168.8 105.3,179.6 107.1,169.4 108.8,154.4 110.5,145.5 112.2,93.9 113.9,126.9 115.6,191.6 117.3,180.8 119.0,171.8 120.7,167.0 122.4,134.1 124.1,101.7 125.8,125.7 127.5,177.8 129.2,164.0 130.9,168.8 132.6,170.0 134.3,131.1 136.0,100.5 137.7,126.9 139.4,190.4 141.1,181.4 142.8,173.0 144.5,176.6 146.2,145.5 148.0,103.5 149.7,135.3 151.4,174.2 153.1,169.4 154.8,185.0 156.5,180.8 158.2,153.8 159.9,96.3 161.6,140.1 163.3,186.8 165.0,173.0 166.7,172.4 168.4,162.8 170.1,146.1 171.8,92.7 173.5,137.1 175.2,194.6 176.9,182.6 178.6,159.8 180.3,160.4 182.0,150.3 183.7,120.3 185.4,135.3 187.1,184.4 188.8,180.8 190.6,180.8 192.3,179.0 194.0,153.8 195.7,108.9 197.4,128.7 199.1,182.0 200.8,187.4 202.5,182.6 204.2,165.8 205.9,144.3 207.6,110.7 209.3,154.4 211.0,199.4 212.7,182.6 214.4,175.4 216.1,171.8 217.8,152.6 219.5,116.1 221.2,138.9 222.9,201.2 224.6,193.4 226.3,180.2 228.0,178.4 229.7,155.6 231.5,117.9 233.2,140.7 234.9,196.4 236.6,197.0 238.3,183.2 240.0,189.2 241.7,157.4 243.4,128.7 245.1,137.1 246.8,177.8 248.5,198.8 250.2,180.2 251.9,182.0 253.6,161.6 255.3,123.9 257.0,143.1 258.7,190.4 260.4,196.4 262.1,191.6 263.8,172.4 265.5,149.1 267.2,128.7 268.9,148.5 270.6,188.6 272.4,178.4 274.1,186.2 275.8,177.2 277.5,165.2 279.2,116.1 280.9,143.7 282.6,198.2 284.3,192.8 286.0,173.6 287.7,170.6 289.4,149.7 291.1,129.3 292.8,155.6 294.5,206.6 296.2,189.2 297.9,196.4 299.6,188.0 301.3,152.0 303.0,135.9 304.7,144.3 306.4,204.2 308.1,192.8 309.8,173.0 311.5,179.0 313.2,161.6 315.0,125.1 316.7,149.7 318.4,200.0 320.1,204.2 321.8,194.6 323.5,171.8 325.2,151.4 326.9,119.1 328.6,147.9 330.3,191.6 332.0,191.0 333.7,184.4 335.4,170.6 337.1,150.9 338.8,125.1 340.5,152.6 342.2,209.0 343.9,197.0 345.6,188.6 347.3,180.8 349.0,158.6 350.7,119.1 352.4,139.5 354.1,204.8 355.9,198.2 357.6,193.4 359.3,174.8 361.0,145.5 362.7,119.1 364.4,141.9 366.1,197.6 367.8,197.0 369.5,190.4 371.2,167.6 372.9,156.8 374.6,120.3 376.3,139.5 378.0,192.2 379.7,182.6 381.4,185.0 383.1,174.8 384.8,151.4 386.5,120.9 388.2,144.3 389.9,187.4 391.6,187.4 393.3,187.4 395.0,175.4 396.8,136.5 398.5,116.1 400.2,144.9 401.9,187.4 403.6,176.0 405.3,183.2 407.0,175.4 408.7,153.8 410.4,121.5 412.1,138.3 413.8,181.4 415.5,182.6 417.2,179.6 418.9,183.2 420.6,151.4 422.3,117.3 424.0,153.2 425.7,191.0 427.4,179.6 429.1,185.0 430.8,175.4 432.5,135.3 434.2,102.9 435.9,124.5 437.6,176.6 439.4,177.2 441.1,176.6 442.8,164.6 444.5,134.7 446.2,102.3 447.9,129.3 449.6,182.0 451.3,173.6 453.0,177.8 454.7,154.4 456.4,135.3 458.1,105.3 459.8,116.1 461.5,192.8 463.2,192.8 464.9,168.2 466.6,168.2 468.3,143.7 470.0,94.5 471.7,117.9 473.4,164.6 475.1,172.4 476.8,174.8 478.5,157.4 480.3,138.9 482.0,98.1 483.7,114.9 485.4,168.8 487.1,185.6 488.8,161.0 490.5,158.0 492.2,130.5 493.9,98.1 495.6,126.3 497.3,178.4 499.0,167.6 500.7,167.0 502.4,159.2 504.1,125.7 505.8,93.9 507.5,129.3 509.2,170.0 510.9,177.2 512.6,162.8 514.3,147.3 516.0,134.7 517.7,89.1 519.4,122.7 521.2,171.8 522.9,172.4 524.6,173.6 526.3,153.8 528.0,120.3 529.7,90.9 531.4,110.1 533.1,174.2 534.8,177.8 536.5,150.9 538.2,147.3 539.9,123.3 541.6,84.3 543.3,120.9 545.0,161.6 546.7,168.2 548.4,146.1 550.1,153.2 551.8,124.5 553.5,77.8 555.2,108.3 556.9,163.4 558.6,162.2 560.3,155.0 562.0,150.3 563.8,110.1 565.5,73.6 567.2,105.9 568.9,163.4 570.6,166.4 572.3,156.8 574.0,143.1 575.7,116.1 577.4,60.4 579.1,102.3 580.8,160.4 582.5,165.2 584.2,144.9 585.9,144.9 587.6,102.9 589.3,81.4 591.0,90.9 592.7,162.8 594.4,158.6 596.1,158.6 597.8,137.7 599.5,106.5 601.2,76.6 602.9,96.9 604.7,165.2 606.4,154.4 608.1,148.5 609.8,148.5 611.5,125.1 613.2,67.6 614.9,90.9 616.6,165.2 618.3,152.6 620.0,141.3 621.7,138.3 623.4,112.5 625.1,57.4 626.8,80.8 628.5,150.3 630.2,136.5 631.9,146.1 633.6,110.1 635.3,93.3 637.0,47.8 638.7,66.4 640.4,146.1 642.1,141.9 643.8,132.9 645.6,134.7 647.3,81.4 649.0,33.4 650.7,68.8 652.4,143.1 654.1,120.3 655.8,122.7 657.5,113.1 659.2,72.4 660.9,25.0 662.6,60.4 664.3,123.3 666.0,118.5"/><polyline class="curve2" style="stroke-width:2.6" points="49.1,145.8 61.0,147.1 73.0,149.0 84.9,149.1 96.8,147.7 108.8,148.4 120.7,153.2 132.6,148.5 144.5,158.0 156.5,157.1 168.4,153.0 180.3,157.6 192.3,159.5 204.2,161.0 216.1,162.4 228.0,166.8 240.0,169.9 251.9,166.8 263.8,168.1 275.8,165.1 287.7,167.1 299.6,173.2 311.5,169.3 323.5,169.9 335.4,166.6 347.3,170.4 359.3,168.2 371.2,167.0 383.1,164.5 395.0,162.1 407.0,162.2 418.9,164.1 430.8,156.2 442.8,151.6 454.7,149.2 466.6,154.0 478.5,145.9 490.5,146.9 502.4,145.9 514.3,143.4 526.3,141.9 538.2,139.8 550.1,134.2 562.0,131.5 574.0,129.8 585.9,127.2 597.8,128.3 609.8,128.6 621.7,121.2 633.6,107.2 645.6,105.6 657.5,93.8"/><line class="curve3" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">günlük</text><line class="curve2" x1="142" y1="22" x2="160" y2="22"/><text class="ink" x="166" y="26" font-size="11">haftalık ortalama</text></svg>
  <figcaption>2024: gri ince çizgi günlük satış, turuncu çizgi tam haftaların ortalaması. Haftanın günleri arasındaki zikzak kovanın içinde eriyor; geriye yılın genel şekli kalıyor.</figcaption>
</figure>

Haftalık seri çok daha sakin: haftanın günleri arasındaki inip çıkma kovanın
içinde eriyor ve geriye trend ile yıllık desen kalıyor. Seyreltmenin ikinci
faydası bu: **gürültüyü ve kısa dönemli mevsimselliği bastırıyor.**

## Aya, çeyreğe, yıla

```python
print(s.resample("ME").sum().loc["2024-03"])     # 2024-03-31    8919
print(s.resample("MS").sum().loc["2024-03"])     # 2024-03-01    8919
print(s.resample("QE").sum().loc["2024"].tolist())   # [26513, 24146, 26025, 30927]
print(s.resample("YE").sum().tolist())               # [82303, 95039, 107611]
```

`"ME"` ile `"MS"` aynı kovaları kuruyor; tek fark **etiket**: ay sonu mu, ay
başı mı. Sayılar, geçen bölümde `to_period("M")` ile bulduklarınla birebir
aynı.

Birden çok özet aynı anda alınabiliyor:

```python
print(s.resample("ME").agg(["sum", "mean", "max", "min"]).round(1).loc["2024-03"])
```

```text
             sum   mean  max  min
date
2024-03-31  8919  287.7  390  220
```

## Hangi işlemle özetlenir?

Bu bölümün en önemli sorusu. Kovanın içindekileri tek sayıya indirirken
**neyi ölçtüğüne** bakıyorsun:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Akış: satış, tüketim, ziyaret</span><span><code>sum</code> · dönem boyunca <b>biriken</b> şey toplanır</span></div>
    <div class="anat-row"><span>Anlık seviye: fiyat, stok, bakiye</span><span><code>last</code> · dönemin <b>sonundaki</b> durum</span></div>
    <div class="anat-row"><span>Anlık ölçüm: sıcaklık, yük</span><span><code>mean</code> · dönemin tipik değeri; tepe için <code>max</code></span></div>
    <div class="anat-row"><span>Sayım: kaç sipariş, kaç hata</span><span><code>count</code> ya da <code>sum</code></span></div>
  </div>
  <figcaption>Soru her zaman aynı: bu değer zaman içinde <b>birikiyor mu</b>, yoksa bir <b>anı</b> mı gösteriyor? Birikiyorsa topla; bir anı gösteriyorsa toplama.</figcaption>
</figure>

Hisse fiyatında yanlış seçim şöyle görünüyor:

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(round(close.resample("ME").sum().iloc[0], 2))             # 2143.76  anlamsiz
print(round(close.resample("ME").last().loc["2024-03"].iloc[0], 2))   # 166.33
print(round(close.resample("ME").mean().loc["2024-03"].iloc[0], 2))   # 153.39
```

Fiyatı toplamak hiçbir şeye karşılık gelmeyen bir sayı veriyor: 2143.76 lira
diye bir fiyat hiç olmadı. **Hata da çıkmıyor.** pandas ne istersen onu
hesaplıyor; doğru işlemi seçmek senin işin.

Fiyat serilerinde sık kullanılan hazır özet `ohlc`: açılış, en yüksek, en
düşük, kapanış.

```python
print(close.resample("ME").ohlc().round(2).loc["2024-03"])
```

```text
              open    high     low   close
date
2024-03-31  140.99  167.73  140.99  166.33
```

## Saatlikten günlüğe

Aynı seriden farklı sorular farklı işlem istiyor. Saatlik elektrik tüketimi
(MW):

```python
load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

daily = load.resample("D").agg(["sum", "mean", "max"]).round(1)
print(daily.head(2))
```

```text
                sum   mean     max
timestamp
2024-03-01  22816.6  950.7  1251.1
2024-03-02  19459.6  810.8  1096.2
```

- **`sum`**: o gün tüketilen toplam enerji (MWh). Fatura bununla kesiliyor.
- **`max`**: günün tepe yükü. Şebekenin dayanması gereken sayı bu.
- **`mean`**: ortalama yük.

Üçü de doğru; hangisini istediğin soruya bağlı. Kovalar daha küçük de
olabiliyor: `load.resample("6h").mean()` günü dört parçaya bölüyor
(822.7, 981.4, 1170.9, 827.7).

## Gizli tehlike: eksik günlü kovalar

Bölüm 03'teki dağınık 2024 dosyasını hatırla: sekiz gün eksikti. Onu haftalığa
toplayalım:

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

print(fixed.resample("W").agg(["sum", "count"]).loc["2024-07-14":"2024-07-28"])
```

```text
             sum  count
date
2024-07-14  1862      7
2024-07-21  1192      4
2024-07-28  1919      7
```

21 Temmuz'da biten haftanın toplamı **1192**. Gerçek değer 1892. O hafta üç
günün kaydı yok ve `sum` elinde olan dört günü toplayıp geçti. **Hata yok,
uyarı yok**; grafikte o hafta satışlar çökmüş gibi görünüyor.

Korunmanın iki yolu:

```python
reg = fixed.asfreq("D")                               # eksikler NaN olur
print(reg.resample("W").sum().loc["2024-07-21"])                # 1192.0
print(reg.resample("W").sum(min_count=7).loc["2024-07-21"])     # nan
```

- **`count` ile bak**: kovada beklenenden az gözlem varsa o kovaya güvenme.
- **`min_count`**: kova en az bu kadar geçerli değer içermiyorsa sonuç `NaN`
  olsun. Eksik bir toplam yerine "bilmiyorum" demek çok daha dürüst.

Ortalama bu durumda daha dayanıklı: eksik günleri atlayıp kalanların
ortalamasını alıyor (o hafta 298.0). Ama kalan dört günün haftanın hangi
günleri olduğuna bağlı olarak o da kayabiliyor.

## Düzensiz veriyi düzenliye çevirmek

Bir makinenin sıcaklık sensörü düzenli aralıkla değil, kafasına göre kayıt
gönderiyor (`machine_log.csv`, 537 satır):

```text
               time  temp_c
2024-05-06 00:04:55    57.9
2024-05-06 00:16:04    55.0
2024-05-06 00:21:32    56.3
2024-05-06 00:23:41    55.7
```

İki kayıt arası 1 dakika ile 5 saat 42 dakika arasında değişiyor. Bu hâliyle
ne başka bir seriyle birleştirilebiliyor ne de "bir önceki saat" diye bir şey
sorulabiliyor. `resample` onu düzenli bir ızgaraya oturtuyor:

```python
temp = pd.read_csv("machine_log.csv", index_col="time", parse_dates=True)["temp_c"]

hourly = temp.resample("h").mean()
print(len(hourly), hourly.isna().sum())     # 72 4
```

Üç gün, 72 saat; her saat için bir satır. Dört saatte hiç kayıt yok (7 Mayıs
03:00–06:00): sensör o aralıkta susmuş.

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="283.7" y="14" width="213.8" height="206" opacity="0.8" style="stroke:none"/><line class="grid" x1="44" y1="206.2" x2="666" y2="206.2"/><text class="dim" x="38" y="209.7" font-size="10.5" text-anchor="end">54</text><line class="grid" x1="44" y1="175.5" x2="666" y2="175.5"/><text class="dim" x="38" y="179.0" font-size="10.5" text-anchor="end">56</text><line class="grid" x1="44" y1="144.7" x2="666" y2="144.7"/><text class="dim" x="38" y="148.2" font-size="10.5" text-anchor="end">58</text><line class="grid" x1="44" y1="113.9" x2="666" y2="113.9"/><text class="dim" x="38" y="117.4" font-size="10.5" text-anchor="end">60</text><line class="grid" x1="44" y1="83.2" x2="666" y2="83.2"/><text class="dim" x="38" y="86.7" font-size="10.5" text-anchor="end">62</text><line class="grid" x1="44" y1="52.4" x2="666" y2="52.4"/><text class="dim" x="38" y="55.9" font-size="10.5" text-anchor="end">64</text><line class="grid" x1="44" y1="21.6" x2="666" y2="21.6"/><text class="dim" x="38" y="25.1" font-size="10.5" text-anchor="end">66</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">20:00</text><line class="line" x1="199.5" y1="220" x2="199.5" y2="224"/><text class="dim" x="199.5" y="236" font-size="10.5" text-anchor="middle">00:00</text><line class="line" x1="355.0" y1="220" x2="355.0" y2="224"/><text class="dim" x="355.0" y="236" font-size="10.5" text-anchor="middle">04:00</text><line class="line" x1="510.5" y1="220" x2="510.5" y2="224"/><text class="dim" x="510.5" y="236" font-size="10.5" text-anchor="middle">08:00</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">12:00</text><circle class="dim" cx="45.0" cy="72.4" r="1.8"/><circle class="dim" cx="46.4" cy="72.4" r="1.8"/><circle class="dim" cx="49.3" cy="72.4" r="1.8"/><circle class="dim" cx="52.0" cy="81.6" r="1.8"/><circle class="dim" cx="55.6" cy="84.7" r="1.8"/><circle class="dim" cx="56.9" cy="92.4" r="1.8"/><circle class="dim" cx="65.4" cy="83.2" r="1.8"/><circle class="dim" cx="67.8" cy="84.7" r="1.8"/><circle class="dim" cx="72.8" cy="80.1" r="1.8"/><circle class="dim" cx="75.3" cy="107.8" r="1.8"/><circle class="dim" cx="79.6" cy="106.2" r="1.8"/><circle class="dim" cx="83.0" cy="97.0" r="1.8"/><circle class="dim" cx="89.1" cy="90.9" r="1.8"/><circle class="dim" cx="95.9" cy="112.4" r="1.8"/><circle class="dim" cx="103.4" cy="107.8" r="1.8"/><circle class="dim" cx="108.2" cy="97.0" r="1.8"/><circle class="dim" cx="111.9" cy="127.8" r="1.8"/><circle class="dim" cx="114.7" cy="127.8" r="1.8"/><circle class="dim" cx="115.5" cy="107.8" r="1.8"/><circle class="dim" cx="120.5" cy="126.2" r="1.8"/><circle class="dim" cx="121.7" cy="129.3" r="1.8"/><circle class="dim" cx="129.3" cy="113.9" r="1.8"/><circle class="dim" cx="132.5" cy="138.5" r="1.8"/><circle class="dim" cx="138.2" cy="130.8" r="1.8"/><circle class="dim" cx="146.7" cy="137.0" r="1.8"/><circle class="dim" cx="148.9" cy="150.8" r="1.8"/><circle class="dim" cx="154.0" cy="147.8" r="1.8"/><circle class="dim" cx="162.5" cy="144.7" r="1.8"/><circle class="dim" cx="164.0" cy="133.9" r="1.8"/><circle class="dim" cx="165.3" cy="155.5" r="1.8"/><circle class="dim" cx="173.2" cy="140.1" r="1.8"/><circle class="dim" cx="178.7" cy="177.0" r="1.8"/><circle class="dim" cx="186.0" cy="143.1" r="1.8"/><circle class="dim" cx="193.4" cy="144.7" r="1.8"/><circle class="dim" cx="201.3" cy="170.8" r="1.8"/><circle class="dim" cx="207.3" cy="166.2" r="1.8"/><circle class="dim" cx="212.9" cy="169.3" r="1.8"/><circle class="dim" cx="221.9" cy="166.2" r="1.8"/><circle class="dim" cx="229.3" cy="177.0" r="1.8"/><circle class="dim" cx="237.6" cy="169.3" r="1.8"/><circle class="dim" cx="244.4" cy="177.0" r="1.8"/><circle class="dim" cx="247.1" cy="181.6" r="1.8"/><circle class="dim" cx="247.8" cy="181.6" r="1.8"/><circle class="dim" cx="254.2" cy="177.0" r="1.8"/><circle class="dim" cx="259.5" cy="183.1" r="1.8"/><circle class="dim" cx="268.5" cy="189.3" r="1.8"/><circle class="dim" cx="270.0" cy="181.6" r="1.8"/><circle class="dim" cx="271.7" cy="200.1" r="1.8"/><circle class="dim" cx="280.2" cy="190.8" r="1.8"/><circle class="dim" cx="502.3" cy="130.8" r="1.8"/><circle class="dim" cx="504.7" cy="118.5" r="1.8"/><circle class="dim" cx="508.9" cy="120.1" r="1.8"/><circle class="dim" cx="510.9" cy="126.2" r="1.8"/><circle class="dim" cx="514.8" cy="118.5" r="1.8"/><circle class="dim" cx="518.1" cy="100.1" r="1.8"/><circle class="dim" cx="526.8" cy="117.0" r="1.8"/><circle class="dim" cx="531.6" cy="123.2" r="1.8"/><circle class="dim" cx="535.6" cy="117.0" r="1.8"/><circle class="dim" cx="539.9" cy="109.3" r="1.8"/><circle class="dim" cx="542.0" cy="113.9" r="1.8"/><circle class="dim" cx="543.9" cy="93.9" r="1.8"/><circle class="dim" cx="546.4" cy="81.6" r="1.8"/><circle class="dim" cx="549.5" cy="75.5" r="1.8"/><circle class="dim" cx="557.1" cy="66.2" r="1.8"/><circle class="dim" cx="564.8" cy="95.5" r="1.8"/><circle class="dim" cx="568.3" cy="84.7" r="1.8"/><circle class="dim" cx="569.7" cy="80.1" r="1.8"/><circle class="dim" cx="577.4" cy="84.7" r="1.8"/><circle class="dim" cx="579.1" cy="60.1" r="1.8"/><circle class="dim" cx="587.5" cy="70.9" r="1.8"/><circle class="dim" cx="595.1" cy="64.7" r="1.8"/><circle class="dim" cx="596.0" cy="101.6" r="1.8"/><circle class="dim" cx="603.5" cy="66.2" r="1.8"/><circle class="dim" cx="611.1" cy="58.5" r="1.8"/><circle class="dim" cx="619.4" cy="69.3" r="1.8"/><circle class="dim" cx="621.7" cy="33.9" r="1.8"/><circle class="dim" cx="630.0" cy="41.6" r="1.8"/><circle class="dim" cx="637.5" cy="50.9" r="1.8"/><circle class="dim" cx="642.8" cy="35.5" r="1.8"/><circle class="dim" cx="645.3" cy="33.9" r="1.8"/><circle class="dim" cx="653.9" cy="43.2" r="1.8"/><circle class="dim" cx="662.0" cy="46.2" r="1.8"/><polyline class="curve" style="stroke-width:2.4" points="63.4,85.3 102.3,112.4 141.2,136.5 180.1,148.4 218.9,169.8 257.8,183.9 296.7,190.8"/><polyline class="curve" style="stroke-width:2.4" points="491.1,123.2 529.9,110.1 568.8,77.2 607.7,65.7 646.6,41.9 685.4,31.4"/><circle class="dot" cx="63.4" cy="85.3" r="3"/><circle class="dot" cx="102.3" cy="112.4" r="3"/><circle class="dot" cx="141.2" cy="136.5" r="3"/><circle class="dot" cx="180.1" cy="148.4" r="3"/><circle class="dot" cx="218.9" cy="169.8" r="3"/><circle class="dot" cx="257.8" cy="183.9" r="3"/><circle class="dot" cx="296.7" cy="190.8" r="3"/><circle class="dot" cx="491.1" cy="123.2" r="3"/><circle class="dot" cx="529.9" cy="110.1" r="3"/><circle class="dot" cx="568.8" cy="77.2" r="3"/><circle class="dot" cx="607.7" cy="65.7" r="3"/><circle class="dot" cx="646.6" cy="41.9" r="3"/><circle class="dot" cx="685.4" cy="31.4" r="3"/><text class="ink" x="390.6" y="20.6" font-size="11" text-anchor="middle">kesinti: kayıt yok</text></svg>
  <figcaption>6–7 Mayıs gecesi. Küçük gri noktalar sensörün düzensiz kayıtları, mor çizgi saatlik ortalama. Kesinti boyunca saatlik kovalar boş kalıyor ve çizgi kopuyor: eksiklik görünür oluyor.</figcaption>
</figure>

**Boş kovada `sum` ve `mean` farklı davranıyor:**

```python
print(temp.resample("h").sum().loc["2024-05-07 04:00"])     # 0.0
print(temp.resample("h").mean().loc["2024-05-07 04:00"])    # nan
```

Hiç kayıt olmayan saatin toplamı **0.0**, ortalaması `NaN`. Sıfır burada
yanlış: makine sıfır derecede değildi, ölçüm yoktu. Sayım yaparken (kaç olay
oldu?) boş kovanın 0 olması doğru; ölçüm toplarken `sum(min_count=1)` yaz.

Boşluğu doldurmak ayrı bir karar:

```python
print(hourly.interpolate().round(2).loc["2024-05-07 02:00":"2024-05-07 07:00"].tolist())
# [55.0, 55.88, 56.76, 57.64, 58.52, 59.4]      iki uc arasinda duz cizgi

print(hourly.ffill().round(2).loc["2024-05-07 03:00":"2024-05-07 06:00"].tolist())
# [55.0, 55.0, 55.0, 55.0]                      son bilinen degeri tasi
```

Hangisinin ne zaman doğru olduğu Bölüm 13'ün konusu. Şimdilik bilmen gereken:
**doldurulan değer bir ölçüm değil, bir tahmin.** `interpolate(limit=2)` gibi
bir sınır koyarsan uzun kesintiler boş kalıyor.

## Sıklaştırmak

Tersi yöne gidelim: 2024'ün aylık toplamları var, günlük seri isteniyor.

```python
monthly = s.loc["2024"].resample("MS").sum()      # 12 satir
daily = monthly.resample("D").ffill()

print(len(daily), daily.index[-1].date())         # 336 2024-12-01
print(daily.loc["2024-03"].sum())                 # 276489
```

İki şey birden yanlış gitti:

1. **Mart'ın toplamı 8919'dan 276489'a çıktı.** `ffill` aylık toplamı ayın her
   gününe **kopyaladı**: 31 gün × 8919. Toplam 31 kat şişti.
2. **Aralık kayboldu.** Sıklaştırma son etikette (1 Aralık) duruyor; ayın geri
   kalan 30 günü yok.

Bir **toplam** günlere kopyalanmaz, **paylaştırılır**:

```python
per_day = monthly / monthly.index.days_in_month
idx = pd.date_range("2024-01-01", "2024-12-31", freq="D")
spread = per_day.reindex(idx, method="ffill")

print(round(spread.loc["2024-03"].sum(), 1))      # 8919.0
print(round(spread.loc["2024-03-09"], 1), s.loc["2024-03-09"])   # 287.7 384
```

Artık aylık toplam tutuyor. Ama son satıra bak: 9 Mart için 287.7 yazıyor,
gerçek satış 384'tü. **Sıklaştırma bilgi üretmiyor.** Aylık veriden
cumartesinin yüksek, pazartesinin düşük olduğunu öğrenmenin yolu yok; her
güne ayın ortalaması düşüyor.

Anlık değerlerde (sıcaklık, fiyat, stok) durum farklı: kopyalamak ya da ara
değer bulmak anlamlı.

```python
t = pd.Series([10.0, 16.0, 13.0],
              index=pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-03"]))
print(t.resample("6h").interpolate().round(1).tolist())
# [10.0, 11.5, 13.0, 14.5, 16.0, 15.2, 14.5, 13.8, 13.0]
```

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Uçlardaki yarım kovaları atmamak | "En kötü hafta" hep ilk ya da son hafta | `count()` ile tam kovaları seç |
| Fiyatı, sıcaklığı toplamak | Anlamsız sayı, hata yok | `last()`, `mean()`, `max()` |
| Eksik günlü kovayı toplamak | Toplam sessizce düşük | `count` ile bak, `min_count` kullan |
| Boş kovada `sum()` | 0 çıkıyor, "ölçüm yok" yerine "sıfır" | `sum(min_count=1)` ya da `mean()` |
| Toplamı `ffill` ile sıklaştırmak | Toplam kat kat şişiyor | Gün sayısına bölüp paylaştır |
| Sıklaştırılmış veriye gerçek gibi davranmak | Olmayan ayrıntı | Doldurulan değer tahmindir |
| `"ME"` ile `"MS"` etiketini karıştırmak | Birleştirmede eşleşmiyor | Birini seç |

## Özet

- **Seyreltmek** (günlük → haftalık): `s.resample("W").sum()`. Kovaları
  kuruyorsun, sonra özetliyorsun.
- İşlemi **değerin anlamına göre** seç: toplamlar için `sum`, anlık değerler
  için `last` ya da `mean`, tepe için `max`, fiyat için `ohlc`.
- **`count()` ile kovaları denetle.** Uçlardaki yarım kovalar ve eksik günlü
  kovalar toplamı sessizce düşürüyor; `min_count` bunu `NaN` yapıyor.
- Boş kovada `sum` 0, `mean` `NaN` veriyor.
- Düzensiz seriyi `resample("h").mean()` düzenli ızgaraya oturtuyor; boş
  kovalar kesintiyi görünür kılıyor.
- **Sıklaştırmak bilgi üretmiyor.** Toplamı paylaştır, anlık değeri taşı ya
  da ara değerle doldur; sonucun ölçüm değil tahmin olduğunu unutma.
