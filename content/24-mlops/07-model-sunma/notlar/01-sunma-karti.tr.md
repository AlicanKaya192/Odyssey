| | Toplu tahmin | Anlık tahmin |
|---|---|---|
| Ne zaman | Belli aralıklarla (her gece) | İstek gelince |
| Sonuç | Bir tablo ya da dosya | API cevabı |
| Hız ihtiyacı | Saatler kabul | Milisaniyeler |
| Altyapı | Zamanlanmış bir betik | Sürekli açık bir servis |
| Örnek | Sabah aranacak müşteri listesi | İptal sayfasında teklif |

## Sunmanın kuralları

- Model program **açılırken** bir kez yüklenir; istekler aynı nesneyi
  kullanır. Dersteki ölçüm: 100 istekte yeniden yükleyen yol 100, bir
  kez yükleyen yol 1 yükleme yaptı.
- Yüklemeden önce dosyanın özeti kayıttakiyle karşılaştırılır.
- Girdi eğitimdeki kurallarla denetlenir; kurala uymayan istek `422`.
- Eğitim ve sunma **aynı** özellik kodunu kullanır.
- Her tahminin yanında model sürümü yazılır: cevapta, dosyada, kayıtta.
- `/health` model sürümünü de söyler.

## Gecikme yüzdelikleri

| Ölçü | Anlamı |
|---|---|
| Ortalama | Yavaş istekler onu çeker; kimsenin yaşamadığı bir sayı olabilir |
| p50 (ortanca) | İsteklerin yarısı bundan hızlı |
| p95 | İsteklerin %95'i bundan hızlı |
| p99 | İsteklerin %99'u bundan hızlı |

Sıra yöntemi (nearest rank): değerleri sırala, `ceil(p / 100 × n)`'inci
elemanı al. Dersteki 20 gecikmede p50 = 13 ms, p95 = 90 ms, ortalama
28,95 ms.

## Terimler

- **Sunmak** (serving): tahminleri kullanılacağı yere ulaştırmak.
- **Toplu tahmin** (batch prediction): çok satırı bir kerede, belli
  aralıklarla puanlamak.
- **Anlık tahmin** (online prediction): gelen isteğe hemen cevap vermek.
- **Gecikme** (latency): bir isteğin cevabının gelme süresi.
- **Yüzdelik** (percentile): değerlerin belli bir yüzdesinin altında
  kaldığı sınır.
