Model kaydının parçaları:

| Parça | Örnek | Ne işe yarar |
|---|---|---|
| Model adı | `churn` | Aynı işi yapan modellerin ailesi |
| Sürüm | `3` | Değişmez, tekrar kullanılmaz |
| Dosya ve özeti | `models/churn-v3.pkl`, `sha256` | Hangi dosya; değişirse anlaşılır |
| Ölçümler | `{"accuracy": 0.818}` | Kapıda karşılaştırma |
| Not | `"more data"` | Bu sürümde ne değişti |
| Etiket (alias) | `production -> 3` | Canlıdaki sürüm |
| Geçmiş | `[["production", 1], ["production", 3]]` | Etiketin sırayla gösterdiği sürümler |

## Yaşam döngüsü

<figure class="fig">
  <div class="flow">
    <span class="node">Eğit</span>
    <span class="arrow">→</span>
    <span class="node">Kaydet</span>
    <span class="arrow">→</span>
    <span class="node acc">Kapı</span>
    <span class="arrow">→</span>
    <span class="node ok">Canlı</span>
  </div>
  <figcaption>Kapıyı geçemeyen sürüm kayıtta kalır ama etiket almaz.</figcaption>
</figure>

## Kapı kuralı

- Aday ve canlıdaki sürüm **aynı** değerlendirme kümesinde ölçülür.
- Aday ancak canlıdakini en az bir eşik (`min_gain`) kadar geçerse
  etiket ona taşınır.
- Kayıtta canlıda hiçbir sürüm yoksa ilk sürüm doğrudan canlıya alınır.

## Geri dönüş

- Etiketi eski sürüme çevir: `set_alias("churn", "production", 1)`.
- Yeni eğitim gerekmez; eski dosya kayıtta duruyor.
- Şartı: eski sürümlerin dosyaları silinmez.

## Terimler

- **Model kaydı** (model registry): modellerin sürümlerini, dosyalarını,
  ölçümlerini ve etiketlerini tutan yer.
- **Etiket** (alias): bir sürüme takılan ad; `production`, `staging`
  gibi.
- **Terfi** (promotion): bir sürümün etiketi alması, örneğin canlıya
  geçmesi.
- **Geri dönüş** (rollback): etiketi önceki sürüme çevirmek.
