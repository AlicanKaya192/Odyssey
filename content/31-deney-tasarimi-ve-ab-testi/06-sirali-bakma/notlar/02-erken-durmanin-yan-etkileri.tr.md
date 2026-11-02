Doğru eşiklerle bile erken durmanın iki yan etkisi vardır.

## Etki abartılır

Erken durulan testler, etkinin şans eseri büyük göründüğü anlarda durur.
Güç Analizi bölümündeki **kazananın laneti** burada da geçerlidir: erken
duran testlerde ölçülen etki, gerçek etkiden ortalamada büyüktür. Raporda
etki yazılırken bu hesaba katılır; mümkünse etki, durduktan sonra toplanan
veriyle yeniden tahmin edilir.

## Hafta döngüsü bozulur

İki haftalık bir test 4. günde durursa yalnızca hafta içi kullanıcılar
görülmüş olabilir. Hafta sonu farklı davranan bir kitlede sonuç bütün
haftayı temsil etmez. Bu yüzden ardışık tasarımlarda bakışlar genellikle
**tam hafta sonlarına** konur.

## Yenilik etkisi

İlk günlerde kullanıcılar yeni bir şeye merakla tıklayabilir; bu etki
sonra söner. Çok erken duran test bu geçici artışı kalıcı sanabilir
(Yenilik Etkisi ve Uzun Vadeli Etki bölümü).

## Özet

Erken durmak, doğru yapılsa bile "daha az bilgiyle karar" demektir. Hız
gerçekten değerliyse (ör. büyük bir zarar ya da çok değerli bir kazanç)
seçilir; değilse sabit süreli test daha temizdir.
