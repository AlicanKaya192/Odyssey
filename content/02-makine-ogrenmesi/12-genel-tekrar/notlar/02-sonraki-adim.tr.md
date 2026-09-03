Bu modül scikit-learn'ün klasik makine öğrenmesi tarafını kapsadı. Aşağısı,
"şimdi ne öğrenmeliyim" sorusunun sırayla cevabı.

## Önce: bir proje yap

Yeni kütüphane öğrenmeden önce **kendi verinle** bir şey yap. Ders
verisinde çalışmayan hiçbir şey öğretmiyor:

- Veriyi kendin bul. Kaggle, kamu kurumlarının açık verileri, kendi
  telefonundaki adım sayacı — fark etmez.
- **Soruyu kendin kur.** Bu modülde hedef sütunu hazır geldi; gerçek
  hayatta "neyi tahmin edeceğiz" en zor karar.
- Taban çizgiden başla ve raporunu bir başkasının okuyacağını varsayarak
  yaz.

**Öğrendiğinin sınavı şu:** modelin taban çizgiyi geçemezse bunu
söyleyebiliyor musun?

## Zaman serisi

Bu modüldeki her şey satırların **bağımsız** olduğunu varsaydı. Sıralı
veride bu doğru değil.

- `train_test_split` **yanlış**: rastgele ayırınca modele geleceği
  gösteriyorsun. Zaman bazlı ayırma gerekiyor.
- `TimeSeriesSplit`, çapraz doğrulamanın zaman uyumlu hâli: her kat
  geçmişte eğitiyor, gelecekte doğruluyor.
- Gecikmeli özellikler (`lag`), hareketli ortalamalar ve mevsimsellik ayrı
  bir konu.
- Kütüphaneler: `statsmodels`, `prophet`, `sktime`.

**Bu modülden sonraki en pratik adım bu**, çünkü gerçek verinin çoğu
tarihli.

## Metin

Bir cümleyi modele vermek için sayıya çevirmek gerekiyor.

- `TfidfVectorizer` başlangıç: kelime sayımına dayalı, hızlı, `Pipeline`
  içine doğrudan giriyor.
- Gömmeler (embedding) devamı: kelimeleri anlamlarına göre yerleştiren
  vektörler.
- `scikit-learn` ile duygu analizi ve konu sınıflandırma yapılabiliyor;
  ötesi derin öğrenme.

## Derin öğrenme

Görüntü, ses ve uzun metin bu modülün dışında kaldı. Sinir ağları ayrı bir
alan.

- `torch` (PyTorch) fiili standart.
- Tablo verisinde **genelde gerekmiyor** — gradyan artırma çoğu zaman daha
  iyi ve çok daha hızlı. Bu, sık yapılan bir hata.
- Görüntüde ve metinde ise alternatifi yok.

**Sıra önemli:** bu modülü atlayıp derin öğrenmeye başlamak, taban çizgi ve
sızıntı kavramları olmadan model kurmak demek.

## Model açıklama

Bölüm 07'de özellik önemini ve üç tuzağını gördün. Devamı:

- `permutation_importance` — sütunu karıştırıp skorun ne kadar düştüğüne
  bakıyor, test kümesinde ölçülebiliyor. sklearn'ün içinde.
- **SHAP** — her tahmini tek tek açıklıyor: "bu hastanın riski neden
  yüksek çıktı?" Ayrı bir paket.
- Kısmi bağımlılık grafikleri (`PartialDependenceDisplay`) — bir sütun
  değişince tahminin nasıl değiştiğini çiziyor.

Bir modeli birine anlatman gerekiyorsa bu araçlar zorunlu hâle geliyor.

## Üretime almak (MLOps)

Kaydedilen dosyayı bir yere koyup çalıştırmak ayrı bir alan:

- Servis etmek: `FastAPI` ile bir HTTP uç noktası.
- Sürümlemek: hangi model, hangi veriyle, ne zaman eğitildi.
- İzlemek: tahminlerin dağılımı ve gerçek sonuçlar geldikçe skor.
- Yeniden eğitmek: düzenli aralıkla, ve **eski modelle karşılaştırarak**.

Bunlar makine öğrenmesi değil yazılım mühendisliği; ama modelin işe
yaraması için gerekli.

## Öğrenirken düşülen dört tuzak

**1. Kütüphane biriktirmek.** XGBoost, LightGBM, CatBoost öğrenmek yeni bir
şey öğrenmek değil — üçü de gradyan artırma. Bu modülde öğrendiğin
kavramlar hepsinde aynı.

**2. Skor kovalamak.** Kaggle yarışmalarında 0.001'lik iyileştirmeler
peşinde koşulur; gerçek projelerde o fark hiçbir şey değiştirmiyor. Zamanın
çoğu veriyi anlamaya gidiyor.

**3. Taban çizgiyi atlamak.** En sık ve en pahalı hata. Yeni bir kütüphane
öğrenmek yerine bu alışkanlığı korumak daha değerli.

**4. Modeli sebep sanmak.** Model korelasyon buluyor. "Destek çağrısı
arttıkça ayrılma artıyor" doğru; "destek çağrısını azaltırsak ayrılma
azalır" **yanlış olabilir**. Sebep bulmak deney tasarımı işi.

## Kaynaklar

- **scikit-learn'ün kendi belgeleri** — kullanıcı kılavuzu (user guide)
  bölümü ders niteliğinde ve ücretsiz.
- **Kendi notların.** Bu modülün her bölümünde bir başvuru notu var; onlar
  senin ilk kaynağın.
- **Kod okumak.** `sklearn` kaynak kodu okunabilir; bir modelin ne yaptığını
  merak ettiğinde bakılabiliyor.

## Son

Bu modülde öğrendiğin en değerli şey bir kütüphane değil, bir alışkanlık:

**Tahmin etme, ölç. Tek sayıya güvenme. Fazla iyi görünen sonuçtan şüphelen.**

Kütüphaneler değişiyor, bu üçü değişmiyor.
