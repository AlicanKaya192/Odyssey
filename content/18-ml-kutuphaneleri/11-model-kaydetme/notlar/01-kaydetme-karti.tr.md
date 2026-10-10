## Yazımlar

| Yazım | Ne yapar |
|---|---|
| `joblib.dump(obj, "m.joblib")` | nesneyi (model, sözlük) kaydeder |
| `joblib.dump(obj, "m.joblib", compress=3)` | sıkıştırarak kaydeder |
| `joblib.load("m.joblib")` | geri yükler; **içindeki kodu çalıştırabilir** |
| `model.feature_names_in_` | eğitimdeki sütun adları |
| `sklearn.__version__` | şu anki sürüm |
| `InconsistentVersionWarning` | başka sürümde kaydedilmiş dosya |
| `warnings.simplefilter("error", InconsistentVersionWarning)` | sürüm farkında dur |

## Modelin yanına

| Anahtar | Neden |
|---|---|
| `"model"` | pipeline'ın tamamı (ön işleme dahil) |
| `"sklearn"`, `"python"` | yüklenecek ortamın sürümü |
| `"columns"` | beklenen sütunlar ve sırası |
| `"threshold"` | seçilen karar eşiği (`predict` 0,5 kullanır) |
| `"cv_auc"` ya da başka skor | hangi başarıyla kaydedildiği |
| `"trained_at"`, `"data"` | ne zaman, hangi veriyle |

## Kontrol listesi

- Kaydedilen şey pipeline mı? Ön işleme ayrı kaldıysa yüklenen model ham
  veriyle yanlış çalışır.
- Ortamın sürümleri bir `requirements.txt` dosyasına sabitlendi mi?
- Tahminden önce `new[bundle["columns"]]` ile sıralanıyor mu?
- Dosya güvenilir bir yerden mi geliyor?
- Yüklenen modelle birkaç bilinen satırın tahmini, kaydetmeden önceki
  tahminlerle aynı mı?
