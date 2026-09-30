## Üç pencere türü

| Pencere | Neye bakıyor | Yazımı |
|---|---|---|
| Hareketli | Son n satır (ya da son n gün) | `s.rolling(7)`, `s.rolling("7D")` |
| Genişleyen | Baştan bugüne her şey | `s.expanding()` |
| Üstel ağırlıklı | Her şey, ama yeniler daha ağır | `s.ewm(span=7)` |

Üçünde de ardından bir işlem geliyor: `.mean()`, `.sum()`, `.std()`...

## `rolling` parametreleri

| Parametre | Ne yapıyor |
|---|---|
| `window=7` | Pencere boyu, **satır** olarak |
| `window="7D"` | Pencere boyu, **süre** olarak (tarih indeksi gerekir) |
| `min_periods=1` | Pencerede en az bu kadar değer varsa sonuç ver |
| `center=True` | Pencereyi satırın iki yanına yerleştir (geleceği kullanır) |
| `closed="left"` | Süre penceresinde bugünü dışarıda bırak |

`min_periods` varsayılanı: satır penceresinde pencere boyu kadar (o yüzden
baş taraf `NaN`), süre penceresinde 1 (baş taraf dolu ama az gözlemli).

## İşlemler

| İşlem | Verdiği |
|---|---|
| `mean()` | Hareketli ortalama: düzleştirme |
| `sum()` | Hareketli toplam: "son 7 günün satışı" |
| `std()`, `var()` | Hareketli oynaklık |
| `min()`, `max()` | Pencerenin en düşük / en yükseği |
| `median()` | Aykırı değere dayanıklı düzleştirme |
| `quantile(0.9)` | Pencerenin %90'lık değeri |
| `count()` | Pencerede kaç geçerli değer var |
| `corr(other)` | İki serinin hareketli korelasyonu |
| `apply(fonksiyon)` | Kendi hesabın (yavaş) |

```python
s.rolling(7).apply(lambda x: x.max() - x.min())     # pencere araligi
s.rolling(90).corr(other)                           # iliski zamanla degisiyor mu
```

## Pencere boyu

| Veri | Bastırılacak desen | Pencere |
|---|---|---|
| Saatlik | Günlük | 24 |
| Saatlik | Haftalık | 168 |
| Günlük | Haftalık | 7 |
| Günlük | Yıllık | 365 |
| İş günü | Haftalık | 5 |
| Aylık | Yıllık | 12 |
| Çeyreklik | Yıllık | 4 |

**Çift sayılı pencere ve ortalama.** 12 aylık ortalanmış pencerenin tam bir
ortası yok (6. ile 7. ayın arası). Klasik çözüm önce 12'lik, sonra 2'lik
ortalama almak (2×12 hareketli ortalama); böylece pencere bir aya tam
oturuyor. Bölüm 10'daki ayrıştırma bunu kendisi yapıyor.

## Gecikme

Geriye dönük n'lik ortalama, yaklaşık **(n - 1) / 2** adım öncesinin durumunu
gösteriyor:

| Pencere | Gecikme |
|---|---|
| 7 | 3 gün |
| 28 | 13–14 gün |
| 365 | yaklaşık 6 ay |

Pencere büyüdükçe seri sakinleşiyor **ve** dönüm noktaları daha geç
görülüyor. İkisini birden iyileştiren bir pencere yok; bu bir tercih.

## Özellik kurarken

```python
past = s.shift(1)                          # dunden geriye

features = pd.DataFrame({
    "mean_7": past.rolling(7).mean(),
    "mean_28": past.rolling(28).mean(),
    "std_7": past.rolling(7).std(),
    "max_7": past.rolling(7).max(),
    "ewm_7": past.ewm(span=7).mean(),
})
```

Bütün pencereler `shift(1)`'den sonra kuruluyor. h adım ileriyi tahmin
edeceksen `shift(h)`: tahmin anında bilinen en son değer h adım önceki.

## Güvenli mi? Hızlı kontrol

| İfade | Geleceği kullanıyor mu |
|---|---|
| `s.rolling(7).mean()` | Hayır, ama **bugünü** içeriyor |
| `s.shift(1).rolling(7).mean()` | Hayır |
| `s.rolling(7, center=True).mean()` | **Evet**: 3 gün ileri |
| `s.expanding().mean()` | Hayır, bugünü içeriyor |
| `s.ewm(span=7).mean()` | Hayır, bugünü içeriyor |
| `s.rolling(7).mean().shift(-3)` | **Evet**: ortalanmış pencereyle aynı |
| `(s - s.mean()) / s.std()` | **Evet**: bütün serinin ortalaması geleceği içerir |

Son satır çok kaçıyor: bütün serinin ortalaması ve standart sapmasıyla
ölçeklemek, gelecekteki değerleri bugünün satırına sızdırıyor. Yerine
`expanding` ya da `rolling` ile hesaplanan ortalama.

## Eksikli ve düzensiz seride

```python
s.rolling("7D").mean()                   # son 7 gunun ortalamasi, kac kayit varsa
s.rolling("7D").count()                  # o pencerede kac kayit var
s.rolling("7D", min_periods=7).mean()    # 7 kayit yoksa NaN
s.rolling("24h").mean()                  # saatlik / duzensiz veride son 24 saat
```

Süre penceresi `center=True` ile kullanılamıyor ve indeksin sıralı olması
gerekiyor.
