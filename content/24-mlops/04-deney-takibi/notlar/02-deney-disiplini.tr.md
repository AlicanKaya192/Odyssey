Kayıt tutmak yetmez; kayıtla doğru karar vermek de gerekir.

## Kazananın laneti

Çok sayıda aday aynı veride ölçülüp en iyisi seçilince, seçilenin skoru
gerçekte olduğundan yüksek görünür. Dersteki ölçüm:

| | Doğrulama | Test |
|---|---|---|
| 20 aynı modelin en iyisinin ortalamadan farkı | +0,028 | +0,009 |

Modeller yalnızca tohumla ayrılıyordu; doğrulamadaki üstünlüğün çoğu
yeni veride kayboldu. Deney sayısı arttıkça bu iyimserlik büyür.

## Kurallar

- Seçim **doğrulamayla**, rapor **testle**.
- Test kümesine seçimden önce bakma. Baktığın an test de doğrulamaya
  dönüşür.
- Deney sayısını kayıtta tut: "200 denemenin en iyisi" ile "3 denemenin
  en iyisi" aynı güveni hak etmez.
- Kötü sonuçları da kaydet; neyin işe yaramadığı da bilgidir.
- Temel çizgiyi her zaman kaydet.
- İki deney yalnızca **tek bir şeyle** ayrılsın; aynı anda iki şey
  değişirse hangisinin işe yaradığı bilinmez.

## Gerçek araçlarda karşılıkları

| Bu bölümde | MLflow |
|---|---|
| `log_run(params, metrics)` | `mlflow.log_param(...)`, `mlflow.log_metric(...)` |
| `runs.jsonl` | `mlruns/` klasörü ya da bir izleme sunucusu |
| Sıralanmış tablo | `mlflow ui` web arayüzü |
| Deney numarası | Çalıştırma kimliği (run ID) |

## Kontrol listesi

- Her deney elle değil, kodun içinden kendiliğinden mi kaydediliyor?
- Ayarların tamamı kayıtta mı? (Kayıtta olmayan bir ayar, yeniden
  üretilemeyen bir deney demek.)
- Test kümesi seçimde hiç kullanılmadı mı?
- Raporlanan sayı test sonucu mu?

## Yapma

- Kayıt dosyasındaki eski satırları değiştirme ya da silme.
- Yalnızca en iyi sonucu kaydetme.
- Deneyleri farklı bölmelerde karşılaştırma; bölmenin şansı farkın
  içine karışır.
