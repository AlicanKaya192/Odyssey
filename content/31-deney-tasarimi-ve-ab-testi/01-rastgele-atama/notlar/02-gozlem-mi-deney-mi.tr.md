Elde zaten veri varken neden deney yapılır? Çünkü gözlemsel veride
"birlikte değişen" iki şeyden birinin ötekine neden olduğunu söylemek çok
zordur.

| | Gözlemsel veri | Rastgele deney |
|---|---|---|
| Kim neyi görüyor? | kişi kendi seçiyor ya da sistem bir kurala göre veriyor | şans karar veriyor |
| Karıştırıcı değişkenler | gruplar arasında farklı olabilir | ortalamada eşit |
| Fark neden geliyor? | değişiklikten, seçimden ya da ikisinden | değişiklikten ya da şanstan |
| Sonuç | ilişki | neden-sonuç |

## Karıştırıcı değişken örnekleri

- Yeni özelliği açanlar zaten daha sık gelen kullanıcılar.
- İndirim kodunu kullananlar zaten alışveriş yapmaya niyetli kişiler.
- Uygulamanın yeni sürümüne geçenler daha yeni telefonlara sahip.

Her birinde "özellik / kod / sürüm satışı artırıyor" sonucu yanlış olabilir.

## Deney yapılamıyorsa

Bazen deney mümkün değildir (fiyatları herkes için değiştirmek, yasal
sınırlar). O zaman karıştırıcıları ölçüp hesaba katan yöntemler (eşleştirme,
regresyon, fark içinde fark) kullanılır. Hepsi "ölçülmemiş karıştırıcı
yok" varsayımına dayanır; rastgele deney bu varsayıma ihtiyaç duymaz.
