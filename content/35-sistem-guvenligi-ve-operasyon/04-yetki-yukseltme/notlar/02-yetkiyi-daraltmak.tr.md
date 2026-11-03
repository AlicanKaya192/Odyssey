Yetki yükseltmeye karşı en etkili savunma, yükseltilecek yetkiyi baştan
**az** tutmaktır. Kimse gerekmeyen bir yetkiye sahip değilse, bir hata ya
da ele geçirilmiş bir hesap da o yetkiye ulaşamaz.

## Hesap düzeyinde

- **Kişiye özel hesaplar:** paylaşılan bir yönetici hesabı, kimin ne
  yaptığını izlemeyi imkânsız kılar.
- **Ayrı yönetici hesabı:** yönetici yetkisi olan kişi günlük işini
  (e-posta, tarayıcı) yönetici olmayan bir hesapla yapar.
- **Tam zamanında yetki** (just-in-time): yönetici yetkisi kalıcı değil,
  bir iş için ve süreli verilir; süre bitince kendiliğinden geri alınır.
- **Düzenli gözden geçirme:** kimin hangi gruplarda olduğu dönem dönem
  okunur; görevini değiştiren ya da ayrılan kişinin yetkisi kaldırılır.

## Uygulama düzeyinde

- Her uç nokta **kimin** istediğine ve **neye** dokunduğuna bakar; ikisi
  ayrı denetimlerdir.
- Yetki denetimi tek bir yerde yazılır ve her istek oradan geçer;
  dağınık denetimlerden biri mutlaka unutulur.
- Varsayılan cevap "hayır"dır: yeni bir uç nokta eklenince yetki
  denetimi yoksa istek reddedilir.

## Sistem düzeyinde

- Hizmetler kendi kısıtlı hesaplarıyla çalışır.
- Ayrıcalıklı çalışan her betik ve programın sahibi ayrıcalıklı hesaptır
  ve başkası onu değiştiremez.
- setuid programların ve zamanlanmış görevlerin bir envanteri tutulur;
  envanterde olmayan yeni bir kayıt araştırılır.
- Yamalar düzenli yüklenir: bilinen bir açığı kapatmak, onu tespit
  etmekten her zaman daha ucuzdur.

## Değişiklikleri izlemek

Yetki yükseltmenin sonucu çoğu zaman bir **değişikliktir**: yönetici
grubuna yeni bir üye, yeni bir zamanlanmış görev, yeni bir setuid dosya.
Bu yüzden bu listelerin anlık görüntüleri düzenli alınır ve bir öncekiyle
karşılaştırılır. Beklenmeyen her fark, bir değişiklik kaydıyla
açıklanmalıdır; açıklanamayan fark bir olay olarak ele alınır (Olay
Müdahalesi bölümü).
