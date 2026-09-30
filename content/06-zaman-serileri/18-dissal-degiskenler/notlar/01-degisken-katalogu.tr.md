## Takvim değişkenleri

Geleceği kesin bilinir; tahmin anında hazırdır.

```python
X = pd.DataFrame(index=index)

X["weekend"] = (index.dayofweek >= 5).astype(int)
X["month_end"] = index.is_month_end.astype(int)
X["payday"] = index.day.isin([1, 15]).astype(int)
X["holiday"] = index.isin(holiday_dates).astype(int)
```

| Değişken | Ne için |
|---|---|
| Hafta sonu / haftanın günü | Haftalık desen (mevsimsel model kullanmıyorsan) |
| Ayın günü, ay sonu, maaş günü | Ay içi desen: kira, fatura, maaş |
| Resmi tatil | Tek günlük kırılma |
| Tatil öncesi / sonrası | Alışveriş telaşı, köprü günleri |
| Okul dönemi, sezon açılışı | Uzun süren rejimler |
| Ay ya da Fourier terimleri | Yıllık desen |

**Tatil penceresi.** Etki çoğu zaman tatilin kendisiyle sınırlı değildir:

```python
holiday = pd.Series(index.isin(holiday_dates).astype(int), index=index)
X["holiday"] = holiday
X["before_holiday"] = holiday.shift(-1, fill_value=0)     # tatilden bir gun once
X["after_holiday"] = holiday.shift(1, fill_value=0)       # tatilden bir gun sonra
```

Burada `shift(-1)` sızıntı **değil**: tatil takvimi önceden bilinir.

**Kayan tatiller.** Dini bayramlar her yıl yaklaşık 11 gün geriye kayar; "ayın
günü" ya da mevsim bileşeni onları yakalayamaz. Açık bir tatil listesi gerekir.

**Her tatil aynı değildir.** Tek bir `holiday` sütunu bütün tatillere aynı
etkiyi verir. Veri yetiyorsa türlere ayır: `religious`, `national`, `new_year`.

## Kukla değişken tuzağı

Bir kategorinin bütün değerleri için ayrı sütun açıp (haftanın 7 günü) modelde
sabit de tutarsan sütunlar birbirini tam olarak belirler ve model kurulamaz.
Birini dışarıda bırak (6 sütun); o, karşılaştırma tabanı olur.

Aynı nedenle: **mevsimsel fark ile mevsim kuklaları birlikte kullanılmaz.**
`seasonal_order=(0, 1, 1, 7)` varken haftanın günü kuklaları eklemek aynı
bilgiyi iki kez vermektir.

## Fourier terimleri

```python
def fourier(index, K, period=365.25):
    day = index.dayofyear.to_numpy()
    columns = {}
    for k in range(1, K + 1):
        columns[f"sin{k}"] = np.sin(2 * np.pi * k * day / period)
        columns[f"cos{k}"] = np.cos(2 * np.pi * k * day / period)
    return pd.DataFrame(columns, index=index)
```

| `K` | Sütun | Şekil |
|---|---|---|
| 1 | 2 | Tek yumuşak dalga |
| 2 | 4 | İki kıvrım; asimetrik tepe |
| 3 | 6 | Daha keskin ayrıntılar |
| 6+ | 12+ | Neredeyse her ayın kendi düzeyi; ezber riski |

- Sinüs ve kosinüs **birlikte** gelir: ikisi dalganın hem boyunu hem kaymasını
  belirler.
- Saatlik veride günlük desen için `period=24` ve saat; haftalık için
  `period=168`.
- Keskin, kısa süren etkileri (yılbaşı haftası) Fourier yakalayamaz; onlar için
  ayrı bir sütun.
- `K`'yi kayan başlangıçla seç. Bu seride `K = 3` hatayı **kötüleştirdi**.

## Planlanan değişkenler

| Değişken | Biçim | Not |
|---|---|---|
| Kampanya | 0 / 1 | Süresi ve türü farklıysa ayrı sütunlar |
| İndirim oranı | Sayı (0.20) | Etki doğrusal olmayabilir |
| Fiyat | Sayı; çoğu zaman `log` | Satış da `log` ise katsayı esnekliktir |
| Reklam harcaması | Sayı; gecikmeli etkili | `shift(1)`, `shift(2)` ya da hareketli toplam |
| Stok / kapasite | Üst sınır | Satış talebi değil, **satılabileni** gösterir |

Planlanan değişkenin geleceğini sen yazarsın; bu, **senaryo** sormayı mümkün
kılar: "kampanyayı yapmazsak ne olur?" için aynı modeli `promo = 0` ile çalıştır.

## Ölçülen değişkenler

| Değişken | Gelecek için ne kullanılır |
|---|---|
| Sıcaklık (uzun ufuk) | Mevsim normali |
| Sıcaklık (1–7 gün) | Hava tahmini servisi; eğitimde de **tahmini** kullan |
| Döviz kuru, fiyat endeksi | Son değer (rastgele yürüyüş) |
| Rakip fiyatı, trafik | Gecikmeli değer: `shift(h)` |

**Eğitim ile tahmin aynı türden olmalı.** Eğitimde gerçek sıcaklığı, tahminde
hava tahminini kullanırsan model, elindekinden daha güvenilir bir değişkene göre
ayarlanmış olur. Mümkünse eğitimde de o günkü hava **tahminini** kullan.

## Gecikmeli dış değişken

Bilinmeyen bir değişkeni sızıntısız kullanmanın yolu:

```python
X["temp_lag1"] = temp.shift(1)       # dunku sicaklik: 1 adimlik tahminde bilinir
X["temp_lag7"] = temp.shift(7)       # 7 adimlik tahminde de bilinir
```

Kural: `h` adım ilerisini tahmin ediyorsan değişken en az `h` adım gecikmeli
olmalı. 28 günlük ufukta `shift(1)` hâlâ sızıntıdır.

## Hangi değişken, tahmin anında hazır mı?

| Değişken | Hazır mı |
|---|---|
| Haftanın günü, ay, tatil, Fourier | Evet |
| Kampanya takvimi, fiyat listesi | Evet (plan değişmezse) |
| Dünkü satış, dünkü sıcaklık | Yalnızca 1 adımlık tahminde |
| Bugünkü müşteri sayısı, bugünkü sıcaklık | Hayır |
| Gelecek haftanın hava tahmini | Evet, ama hatalı; eğitimde de tahmini kullan |
