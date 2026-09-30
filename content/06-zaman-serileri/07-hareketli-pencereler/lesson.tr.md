# Hareketli Pencereler

Günlük satış grafiğinde trendi görmek zor: her hafta aynı zikzak çizgiyi
kaplıyor. Bölüm 05'te bunu haftalığa toplayarak çözdün, ama bedeli vardı:
1096 gün 156 haftaya indi.

Hareketli pencere aynı sakinliği **satır kaybetmeden** veriyor. Her gün için
"son 7 günün ortalaması" hesaplanıyor; pencere bir gün kayıyor, hesap
tekrarlanıyor. Sonuç yine günlük bir seri, ama pürüzsüz.

## Hareketli ortalama

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

ma7 = s.rolling(7).mean()
print(ma7.head(8).round(1).tolist())
# [nan, nan, nan, nan, nan, nan, 230.1, 229.3]
```

`rolling(7)` her satır için **o satır ve önceki 6 satırdan** oluşan bir
pencere kuruyor; `.mean()` pencerenin ortalamasını alıyor. Yazım yine
`resample` ve `groupby` ile aynı kalıpta: önce pencere, sonra işlem.

İlk altı satır boş, çünkü yedi değer birikmeden pencere dolmuyor.

```python
print(round(ma7.loc["2024-03-10"], 1))                       # 282.6
print(round(s.loc["2024-03-04":"2024-03-10"].mean(), 1))     # 282.6
```

10 Mart pazar günündeki değer, o gün biten haftanın ortalaması. Haftalık
`resample` bu sayıyı yalnızca pazar günleri veriyordu; hareketli ortalama her
gün için veriyor.

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="206.6" x2="666" y2="206.6"/><text class="dim" x="38" y="210.1" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="146.7" x2="666" y2="146.7"/><text class="dim" x="38" y="150.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="86.7" x2="666" y2="86.7"/><text class="dim" x="38" y="90.2" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="26.8" x2="666" y2="26.8"/><text class="dim" x="38" y="30.3" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="199.1" y1="220" x2="199.1" y2="224"/><text class="dim" x="199.1" y="236" font-size="10.5" text-anchor="middle">Nis</text><line class="line" x1="354.1" y1="220" x2="354.1" y2="224"/><text class="dim" x="354.1" y="236" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="510.9" y1="220" x2="510.9" y2="224"/><text class="dim" x="510.9" y="236" font-size="10.5" text-anchor="middle">Eki</text><polyline class="curve3" style="stroke-width:1.0" points="44.0,167.6 45.7,176.0 47.4,174.8 49.1,164.6 50.8,126.9 52.5,89.1 54.2,121.5 55.9,184.4 57.6,176.6 59.3,167.6 61.0,155.6 62.7,137.7 64.4,84.9 66.2,122.7 67.9,168.8 69.6,183.2 71.3,164.0 73.0,162.2 74.7,149.1 76.4,89.7 78.1,125.7 79.8,170.6 81.5,182.0 83.2,169.4 84.9,158.0 86.6,147.3 88.3,97.5 90.0,119.1 91.7,183.8 93.4,179.6 95.1,164.0 96.8,143.1 98.5,141.9 100.2,93.3 101.9,128.1 103.6,168.8 105.3,179.6 107.1,169.4 108.8,154.4 110.5,145.5 112.2,93.9 113.9,126.9 115.6,191.6 117.3,180.8 119.0,171.8 120.7,167.0 122.4,134.1 124.1,101.7 125.8,125.7 127.5,177.8 129.2,164.0 130.9,168.8 132.6,170.0 134.3,131.1 136.0,100.5 137.7,126.9 139.4,190.4 141.1,181.4 142.8,173.0 144.5,176.6 146.2,145.5 148.0,103.5 149.7,135.3 151.4,174.2 153.1,169.4 154.8,185.0 156.5,180.8 158.2,153.8 159.9,96.3 161.6,140.1 163.3,186.8 165.0,173.0 166.7,172.4 168.4,162.8 170.1,146.1 171.8,92.7 173.5,137.1 175.2,194.6 176.9,182.6 178.6,159.8 180.3,160.4 182.0,150.3 183.7,120.3 185.4,135.3 187.1,184.4 188.8,180.8 190.6,180.8 192.3,179.0 194.0,153.8 195.7,108.9 197.4,128.7 199.1,182.0 200.8,187.4 202.5,182.6 204.2,165.8 205.9,144.3 207.6,110.7 209.3,154.4 211.0,199.4 212.7,182.6 214.4,175.4 216.1,171.8 217.8,152.6 219.5,116.1 221.2,138.9 222.9,201.2 224.6,193.4 226.3,180.2 228.0,178.4 229.7,155.6 231.5,117.9 233.2,140.7 234.9,196.4 236.6,197.0 238.3,183.2 240.0,189.2 241.7,157.4 243.4,128.7 245.1,137.1 246.8,177.8 248.5,198.8 250.2,180.2 251.9,182.0 253.6,161.6 255.3,123.9 257.0,143.1 258.7,190.4 260.4,196.4 262.1,191.6 263.8,172.4 265.5,149.1 267.2,128.7 268.9,148.5 270.6,188.6 272.4,178.4 274.1,186.2 275.8,177.2 277.5,165.2 279.2,116.1 280.9,143.7 282.6,198.2 284.3,192.8 286.0,173.6 287.7,170.6 289.4,149.7 291.1,129.3 292.8,155.6 294.5,206.6 296.2,189.2 297.9,196.4 299.6,188.0 301.3,152.0 303.0,135.9 304.7,144.3 306.4,204.2 308.1,192.8 309.8,173.0 311.5,179.0 313.2,161.6 315.0,125.1 316.7,149.7 318.4,200.0 320.1,204.2 321.8,194.6 323.5,171.8 325.2,151.4 326.9,119.1 328.6,147.9 330.3,191.6 332.0,191.0 333.7,184.4 335.4,170.6 337.1,150.9 338.8,125.1 340.5,152.6 342.2,209.0 343.9,197.0 345.6,188.6 347.3,180.8 349.0,158.6 350.7,119.1 352.4,139.5 354.1,204.8 355.9,198.2 357.6,193.4 359.3,174.8 361.0,145.5 362.7,119.1 364.4,141.9 366.1,197.6 367.8,197.0 369.5,190.4 371.2,167.6 372.9,156.8 374.6,120.3 376.3,139.5 378.0,192.2 379.7,182.6 381.4,185.0 383.1,174.8 384.8,151.4 386.5,120.9 388.2,144.3 389.9,187.4 391.6,187.4 393.3,187.4 395.0,175.4 396.8,136.5 398.5,116.1 400.2,144.9 401.9,187.4 403.6,176.0 405.3,183.2 407.0,175.4 408.7,153.8 410.4,121.5 412.1,138.3 413.8,181.4 415.5,182.6 417.2,179.6 418.9,183.2 420.6,151.4 422.3,117.3 424.0,153.2 425.7,191.0 427.4,179.6 429.1,185.0 430.8,175.4 432.5,135.3 434.2,102.9 435.9,124.5 437.6,176.6 439.4,177.2 441.1,176.6 442.8,164.6 444.5,134.7 446.2,102.3 447.9,129.3 449.6,182.0 451.3,173.6 453.0,177.8 454.7,154.4 456.4,135.3 458.1,105.3 459.8,116.1 461.5,192.8 463.2,192.8 464.9,168.2 466.6,168.2 468.3,143.7 470.0,94.5 471.7,117.9 473.4,164.6 475.1,172.4 476.8,174.8 478.5,157.4 480.3,138.9 482.0,98.1 483.7,114.9 485.4,168.8 487.1,185.6 488.8,161.0 490.5,158.0 492.2,130.5 493.9,98.1 495.6,126.3 497.3,178.4 499.0,167.6 500.7,167.0 502.4,159.2 504.1,125.7 505.8,93.9 507.5,129.3 509.2,170.0 510.9,177.2 512.6,162.8 514.3,147.3 516.0,134.7 517.7,89.1 519.4,122.7 521.2,171.8 522.9,172.4 524.6,173.6 526.3,153.8 528.0,120.3 529.7,90.9 531.4,110.1 533.1,174.2 534.8,177.8 536.5,150.9 538.2,147.3 539.9,123.3 541.6,84.3 543.3,120.9 545.0,161.6 546.7,168.2 548.4,146.1 550.1,153.2 551.8,124.5 553.5,77.8 555.2,108.3 556.9,163.4 558.6,162.2 560.3,155.0 562.0,150.3 563.8,110.1 565.5,73.6 567.2,105.9 568.9,163.4 570.6,166.4 572.3,156.8 574.0,143.1 575.7,116.1 577.4,60.4 579.1,102.3 580.8,160.4 582.5,165.2 584.2,144.9 585.9,144.9 587.6,102.9 589.3,81.4 591.0,90.9 592.7,162.8 594.4,158.6 596.1,158.6 597.8,137.7 599.5,106.5 601.2,76.6 602.9,96.9 604.7,165.2 606.4,154.4 608.1,148.5 609.8,148.5 611.5,125.1 613.2,67.6 614.9,90.9 616.6,165.2 618.3,152.6 620.0,141.3 621.7,138.3 623.4,112.5 625.1,57.4 626.8,80.8 628.5,150.3 630.2,136.5 631.9,146.1 633.6,110.1 635.3,93.3 637.0,47.8 638.7,66.4 640.4,146.1 642.1,141.9 643.8,132.9 645.6,134.7 647.3,81.4 649.0,33.4 650.7,68.8 652.4,143.1 654.1,120.3 655.8,122.7 657.5,113.1 659.2,72.4 660.9,25.0 662.6,60.4 664.3,123.3 666.0,118.5"/><polyline class="curve" style="stroke-width:2.2" points="44.0,120.9 45.7,123.7 47.4,128.3 49.1,132.9 50.8,134.8 52.5,140.5 54.2,145.8 55.9,148.2 57.6,148.3 59.3,147.3 61.0,146.0 62.7,147.5 64.4,146.9 66.2,147.1 67.9,144.9 69.6,145.8 71.3,145.3 73.0,146.2 74.7,147.9 76.4,148.5 78.1,149.0 79.8,149.2 81.5,149.1 83.2,149.8 84.9,149.2 86.6,149.0 88.3,150.1 90.0,149.1 91.7,151.0 93.4,150.7 95.1,149.9 96.8,147.8 98.5,147.0 100.2,146.4 101.9,147.7 103.6,145.5 105.3,145.5 107.1,146.3 108.8,147.9 110.5,148.5 112.2,148.5 113.9,148.4 115.6,151.6 117.3,151.8 119.0,152.1 120.7,153.9 122.4,152.3 124.1,153.4 125.8,153.2 127.5,151.3 129.2,148.9 130.9,148.5 132.6,148.9 134.3,148.5 136.0,148.3 137.7,148.5 139.4,150.3 141.1,152.7 142.8,153.3 144.5,154.3 146.2,156.3 148.0,156.8 149.7,158.0 151.4,155.6 153.1,153.9 154.8,155.6 156.5,156.2 158.2,157.4 159.9,156.4 161.6,157.1 163.3,158.9 165.0,159.4 166.7,157.6 168.4,155.0 170.1,153.9 171.8,153.4 173.5,153.0 175.2,154.1 176.9,155.5 178.6,153.7 180.3,153.3 182.0,153.9 183.7,157.9 185.4,157.6 187.1,156.2 188.8,155.9 190.6,158.9 192.3,161.5 194.0,162.1 195.7,160.4 197.4,159.5 199.1,159.2 200.8,160.1 202.5,160.4 204.2,158.5 205.9,157.1 207.6,157.4 209.3,161.0 211.0,163.5 212.7,162.8 214.4,161.8 216.1,162.7 217.8,163.9 219.5,164.6 221.2,162.4 222.9,162.7 224.6,164.2 226.3,164.9 228.0,165.8 229.7,166.3 231.5,166.5 233.2,166.8 234.9,166.1 236.6,166.6 238.3,167.0 240.0,168.6 241.7,168.8 243.4,170.4 245.1,169.9 246.8,167.2 248.5,167.5 250.2,167.0 251.9,166.0 253.6,166.6 255.3,165.9 257.0,166.8 258.7,168.6 260.4,168.2 262.1,169.9 263.8,168.5 265.5,166.7 267.2,167.4 268.9,168.1 270.6,167.9 272.4,165.3 274.1,164.5 275.8,165.2 277.5,167.5 279.2,165.7 280.9,165.1 282.6,166.4 284.3,168.5 286.0,166.7 287.7,165.7 289.4,163.5 291.1,165.4 292.8,167.1 294.5,168.3 296.2,167.8 297.9,171.0 299.6,173.5 301.3,173.9 303.0,174.8 304.7,173.2 306.4,172.8 308.1,173.4 309.8,170.0 311.5,168.7 313.2,170.1 315.0,168.6 316.7,169.3 318.4,168.7 320.1,170.4 321.8,173.4 323.5,172.4 325.2,171.0 326.9,170.1 328.6,169.9 330.3,168.7 332.0,166.8 333.7,165.3 335.4,165.1 337.1,165.1 338.8,165.9 340.5,166.6 342.2,169.1 343.9,169.9 345.6,170.5 347.3,172.0 349.0,173.1 350.7,172.2 352.4,170.4 354.1,169.8 355.9,169.9 357.6,170.6 359.3,169.8 361.0,167.9 362.7,167.9 364.4,168.2 366.1,167.2 367.8,167.0 369.5,166.6 371.2,165.6 372.9,167.2 374.6,167.4 376.3,167.0 378.0,166.3 379.7,164.2 381.4,163.4 383.1,164.5 384.8,163.7 386.5,163.8 388.2,164.5 389.9,163.8 391.6,164.5 393.3,164.8 395.0,164.9 396.8,162.7 398.5,162.1 400.2,162.1 401.9,162.1 403.6,160.5 405.3,159.9 407.0,159.9 408.7,162.4 410.4,163.2 412.1,162.2 413.8,161.4 415.5,162.3 417.2,161.8 418.9,162.9 420.6,162.6 422.3,162.0 424.0,164.1 425.7,165.5 427.4,165.1 429.1,165.8 430.8,164.7 432.5,162.4 434.2,160.4 435.9,156.2 437.6,154.2 439.4,153.8 441.1,152.6 442.8,151.1 444.5,151.0 446.2,150.9 447.9,151.6 449.6,152.4 451.3,151.9 453.0,152.0 454.7,150.6 456.4,150.7 458.1,151.1 459.8,149.2 461.5,150.8 463.2,153.5 464.9,152.1 466.6,154.1 468.3,155.3 470.0,153.8 471.7,154.0 473.4,150.0 475.1,147.1 476.8,148.0 478.5,146.5 480.3,145.8 482.0,146.3 483.7,145.9 485.4,146.5 487.1,148.4 488.8,146.4 490.5,146.5 492.2,145.3 493.9,145.3 495.6,146.9 497.3,148.3 499.0,145.7 500.7,146.6 502.4,146.7 504.1,146.1 505.8,145.5 507.5,145.9 509.2,144.7 510.9,146.1 512.6,145.5 514.3,143.7 516.0,145.0 517.7,144.3 519.4,143.4 521.2,143.7 522.9,143.0 524.6,144.5 526.3,145.5 528.0,143.4 529.7,143.7 531.4,141.9 533.1,142.2 534.8,143.0 536.5,139.7 538.2,138.8 539.9,139.2 541.6,138.3 543.3,139.8 545.0,138.0 546.7,136.6 548.4,136.0 550.1,136.8 551.8,137.0 553.5,136.0 555.2,134.2 556.9,134.5 558.6,133.6 560.3,134.9 562.0,134.5 563.8,132.4 565.5,131.8 567.2,131.5 568.9,131.5 570.6,132.1 572.3,132.4 574.0,131.3 575.7,132.2 577.4,130.3 579.1,129.8 580.8,129.4 582.5,129.2 584.2,127.5 585.9,127.7 587.6,125.9 589.3,128.9 591.0,127.2 592.7,127.6 594.4,126.6 596.1,128.6 597.8,127.6 599.5,128.1 601.2,127.4 602.9,128.3 604.7,128.6 606.4,128.0 608.1,126.5 609.8,128.1 611.5,130.7 613.2,129.5 614.9,128.6 616.6,128.6 618.3,128.3 620.0,127.3 621.7,125.9 623.4,124.1 625.1,122.6 626.8,121.2 628.5,119.0 630.2,116.7 631.9,117.4 633.6,113.4 635.3,110.6 637.0,109.3 638.7,107.2 640.4,106.6 642.1,107.4 643.8,105.5 645.6,109.0 647.3,107.3 649.0,105.2 650.7,105.6 652.4,105.1 654.1,102.1 655.8,100.6 657.5,97.5 659.2,96.2 660.9,95.0 662.6,93.8 664.3,91.0 666.0,90.8"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,128.2 45.7,128.4 47.4,128.5 49.1,129.1 50.8,129.3 52.5,130.1 54.2,130.4 55.9,130.9 57.6,131.8 59.3,131.8 61.0,132.0 62.7,133.0 64.4,133.3 66.2,134.7 67.9,134.8 69.6,135.6 71.3,136.1 73.0,136.9 74.7,138.2 76.4,139.1 78.1,140.3 79.8,140.8 81.5,141.7 83.2,142.7 84.9,143.6 86.6,144.8 88.3,146.5 90.0,147.7 91.7,148.3 93.4,148.5 95.1,148.1 96.8,147.3 98.5,147.8 100.2,148.0 101.9,148.2 103.6,147.7 105.3,147.8 107.1,147.8 108.8,147.8 110.5,148.1 112.2,148.4 113.9,148.5 115.6,149.4 117.3,149.3 119.0,149.5 120.7,149.7 122.4,149.2 124.1,149.6 125.8,149.6 127.5,149.9 129.2,149.2 130.9,149.2 132.6,149.6 134.3,149.1 136.0,149.2 137.7,149.4 139.4,149.7 141.1,149.7 142.8,150.1 144.5,151.3 146.2,151.4 148.0,151.7 149.7,152.0 151.4,152.2 153.1,151.8 154.8,152.4 156.5,153.3 158.2,153.6 159.9,153.7 161.6,154.2 163.3,154.0 165.0,153.7 166.7,153.8 168.4,153.6 170.1,154.0 171.8,153.7 173.5,154.1 175.2,154.7 176.9,155.4 178.6,155.1 180.3,154.7 182.0,155.4 183.7,156.1 185.4,156.4 187.1,156.2 188.8,156.2 190.6,156.5 192.3,156.5 194.0,156.8 195.7,157.0 197.4,156.8 199.1,157.1 200.8,157.7 202.5,157.6 204.2,157.1 205.9,156.8 207.6,157.3 209.3,157.8 211.0,158.2 212.7,158.6 214.4,158.7 216.1,159.0 217.8,159.2 219.5,160.1 221.2,160.1 222.9,160.4 224.6,160.8 226.3,161.5 228.0,162.1 229.7,162.3 231.5,162.2 233.2,162.4 234.9,162.9 236.6,163.4 238.3,163.5 240.0,163.9 241.7,164.0 243.4,164.7 245.1,165.0 246.8,164.9 248.5,165.3 250.2,165.2 251.9,165.8 253.6,166.4 255.3,166.9 257.0,166.4 258.7,166.1 260.4,166.6 262.1,167.2 263.8,167.2 265.5,167.1 267.2,167.5 268.9,167.9 270.6,167.4 272.4,166.9 274.1,167.1 275.8,167.1 277.5,167.4 279.2,167.3 280.9,167.5 282.6,167.5 284.3,167.4 286.0,167.0 287.7,166.4 289.4,166.1 291.1,166.1 292.8,166.8 294.5,167.8 296.2,167.5 297.9,168.0 299.6,168.2 301.3,167.9 303.0,168.3 304.7,168.4 306.4,168.9 308.1,168.7 309.8,168.1 311.5,168.3 313.2,168.8 315.0,168.6 316.7,168.7 318.4,169.1 320.1,170.0 321.8,170.3 323.5,170.1 325.2,169.6 326.9,169.7 328.6,169.9 330.3,169.6 332.0,169.6 333.7,170.0 335.4,170.0 337.1,170.0 338.8,169.9 340.5,169.7 342.2,169.8 343.9,170.1 345.6,169.8 347.3,169.6 349.0,169.8 350.7,169.2 352.4,169.0 354.1,169.1 355.9,169.3 357.6,170.0 359.3,169.8 361.0,169.3 362.7,169.0 364.4,168.8 366.1,168.7 367.8,168.4 369.5,168.3 371.2,168.1 372.9,168.3 374.6,168.4 376.3,168.1 378.0,168.1 379.7,167.8 381.4,167.8 383.1,167.9 384.8,168.0 386.5,167.8 388.2,167.5 389.9,166.7 391.6,166.4 393.3,166.4 395.0,166.2 396.8,165.4 398.5,165.3 400.2,165.5 401.9,164.8 403.6,164.1 405.3,163.7 407.0,163.7 408.7,164.0 410.4,164.1 412.1,164.0 413.8,163.4 415.5,162.9 417.2,162.5 418.9,163.0 420.6,162.9 422.3,162.7 424.0,163.2 425.7,163.2 427.4,163.1 429.1,163.1 430.8,163.1 432.5,162.5 434.2,161.9 435.9,161.2 437.6,160.8 439.4,160.4 441.1,160.1 442.8,159.7 444.5,159.6 446.2,159.1 447.9,158.6 449.6,158.4 451.3,158.3 453.0,158.1 454.7,157.3 456.4,156.7 458.1,156.1 459.8,155.3 461.5,155.7 463.2,156.1 464.9,155.7 466.6,155.1 468.3,154.9 470.0,154.0 471.7,152.8 473.4,151.8 475.1,151.6 476.8,151.2 478.5,150.6 480.3,150.7 482.0,150.5 483.7,150.2 485.4,149.9 487.1,150.2 488.8,149.7 490.5,149.4 492.2,149.3 493.9,149.1 495.6,149.0 497.3,148.9 499.0,148.7 500.7,148.3 502.4,148.5 504.1,148.1 505.8,147.7 507.5,148.2 509.2,147.4 510.9,146.8 512.6,146.6 514.3,145.9 516.0,145.5 517.7,145.4 519.4,145.5 521.2,145.8 522.9,145.8 524.6,145.7 526.3,145.6 528.0,144.9 529.7,144.7 531.4,144.5 533.1,144.7 534.8,144.4 536.5,144.1 538.2,143.7 539.9,143.4 541.6,142.9 543.3,142.7 545.0,142.1 546.7,142.2 548.4,141.4 550.1,141.2 551.8,141.2 553.5,140.6 555.2,139.8 556.9,139.6 558.6,139.1 560.3,138.8 562.0,138.9 563.8,138.0 565.5,137.5 567.2,136.9 568.9,136.6 570.6,136.3 572.3,135.7 574.0,135.4 575.7,135.2 577.4,134.1 579.1,133.8 580.8,133.3 582.5,132.9 584.2,132.7 585.9,132.6 587.6,131.9 589.3,131.8 591.0,130.7 592.7,130.7 594.4,130.4 596.1,130.8 597.8,130.3 599.5,129.6 601.2,129.6 602.9,129.2 604.7,129.3 606.4,129.0 608.1,128.7 609.8,128.7 611.5,129.2 613.2,129.0 614.9,128.5 616.6,128.5 618.3,128.0 620.0,127.5 621.7,127.3 623.4,127.2 625.1,127.1 626.8,126.3 628.5,125.9 630.2,124.9 631.9,125.0 633.6,123.7 635.3,123.4 637.0,122.2 638.7,121.3 640.4,120.7 642.1,120.1 643.8,119.2 645.6,119.1 647.3,118.2 649.0,116.6 650.7,115.6 652.4,114.8 654.1,113.6 655.8,112.7 657.5,111.4 659.2,109.6 660.9,108.0 662.6,106.9 664.3,105.4 666.0,104.2"/><line class="curve3" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">günlük</text><line class="curve" x1="142" y1="22" x2="160" y2="22"/><text class="ink" x="166" y="26" font-size="11">7 günlük ortalama</text><line class="curve2" x1="307" y1="22" x2="325" y2="22"/><text class="ink" x="331" y="26" font-size="11">28 günlük ortalama</text></svg>
  <figcaption>2024. Gri: günlük satış. Mor: 7 günlük hareketli ortalama, haftalık zikzak gitmiş. Turuncu: 28 günlük ortalama, daha da düz ama yıl sonu yükselişini daha geç gösteriyor.</figcaption>
</figure>

Pencere büyüdükçe seri sakinleşiyor:

```python
print(round(s.std(), 1))                        # 58.9   ham
print(round(s.rolling(7).mean().std(), 1))      # 39.1
print(round(s.rolling(28).mean().std(), 1))     # 37.0
print(round(s.rolling(365).mean().std(), 1))    # 19.7
```

## Pencere boyu nasıl seçilir?

**Pencere, bastırmak istediğin mevsimin uzunluğu kadar olmalı.** 7 günlük
pencerede her zaman tam bir pazartesi, bir salı, ..., bir pazar var; haftanın
deseni pencerenin içinde birbirini götürüyor.

Pencere mevsime uymazsa (örneğin 5 gün) içine bazen iki hafta sonu, bazen bir
hafta sonu giriyor ve ortalama yine dalgalanıyor.

365 günlük pencere hem haftayı hem yılı bastırıyor; geriye **trend** kalıyor:

```python
trend = s.rolling(365).mean()

print(round(trend.loc["2022-12-31"], 1))     # 225.5
print(round(trend.loc["2023-12-31"], 1))     # 260.4
print(round(trend.loc["2024-12-31"], 1))     # 294.1
```

Yıl sonlarındaki değerler, Bölüm 00'da bulduğun yıllık ortalamalar. Bedeli:
ilk 364 gün `NaN`.

## Geriye dönük ve ortalanmış pencere

`rolling(28)` varsayılan olarak **geriye** bakıyor: bugün ve önceki 27 gün.
`center=True` pencereyi bugünün **iki yanına** yerleştiriyor:

```python
trailing = s.rolling(28).mean()
centered = s.rolling(28, center=True).mean()

window = slice("2023-11-15", "2024-02-15")
print(trailing.loc[window].idxmax().date())     # 2024-01-01
print(centered.loc[window].idxmax().date())     # 2023-12-19
```

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="215.3" x2="666" y2="215.3"/><text class="dim" x="38" y="218.8" font-size="10.5" text-anchor="end">280</text><line class="grid" x1="44" y1="145.0" x2="666" y2="145.0"/><text class="dim" x="38" y="148.5" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="74.7" x2="666" y2="74.7"/><text class="dim" x="38" y="78.2" font-size="10.5" text-anchor="end">320</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="152.2" y1="220" x2="152.2" y2="224"/><text class="dim" x="152.2" y="236" font-size="10.5" text-anchor="middle">1 Ara</text><line class="line" x1="361.8" y1="220" x2="361.8" y2="224"/><text class="dim" x="361.8" y="236" font-size="10.5" text-anchor="middle">1 Oca</text><line class="line" x1="571.3" y1="220" x2="571.3" y2="224"/><text class="dim" x="571.3" y="236" font-size="10.5" text-anchor="middle">1 Şub</text><line class="curve3" stroke-dasharray="4 4" x1="273.9" y1="14" x2="273.9" y2="220"/><line class="curve3" stroke-dasharray="4 4" x1="361.8" y1="14" x2="361.8" y2="220"/><polyline class="curve" style="stroke-width:2.4" points="44.0,181.4 50.8,178.6 57.5,175.0 64.3,175.6 71.0,172.9 77.8,169.3 84.6,170.4 91.3,167.3 98.1,166.5 104.8,166.1 111.6,161.8 118.4,154.3 125.1,150.8 131.9,149.8 138.7,143.6 145.4,140.0 152.2,135.3 158.9,128.0 165.7,123.5 172.5,113.0 179.2,110.0 186.0,106.7 192.7,100.7 199.5,95.5 206.3,93.1 213.0,86.0 219.8,79.0 226.5,75.7 233.3,71.6 240.1,66.7 246.8,61.3 253.6,54.7 260.3,46.6 267.1,38.4 273.9,36.5 280.6,37.8 287.4,38.5 294.2,41.9 300.9,43.1 307.7,47.7 314.4,49.5 321.2,52.5 328.0,57.7 334.7,57.7 341.5,59.0 348.2,65.2 355.0,66.8 361.8,74.7 368.5,75.7 375.3,79.8 382.0,83.0 388.8,87.9 395.6,95.3 402.3,100.6 409.1,107.8 415.8,110.6 422.6,116.0 429.4,121.5 436.1,126.9 442.9,134.1 449.7,144.1 456.4,151.4 463.2,154.8 469.9,155.5 476.7,153.3 483.5,148.8 490.2,151.9 497.0,152.8 503.7,154.2 510.5,150.9 517.3,151.5 524.0,151.9 530.8,151.6 537.5,153.3 544.3,155.2 551.1,156.0 557.8,160.8 564.6,160.3 571.3,161.9 578.1,162.9 584.9,159.8 591.6,162.3 598.4,162.3 605.2,163.8 611.9,160.1 618.7,159.9 625.4,162.4 632.2,159.1 639.0,159.7 645.7,161.3 652.5,162.7 659.2,163.1 666.0,165.0"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,192.8 50.8,194.8 57.5,196.5 64.3,194.2 71.0,194.7 77.8,197.5 84.6,196.3 91.3,194.1 98.1,195.5 104.8,191.7 111.6,188.6 118.4,185.7 125.1,184.0 131.9,181.4 138.7,178.6 145.4,175.0 152.2,175.6 158.9,172.9 165.7,169.3 172.5,170.4 179.2,167.3 186.0,166.5 192.7,166.1 199.5,161.8 206.3,154.3 213.0,150.8 219.8,149.8 226.5,143.6 233.3,140.0 240.1,135.3 246.8,128.0 253.6,123.5 260.3,113.0 267.1,110.0 273.9,106.7 280.6,100.7 287.4,95.5 294.2,93.1 300.9,86.0 307.7,79.0 314.4,75.7 321.2,71.6 328.0,66.7 334.7,61.3 341.5,54.7 348.2,46.6 355.0,38.4 361.8,36.5 368.5,37.8 375.3,38.5 382.0,41.9 388.8,43.1 395.6,47.7 402.3,49.5 409.1,52.5 415.8,57.7 422.6,57.7 429.4,59.0 436.1,65.2 442.9,66.8 449.7,74.7 456.4,75.7 463.2,79.8 469.9,83.0 476.7,87.9 483.5,95.3 490.2,100.6 497.0,107.8 503.7,110.6 510.5,116.0 517.3,121.5 524.0,126.9 530.8,134.1 537.5,144.1 544.3,151.4 551.1,154.8 557.8,155.5 564.6,153.3 571.3,148.8 578.1,151.9 584.9,152.8 591.6,154.2 598.4,150.9 605.2,151.5 611.9,151.9 618.7,151.6 625.4,153.3 632.2,155.2 639.0,156.0 645.7,160.8 652.5,160.3 659.2,161.9 666.0,162.9"/><circle class="dot" cx="273.9" cy="36.5" r="4"/><circle class="dot2" cx="361.8" cy="36.5" r="4"/><text class="ink" x="273.9" y="22.0" font-size="11" text-anchor="middle">19 Ara</text><text class="ink" x="361.8" y="22.0" font-size="11" text-anchor="middle">1 Oca</text><line class="curve" x1="54" y1="204" x2="72" y2="204"/><text class="ink" x="78" y="208" font-size="11">ortalanmış</text><line class="curve2" x1="170" y1="204" x2="188" y2="204"/><text class="ink" x="194" y="208" font-size="11">geriye dönük</text></svg>
  <figcaption>Aynı 28 günlük ortalama, iki yerleşim. Ortalanmış pencere (mor) tepeyi 19 Aralık'ta, geriye dönük pencere (turuncu) 1 Ocak'ta gösteriyor: iki eğri aynı, biri 13 gün sağa kaymış.</figcaption>
</figure>

Aynı tepe, iki farklı tarih. Satış Aralık'ın ikinci yarısında tepe yapıyor;
geriye dönük ortalama bunu **13 gün geç** gösteriyor. Sebep basit: son 28
günün ortalaması, 14 gün öncesinin durumunu anlatıyor.

Hangisi ne zaman:

- **Ortalanmış pencere** geçmişi anlamak için doğru: tepe gerçekten olduğu
  yerde görünüyor. Bölüm 10'daki ayrıştırma bunu kullanıyor.
- **Geriye dönük pencere** canlı izlemek ve tahmin için tek seçenek:
  ortalanmış pencere geleceği kullanıyor. Bugün için hesaplamak isteyince
  önümüzdeki 14 gün gerekiyor ve o yüzden serinin son günleri `NaN`.

**Ortalanmış pencere bir tahmin modelinin girdisi olamaz.** Bölüm 06'daki
`shift(-1)` ile aynı sızıntı, daha iyi gizlenmiş hâliyle.

## Özellik olarak hareketli ortalama

Geriye dönük pencere de tek başına yeterince güvenli değil. `s.rolling(7)`
penceresinin içinde **bugün** de var:

```python
print(round(s.rolling(7).mean().loc["2024-03-09"], 1))            # 283.7  bugun dahil
print(round(s.shift(1).rolling(7).mean().loc["2024-03-09"], 1))   # 282.0  dune kadar
```

Bugünün satışını tahmin ederken bugünün satışını içeren bir ortalamayı
kullanamazsın. Kural: **önce `shift(1)`, sonra `rolling`.** Böylece pencere
dünde bitiyor.

## Ortalamadan başka işlemler

Pencere üzerinde her özet alınabiliyor:

```python
w = s.rolling(7)

print(w.sum().loc["2024-03-10"])        # 1978.0   son 7 gunun toplami
print(w.max().loc["2024-03-10"])        # 384.0
print(w.min().loc["2024-03-10"])        # 236.0
print(w.median().loc["2024-03-10"])     # 262.0
print(round(w.std().loc["2024-03-10"], 1))   # 51.8
```

**Hareketli standart sapma** serinin o dönemde ne kadar oynak olduğunu
ölçüyor. Fiyat serilerinde bunun adı **oynaklık** (volatility):

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
r = close.pct_change()

vol = r.rolling(20).std() * (252 ** 0.5) * 100      # yilliklandirilmis, yuzde
print(round(vol.mean(), 1))                         # 27.0
print(vol.idxmax().date(), round(vol.max(), 1))     # 2023-03-02 39.8
```

Oynaklık sabit değil: sakin dönemde %18.5'e iniyor, çalkantıda %39.8'e
çıkıyor.

## Ortalama ve ortanca: aykırı değer

Web sitesinin günlük ziyaret sayısında (`web_traffic.csv`) 14 Mart'ta bir
sıçrama var:

```python
visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
print(visits.loc["2024-03-12":"2024-03-16"].tolist())
# [4090, 3737, 9593, 3965, 3147]

print(round(visits.rolling(7).mean().loc["2024-03-14"]))     # 4587
print(visits.rolling(7).median().loc["2024-03-14"])          # 4090.0
```

Tek bir olağandışı gün 7 günlük ortalamayı 3810'dan 4587'ye çekiyor ve
pencere o günü dışarı atana kadar bir hafta boyunca yüksek tutuyor. Ortanca
hiç etkilenmiyor. **Aykırı değeri olan seride düzleştirmek için ortanca,
ortalamadan sağlam.**

Aynı araç aykırı değeri **bulmak** için de kullanılıyor. Her günü, kendisinden
önceki 28 günün ortalaması ve yayılımıyla karşılaştır:

```python
base = visits.shift(1).rolling(28)
z = (visits - base.mean()) / base.std()

print(round(z.loc["2024-03-14"], 1))              # 11.2
print(z[z.abs() > 3].index.strftime("%m-%d").tolist())
# ['03-14', '06-20', '10-08']
```

14 Mart, kendi geçmişinin 11 standart sapma üstünde. Eşik 3 alınınca yılın üç
olağandışı günü çıkıyor: iki sıçrama ve bir kesinti. (`shift(1)` burada da
gerekli: günü kendi ortalamasına katarsan sapmasını küçültmüş oluyorsun.)
Bölüm 21 bu fikri sistematik hâle getiriyor.

## Zamana göre pencere

`rolling(7)` yedi **satır** sayıyor. Eksik günleri olan seride bu, Bölüm
06'daki tuzağın aynısı:

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

print(fixed.rolling(7).sum().loc["2024-07-20"])        # 2092.0
print(fixed.rolling("7D").sum().loc["2024-07-20"])     # 1200.0
print(fixed.rolling("7D").count().loc["2024-07-20"])   # 4.0
```

Yedi satırlık pencere 20 Temmuz'dan geriye 10 günü kapsıyor (11–20 Temmuz),
çünkü arada üç gün eksik: "son 7 günün toplamı" diye okunan sayı aslında 10
günlük bir aralığın 7 kaydı.

`rolling("7D")` satır değil **süre** sayıyor: 14–20 Temmuz arası. O aralıkta
yalnızca dört kayıt var ve `count` bunu gösteriyor. Düzensiz ya da eksikli
seride pencereyi süreyle tanımla ve kaç gözlem içerdiğine bak.

## Genişleyen pencere

`rolling` sabit boyda bir pencereyi kaydırıyor. `expanding` pencerenin başını
sabit tutup sonunu uzatıyor: **baştan bugüne her şey.**

```python
print(s.expanding().mean().head(3).round(1).tolist())   # [305.0, 291.0, 261.0]
print(round(s.expanding().mean().iloc[-1], 1))          # 260.0

record = s.expanding().max()
print((record.diff() > 0).sum())                        # 17
```

"Bugüne kadarki ortalama", "bugüne kadarki rekor": mağaza üç yılda 17 kez
satış rekoru kırmış. `expanding` hiçbir zaman geleceğe bakmıyor; her satır o
gün bilinen bilgiyle hesaplanıyor.

## Üstel ağırlıklı ortalama

Hareketli ortalamada penceredeki her gün **eşit** ağırlıkta; 7 gün önceki
değer bugünkü kadar sayılıyor, 8 gün önceki ise hiç sayılmıyor. Üstel
ağırlıklı ortalama (`ewm`) ağırlığı yumuşakça azaltıyor:

<figure class="fig">
  <svg viewBox="0 0 680 200" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="40" y1="170.0" x2="316" y2="170.0"/><text class="dim" x="34" y="173.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="118.1" x2="316" y2="118.1"/><text class="dim" x="34" y="121.6" font-size="10.5" text-anchor="end">0.1</text><line class="grid" x1="40" y1="66.3" x2="316" y2="66.3"/><text class="dim" x="34" y="69.8" font-size="10.5" text-anchor="end">0.2</text><line class="line" x1="40" y1="170" x2="316" y2="170"/><line class="line" x1="52.5" y1="170" x2="52.5" y2="174"/><text class="dim" x="52.5" y="186" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="178.0" y1="170" x2="178.0" y2="174"/><text class="dim" x="178.0" y="186" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="303.5" y1="170" x2="303.5" y2="174"/><text class="dim" x="303.5" y="186" font-size="10.5" text-anchor="middle">14</text><rect class="dot2" x="47.0" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="64.9" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="82.8" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="100.8" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="118.7" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="136.6" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="154.5" y="95.9" width="11.1" height="74.1" rx="3" opacity="0.9"/><rect class="dot2" x="172.4" y="170.0" width="11.2" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="190.4" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="208.3" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="226.2" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="244.1" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="262.1" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="280.0" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><rect class="dot2" x="297.9" y="170.0" width="11.1" height="0.0" rx="3" opacity="0.9"/><text class="ink" x="40" y="18" font-size="12" text-anchor="start" font-weight="600">rolling(7)</text></g><g transform="translate(350,0)"><line class="grid" x1="40" y1="170.0" x2="316" y2="170.0"/><text class="dim" x="34" y="173.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="118.1" x2="316" y2="118.1"/><text class="dim" x="34" y="121.6" font-size="10.5" text-anchor="end">0.1</text><line class="grid" x1="40" y1="66.3" x2="316" y2="66.3"/><text class="dim" x="34" y="69.8" font-size="10.5" text-anchor="end">0.2</text><line class="line" x1="40" y1="170" x2="316" y2="170"/><line class="line" x1="52.5" y1="170" x2="52.5" y2="174"/><text class="dim" x="52.5" y="186" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="178.0" y1="170" x2="178.0" y2="174"/><text class="dim" x="178.0" y="186" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="303.5" y1="170" x2="303.5" y2="174"/><text class="dim" x="303.5" y="186" font-size="10.5" text-anchor="middle">14</text><rect class="dot" x="47.0" y="40.4" width="11.1" height="129.6" rx="3" opacity="0.9"/><rect class="dot" x="64.9" y="72.8" width="11.1" height="97.2" rx="3" opacity="0.9"/><rect class="dot" x="82.8" y="97.1" width="11.1" height="72.9" rx="3" opacity="0.9"/><rect class="dot" x="100.8" y="115.3" width="11.1" height="54.7" rx="3" opacity="0.9"/><rect class="dot" x="118.7" y="129.0" width="11.1" height="41.0" rx="3" opacity="0.9"/><rect class="dot" x="136.6" y="139.2" width="11.1" height="30.8" rx="3" opacity="0.9"/><rect class="dot" x="154.5" y="146.9" width="11.1" height="23.1" rx="3" opacity="0.9"/><rect class="dot" x="172.4" y="152.7" width="11.2" height="17.3" rx="3" opacity="0.9"/><rect class="dot" x="190.4" y="157.0" width="11.1" height="13.0" rx="3" opacity="0.9"/><rect class="dot" x="208.3" y="160.3" width="11.1" height="9.7" rx="3" opacity="0.9"/><rect class="dot" x="226.2" y="162.7" width="11.1" height="7.3" rx="3" opacity="0.9"/><rect class="dot" x="244.1" y="164.5" width="11.1" height="5.5" rx="3" opacity="0.9"/><rect class="dot" x="262.1" y="165.9" width="11.1" height="4.1" rx="3" opacity="0.9"/><rect class="dot" x="280.0" y="166.9" width="11.1" height="3.1" rx="3" opacity="0.9"/><rect class="dot" x="297.9" y="167.7" width="11.1" height="2.3" rx="3" opacity="0.9"/><text class="ink" x="40" y="18" font-size="12" text-anchor="start" font-weight="600">ewm(span=7)</text></g></svg>
  <figcaption>Her günün ortalamadaki ağırlığı (yatay eksen: kaç gün önce). Hareketli ortalamada yedi gün eşit, sekizinci gün sıfır. Üstel ağırlıkta en yeni gün en ağır; ağırlık hiç sıfıra inmiyor, yalnızca küçülüyor.</figcaption>
</figure>

```python
ewm7 = s.ewm(span=7).mean()

print(round(ewm7.loc["2024-03-09"], 1))                  # 299.2
print(round(s.rolling(7).mean().loc["2024-03-09"], 1))   # 283.7
```

9 Mart cumartesi satış yüksekti (384). `ewm` en yeni güne en büyük ağırlığı
verdiği için daha hızlı tepki veriyor. `span=7`, en yeni güne `2 / (7 + 1) =
0.25` ağırlık demek; her eski gün bir öncekinin dörtte üçü kadar sayılıyor.

Ani bir seviye değişiminde fark açık:

<figure class="fig">
  <svg viewBox="0 0 680 220" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="175.3" x2="666" y2="175.3"/><text class="dim" x="38" y="178.8" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="102.0" x2="666" y2="102.0"/><text class="dim" x="38" y="105.5" font-size="10.5" text-anchor="end">150</text><line class="grid" x1="44" y1="28.7" x2="666" y2="28.7"/><text class="dim" x="38" y="32.2" font-size="10.5" text-anchor="end">200</text><line class="line" x1="44" y1="190" x2="666" y2="190"/><line class="line" x1="240.4" y1="190" x2="240.4" y2="194"/><text class="dim" x="240.4" y="206" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="404.1" y1="190" x2="404.1" y2="194"/><text class="dim" x="404.1" y="206" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="567.8" y1="190" x2="567.8" y2="194"/><text class="dim" x="567.8" y="206" font-size="10.5" text-anchor="middle">10</text><polyline class="curve3" style="stroke-width:1.6" points="44.0,175.3 76.7,175.3 109.5,175.3 142.2,175.3 174.9,175.3 207.7,175.3 240.4,28.7 273.2,28.7 305.9,28.7 338.6,28.7 371.4,28.7 404.1,28.7 436.8,28.7 469.6,28.7 502.3,28.7 535.1,28.7 567.8,28.7 600.5,28.7 633.3,28.7 666.0,28.7"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,175.3 76.7,175.3 109.5,175.3 142.2,175.3 174.9,175.3 207.7,175.3 240.4,146.0 273.2,116.7 305.9,87.3 338.6,58.0 371.4,28.7 404.1,28.7 436.8,28.7 469.6,28.7 502.3,28.7 535.1,28.7 567.8,28.7 600.5,28.7 633.3,28.7 666.0,28.7"/><polyline class="curve" style="stroke-width:2.4" points="44.0,175.3 76.7,175.3 109.5,175.3 142.2,175.3 174.9,175.3 207.7,175.3 240.4,126.4 273.2,93.9 305.9,72.1 338.6,57.6 371.4,48.0 404.1,41.5 436.8,37.3 469.6,34.4 502.3,32.5 535.1,31.2 567.8,30.4 600.5,29.8 633.3,29.4 666.0,29.2"/><line class="curve3" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">seri</text><line class="curve2" x1="128" y1="22" x2="146" y2="22"/><text class="ink" x="152" y="26" font-size="11">rolling(5)</text><line class="curve" x1="244" y1="22" x2="262" y2="22"/><text class="ink" x="268" y="26" font-size="11">ewm(span=5)</text></svg>
  <figcaption>Seri 100'den 200'e sıçrıyor (yatay eksen: sıçramadan sonraki adım). Üstel ağırlıklı ortalama ilk adımda daha çok tepki veriyor; hareketli ortalama düz bir rampayla beş adımda yetişiyor, üstel olan yaklaşıyor ama tam yetişmesi uzun sürüyor.</figcaption>
</figure>

`ewm`'in iki artısı daha var: baştaki satırlar boş kalmıyor ve hesap için
yalnızca bir önceki değer yetiyor. Bölüm 16'daki üstel düzleştirme tam olarak
bu fikrin tahmin yöntemine dönüşmüş hâli.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Pencereyi mevsim uzunluğuna uydurmamak | Düzleşmiş seri hâlâ dalgalı | Haftalık desen için 7, yıllık için 365 |
| `center=True`'yu özellik olarak kullanmak | Model geleceği görüyor | Geriye dönük pencere |
| `shift(1)` olmadan `rolling` özelliği | Bugünün değeri kendi tahminine giriyor | `s.shift(1).rolling(7).mean()` |
| Geriye dönük ortalamanın gecikmesini unutmak | Dönüm noktası geç görülüyor | Pencerenin yarısı kadar gecikme bekle |
| Eksik günlü seride `rolling(7)` | Pencere 7 günden uzun bir aralığı kapsıyor | `rolling("7D")` ve `count()` |
| Aykırı değerli seride ortalama | Tek gün bir haftayı kaydırıyor | `rolling(...).median()` |
| Baştaki `NaN`'leri görmemek | Grafik geç başlıyor, model satır kaybediyor | `min_periods` ya da bilerek at |

## Özet

- **`s.rolling(n).mean()`** her satır için son n satırın ortalaması:
  satır kaybetmeden düzleştirme. İlk n-1 satır `NaN`.
- Pencere boyu **mevsim uzunluğu** kadar: 7 haftayı, 365 yılı bastırıyor.
- **Geriye dönük** pencere gecikmeli ama dürüst; **ortalanmış** pencere
  doğru yerde ama geleceği kullanıyor.
- Özellik kurarken **önce `shift(1)`, sonra `rolling`.**
- Pencerede her özet alınıyor: `sum`, `std` (oynaklık), `max`, `median`
  (aykırı değere dayanıklı).
- Eksikli seride **`rolling("7D")`**: satır değil süre.
- **`expanding`** baştan bugüne; **`ewm`** yeni günlere daha çok ağırlık
  veriyor ve daha hızlı tepki veriyor.
