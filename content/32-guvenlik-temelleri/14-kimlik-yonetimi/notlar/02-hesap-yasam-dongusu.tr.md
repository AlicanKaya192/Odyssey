Bir hesabın her olayında yapılacaklar. Kurumlar bunu çoğu zaman insan
kaynaklarındaki kayda bağlar: işe giriş, görev değişikliği ve çıkış kaydı
açılınca kimlik sistemi kendiliğinden harekete geçer.

## Katılan (joiner)

- Hesaplar **rolün** standart yetkileriyle açılır; kişiye özel ek yetki
  ayrı bir onayla verilir.
- İlk parola tek kullanımlıktır, ilk girişte değiştirilir; çok faktörlü
  doğrulama ilk gün kurulur.
- Hesabın bir **sahibi** (yöneticisi) kayda geçer.

## Değişen (mover)

- Yeni rolün yetkileri eklenir, eski rolün yetkileri **aynı gün**
  kaldırılır.
- Geçiş dönemi gerekiyorsa eski yetki **bitiş tarihiyle** bırakılır.
- Görev ayrılığı yeniden denetlenir: yeni rol eskisiyle birlikte
  çakışan bir yetki çifti oluşturuyor mu?

## Ayrılan (leaver)

- Dizindeki kayıt kapatılır; dizine bağlı olmayan her sistem tek tek
  kapatılır (liste tutulur).
- Kişinin bildiği **ortak sırlar** (ortak hesap parolaları, API
  anahtarları) değiştirilir.
- Açık oturumlar ve jetonlar iptal edilir.
- Cihazlar ve kartlar geri alınır.
- Kişinin dosyaları ve sahip olduğu hizmet hesapları başka birine
  devredilir.

## Düzenli işler

- **Erişim gözden geçirmesi:** yöneticiler ekiplerinin yetkilerini
  onaylar ya da kaldırır.
- **Öksüz hesap taraması:** etkin çalışan listesiyle her sistemin hesap
  listesi karşılaştırılır.
- **Kullanılmayan hesap:** uzun süredir giriş yapılmamış hesap önce
  kilitlenir, sonra kapatılır.
- **Hizmet hesapları:** her birinin sahibi, amacı ve son parola
  değişikliği kayıtlıdır.
