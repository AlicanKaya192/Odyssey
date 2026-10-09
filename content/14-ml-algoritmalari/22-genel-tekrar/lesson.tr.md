# Genel Tekrar

ALG 3'ün sonuna geldin. Makine öğrenmesi algoritmalarının çoğunu NumPy ile
**sıfırdan** yazdın ve sonuçlarını scikit-learn'le karşılaştırdın. Artık bir
kütüphane fonksiyonunu çağırdığında arkasında ne döndüğünü biliyorsun: hangi
kaybı küçülttüğünü, hangi varsayıma dayandığını, nerede yanıldığını. Bu bölüm
her algoritmanın özünü ve ölçtüğümüz en önemli sonuçları bir arada topluyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>00–02</small></span><span class="arrow">→</span>
    <span class="node">Doğrusal modeller<br><small>03–07</small></span><span class="arrow">→</span>
    <span class="node">Sınıflandırıcılar<br><small>08–13</small></span><span class="arrow">→</span>
    <span class="node">Denetimsiz<br><small>14–19</small></span><span class="arrow">→</span>
    <span class="node acc">Ağ ve öneri<br><small>20–21</small></span>
  </div>
  <figcaption>ALG 3'ün yolu: ölçmeyi öğren, doğrusal modelleri kur, sınıflandırıcıları karşılaştır, etiketsiz veriye geç, sonunda sinir ağı ve öneri.</figcaption>
</figure>

## 1. Temeller (Bölüm 0–2)

Algoritmayı sıfırdan yazmanın ilk dersi **vektörleştirme**: Python döngüsü
yerine `X @ w` gibi dizi işlemleri. İkincisi **taban çizgisi**: her zaman en
sık sınıfı söyleyen "model" bile bir doğruluk alır; gerçek model onu geçmeli.
İstatistikte dikkat sayısal hassasiyete: varyansı tek geçişte saf formülle
hesaplamak büyük sayılarda bozulur, Welford yöntemi bozulmaz. Bir modelin ne
kadar iyi olduğu **yeniden örnekleme** ile ölçülür: tek bir bölme şansa bağlı,
k-katlı çapraz doğrulama daha kararlı; permütasyon testi "bu sonuç şans mı?"
sorusunu cevaplar.

## 2. Doğrusal modeller (Bölüm 3–7)

- **Doğrusal regresyon:** normal denklem ya da gradyan inişi; birbirine çok
  bağlı özelliklerde katsayılar anlamsız büyür, yüksek dereceli polinom test
  verisinde patlar.
- **Gradyan inişi:** öğrenme hızı ve **ölçekleme** belirleyici; ölçeklenmemiş
  veride aynı problem yüz bin adımda bile bitmiyordu, ölçekleyince 23
  adımda bitti.
- **Lojistik regresyon:** sigmoid + log-kayıp; çok sınıfta softmax.
- **Değerlendirme:** karışıklık matrisi, kesinlik/duyarlılık/F1, ROC ve AUC.
  Doğruluk dengesiz veride yanıltır.
- **Düzenlileştirme:** Ridge (L2) katsayıları küçültür, Lasso (L1) bazılarını
  tam sıfır yapar; güç çapraz doğrulamayla seçilir.

## 3. Sınıflandırıcılar (Bölüm 8–13)

| Algoritma | Fikir | Dikkat |
|---|---|---|
| KNN | en yakın `k` komşunun oyu | ölçekleme, boyut laneti |
| Naive Bayes | sınıf olasılığı × özelliklerin olasılıkları | log ile topla (alt taşma), Laplace düzeltmesi |
| Karar ağacı | en çok saflaştıran bölme (Gini) | derinlik sınırı, aşırı uyum |
| Rastgele orman | ağaçların oyu, her ağaçta rastgelelik | OOB ile ücretsiz doğrulama |
| Boosting | her yeni ağaç öncekilerin hatasına | öğrenme hızı, erken durdurma |
| SVM | marjı en büyük sınır, menteşe kaybı | `C`, çekirdek, ölçekleme |

Ağaçtan ormana geçişin değeri ölçüldü: tek ağaç 0,738, bagging 0,80, rastgele
orman 0,814; OOB tahmini 0,828. Boosting ve SVM'de kendi yazdığımız sürümler
scikit-learn'le birebir ya da çok yakın sonuç verdi.

## 4. Etiketsiz veri (Bölüm 14–19)

- **K-Means:** ata ve güncelle; başlangıca bağlı, 100 rastgele başlangıcın 4'ü
  yerel minimuma takıldı, k-means++ bunu 1'e indirdi. `k` dirsek ve siluetle.
- **GMM ve EM:** yumuşak atama, elips şeklinde kümeler; bileşen sayısı BIC
  ile.
- **Hiyerarşik ve DBSCAN:** ağaç kurup kesmek; yoğunluğa göre küme ve
  gürültü. Gürültülü hilallerde DBSCAN 1,0, K-Means 0,221.
- **PCA:** kovaryansın özvektörleri; rakam verisinde 64 pikselin varyansının
  %90'ı 21 bileşende. Ölçeklemeden yapılan PCA birimi büyük sütunu bulur.
- **Birliktelik kuralları:** destek, güven, kaldıraç; Apriori budaması.
  Güven yanıltır (çay → süt 0,615 ama kaldıraç 1,05).
- **PageRank:** rastgele gezgin, kuvvet yinelemesi; bağlantılar sayılmaz,
  tartılır.

## 5. Sinir ağı ve öneri (Bölüm 20–21)

Sinir ağı katman katman nöronlardır; geri yayılım türevleri zincir kuralıyla
taşır ve sayısal türevle denetlenir. Tek nöron XOR'u çözemez, üç gizli nöron
çözer. Ağırlıklar rastgele başlamalı, yoksa nöronlar aynı kalır. Öneri
sistemlerinde matris ayrıştırma gizli zevkleri bulur: test hatası 0,628 ile
taban çizgilerinin hepsinden iyi, ilk 5 önerinin isabeti popülerliğin
yaklaşık 1,8 katı.

## Ortak dersler

1. **Önce taban çizgisi.** Her modeli basit bir rakiple karşılaştır.
2. **Ölçekle.** Uzaklığa ya da gradyana dayanan her yöntem (KNN, SVM,
   K-Means, PCA, gradyan inişi) ölçeğe duyarlı.
3. **Test verisine dokunma.** Ölçekleme, PCA, seçim; hepsi yalnızca eğitim
   verisine uyar (`Pipeline`).
4. **Ayarları çapraz doğrulamayla seç.** `k`, `C`, `alpha`, derinlik,
   bileşen sayısı.
5. **Karmaşıklık bedava değil.** Eğitim hatası düşerken test hatası
   yükseliyorsa model ezberliyor.
6. **Sıfırdan yazınca doğrula.** Kütüphaneyle, sayısal türevle, kaba
   kuvvetle karşılaştır.

## Bu bölümde

40 karışık soru ve beş alıştırma: ölçeklemeyi sızıntısız yapmak, sınıflandırma
ölçülerini hesaplamak, KNN ile tahmin, en iyi ağaç bölmesini bulmak ve
lojistik regresyonu gradyan inişiyle eğitmek. Ders notlarında hızlı başvuru
kalıpları ve buradan sonrası var.
