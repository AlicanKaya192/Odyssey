Bir model kartını doldurmak için şablon. Her alan kısa olabilir ama boş
kalmamalı.

| Alan | Soru | Bu modülün modeli için |
|---|---|---|
| Ad ve sürüm | Hangi model? | `churn`, sürüm 1 |
| Ne yapar | Neyi tahmin ediyor? | Aboneliğini iptal edecek müşterileri |
| Kim kullanır | Tahmin hangi kararda kullanılıyor? | Müşteri ekibi, kimi arayacağını seçerken |
| Veri | Hangi veriyle eğitildi? | 2000 müşteri, 0. ay, parmak izi kayıtta |
| Ölçüm | Nasıl ölçüldü? | 1000 müşterilik değerlendirme kümesinde doğruluk; temel çizgiyle birlikte |
| Sınırlar | Nerede kullanılmamalı? | Başka bir hizmetin müşterilerinde; fiyatlar büyük ölçüde değişince |
| Bilinen hatalar | Nerede yanılıyor? | Yeni müşterilerde (kısa abonelik) daha sık |
| Sorumlu | Sorun olunca kime sorulur? | Modeli kaydeden ekip |

## Neden sınırlar en önemlisi?

Model, eğitildiği dünyanın dışında hata vermez; yalnızca yanlış tahmin
eder. Kartın sınırlar bölümü, kullanan kişinin bunu baştan bilmesini
sağlar. İleride Kavram Kayması bölümünde fiyat ağırlığı değiştiğinde ne
olduğunu ölçeceğiz: tam olarak bu satırın uyardığı durum.

## Kontrol listesi

- Her canlı sürümün bir kartı var mı?
- Kart kayıttaki sürümle aynı numarayı taşıyor mu?
- Ölçümün yanında temel çizgi yazıyor mu?
- Sınırlar bölümü dolu mu?

## Yapma

- Kartı bir kez yazıp bırakma; yeni sürümde veri ya da ölçüm değiştiyse
  kart da değişir.
- Ölçüm olarak yalnızca en iyi görünen sayıyı yazma; nasıl ölçüldüğü de
  yazılır.
