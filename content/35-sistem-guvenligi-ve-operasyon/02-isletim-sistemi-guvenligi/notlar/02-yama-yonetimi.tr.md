Bir açığın düzeltmesi yayınlandığı an, açık herkesin bildiği bir şeye
dönüşür. Düzeltmeyi yükleyen sistem korunur; yüklemeyen, artık tarifi
herkesçe bilinen bir açıkla çalışmaya devam eder. **Yama yönetimi**
(patch management) bu aradaki süreyi kısaltma işidir.

## Yama döngüsü

1. **Envanter:** hangi bilgisayarda hangi yazılımın hangi sürümü kurulu?
   Bilinmeyen yazılım güncellenemez.
2. **İzleme:** yazılımların güvenlik duyurularını (advisory) takip et. Her
   duyuru hangi sürümde düzeltildiğini söyler.
3. **Karşılaştırma:** kurulu sürüm düzeltilmiş sürümden eski mi? (Sürümler
   sayı demeti olarak karşılaştırılır.)
4. **Önceliklendirme:** önce internete açık sistemler ve ciddi açıklar.
5. **Deneme ve yükleme:** yamayı önce küçük bir grupta dene, sonra hepsine
   yükle.
6. **Doğrulama:** yükleme gerçekten yapıldı mı, sürüm değişti mi?

## Önceliği ne belirler?

| Soru | Evetse |
|---|---|
| Sistem internetten erişilebilir mi? | Öne al |
| Açık uzaktan, kimlik doğrulamadan kullanılabiliyor mu? | Öne al |
| Açığın kullanıldığı biliniyor mu? | En öne al |
| Sistem kritik veri tutuyor mu? | Öne al |

Bu sorular Riski Değerlendirmek bölümündeki olasılık ve etki fikrinin
yamaya uygulanmasıdır.

## Yama hemen yüklenemiyorsa

Bazen bir yama uyumluluk yüzünden hemen yüklenemez. O zaman açığın
**etkisini azaltan** geçici önlemler alınır: ilgili hizmeti kapatmak,
erişimi güvenlik duvarıyla sınırlamak, izlemeyi artırmak. Bunlar yamanın
yerini tutmaz, yalnızca süre kazandırır; geçici önlemin bir bitiş tarihi
olur.

## Sık hatalar

- Envanteri olmadan "her şey güncel" sanmak.
- Sürümü metin olarak karşılaştırmak (`"2.4.10" < "2.4.9"`).
- Yalnızca işletim sistemini güncelleyip uygulamaları ve kütüphaneleri
  unutmak.
- Yükledikten sonra doğrulamamak: yeniden başlatılmamış bir sistem eski
  kodu çalıştırmaya devam edebilir.
