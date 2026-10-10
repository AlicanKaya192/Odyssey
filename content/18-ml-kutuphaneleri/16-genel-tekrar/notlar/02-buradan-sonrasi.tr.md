Bu modül tablo verisinde bir modelin bütün yolunu kütüphanelerle gösterdi.
Buradan sonrası birkaç yöne açılıyor.

## Bu programda

| Patika / modül | Bu modülün hangi kısmı |
|---|---|
| Makine Öğrenmesi | kavramların kendisi: doğrulama, aşırı öğrenme, dengesiz veri |
| ML Algoritmaları | burada kullanılan modelleri NumPy ile sıfırdan yazmak |
| Zaman Serileri | `TimeSeriesSplit`, statsmodels; zamanda doğrulama |
| FastAPI ile REST API | kaydedilen modeli bir API'nin arkasına koymak |
| Docker | modeli ve ortamını sabit sürümlerle paketlemek |
| Büyük Veri | belleğe sığmayan veride özellik hazırlamak |

## Programın dışında

- **Derin öğrenme:** resim, ses ve metin gibi yapısız veride sinir ağları
  (PyTorch, TensorFlow). Tablo verisinde çoğu zaman boosting daha iyi ya da
  eşit; yapısız veride sinir ağları önde.
- **Diğer boosting kütüphaneleri:** XGBoost ve CatBoost, LightGBM ile aynı
  aileden; scikit-learn arayüzleri neredeyse aynı.
- **Model açıklama:** SHAP gibi kütüphaneler tek bir tahminin hangi
  sütunlardan geldiğini ayrıştırır; permütasyon önemi ve ICE'ın devamı.
- **Model izleme:** yayına çıkan model zamanla bozulur (veri değişir);
  tahminlerin ve girdilerin dağılımı izlenir, gerektiğinde yeniden eğitilir.

## Kendi başına

- scikit-learn'ün "User Guide" belgesi her sınıfın ne zaman işe yaradığını
  örneklerle anlatır; bu modülde anlatılmayan birçok aracı içerir.
- Kendi verinle bu modülün yolunu baştan sona yürü: ayır, hazırla,
  doğrula, ara, eşik seç, test et, açıkla, kaydet. Hızlı Başvuru notundaki on
  adım o yolun listesi.
