## Ayarlar

| Ayar | Ne değiştirir | scikit-learn |
|---|---|---|
| `k` | küçük: karmaşık sınır; büyük: düz sınır | `n_neighbors` |
| Ağırlık | eşit oy ya da `1 / uzaklık` | `weights="uniform"` / `"distance"` |
| Uzaklık | Öklid, Manhattan, kosinüs… | `metric` |
| Arama yapısı | kaba kuvvet, KD-ağacı, top ağacı | `algorithm` |

## Maliyet

- Eğitim: yok (veriyi saklamak).
- Tahmin: kaba kuvvette sorgu başına `O(n · d)`; KD-ağacı az boyutta
  hızlandırır, çok boyutta faydası kaybolur.
- Bellek: bütün eğitim verisi.

## Ne zaman iyi, ne zaman kötü?

- İyi: az boyut, yerel yapısı olan veri, sınırı düzensiz problemler, hızlı
  bir taban çizgisi.
- Kötü: çok boyut (boyut laneti), çok büyük veri (tahmin yavaş), ölçeği
  karışık özellikler (önce standartlaştır).

## Sık hatalar

- Standartlaştırmayı unutmak: büyük birimli özellik uzaklığı yönetir.
- `k`'yı eğitim doğruluğuyla seçmek: `k = 1` hep kusursuz görünür.
- İki sınıfta çift `k`: oylar eşit kalabilir; tek sayı seçmek eşitliği azaltır.
