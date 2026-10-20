Bir modeli sunan servisi yayına almadan önce:

## Kontrol listesi

- Model dosyası kayıttaki sürümle aynı mı (özet tutuyor mu)?
- `requirements.txt`'teki kütüphane sürümleri eğitimdekiyle aynı ve
  `==` ile sabit mi?
- Model açılışta mı yükleniyor? İlk istek modeli yükletmiyor mu?
- Girdi doğrulaması eğitimdeki şemayla aynı kuralları mı kullanıyor?
- Özellik kodu eğitimdekiyle **aynı dosyadan** mı geliyor?
- `/health` model sürümünü söylüyor mu?
- Cevaplarda ve toplu sonuç dosyalarında model sürümü var mı?
- Hız sözü p95 üzerinden mi verildi, ölçüldü mü?
- İmaj kök olmayan bir kullanıcıyla mı çalışıyor?
- Geri dönüş yolu belli mi? (Bir önceki imaj etiketi ya da kayıttaki
  bir önceki sürüm.)

## İki paketleme yolu

| | Model imajın içinde | Model açılışta kayıttan |
|---|---|---|
| İmaj etiketi | Model sürümünü taşır (`churn-api:3`) | Kodu taşır |
| Model değişince | Yeni imaj derlenir | Etiket değişir, imaj aynı |
| Açılış | Dış bağımlılık yok | Kayda ve ağa bağlı |
| Geri dönüş | Eski imaja dön | Etiketi eski sürüme çevir |

## Yapma

- Modeli istek başına yükleme.
- Eğitim ve sunma için özellik kodunu iki kez yazma; iki kopya er geç
  ayrışır.
- Hızı ortalamayla raporlama.
- Model sürümü olmayan tahmin kaydetme; sonradan hangi modelin karar
  verdiği bilinmez.
