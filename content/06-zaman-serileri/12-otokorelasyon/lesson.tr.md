# Otokorelasyon

Bölüm 06'da bir soru sormuştun: bugünkü satış, dünkü satış hakkında ne
söylüyor? Cevabı iki sayıyla ölçmüştün: 1 gün öncesiyle korelasyon 0.695,
7 gün öncesiyle 0.958.

Bu bölüm o soruyu **bütün gecikmeler için** soruyor ve cevabı tek bir grafikte
topluyor. Bir serinin kendi geçmişiyle korelasyonuna **otokorelasyon** deniyor;
serinin hafızasının haritası. Bölüm 17'de ARIMA'yı kurarken bu haritayı
okuyarak karar vereceksin.

## 1. Otokorelasyon fonksiyonu (ACF)

Her gecikme `k` için serinin `k` adım önceki hâliyle korelasyonu:

```python
import pandas as pd
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

values = acf(s, nlags=21)
print(values.round(2).tolist())
# [1.0, 0.69, 0.28, 0.11, 0.1, 0.26, 0.67, 0.94, 0.67, 0.26, ...]
```

Dönen dizinin ilk elemanı gecikme 0 (serinin kendisiyle korelasyonu, her zaman
1), sonra gecikme 1, 2, 3...

Sayılar `s.corr(s.shift(k))` ile bulduklarına çok yakın ama birebir aynı değil
(7. gecikme: 0.958 yerine 0.94). `acf` her gecikmede serinin **tamamının**
ortalamasını ve varyansını kullanıyor; `corr` ise o gecikmede üst üste gelen
parçanınkini. Standart olan `acf`.

## 2. Korelogram

ACF değerlerinin çubuk grafiğine **korelogram** deniyor:

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="line" x1="40" y1="172.7" x2="666" y2="172.7"/><text class="dim" x="34" y="176.2" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="103.8" x2="666" y2="103.8"/><text class="dim" x="34" y="107.3" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="34.9" x2="666" y2="34.9"/><text class="dim" x="34" y="38.4" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="214" x2="666" y2="214"/><line class="line" x1="62.2" y1="214" x2="62.2" y2="218"/><text class="dim" x="62.2" y="230" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="256.1" y1="214" x2="256.1" y2="218"/><text class="dim" x="256.1" y="230" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="449.9" y1="214" x2="449.9" y2="218"/><text class="dim" x="449.9" y="230" font-size="10.5" text-anchor="middle">14</text><line class="line" x1="643.8" y1="214" x2="643.8" y2="218"/><text class="dim" x="643.8" y="230" font-size="10.5" text-anchor="middle">21</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="164.5" x2="666" y2="164.5"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="180.8" x2="666" y2="180.8"/><rect class="dot" x="54.5" y="34.9" width="15.3" height="137.8" rx="3" opacity="0.9"/><rect class="dot" x="82.2" y="77.1" width="15.3" height="95.6" rx="3" opacity="0.9"/><rect class="dot" x="109.9" y="134.6" width="15.3" height="38.1" rx="3" opacity="0.9"/><rect class="dot" x="137.6" y="158.1" width="15.3" height="14.6" rx="3" opacity="0.9"/><rect class="dot" x="165.3" y="159.0" width="15.3" height="13.7" rx="3" opacity="0.9"/><rect class="dot" x="193.0" y="136.4" width="15.3" height="36.3" rx="3" opacity="0.9"/><rect class="dot" x="220.7" y="80.5" width="15.3" height="92.2" rx="3" opacity="0.9"/><rect class="dot" x="248.4" y="43.7" width="15.3" height="129.0" rx="3" opacity="0.9"/><rect class="dot" x="276.1" y="80.8" width="15.3" height="91.9" rx="3" opacity="0.9"/><rect class="dot" x="303.8" y="137.2" width="15.3" height="35.5" rx="3" opacity="0.9"/><rect class="dot" x="331.5" y="161.2" width="15.3" height="11.5" rx="3" opacity="0.9"/><rect class="dot" x="359.2" y="161.8" width="15.3" height="10.9" rx="3" opacity="0.9"/><rect class="dot" x="386.9" y="139.3" width="15.3" height="33.4" rx="3" opacity="0.9"/><rect class="dot" x="414.6" y="83.8" width="15.3" height="88.9" rx="3" opacity="0.9"/><rect class="dot" x="442.3" y="47.2" width="15.3" height="125.5" rx="3" opacity="0.9"/><rect class="dot" x="470.0" y="84.0" width="15.3" height="88.7" rx="3" opacity="0.9"/><rect class="dot" x="497.7" y="139.9" width="15.3" height="32.8" rx="3" opacity="0.9"/><rect class="dot" x="525.4" y="163.4" width="15.3" height="9.3" rx="3" opacity="0.9"/><rect class="dot" x="553.1" y="164.0" width="15.3" height="8.7" rx="3" opacity="0.9"/><rect class="dot" x="580.8" y="141.9" width="15.3" height="30.8" rx="3" opacity="0.9"/><rect class="dot" x="608.5" y="87.0" width="15.3" height="85.7" rx="3" opacity="0.9"/><rect class="dot" x="636.2" y="50.8" width="15.3" height="121.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Günlük satışın otokorelasyonu</text></svg>
  <figcaption>Yatay eksen gecikme (gün), dikey eksen korelasyon. Kesik çizgiler güven bandı (±0.059). 7, 14 ve 21. gecikmelerdeki tepeler haftalık desen.</figcaption>
</figure>

Aynı grafiği statsmodels tek satırda çiziyor:

```python
from statsmodels.graphics.tsaplots import plot_acf

fig = plot_acf(s, lags=21)
fig.savefig("chart.png")
```

Grafikte iki şey var:

**Çubuklar.** Her gecikmenin korelasyonu. Günlük satışta 7, 14 ve 21. gecikmeler
tepe yapıyor: haftalık desen. Aradaki gecikmeler (3, 4) neredeyse sıfır:
cumartesi ile salı birbirine benzemiyor.

**Güven bandı.** Seri tamamen rastgele olsaydı bile çubuklar tam sıfır çıkmazdı;
şans eseri biraz oynarlardı. Bant bu oynamanın sınırı:

$$\pm \frac{1.96}{\sqrt{n}}$$

1096 gözlem için ±0.059. **Bandın içindeki çubuk sıfırdan ayırt edilemez.**
Dışındaki çubuk gerçek bir ilişkiye işaret ediyor. Dikkat: bant %95'lik; rastgele
bir seride bile 20 çubuktan 1'i dışarı taşabilir.

Seri kısaldıkça bant genişler: 100 gözlemde ±0.196. Kısa seride küçük
korelasyonlara güvenme.

## 3. Dört iz

Korelogramın şekli, serinin ne tür bir hafıza taşıdığını söyler. Dört temel
şekil var:

<figure class="fig">
  <svg viewBox="0 0 680 392" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="126.7" x2="316" y2="126.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="140.8" x2="316" y2="140.8"/><rect class="dot" x="47.0" y="34.2" width="7.4" height="99.6" rx="3" opacity="0.9"/><rect class="dot" x="60.4" y="35.4" width="7.4" height="98.4" rx="3" opacity="0.9"/><rect class="dot" x="73.8" y="36.8" width="7.4" height="97.0" rx="3" opacity="0.9"/><rect class="dot" x="87.2" y="38.1" width="7.4" height="95.7" rx="3" opacity="0.9"/><rect class="dot" x="100.6" y="39.5" width="7.4" height="94.3" rx="3" opacity="0.9"/><rect class="dot" x="114.0" y="40.8" width="7.4" height="93.0" rx="3" opacity="0.9"/><rect class="dot" x="127.4" y="42.1" width="7.4" height="91.7" rx="3" opacity="0.9"/><rect class="dot" x="140.8" y="43.5" width="7.4" height="90.3" rx="3" opacity="0.9"/><rect class="dot" x="154.2" y="44.8" width="7.4" height="89.0" rx="3" opacity="0.9"/><rect class="dot" x="167.6" y="46.1" width="7.4" height="87.7" rx="3" opacity="0.9"/><rect class="dot" x="181.0" y="47.4" width="7.4" height="86.4" rx="3" opacity="0.9"/><rect class="dot" x="194.4" y="48.5" width="7.4" height="85.3" rx="3" opacity="0.9"/><rect class="dot" x="207.8" y="49.7" width="7.4" height="84.1" rx="3" opacity="0.9"/><rect class="dot" x="221.2" y="50.8" width="7.4" height="83.0" rx="3" opacity="0.9"/><rect class="dot" x="234.6" y="51.9" width="7.4" height="81.9" rx="3" opacity="0.9"/><rect class="dot" x="248.0" y="52.9" width="7.4" height="80.9" rx="3" opacity="0.9"/><rect class="dot" x="261.4" y="53.9" width="7.4" height="79.9" rx="3" opacity="0.9"/><rect class="dot" x="274.8" y="55.0" width="7.4" height="78.8" rx="3" opacity="0.9"/><rect class="dot" x="288.2" y="56.0" width="7.4" height="77.8" rx="3" opacity="0.9"/><rect class="dot" x="301.6" y="57.1" width="7.4" height="76.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Trend: fiyat</text></g><g transform="translate(350,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="127.8" x2="316" y2="127.8"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="139.7" x2="316" y2="139.7"/><rect class="dot2" x="47.0" y="63.9" width="7.4" height="69.9" rx="3" opacity="0.9"/><rect class="dot2" x="60.4" y="106.0" width="7.4" height="27.8" rx="3" opacity="0.9"/><rect class="dot2" x="73.8" y="123.1" width="7.4" height="10.7" rx="3" opacity="0.9"/><rect class="dot2" x="87.2" y="123.8" width="7.4" height="10.0" rx="3" opacity="0.9"/><rect class="dot2" x="100.6" y="107.2" width="7.4" height="26.6" rx="3" opacity="0.9"/><rect class="dot2" x="114.0" y="66.4" width="7.4" height="67.4" rx="3" opacity="0.9"/><rect class="dot2" x="127.4" y="39.5" width="7.4" height="94.3" rx="3" opacity="0.9"/><rect class="dot2" x="140.8" y="66.6" width="7.4" height="67.2" rx="3" opacity="0.9"/><rect class="dot2" x="154.2" y="107.9" width="7.4" height="25.9" rx="3" opacity="0.9"/><rect class="dot2" x="167.6" y="125.4" width="7.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="181.0" y="125.8" width="7.4" height="8.0" rx="3" opacity="0.9"/><rect class="dot2" x="194.4" y="109.4" width="7.4" height="24.4" rx="3" opacity="0.9"/><rect class="dot2" x="207.8" y="68.8" width="7.4" height="65.0" rx="3" opacity="0.9"/><rect class="dot2" x="221.2" y="42.1" width="7.4" height="91.7" rx="3" opacity="0.9"/><rect class="dot2" x="234.6" y="69.0" width="7.4" height="64.8" rx="3" opacity="0.9"/><rect class="dot2" x="248.0" y="109.8" width="7.4" height="24.0" rx="3" opacity="0.9"/><rect class="dot2" x="261.4" y="127.0" width="7.4" height="6.8" rx="3" opacity="0.9"/><rect class="dot2" x="274.8" y="127.5" width="7.4" height="6.3" rx="3" opacity="0.9"/><rect class="dot2" x="288.2" y="111.3" width="7.4" height="22.5" rx="3" opacity="0.9"/><rect class="dot2" x="301.6" y="71.1" width="7.4" height="62.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Mevsim: günlük satış</text></g><g transform="translate(0,196)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="126.7" x2="316" y2="126.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="140.8" x2="316" y2="140.8"/><rect class="dot" x="47.0" y="129.7" width="7.4" height="4.1" rx="3" opacity="0.9"/><rect class="dot" x="60.4" y="126.3" width="7.4" height="7.5" rx="3" opacity="0.9"/><rect class="dot" x="73.8" y="132.2" width="7.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="87.2" y="129.8" width="7.4" height="4.0" rx="3" opacity="0.9"/><rect class="dot" x="100.6" y="133.8" width="7.4" height="6.2" rx="3" opacity="0.9"/><rect class="dot" x="114.0" y="133.8" width="7.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="127.4" y="132.5" width="7.4" height="1.3" rx="3" opacity="0.9"/><rect class="dot" x="140.8" y="130.1" width="7.4" height="3.7" rx="3" opacity="0.9"/><rect class="dot" x="154.2" y="133.8" width="7.4" height="1.4" rx="3" opacity="0.9"/><rect class="dot" x="167.6" y="133.8" width="7.4" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="181.0" y="133.8" width="7.4" height="5.6" rx="3" opacity="0.9"/><rect class="dot" x="194.4" y="133.8" width="7.4" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="207.8" y="133.8" width="7.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="221.2" y="133.8" width="7.4" height="5.7" rx="3" opacity="0.9"/><rect class="dot" x="234.6" y="133.4" width="7.4" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="248.0" y="133.8" width="7.4" height="0.7" rx="3" opacity="0.9"/><rect class="dot" x="261.4" y="131.1" width="7.4" height="2.7" rx="3" opacity="0.9"/><rect class="dot" x="274.8" y="133.8" width="7.4" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="288.2" y="133.8" width="7.4" height="6.5" rx="3" opacity="0.9"/><rect class="dot" x="301.6" y="133.8" width="7.4" height="2.2" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Beyaz gürültü: fiyatın farkı</text></g><g transform="translate(350,196)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot2" x="47.0" y="61.1" width="7.4" height="72.7" rx="3" opacity="0.9"/><rect class="dot2" x="60.4" y="82.9" width="7.4" height="50.9" rx="3" opacity="0.9"/><rect class="dot2" x="73.8" y="95.3" width="7.4" height="38.5" rx="3" opacity="0.9"/><rect class="dot2" x="87.2" y="105.7" width="7.4" height="28.1" rx="3" opacity="0.9"/><rect class="dot2" x="100.6" y="114.9" width="7.4" height="18.9" rx="3" opacity="0.9"/><rect class="dot2" x="114.0" y="121.1" width="7.4" height="12.7" rx="3" opacity="0.9"/><rect class="dot2" x="127.4" y="122.6" width="7.4" height="11.2" rx="3" opacity="0.9"/><rect class="dot2" x="140.8" y="122.0" width="7.4" height="11.8" rx="3" opacity="0.9"/><rect class="dot2" x="154.2" y="122.1" width="7.4" height="11.7" rx="3" opacity="0.9"/><rect class="dot2" x="167.6" y="121.9" width="7.4" height="11.9" rx="3" opacity="0.9"/><rect class="dot2" x="181.0" y="122.4" width="7.4" height="11.4" rx="3" opacity="0.9"/><rect class="dot2" x="194.4" y="122.2" width="7.4" height="11.6" rx="3" opacity="0.9"/><rect class="dot2" x="207.8" y="123.0" width="7.4" height="10.8" rx="3" opacity="0.9"/><rect class="dot2" x="221.2" y="123.3" width="7.4" height="10.5" rx="3" opacity="0.9"/><rect class="dot2" x="234.6" y="123.9" width="7.4" height="9.9" rx="3" opacity="0.9"/><rect class="dot2" x="248.0" y="125.4" width="7.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="261.4" y="124.5" width="7.4" height="9.3" rx="3" opacity="0.9"/><rect class="dot2" x="274.8" y="123.8" width="7.4" height="10.0" rx="3" opacity="0.9"/><rect class="dot2" x="288.2" y="126.8" width="7.4" height="7.0" rx="3" opacity="0.9"/><rect class="dot2" x="301.6" y="128.4" width="7.4" height="5.4" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Kısa hafıza: sıcaklık sapması</text></g></svg>
  <figcaption>Dört serinin ilk 20 gecikmesi. Her şekil farklı bir hafıza türünün parmak izi.</figcaption>
</figure>

| Şekil | Anlamı | Örnek |
|---|---|---|
| Çok yavaş sönen, hepsi yüksek | Trend: seri durağan değil | Fiyat: 0.99, 0.94, 0.87, 0.76... |
| Düzenli aralıklarla tepe | Mevsim | Satış: 7, 14, 21 |
| Hepsi bandın içinde | Beyaz gürültü: hafıza yok | Fiyatın farkı |
| Hızla sönen | Kısa hafıza | Sıcaklık sapması: 0.72, 0.51, 0.38... |

## 4. Önce durağanlaştır

Fiyat serisinin ACF'si 50. gecikmede hâlâ 0.57. Bu "fiyat 50 gün öncesini
hatırlıyor" demek değil; yalnızca "seride trend var" demek. Trend bütün
gecikmeleri yükseltir ve altındaki asıl yapıyı gizler.

**ACF'yi durağan seri üzerinde oku** (Bölüm 11). Günlük satışın mevsimsel
farkında:

```python
d7 = s.diff(7).dropna()
print(acf(d7, nlags=8).round(2).tolist()[1:])
# [0.16, 0.05, 0.13, 0.09, 0.1, 0.03, -0.41, 0.02]
```

Haftalık tepeler gitti. İki şey kaldı: 1. gecikmede küçük bir artı (0.16) ve
7. gecikmede belirgin bir eksi (−0.41). Bunlar serinin gerçek kısa dönem
hafızası; Bölüm 17'deki model tam olarak bunları yakalamaya çalışacak.

## 5. Kısmi otokorelasyon (PACF)

Günlük sıcaklığın mevsim normalinden sapmasına bak (o gün, o takvim günü
ortalamasından kaç derece farklı):

```python
t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"]

normal = t.groupby(t.index.dayofyear).transform("mean")
anomaly = t - normal

print(acf(anomaly, nlags=4).round(2).tolist()[1:])
# [0.72, 0.51, 0.38, 0.28]
```

Bugün ile dün 0.72, bugün ile iki gün önce 0.51 korelasyonlu. Peki iki gün
öncesi bugünü **doğrudan** mı etkiliyor, yoksa yalnızca dün üzerinden mi?

Dikkat et: 0.72 × 0.72 = 0.52. İki gün önceki sıcaklık dünü etkiledi, dün de
bugünü. 0.51'in tamamı bu **zincirden** geliyor olabilir.

**Kısmi otokorelasyon** tam bu soruyu cevaplıyor: aradaki gecikmelerin etkisi
çıkarıldıktan sonra `k` gecikmesinin **doğrudan** katkısı.

```python
from statsmodels.tsa.stattools import pacf

print(pacf(anomaly, nlags=4).round(2).tolist()[1:])
# [0.72, -0.03, 0.06, -0.02]
```

<figure class="fig">
  <svg viewBox="0 0 680 190" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="60.8" y1="164" x2="60.8" y2="168"/><text class="dim" x="60.8" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="86.9" y1="164" x2="86.9" y2="168"/><text class="dim" x="86.9" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="138.9" y1="164" x2="138.9" y2="168"/><text class="dim" x="138.9" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="191.0" y1="164" x2="191.0" y2="168"/><text class="dim" x="191.0" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="243.1" y1="164" x2="243.1" y2="168"/><text class="dim" x="243.1" y="180" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="295.2" y1="164" x2="295.2" y2="168"/><text class="dim" x="295.2" y="180" font-size="10.5" text-anchor="middle">10</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot" x="53.7" y="61.1" width="14.3" height="72.7" rx="3" opacity="0.9"/><rect class="dot" x="79.7" y="82.9" width="14.3" height="50.9" rx="3" opacity="0.9"/><rect class="dot" x="105.7" y="95.3" width="14.4" height="38.5" rx="3" opacity="0.9"/><rect class="dot" x="131.8" y="105.7" width="14.3" height="28.1" rx="3" opacity="0.9"/><rect class="dot" x="157.8" y="114.9" width="14.3" height="18.9" rx="3" opacity="0.9"/><rect class="dot" x="183.9" y="121.1" width="14.3" height="12.7" rx="3" opacity="0.9"/><rect class="dot" x="209.9" y="122.6" width="14.3" height="11.2" rx="3" opacity="0.9"/><rect class="dot" x="235.9" y="122.0" width="14.4" height="11.8" rx="3" opacity="0.9"/><rect class="dot" x="262.0" y="122.1" width="14.3" height="11.7" rx="3" opacity="0.9"/><rect class="dot" x="288.0" y="121.9" width="14.3" height="11.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">ACF: toplam ilişki</text></g><g transform="translate(350,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="60.8" y1="164" x2="60.8" y2="168"/><text class="dim" x="60.8" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="86.9" y1="164" x2="86.9" y2="168"/><text class="dim" x="86.9" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="138.9" y1="164" x2="138.9" y2="168"/><text class="dim" x="138.9" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="191.0" y1="164" x2="191.0" y2="168"/><text class="dim" x="191.0" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="243.1" y1="164" x2="243.1" y2="168"/><text class="dim" x="243.1" y="180" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="295.2" y1="164" x2="295.2" y2="168"/><text class="dim" x="295.2" y="180" font-size="10.5" text-anchor="middle">10</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot2" x="53.7" y="61.0" width="14.3" height="72.8" rx="3" opacity="0.9"/><rect class="dot2" x="79.7" y="133.8" width="14.3" height="3.2" rx="3" opacity="0.9"/><rect class="dot2" x="105.7" y="127.9" width="14.4" height="5.9" rx="3" opacity="0.9"/><rect class="dot2" x="131.8" y="133.8" width="14.3" height="2.1" rx="3" opacity="0.9"/><rect class="dot2" x="157.8" y="133.8" width="14.3" height="3.1" rx="3" opacity="0.9"/><rect class="dot2" x="183.9" y="133.7" width="14.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot2" x="209.9" y="128.5" width="14.3" height="5.3" rx="3" opacity="0.9"/><rect class="dot2" x="235.9" y="129.0" width="14.4" height="4.8" rx="3" opacity="0.9"/><rect class="dot2" x="262.0" y="132.4" width="14.3" height="1.4" rx="3" opacity="0.9"/><rect class="dot2" x="288.0" y="131.1" width="14.3" height="2.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">PACF: doğrudan katkı</text></g></svg>
  <figcaption>Sıcaklık sapması. ACF adım adım sönüyor; PACF'de yalnızca 1. gecikme var. Uzun kuyruk, tek bir doğrudan bağın yankısı.</figcaption>
</figure>

İkinci gecikmenin doğrudan katkısı −0.03: yok. Bugünü tahmin etmek için dünü
bilmek yetiyor; iki gün öncesi ek bilgi taşımıyor. ACF'deki uzun kuyruk yalnızca
dünün etkisinin yankısı.

Bir benzetme: dedikodu kulaktan kulağa yayılıyor. Üç kişi önceki söylenenle
senin duyduğun benziyor (ACF), ama sen onu yalnızca yanındakinden duydun
(PACF).

Çizimi: `plot_pacf(anomaly, lags=20)`.

## 6. İki temel süreç: AR ve MA

Durağan serilerdeki kısa hafıza iki temel biçimde ortaya çıkar.

**AR (otoregresif):** bugün, dünün bir katı artı yeni bir şok.

$$y_t = 0.7\, y_{t-1} + e_t$$

Şokun etkisi her gün 0.7 ile çarpılarak sönüyor: uzun ama zayıflayan bir yankı.
Sıcaklık sapması tam böyle bir seri.

**MA (hareketli ortalama):** bugün, bugünün şoku artı dünkü şokun bir katı.

$$y_t = e_t + 0.7\, e_{t-1}$$

Şok yalnızca bir gün daha hissediliyor, sonra tamamen kayboluyor: kısa ve
keskin bir yankı. (Bu adın Bölüm 07'deki hareketli ortalamayla ilgisi yok.)

İkisinin korelogramı **birbirinin aynadaki görüntüsü**:

<figure class="fig">
  <svg viewBox="0 0 680 392" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot" x="56.8" y="48.6" width="17.7" height="66.8" rx="3" opacity="0.9"/><rect class="dot" x="88.9" y="70.3" width="17.7" height="45.1" rx="3" opacity="0.9"/><rect class="dot" x="121.0" y="84.7" width="17.7" height="30.7" rx="3" opacity="0.9"/><rect class="dot" x="153.1" y="92.7" width="17.7" height="22.7" rx="3" opacity="0.9"/><rect class="dot" x="185.2" y="97.6" width="17.7" height="17.8" rx="3" opacity="0.9"/><rect class="dot" x="217.3" y="98.0" width="17.7" height="17.4" rx="3" opacity="0.9"/><rect class="dot" x="249.4" y="99.7" width="17.7" height="15.7" rx="3" opacity="0.9"/><rect class="dot" x="281.5" y="103.5" width="17.7" height="11.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">AR(1) · ACF</text></g><g transform="translate(350,0)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot2" x="56.8" y="48.5" width="17.7" height="66.9" rx="3" opacity="0.9"/><rect class="dot2" x="88.9" y="115.4" width="17.7" height="1.7" rx="3" opacity="0.9"/><rect class="dot2" x="121.0" y="114.8" width="17.7" height="0.6" rx="3" opacity="0.9"/><rect class="dot2" x="153.1" y="112.1" width="17.7" height="3.3" rx="3" opacity="0.9"/><rect class="dot2" x="185.2" y="113.3" width="17.7" height="2.1" rx="3" opacity="0.9"/><rect class="dot2" x="217.3" y="108.5" width="17.7" height="6.9" rx="3" opacity="0.9"/><rect class="dot2" x="249.4" y="114.8" width="17.7" height="0.6" rx="3" opacity="0.9"/><rect class="dot2" x="281.5" y="115.4" width="17.7" height="2.8" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">AR(1) · PACF</text></g><g transform="translate(0,196)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot" x="56.8" y="71.0" width="17.7" height="44.4" rx="3" opacity="0.9"/><rect class="dot" x="88.9" y="115.4" width="17.7" height="3.6" rx="3" opacity="0.9"/><rect class="dot" x="121.0" y="115.4" width="17.7" height="4.3" rx="3" opacity="0.9"/><rect class="dot" x="153.1" y="115.4" width="17.7" height="3.1" rx="3" opacity="0.9"/><rect class="dot" x="185.2" y="115.4" width="17.7" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="217.3" y="109.6" width="17.7" height="5.8" rx="3" opacity="0.9"/><rect class="dot" x="249.4" y="109.2" width="17.7" height="6.2" rx="3" opacity="0.9"/><rect class="dot" x="281.5" y="112.6" width="17.7" height="2.8" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">MA(1) · ACF</text></g><g transform="translate(350,196)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot2" x="56.8" y="70.9" width="17.7" height="44.5" rx="3" opacity="0.9"/><rect class="dot2" x="88.9" y="115.4" width="17.7" height="30.4" rx="3" opacity="0.9"/><rect class="dot2" x="121.0" y="98.8" width="17.7" height="16.6" rx="3" opacity="0.9"/><rect class="dot2" x="153.1" y="115.4" width="17.7" height="13.7" rx="3" opacity="0.9"/><rect class="dot2" x="185.2" y="105.8" width="17.7" height="9.6" rx="3" opacity="0.9"/><rect class="dot2" x="217.3" y="113.9" width="17.7" height="1.5" rx="3" opacity="0.9"/><rect class="dot2" x="249.4" y="113.0" width="17.7" height="2.4" rx="3" opacity="0.9"/><rect class="dot2" x="281.5" y="115.0" width="17.7" height="0.4" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">MA(1) · PACF</text></g></svg>
  <figcaption>Üst satır AR(1), alt satır MA(1); ikisinde de katsayı 0.7, 600 gözlem. AR'da ACF sönüyor, PACF kesiliyor; MA'da tam tersi.</figcaption>
</figure>

<figure class="fig">
<div class="versus">
<div><h4>AR(1)</h4><p>ACF: <b>yavaşça sönüyor</b> (0.69, 0.46, 0.32, 0.23).</p><p>PACF: 1. gecikmeden sonra <b>kesiliyor</b> (0.69, −0.02, 0.01).</p></div>
<div><h4>MA(1)</h4><p>ACF: 1. gecikmeden sonra <b>kesiliyor</b> (0.46, −0.04, −0.04).</p><p>PACF: <b>yavaşça sönüyor</b>, işaret değiştirerek (0.46, −0.31, 0.17).</p></div>
</div>
<figcaption>Kesilen grafik mertebeyi söylüyor: PACF 2. gecikmeden sonra kesiliyorsa AR(2), ACF 3. gecikmeden sonra kesiliyorsa MA(3).</figcaption>
</figure>

Şimdilik bu iki şekli tanımak yeterli. Bölüm 17'de ARIMA'nın `p` ve `q`
sayılarını tam olarak bu grafiklerden okuyacaksın.

## 7. Hafıza kaldı mı? Ljung–Box testi

Korelogramda 20 çubuğa tek tek bakmak yerine tek bir soru: **ilk m gecikmenin
hepsi birden sıfır mı?**

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(acorr_ljungbox(k.diff().dropna(), lags=[10]))
#       lb_stat  lb_pvalue
# 10     12.026      0.283
```

Testin varsayımı "seri beyaz gürültü". p = 0.283: reddedilemiyor. Fiyatın günlük
değişiminde ilk 10 gecikmede kullanılabilir bir hafıza görünmüyor; rastgele
yürüyüş teşhisiyle (Bölüm 11) uyumlu.

```python
print(acorr_ljungbox(d7, lags=[14]))
#       lb_stat  lb_pvalue
# 14    261.782        0.0
```

Satışın mevsimsel farkında p = 0.000: içinde hâlâ modellenebilir yapı var.

Bu testin asıl işi **model denetimi**. Bir model kurduktan sonra kalıntıya
uygularsın: p büyükse model hafızanın tamamını almış; küçükse kalıntıda hâlâ
bilgi var ve model eksik. Bölüm 10'daki ayrıştırmaların kalıntısı bu testten
geçemiyor (p = 0.000): ayrıştırma trend ve mevsimi alıyor, kısa dönem hafızayı
almıyor. Onu almak ARIMA'nın işi.

## 8. Periyodu bulmak

Mevsimin boyunu bilmiyorsan ACF söyler. Saatlik elektrik tüketiminde:

```python
load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)
load = load["load_mw"]

values = acf(load, nlags=200)
print(values[[12, 24, 48, 168]].round(2).tolist())
# [-0.47, 0.88, 0.77, 0.87]
```

12 saat sonrası **ters** yönde (gündüz–gece), 24 saat sonrası 0.88 (aynı saat),
168 saat sonrası 0.87 (aynı saat, aynı gün). İki periyot var: 24 ve 168.
Bölüm 10'da `MSTL(periods=(24, 168))` demenin gerekçesi bu.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Trendli seride ACF okumak | Her gecikme yüksek; yapı görünmüyor | Önce durağanlaştır |
| Bandın içindeki çubuğu yorumlamak | Gürültüden anlam çıkarmak | Yalnızca bandı aşanlara bak |
| Bandı aşan tek bir uzak gecikmeye anlam yüklemek | 20'de 1 şans eseri aşar | Mantıklı bir gecikme mi (7, 12, 24)? |
| ACF ile PACF'yi karıştırmak | Yanlış model mertebesi | ACF: toplam ilişki. PACF: doğrudan katkı |
| `acf` dizisinde gecikme 0'ı unutmak | Bir kaydırılmış okuma | `values[k]` gecikme `k`; `values[0]` hep 1 |
| Seride `NaN` varken çağırmak | Sonuç `NaN` | `dropna()` |
| Kısa seride çok gecikme | Geniş bant, güvenilmez değerler | En çok `n / 4` gecikme |
| Ljung–Box'ta büyük p'yi "model doğru" sanmak | Aşırı güven | "Kalan hafıza bulunamadı" demek |

## Özet

- **Otokorelasyon**: serinin kendi gecikmesiyle korelasyonu. **ACF** bütün
  gecikmeleri verir; grafiği **korelogram**.
- **Güven bandı** ±1.96/√n: içindeki çubuk sıfırdan ayırt edilemez.
- Dört iz: yavaş sönüş (trend), düzenli tepeler (mevsim), hepsi bantta (beyaz
  gürültü), hızlı sönüş (kısa hafıza).
- ACF'yi **durağan** seri üzerinde oku.
- **PACF**: aradaki gecikmelerin etkisi çıkarıldıktan sonra doğrudan katkı.
- **AR**: ACF sönüyor, PACF kesiliyor. **MA**: ACF kesiliyor, PACF sönüyor.
- **Ljung–Box**: "ilk m gecikme birden sıfır mı"; kalıntı denetiminin standart
  testi.

Artık bir seriyi tanıyabiliyorsun: bileşenleri, durağanlığı, hafızası. Tahmine
geçmeden önce son bir hazırlık kaldı: gerçek veri eksik ve kirli gelir. Bölüm 13
eksik veriyi ve aykırı değerleri ele alıyor.
