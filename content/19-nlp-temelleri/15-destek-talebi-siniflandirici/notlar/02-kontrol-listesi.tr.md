Bu modülde bir metin sınıflandırma projesinin bütün adımlarını gördük.
Yeni bir projeye başlarken bu listeyi sırayla geç.

## Veri

- [ ] Metinlere **bak**: rastgele 50 örneği oku. Kodlama, HTML artığı,
  görünmez boşluk var mı (01)?
- [ ] Sınıf dağılımını say. Dengesizse ölçü doğruluk değil macro F1 (09).
- [ ] Tam ve yakın kopyaları bul (13). Aynı metin hem eğitimde hem testte
  olursa skor şişer.
- [ ] Etiketleri kim, nasıl verdi? Birkaç örneğin etiketini kendin ver ve
  karşılaştır: etiket gürültüsü ne kadar?

## Ölçü

- [ ] Test verisini **en başta** ayır ve en sona kadar dokunma. `stratify`
  ile.
- [ ] Taban çizgisini ölç: en sık sınıf, basit bir kural (00, 15).
- [ ] İş için hangi hata daha pahalı? Kesinlik mi duyarlılık mı (09)?

## Model

- [ ] Ön işlemeyi Pipeline'ın içine koy (10): temizlik, maskeleme (15).
- [ ] Önce basit, güçlü taban modeller: TF-IDF + lojistik regresyon,
  doğrusal SVM, Naive Bayes (08, 09).
- [ ] Kelime çiftleri olumsuzlamayı yakalar (09); harf n-gram'ları yazım
  hatası çok olan metinde işe yarar (10).
- [ ] Ayarları çapraz doğrulamayla ara; `best_score_` iyimserdir (10).

## İnceleme

- [ ] Karışıklık matrisine ve sınıf sınıf F1'e bak (09).
- [ ] En emin olunan hataları oku (09): model mi yanlış, etiket mi?
- [ ] Hatalar görevin sınırından mı geliyor (iki konulu talepler, ironi)?
  O zaman çözüm model değil görevin tanımı (11, 15).
- [ ] Kapsam dışı girdi için bir "emin değilim" kapısı düşün (bu bölümün
  ilk notu).

## Kullanım

- [ ] Pipeline'ı tek dosyaya kaydet; kendi fonksiyonlarını bir modülde tut
  (10).
- [ ] Gerçek kullanımda gelen metinler zamanla değişir. Belli aralıklarla
  yeni örnekleri etiketleyip modeli yeniden ölç.

Bu liste bir sonraki modülde de geçerli. Orada metni kelime sayımlarıyla
değil **gömmelerle** (embedding) temsil edeceğiz; ama ölçme, ayırma ve
inceleme adımları aynen kalıyor.
