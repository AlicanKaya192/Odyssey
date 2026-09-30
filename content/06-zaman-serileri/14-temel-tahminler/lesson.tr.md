# Temel Tahminler

On dört bölümdür seriyi **anlamaya** çalışıyorsun: tarihler, desenler,
bileşenler, hafıza, temizlik. Şimdi ilk kez geleceğe bakıyorsun.

Başlangıç noktası şaşırtıcı derecede basit: dört yöntem, her biri tek satır.
Bunlara **temel tahminler** (baseline) deniyor ve iki işleri var. Birincisi,
çoğu zaman düşündüğünden iyi çalışıyorlar. İkincisi ve daha önemlisi, bir
**çıta** koyuyorlar: bundan sonra kuracağın her model önce bunları geçmek
zorunda. Geçemiyorsa karmaşıklığının hiçbir anlamı yok.

## 1. Tahminin dili

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Eğitim verisi</span><span>Tahmini yaparken bildiğin geçmiş. Model yalnızca bunu görür.</span></div>
<div class="anat-row"><span>Test verisi</span><span>Bilmiyormuş gibi yaptığın, tahminle karşılaştırmak için sakladığın son dönem.</span></div>
<div class="anat-row"><span>Başlangıç</span><span>Eğitim verisinin son anı. Tahmin buradan ileriye yapılır.</span></div>
<div class="anat-row"><span>Ufuk</span><span>Kaç adım ileriye tahmin ettiğin: 1 gün, 28 gün, 12 ay.</span></div>
</div>
<figcaption>Tek kural: tahmin, <b>başlangıç anına kadar bilinenle</b> yapılır. Test verisine bakan her hesap hiledir.</figcaption>
</figure>

Günlük mağaza satışında son 28 günü saklayalım:

```python
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D").loc[:"2024-12-03"]

train = s.iloc[:-28]          # 2022-01-01 ... 2024-11-05
test = s.iloc[-28:]           # 2024-11-06 ... 2024-12-03
h = len(test)                 # ufuk: 28 gun
```

Zaman serisinde eğitim ve test **rastgele** ayrılmaz (makine öğrenmesindeki
gibi karıştırılmaz): test her zaman **sonda**, çünkü gelecek geçmişten sonra
gelir.

Tahmin de bir seridir; indeksi gelecekteki tarihler:

```python
future = pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=h, freq="D")
```

## 2. Dört temel yöntem

**Ortalama.** Gelecek, geçmişin ortalaması kadar olacak.

```python
mean_fc = pd.Series(train.mean(), index=future)            # hep 255.1
```

**Naif.** Gelecek, son gözlem kadar olacak.

```python
naive_fc = pd.Series(train.iloc[-1], index=future)         # hep 267
```

**Mevsimsel naif.** Her gün, bir önceki mevsimin aynı günü kadar olacak: son
haftayı kopyala, gerektiği kadar tekrarla.

```python
last_week = train.iloc[-7:].to_numpy()
snaive_fc = pd.Series([last_week[i % 7] for i in range(h)], index=future)
```

`i % 7` kalanı 0'dan 6'ya döndürüyor: 8. gün yine 1. günün değerini alıyor.

**Kayma (drift).** Naif tahmine, serinin ilk gününden son gününe ortalama
günlük değişimi ekle: ilk ve son noktayı birleştiren doğruyu uzat.

```python
slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
drift_fc = pd.Series(train.iloc[-1] + slope * np.arange(1, h + 1), index=future)
```

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="220.0" x2="666" y2="220.0"/><text class="dim" x="38" y="223.5" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="183.0" x2="666" y2="183.0"/><text class="dim" x="38" y="186.5" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="146.0" x2="666" y2="146.0"/><text class="dim" x="38" y="149.5" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="109.0" x2="666" y2="109.0"/><text class="dim" x="38" y="112.5" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="72.0" x2="666" y2="72.0"/><text class="dim" x="38" y="75.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="35.0" x2="666" y2="35.0"/><text class="dim" x="38" y="38.5" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">9 Eki</text><line class="line" x1="202.3" y1="240" x2="202.3" y2="244"/><text class="dim" x="202.3" y="256" font-size="10.5" text-anchor="middle">23 Eki</text><line class="line" x1="360.7" y1="240" x2="360.7" y2="244"/><text class="dim" x="360.7" y="256" font-size="10.5" text-anchor="middle">6 Kas</text><line class="line" x1="519.0" y1="240" x2="519.0" y2="244"/><text class="dim" x="519.0" y="256" font-size="10.5" text-anchor="middle">20 Kas</text><rect class="box" x="355.0" y="32" width="311.0" height="208" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,216.3 55.3,191.9 66.6,150.4 77.9,114.2 89.2,137.8 100.5,217.0 111.9,221.5 123.2,188.2 134.5,183.7 145.8,154.1 157.1,106.0 168.4,151.2 179.7,201.5 191.0,209.6 202.3,182.2 213.6,191.1 224.9,155.6 236.3,97.9 247.6,135.6 258.9,203.7 270.2,202.2 281.5,193.3 292.8,187.4 304.1,137.8 315.4,92.7 326.7,132.7 338.0,203.7 349.3,207.4 360.7,195.6 372.0,178.5 383.3,145.2 394.6,76.4 405.9,128.2 417.2,200.0 428.5,205.9 439.8,180.8 451.1,180.8 462.4,129.0 473.7,102.3 485.1,114.2 496.4,203.0 507.7,197.8 519.0,197.8 530.3,171.9 541.6,133.4 552.9,96.4 564.2,121.6 575.5,205.9 586.8,192.6 598.1,185.2 609.5,185.2 620.8,156.3 632.1,85.3 643.4,114.2 654.7,205.9 666.0,190.4"/><polyline class="curve4" style="stroke-width:2.2" points="360.7,216.2 372.0,216.2 383.3,216.2 394.6,216.2 405.9,216.2 417.2,216.2 428.5,216.2 439.8,216.2 451.1,216.2 462.4,216.2 473.7,216.2 485.1,216.2 496.4,216.2 507.7,216.2 519.0,216.2 530.3,216.2 541.6,216.2 552.9,216.2 564.2,216.2 575.5,216.2 586.8,216.2 598.1,216.2 609.5,216.2 620.8,216.2 632.1,216.2 643.4,216.2 654.7,216.2 666.0,216.2"/><polyline class="curve2" style="stroke-width:2.2" points="360.7,207.4 372.0,207.4 383.3,207.4 394.6,207.4 405.9,207.4 417.2,207.4 428.5,207.4 439.8,207.4 451.1,207.4 462.4,207.4 473.7,207.4 485.1,207.4 496.4,207.4 507.7,207.4 519.0,207.4 530.3,207.4 541.6,207.4 552.9,207.4 564.2,207.4 575.5,207.4 586.8,207.4 598.1,207.4 609.5,207.4 620.8,207.4 632.1,207.4 643.4,207.4 654.7,207.4 666.0,207.4"/><polyline class="curve" style="stroke-width:2.2" points="360.7,193.3 372.0,187.4 383.3,137.8 394.6,92.7 405.9,132.7 417.2,203.7 428.5,207.4 439.8,193.3 451.1,187.4 462.4,137.8 473.7,92.7 485.1,132.7 496.4,203.7 507.7,207.4 519.0,193.3 530.3,187.4 541.6,137.8 552.9,92.7 564.2,132.7 575.5,203.7 586.8,207.4 598.1,193.3 609.5,187.4 620.8,137.8 632.1,92.7 643.4,132.7 654.7,203.7 666.0,207.4"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve4" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">ortalama</text><line class="curve2" x1="244" y1="40" x2="262" y2="40"/><text class="ink" x="268" y="44" font-size="11">naif</text><line class="curve" x1="318" y1="40" x2="336" y2="40"/><text class="ink" x="342" y="44" font-size="11">mevsimsel naif</text></svg>
  <figcaption>Gölgeli bölge test dönemi (28 gün); solundaki her şey eğitim verisi. Ortalama ve naif düz birer çizgi; kayma naifin neredeyse üstünde kaldığı için çizilmedi. Mevsimsel naif son haftayı dört kez tekrarlıyor.</figcaption>
</figure>

## 3. Ölç

Tahmin hatası, gerçek eksi tahmin. Tek bir sayıya indirmek için en sade ölçü
**ortalama mutlak hata** (MAE): hataların işaretini atıp ortalamasını al.

```python
def mae(actual, forecast):
    return (actual - forecast).abs().mean()
```

| Yöntem | MAE (28 gün) |
|---|---|
| Ortalama | 76.0 |
| Kayma | 64.6 |
| Naif | 64.1 |
| Mevsimsel naif | 11.6 |

Günde ortalama 331 birim satılan bir dönemde mevsimsel naif 12 birim
yanılıyor: %3.5. Hiçbir model kurmadan, son haftayı kopyalayarak.

Öbür üçü neden kötü? Hepsi **düz bir çizgi** çiziyor; haftalık deseni
bilmiyorlar. Naif tahmin "salı günü 267 satıldı, o hâlde cumartesi de 267"
diyor. Kayma da yardımcı olmuyor: eğimi yalnızca ilk ve son günden
hesaplıyor, ve ilk gün (1 Ocak 2022) tesadüfen yüksek bir cumartesi. **Kayma
iki noktaya bakar; o iki nokta şanssızsa eğim anlamsız.**

## 4. Her serinin çıtası başka

Hangi temel yöntem en iyisi, serinin yapısına bağlı. Üç seri, üç sonuç:

| Seri | Yapı | Ortalama | Naif | Kayma | Mevsimsel naif |
|---|---|---|---|---|---|
| Günlük satış, 28 gün | Güçlü haftalık desen | 76.0 | 64.1 | 64.6 | **11.6** |
| Hisse fiyatı, 40 gün | Rastgele yürüyüş | 32.3 | 18.8 | **17.6** | mevsim yok |
| Aylık yolcu, 12 ay | Trend + yıllık mevsim | 167.8 | 55.8 | 48.2 | **40.4** |

- **Rastgele yürüyüşte** (Bölüm 11) en taze bilgi son değer: naif ve kayma
  başa baş, ortalama çok geride.
- **Mevsimli seride** mevsimsel naif açık ara önde.
- **Trendli seride ortalama en kötüsü**: 11 yılın ortalaması (222) bugünün
  düzeyinin (345) çok altında.

Genel kural: seriyi tanı (Bölüm 09–12), yapısına uyan temel yöntemi çıta yap.

## 5. Yanlılık: hata hep aynı yöne mi?

Aynı 28 günlük deneyi bir ay sonra yap: eğitim 3 Aralık'a kadar, test Aralık'ın
geri kalanı.

```python
error = test - snaive_fc
print(round(error.abs().mean(), 2), round(error.mean(), 2))     # 40.25 40.25
```

MAE 11.6'dan 40.3'e çıktı. İkinci sayı daha da önemli: hataların **ortalaması**
da 40.25. Mutlak değer almadan ortalama aynı çıkıyorsa **bütün hatalar aynı
işaretli**: tahmin 28 günün 28'inde de düşük kalmış.

Hatanın ortalamasına **yanlılık** (bias) deniyor:

- Sıfıra yakın: tahmin bazen yüksek, bazen düşük; sistematik bir kayma yok.
- Artı: tahmin sistematik olarak **düşük** (gerçek hep üstünde).
- Eksi: tahmin sistematik olarak **yüksek**.

Neden düşük? Aralık yükseliş ayı; mevsimsel naif Kasım sonunun haftasını
kopyalıyor ve yıl sonu tırmanışını göremiyor. **Temel yöntemler bildiğini
tekrar eder; yeni bir yönü öngöremez.**

Yolcu serisinde de aynı: mevsimsel naif 2024 için 2023'ü kopyalıyor. MAE 40.4,
yanlılık +40.4: on iki ayın on ikisinde de düşük. Seri büyüyor ve kopya bir
yıl geride kalıyor.

## 6. Temel yöntemi büyütmek

Yanlılığın nedeni belliyse düzeltmesi de basit. Yolcu serisinde geçen yılın
değerlerini büyüme oranıyla çarp:

```python
p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]

train, test = p.loc[:"2023"], p.loc["2024"]

growth = train.loc["2023"].sum() / train.loc["2022"].sum()      # 1.0993
forecast = train.loc["2023"].to_numpy() * growth
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Oca 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Tem 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Oca 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Tem 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Oca 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Tem 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve2" style="stroke-width:2.2" points="470.5,195.0 488.3,203.8 506.1,177.5 523.8,176.3 541.6,163.2 559.4,131.3 577.1,112.6 594.9,98.2 612.7,147.6 630.5,159.4 648.2,188.8 666.0,162.5"/><polyline class="curve" style="stroke-width:2.2" points="470.5,176.9 488.3,186.5 506.1,157.6 523.8,156.2 541.6,141.8 559.4,106.8 577.1,86.2 594.9,70.4 612.7,124.7 630.5,137.7 648.2,170.0 666.0,141.1"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">gerçek</text><line class="curve2" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">mevsimsel naif</text><line class="curve" x1="286" y1="40" x2="304" y2="40"/><text class="ink" x="310" y="44" font-size="11">mevsimsel naif × büyüme</text></svg>
  <figcaption>2024'ün tahmini. Mevsimsel naif (turuncu) 2023'ün kopyası: şekli doğru, düzeyi on iki ayın hepsinde düşük. Büyüme oranıyla çarpınca (mor) gerçeğin üstüne oturuyor.</figcaption>
</figure>

| Yöntem | MAE | Yüzde hata |
|---|---|---|
| Mevsimsel naif | 40.4 | %10.3 |
| Mevsimsel naif + kayma | 18.5 | %4.6 |
| Mevsimsel naif × büyüme | 11.1 | %2.8 |

Büyüme çarpımsal olduğu için (Bölüm 10) çarpmak, toplamaktan iyi sonuç veriyor.
%2.8 hata: iki satırlık bir tahmin için çok iyi, ve artık **gerçek çıta** bu.
Bölüm 16'daki üstel düzleştirme tam olarak bu fikrin (düzey + trend + mevsim)
özenli hâli.

## 7. Ufuk uzadıkça hata büyür

Yarını tahmin etmek, gelecek ayı tahmin etmekten kolaydır. Ne kadar? Hisse
fiyatında naif tahminin hatası, ufka göre:

```python
k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

for h in (1, 5, 10, 20, 40):
    print(h, round((k.shift(-h) - k).abs().mean(), 2))
# 1 1.83 | 5 4.5 | 10 6.42 | 20 8.76 | 40 12.16
```

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="201.8" x2="666" y2="201.8"/><text class="dim" x="38" y="205.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="148.0" x2="666" y2="148.0"/><text class="dim" x="38" y="151.5" font-size="10.5" text-anchor="end">4</text><line class="grid" x1="44" y1="94.2" x2="666" y2="94.2"/><text class="dim" x="38" y="97.7" font-size="10.5" text-anchor="end">8</text><line class="grid" x1="44" y1="40.3" x2="666" y2="40.3"/><text class="dim" x="38" y="43.8" font-size="10.5" text-anchor="end">12</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="44.0" y1="210" x2="44.0" y2="214"/><text class="dim" x="44.0" y="226" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="107.8" y1="210" x2="107.8" y2="214"/><text class="dim" x="107.8" y="226" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="187.5" y1="210" x2="187.5" y2="214"/><text class="dim" x="187.5" y="226" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="347.0" y1="210" x2="347.0" y2="214"/><text class="dim" x="347.0" y="226" font-size="10.5" text-anchor="middle">20</text><line class="line" x1="506.5" y1="210" x2="506.5" y2="214"/><text class="dim" x="506.5" y="226" font-size="10.5" text-anchor="middle">30</text><line class="line" x1="666.0" y1="210" x2="666.0" y2="214"/><text class="dim" x="666.0" y="226" font-size="10.5" text-anchor="middle">40</text><polyline class="curve3" stroke-dasharray="5 4" style="stroke-width:1.6" points="44.0,177.2 59.9,167.0 75.9,159.2 91.8,152.6 107.8,146.8 123.7,141.5 139.7,136.7 155.6,132.2 171.6,128.0 187.5,124.0 203.5,120.2 219.4,116.6 235.4,113.1 251.3,109.8 267.3,106.5 283.2,103.4 299.2,100.4 315.1,97.4 331.1,94.6 347.0,91.8 363.0,89.1 378.9,86.4 394.9,83.8 410.8,81.3 426.8,78.8 442.7,76.4 458.7,74.0 474.6,71.6 490.6,69.3 506.5,67.0 522.5,64.8 538.4,62.6 554.4,60.5 570.3,58.3 586.3,56.2 602.2,54.2 618.2,52.1 634.1,50.1 650.1,48.2 666.0,46.2"/><polyline class="curve" style="stroke-width:2.4" points="44.0,177.2 59.9,166.4 75.9,156.8 91.8,148.4 107.8,141.3 123.7,135.7 139.7,130.9 155.6,126.0 171.6,120.2 187.5,115.4 203.5,110.7 219.4,107.0 235.4,103.1 251.3,100.1 267.3,96.7 283.2,93.8 299.2,91.0 315.1,88.6 331.1,86.1 347.0,83.9 363.0,81.9 378.9,79.4 394.9,76.8 410.8,74.1 426.8,71.7 442.7,69.5 458.7,66.6 474.6,63.8 490.6,61.4 506.5,58.7 522.5,56.2 538.4,53.4 554.4,50.7 570.3,48.2 586.3,45.9 602.2,43.9 618.2,42.1 634.1,40.4 650.1,39.2 666.0,38.2"/><line class="curve" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">naif tahminin hatası (MAE)</text><line class="curve3" x1="282" y1="38" x2="300" y2="38"/><text class="ink" x="306" y="42" font-size="11">karekök eğrisi</text></svg>
  <figcaption>Yatay eksen ufuk (iş günü), dikey eksen ortalama mutlak hata. Hata büyüyor ama yavaşlayarak; kesik çizgi bir günlük hatanın ufkun kareköküyle çarpımı.</figcaption>
</figure>

Hata ufukla birlikte büyüyor, ama **yavaşlayarak**: 40 kat uzak ufukta 40 kat
değil, 6.7 kat hata. Rastgele adımlar birbirini kısmen götürdüğü için hata
ufkun karekökü kadar büyür (√40 = 6.3).

Günlük satışta mevsimsel naifin hatası: 1 hafta sonrası için 13.4, 4 hafta
sonrası için 17.5, 8 hafta sonrası için 22.9.

**Ufku söylemeden hata söylenmez.** "Modelimin hatası 12" cümlesi eksik:
"28 günlük ufukta ortalama 12" tam.

## 8. Tek adım ve çok adım

Şimdiye kadar **çok adımlı** tahmin yaptın: bir başlangıç noktasından 28 günü
birden. Günlük çalışan bir sistemde ise çoğu zaman her gün yalnızca **yarını**
tahmin edersin ve ertesi gün yeni veriyle yeniden başlarsın: **tek adımlı**
tahmin.

Temel yöntemlerde tek adımlı tahmini `shift` ile bütün geçmiş için tek satırda
kurabilirsin:

```python
naive_1 = s.shift(1)                          # yarin = bugun
snaive_1 = s.shift(7)                         # yarin = gecen haftanin ayni gunu
ma7_1 = s.shift(1).rolling(7).mean()          # yarin = son 7 gunun ortalamasi
```

Bölüm 07'deki kural burada hayati: `rolling` o günü de içerdiği için önce
`shift(1)`. Yoksa tahmin, tahmin ettiği değeri görmüş olur.

2024'ün 366 günü için tek adımlı hatalar:

| Yöntem | MAE |
|---|---|
| Geçmişin ortalaması | 52.5 |
| Son 7 günün ortalaması | 42.7 |
| Naif | 41.1 |
| Mevsimsel naif | 13.9 |

366 ayrı tahmin, 366 ayrı hata: tek bir 28 günlük pencereye göre çok daha
güvenilir bir ölçüm. Bölüm 15 bu fikri (kayan başlangıç) sistemli hâle
getiriyor.

## 9. Çıta

Bir modelin değeri, temel yönteme göre ne kadar iyi olduğudur:

$$\text{beceri} = 1 - \frac{\text{MAE}_{\text{model}}}{\text{MAE}_{\text{temel}}}$$

- 0: temel yöntemle aynı. Model hiçbir şey katmamış.
- 0.5: hatayı yarıya indirmiş.
- Eksi: temel yöntemden **kötü**.

Yolcu serisinde "mevsimsel naif × büyüme"nin mevsimsel naife göre becerisi
1 − 11.1 / 40.4 = 0.73.

Bunun pratik anlamı büyük. Haftalarca uğraşıp kurduğun bir model günlük satışta
MAE 11 veriyorsa başarı gibi görünür, ta ki son haftayı kopyalamanın 11.6
verdiğini görene kadar. **Her tahmin işi, temel yöntemlerin tablosuyla
başlar.**

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Eğitim ve testi rastgele ayırmak | Model geleceği görerek öğrenir | Test her zaman sonda |
| Ortalamayı ya da büyümeyi bütün veriden hesaplamak | Test verisi tahmine sızar | Yalnızca `train` üzerinden |
| Temel yöntemle karşılaştırmamak | Kötü model iyi sanılır | Önce dört temel yöntemin tablosu |
| Mevsimli seride düz naif | Desen yok sayılır | Mevsimsel naif |
| Trendli seride ortalama | Düzey çok geride kalır | Naif, kayma ya da büyümeli mevsimsel naif |
| Yalnızca MAE'ye bakmak | Sistematik kayma görünmez | Yanlılığa (hatanın ortalaması) da bak |
| Ufku söylememek | Hatalar karşılaştırılamaz | "h adımlık ufukta" de |
| Tek adımlı hatayı çok adımlıyla karşılaştırmak | Elma ile armut | Aynı ufuk, aynı dönem |
| `rolling` tahmininde `shift(1)` unutmak | Tahmin kendi hedefini görür | `s.shift(1).rolling(n).mean()` |

## Özet

- **Eğitim** geçmiş, **test** saklanan son dönem; ayrım zaman sırasına göre.
- Dört temel yöntem: **ortalama**, **naif** (son değer), **mevsimsel naif**
  (geçen mevsimin aynı konumu), **kayma** (ilk–son doğrusunu uzat).
- **MAE**: hataların mutlak değerinin ortalaması. **Yanlılık**: hataların
  ortalaması; sıfırdan uzaksa tahmin sistematik olarak kayık.
- En iyi temel yöntem serinin yapısına bağlı: rastgele yürüyüşte naif,
  mevsimli seride mevsimsel naif, büyüyen mevsimli seride büyümeli mevsimsel
  naif.
- **Hata ufukla büyür**; ufku söylemeden hata söylenmez.
- Tek adımlı temel tahminler `shift` ile kurulur; `rolling`'den önce
  `shift(1)`.
- Her modelin **çıtası** temel yöntemdir; beceri = 1 − MAE oranı.

Tek bir 28 günlük pencere şansa açık. Sıradaki bölüm bir tahmini **doğru
biçimde doğrulamayı** öğretiyor: başka hata ölçüleri, kayan başlangıç ve en
sinsi hata olan sızıntı.
