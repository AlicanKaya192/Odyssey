CUPED'in kazancı tamamen ortak değişkenin (X) seçimine bağlıdır.

## İyi bir X

- **Atamadan önce ölçülmüştür.** Testten etkilenemez, bu yüzden iki
  grupta ortalaması aynıdır ve etkinin tahminini kaydırmaz.
- **Metrikle güçlü ilişkilidir.** Genellikle en iyisi aynı metriğin
  deneyden önceki değeridir: testten önceki dakikalar, testten önceki
  satın almalar.
- **Herkes için vardır** ya da yoksa nasıl doldurulacağı önceden
  yazılmıştır.

## Önceki verisi olmayan kullanıcılar

Test sırasında ilk kez gelen kullanıcıların "önceki dakikası" yoktur. Yaygın
çözüm X'i onlar için ortalamayla doldurmaktır: o zaman X − X̄ sıfır olur
ve bu kullanıcılar düzeltilmeden kalır. Bu geçerlidir ama kazanç küçülür;
yeni kullanıcıların payı büyükse CUPED'in yararı da azalır.

## Kötü bir X

- Test sırasında ölçülen her şey: oturumlar, tıklamalar, sepete eklemeler.
  B bunları değiştirebilir ve düzeltme etkinin bir kısmını siler.
- Atamadan sonra hesaplanmış bir "segment" (ör. testte çok aktif olanlar).
- Sonuca bakılarak seçilmiş bir X: en çok kazanç vereni deneye deneye
  seçmek, Çoklu Karşılaştırma bölümündeki tuzağın başka bir hâlidir. X
  plana önceden yazılır.
