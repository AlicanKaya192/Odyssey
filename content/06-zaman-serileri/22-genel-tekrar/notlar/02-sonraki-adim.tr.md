Bu patika tek bir seriyi sağlam biçimde tahmin etmeyi öğretti. Buradan üç yöne
gidilebilir: daha derine, daha genişe, ya da gerçek bir işe.

## Önce: kendi verinle tekrar et

Öğrenmenin en hızlı yolu, akışı **kendi seçtiğin** bir seride baştan sona
yürütmek. Açık ve uzun seriler:

| Kaynak | Ne var |
|---|---|
| Ulusal istatistik kurumları (TÜİK, Eurostat) | Aylık enflasyon, işsizlik, üretim, turizm |
| Merkez bankaları | Döviz kuru, faiz, para arzı |
| Meteoroloji arşivleri | Saatlik / günlük sıcaklık, yağış |
| Şehir açık veri portalları | Toplu taşıma, trafik, bisiklet, enerji |
| Kendi verin | Adım sayısı, harcama, uyku: küçük ama senin |

Her seride aynı sekiz adım: ham veri → düzenli seri → tanı → taban çizgi →
düzenek → model → aralık → izleme. Bir seriyi bitirmek, on seriye başlamaktan
daha çok öğretir.

## Daha derine: aynı konunun devamı

| Konu | Ne ekler | Nereden başlanır |
|---|---|---|
| Durum-uzay modelleri, Kalman süzgeci | Eksik veriyle doğal çalışan, bileşenleri zamanla değişen modeller | `statsmodels.tsa.statespace`, `UnobservedComponents` |
| ETS ailesi | Üstel düzleştirmenin aralık veren, otomatik seçilen sürümü | `statsmodels` `ETSModel` |
| Otomatik model seçimi | `(p, d, q)` aramasını elle yapmamak | `pmdarima`, `statsforecast` |
| Çoklu mevsimsellik | Saatlik veride günlük + haftalık + yıllık | `MSTL`, TBATS, Fourier |
| Değişim noktası yöntemleri | Çok sayıda kırılmayı birlikte bulmak | `ruptures` |
| Olasılıksal tahmin | Tek aralık yerine bütün dağılım; CRPS ölçüsü | Yüzdelik regresyonu, uyumlu (conformal) aralıklar |

## Daha genişe: bu patikada olmayanlar

| Konu | Hangi soruya cevap verir |
|---|---|
| Küresel modeller | Bin seriyi tek modelle tahmin etmek; kısa seriler birbirinden öğrenir |
| Hiyerarşik tahmin | Mağaza, şehir, ülke tahminlerinin birbirini tutması |
| VAR, eşbütünleşme | Birbirini etkileyen seriler (faiz ile kur) |
| GARCH | Finansal serilerde değişen oynaklık |
| Aralıklı talep | Çoğu gün sıfır olan seriler (yedek parça); Croston yöntemi |
| Derin öğrenme | Çok uzun, çok sayıda seri; N-BEATS, zamansal dönüştürücüler |
| Nedensel etki | "Kampanya olmasaydı ne olurdu?": kesintili zaman serisi, sentetik kontrol |

Kütüphaneler: `statsforecast` (hızlı klasik modeller), `sktime` ve `darts`
(tek arayüzde çok yöntem), `prophet` (takvim etkileri ağır iş serileri).
Hiçbiri uygulamayla birlikte gelmiyor; kendi ortamına kurarsın (Paketler ve
Ortamlar bölümü).

Hangisini kullanırsan kullan, bu patikanın düzeneği değişmez: taban çizgi,
kayan başlangıç, en kötü deney, kalıntı. Yeni bir yöntem mevsimsel naifi 13
deneyde yenemiyorsa, adı ne kadar parlak olursa olsun yenememiştir.

## Gerçek bir işte farklı olanlar

- **Veri geç ve düzeltilerek gelir.** Dünün sayısı yarın değişir. Tahmini
  yaparken elinde **o gün** ne olduğunu sakla; yoksa geçmişe dönük sınamalar
  gerçekte olmayan bir bilgiyle yapılır.
- **Tahmin bir karar içindir.** "MAE kaç?" değil "bu tahminle hangi karar
  verilecek, yanılmanın maliyeti ne?" sorusu yöntemi ve ölçüyü belirler.
- **Basit model yaşar.** Her gece çalışan, bozulduğunda anlaşılan, bir cümleyle
  açıklanan model; %2 daha iyi ama kimsenin anlamadığı modelden değerlidir.
- **İnsanlar tahmine müdahale eder.** Satış ekibi sayıyı elle düzeltir. İki
  sürümü de sakla ve hangisinin daha iyi olduğunu ölç.
- **Seri kendini bozar.** Tahmine göre stok artırılırsa satış da değişir;
  model, kendi etkilediği bir dünyayı tahmin etmeye başlar.

## Odyssey'de sıradaki

Bu patika Makine Öğrenmesi patikasıyla aynı zemini paylaşıyor: özellik tablosu,
doğrulama, sızıntı. Henüz bitirmediysen oraya geç; bitirdiysen Bölüm 19'u bir
kez daha oku, ikisi birbirini tamamlıyor. Matematik patikasındaki olasılık ve
istatistik bölümleri, aralıkların ve testlerin arkasındaki mantığı veriyor.
