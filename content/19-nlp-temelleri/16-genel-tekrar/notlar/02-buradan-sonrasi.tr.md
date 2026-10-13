Bu modül klasik NLP'nin araç kutusunu verdi. Buradan sonrası birkaç yöne
açılıyor.

## Bu patikada sırada

**Gömmeler ve Dil Modelleri** modülü bu modülün bıraktığı iki boşluğu
dolduruyor:

- **Anlam.** Kelime torbasında "car" ve "automobile" iki ayrı sütun, hiç
  ortak noktaları yok. Gömmeler (embedding) kelimeleri, birlikte geçtikleri
  kelimelere bakarak vektöre çevirir; benzer anlamlı kelimeler birbirine
  yakın düşer. PPMI ve SVD'den Word2Vec'e kadar sıfırdan kuracağız.
- **Sıra.** Kelime torbası sırayı unutur. Dil modelleri bir sonraki kelimeyi
  tahmin eder: n-gram modelinden HMM'e, RNN'den dikkat mekanizmasına ve
  transformer'a kadar.

Bu modülün yöntemleri orada da kullanılıyor:

| Bu modülde | Sonraki modülde |
|---|---|
| Parçalayıcı (02) | BPE ile alt kelime parçalama |
| n-gram sayımları (04) | n-gram dil modeli, düzgünleştirme |
| PMI (04) | PPMI matrisi ve kelime vektörleri |
| Kosinüs ve arama (07) | belge gömmeleriyle anlamsal arama |
| BIO etiketleme (14) | HMM ve Viterbi ile sıra etiketleme |
| Hata analizi (15) | dil modellerini değerlendirmek |

## Diğer patikalarla bağlantı

| Patika / modül | Bu modülün hangi kısmı |
|---|---|
| Makine Öğrenmesi | doğrusal modeller, ölçüler, çapraz doğrulama |
| ML Kütüphaneleri | `Pipeline`, `GridSearchCV`, sızıntı |
| ML Algoritmaları | Naive Bayes, lojistik regresyon, K-Means'in içi |
| Algoritma Teknikleri | metin algoritmaları, olasılıksal veri yapıları (Bloom filtresi, MinHash) |
| Büyük Veri | çok büyük metin koleksiyonlarında parça parça sayım, MapReduce |

## Kendi başına keşfetmek

- scikit-learn kılavuzundaki metin özellikleri bölümü
  (`sklearn.feature_extraction.text`) burada anlatılmayan ayarları
  içerir.
- Kendi verinle çalış: e-postaların, notların, bir forumun mesajları. Bu
  modülün kontrol listesini (15'in ikinci notu) sırayla geç.
- Türkçe metinle dene: sondan eklemeli bir dilde kök bulmanın ve
  parçalamanın neden zor olduğunu (02, 03) kendi gözünle gör.

## Sık yapılan hataların kısa listesi

| Hata | Bu modülde |
|---|---|
| Vektörleştiriciyi bütün veriyle kurmak | Kelime Torbası, Metin için Pipeline |
| "not"u durak kelime diye atmak | Normalleştirme, Duygu Analizi |
| Dengesiz veride yalnızca doğruluğa bakmak | Doğrusal Modeller ve Değerlendirme |
| `best_score_`'u gerçek sonuç sanmak | Metin için Pipeline |
| Konuları kategori sanmak | Konu Modelleme |
| Kuralı ölçmeden genişletmek | Bilgi Çıkarma |
