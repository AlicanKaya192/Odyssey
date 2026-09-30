# Eksik Veri ve Aykırı Değerler

Buraya kadar çalıştığın seriler temizdi: her gün için bir satır, her satırda
makul bir sayı. Gerçek veri böyle gelmez. Kasa bir gün kapalı kalır, sensör beş
saat susar, bir kampanya günü trafiği ikiye katlar, biri aynı günü iki kez
girer.

Zaman serisinde bu sorunların bedeli ağırdır, çünkü her şey **sıraya ve düzenli
aralığa** yaslanıyor: `shift(7)` "7 satır önce" demek, `rolling(7)` "son 7
satır". Bir gün eksikse hepsi sessizce kayar (Bölüm 03). Tek bir aykırı gün ise
ortalamayı, trendi ve haftalık deseni birden bozar (Bölüm 10).

Bu bölüm tahminden önceki son hazırlık: eksikleri bul, doldur ya da bırak;
aykırı günleri bul, düzelt ya da işaretle.

## 1. Eksik verinin üç hâli

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Satır yok</span><span>O günün kaydı hiç yazılmamış. Tabloda <code>NaN</code> görünmez; en sinsi hâli.</span></div>
<div class="anat-row"><span>Satır var, değer boş</span><span>Tarih var, değer <code>NaN</code>. <code>isna()</code> ile sayılır.</span></div>
<div class="anat-row"><span>Boşluk kılık değiştirmiş</span><span>Eksik yerine <code>0</code>, <code>-1</code> ya da <code>999</code> yazılmış. Sayı gibi görünür, ortalamaya girer.</span></div>
</div>
<figcaption>Üçü de aynı şey: o an için ölçüm yok. Ama yalnızca ortadaki kendiliğinden görünür.</figcaption>
</figure>

`sales_messy.csv` bir mağazanın 2024 satışı, sistemden çıktığı hâliyle:

```python
import pandas as pd

raw = pd.read_csv("sales_messy.csv", parse_dates=["date"])
print(len(raw), raw["date"].nunique(), int(raw["sales"].isna().sum()))
# 362 358 0
```

362 satır, 358 farklı gün, **sıfır `NaN`**. İlk bakışta temiz. Oysa 2024'te 366
gün var: 8 gün kayıp ve 4 gün iki kez yazılmış. Satırlar da karışık sırada.

## 2. Önce görünür kıl

Doldurmadan önce eksikleri **`NaN`'a çevir**. Üç adım:

```python
daily = raw.groupby("date")["sales"].sum()      # ayni gunun parcalarini topla
daily = daily.sort_index()
full = daily.asfreq("D")                        # her gune bir satir

print(len(full), int(full.isna().sum()))        # 366 8
print(full[full.isna()].index.strftime("%m-%d").tolist())
# ['02-10', '02-11', '04-23', '07-15', '07-16', '07-17', '10-29', '12-25']
```

İki kez yazılan günler yinelenmiş kayıt değil, **bölünmüş** kayıttı (sabah ve
akşam kasası): toplanınca doğru sayı çıkıyor. Bunu bilmeden `drop_duplicates`
yapsaydın o günlerin satışının yarısını silerdin. Veriyi tanımadan temizleme.

Boşlukların **uzunluğu** da önemli; tek günlük boşluk ile üç günlük boşluk aynı
ilacı almaz:

```python
missing = full.isna()
run_id = (missing != missing.shift()).cumsum()
print(missing.groupby(run_id).sum().loc[lambda x: x > 0].tolist())
# [2, 1, 3, 1, 1]
```

`(missing != missing.shift()).cumsum()` her değişimde bir artan bir sayaç:
art arda gelen eksik günler aynı numarayı alıyor. Bu kalıbı bir kenara yaz;
"art arda kaç tane" sorusunun standart cevabı.

## 3. Neden eksik?

Doldurma yöntemi **nedene** bağlı (Bölüm 08'deki iki tür eksiklik):

| Neden | Gerçek değer | Doğru işlem |
|---|---|---|
| Mağaza kapalıydı, satış olmadı | 0 | `fillna(0)` |
| Satış oldu, kayıt kayboldu | Bilinmiyor | Tahmin ederek doldur, ya da boş bırak |
| Sensör arızalıydı | Bilinmiyor | Kısa ise doldur, uzun ise boş bırak |
| Ürün o tarihte henüz yoktu | Tanımsız | Doldurma; seriyi o tarihten başlat |

Bu mağaza her gün açık; 8 gün kayıt hatası. Yani **bilinmeyen bir sayıyı tahmin
edeceksin**. Doldurmak küçük bir tahmin problemidir.

## 4. Doldurma yöntemleri: hangisi ne kadar tutuyor?

Bu 8 günün gerçek değerleri başka bir dosyada duruyor (`store_sales.csv`),
dolayısıyla her yöntemi **ölçebiliriz**: doldurulan değer gerçeğinden ortalama
kaç birim sapıyor?

```python
zero     = full.fillna(0)
average  = full.fillna(full.mean())
forward  = full.ffill()                          # son bilinen deger
linear   = full.interpolate()                    # iki komsu arasinda duz cizgi
weekday  = full.fillna(full.groupby(full.index.dayofweek).transform("mean"))
week_ago = full.fillna(full.shift(7))            # gecen haftanin ayni gunu
```

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.0" x2="666" y2="210.0"/><text class="dim" x="38" y="213.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="154.2" x2="666" y2="154.2"/><text class="dim" x="38" y="157.7" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="98.5" x2="666" y2="98.5"/><text class="dim" x="38" y="102.0" font-size="10.5" text-anchor="end">40</text><line class="grid" x1="44" y1="42.7" x2="666" y2="42.7"/><text class="dim" x="38" y="46.2" font-size="10.5" text-anchor="end">60</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="104.2" y1="210" x2="104.2" y2="214"/><text class="dim" x="104.2" y="226" font-size="10.5" text-anchor="middle">ortalama</text><line class="line" x1="204.5" y1="210" x2="204.5" y2="214"/><text class="dim" x="204.5" y="226" font-size="10.5" text-anchor="middle">doğrusal</text><line class="line" x1="304.8" y1="210" x2="304.8" y2="214"/><text class="dim" x="304.8" y="226" font-size="10.5" text-anchor="middle">ffill</text><line class="line" x1="405.2" y1="210" x2="405.2" y2="214"/><text class="dim" x="405.2" y="226" font-size="10.5" text-anchor="middle">gün ortalaması</text><line class="line" x1="505.5" y1="210" x2="505.5" y2="214"/><text class="dim" x="505.5" y="226" font-size="10.5" text-anchor="middle">geçen hafta</text><line class="line" x1="605.8" y1="210" x2="605.8" y2="214"/><text class="dim" x="605.8" y="226" font-size="10.5" text-anchor="middle">önce + sonra</text><rect class="dot2" x="73.1" y="49.8" width="62.2" height="160.2" rx="3" opacity="0.9"/><rect class="dot2" x="173.4" y="81.6" width="62.2" height="128.4" rx="3" opacity="0.9"/><rect class="dot2" x="273.7" y="84.5" width="62.2" height="125.5" rx="3" opacity="0.9"/><rect class="dot" x="374.1" y="138.4" width="62.2" height="71.6" rx="3" opacity="0.9"/><rect class="dot" x="474.4" y="182.8" width="62.2" height="27.2" rx="3" opacity="0.9"/><rect class="dot" x="574.7" y="190.5" width="62.2" height="19.5" rx="3" opacity="0.9"/><text class="ink" x="104.2" y="42.9" font-size="11.5" text-anchor="middle">57.5</text><text class="ink" x="204.5" y="74.6" font-size="11.5" text-anchor="middle">46.1</text><text class="ink" x="304.8" y="77.6" font-size="11.5" text-anchor="middle">45.0</text><text class="ink" x="405.2" y="131.5" font-size="11.5" text-anchor="middle">25.7</text><text class="ink" x="505.5" y="175.8" font-size="11.5" text-anchor="middle">9.8</text><text class="ink" x="605.8" y="183.5" font-size="11.5" text-anchor="middle">7.0</text></svg>
  <figcaption>Sekiz eksik günün doldurulmasında ortalama mutlak hata (birim). Mevsimi bilmeyen üç yöntem (turuncu) birbirine yakın ve kötü; haftalık deseni kullananlar (mor) çok daha isabetli.</figcaption>
</figure>

| Yöntem | Ortalama mutlak hata |
|---|---|
| Sıfır | 281.4 |
| Genel ortalama | 57.5 |
| `interpolate()` (doğrusal) | 46.1 |
| `ffill()` | 45.0 |
| Aynı haftanın günü ortalaması | 25.7 |
| Geçen haftanın aynı günü | 9.8 |
| Bir hafta öncesi ile sonrasının ortalaması | 7.0 |

`ffill` ve doğrusal doldurma neredeyse genel ortalama kadar kötü. Neden?
10 Şubat Cumartesi'ye bak: gerçek değer 388. `ffill` cuma gününün 302'sini
yazıyor; doğrusal doldurma cuma ile pazartesi arasına çizgi çekip 276 diyor.
İkisi de **haftalık deseni bilmiyor**. "Geçen cumartesi 389'du" diyen yöntem
1 birimle tutturuyor.

**Mevsimsel seride mevsimsel doldur.** En iyi sonuç iki taraftan bakan yöntemde:

```python
both = pd.concat([full.shift(7), full.shift(-7)], axis=1).mean(axis=1)
filled = full.fillna(both)
```

`mean(axis=1)` boşları atladığı için yalnızca bir tarafı bilinen günlerde
(25 Aralık: bir hafta sonrası 2025'te) kendiliğinden tek tarafa düşüyor.

`ffill` ve `interpolate` kötü yöntemler değil; **mevsimi olmayan**, yavaş
değişen seride (sıcaklık sensörü, stok düzeyi, fiyat) doğru seçim onlar.

## 5. Uzun boşluk

Boşluk uzadıkça basit yöntemler daha da kötüleşiyor. Temmuz'da 14 günlük bir
kesinti olduğunu düşün:

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="206.3" x2="666" y2="206.3"/><text class="dim" x="38" y="209.8" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="162.8" x2="666" y2="162.8"/><text class="dim" x="38" y="166.3" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="119.3" x2="666" y2="119.3"/><text class="dim" x="38" y="122.8" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="75.8" x2="666" y2="75.8"/><text class="dim" x="38" y="79.3" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="32.3" x2="666" y2="32.3"/><text class="dim" x="38" y="35.8" font-size="10.5" text-anchor="end">400</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">24 Haz</text><line class="line" x1="150.2" y1="220" x2="150.2" y2="224"/><text class="dim" x="150.2" y="236" font-size="10.5" text-anchor="middle">1 Tem</text><line class="line" x1="256.4" y1="220" x2="256.4" y2="224"/><text class="dim" x="256.4" y="236" font-size="10.5" text-anchor="middle">8 Tem</text><line class="line" x1="362.6" y1="220" x2="362.6" y2="224"/><text class="dim" x="362.6" y="236" font-size="10.5" text-anchor="middle">15 Tem</text><line class="line" x1="468.8" y1="220" x2="468.8" y2="224"/><text class="dim" x="468.8" y="236" font-size="10.5" text-anchor="middle">22 Tem</text><line class="line" x1="575.0" y1="220" x2="575.0" y2="224"/><text class="dim" x="575.0" y="236" font-size="10.5" text-anchor="middle">29 Tem</text><rect class="box" x="248.8" y="30" width="212.4" height="190" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.4" points="44.0,209.8 59.2,192.4 74.3,180.2 89.5,168.9 104.7,136.7 119.9,79.3 135.0,108.9 150.2,203.7 165.4,194.2 180.5,187.2 195.7,160.2 210.9,117.6 226.0,79.3 241.2,112.4 256.4,193.3 271.6,192.4 286.7,182.9 301.9,149.8 317.1,134.1 332.2,81.1 347.4,108.9 362.6,185.5 377.8,171.5 392.9,175.0 408.1,160.2 423.3,126.3 438.4,81.9 453.6,115.9 468.8,178.5 484.0,178.5 499.1,178.5 514.3,161.1 529.5,104.6 544.6,75.0 559.8,116.7 575.0,178.5 590.1,162.0 605.3,172.4 620.5,161.1 635.7,129.8 650.8,82.8 666.0,107.2"/><polyline class="curve2" style="stroke-width:2.4" points="241.2,112.4 256.4,116.8 271.6,121.2 286.7,125.6 301.9,130.0 317.1,134.4 332.2,138.8 347.4,143.2 362.6,147.6 377.8,152.1 392.9,156.5 408.1,160.9 423.3,165.3 438.4,169.7 453.6,174.1 468.8,178.5"/><polyline class="curve" style="stroke-width:2.4" points="256.4,203.7 271.6,194.2 286.7,187.2 301.9,160.2 317.1,117.6 332.2,79.3 347.4,112.4 362.6,203.7 377.8,194.2 392.9,187.2 408.1,160.2 423.3,117.6 438.4,79.3 453.6,112.4"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">gerçek</text><line class="curve2" x1="142" y1="38" x2="160" y2="38"/><text class="ink" x="166" y="42" font-size="11">doğrusal doldurma</text><line class="curve" x1="307" y1="38" x2="325" y2="38"/><text class="ink" x="331" y="42" font-size="11">haftalık zincir</text></svg>
  <figcaption>Gölgeli iki hafta silinip iki yöntemle dolduruldu. Doğrusal doldurma düz bir çizgi; haftalık zincir cumartesi tepelerini koruyor ve gerçeğin yanından gidiyor.</figcaption>
</figure>

| Yöntem | Ortalama mutlak hata |
|---|---|
| `ffill()` | 50.6 |
| `interpolate()` | 47.5 |
| Haftalık zincir (her gün, 7 gün öncesinden) | 9.6 |

Doğrusal doldurma iki haftayı dümdüz bir çizgiyle geçiyor; iki cumartesi tepesi
yok oluyor. Haftalık zincir deseni koruyor:

```python
chain = gap.copy()
for day in chain[chain.isna()].index:
    chain.loc[day] = chain.loc[day - pd.Timedelta(days=7)]
```

İkinci haftanın günleri, birinci haftanın **doldurulmuş** değerlerinden
besleniyor.

Uzun boşlukları yanlışlıkla doldurmamak için `limit`:

```python
full.ffill(limit=2)          # en cok 2 ardisik bosluk doldurulur
```

Dikkat: `limit=2` on günlük bir boşluğun **ilk iki gününü** dolduruyor, gerisini
bırakıyor. Çoğu zaman istediğin "kısa boşlukları doldur, uzunlara hiç dokunma".
Onu Kısım 2'deki sayaçla yaparsın:

```python
missing = r.isna()
run_id = (missing != missing.shift()).cumsum()
run_length = missing.groupby(run_id).transform("sum")

short = missing & (run_length <= 3)
result = r.where(~short, r.interpolate())
```

Makine sensörü kaydında (`machine_log.csv`, düzensiz aralıklı) 10 dakikalık
ızgaraya oturtunca 54 boş hücre çıkıyor: 21'i birkaç hücrelik kısa boşluk, 33'ü
tek bir beş buçuk saatlik arıza. Yukarıdaki kod 21'ini dolduruyor, arızaya
dokunmuyor. Beş saati "tahmin etmek" veri üretmek olurdu.

## 6. Doldurmanın bedeli

Doldurulmuş değer **ölçüm değil, tahmin.** Üç kural:

**İşaretle.** Hangi satırların doldurulduğunu bir sütunda sakla:

```python
frame = pd.DataFrame({"sales": filled, "was_missing": full.isna()})
```

Sonradan "bu ayın toplamının ne kadarı gerçek" sorusunu cevaplayabilirsin ve
model doğrularken doldurulmuş günleri dışarıda tutabilirsin.

**Geleceği kullanma.** `interpolate` ve "bir hafta sonrası" boşluğun
**sonrasındaki** değeri kullanıyor. Geçmişi temizlerken sorun değil. Ama bir
tahmin modelini sınarken (Bölüm 15) eğitim verisine gelecekten bilgi sızdırır.
Orada yalnızca geriye bakan yöntemler: `ffill`, geçen haftanın aynı günü.

**Oynaklık azalır.** Doldurulan değerler "ortalama" tahminlerdir; gerçek günlerin
sürprizini taşımazlar. Çok doldurulmuş bir seri olduğundan daha düzenli görünür
ve model belirsizliği küçümser.

Verinin **%5–10'undan fazlası** eksikse doldurmak yerine eksikliği kabul eden
bir yöntem düşün, ya da daha kaba bir sıklığa geç (günlük yerine haftalık).

## 7. Aykırı değer

Aykırı değer, serinin geri kalanının davranışına uymayan gözlem. Web trafiğinde
(`web_traffic.csv`) üç tane var: iki kampanya günü ve bir kesinti.

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="212.8" x2="666" y2="212.8"/><text class="dim" x="38" y="216.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="175.4" x2="666" y2="175.4"/><text class="dim" x="38" y="178.9" font-size="10.5" text-anchor="end">2,000</text><line class="grid" x1="44" y1="137.9" x2="666" y2="137.9"/><text class="dim" x="38" y="141.4" font-size="10.5" text-anchor="end">4,000</text><line class="grid" x1="44" y1="100.5" x2="666" y2="100.5"/><text class="dim" x="38" y="104.0" font-size="10.5" text-anchor="end">6,000</text><line class="grid" x1="44" y1="63.0" x2="666" y2="63.0"/><text class="dim" x="38" y="66.5" font-size="10.5" text-anchor="end">8,000</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">Oca</text><line class="line" x1="146.2" y1="220" x2="146.2" y2="224"/><text class="dim" x="146.2" y="236" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="250.2" y1="220" x2="250.2" y2="224"/><text class="dim" x="250.2" y="236" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="354.1" y1="220" x2="354.1" y2="224"/><text class="dim" x="354.1" y="236" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="459.8" y1="220" x2="459.8" y2="224"/><text class="dim" x="459.8" y="236" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="563.8" y1="220" x2="563.8" y2="224"/><text class="dim" x="563.8" y="236" font-size="10.5" text-anchor="middle">Kas</text><polyline class="curve" style="stroke-width:1.2" points="44.0,139.4 45.7,136.9 47.4,135.6 49.1,141.5 50.8,135.0 52.5,158.2 54.2,156.7 55.9,136.9 57.6,133.4 59.3,141.3 61.0,131.0 62.7,133.3 64.4,160.5 66.2,157.1 67.9,136.2 69.6,144.2 71.3,135.6 73.0,140.1 74.7,138.9 76.4,160.5 78.1,160.0 79.8,137.7 81.5,137.6 83.2,143.5 84.9,138.9 86.6,142.8 88.3,162.2 90.0,159.8 91.7,134.6 93.4,135.5 95.1,140.1 96.8,140.5 98.5,140.9 100.2,158.5 101.9,156.3 103.6,137.8 105.3,135.3 107.1,136.7 108.8,132.1 110.5,145.1 112.2,164.3 113.9,159.4 115.6,135.5 117.3,139.4 119.0,136.3 120.7,142.2 122.4,142.5 124.1,160.8 125.8,156.6 127.5,135.3 129.2,140.5 130.9,137.2 132.6,140.3 134.3,137.8 136.0,161.8 137.7,159.0 139.4,140.6 141.1,138.1 142.8,140.3 144.5,140.9 146.2,137.5 148.0,159.8 149.7,158.8 151.4,139.5 153.1,135.6 154.8,140.9 156.5,135.0 158.2,132.8 159.9,159.6 161.6,154.0 163.3,129.9 165.0,136.2 166.7,142.8 168.4,33.2 170.1,138.6 171.8,153.9 173.5,157.3 175.2,135.0 176.9,138.9 178.6,140.6 180.3,136.5 182.0,142.0 183.7,159.4 185.4,157.5 187.1,137.8 188.8,135.9 190.6,139.6 192.3,135.6 194.0,136.4 195.7,163.2 197.4,161.6 199.1,140.6 200.8,135.4 202.5,136.8 204.2,136.8 205.9,137.3 207.6,157.1 209.3,156.3 211.0,140.0 212.7,143.6 214.4,135.4 216.1,138.7 217.8,137.7 219.5,159.4 221.2,161.8 222.9,143.4 224.6,134.2 226.3,133.7 228.0,134.3 229.7,137.1 231.5,158.2 233.2,160.0 234.9,137.7 236.6,139.4 238.3,139.9 240.0,137.1 241.7,131.3 243.4,163.7 245.1,157.2 246.8,135.3 248.5,142.3 250.2,136.7 251.9,137.5 253.6,139.6 255.3,160.2 257.0,162.6 258.7,131.2 260.4,128.6 262.1,131.7 263.8,139.0 265.5,136.8 267.2,157.9 268.9,161.0 270.6,138.9 272.4,135.9 274.1,139.5 275.8,144.2 277.5,142.5 279.2,158.2 280.9,159.8 282.6,139.0 284.3,132.7 286.0,137.6 287.7,140.6 289.4,138.2 291.1,152.7 292.8,161.8 294.5,130.9 296.2,132.3 297.9,138.5 299.6,139.2 301.3,132.4 303.0,158.2 304.7,160.3 306.4,130.8 308.1,137.3 309.8,136.7 311.5,137.8 313.2,139.0 315.0,158.5 316.7,159.9 318.4,136.0 320.1,133.9 321.8,133.7 323.5,133.3 325.2,132.1 326.9,156.8 328.6,160.5 330.3,134.2 332.0,143.9 333.7,140.5 335.4,45.6 337.1,144.0 338.8,154.8 340.5,161.6 342.2,143.3 343.9,140.7 345.6,140.7 347.3,138.0 349.0,138.5 350.7,156.0 352.4,159.3 354.1,137.3 355.9,141.5 357.6,136.0 359.3,140.8 361.0,144.9 362.7,155.3 364.4,161.7 366.1,141.9 367.8,141.1 369.5,135.4 371.2,143.4 372.9,139.4 374.6,157.3 376.3,153.5 378.0,139.0 379.7,137.7 381.4,141.1 383.1,130.1 384.8,138.4 386.5,159.1 388.2,158.5 389.9,141.3 391.6,138.0 393.3,142.5 395.0,132.1 396.8,138.5 398.5,159.3 400.2,155.6 401.9,142.3 403.6,132.5 405.3,132.0 407.0,140.7 408.7,135.3 410.4,159.1 412.1,156.5 413.8,137.8 415.5,141.2 417.2,135.5 418.9,138.7 420.6,137.2 422.3,156.2 424.0,155.5 425.7,135.5 427.4,143.0 429.1,135.3 430.8,139.0 432.5,133.8 434.2,159.4 435.9,154.9 437.6,136.0 439.4,137.9 441.1,136.8 442.8,144.2 444.5,135.7 446.2,158.6 447.9,161.8 449.6,136.4 451.3,136.7 453.0,136.6 454.7,138.3 456.4,134.9 458.1,156.7 459.8,158.6 461.5,115.7 463.2,117.6 464.9,118.3 466.6,112.4 468.3,118.1 470.0,147.5 471.7,141.8 473.4,109.9 475.1,116.8 476.8,111.1 478.5,113.1 480.3,120.2 482.0,141.6 483.7,143.1 485.4,112.1 487.1,128.1 488.8,111.3 490.5,111.8 492.2,119.8 493.9,138.9 495.6,143.2 497.3,114.5 499.0,111.1 500.7,108.7 502.4,114.6 504.1,112.0 505.8,141.1 507.5,145.2 509.2,107.1 510.9,111.6 512.6,114.7 514.3,110.0 516.0,112.7 517.7,144.6 519.4,139.1 521.2,115.1 522.9,210.2 524.6,110.6 526.3,110.6 528.0,105.7 529.7,141.9 531.4,143.2 533.1,118.8 534.8,118.3 536.5,112.0 538.2,113.2 539.9,119.4 541.6,144.7 543.3,144.1 545.0,107.4 546.7,119.7 548.4,113.5 550.1,122.9 551.8,116.4 553.5,137.5 555.2,146.8 556.9,109.5 558.6,124.0 560.3,115.0 562.0,120.5 563.8,115.4 565.5,143.4 567.2,139.7 568.9,113.9 570.6,114.4 572.3,117.9 574.0,113.0 575.7,119.1 577.4,144.8 579.1,144.7 580.8,112.4 582.5,103.6 584.2,115.6 585.9,105.4 587.6,120.1 589.3,144.6 591.0,140.7 592.7,112.2 594.4,111.5 596.1,107.2 597.8,116.2 599.5,109.8 601.2,141.7 602.9,151.8 604.7,120.0 606.4,117.8 608.1,114.7 609.8,112.6 611.5,116.5 613.2,137.8 614.9,145.9 616.6,115.3 618.3,110.6 620.0,120.5 621.7,108.9 623.4,110.5 625.1,143.1 626.8,142.5 628.5,115.6 630.2,115.1 631.9,108.9 633.6,112.7 635.3,121.7 637.0,147.7 638.7,140.4 640.4,127.2 642.1,122.6 643.8,118.2 645.6,115.4 647.3,108.5 649.0,142.0 650.7,129.1 652.4,114.2 654.1,111.0 655.8,110.2 657.5,115.8 659.2,110.5 660.9,140.5 662.6,141.8 664.3,118.3 666.0,117.3"/><circle class="dot2" cx="168.4" cy="33.2" r="4.5"/><circle class="dot2" cx="335.4" cy="45.6" r="4.5"/><circle class="dot2" cx="522.9" cy="210.2" r="4.5"/><text class="ink" x="178.6" y="28.5" font-size="11" text-anchor="start">kampanya</text><text class="ink" x="345.6" y="40.9" font-size="11" text-anchor="start">kampanya</text><text class="ink" x="533.1" y="201.8" font-size="11" text-anchor="start">kesinti</text><line class="curve3" stroke-dasharray="4 4" x1="461.5" y1="26" x2="461.5" y2="220"/><text class="dim" x="470.0" y="70.5" font-size="11" text-anchor="start">seviye kayması</text></svg>
  <figcaption>Günlük ziyaret, 2024. Üç turuncu nokta aykırı değer. 2 Eylül'deki kesik çizgi aykırı değer değil: o günden sonra düzey kalıcı olarak yükseliyor.</figcaption>
</figure>

Üç gün, 366 günün %1'inden az. Etkileri:

```python
visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

print(round(visits.mean(), 1), visits.median())      # 4081.1 4002.0
print(round(visits.std(), 1))                        # 914.2
```

Bu üç gün onarılınca standart sapma 914'ten 806'ya iniyor. Daha sinsi olanı:
iki kampanya da perşembeye denk geldi ve perşembe ortalaması 4424 yerine 4621
çıkıyor. Haftalık desen, **yalnızca iki gün yüzünden** yanlış öğreniliyor.

## 8. Aykırı değeri bulmak

**z-skoru.** Ortalamadan kaç standart sapma uzakta:

```python
z = (visits - visits.mean()) / visits.std()
print(z[z.abs() > 3].index.strftime("%m-%d").tolist())
# ['03-14', '06-20', '10-08']
```

Burada üçünü de buldu. Ama bir zayıflığı var: ortalama ve standart sapmanın
**kendisi** aykırı değerlerden etkileniyor. Aykırı gün çoğaldıkça standart sapma
şişiyor ve aykırı günler birbirini gizliyor (**maskeleme**).

**Dayanıklı z-skoru.** Ortalama yerine ortanca, standart sapma yerine **MAD**
(ortancadan mutlak sapmaların ortancası):

```python
median = visits.median()
mad = (visits - median).abs().median()
robust_z = 0.6745 * (visits - median) / mad
```

0.6745 katsayısı, sonucu normal dağılımda z-skoruyla aynı ölçeğe getiriyor.
Ortanca ve MAD birkaç uç değerden etkilenmiyor. Yaygın eşik 3.5.

**Önce yapıyı çıkar.** Ham seride her iki yöntem de trend ve mevsimle
karışıyor: cumartesi "yüksek", Aralık "yüksek". Bu seride 2 Eylül'den sonra
düzey 3917'den 5129'a çıkıyor; ham seriye uygulanan çeyrekler arası aralık
kuralı sonbaharın 20 gününü aykırı sayıyor. Çözüm Bölüm 10'dan: dayanıklı
STL'in **kalıntısına** bak.

```python
from statsmodels.tsa.seasonal import STL

resid = STL(visits, period=7, robust=True).fit().resid
score = 0.6745 * (resid - resid.median()) / (resid - resid.median()).abs().median()
print(score.abs().sort_values(ascending=False).head(5).round(1).tolist())
# [50.0, 46.3, 45.4, 12.9, 5.8]
```

Üç gün 45–50 puanla öbür her şeyden kopuk. Dördüncü sıradaki gün 12.9, sonrası
6'nın altında.

**Eşik bir yargıdır.** 3.5 eşiği burada 30 günü işaretlerdi: gerçek kalıntılar
normal dağılımdan daha kalın kuyrukludur. Sabit bir eşiğe körü körüne güvenme;
puanları **sırala** ve kopmanın nerede olduğuna bak.

## 9. Ne yapmalı?

Aykırı değeri bulmak işin kolay kısmı. Zor olan karar: **bu gerçek mi?**

| Durum | Örnek | İşlem |
|---|---|---|
| Ölçüm ya da kayıt hatası | Kesinti günü 140 ziyaret; sensör −999 | Düzelt: eksik say, doldur |
| Gerçek, tekrar etmeyecek olay | Tek seferlik kampanya | İşaretle; desen öğrenirken düzeltilmiş değeri kullan |
| Gerçek, tekrar edecek olay | Bayram, yılbaşı | Dokunma; olayı modele anlat (Bölüm 18) |
| Kalıcı değişim | 2 Eylül seviye artışı | Aykırı değer değil; değişim noktası (Bölüm 21) |

Düzeltmek = aykırı günü eksik sayıp Kısım 4'teki yöntemle doldurmak:

```python
days = pd.to_datetime(["2024-03-14", "2024-06-20", "2024-10-08"])

clean = visits.astype(float).copy()
clean.loc[days] = float("nan")
both = pd.concat([clean.shift(7), clean.shift(-7)], axis=1).mean(axis=1)
clean = clean.fillna(both)

print(clean.loc[days].tolist())        # [4116.0, 4120.5, 5226.5]
```

İki kural:

- **Satırı silme.** Silmek düzenli aralığı bozar; aykırı gün eksik güne döner
  ve bütün `shift` ve `rolling` hesapları kayar. Değeri değiştir, satırı bırak.
- **Özgün veriyi sakla.** Düzeltilmiş seriyi ayrı bir sütunda tut ve hangi
  günlere dokunduğunu işaretle. Kampanyanın etkisini soran biri çıkacak.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| `isna().sum()` sıfır diye "eksik yok" demek | Satırı olmayan günler görünmüyor | `asfreq` ile düzenli indeks, sonra say |
| Tanımadan `drop_duplicates` | Bölünmüş kayıtların yarısı siliniyor | Yinelenen günlere bak; gerekirse topla |
| Bilinmeyeni sıfırla doldurmak | Toplam ve ortalama çöküyor | Sıfır yalnızca gerçekten sıfırsa |
| Mevsimsel seride `ffill` / `interpolate` | Desen siliniyor | Geçen mevsimin aynı konumu |
| Uzun boşluğu doldurmak | Uydurma veri | Kısa boşlukları doldur, uzunu bırak |
| Doldurulanı işaretlememek | Gerçek ile tahmin ayırt edilemiyor | `was_missing` sütunu |
| Model sınarken geleceğe bakan doldurma | Sızıntı | Yalnızca geriye bakan yöntem |
| Ham seride z-skoru | Mevsim ve trend aykırı sanılıyor | Kalıntıda ara |
| Aykırı günün satırını silmek | Düzenli aralık bozuluyor | Değeri değiştir |
| Seviye kaymasını "düzeltmek" | Gerçek değişim siliniyor | Değişim noktası olarak ele al |

## Özet

- Eksik veri üç hâlde gelir: satır yok, değer boş, boşluk kılık değiştirmiş.
  **Önce `asfreq` ile görünür kıl.**
- Doldurmadan önce **nedenini** sor: gerçek sıfır mı, bilinmeyen mi?
- Mevsimsel seride **mevsimsel doldurma** (geçen haftanın aynı günü) `ffill` ve
  doğrusal doldurmadan kat kat iyi: hata 45'ten 7'ye.
- Kısa boşluğu doldur, uzun boşluğu bırak; doldurduğunu **işaretle**; model
  sınarken geleceğe bakma.
- Aykırı değer ortalamayı, standart sapmayı ve **deseni** bozar.
- Bulmak için **dayanıklı z-skoru** (ortanca ve MAD), mevsimli seride **STL
  kalıntısı** üzerinde. Eşik yerine sıralamaya bak.
- Karar nedene göre: hata → düzelt; tek seferlik olay → işaretle; tekrar eden
  olay → modelle; kalıcı değişim → aykırı değer değil.

Veri artık hazır. Sıradaki bölümde ilk tahminlerini yapıyorsun: en basit
yöntemlerle, çünkü her karmaşık modelin önce onları geçmesi gerekiyor.
