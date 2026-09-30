Patikanın kalanında bu terimler sürekli geçecek. İngilizceleri parantez içinde:
kütüphane belgelerinde ve hata mesajlarında onları göreceksin.

## Veri

| Terim | Anlamı |
|---|---|
| Eğitim verisi (train) | Modelin gördüğü geçmiş |
| Test verisi (test, holdout) | Tahminle karşılaştırmak için saklanan son dönem |
| Doğrulama verisi (validation) | Model ve ayar seçerken kullanılan ara dönem; test en sona saklanır |
| Başlangıç (origin) | Eğitim verisinin son anı; tahminin yapıldığı an |
| Ufuk (horizon, `h`) | Kaç adım ileriye tahmin edildiği |
| Adım (step) | Verinin bir sıklık birimi: bir gün, bir ay |

## Tahmin türleri

| Terim | Anlamı |
|---|---|
| Nokta tahmini (point forecast) | Tek bir sayı: "yarın 310" |
| Aralık tahmini (prediction interval) | Bir aralık ve olasılık: "%95 olasılıkla 280–340" (Bölüm 20) |
| Tek adımlı (one-step) | Yalnızca bir sonraki adım |
| Çok adımlı (multi-step) | Aynı başlangıçtan birden çok adım |
| Örnek içi (in-sample) | Modelin eğitildiği dönemdeki uyumu |
| Örnek dışı (out-of-sample) | Modelin görmediği dönemdeki tahmini; asıl ölçü bu |

Örnek içi hata her zaman iyimserdir: model o veriyi zaten görmüştür. Bir
modelin başarısı yalnızca **örnek dışı** hatayla ölçülür.

## Çok adımlı tahminin iki yolu

**Özyinelemeli (recursive).** Bir adım tahmin et, o tahmini veri sayıp bir
sonrakini tahmin et. Hatalar birikir ama tek model yeter. Mevsimsel naifin
haftalık zinciri bunun en basit hâli.

**Doğrudan (direct).** Her ufuk için ayrı bir kural ya da model: "7 gün sonrası"
için bir tane, "14 gün sonrası" için bir tane. Hata birikmez ama çok model
gerekir. Bölüm 19'da ikisini de kuracaksın.

## Hata

| Terim | Tanım | Ne söyler |
|---|---|---|
| Hata (error) | gerçek − tahmin | Tek bir adımın sapması |
| Kalıntı (residual) | gerçek − örnek içi uyum | Modelin eğitim verisindeki sapması |
| MAE | Mutlak hataların ortalaması | Tipik sapma, serinin biriminde |
| Yanlılık (bias) | Hataların ortalaması | Sistematik kayma ve yönü |
| Beceri (skill) | 1 − MAE / temel MAE | Temel yönteme göre kazanç |

İşaret kuralı: **hata = gerçek − tahmin**. Artı hata: tahmin düşük kalmış.
Bazı kaynaklar tersini kullanır; bir raporu okurken hangisi olduğuna bak.

Kalıntı ile hata aynı şey değil: kalıntı modelin **gördüğü** veride, hata
**görmediği** veride. Kalıntılar küçükken hatalar büyükse model ezberlemiştir.

## Sızıntı (leakage)

Tahmin anında bilinemeyecek bir bilginin modele ulaşması. Zaman serisinde en
sık yolları:

- Eğitim ve testi rastgele ayırmak.
- Ortalama, ölçek, büyüme oranı gibi sayıları bütün veriden hesaplamak.
- `center=True` pencere, `shift(-k)`, `interpolate`, `bfill`: hepsi geleceğe
  bakar.
- `rolling`'den önce `shift(1)` koymamak.
- Tahmin anında henüz yayınlanmamış bir dış değişkeni kullanmak (Bölüm 18).

Sızıntının işareti: inanılmayacak kadar iyi bir test hatası. Bir sonuç fazla
iyiyse önce sızıntı ara.

## Geriye dönük sınama (backtesting)

Modeli geçmişte birçok farklı başlangıç noktasından çalıştırıp her birinde
tahminini gerçekle karşılaştırmak. Tek bir eğitim/test ayrımı yerine onlarca;
sonuç şansa çok daha az bağlı. Bölüm 15'in ana konusu.

## Temel yöntem (baseline, benchmark)

Hiçbir şey öğrenmeden üretilen basit tahmin: ortalama, naif, mevsimsel naif,
kayma. Her modelin karşılaştırılacağı **çıta**.
