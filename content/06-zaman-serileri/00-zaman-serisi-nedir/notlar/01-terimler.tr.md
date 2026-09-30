Patika boyunca bu kelimeler tekrar tekrar geçecek. Parantez içindekiler
İngilizce karşılıkları; kaynaklarda ve kütüphane belgelerinde bu adlarla
karşılaşacaksın.

## Serinin kendisi

| Terim | Anlamı |
|---|---|
| Zaman serisi (time series) | Zamanda sıralanmış ölçümler |
| Zaman damgası (timestamp) | Bir ölçümün yapıldığı an: `2022-01-01` ya da `2024-03-01 14:00` |
| Gözlem (observation) | Tek bir (zaman, değer) çifti; tablodaki bir satır |
| Sıklık (frequency) | İki gözlem arasındaki aralık: saatlik, günlük, aylık |
| Düzenli seri (regular) | Gözlemler eşit aralıklı; her gün için tam bir satır |
| Düzensiz seri (irregular) | Aralıklar eşit değil; olay geldikçe kaydediliyor |
| Tek değişkenli (univariate) | Her zaman damgasında tek bir değer (yalnızca satış) |
| Çok değişkenli (multivariate) | Her zaman damgasında birden fazla değer (satış, fiyat, hava) |

## Desenler

| Terim | Anlamı |
|---|---|
| Trend | Uzun vadeli yön: yukarı, aşağı, düz |
| Mevsimsellik (seasonality) | Sabit uzunlukta, takvime bağlı tekrar |
| Mevsim uzunluğu (period) | Desenin kaç adımda bir tekrarladığı: günlük veride haftalık desen için 7 |
| Döngü (cycle) | Tekrar eden ama uzunluğu sabit olmayan iniş çıkış |
| Gürültü (noise) | Hiçbir desenle açıklanamayan kalan |
| Seviye (level) | Serinin o anki "ortalama yüksekliği" |
| Yapısal kırılma (structural break) | Serinin kuralının bir anda değişmesi |

## Tahmin

| Terim | Anlamı |
|---|---|
| Tahmin (forecast) | Gelecekteki değerlerin kestirimi |
| Ufuk (horizon) | Kaç adım ileriyi tahmin ettiğin: "önümüzdeki 30 gün" için 30 |
| Gecikme (lag) | Geçmişteki bir değer: 1 gün önceki satış 1. gecikme |
| Zamana göre ayırma | Eğitim geçmiş, test gelecek; rastgele ayırmanın yerine |
| Geriye dönük test (backtesting) | Geçmişin farklı noktalarında "o gün tahmin etseydim" diye tekrar tekrar ölçmek |
| Sızıntı (leakage) | Modelin, gerçekte o an bilinmeyen gelecek bilgisini görmesi |

## Sonraki bölümlerde gelecek olanlar

Bunları şimdilik yalnızca adıyla bil; her biri kendi bölümünde anlatılıyor.

| Terim | Nerede |
|---|---|
| Yeniden örnekleme (resampling) | Bölüm 05 |
| Hareketli pencere (rolling window) | Bölüm 07 |
| Ayrıştırma (decomposition) | Bölüm 10 |
| Durağanlık (stationarity) | Bölüm 11 |
| Otokorelasyon (autocorrelation) | Bölüm 12 |
| Üstel düzleştirme (exponential smoothing) | Bölüm 16 |
| ARIMA | Bölüm 17 |
| Tahmin aralığı (prediction interval) | Bölüm 20 |
