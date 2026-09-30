# Anomali ve Değişim Noktası

Şimdiye kadar serinin **düzenini** öğrendin: trend, mevsim, otokorelasyon. Bu
bölüm düzenin **bozulduğu** anlarla ilgili. Bir sunucu çöktü, bir sensör
takıldı, bir kampanya tuttu, bir rakip çıktı: hepsi seride bir iz bırakır.

İki ayrı soru var. **Anomali**: "bu gözlem olağan mı?" **Değişim noktası**:
"serinin kendisi mi değişti?" İkisinin cevabı, yapılacak iş ve kullanılacak
yöntem farklı.

Bölüm 13'te aykırı değerleri **geriye dönük** buldun ve onardın. Burada iki şey
ekleniyor: **canlı izleme** (yalnızca geçmişi bilerek karar vermek) ve kalıcı
değişimleri yakalamak.

## 1. Beklenmeyenin türleri

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Nokta anomalisi</span><span>Tek bir gözlem her ölçüye göre uçta: kampanya günü, kesinti.</span></div>
<div class="anat-row"><span>Bağlamsal anomali</span><span>Değer kendi başına olağan, <b>o an için</b> değil: gece saatinde gündüz basıncı.</span></div>
<div class="anat-row"><span>Toplu anomali</span><span>Tek tek olağan görünen, birlikte olağan olmayan bir dizi: dokuz saat aynı değeri yazan sensör.</span></div>
<div class="anat-row"><span>Düzey kayması</span><span>Seri yeni bir düzeye geçiyor ve <b>orada kalıyor</b>.</span></div>
<div class="anat-row"><span>Eğim değişimi</span><span>Büyüme hızlanıyor ya da yavaşlıyor; sıçrama yok.</span></div>
<div class="anat-row"><span>Oynaklık değişimi</span><span>Ortalama aynı, gürültü büyüyor ya da küçülüyor.</span></div>
</div>
<figcaption>İlk üçü <b>anomali</b>: geçici, seri eski hâline döner. Son üçü <b>değişim noktası</b>: kalıcı, "olağan"ın tanımı değişir.</figcaption>
</figure>

Web trafiği serisinde (`web_traffic.csv`) dört olay var:

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="228.2" x2="666" y2="228.2"/><text class="dim" x="38" y="231.7" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="185.5" x2="666" y2="185.5"/><text class="dim" x="38" y="189.0" font-size="10.5" text-anchor="end">2,500</text><line class="grid" x1="44" y1="142.8" x2="666" y2="142.8"/><text class="dim" x="38" y="146.3" font-size="10.5" text-anchor="end">5,000</text><line class="grid" x1="44" y1="100.1" x2="666" y2="100.1"/><text class="dim" x="38" y="103.6" font-size="10.5" text-anchor="end">7,500</text><line class="grid" x1="44" y1="57.4" x2="666" y2="57.4"/><text class="dim" x="38" y="60.9" font-size="10.5" text-anchor="end">10,000</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="96.8" y1="240" x2="96.8" y2="244"/><text class="dim" x="96.8" y="256" font-size="10.5" text-anchor="middle">Şub</text><line class="line" x1="146.2" y1="240" x2="146.2" y2="244"/><text class="dim" x="146.2" y="256" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="199.1" y1="240" x2="199.1" y2="244"/><text class="dim" x="199.1" y="256" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="250.2" y1="240" x2="250.2" y2="244"/><text class="dim" x="250.2" y="256" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="303.0" y1="240" x2="303.0" y2="244"/><text class="dim" x="303.0" y="256" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="354.1" y1="240" x2="354.1" y2="244"/><text class="dim" x="354.1" y="256" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="407.0" y1="240" x2="407.0" y2="244"/><text class="dim" x="407.0" y="256" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="459.8" y1="240" x2="459.8" y2="244"/><text class="dim" x="459.8" y="256" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="510.9" y1="240" x2="510.9" y2="244"/><text class="dim" x="510.9" y="256" font-size="10.5" text-anchor="middle">Eki</text><line class="line" x1="563.8" y1="240" x2="563.8" y2="244"/><text class="dim" x="563.8" y="256" font-size="10.5" text-anchor="middle">Kas</text><line class="line" x1="614.9" y1="240" x2="614.9" y2="244"/><text class="dim" x="614.9" y="256" font-size="10.5" text-anchor="middle">Ara</text><polyline class="curve3" style="stroke-width:1.2" points="44.0,161.2 45.7,159.0 47.4,157.8 49.1,163.1 50.8,157.2 52.5,178.4 54.2,177.1 55.9,159.0 57.6,155.8 59.3,163.0 61.0,153.6 62.7,155.7 64.4,180.5 66.2,177.4 67.9,158.4 69.6,165.6 71.3,157.8 73.0,161.9 74.7,160.7 76.4,180.5 78.1,180.1 79.8,159.7 81.5,159.6 83.2,165.0 84.9,160.8 86.6,164.3 88.3,182.0 90.0,179.9 91.7,156.9 93.4,157.7 95.1,161.9 96.8,162.3 98.5,162.7 100.2,178.7 101.9,176.7 103.6,159.8 105.3,157.5 107.1,158.8 108.8,154.6 110.5,166.4 112.2,184.0 113.9,179.5 115.6,157.7 117.3,161.3 119.0,158.4 120.7,163.8 122.4,164.1 124.1,180.7 125.8,176.9 127.5,157.5 129.2,162.3 130.9,159.3 132.6,162.1 134.3,159.8 136.0,181.7 137.7,179.1 139.4,162.4 141.1,160.0 142.8,162.1 144.5,162.6 146.2,159.5 148.0,179.8 149.7,179.0 151.4,161.3 153.1,157.8 154.8,162.6 156.5,157.2 158.2,155.2 159.9,179.7 161.6,174.5 163.3,152.6 165.0,158.4 166.7,164.4 168.4,64.4 170.1,160.5 171.8,174.5 173.5,177.6 175.2,157.2 176.9,160.7 178.6,162.4 180.3,158.6 182.0,163.6 183.7,179.5 185.4,177.7 187.1,159.8 188.8,158.1 190.6,161.4 192.3,157.8 194.0,158.5 195.7,182.9 197.4,181.5 199.1,162.3 200.8,157.6 202.5,158.8 204.2,158.9 205.9,159.3 207.6,177.4 209.3,176.6 211.0,161.8 212.7,165.1 214.4,157.6 216.1,160.6 217.8,159.7 219.5,179.4 221.2,181.7 222.9,164.9 224.6,156.5 226.3,156.0 228.0,156.6 229.7,159.2 231.5,178.4 233.2,180.0 234.9,159.7 236.6,161.3 238.3,161.7 240.0,159.2 241.7,153.8 243.4,183.4 245.1,177.5 246.8,157.6 248.5,163.9 250.2,158.8 251.9,159.5 253.6,161.5 255.3,180.2 257.0,182.4 258.7,153.8 260.4,151.4 262.1,154.3 263.8,160.9 265.5,158.9 267.2,178.1 268.9,181.0 270.6,160.8 272.4,158.0 274.1,161.3 275.8,165.6 277.5,164.1 279.2,178.4 280.9,179.8 282.6,160.9 284.3,155.1 286.0,159.6 287.7,162.3 289.4,160.1 291.1,173.4 292.8,181.7 294.5,153.5 296.2,154.8 297.9,160.4 299.6,161.0 301.3,154.9 303.0,178.4 304.7,180.3 306.4,153.4 308.1,159.3 309.8,158.7 311.5,159.8 313.2,160.9 315.0,178.7 316.7,179.9 318.4,158.1 320.1,156.2 321.8,156.1 323.5,155.7 325.2,154.6 326.9,177.1 328.6,180.5 330.3,156.5 332.0,165.3 333.7,162.3 335.4,75.7 337.1,165.4 338.8,175.3 340.5,181.5 342.2,164.8 343.9,162.4 345.6,162.5 347.3,160.0 349.0,160.4 350.7,176.4 352.4,179.4 354.1,159.3 355.9,163.2 357.6,158.2 359.3,162.5 361.0,166.2 362.7,175.7 364.4,181.5 366.1,163.5 367.8,162.8 369.5,157.6 371.2,164.9 372.9,161.2 374.6,177.6 376.3,174.1 378.0,160.9 379.7,159.7 381.4,162.8 383.1,152.8 384.8,160.4 386.5,179.2 388.2,178.7 389.9,162.9 391.6,159.9 393.3,164.1 395.0,154.6 396.8,160.4 398.5,179.4 400.2,176.1 401.9,163.9 403.6,154.9 405.3,154.5 407.0,162.5 408.7,157.5 410.4,179.3 412.1,176.8 413.8,159.8 415.5,162.9 417.2,157.7 418.9,160.6 420.6,159.3 422.3,176.6 424.0,175.9 425.7,157.7 427.4,164.6 429.1,157.5 430.8,160.9 432.5,156.1 434.2,179.5 435.9,175.4 437.6,158.1 439.4,159.9 441.1,158.9 442.8,165.7 444.5,157.9 446.2,178.7 447.9,181.7 449.6,158.5 451.3,158.8 453.0,158.7 454.7,160.3 456.4,157.1 458.1,177.0 459.8,178.8 461.5,139.7 463.2,141.4 464.9,142.0 466.6,136.6 468.3,141.8 470.0,168.6 471.7,163.5 473.4,134.3 475.1,140.6 476.8,135.4 478.5,137.2 480.3,143.8 482.0,163.2 483.7,164.6 485.4,136.3 487.1,150.9 488.8,135.6 490.5,136.0 492.2,143.4 493.9,160.7 495.6,164.7 497.3,138.6 499.0,135.5 500.7,133.2 502.4,138.6 504.1,136.3 505.8,162.8 507.5,166.5 509.2,131.8 510.9,135.9 512.6,138.7 514.3,134.4 516.0,136.9 517.7,166.0 519.4,160.9 521.2,139.1 522.9,225.8 524.6,135.0 526.3,135.0 528.0,130.5 529.7,163.6 531.4,164.7 533.1,142.5 534.8,142.0 536.5,136.3 538.2,137.4 539.9,143.0 541.6,166.1 543.3,165.6 545.0,132.0 546.7,143.3 548.4,137.6 550.1,146.2 551.8,140.2 553.5,159.5 555.2,168.0 556.9,133.9 558.6,147.2 560.3,139.0 562.0,144.0 563.8,139.3 565.5,164.9 567.2,161.5 568.9,138.0 570.6,138.5 572.3,141.6 574.0,137.2 575.7,142.7 577.4,166.2 579.1,166.1 580.8,136.7 582.5,128.6 584.2,139.5 585.9,130.3 587.6,143.6 589.3,166.0 591.0,162.5 592.7,136.5 594.4,135.8 596.1,131.9 597.8,140.1 599.5,134.3 601.2,163.3 602.9,172.6 604.7,143.5 606.4,141.5 608.1,138.7 609.8,136.8 611.5,140.4 613.2,159.8 614.9,167.2 616.6,139.3 618.3,135.0 620.0,144.0 621.7,133.4 623.4,134.9 625.1,164.6 626.8,164.1 628.5,139.6 630.2,139.1 631.9,133.5 633.6,136.9 635.3,145.1 637.0,168.9 638.7,162.2 640.4,150.1 642.1,145.9 643.8,141.9 645.6,139.3 647.3,133.0 649.0,163.6 650.7,151.9 652.4,138.3 654.1,135.3 655.8,134.6 657.5,139.7 659.2,134.9 660.9,162.2 662.6,163.4 664.3,142.0 666.0,141.1"/><polyline class="curve" style="stroke-width:2.2" points="44.0,165.2 459.8,165.2"/><polyline class="curve" style="stroke-width:2.2" points="461.5,145.8 666.0,145.8"/><circle class="dot2" cx="168.4" cy="64.4" r="4"/><circle class="dot2" cx="335.4" cy="75.7" r="4"/><circle class="dot2" cx="522.9" cy="225.8" r="4"/><text class="ink" x="176.9" y="66.1" font-size="11" text-anchor="start">kampanya</text><text class="ink" x="343.9" y="77.4" font-size="11" text-anchor="start">kampanya</text><text class="ink" x="531.4" y="222.6" font-size="11" text-anchor="start">kesinti</text><text class="ink" x="468.3" y="103.5" font-size="11" text-anchor="start" font-weight="600">düzey kayması</text></svg>
  <figcaption>Bir yıllık günlük ziyaret. Turuncu noktalar üç nokta anomalisi: seri ertesi gün eski hâline dönüyor. 2 Eylül'de ise düzey (mor çizgi) yükseliyor ve orada kalıyor.</figcaption>
</figure>

Ayrım önemli, çünkü tepki farklı: anomali **işaretlenir ve açıklanır**;
değişim noktasından sonra ise **model yeniden kurulur**.

## 2. Anomali, beklenenden sapmadır

Bir pompanın saatlik basıncı (`pump_pressure.csv`, altı hafta). Bakım defterinde
(`pump_events.csv`) 12 olay kayıtlı. En tanıdık yöntem, bütün seriye z-skoru:

```python
import pandas as pd

pressure = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
pressure = pressure["pressure"]
calm = pressure.loc[:"2024-10-06"]                  # son hafta ayri (Kisim 9)

z = (calm - calm.mean()) / calm.std()
print(z[z.abs() > 3].index.strftime("%m-%d %H").tolist())     # ['09-03 14']
```

12 olayın **biri**. Neden? Basınç gün içinde 5.2 ile 6.8 arasında zaten
dolaşıyor; standart sapma 0.57 ve bu oynamanın neredeyse tamamı **günlük
döngü**. 5 Eylül 03:00'teki 5.89 değeri ortalamaya (6.00) çok yakın, z-skoru
−0.2. Ama saat 03:00'te olağan değer 5.22.

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="212.9" x2="666" y2="212.9"/><text class="dim" x="38" y="216.4" font-size="10.5" text-anchor="end">5</text><line class="grid" x1="44" y1="181.0" x2="666" y2="181.0"/><text class="dim" x="38" y="184.5" font-size="10.5" text-anchor="end">5.5</text><line class="grid" x1="44" y1="149.1" x2="666" y2="149.1"/><text class="dim" x="38" y="152.6" font-size="10.5" text-anchor="end">6</text><line class="grid" x1="44" y1="117.2" x2="666" y2="117.2"/><text class="dim" x="38" y="120.7" font-size="10.5" text-anchor="end">6.5</text><line class="grid" x1="44" y1="85.4" x2="666" y2="85.4"/><text class="dim" x="38" y="88.9" font-size="10.5" text-anchor="end">7</text><line class="grid" x1="44" y1="53.5" x2="666" y2="53.5"/><text class="dim" x="38" y="57.0" font-size="10.5" text-anchor="end">7.5</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">4 Eyl</text><line class="line" x1="149.1" y1="230" x2="149.1" y2="234"/><text class="dim" x="149.1" y="246" font-size="10.5" text-anchor="middle">12:00</text><line class="line" x1="254.3" y1="230" x2="254.3" y2="234"/><text class="dim" x="254.3" y="246" font-size="10.5" text-anchor="middle">5 Eyl</text><line class="line" x1="359.4" y1="230" x2="359.4" y2="234"/><text class="dim" x="359.4" y="246" font-size="10.5" text-anchor="middle">12:00</text><line class="line" x1="464.5" y1="230" x2="464.5" y2="234"/><text class="dim" x="464.5" y="246" font-size="10.5" text-anchor="middle">6 Eyl</text><line class="line" x1="569.6" y1="230" x2="569.6" y2="234"/><text class="dim" x="569.6" y="246" font-size="10.5" text-anchor="middle">12:00</text><line class="dim" stroke-dasharray="4 4" x1="44" y1="149.4" x2="666" y2="149.4"/><polyline class="curve" stroke-dasharray="5 4" style="stroke-width:2" points="44.0,193.8 52.8,199.5 61.5,200.8 70.3,198.9 79.0,193.1 87.8,183.6 96.6,174.0 105.3,163.8 114.1,146.6 122.8,134.5 131.6,124.9 140.4,112.8 149.1,105.8 157.9,99.4 166.6,98.1 175.4,100.0 184.2,105.1 192.9,110.9 201.7,125.5 210.5,135.1 219.2,149.8 228.0,163.2 236.7,174.6 245.5,185.5 254.3,193.8 263.0,199.5 271.8,200.8 280.5,198.9 289.3,193.1 298.1,183.6 306.8,174.0 315.6,163.8 324.3,146.6 333.1,134.5 341.9,124.9 350.6,112.8 359.4,105.8 368.1,99.4 376.9,98.1 385.7,100.0 394.4,105.1 403.2,110.9 411.9,125.5 420.7,135.1 429.5,149.8 438.2,163.2 447.0,174.6 455.7,185.5 464.5,193.8 473.3,199.5 482.0,200.8 490.8,198.9 499.5,193.1 508.3,183.6 517.1,174.0 525.8,163.8 534.6,146.6 543.4,134.5 552.1,124.9 560.9,112.8 569.6,105.8 578.4,99.4 587.2,98.1 595.9,100.0 604.7,105.1 613.4,110.9 622.2,125.5 631.0,135.1 639.7,149.8 648.5,163.2 657.2,174.6 666.0,185.5"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,191.9 52.8,186.1 61.5,200.8 70.3,204.6 79.0,192.5 87.8,177.2 96.6,169.5 105.3,156.8 114.1,156.1 122.8,124.9 131.6,120.4 140.4,117.9 149.1,107.7 157.9,110.2 166.6,91.7 175.4,101.3 184.2,109.6 192.9,110.2 201.7,128.7 210.5,139.6 219.2,143.4 228.0,157.4 236.7,165.7 245.5,182.3 254.3,190.6 263.0,203.3 271.8,208.4 280.5,156.1 289.3,189.9 298.1,183.6 306.8,183.6 315.6,161.3 324.3,151.7 333.1,140.2 341.9,120.4 350.6,112.8 359.4,101.9 368.1,101.9 376.9,90.5 385.7,106.4 394.4,93.6 403.2,119.8 411.9,124.3 420.7,133.2 429.5,160.6 438.2,163.8 447.0,172.1 455.7,185.5 464.5,202.7 473.3,192.5 482.0,199.5 490.8,200.2 499.5,197.6 508.3,182.3 517.1,177.8 525.8,167.6 534.6,146.6 543.4,133.8 552.1,114.7 560.9,111.5 569.6,109.0 578.4,98.8 587.2,104.5 595.9,109.0 604.7,105.1 613.4,109.0 622.2,116.0 631.0,135.1 639.7,155.5 648.5,172.1 657.2,168.9 666.0,186.8"/><circle class="dot2" cx="280.5" cy="156.1" r="4.5"/><text class="ink" x="293.7" y="148.5" font-size="11.5" text-anchor="start" font-weight="600">5.89</text><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">basınç</text><line class="curve" x1="142" y1="38" x2="160" y2="38"/><text class="ink" x="166" y="42" font-size="11">o saatin ortancası</text><text class="dim" x="48.4" y="145.5" font-size="10.5" text-anchor="start">genel ortalama</text></svg>
  <figcaption>5 Eylül 03:00'teki değer (turuncu) genel ortalamanın hemen yanında: bütün seriye bakan bir kural onu göremez. Ama gecenin o saatinde beklenen 5.22; sapma açık.</figcaption>
</figure>

Çare Bölüm 13'teki ile aynı fikir: **önce bekleneni çıkar, kalıntıya bak**.
Burada beklenen, o saatin ortancası:

```python
profile = calm.groupby(calm.index.hour).median()
expected = profile.reindex(calm.index.hour).to_numpy()
resid = calm - expected

mad = (resid - resid.median()).abs().median()
score = 0.6745 * (resid - resid.median()) / mad

flagged = score[score.abs() > 3]
print(len(flagged))                                 # 20
```

5 Eylül 03:00'ün puanı 7.5. 20 işaretin 12'si defterdeki olayların **hepsi**.
Kalan sekizi de rastgele değil: hepsi 30 Eylül'de, art arda.

<figure class="fig">
<div class="flow">
<span class="node">Gözlem</span><span class="arrow">→</span>
<span class="node">Beklenen</span><span class="arrow">→</span>
<span class="node">Kalıntı</span><span class="arrow">→</span>
<span class="node">Ölçek (MAD)</span><span class="arrow">→</span>
<span class="node">Puan</span><span class="arrow">→</span>
<span class="node acc">Eşik → alarm</span>
</div>
<figcaption>Her anomali dedektörü bu zincirdir. Yöntemler yalnızca "beklenen"i nasıl kurduklarında ayrılır: saat ortancası, mevsimsel naif, STL, bir tahmin modeli.</figcaption>
</figure>

Bölüm 20'nin diliyle: anomali, **tahmin aralığının dışına düşen** gözlemdir.
İyi bir tahmin modeli aynı zamanda iyi bir anomali dedektörüdür.

## 3. Toplu anomali: takılı sensör

30 Eylül'deki sekiz saat neydi? Değerlere bakınca:

```python
day = pressure.loc["2024-09-30 07:00":"2024-09-30 17:00"]
print(day.nunique(), len(day))                      # 3 11
```

On bir saatte yalnızca üç farklı değer: sensör 08:00'de **takılmış** ve dokuz
saat aynı sayıyı yazmış. Değerin kendisi olağan; olağan olmayan,
**değişmemesi**. Günlük döngü yükselirken sensör yerinde saydığı için kalıntı
saat saat büyümüş ve dedektör bunu dolaylı yoldan yakalamış.

Doğrudan yakalamak daha sağlam: art arda aynı değerlerin uzunluğunu say.

```python
same = pressure.diff() == 0                         # oncekiyle ayni mi
block = (~same).cumsum()                            # her yeni deger yeni blok
length = same.groupby(block).sum() + 1              # bloktaki deger sayisi

print(int(length.max()))                            # 9
print(int((length == 2).sum()))                     # 12
```

İki ondalığa yuvarlanmış bir seride iki komşu değerin tesadüfen eşit çıkması
olağan (12 kez olmuş); dokuz kez üst üste olması değil. Kural: **üç ve üzeri**
tekrar işaretlenir.

Takılı sensör, "değer çok uçta" diye bakan hiçbir kuralın doğrudan göremediği
bir anomali türü. Toplu anomaliler için puan tek gözleme değil, **pencereye**
verilir: tekrar uzunluğu, pencere standart sapması, pencere ortalaması.

## 4. Canlı izleme: yalnızca geçmiş

Kısım 2'deki profil bütün seriden hesaplandı; yani 5 Eylül'ü değerlendirirken
Ekim'in verisi kullanıldı. Geriye dönük temizlikte sorun değil. Ama bir alarm
sistemi **bugünü, bugün** değerlendirir: elinde yalnızca geçmiş vardır. Tahmin
doğrulamadaki kuralın (Bölüm 15) aynısı.

Web trafiğinde beklenen değer: aynı günün **son dört haftadaki** ortancası.

```python
visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

past = pd.concat([visits.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)
expected = past.median(axis=1)
deviation = visits / expected - 1                   # oransal sapma

alarm = deviation.abs() > 0.25
print(int(alarm.sum()))                             # 12
```

Olağan günlerde sapmanın standart sapması %5 civarında; %25 eşiği kabaca beş
standart sapma. 12 alarm: 14 Mart ve 20 Haziran (kampanyalar), 8 Ekim (kesinti)
ve 2–14 Eylül arasında dokuz gün.

**Neden ortanca?** Ortalama kullanılsaydı her anomali, sonraki dört haftanın
beklentisini bozardı:

| 21 Mart (kampanyadan bir hafta sonra) | Beklenen | Gerçek | Sapma |
|---|---|---|---|
| Son dört perşembenin **ortalaması** | 5366 | 4075 | −%24 |
| Son dört perşembenin **ortancası** | 4015 | 4075 | +%1.5 |

Ortalamayla aynı eşik 16 alarm veriyor; fazladan gelenler kampanyanın ve
kesintinin **yankıları**: tamamen olağan günler, bozulmuş bir beklentiyle
karşılaştırıldıkları için alarm veriyor. Dedektörün beklentisi, yakalamaya
çalıştığı şeyden etkilenmemeli: **dayanıklı** istatistik kullan.

## 5. Alarmların dizilişi de bilgidir

12 alarmı art arda gelenleri birleştirerek **olaylara** çevir:

| Olay | Alarm sayısı | Yön | Yorum |
|---|---|---|---|
| 14 Mart | 1 | yukarı | Nokta anomalisi |
| 20 Haziran | 1 | yukarı | Nokta anomalisi |
| 2–14 Eylül | 9 | hep yukarı | **Düzey kayması** |
| 8 Ekim | 1 | aşağı | Nokta anomalisi |

Tek başına bir alarm bir anomalidir. **Aynı yönde art arda** gelen alarmlar ise
serinin yeni bir düzeye geçtiğini söyler. Alarmı tek tek değil, dizisiyle oku.

Dikkat edilecek bir şey daha: Eylül alarmları 14'ünde **kendiliğinden
kesiliyor**. Dört haftalık pencere yeni düzeyle dolunca beklenti de yeni düzeye
çıkıyor. Bu iki ucu keskin bir özellik: dedektör kendini yeniliyor (iyi), ama
iki hafta içinde bakmayan biri değişimi hiç görmeyebilir (kötü). Kalıcı
değişimler ayrıca kaydedilmeli.

## 6. CUSUM: sapmayı biriktir

Eşik dedektörü her günü tek başına değerlendirir. Küçük ama **kalıcı** bir
kayma (diyelim bir standart sapma) hiçbir gün eşiği aşmaz ve hiç fark edilmez.
**CUSUM** (kümülatif toplam) sapmaları biriktirir:

$$S_t = \max(0,\; S_{t-1} + z_t - k)$$

`z`, standartlaştırılmış sapma; `k`, her adımda düşülen **pay** (olağan
oynamanın birikmesini önler); toplam `h` **eşiğini** geçince alarm. Olağan
günlerde `z − k` eksi olduğundan toplam sıfıra yapışık kalır; kalıcı bir
kaymada her gün biraz daha büyür.

Referans dönem Ocak–Şubat: her haftanın gününün ortancası ve oransal sapmanın
standart sapması (0.042) oradan.

```python
ref = visits.loc["2024-01":"2024-02"]
profile = ref.groupby(ref.index.dayofweek).median()
base = profile.reindex(visits.index.dayofweek).to_numpy()

rel = visits / base - 1
sd = (ref / profile.reindex(ref.index.dayofweek).to_numpy() - 1).std()
z = (rel / sd).clip(-3, 3)                          # tek bir gun en cok 3 sayilir

k, h = 1.0, 8.0
total, first = 0.0, None
for day, value in z.items():
    total = max(0.0, total + value - k)
    if total > h and first is None:
        first = day
print(first.strftime("%Y-%m-%d"))                   # 2024-09-05
```

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="199.8" x2="666" y2="199.8"/><text class="dim" x="38" y="203.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="151.4" x2="666" y2="151.4"/><text class="dim" x="38" y="154.9" font-size="10.5" text-anchor="end">4</text><line class="grid" x1="44" y1="102.9" x2="666" y2="102.9"/><text class="dim" x="38" y="106.4" font-size="10.5" text-anchor="end">8</text><line class="grid" x1="44" y1="54.4" x2="666" y2="54.4"/><text class="dim" x="38" y="57.9" font-size="10.5" text-anchor="end">12</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="44.0" y1="210" x2="44.0" y2="214"/><text class="dim" x="44.0" y="226" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="120.8" y1="210" x2="120.8" y2="214"/><text class="dim" x="120.8" y="226" font-size="10.5" text-anchor="middle">Şub</text><line class="line" x1="192.7" y1="210" x2="192.7" y2="214"/><text class="dim" x="192.7" y="226" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="269.5" y1="210" x2="269.5" y2="214"/><text class="dim" x="269.5" y="226" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="343.8" y1="210" x2="343.8" y2="214"/><text class="dim" x="343.8" y="226" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="420.7" y1="210" x2="420.7" y2="214"/><text class="dim" x="420.7" y="226" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="495.0" y1="210" x2="495.0" y2="214"/><text class="dim" x="495.0" y="226" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="571.8" y1="210" x2="571.8" y2="214"/><text class="dim" x="571.8" y="226" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="648.7" y1="210" x2="648.7" y2="214"/><text class="dim" x="648.7" y="226" font-size="10.5" text-anchor="middle">Eyl</text><line class="curve2" stroke-dasharray="4 4" x1="44" y1="102.9" x2="666" y2="102.9"/><line class="curve3" stroke-dasharray="4 4" x1="651.1" y1="20" x2="651.1" y2="210"/><polyline class="curve" style="stroke-width:1.8" points="44.0,199.8 46.5,199.8 49.0,199.8 51.4,199.8 53.9,192.4 56.4,191.0 58.9,196.2 61.3,199.8 63.8,196.1 66.3,199.8 68.8,175.6 71.3,161.4 73.7,172.7 76.2,179.6 78.7,189.2 81.2,199.8 83.6,199.8 86.1,199.8 88.6,199.8 91.1,199.8 93.6,199.8 96.0,199.8 98.5,199.8 101.0,199.8 103.5,199.8 106.0,199.8 108.4,199.8 110.9,199.8 113.4,199.8 115.9,199.8 118.3,199.8 120.8,199.8 123.3,199.8 125.8,199.8 128.3,199.8 130.7,199.8 133.2,199.8 135.7,199.8 138.2,179.1 140.6,199.8 143.1,199.8 145.6,199.8 148.1,199.8 150.6,199.8 153.0,199.8 155.5,199.8 158.0,199.8 160.5,199.8 162.9,199.8 165.4,199.8 167.9,199.8 170.4,199.8 172.9,199.8 175.3,199.8 177.8,199.8 180.3,199.8 182.8,199.8 185.3,199.8 187.7,199.8 190.2,199.8 192.7,199.8 195.2,199.8 197.6,199.8 200.1,199.8 202.6,199.8 205.1,199.8 207.6,190.7 210.0,174.5 212.5,180.9 215.0,171.4 217.5,156.9 219.9,163.9 222.4,197.5 224.9,173.3 227.4,180.1 229.9,155.9 232.3,164.1 234.8,169.1 237.3,186.2 239.8,199.8 242.2,196.8 244.7,199.8 247.2,199.8 249.7,199.8 252.2,199.8 254.6,199.8 257.1,199.8 259.6,193.4 262.1,191.5 264.5,199.8 267.0,199.8 269.5,199.8 272.0,199.8 274.5,199.8 276.9,198.2 279.4,199.8 281.9,192.6 284.4,195.4 286.9,199.8 289.3,199.8 291.8,199.8 294.3,199.8 296.8,199.8 299.2,199.8 301.7,199.8 304.2,199.8 306.7,199.0 309.2,197.6 311.6,185.9 314.1,187.0 316.6,185.4 319.1,199.8 321.5,199.8 324.0,199.8 326.5,199.8 329.0,199.4 331.5,177.3 333.9,199.8 336.4,199.8 338.9,199.8 341.4,199.8 343.8,199.8 346.3,199.8 348.8,199.8 351.3,199.8 353.8,199.8 356.2,190.4 358.7,168.0 361.2,159.0 363.7,165.9 366.2,165.8 368.6,162.6 371.1,190.5 373.6,199.8 376.1,199.8 378.5,199.8 381.0,199.8 383.5,199.8 386.0,198.4 388.5,199.8 390.9,199.8 393.4,193.1 395.9,199.8 398.4,199.8 400.8,199.8 403.3,175.6 405.8,199.8 408.3,189.1 410.8,181.1 413.2,198.1 415.7,199.8 418.2,182.2 420.7,181.0 423.1,199.8 425.6,188.6 428.1,199.5 430.6,199.8 433.1,199.8 435.5,199.8 438.0,199.8 440.5,199.8 443.0,199.8 445.5,197.7 447.9,196.4 450.4,180.6 452.9,161.7 455.4,152.5 457.8,177.6 460.3,179.5 462.8,199.8 465.3,199.8 467.8,175.6 470.2,199.8 472.7,179.4 475.2,199.8 477.7,199.8 480.1,199.8 482.6,199.8 485.1,199.8 487.6,199.8 490.1,186.5 492.5,199.8 495.0,199.8 497.5,199.8 500.0,199.8 502.4,199.8 504.9,199.8 507.4,182.1 509.9,199.8 512.4,199.8 514.8,199.8 517.3,199.8 519.8,199.8 522.3,199.8 524.7,193.5 527.2,181.7 529.7,199.8 532.2,199.8 534.7,199.8 537.1,175.6 539.6,181.9 542.1,185.3 544.6,199.8 547.1,199.8 549.5,199.8 552.0,199.8 554.5,179.3 557.0,185.8 559.4,190.7 561.9,190.2 564.4,199.8 566.9,192.4 569.4,184.4 571.8,198.3 574.3,192.1 576.8,196.0 579.3,199.7 581.7,199.8 584.2,199.8 586.7,199.8 589.2,199.8 591.7,199.8 594.1,187.3 596.6,186.0 599.1,193.0 601.6,199.8 604.0,199.8 606.5,199.8 609.0,187.7 611.5,193.0 614.0,188.5 616.4,197.1 618.9,199.8 621.4,199.8 623.9,199.8 626.4,195.4 628.8,196.1 631.3,199.8 633.8,199.8 636.3,199.8 638.7,199.8 641.2,199.8 643.7,192.1 646.2,182.3 648.7,197.4 651.1,173.2 653.6,149.0 656.1,124.7 658.6,100.5 661.0,76.3 663.5,52.0 666.0,30.2"/><text class="ink" x="53.9" y="96.8" font-size="11" text-anchor="start">eşik h = 8</text><text class="ink" x="641.2" y="49.6" font-size="11" text-anchor="end">2 Eylül</text></svg>
  <figcaption>CUSUM toplamı. Sekiz ay boyunca sıfırın hemen üstünde dolaşıyor; kampanya günleri (Mart, Haziran) kırpıldığı için küçük birer diş. Düzey kaymasından sonra her gün büyüyor ve dördüncü gün eşiği geçiyor.</figcaption>
</figure>

Sekiz ay boyunca toplam en çok 3.9'a çıkıyor. 2 Eylül'den sonra her gün 2
artıyor (2.2, 4.2, 6.2, 8.2) ve dördüncü gün, 5 Eylül'de alarm veriyor.

İki ayrıntı:

- **Kırpma** (`clip(-3, 3)`). Kırpılmazsa 14 Mart'taki tek kampanya günü tek
  başına eşiği aşar ve ilk alarm 14 Mart olur. Kırpınca CUSUM nokta
  anomalilerine **sağır**, kalıcı kaymalara duyarlı hâle gelir: eşik
  dedektörünün tam tersi. İkisi birlikte kullanılır.
- **Alarmdan sonra.** Referans güncellenmezse CUSUM susmaz: toplam her alarmda
  sıfırlansa bile yıl sonuna kadar 23 kez çalar. Alarm "referansın artık
  geçersiz" demektir; yeni düzey öğrenilip referans yenilenir.

`k` ve `h` bir ödünleşim: küçük değerler küçük kaymaları çabuk yakalar ama
yanlış alarm verir (`k = 0.5`, `h = 5` bu seride Eylül'den önce üç kez çalıyor).

## 7. Değişim noktasını geriye dönük bulmak

CUSUM "bir şey değişti" der, ama üç gün gecikmeyle. Elinde bütün seri varken
daha kesin bir soru sorabilirsin: **seriyi hangi günden ikiye bölersem iki
parça kendi içinde en tutarlı olur?**

Her olası kesim için iki parçanın kendi ortalamasından sapmalarının kare
toplamını hesapla; en küçüğü veren kesim değişim noktasıdır.

```python
import numpy as np


def best_split(x, margin=14):
    x = np.asarray(x, dtype=float)
    total = ((x - x.mean()) ** 2).sum()
    best_k, best_sse = None, None
    for k in range(margin, len(x) - margin):
        left, right = x[:k], x[k:]
        sse = ((left - left.mean()) ** 2).sum()
        sse += ((right - right.mean()) ** 2).sum()
        if best_sse is None or sse < best_sse:
            best_k, best_sse = k, sse
    return best_k, 1 - best_sse / total
```

İkinci dönen değer **kazanç**: bölmenin toplam oynamanın ne kadarını
açıkladığı. Aynı seride üç deneme:

| Seri | Bulunan gün | Kazanç |
|---|---|---|
| Ham | 2 Eylül | 0.30 |
| Hafta sonu etkisi giderilmiş | 2 Eylül | 0.52 |
| Ayrıca üç anomali çıkarılmış | 2 Eylül | **0.88** |

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="209.8" x2="666" y2="209.8"/><text class="dim" x="38" y="213.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="167.4" x2="666" y2="167.4"/><text class="dim" x="38" y="170.9" font-size="10.5" text-anchor="end">0.25</text><line class="grid" x1="44" y1="125.0" x2="666" y2="125.0"/><text class="dim" x="38" y="128.5" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="44" y1="82.6" x2="666" y2="82.6"/><text class="dim" x="38" y="86.1" font-size="10.5" text-anchor="end">0.75</text><line class="grid" x1="44" y1="40.2" x2="666" y2="40.2"/><text class="dim" x="38" y="43.7" font-size="10.5" text-anchor="end">1</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="96.8" y1="220" x2="96.8" y2="224"/><text class="dim" x="96.8" y="236" font-size="10.5" text-anchor="middle">Şub</text><line class="line" x1="146.2" y1="220" x2="146.2" y2="224"/><text class="dim" x="146.2" y="236" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="199.1" y1="220" x2="199.1" y2="224"/><text class="dim" x="199.1" y="236" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="250.2" y1="220" x2="250.2" y2="224"/><text class="dim" x="250.2" y="236" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="303.0" y1="220" x2="303.0" y2="224"/><text class="dim" x="303.0" y="236" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="354.1" y1="220" x2="354.1" y2="224"/><text class="dim" x="354.1" y="236" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="407.0" y1="220" x2="407.0" y2="224"/><text class="dim" x="407.0" y="236" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="459.8" y1="220" x2="459.8" y2="224"/><text class="dim" x="459.8" y="236" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="510.9" y1="220" x2="510.9" y2="224"/><text class="dim" x="510.9" y="236" font-size="10.5" text-anchor="middle">Eki</text><line class="line" x1="563.8" y1="220" x2="563.8" y2="224"/><text class="dim" x="563.8" y="236" font-size="10.5" text-anchor="middle">Kas</text><line class="line" x1="614.9" y1="220" x2="614.9" y2="224"/><text class="dim" x="614.9" y="236" font-size="10.5" text-anchor="middle">Ara</text><polyline class="curve3" style="stroke-width:1.6" points="67.9,208.9 69.6,209.0 71.3,208.9 73.0,209.0 74.7,208.9 76.4,208.9 78.1,208.5 79.8,208.1 81.5,208.1 83.2,208.2 84.9,208.1 86.6,208.1 88.3,208.0 90.0,207.5 91.7,207.0 93.4,207.1 95.1,207.2 96.8,207.2 98.5,207.2 100.2,207.1 101.9,206.7 103.6,206.2 105.3,206.3 107.1,206.4 108.8,206.5 110.5,206.7 112.2,206.5 113.9,205.9 115.6,205.4 117.3,205.5 119.0,205.5 120.7,205.6 122.4,205.5 124.1,205.4 125.8,204.8 127.5,204.4 129.2,204.5 130.9,204.5 132.6,204.5 134.3,204.5 136.0,204.6 137.7,203.9 139.4,203.4 141.1,203.3 142.8,203.4 144.5,203.4 146.2,203.3 148.0,203.4 149.7,202.8 151.4,202.2 153.1,202.2 154.8,202.3 156.5,202.3 158.2,202.4 159.9,202.6 161.6,202.0 163.3,201.6 165.0,201.8 166.7,201.9 168.4,201.8 170.1,204.6 171.8,204.6 173.5,204.3 175.2,203.8 176.9,203.9 178.6,203.9 180.3,203.8 182.0,203.9 183.7,203.8 185.4,203.3 187.1,202.8 188.8,202.8 190.6,202.9 192.3,202.9 194.0,202.9 195.7,203.0 197.4,202.4 199.1,201.7 200.8,201.7 202.5,201.8 204.2,201.8 205.9,201.9 207.6,201.9 209.3,201.4 211.0,200.9 212.7,200.8 214.4,200.7 216.1,200.8 217.8,200.8 219.5,200.8 221.2,200.2 222.9,199.5 224.6,199.4 226.3,199.5 228.0,199.6 229.7,199.7 231.5,199.8 233.2,199.2 234.9,198.5 236.6,198.5 238.3,198.5 240.0,198.5 241.7,198.5 243.4,198.7 245.1,197.9 246.8,197.3 248.5,197.4 250.2,197.3 251.9,197.3 253.6,197.3 255.3,197.3 257.0,196.6 258.7,195.8 260.4,196.0 262.1,196.3 263.8,196.5 265.5,196.5 267.2,196.5 268.9,195.9 270.6,195.1 272.4,195.1 274.1,195.1 275.8,195.1 277.5,194.9 279.2,194.7 280.9,194.0 282.6,193.2 284.3,193.2 286.0,193.4 287.7,193.4 289.4,193.3 291.1,193.2 292.8,192.7 294.5,191.8 296.2,192.1 297.9,192.3 299.6,192.2 301.3,192.2 303.0,192.3 304.7,191.6 306.4,190.8 308.1,191.0 309.8,191.0 311.5,191.0 313.2,191.0 315.0,190.9 316.7,190.1 318.4,189.3 320.1,189.3 321.8,189.4 323.5,189.6 325.2,189.7 326.9,189.9 328.6,189.1 330.3,188.2 332.0,188.3 333.7,188.1 335.4,187.9 337.1,191.3 338.8,191.1 340.5,190.4 342.2,189.5 343.9,189.2 345.6,189.1 347.3,188.9 349.0,188.9 350.7,188.8 352.4,188.0 354.1,187.1 355.9,187.1 357.6,186.9 359.3,186.9 361.0,186.7 362.7,186.4 364.4,185.6 366.1,184.6 367.8,184.3 369.5,184.1 371.2,184.1 372.9,183.8 374.6,183.7 376.3,182.8 378.0,182.0 379.7,181.9 381.4,181.8 383.1,181.5 384.8,181.8 386.5,181.7 388.2,180.6 389.9,179.6 391.6,179.3 393.3,179.2 395.0,178.9 396.8,179.0 398.5,178.9 400.2,177.8 401.9,176.8 403.6,176.4 405.3,176.6 407.0,176.7 408.7,176.5 410.4,176.4 412.1,175.3 413.8,174.2 415.5,174.0 417.2,173.7 418.9,173.7 420.6,173.5 422.3,173.3 424.0,172.2 425.7,171.1 427.4,171.0 429.1,170.6 430.8,170.5 432.5,170.3 434.2,170.3 435.9,168.9 437.6,167.8 439.4,167.7 441.1,167.5 442.8,167.3 444.5,166.7 446.2,166.6 447.9,165.2 449.6,163.5 451.3,163.3 453.0,163.1 454.7,163.0 456.4,162.7 458.1,162.6 459.8,161.1 461.5,159.5 463.2,160.6 464.9,161.6 466.6,162.5 468.3,163.7 470.0,164.6 471.7,163.7 473.4,163.2 475.1,164.6 476.8,165.5 478.5,166.8 480.3,168.0 482.0,168.7 483.7,168.2 485.4,167.6 487.1,168.8 488.8,169.0 490.5,170.3 492.2,171.5 493.9,172.2 495.6,171.8 497.3,171.2 499.0,172.2 500.7,173.4 502.4,174.7 504.1,175.7 505.8,176.8 507.5,176.3 509.2,175.6 510.9,177.0 512.6,178.1 514.3,179.1 516.0,180.2 517.7,181.3 519.4,180.6 521.2,180.2 522.9,181.1 524.6,176.8 526.3,178.0 528.0,179.2 529.7,180.6 531.4,180.0 533.1,179.4 534.8,180.1 536.5,180.8 538.2,181.8 539.9,182.8 541.6,183.5 543.3,182.7 545.0,182.0 546.7,183.3 548.4,184.0 550.1,184.9 551.8,185.3 553.5,186.1 555.2,185.8 556.9,184.9 558.6,186.1 560.3,186.4 562.0,187.3 563.8,187.8 565.5,188.6 567.2,188.0 568.9,187.5 570.6,188.4 572.3,189.3 574.0,189.9 575.7,190.8 577.4,191.4 579.1,190.7 580.8,189.9 582.5,190.9 584.2,192.3 585.9,193.0 587.6,194.3 589.3,194.8 591.0,194.1 592.7,193.6 594.4,194.5 596.1,195.5 597.8,196.6 599.5,197.3 601.2,198.2 602.9,197.7 604.7,196.7 606.4,197.2 608.1,197.8 609.8,198.5 611.5,199.4 613.2,200.0 614.9,199.7 616.6,198.9 618.3,199.6 620.0,200.6 621.7,201.0 623.4,202.0 625.1,202.9 626.8,202.3 628.5,201.7 630.2,202.4 631.9,203.1 633.6,204.0 635.3,204.8 637.0,205.2 638.7,204.4 640.4,203.9 642.1,204.0"/><polyline class="curve" style="stroke-width:2.2" points="67.9,207.7 69.6,207.6 71.3,207.1 73.0,207.0 74.7,206.6 76.4,206.4 78.1,206.0 79.8,205.7 81.5,205.5 83.2,205.3 84.9,204.7 86.6,204.4 88.3,203.9 90.0,203.4 91.7,203.0 93.4,203.0 95.1,202.9 96.8,202.5 98.5,202.1 100.2,201.7 101.9,201.4 103.6,201.4 105.3,201.1 107.1,201.0 108.8,200.9 110.5,201.0 112.2,200.3 113.9,199.5 115.6,199.2 117.3,199.1 119.0,198.7 120.7,198.5 122.4,198.0 124.1,197.4 125.8,197.0 127.5,196.9 129.2,196.8 130.9,196.3 132.6,196.1 134.3,195.7 136.0,195.4 137.7,194.8 139.4,194.5 141.1,194.0 142.8,193.7 144.5,193.2 146.2,192.7 148.0,192.5 149.7,192.0 151.4,191.7 153.1,191.3 154.8,191.2 156.5,190.6 158.2,190.5 159.9,190.6 161.6,190.2 163.3,190.3 165.0,190.5 166.7,190.3 168.4,189.7 170.1,189.1 171.8,188.8 173.5,188.9 175.2,188.7 176.9,188.6 178.6,188.2 180.3,187.6 182.0,187.4 183.7,186.8 185.4,186.3 187.1,186.1 188.8,185.8 190.6,185.6 192.3,185.1 194.0,184.9 195.7,184.6 197.4,183.8 199.1,183.1 200.8,182.6 202.5,182.4 204.2,182.1 205.9,181.8 207.6,181.5 209.3,181.2 211.0,181.1 212.7,180.6 214.4,179.7 216.1,179.5 217.8,179.1 219.5,178.7 221.2,178.2 222.9,177.5 224.6,176.6 226.3,176.5 228.0,176.4 229.7,176.3 231.5,175.9 233.2,175.5 234.9,174.9 236.6,174.5 238.3,174.0 240.0,173.4 241.7,173.0 243.4,173.1 245.1,172.0 246.8,171.7 248.5,171.5 250.2,170.7 251.9,170.3 253.6,169.9 255.3,169.2 257.0,168.6 258.7,167.6 260.4,167.7 262.1,168.0 263.8,168.0 265.5,167.4 267.2,167.0 268.9,166.6 270.6,165.8 272.4,165.2 274.1,164.9 275.8,164.2 277.5,163.2 279.2,162.2 280.9,161.7 282.6,161.1 284.3,160.4 286.0,160.3 287.7,159.8 289.4,159.0 291.1,158.4 292.8,158.6 294.5,157.6 296.2,157.6 297.9,157.6 299.6,156.9 301.3,156.2 303.0,156.1 304.7,155.6 306.4,154.7 308.1,154.8 309.8,154.2 311.5,153.7 313.2,153.1 315.0,152.4 316.7,151.7 318.4,150.9 320.1,150.4 321.8,150.2 323.5,149.9 325.2,149.7 326.9,149.6 328.6,149.1 330.3,148.2 332.0,147.9 333.7,146.6 335.4,145.6 337.1,144.5 338.8,143.1 340.5,142.9 342.2,141.8 343.9,140.5 345.6,139.4 347.3,138.3 349.0,137.6 350.7,136.7 352.4,136.3 354.1,135.4 355.9,134.6 357.6,133.4 359.3,132.8 361.0,131.6 362.7,130.0 364.4,129.7 366.1,128.3 367.8,127.0 369.5,125.7 371.2,125.1 372.9,123.5 374.6,122.4 376.3,121.7 378.0,121.5 379.7,120.5 381.4,119.5 383.1,118.1 384.8,118.1 386.5,117.0 388.2,115.9 389.9,114.9 391.6,113.4 393.3,112.3 395.0,110.7 396.8,110.3 398.5,109.2 400.2,107.9 401.9,107.3 403.6,105.6 405.3,105.1 407.0,104.7 408.7,103.2 410.4,102.3 412.1,101.0 413.8,100.2 415.5,98.9 417.2,97.2 418.9,96.3 420.6,94.8 422.3,93.6 424.0,92.7 425.7,92.0 427.4,91.0 429.1,88.9 430.8,87.8 432.5,86.2 434.2,85.4 435.9,83.7 437.6,83.0 439.4,81.8 441.1,80.2 442.8,78.9 444.5,76.3 446.2,75.1 447.9,73.5 449.6,71.1 451.3,69.7 453.0,68.2 454.7,66.7 456.4,64.8 458.1,63.5 459.8,62.1 461.5,60.3 463.2,62.0 464.9,63.4 466.6,64.6 468.3,66.8 470.0,68.0 471.7,68.6 473.4,70.4 475.1,72.9 476.8,74.3 478.5,76.6 480.3,78.6 482.0,79.4 483.7,81.2 485.4,82.6 487.1,84.7 488.8,84.3 490.5,86.5 492.2,88.5 493.9,89.4 495.6,91.6 497.3,92.9 499.0,94.5 500.7,96.6 502.4,99.1 504.1,100.6 505.8,102.6 507.5,104.2 509.2,105.1 510.9,107.7 512.6,109.6 514.3,111.1 516.0,113.2 517.7,114.9 519.4,115.8 521.2,117.8 522.9,119.2 524.6,120.8 526.3,122.8 528.0,124.7 529.7,127.3 531.4,128.7 533.1,129.8 534.8,130.5 536.5,131.4 538.2,133.1 539.9,134.6 541.6,135.3 543.3,136.1 545.0,136.9 546.7,139.2 548.4,139.8 550.1,141.2 551.8,141.4 553.5,142.4 555.2,144.5 556.9,144.8 558.6,146.7 560.3,146.7 562.0,147.9 563.8,148.4 565.5,149.5 567.2,150.4 568.9,152.0 570.6,153.3 572.3,154.5 574.0,155.2 575.7,156.6 577.4,157.2 579.1,157.8 580.8,158.4 582.5,159.9 584.2,162.4 585.9,163.4 587.6,165.6 589.3,166.1 591.0,166.7 592.7,168.0 594.4,169.3 596.1,170.8 597.8,172.8 599.5,173.6 601.2,175.2 602.9,176.3 604.7,175.7 606.4,176.1 608.1,176.8 609.8,177.8 611.5,179.1 613.2,179.9 614.9,181.5 616.6,181.9 618.3,182.8 620.0,184.3 621.7,184.6 623.4,186.2 625.1,187.7 626.8,188.4 628.5,189.3 630.2,190.1 631.9,191.0 633.6,192.6 635.3,193.8 637.0,193.9 638.7,193.9 640.4,195.1 642.1,194.5"/><circle class="dot" cx="461.5" cy="60.3" r="4"/><text class="ink" x="471.7" y="56.9" font-size="11.5" text-anchor="start" font-weight="600">2 Eylül: 0.88</text><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">ham seri</text><line class="curve" x1="156" y1="38" x2="174" y2="38"/><text class="ink" x="180" y="42" font-size="11">hafta sonu giderilmiş, anomaliler onarılmış</text></svg>
  <figcaption>Her olası kesim günü için kazanç. İki eğrinin tepesi aynı günde; ama temizlenmiş seride tepe sivri ve yüksek, ham seride basık. Tepenin sivriliği, değişim gününden ne kadar emin olduğunu gösterir.</figcaption>
</figure>

Üçü de doğru günü buluyor, ama kanıtın gücü çok farklı. Ham seride haftalık
desen ve anomaliler oynamanın büyük kısmını oluşturduğu için düzey kayması
%30'luk bir açıklama gibi görünüyor; temizlenince %88. **Önce yapıyı ve
anomalileri çıkar, sonra değişim ara.**

Düzey 4004'ten 5235'e çıkmış: +%31.

**Başka değişim var mı?** İki parçanın her birine aynı aramayı yeniden uygula:

| Parça | En iyi kesim | Kazanç |
|---|---|---|
| 2 Eylül öncesi | 7 Mart | 0.013 |
| 2 Eylül sonrası | 18 Eylül | 0.015 |

`best_split` **her zaman** bir gün döndürür; değişim olmayan seride de. Karar
kazançtan verilir: 0.88 bir değişim, 0.013 gürültü. Bu "böl, parçalara yeniden
uygula, kazanç küçülünce dur" yöntemine **ikili bölütleme** denir; hazırı
`ruptures` kütüphanesinde var.

## 8. Eğim değişimi

Bir uygulamanın abone sayısı (`subscribers.csv`). Sıçrama yok; seri hep
artıyor. Ama büyüme bir yerde yavaşlamış:

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="50" y1="209.9" x2="666" y2="209.9"/><text class="dim" x="44" y="213.4" font-size="10.5" text-anchor="end">1,000</text><line class="grid" x1="50" y1="162.9" x2="666" y2="162.9"/><text class="dim" x="44" y="166.4" font-size="10.5" text-anchor="end">2,000</text><line class="grid" x1="50" y1="115.9" x2="666" y2="115.9"/><text class="dim" x="44" y="119.4" font-size="10.5" text-anchor="end">3,000</text><line class="grid" x1="50" y1="68.9" x2="666" y2="68.9"/><text class="dim" x="44" y="72.4" font-size="10.5" text-anchor="end">4,000</text><line class="line" x1="50" y1="230" x2="666" y2="230"/><line class="line" x1="50.0" y1="230" x2="50.0" y2="234"/><text class="dim" x="50.0" y="246" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="102.3" y1="230" x2="102.3" y2="234"/><text class="dim" x="102.3" y="246" font-size="10.5" text-anchor="middle">Şub</text><line class="line" x1="151.3" y1="230" x2="151.3" y2="234"/><text class="dim" x="151.3" y="246" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="203.6" y1="230" x2="203.6" y2="234"/><text class="dim" x="203.6" y="246" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="254.2" y1="230" x2="254.2" y2="234"/><text class="dim" x="254.2" y="246" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="306.5" y1="230" x2="306.5" y2="234"/><text class="dim" x="306.5" y="246" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="357.2" y1="230" x2="357.2" y2="234"/><text class="dim" x="357.2" y="246" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="409.5" y1="230" x2="409.5" y2="234"/><text class="dim" x="409.5" y="246" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="461.8" y1="230" x2="461.8" y2="234"/><text class="dim" x="461.8" y="246" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="512.4" y1="230" x2="512.4" y2="234"/><text class="dim" x="512.4" y="246" font-size="10.5" text-anchor="middle">Eki</text><line class="line" x1="564.7" y1="230" x2="564.7" y2="234"/><text class="dim" x="564.7" y="246" font-size="10.5" text-anchor="middle">Kas</text><line class="line" x1="615.4" y1="230" x2="615.4" y2="234"/><text class="dim" x="615.4" y="246" font-size="10.5" text-anchor="middle">Ara</text><polyline class="curve3" style="stroke-width:1.4" points="50.0,209.9 51.7,209.7 53.4,207.3 55.1,208.3 56.8,207.3 58.4,207.0 60.1,206.7 61.8,205.3 63.5,206.2 65.2,205.9 66.9,205.0 68.6,203.0 70.3,202.7 71.9,201.7 73.6,202.7 75.3,202.7 77.0,201.0 78.7,200.8 80.4,200.1 82.1,198.9 83.8,199.9 85.4,199.6 87.1,198.5 88.8,198.5 90.5,197.8 92.2,196.7 93.9,196.2 95.6,195.4 97.3,194.5 98.9,192.9 100.6,191.6 102.3,191.8 104.0,192.0 105.7,190.8 107.4,190.1 109.1,189.6 110.8,189.9 112.4,188.8 114.1,187.7 115.8,188.6 117.5,187.1 119.2,186.7 120.9,186.6 122.6,187.0 124.3,186.1 125.9,185.2 127.6,184.6 129.3,184.6 131.0,184.3 132.7,182.7 134.4,181.9 136.1,181.1 137.8,180.1 139.4,179.2 141.1,177.8 142.8,178.0 144.5,177.9 146.2,178.2 147.9,177.3 149.6,176.5 151.3,176.5 152.9,175.8 154.6,175.1 156.3,172.1 158.0,172.8 159.7,171.8 161.4,171.5 163.1,171.5 164.8,170.9 166.4,170.4 168.1,170.1 169.8,169.8 171.5,169.5 173.2,169.1 174.9,168.2 176.6,167.7 178.3,166.5 180.0,165.2 181.6,165.2 183.3,165.1 185.0,163.8 186.7,163.6 188.4,163.2 190.1,163.0 191.8,162.4 193.5,161.1 195.1,160.3 196.8,160.9 198.5,160.8 200.2,160.3 201.9,159.7 203.6,158.4 205.3,159.3 207.0,157.4 208.6,157.6 210.3,156.1 212.0,156.4 213.7,155.8 215.4,154.4 217.1,153.9 218.8,152.6 220.5,150.8 222.1,151.4 223.8,151.9 225.5,152.0 227.2,152.1 228.9,151.2 230.6,151.2 232.3,151.8 234.0,150.5 235.6,148.0 237.3,147.2 239.0,147.5 240.7,147.2 242.4,145.7 244.1,145.0 245.8,144.7 247.5,143.3 249.1,142.8 250.8,142.7 252.5,142.2 254.2,141.4 255.9,140.1 257.6,140.7 259.3,140.2 261.0,139.7 262.6,140.3 264.3,139.6 266.0,139.6 267.7,138.2 269.4,137.3 271.1,136.3 272.8,135.5 274.5,136.0 276.1,135.0 277.8,133.9 279.5,132.7 281.2,132.3 282.9,132.3 284.6,131.5 286.3,130.0 288.0,129.7 289.6,130.5 291.3,129.3 293.0,128.7 294.7,128.2 296.4,127.8 298.1,127.2 299.8,126.5 301.5,126.9 303.2,125.3 304.8,125.0 306.5,124.4 308.2,124.0 309.9,122.4 311.6,121.4 313.3,120.3 315.0,120.6 316.7,121.3 318.3,120.7 320.0,119.2 321.7,118.0 323.4,118.4 325.1,117.1 326.8,117.8 328.5,117.2 330.2,116.4 331.8,114.8 333.5,115.9 335.2,116.0 336.9,116.4 338.6,115.6 340.3,115.5 342.0,113.7 343.7,113.4 345.3,112.7 347.0,110.2 348.7,109.5 350.4,109.6 352.1,108.7 353.8,107.8 355.5,106.7 357.2,107.1 358.8,106.5 360.5,106.0 362.2,105.6 363.9,105.3 365.6,104.1 367.3,103.2 369.0,104.0 370.7,103.6 372.3,102.8 374.0,101.5 375.7,100.9 377.4,99.8 379.1,99.7 380.8,99.6 382.5,98.8 384.2,97.4 385.8,97.6 387.5,97.7 389.2,97.9 390.9,97.4 392.6,96.4 394.3,96.3 396.0,96.3 397.7,96.3 399.3,96.8 401.0,96.4 402.7,97.7 404.4,96.4 406.1,96.0 407.8,95.0 409.5,94.6 411.2,94.3 412.8,94.6 414.5,93.5 416.2,92.8 417.9,93.7 419.6,93.2 421.3,91.9 423.0,91.9 424.7,92.5 426.4,93.4 428.0,91.7 429.7,92.5 431.4,93.2 433.1,91.6 434.8,90.8 436.5,90.6 438.2,90.1 439.9,90.1 441.5,89.6 443.2,89.4 444.9,89.2 446.6,89.1 448.3,88.6 450.0,89.0 451.7,88.6 453.4,89.4 455.0,89.1 456.7,87.7 458.4,87.6 460.1,87.7 461.8,87.6 463.5,86.7 465.2,87.1 466.9,85.5 468.5,85.6 470.2,85.4 471.9,83.9 473.6,83.1 475.3,84.1 477.0,84.8 478.7,84.8 480.4,84.5 482.0,83.5 483.7,84.1 485.4,83.9 487.1,84.4 488.8,82.9 490.5,82.1 492.2,83.8 493.9,83.1 495.5,82.8 497.2,82.3 498.9,81.9 500.6,81.7 502.3,81.2 504.0,81.2 505.7,80.1 507.4,79.6 509.0,81.4 510.7,80.1 512.4,79.9 514.1,80.5 515.8,80.3 517.5,79.5 519.2,78.5 520.9,77.7 522.5,78.2 524.2,78.3 525.9,77.3 527.6,77.4 529.3,77.6 531.0,78.8 532.7,77.7 534.4,77.0 536.0,77.0 537.7,76.7 539.4,77.5 541.1,76.5 542.8,75.2 544.5,74.5 546.2,75.3 547.9,75.6 549.6,75.5 551.2,75.3 552.9,74.5 554.6,73.7 556.3,74.2 558.0,74.2 559.7,74.6 561.4,72.3 563.1,73.2 564.7,72.0 566.4,71.9 568.1,71.6 569.8,71.4 571.5,71.9 573.2,71.0 574.9,72.0 576.6,71.7 578.2,70.5 579.9,70.2 581.6,71.0 583.3,71.0 585.0,70.9 586.7,69.1 588.4,69.1 590.1,69.0 591.7,68.4 593.4,67.7 595.1,67.9 596.8,67.8 598.5,68.4 600.2,68.0 601.9,69.0 603.6,67.9 605.2,67.0 606.9,67.5 608.6,67.4 610.3,67.3 612.0,67.7 613.7,66.3 615.4,66.5 617.1,66.9 618.7,66.4 620.4,65.3 622.1,65.4 623.8,64.7 625.5,64.5 627.2,64.3 628.9,63.9 630.6,62.8 632.2,62.1 633.9,61.8 635.6,62.0 637.3,62.4 639.0,62.8 640.7,61.2 642.4,60.7 644.1,61.1 645.7,60.8 647.4,60.6 649.1,59.6 650.8,58.9 652.5,60.9 654.2,59.8 655.9,60.0 657.6,59.7 659.2,60.3 660.9,60.1 662.6,59.9 664.3,58.9 666.0,59.2"/><polyline class="curve2" stroke-dasharray="5 4" style="stroke-width:1.8" points="50.0,196.5 51.7,196.1 53.4,195.7 55.1,195.3 56.8,194.8 58.4,194.4 60.1,194.0 61.8,193.6 63.5,193.2 65.2,192.7 66.9,192.3 68.6,191.9 70.3,191.5 71.9,191.0 73.6,190.6 75.3,190.2 77.0,189.8 78.7,189.4 80.4,188.9 82.1,188.5 83.8,188.1 85.4,187.7 87.1,187.2 88.8,186.8 90.5,186.4 92.2,186.0 93.9,185.6 95.6,185.1 97.3,184.7 98.9,184.3 100.6,183.9 102.3,183.4 104.0,183.0 105.7,182.6 107.4,182.2 109.1,181.8 110.8,181.3 112.4,180.9 114.1,180.5 115.8,180.1 117.5,179.6 119.2,179.2 120.9,178.8 122.6,178.4 124.3,178.0 125.9,177.5 127.6,177.1 129.3,176.7 131.0,176.3 132.7,175.9 134.4,175.4 136.1,175.0 137.8,174.6 139.4,174.2 141.1,173.7 142.8,173.3 144.5,172.9 146.2,172.5 147.9,172.1 149.6,171.6 151.3,171.2 152.9,170.8 154.6,170.4 156.3,169.9 158.0,169.5 159.7,169.1 161.4,168.7 163.1,168.3 164.8,167.8 166.4,167.4 168.1,167.0 169.8,166.6 171.5,166.1 173.2,165.7 174.9,165.3 176.6,164.9 178.3,164.5 180.0,164.0 181.6,163.6 183.3,163.2 185.0,162.8 186.7,162.3 188.4,161.9 190.1,161.5 191.8,161.1 193.5,160.7 195.1,160.2 196.8,159.8 198.5,159.4 200.2,159.0 201.9,158.5 203.6,158.1 205.3,157.7 207.0,157.3 208.6,156.9 210.3,156.4 212.0,156.0 213.7,155.6 215.4,155.2 217.1,154.7 218.8,154.3 220.5,153.9 222.1,153.5 223.8,153.1 225.5,152.6 227.2,152.2 228.9,151.8 230.6,151.4 232.3,150.9 234.0,150.5 235.6,150.1 237.3,149.7 239.0,149.3 240.7,148.8 242.4,148.4 244.1,148.0 245.8,147.6 247.5,147.2 249.1,146.7 250.8,146.3 252.5,145.9 254.2,145.5 255.9,145.0 257.6,144.6 259.3,144.2 261.0,143.8 262.6,143.4 264.3,142.9 266.0,142.5 267.7,142.1 269.4,141.7 271.1,141.2 272.8,140.8 274.5,140.4 276.1,140.0 277.8,139.6 279.5,139.1 281.2,138.7 282.9,138.3 284.6,137.9 286.3,137.4 288.0,137.0 289.6,136.6 291.3,136.2 293.0,135.8 294.7,135.3 296.4,134.9 298.1,134.5 299.8,134.1 301.5,133.6 303.2,133.2 304.8,132.8 306.5,132.4 308.2,132.0 309.9,131.5 311.6,131.1 313.3,130.7 315.0,130.3 316.7,129.8 318.3,129.4 320.0,129.0 321.7,128.6 323.4,128.2 325.1,127.7 326.8,127.3 328.5,126.9 330.2,126.5 331.8,126.0 333.5,125.6 335.2,125.2 336.9,124.8 338.6,124.4 340.3,123.9 342.0,123.5 343.7,123.1 345.3,122.7 347.0,122.3 348.7,121.8 350.4,121.4 352.1,121.0 353.8,120.6 355.5,120.1 357.2,119.7 358.8,119.3 360.5,118.9 362.2,118.5 363.9,118.0 365.6,117.6 367.3,117.2 369.0,116.8 370.7,116.3 372.3,115.9 374.0,115.5 375.7,115.1 377.4,114.7 379.1,114.2 380.8,113.8 382.5,113.4 384.2,113.0 385.8,112.5 387.5,112.1 389.2,111.7 390.9,111.3 392.6,110.9 394.3,110.4 396.0,110.0 397.7,109.6 399.3,109.2 401.0,108.7 402.7,108.3 404.4,107.9 406.1,107.5 407.8,107.1 409.5,106.6 411.2,106.2 412.8,105.8 414.5,105.4 416.2,104.9 417.9,104.5 419.6,104.1 421.3,103.7 423.0,103.3 424.7,102.8 426.4,102.4 428.0,102.0 429.7,101.6 431.4,101.1 433.1,100.7 434.8,100.3 436.5,99.9 438.2,99.5 439.9,99.0 441.5,98.6 443.2,98.2 444.9,97.8 446.6,97.3 448.3,96.9 450.0,96.5 451.7,96.1 453.4,95.7 455.0,95.2 456.7,94.8 458.4,94.4 460.1,94.0 461.8,93.6 463.5,93.1 465.2,92.7 466.9,92.3 468.5,91.9 470.2,91.4 471.9,91.0 473.6,90.6 475.3,90.2 477.0,89.8 478.7,89.3 480.4,88.9 482.0,88.5 483.7,88.1 485.4,87.6 487.1,87.2 488.8,86.8 490.5,86.4 492.2,86.0 493.9,85.5 495.5,85.1 497.2,84.7 498.9,84.3 500.6,83.8 502.3,83.4 504.0,83.0 505.7,82.6 507.4,82.2 509.0,81.7 510.7,81.3 512.4,80.9 514.1,80.5 515.8,80.0 517.5,79.6 519.2,79.2 520.9,78.8 522.5,78.4 524.2,77.9 525.9,77.5 527.6,77.1 529.3,76.7 531.0,76.2 532.7,75.8 534.4,75.4 536.0,75.0 537.7,74.6 539.4,74.1 541.1,73.7 542.8,73.3 544.5,72.9 546.2,72.4 547.9,72.0 549.6,71.6 551.2,71.2 552.9,70.8 554.6,70.3 556.3,69.9 558.0,69.5 559.7,69.1 561.4,68.7 563.1,68.2 564.7,67.8 566.4,67.4 568.1,67.0 569.8,66.5 571.5,66.1 573.2,65.7 574.9,65.3 576.6,64.9 578.2,64.4 579.9,64.0 581.6,63.6 583.3,63.2 585.0,62.7 586.7,62.3 588.4,61.9 590.1,61.5 591.7,61.1 593.4,60.6 595.1,60.2 596.8,59.8 598.5,59.4 600.2,58.9 601.9,58.5 603.6,58.1 605.2,57.7 606.9,57.3 608.6,56.8 610.3,56.4 612.0,56.0 613.7,55.6 615.4,55.1 617.1,54.7 618.7,54.3 620.4,53.9 622.1,53.5 623.8,53.0 625.5,52.6 627.2,52.2 628.9,51.8 630.6,51.3 632.2,50.9 633.9,50.5 635.6,50.1 637.3,49.7 639.0,49.2 640.7,48.8 642.4,48.4 644.1,48.0 645.7,47.5 647.4,47.1 649.1,46.7 650.8,46.3 652.5,45.9 654.2,45.4 655.9,45.0 657.6,44.6 659.2,44.2 660.9,43.7 662.6,43.3 664.3,42.9 666.0,42.5"/><polyline class="curve" style="stroke-width:2.2" points="50.0,209.9 51.7,209.4 53.4,208.8 55.1,208.3 56.8,207.7 58.4,207.1 60.1,206.6 61.8,206.0 63.5,205.4 65.2,204.9 66.9,204.3 68.6,203.7 70.3,203.2 71.9,202.6 73.6,202.1 75.3,201.5 77.0,200.9 78.7,200.4 80.4,199.8 82.1,199.2 83.8,198.7 85.4,198.1 87.1,197.6 88.8,197.0 90.5,196.4 92.2,195.9 93.9,195.3 95.6,194.7 97.3,194.2 98.9,193.6 100.6,193.0 102.3,192.5 104.0,191.9 105.7,191.4 107.4,190.8 109.1,190.2 110.8,189.7 112.4,189.1 114.1,188.5 115.8,188.0 117.5,187.4 119.2,186.8 120.9,186.3 122.6,185.7 124.3,185.2 125.9,184.6 127.6,184.0 129.3,183.5 131.0,182.9 132.7,182.3 134.4,181.8 136.1,181.2 137.8,180.7 139.4,180.1 141.1,179.5 142.8,179.0 144.5,178.4 146.2,177.8 147.9,177.3 149.6,176.7 151.3,176.1 152.9,175.6 154.6,175.0 156.3,174.5 158.0,173.9 159.7,173.3 161.4,172.8 163.1,172.2 164.8,171.6 166.4,171.1 168.1,170.5 169.8,169.9 171.5,169.4 173.2,168.8 174.9,168.3 176.6,167.7 178.3,167.1 180.0,166.6 181.6,166.0 183.3,165.4 185.0,164.9 186.7,164.3 188.4,163.8 190.1,163.2 191.8,162.6 193.5,162.1 195.1,161.5 196.8,160.9 198.5,160.4 200.2,159.8 201.9,159.2 203.6,158.7 205.3,158.1 207.0,157.6 208.6,157.0 210.3,156.4 212.0,155.9 213.7,155.3 215.4,154.7 217.1,154.2 218.8,153.6 220.5,153.0 222.1,152.5 223.8,151.9 225.5,151.4 227.2,150.8 228.9,150.2 230.6,149.7 232.3,149.1 234.0,148.5 235.6,148.0 237.3,147.4 239.0,146.9 240.7,146.3 242.4,145.7 244.1,145.2 245.8,144.6 247.5,144.0 249.1,143.5 250.8,142.9 252.5,142.3 254.2,141.8 255.9,141.2 257.6,140.7 259.3,140.1 261.0,139.5 262.6,139.0 264.3,138.4 266.0,137.8 267.7,137.3 269.4,136.7 271.1,136.1 272.8,135.6 274.5,135.0 276.1,134.5 277.8,133.9 279.5,133.3 281.2,132.8 282.9,132.2 284.6,131.6 286.3,131.1 288.0,130.5 289.6,130.0 291.3,129.4 293.0,128.8 294.7,128.3 296.4,127.7 298.1,127.1 299.8,126.6 301.5,126.0 303.2,125.4 304.8,124.9 306.5,124.3 308.2,123.8 309.9,123.2 311.6,122.6 313.3,122.1 315.0,121.5 316.7,120.9 318.3,120.4 320.0,119.8 321.7,119.2 323.4,118.7 325.1,118.1 326.8,117.6 328.5,117.0 330.2,116.4 331.8,115.9 333.5,115.3 335.2,114.7 336.9,114.2 338.6,113.6 340.3,113.1 342.0,112.5 343.7,111.9 345.3,111.4 347.0,110.8 348.7,110.2 350.4,109.7 352.1,109.1 353.8,108.5 355.5,108.0 357.2,107.4 358.8,106.9 360.5,106.3 362.2,105.7 363.9,105.2 365.6,104.6 367.3,104.0 369.0,103.5 370.7,102.9 372.3,102.4 374.0,101.8 375.7,101.2 377.4,100.7 379.1,100.1 380.8,99.5 382.5,99.0"/><polyline class="curve" style="stroke-width:2.2" points="384.2,98.1 385.8,97.9 387.5,97.6 389.2,97.4 390.9,97.1 392.6,96.9 394.3,96.7 396.0,96.4 397.7,96.2 399.3,96.0 401.0,95.7 402.7,95.5 404.4,95.3 406.1,95.0 407.8,94.8 409.5,94.5 411.2,94.3 412.8,94.1 414.5,93.8 416.2,93.6 417.9,93.4 419.6,93.1 421.3,92.9 423.0,92.6 424.7,92.4 426.4,92.2 428.0,91.9 429.7,91.7 431.4,91.5 433.1,91.2 434.8,91.0 436.5,90.8 438.2,90.5 439.9,90.3 441.5,90.0 443.2,89.8 444.9,89.6 446.6,89.3 448.3,89.1 450.0,88.9 451.7,88.6 453.4,88.4 455.0,88.1 456.7,87.9 458.4,87.7 460.1,87.4 461.8,87.2 463.5,87.0 465.2,86.7 466.9,86.5 468.5,86.3 470.2,86.0 471.9,85.8 473.6,85.5 475.3,85.3 477.0,85.1 478.7,84.8 480.4,84.6 482.0,84.4 483.7,84.1 485.4,83.9 487.1,83.6 488.8,83.4 490.5,83.2 492.2,82.9 493.9,82.7 495.5,82.5 497.2,82.2 498.9,82.0 500.6,81.8 502.3,81.5 504.0,81.3 505.7,81.0 507.4,80.8 509.0,80.6 510.7,80.3 512.4,80.1 514.1,79.9 515.8,79.6 517.5,79.4 519.2,79.1 520.9,78.9 522.5,78.7 524.2,78.4 525.9,78.2 527.6,78.0 529.3,77.7 531.0,77.5 532.7,77.3 534.4,77.0 536.0,76.8 537.7,76.5 539.4,76.3 541.1,76.1 542.8,75.8 544.5,75.6 546.2,75.4 547.9,75.1 549.6,74.9 551.2,74.6 552.9,74.4 554.6,74.2 556.3,73.9 558.0,73.7 559.7,73.5 561.4,73.2 563.1,73.0 564.7,72.8 566.4,72.5 568.1,72.3 569.8,72.0 571.5,71.8 573.2,71.6 574.9,71.3 576.6,71.1 578.2,70.9 579.9,70.6 581.6,70.4 583.3,70.1 585.0,69.9 586.7,69.7 588.4,69.4 590.1,69.2 591.7,69.0 593.4,68.7 595.1,68.5 596.8,68.3 598.5,68.0 600.2,67.8 601.9,67.5 603.6,67.3 605.2,67.1 606.9,66.8 608.6,66.6 610.3,66.4 612.0,66.1 613.7,65.9 615.4,65.6 617.1,65.4 618.7,65.2 620.4,64.9 622.1,64.7 623.8,64.5 625.5,64.2 627.2,64.0 628.9,63.8 630.6,63.5 632.2,63.3 633.9,63.0 635.6,62.8 637.3,62.6 639.0,62.3 640.7,62.1 642.4,61.9 644.1,61.6 645.7,61.4 647.4,61.1 649.1,60.9 650.8,60.7 652.5,60.4 654.2,60.2 655.9,60.0 657.6,59.7 659.2,59.5 660.9,59.3 662.6,59.0 664.3,58.8 666.0,58.5"/><line class="curve3" stroke-dasharray="4 4" x1="384.2" y1="30" x2="384.2" y2="230"/><line class="curve3" x1="60" y1="38" x2="78" y2="38"/><text class="ink" x="84" y="42" font-size="11">abone</text><line class="curve2" x1="141" y1="38" x2="159" y2="38"/><text class="ink" x="165" y="42" font-size="11">tek doğru</text><line class="curve" x1="250" y1="38" x2="268" y2="38"/><text class="ink" x="274" y="42" font-size="11">iki parçalı doğru</text></svg>
  <figcaption>Turuncu kesik çizgi tek doğru: başta ve sonda serinin üstünde, ortada altında kalıyor. Mor, 17 Temmuz'da kırılan iki parçalı doğru: eğim 12'den 5'e iniyor.</figcaption>
</figure>

Aynı arama, bu kez ortalama yerine **doğru** ile: her olası kesim için iki
parçaya ayrı birer doğru uydur, kalıntı kareleri toplamı en küçük olanı seç.

| | Eğim (abone/gün) |
|---|---|
| Tek doğru | 8.98 |
| 17 Temmuz öncesi | 11.99 |
| 17 Temmuz sonrası | 5.04 |

Tek doğrunun eğimi iki dönemin de eğimi değil; **hiçbir dönemi anlatmıyor**.
İpucu kalıntıda: tek doğrunun kalıntısı rastgele dağılmıyor, uçlarda eksi
(−284, −356), ortada artı (+332, tam 17 Temmuz'da). Ters V şeklindeki kalıntı,
eğim değişiminin imzasıdır.

Tahmine etkisi: 30 gün sonrası için tek doğru 4832, son 60 güne uydurulan doğru
4373 diyor. Büyüme aynı hızda sürerse beklenen 4368.

## 9. Oynaklık değişimi

Pompa serisinin son haftasına dön. Kısım 2'deki dedektör (eşik 4) haftalara
göre kaç alarm veriyor?

| Hafta | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Alarm | 3 | 2 | 3 | 1 | 9 | **15** |

Beşinci haftadaki dokuz alarmın sekizi takılı sensör. Altıncı haftada 15 alarm
var ve defterde **hiç olay yok**. Ortalama yerinde; değişen gürültünün boyu.
72 saatlik pencerede kalıntının dayanıklı standart sapması (1.4826 × MAD):

```python
def robust_sd(x):
    return 1.4826 * np.median(np.abs(x - np.median(x)))


hours = pressure.index.hour
resid_all = pressure - profile.reindex(hours).to_numpy()
spread = resid_all.rolling(72).apply(robust_sd, raw=True)
```

İlk beş haftada 0.06 ile 0.09 arasında; 7 Ekim'den sonraki üç gün içinde
0.20'nin üstüne çıkıyor. Pompada bir şey gevşemiş.

Alarm sayısının **birden artması** kendisi bir işarettir: ya oynaklık değişti
ya da beklenti artık geçersiz. Eşiği yükseltip alarmları susturmak değil,
nedenini bulmak gerekir; sonra ölçek yeniden hesaplanır.

## 10. Eşik: yanlış alarm ile kaçan olay

Eşik düşükse her şey alarm, yüksekse gerçek olaylar kaçar. İki ölçü:

- **Kesinlik** (precision): alarmların ne kadarı gerçek olay?
- **Duyarlılık** (recall): gerçek olayların ne kadarı yakalandı?

Pompa serisinde defterdeki 12 olaya karşı (takılı sensör saatleri ayrı
tutuldu):

| Eşik | Alarm | Doğru | Kesinlik | Duyarlılık |
|---|---|---|---|---|
| 2 | 38 | 12 | 0.32 | 1.00 |
| 2.5 | 16 | 12 | 0.75 | 1.00 |
| 3 | 12 | 12 | **1.00** | **1.00** |
| 4 | 10 | 10 | 1.00 | 0.83 |
| 6 | 8 | 8 | 1.00 | 0.67 |

Burada 3 kusursuz; gerçek hayatta böyle temiz bir nokta nadiren bulunur ve
seçim **maliyete** göre yapılır (Bölüm 20'deki stok kararı gibi): kaçan bir
arıza pahalıysa düşük eşik, her alarm bir teknisyeni yola çıkarıyorsa yüksek.

Sık gözlem, çok alarm demek. Kusursuz normal dağılan bir kalıntıda bile:

| Eşik | Saatlik veride yılda beklenen yanlış alarm |
|---|---|
| 2 | 399 |
| 3 | 24 |
| 4 | 0.6 |

Günde bir yanlış alarm veren sisteme kimse bakmaz (**alarm yorgunluğu**).
Etiketli olay yoksa da eşiği sına: geçmişe uygula, kaç alarm verdiğine ve
bunların neye denk geldiğine bak.

## 11. Değişimden sonra tahmin

Değişim noktası tahmin için kötü haber: geçmişin bir kısmı artık geleceği
anlatmıyor. Kasım–Aralık web trafiğini haftanın günü ortalamasıyla tahmin et:

| Eğitim verisi | MAE | Yanlılık |
|---|---|---|
| 31 Ekim'e kadar bütün geçmiş (302 gün) | 917.7 | +917.7 |
| Yalnızca 2 Eylül'den sonrası (59 gün) | **213.4** | +19.4 |

Beş kat daha az veriyle dört kat daha iyi tahmin. **Daha çok veri her zaman
daha iyi değildir**; ilgili veri daha iyidir.

Seçenekler:

| Yol | Ne zaman |
|---|---|
| Değişimden sonrasıyla eğit | Sonrasında yeterli veri varsa |
| Basamak değişkeni ekle (Bölüm 18): değişimden önce 0, sonra 1 | Mevsimi öğrenmek için eski veri de gerekiyorsa |
| Son değerlere ağırlık veren yöntem (üstel düzleştirme, fark alan ARIMA) | Değişimler sık ve habersizse |
| Eski dönemi yeni düzeye ölçekle | Desen aynı, yalnızca düzey değiştiyse |

Anomaliler için kural tersine: eğitimden önce **onarılır** (Bölüm 13), çünkü
tekrar etmeyecekler. Değişim noktası ise onarılmaz: o artık serinin kendisi.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Ham seriye tek eşik | Mevsim tepesi alarm, bağlamsal anomali kaçar | Bekleneni çıkar, kalıntıya bak |
| Ölçeği standart sapmayla kurmak | Anomaliler ölçeği şişirir, birbirini gizler | Ortanca ve MAD |
| Beklentiyi ortalamayla kurmak | Her anomalinin yankısı yanlış alarm olur | Ortanca |
| Canlı dedektörü gelecekle sınamak | Gerçekte olmayan bir başarı | Yalnızca geçmiş: `shift` |
| Düzey kaymasını anomali diye onarmak | Yeni düzey silinir, tahmin eskiye döner | Değişim noktası olarak kaydet |
| Değişimden sonra eski veriyle eğitmek | Yanlı tahmin | Sonrasıyla eğit ya da basamak değişkeni |
| `best_split` sonucunu sorgusuz kabul etmek | Olmayan değişim "bulunur" | Kazanca bak |
| Alarm çoğalınca eşiği yükseltmek | Gerçek değişim gizlenir | Önce nedenini bul |
| Yalnızca uç değere bakmak | Takılı sensör görülmez | Tekrar uzunluğu, pencere ölçüleri |

## Özet

- **Anomali** geçicidir, **değişim noktası** kalıcıdır; tepkileri farklıdır.
- Anomali **beklenenden sapmadır**: gözlem → beklenen → kalıntı → dayanıklı
  ölçek → puan → eşik.
- **Bağlamsal** anomali ham değerde görünmez; **toplu** anomali tek gözlemde
  görünmez.
- Canlı izlemede yalnızca **geçmiş** kullanılır; beklenti **ortancayla** kurulur.
- Aynı yönde art arda alarmlar düzey kaymasıdır. **CUSUM** küçük, kalıcı
  kaymaları biriktirerek yakalar.
- Geriye dönük: **en iyi kesim** ve kazancı. Önce mevsimi ve anomalileri çıkar.
- Eğim ve oynaklık da değişebilir: parçalı doğru, pencere ölçeği.
- Eşik bir ödünleşimdir: **kesinlik** ile **duyarlılık**.
- Değişimden sonra model yeniden kurulur: ilgili veri, çok veriden iyidir.

Patikanın konuları burada bitiyor. Son bölüm, baştan sona bütün araçları tek
bir işte bir araya getiren genel tekrar.
