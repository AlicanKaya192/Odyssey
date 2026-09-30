## Basit getiri ve logaritmik getiri

```python
r = close.pct_change()            # basit getiri
log_r = np.log(close).diff()      # logaritmik getiri
```

| | Basit getiri | Logaritmik getiri |
|---|---|---|
| Tanım | `P1 / P0 - 1` | `ln(P1 / P0)` |
| Okunuşu | Doğrudan yüzde | Küçük değerlerde yüzdeye çok yakın |
| Zamanda birikim | **Çarpılır**: `(1 + r).cumprod()` | **Toplanır**: `log_r.cumsum()` |
| Simetri | %10 artış + %10 düşüş ≠ 0 | +0.0953 ve -0.0953 tam olarak sıfırlanır |
| Ne zaman | Raporlama, insanlara anlatma | Modelleme, istatistik |

Küçük değişimlerde ikisi neredeyse aynı: %1'lik basit getiri 0.00995 log
getiri. Fark büyüdükçe açılıyor: %50'lik artış 0.405, %50'lik düşüş -0.693.

## Neden toplanmıyor?

| Gün | Fiyat | Basit getiri | Log getiri |
|---|---|---|---|
| 0 | 100 | — | — |
| 1 | 110 | +%10 | +0.0953 |
| 2 | 99 | -%10 | -0.1054 |
| Toplam | | %0 (yanlış) | -0.0101 → %-1.0 (doğru) |

Fiyat 100'den 99'a indi: gerçek değişim %-1. Basit getirilerin toplamı sıfır
diyor. İkinci günün %10'u daha büyük bir tabandan (110) hesaplandığı için iki
yüzde aynı büyüklükte değil.

Log getiriden basit getiriye dönüş: `np.exp(toplam) - 1`.

## Birikimli getiri

```python
cumulative = (1 + r).cumprod() - 1            # her gun, bastan o gune getiri
total = (1 + r).prod() - 1                    # tek sayi
same = close.iloc[-1] / close.iloc[0] - 1     # ayni sey
```

## 100 tabanlı endeks

Farklı düzeydeki serileri aynı grafikte karşılaştırmanın yolu, hepsini aynı
noktadan başlatmak:

```python
index = close / close.iloc[0] * 100
```

İlk gün 100; 166.1 yazan gün, başlangıca göre %66.1 yukarıda demek. 50
liralık ve 5000 liralık iki hisse artık yan yana okunabiliyor.

Taban başka bir tarih de olabilir: `close / close.loc["2024-01-02"] * 100`.
Hangi tarihi taban seçtiğin grafiğin hikâyesini değiştiriyor; seçimi
gerekçelendir.

## Yıllık bileşik büyüme

Birkaç yıllık bir değişimi "yılda ortalama yüzde kaç" diye özetlemek için:

```python
years = (close.index[-1] - close.index[0]).days / 365.25
cagr = (close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1
```

Üç yılda %66 büyüme yılda %22 değil, yaklaşık **%18**: büyüme her yıl bir
öncekinin üstüne biniyor. Toplamı yıl sayısına bölmek bileşik etkiyi
görmezden geliyor.

## Tepeden düşüş

Bir serinin bugüne kadarki en yüksek noktasına göre ne kadar aşağıda olduğu:

```python
peak = close.cummax()
drawdown = close / peak - 1          # 0 ya da eksi
worst = drawdown.min()               # en derin dusus
```

`cummax` her güne o güne kadar görülen en yüksek değeri yazıyor. Geleceğe
bakmıyor; bu yüzden her gün için o gün bilinen bilgiyle hesaplanabiliyor.

## Birikim ve karşılaştırma

```python
ytd = s.groupby(s.index.year).cumsum()                    # her yil sifirdan baslar
share = s.groupby(s.index.year).cumsum() / s.groupby(s.index.year).transform("sum")
```

İlki her yılı kendi içinde biriktiriyor; ikincisi "yılın yüzde kaçı
tamamlandı" sorusunu cevaplıyor. İki yılı gün numarasına (`dayofyear`) göre
yan yana koymak hangisinin önde gittiğini gösteriyor.

## Getirilerin özellikleri

Fiyat serilerinde tekrar tekrar karşına çıkacak üç gözlem:

- **Fiyat düzeyi çok kalıcı, getiri değil.** Bugünün fiyatı dünün fiyatına
  0.99 bağlı; bugünün getirisi dünün getirisine neredeyse hiç bağlı değil.
- **Oynaklık kümeleniyor.** Büyük değişimleri büyük değişimler izliyor; sakin
  dönemler sakin kalıyor. Getirinin **büyüklüğü** getirinin kendisinden daha
  tahmin edilebilir.
- **Uç değerler beklenenden sık.** Günlük getirilerin dağılımı çan eğrisinden
  daha kalın kuyruklu.

Bu yüzden fiyat serilerinde düzeyi değil, getiriyi modellemek standart
yaklaşım.
