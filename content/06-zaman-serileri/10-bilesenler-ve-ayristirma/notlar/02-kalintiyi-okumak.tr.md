Kalıntı "çöp" değil, **teşhis aracı**. İyi bir ayrıştırmada kalıntı sıkıcıdır:
sıfırın etrafında, desensiz, her dönemde aynı genişlikte. Sıkıcı değilse sana
bir şey söylüyor.

## Beş soru

```python
r = seasonal_decompose(s, model="additive", period=7)
e = r.resid.dropna()
```

**1. Ortalaması sıfır mı?**

```python
print(round(e.mean(), 3))
```

Toplamsal modelde sıfıra, çarpımsalda 1'e çok yakın olmalı. Değilse trend
düzeyi kaçırmış.

**2. Takvime göre desen var mı?**

```python
print(e.groupby(e.index.dayofweek).mean().round(1).tolist())
print(e.groupby(e.index.month).mean().round(1).tolist())
```

Bütün gruplar sıfıra yakın olmalı. Belirli bir gün ya da ay sürekli artı ya da
eksi çıkıyorsa ayrılmamış bir mevsim var: periyot yanlış ya da ikinci bir
periyot gerekiyor.

**3. Genişliği zamanla değişiyor mu?**

```python
print(e.abs().groupby(e.index.year).mean().round(1).tolist())
```

Yıldan yıla büyüyorsa (ya da yolcu serisindeki gibi uçlarda büyük, ortada
küçükse) model toplamsal ama seri çarpımsal.

**4. Komşu günler birbirine benziyor mu?**

```python
print(round(e.corr(e.shift(1)), 2))
```

Sıfıra yakın olmalı. Yüksekse kalıntıda hâlâ kullanılabilir bilgi var: dünün
sürprizi bugünü haber veriyor. Bölüm 12 (otokorelasyon) bu sorunun tam hâli ve
ARIMA'nın çıkış noktası.

**5. Uç değerler hangi günler?**

```python
print(e.abs().sort_values(ascending=False).head(5))
```

Bunlar olaylar: kampanya, tatil, kesinti, veri hatası. Takvimle karşılaştır
(Bölüm 04'teki tatil listesi). Aynı tarih her yıl çıkıyorsa o bir olay değil,
ayrılmamış bir mevsim.

## Belirtiden teşhise

| Kalıntıda ne görüyorsun | Ne demek | Ne yap |
|---|---|---|
| Yavaş dalga | Trend fazla katı ya da ikinci bir mevsim | Daha kısa trend penceresi; MSTL |
| Belirli günlerde hep aynı işaret | Ayrılmamış mevsim | `period`'u düzelt, ikinci periyot ekle |
| Genişlik düzeyle büyüyor | Çarpımsal yapı | `model="multiplicative"` ya da logaritma |
| Tek tek büyük sıçramalar | Olaylar | `robust=True`; olayları işaretle (Bölüm 13, 21) |
| Sıçramanın çevresinde ters işaretli kalıntılar | Aykırı değer trendi çekmiş | `STL(..., robust=True)` |
| Bir tarihten sonra hep artı | Seviye kayması | Değişim noktası (Bölüm 21) |
| Komşu günler benzer | Kalan bağımlılık | Modellenebilir: Bölüm 12 ve 17 |

## Kalıntıyla olağandışı gün aramak

Bölüm 07'deki hareketli z-skoru ham seriye bakıyordu; haftalık desen güçlüyse
her cumartesi biraz "olağandışı" çıkıyordu. Kalıntıda desen zaten çıkarılmış:

```python
fit = STL(s, period=7, robust=True).fit()
z = (fit.resid - fit.resid.mean()) / fit.resid.std()
unusual = z[z.abs() > 3]
```

`robust=True` burada şart: yoksa aykırı günün kendisi trendi ve mevsimi
bozuyor, kendi kalıntısını küçültüyor. Bölüm 21 bu fikri sonuna kadar götürüyor.

## Ayrıştırma bir tahmin değil

Ayrıştırma **geçmişi** açıklıyor. Geleceğe uzatmak için her bileşeni ayrı
düşünmek gerekiyor:

- **Mevsim**: tekrar ediyor; bir sonraki haftaya aynen kopyalanabilir.
- **Trend**: uzatılması gerekiyor; nasıl uzatılacağı bir model seçimi.
- **Kalıntı**: tanım gereği öngörülemeyen kısım; belirsizliğin boyunu veriyor.

Bölüm 14'teki temel tahminler ve Bölüm 16'daki üstel düzleştirme tam olarak bu
üç bileşeni ileri taşımanın yolları.
