Bu modül veri biliminin günlük araçlarını derinlemesine gösterdi. Buradan
sonrası birkaç yöne açılıyor.

## Bu patikada sırada

**ML Kütüphaneleri** modülü scikit-learn'ün bütün yapısını ele alıyor: ön
işleme, `Pipeline`, çapraz doğrulama, model seçimi, metrikler. Burada
öğrendiklerin orada doğrudan kullanılıyor:

- **NumPy dizileri** modelin girdisi ve çıktısı; yayınlama, ölçekleme ve
  `rng` tohumları her yerde.
- **pandas** veriyi modele hazırlar: birleştirme, eksik değer, kategori,
  zaman özellikleri.
- **Grafikler** modelin hatalarını görmenin yolu: artıklar, karışıklık
  matrisi, öğrenme eğrisi.
- **SciPy**'nin istatistiği iki modeli karşılaştırırken, en iyilemesi
  modelin içinde çalışır.

## Diğer patikalarla bağlantı

| Patika / modül | Bu modülün hangi kısmı |
|---|---|
| Zaman Serileri | pandas zaman araçları, `resample`, `rolling`, `shift` |
| Büyük Veri | pandas performansı, türler, bellek; parça parça okumak |
| ML Algoritmaları | NumPy ve doğrusal cebir: modelleri sıfırdan yazmak |
| Matematik | dağılımlar, testler ve doğrusal cebirin anlamı |

## Kendi başına keşfetmek

- Her kütüphanenin "User Guide" belgesi: pandas'ın, NumPy'nin, matplotlib'in
  ve SciPy'nin resmi kılavuzları bu modülde anlatılmayan birçok aracı
  içerir.
- matplotlib'in örnek galerisi: bir grafiğin nasıl yapıldığını görmenin en
  hızlı yolu.
- Kendi verinle çalış: bir CSV bul, sor, birleştir, çiz, sına. Bu modülün her
  bölümü o akışın bir adımı.

## Sık yapılan hataların kısa listesi

| Hata | Bu modülde |
|---|---|
| Satırların sessizce kaybolması | Birleştirme |
| Yanlış eksende işlem | Yayınlama |
| Değişmeyen tablo | pandas Performansı (Copy-on-Write) |
| Yanlış hesaplanmış çubuk | seaborn |
| p'ye fazla anlam yüklemek | scipy.stats |
| Kısıtı unutmak | scipy.optimize |
