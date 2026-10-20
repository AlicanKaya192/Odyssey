**Kendi projende ilk MLOps hattı**

1. Eğitimi tek bir betiğe al: tohum, ayarlar ve verinin özeti bir kayda
   yazılsın. Aynı ayarla iki kez çalıştırıp aynı sonucu gör.
2. Veriye şema yaz; eğitimden önce denetle.
3. Bir temel çizgi ve basit bir kapı kur: yeni model onu geçmeden
   kaydedilmesin.
4. Modeli sun ve her tahmini sürümüyle kaydet.
5. Etiketler gelince doğruluğu ölç; kaymayı her gün ölç.
6. Hattı bir iş akışına bağla: takvimle ve elle.

Her adımdan sonra hattın gerçekten durduğunu görmek için bir şeyi bilerek
boz (bir sütunu kaydır, tohumu kaldır): durmayan kapı kapı değildir.

**Bu modülde kendimiz yazdıklarımız**

Her parçayı birkaç satırla kurduk; gerçek projelerde aynı işleri hazır
araçlar yapar:

| Bizim yazdığımız | Hazır araçlara örnek |
|---|---|
| İçerik adresli depo ve işaret dosyası | DVC |
| Deney kaydı ve model kaydı | MLflow |
| Şema denetimi | pandera |
| Özellik deposu | Feast |
| İzleme ve uyarı | Prometheus, Grafana |

Araçların sürümleri ve ayrıntıları zamanla değişir; kurarken kendi
belgelerine bakılır. Ama neye baktıkları bu modülde ölçtüğün şeyler.

**Odyssey'de buradan nereye?**

- **CI/CD ve DevOps:** bu modülün hatlarının dayandığı iş akışları.
- **Docker:** modeli bir imaja koymak ve aynı ortamda çalıştırmak.
- **FastAPI ile REST API Yazmak:** modeli sunan servisi derinlemesine
  kurmak.
- **Büyük Veri:** eğitim verisi bir bilgisayara sığmadığında.

**Pratik öneriler**

1. Bitirme hattını kendi küçük veri setinle kur.
2. Her ay hattın satırını oku; `kept out` ve `data rejected` satırlarının
   nedenini yaz.
3. Tasarım belgesini koddan önce yaz; eşikleri oradan al.
4. Yeni bir eşik koyarken önce gürültüyü ölç.
