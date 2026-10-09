ML Algoritmaları modülünde klasik makine öğrenmesinin çekirdeğini kurdun. Buradan birkaç yol
açılıyor:

- **Derin öğrenme.** Bölüm 20'deki ağın aynısı, daha çok katmanla. PyTorch ya
  da TensorFlow türevleri otomatik hesaplar (autograd); senin yazdığın
  `backward` fonksiyonunu kütüphane yazar. Görüntü için evrişimli ağlar (CNN),
  metin ve dizi için dikkat mekanizması ve transformer'lar sıradaki adımlar.
- **Gradyan boosting kütüphaneleri.** XGBoost, LightGBM ve CatBoost, Bölüm
  12'deki fikri büyük tablo verisinde hızlı ve güçlü uygular; tablo verisi
  yarışmalarında sık kullanılırlar.
- **Olasılıksal modelleme.** Naive Bayes ve GMM'nin ardındaki düşünce: Bayes
  istatistiği, gizli değişkenli modeller, belirsizliği ölçen tahminler.
- **Zaman serileri.** Sıralı veride doğrulama başka kurallarla yapılır;
  bunun için Odyssey'de ayrı bir patika var.
- **Büyük veri ve üretim.** Modeli bir API ile sunmak (API 2), Docker ile
  paketlemek, büyük veride çalışmak (Büyük Veri patikası).

Sıfırdan yazma alışkanlığını koru: yeni bir yöntemi önce küçük bir örnekte elle
yaz, sonra kütüphaneyle karşılaştır. Bir yöntem beklenmedik sonuç verdiğinde
neye bakacağını bu alışkanlık söyler.
