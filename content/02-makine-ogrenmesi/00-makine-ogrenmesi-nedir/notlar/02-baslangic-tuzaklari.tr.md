Bu bölümdeki hataların hiçbiri kod hatası değil. Kod çalışıyor, model
kuruluyor, sayı çıkıyor — ve sayı yanıltıyor.

## 1. Modeli eğitildiği veriyle sınamak

En temel hata. Model eğitim verisini ezberleyebiliyor; o veride %99 doğru
olması hiçbir şey söylemiyor.

```python
model.fit(X, y)
model.score(X, y)     # anlamsiz
```

Doğrusu: veriyi ayır, **testte** ölç. Bu sayı bir "sınav notu" ve sınav
soruları önceden verilmemeli.

## 2. Taban çizgi kurmadan başarıya sevinmek

"%80 doğru" tek başına bilgi değil. Yüz kaydın 80'i tek bir sınıfa aitse,
her şeye o sınıfı diyen bir satır da %80 doğru oluyor.

| Problem | Taban çizgi |
|---|---|
| Regresyon | Eğitim verisinin ortalamasını söyle |
| Sınıflandırma | En sık görülen sınıfı söyle |

Modelin bunu geçemiyorsa ortada model yok.

## 3. Dengesiz veride accuracy'ye bakmak

Bin hastanın onunda hastalık varsa, "kimsede yok" diyen model **%99
doğru**. Ama işe yaramaz: bulunması gereken on kişiyi bulmuyor.

Dengesiz veride accuracy susturucu bir sayı; precision, recall ve karışıklık
matrisi bakılıyor. 3. ve 9. bölümün konusu.

## 4. Regresyonla sınıflandırmayı karıştırmak

Hedef sayıysa regresyon, kategoriyse sınıflandırma. Bu ayrım yöntemi de
**ölçüyü de** belirliyor: sınıflandırmada MAE, regresyonda accuracy anlamsız.

Sınır bazen belirsiz ("kaç yıldız"). Kararı verirsin ama **verdiğin kararı
yazarsın**.

## 5. Ölçeklemeyi unutmak

Bir sütun 0-1 arasında, öteki 0-100.000 arasındaysa mesafeye bakan yöntemler
(KNN gibi) yalnızca büyük sütunu duyar. Küçük sütun sanki yokmuş gibi
davranır.

Ağaç yöntemleri bundan etkilenmiyor; KNN, doğrusal modeller ve
kümeleme etkileniyor. 4. ve 6. bölümün konusu.

## 6. Veri sızıntısı

Modelin, tahmin anında elinde **olmayacak** bir bilgiyi eğitimde görmesi.

Klasik örneği: ölçeklemeyi bütün veriye uygulayıp sonra ayırmak. Test
verisinin ortalaması eğitim aşamasına sızıyor ve testteki başarı olduğundan
yüksek çıkıyor.

İkinci klasik: "hastaneye yatış tarihi" sütunuyla hastalığı tahmin etmek.
Model harika çalışıyor, çünkü cevabı zaten söyleyen bir sütun var.

Kural: **önce ayır, sonra dokun.** 4. ve 11. bölümün konusu.

## 7. Test verisine bakarak ayar seçmek

Test kümesine bakıp "şu ayar daha iyiymiş" demek, testi eğitim verisine
çeviriyor. Yirmi ayar denenip en iyisi test skoruna göre seçildiğinde o
skor artık dürüst değil.

Doğrusu: ayarları **doğrulama** kümesinde ya da çapraz doğrulamayla seç,
teste yalnızca sonda bir kez bak. 5. bölümün konusu.

## 8. Veri az olduğu hâlde karmaşık model kurmak

Otuz satırlık bir veride derin bir ağaç kurmak, veriyi ezberlemekten
başka bir şey yapmıyor. Az veride basit model daha çok iş görüyor.

Kaba bir alışkanlık: özellik sayısı örnek sayısına yaklaşıyorsa model
neredeyse kesin ezberliyor.

## 9. Modelin sebep söylediğini sanmak

Model "metrekare arttıkça fiyat artıyor" diyorsa bu bir **birliktelik**.
Önceki modülün kuralı burada da geçerli; model onu değiştirmiyor.

Özellik önem düzeyleri de aynı: "en önemli değişken" o değişkenin **sebep**
olduğu anlamına gelmiyor.

## 10. Rastgeleliği sabitlememek

Veri ayrımı ve birçok model rastgelelik taşıyor. `random_state`
verilmediğinde her çalıştırmada farklı sonuç çıkıyor ve "iyileştim mi,
şansım mı yaver gitti" ayırt edilemiyor.

Sonuçları karşılaştırmak istiyorsan rastgeleliği sabitle.

## 11. Kirli veriyle iyi model beklemek

Eksik değerler, tutarsız yazılmış kategoriler, aykırı değerler modele
olduğu gibi giriyor. Önceki modülün tamamı bu yüzden vardı ve buradaki
işin yarısı hâlâ orası.

## 12. Sonucu tek sayıya indirmek

"Modelin R²'si 0.85" bir rapor değil. Hangi veride, kaç kayıtla, hangi taban
çizgiye karşı, hangi hatalarda yanılıyor — rapor bunlar.

Bir modelin **nerede yanıldığı**, ne kadar doğru olduğu kadar önemli.
