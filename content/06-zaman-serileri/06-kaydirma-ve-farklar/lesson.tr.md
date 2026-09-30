# Kaydırma ve Farklar

Bölüm 00'da bir deney yapmıştın: bugünün satışını dünle eşleştirmek için
diziyi elle dilimledin (`values[:-1]` ile `values[1:]`). Zaman serisinde bu
eşleştirme o kadar sık gerekiyor ki pandas'ın ona ayrılmış araçları var.

Bu bölümün dört aracı aynı soruyu farklı biçimlerde soruyor: **şimdiki değer,
geçmişteki bir değere göre nerede?**

- `shift`: geçmiş değeri bugünün satırına getir.
- `diff`: aradaki fark ne kadar?
- `pct_change`: yüzde kaç değişti?
- `cumsum`: baştan bugüne ne kadar birikti?

## `shift`: değerleri kaydırmak

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

table = pd.DataFrame({
    "sales": s,
    "lag1": s.shift(1),
    "lag7": s.shift(7),
})
print(table.head(9))
```

```text
            sales   lag1   lag7
date
2022-01-01    305    NaN    NaN
2022-01-02    277  305.0    NaN
2022-01-03    201  277.0    NaN
2022-01-04    182  201.0    NaN
2022-01-05    184  182.0    NaN
2022-01-06    211  184.0    NaN
2022-01-07    251  211.0    NaN
2022-01-08    299  251.0  305.0
2022-01-09    278  299.0  277.0
```

`shift(1)` her değeri **bir satır aşağı** itiyor: 2 Ocak satırında artık 1
Ocak'ın satışı duruyor. Böylece her satırda "bugün" ile "dün" yan yana.
`shift(7)` aynısını bir hafta için yapıyor.

İki ayrıntı:

- **Baştaki satırlar boş.** İlk günün dünü yok; `lag7` için ilk yedi günün
  geçen haftası yok. Kaydırma kadar `NaN` oluşuyor.
- **Tarihler yerinde duruyor, değerler kayıyor.** İndeks aynı.

Geçmişten getirilen değere **gecikme** (lag) deniyor. Bölüm 00'daki deneyi
artık tek satırla yapabiliyorsun:

```python
print(round(s.corr(s.shift(1)), 3))    # 0.695
print(round(s.corr(s.shift(7)), 3))    # 0.958
```

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><line class="line" x1="44" y1="182.4" x2="666" y2="182.4"/><text class="dim" x="38" y="185.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="145.7" x2="666" y2="145.7"/><text class="dim" x="38" y="149.2" font-size="10.5" text-anchor="end">0.25</text><line class="grid" x1="44" y1="109.1" x2="666" y2="109.1"/><text class="dim" x="38" y="112.6" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="44" y1="72.4" x2="666" y2="72.4"/><text class="dim" x="38" y="75.9" font-size="10.5" text-anchor="end">0.75</text><line class="grid" x1="44" y1="35.7" x2="666" y2="35.7"/><text class="dim" x="38" y="39.2" font-size="10.5" text-anchor="end">1</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="67.0" y1="200" x2="67.0" y2="204"/><text class="dim" x="67.0" y="216" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="239.8" y1="200" x2="239.8" y2="204"/><text class="dim" x="239.8" y="216" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="441.4" y1="200" x2="441.4" y2="204"/><text class="dim" x="441.4" y="216" font-size="10.5" text-anchor="middle">14</text><line class="line" x1="643.0" y1="200" x2="643.0" y2="204"/><text class="dim" x="643.0" y="216" font-size="10.5" text-anchor="middle">21</text><rect class="dot3" x="58.1" y="80.5" width="17.9" height="101.9" rx="3" opacity="0.55"/><rect class="dot3" x="86.9" y="141.8" width="17.9" height="40.6" rx="3" opacity="0.55"/><rect class="dot3" x="115.7" y="166.8" width="17.9" height="15.6" rx="3" opacity="0.55"/><rect class="dot3" x="144.5" y="167.6" width="17.9" height="14.8" rx="3" opacity="0.55"/><rect class="dot3" x="173.3" y="143.0" width="17.8" height="39.4" rx="3" opacity="0.55"/><rect class="dot3" x="202.1" y="82.1" width="17.8" height="100.3" rx="3" opacity="0.55"/><rect class="dot3" x="230.9" y="42.0" width="17.8" height="140.4" rx="3" opacity="0.55"/><rect class="dot3" x="259.7" y="82.2" width="17.8" height="100.2" rx="3" opacity="0.55"/><rect class="dot3" x="288.5" y="143.7" width="17.8" height="38.7" rx="3" opacity="0.55"/><rect class="dot3" x="317.3" y="169.8" width="17.8" height="12.6" rx="3" opacity="0.55"/><rect class="dot3" x="346.1" y="170.4" width="17.8" height="12.0" rx="3" opacity="0.55"/><rect class="dot3" x="374.9" y="145.3" width="17.8" height="37.1" rx="3" opacity="0.55"/><rect class="dot3" x="403.7" y="83.7" width="17.8" height="98.7" rx="3" opacity="0.55"/><rect class="dot3" x="432.5" y="43.1" width="17.8" height="139.3" rx="3" opacity="0.55"/><rect class="dot3" x="461.3" y="83.9" width="17.8" height="98.5" rx="3" opacity="0.55"/><rect class="dot3" x="490.1" y="146.0" width="17.8" height="36.4" rx="3" opacity="0.55"/><rect class="dot3" x="518.9" y="172.0" width="17.8" height="10.4" rx="3" opacity="0.55"/><rect class="dot3" x="547.6" y="172.6" width="17.9" height="9.8" rx="3" opacity="0.55"/><rect class="dot3" x="576.4" y="147.7" width="17.9" height="34.7" rx="3" opacity="0.55"/><rect class="dot3" x="605.2" y="85.5" width="17.9" height="96.9" rx="3" opacity="0.55"/><rect class="dot3" x="634.0" y="44.4" width="17.9" height="138.0" rx="3" opacity="0.55"/><rect class="dot" x="230.9" y="42.0" width="17.8" height="140.4" rx="3" opacity="0.9"/><rect class="dot" x="432.5" y="43.1" width="17.8" height="139.3" rx="3" opacity="0.9"/><rect class="dot" x="634.0" y="44.4" width="17.9" height="138.0" rx="3" opacity="0.9"/><text class="ink" x="239.8" y="34.6" font-size="11" text-anchor="middle">0.96</text><text class="ink" x="441.4" y="35.8" font-size="11" text-anchor="middle">0.95</text><text class="ink" x="643.0" y="37.1" font-size="11" text-anchor="middle">0.94</text><text class="dim" x="67.0" y="73.2" font-size="10.5" text-anchor="middle">0.69</text><text class="dim" x="124.6" y="159.5" font-size="10.5" text-anchor="middle">0.11</text></svg>
  <figcaption>Bugünün satışı ile k gün önceki satış arasındaki korelasyon (yatay eksen: k). Her 7 günde bir tepe: mağaza bir hafta öncesini çok iyi hatırlıyor, üç gün öncesini neredeyse hiç.</figcaption>
</figure>

Grafik mağazanın hafızasını gösteriyor. 3 gün önceki satışın bugünle neredeyse
hiçbir ilgisi yok (0.106); 7 ve 14 gün önceki ise çok güçlü. Bu grafiğin adı
**otokorelasyon** ve Bölüm 12'nin tamamı ona ayrılmış.

## Geçmiş ve gelecek

`shift` eksi sayı da alıyor:

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4><code>shift(1)</code>: gecikme</h4><p><b>Geçmişi</b> bugünün satırına getiriyor.<br>O gün gerçekten bilinen bir değer.<br>Özellik olarak güvenli.</p></div>
    <div class="no"><h4><code>shift(-1)</code>: öncü</h4><p><b>Geleceği</b> bugünün satırına getiriyor.<br>O gün henüz bilinmeyen bir değer.<br>Yalnızca hedef (cevap) sütunu için.</p></div>
  </div>
  <figcaption>Kontrol sorusu: tahmini yaptığın gün bu değeri bilebilir miydin? Hayırsa, özellik olamaz.</figcaption>
</figure>

```python
s.shift(-1)     # yarinin degeri bugunun satirinda
```

Bu masum görünüyor ama zaman serisindeki sızıntının en yaygın kaynağı. Tahmin
modelinin **girdisi** her zaman geçmişe bakmalı (`shift(1)`, `shift(7)`).
`shift(-1)` yalnızca **hedefi** kurarken kullanılır: "bugünün verisiyle yarını
tahmin et" derken yarın cevap sütunudur, özellik değil.

## `diff`: fark

Bugün ile dün arasındaki fark `s - s.shift(1)`. Kısası:

```python
change = s.diff()

print(change.head(4).tolist())           # [nan, -28.0, -76.0, -19.0]
print(round(change.abs().mean(), 1))     # 36.8
print(change.idxmax().date(), change.max())   # 2023-12-30 106.0
print(change.idxmin().date(), change.min())   # 2024-01-01 -139.0
```

Satış bir günden ötekine ortalama 36.8 birim oynuyor. En büyük düşüş 1 Ocak
2024: yılbaşı gecesinden sonraki gün.

`diff(7)` bugünü **geçen haftanın aynı günüyle** karşılaştırıyor:

```python
print(s.diff(7).loc["2024-03-09"])       # 12.0     384 - 372

print(round(s.diff().std(), 1))          # 46.1
print(round(s.diff(7).std(), 1))         # 17.1
```

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="202.2" x2="666" y2="202.2"/><text class="dim" x="38" y="205.7" font-size="10.5" text-anchor="end">−100</text><line class="grid" x1="44" y1="157.8" x2="666" y2="157.8"/><text class="dim" x="38" y="161.3" font-size="10.5" text-anchor="end">−50</text><line class="line" x1="44" y1="113.4" x2="666" y2="113.4"/><text class="dim" x="38" y="116.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="69.1" x2="666" y2="69.1"/><text class="dim" x="38" y="72.6" font-size="10.5" text-anchor="end">50</text><line class="grid" x1="44" y1="24.7" x2="666" y2="24.7"/><text class="dim" x="38" y="28.2" font-size="10.5" text-anchor="end">100</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">1 Mar</text><line class="line" x1="365.4" y1="220" x2="365.4" y2="224"/><text class="dim" x="365.4" y="236" font-size="10.5" text-anchor="middle">1 Nis</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">30 Nis</text><polyline class="curve3" style="stroke-width:1.4" points="44.0,67.3 54.4,51.3 64.7,160.5 75.1,171.2 85.5,106.3 95.8,136.5 106.2,107.2 116.6,73.5 126.9,28.2 137.3,178.3 147.7,182.7 158.0,93.0 168.4,112.6 178.8,99.2 189.1,88.6 199.5,34.4 209.9,179.2 220.2,198.7 230.6,95.7 241.0,79.7 251.3,114.3 261.7,98.4 272.1,69.1 282.4,135.6 292.8,186.3 303.2,108.1 313.5,113.4 323.9,110.8 334.3,76.2 344.6,46.9 355.0,142.8 365.4,192.5 375.7,121.4 386.1,106.3 396.5,88.6 406.8,81.5 417.2,63.7 427.6,178.3 437.9,180.0 448.3,88.6 458.7,102.8 469.0,108.1 479.4,85.0 489.8,59.3 500.1,147.2 510.5,205.8 520.9,101.9 531.2,93.9 541.6,110.8 552.0,79.7 562.3,57.5 572.7,147.2 583.1,196.0 593.4,114.3 603.8,93.0 614.2,122.3 624.5,66.4 634.9,70.8 645.3,125.9 655.6,173.8 666.0,144.5"/><polyline class="curve" style="stroke-width:2.4" points="44.0,134.8 54.4,117.9 64.7,125.9 75.1,89.5 85.5,95.7 95.8,131.2 106.2,119.7 116.6,125.9 126.9,102.8 137.3,120.6 147.7,132.1 158.0,118.8 168.4,94.8 178.8,86.8 189.1,101.9 199.5,108.1 209.9,109.0 220.2,125.0 230.6,127.7 241.0,94.8 251.3,109.9 261.7,119.7 272.1,154.3 282.4,110.8 292.8,98.4 303.2,110.8 313.5,144.5 323.9,141.0 334.3,118.8 344.6,96.6 355.0,103.7 365.4,109.9 375.7,123.2 386.1,116.1 396.5,93.9 406.8,99.2 417.2,116.1 427.6,151.6 437.9,139.2 448.3,106.3 458.7,102.8 469.0,122.3 479.4,125.9 489.8,121.4 500.1,90.4 510.5,116.1 520.9,129.4 531.2,120.6 541.6,123.2 552.0,117.9 562.3,116.1 572.7,116.1 583.1,106.3 593.4,118.8 603.8,117.9 614.2,129.4 624.5,116.1 634.9,129.4 645.3,108.1 655.6,85.9 666.0,116.1"/><line class="curve3" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">diff()  düne göre</text><line class="curve" x1="219" y1="22" x2="237" y2="22"/><text class="ink" x="243" y="26" font-size="11">diff(7)  geçen haftaya göre</text></svg>
  <figcaption>Mart–Nisan 2024. Gri çizgi bir önceki güne göre fark: her hafta aynı zikzağı çiziyor. Mor çizgi geçen haftanın aynı gününe göre fark: haftalık desen gitmiş, sıfırın çevresinde dar bir bantta.</figcaption>
</figure>

Günlük farkların yayılımı 46.1; haftalık farkların yayılımı 17.1. Sebep açık:
cumartesiyi cumayla karşılaştırmak haftanın desenini ölçüyor, cumartesiyi
geçen cumartesiyle karşılaştırmak **gerçek değişimi.** Mevsim uzunluğu kadar
geriye giderek alınan farka **mevsimsel fark** deniyor ve mevsimselliği
seriden çıkarıyor. Bölüm 11'de durağanlık için bunu kullanacağız.

Fark almak geri alınabiliyor: `diff` ile `cumsum` birbirinin tersi.

```python
back = s.diff().cumsum() + s.iloc[0]      # ilk deger haric seriyi geri verir
```

## `pct_change`: yüzde değişim

Fark mutlak sayı veriyor; büyüklüğü serinin düzeyine bağlı. Yüzde değişim
düzeyden bağımsız:

```python
print(round(s.pct_change().loc["2024-03-09"] * 100, 1))     # 33.3   dune gore
print(round(s.pct_change(7).loc["2024-03-09"] * 100, 1))    # 3.2    gecen haftaya gore
```

9 Mart cumartesi satış düne göre %33.3 arttı. Bu bir haber değil; her
cumartesi böyle. Geçen cumartesiye göre artış %3.2: asıl bilgi bu.

**Neyle karşılaştırdığın, ne söylediğini belirliyor.** Aylık düzeyde:

```python
daily_mean = s.resample("ME").mean()

mom = daily_mean.pct_change() * 100       # bir onceki aya gore
yoy = daily_mean.pct_change(12) * 100     # gecen yilin ayni ayina gore

print(mom.round(1).loc["2024-01":"2024-04"].tolist())   # [-11.5, -0.3, -1.7, -7.3]
print(yoy.round(1).loc["2024-01":"2024-04"].tolist())   # [11.9, 12.8, 16.4, 10.5]
```

Aynı dört ay, iki ayrı hikâye. Bir önceki aya göre satış **her ay düşüyor**;
geçen yıla göre **her ay %10'dan fazla büyüyor.** İkisi de doğru:

- **Aydan aya** değişim mevsimselliği içeriyor. Aralık tepesinden sonra Ocak
  her yıl düşüyor.
- **Yıldan yıla** değişim aynı mevsimi karşılaştırdığı için mevsimselliği
  dışarıda bırakıyor ve trendi gösteriyor.

Mevsimselliği olan bir seride "büyüyor muyuz?" sorusunun cevabı yıldan yıla
değişimde.

## "Geçen yılın aynı günü" tuzağı

Günlük veride yıldan yıla karşılaştırma için kaç gün geriye gidilir? 365 akla
ilk gelen:

```python
print(s.loc["2024-03-09"])                # 384   cumartesi
print(s.shift(365).loc["2024-03-09"])     # 265   10 Mart 2023, cuma
print(s.shift(364).loc["2024-03-09"])     # 323   11 Mart 2023, cumartesi
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>9 Mart 2024</span><span>cumartesi · satış <b>384</b></span></div>
    <div class="anat-row"><span>365 gün önce</span><span>10 Mart 2023, <b>cuma</b> · 265 · büyüme <b>%45</b> görünüyor</span></div>
    <div class="anat-row"><span>364 gün önce</span><span>11 Mart 2023, <b>cumartesi</b> · 323 · büyüme <b>%19</b></span></div>
  </div>
  <figcaption>365 = 52 × 7 + 1. Bir günlük kayma, cumartesiyi cumayla karşılaştırmak demek. 364 tam 52 hafta.</figcaption>
</figure>

365 gün geriye gitmek **haftanın başka bir gününe** düşüyor, çünkü 365, 7'ye
tam bölünmüyor. Cumartesiyi cumayla karşılaştırınca büyüme %45 görünüyor;
cumartesiyi cumartesiyle karşılaştırınca %19.

364 gün tam 52 hafta. Yılın tamamında farkı ölç:

```python
yoy_364 = (s / s.shift(364) - 1) * 100
yoy_365 = (s / s.shift(365) - 1) * 100

print(round(yoy_364.loc["2024"].std(), 1))    # 7.2
print(round(yoy_365.loc["2024"].std(), 1))    # 18.7
```

365 ile yapılan karşılaştırma gün gün 18.7 puanlık bir oynama gösteriyor;
bunun çoğu büyüme değil, haftanın günlerinin karışması. **Haftalık deseni
olan günlük seride yıllık karşılaştırma için 364 gün.**

## Eksik günlerde `shift` yanılıyor

`shift(1)` "bir gün önce" demek değil, **"bir satır önce"** demek. Satırlar
tam ve sıralıysa ikisi aynı şey. Değilse:

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

print(fixed.loc["2024-07-13":"2024-07-19"])
```

```text
date
2024-07-13    344
2024-07-14    312
2024-07-18    253
2024-07-19    292
```

```python
print(fixed.diff().loc["2024-07-18"])                  # -59.0
print(fixed.asfreq("D").diff().loc["2024-07-18"])      # nan
```

İlk satır 18 Temmuz için "düne göre -59" diyor. Oysa bir önceki satır 14
Temmuz: **dört gün önce.** Hata yok; sayı makul görünüyor ve yanlış.

Önce takvime oturtulunca (`asfreq("D")`) 17 Temmuz için boş bir satır oluyor
ve fark dürüstçe `NaN` çıkıyor. Bölüm 03'teki kuralın sebebi buydu: **fark ve
gecikme hesabından önce seri düzenli olmalı.**

## `cumsum`: birikim

Ters yöne gidelim: değişimlerden toplama.

```python
ytd = s.loc["2024"].cumsum()

print(ytd.iloc[-1])                          # 107611   yil sonu toplami
print((ytd >= 50000).idxmax().date())        # 2024-06-28
```

`cumsum` her satıra o güne kadarki toplamı yazıyor: **yıl başından bugüne**
(year to date). 2024'te 50 bin birime 28 Haziran'da ulaşıldı; 2023'te aynı
eşiğe 24 Temmuz'da. İki yılı birikimli çizmek, aradaki farkın yıl boyunca
nasıl açıldığını gösteriyor.

## Getiriler

Fiyat serilerinde yüzde değişimin özel bir adı var: **getiri** (return).

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
r = close.pct_change()

print(round(r.std() * 100, 2))                      # 1.72   gunluk oynaklik
print(r.idxmax().date(), round(r.max() * 100, 2))   # 2023-03-02 5.3
```

**Yüzdeler toplanmaz.** Üç yılın toplam getirisini bulmak için günlük
getirileri toplarsan yanlış çıkıyor:

```python
print(round((close.iloc[-1] / close.iloc[0] - 1) * 100, 1))   # 66.1   gercek
print(round(r.sum() * 100, 1))                                # 62.3   yanlis
print(round(((1 + r).cumprod().iloc[-1] - 1) * 100, 1))       # 66.1   dogru
```

Getiriler **çarpılarak** birikiyor: %10 artıp sonra %10 düşen fiyat başladığı
yere dönmüyor, 99'a iniyor (`100 × 1.10 × 0.90`). Birikimli getiri bu yüzden
`cumsum` değil `(1 + r).cumprod()`.

Toplanabilen bir getiri istiyorsan **logaritmik getiri**:

```python
import numpy as np

log_r = np.log(close).diff()
print(round((np.exp(log_r.sum()) - 1) * 100, 1))     # 66.1
```

Ayrıntıları "Getiriler ve Birikim" notunda.

Son bir gözlem, ileride çok önemli olacak:

```python
print(round(close.corr(close.shift(1)), 4))     # 0.9927
print(round(r.corr(r.shift(1)), 3))             # 0.045
```

Bugünün **fiyatı** dünün fiyatına neredeyse birebir bağlı. Bugünün
**getirisi** ise dünün getirisinden bağımsız. Fiyatın düzeyi tahmin
edilebilir görünüyor ama değişimi edilemiyor. Bu serinin adı rastgele yürüyüş
ve Bölüm 11–12'de geri döneceğiz.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Özellik olarak `shift(-1)` kullanmak | Model geleceği görüyor | Özellikler için pozitif `shift` |
| Eksik günlü seride `shift` / `diff` | "Dün" aslında günler öncesi | Önce `asfreq` |
| Yıllık karşılaştırmada `shift(365)` | Haftanın başka günü | `shift(364)` |
| Mevsimsel seride aydan aya değişime bakmak | Mevsimsellik "düşüş" sanılıyor | Yıldan yıla değişim |
| Günlük getirileri toplamak | Yanlış toplam getiri | `(1 + r).cumprod()` ya da log getiri |
| Baştaki `NaN`'leri unutmak | Model hata veriyor ya da satır kayıyor | `dropna()`; kaç satır gittiğini bil |
| Yüzde ile yüzde puanı karıştırmak | %10'dan %12'ye "yüzde 2 arttı" | 2 **puan**, yüzde 20 |

## Özet

- **`shift(k)`** k satır önceki değeri bugünün satırına getiriyor: gecikme
  (lag). İlk k satır `NaN`.
- **`shift(-k)`** geleceği getiriyor; yalnızca hedef kurarken.
- **`diff(k)`** k satır önceye göre fark. `diff(7)` mevsimsel fark:
  haftalık deseni çıkarıyor.
- **`pct_change(k)`** yüzde değişim. Aydan aya mevsimselliği, yıldan yıla
  trendi gösteriyor.
- Günlük veride yıllık karşılaştırma **364 gün**; 365 haftanın gününü
  kaydırıyor.
- `shift` ve `diff` **satır** sayıyor, gün değil. Önce `asfreq`.
- **`cumsum`** birikimi veriyor. Getiriler çarpılarak birikiyor:
  `(1 + r).cumprod()`.
