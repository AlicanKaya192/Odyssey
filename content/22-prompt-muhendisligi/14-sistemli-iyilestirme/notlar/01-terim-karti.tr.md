| Terim | Anlamı |
|---|---|
| **Geliştirme kümesi** (development set) | Değişikliklere karar verirken ölçülen mesajlar; hataları okunur |
| **Test kümesi** (test set) | Hiç bakılmadan bekletilen mesajlar; en sonda bir kez ölçülür |
| **Başlangıç ölçüsü** (baseline) | İlk sürümün ölçüsü; sonraki her değişiklik buna göre değerlendirilir |
| **Hata incelemesi** (error analysis) | Hataları tek tek okuyup türlerine göre saymak |
| **Ezber** (overfitting) | Prompt'un geliştirme kümesindeki ayrıntılara uyup yeni mesajlarda aynı başarıyı göstermemesi |
| **Ablasyon** (ablation) | Bir parçayı çıkarıp yeniden ölçerek katkısını bulmak |
| **Oyuncak model** | Bu bölümde yöntemi göstermek için kullanılan, prompt'taki kelime listelerine göre karar veren basit program; gerçek bir dil modeli değil |

**Akılda tut:**

- Oyuncak modelde `v1` geliştirme ve testte 0,60; `v2` (anlamdan gelen
  kelimeler) 0,90 ve 0,75; `v3` (geliştirme mesajlarından kopyalanan
  kelimeler) 1,00 ve 0,75.
- `v3` testte hiçbir şey kazandırmadı ama prompt'u 100'den 139 token'a
  çıkardı.
- `v1`'in sekiz hatasının sekizi de `unknown` idi: tanımlar fazla dardı.
- Ablasyonda `back`'i çıkarmak başarıyı artırdı; `send` ile `back`
  birlikte çıkarılınca toplam aynı kaldı ama iki mesajın cevabı değişti.
