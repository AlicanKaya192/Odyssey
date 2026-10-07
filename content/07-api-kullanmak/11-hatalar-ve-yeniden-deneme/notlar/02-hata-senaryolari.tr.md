Gerçek hayattan hata durumları ve doğru tepkiler.

## Program donup kaldı

**Belirti:** Çıktı yok, program bitmiyor.
**Neden:** `timeout` yok; sunucu cevap vermiyor ve requests sonsuza kadar
bekliyor.
**Tepki:** Her isteğe `timeout=5` gibi bir değer ver; `requests.Timeout`'u
yakala.

## Gece çalışan betik sabah yarıda kalmış

**Belirti:** 300 sayfanın 140'ında `ConnectionError` ile durmuş.
**Neden:** Ağ bir an kopmuş; tek bir hata bütün işi bitirmiş.
**Tepki:** Sayfa isteğini yeniden deneme fonksiyonuyla sar; ayrıca o ana
kadar alınanları kaydet ki baştan başlamak gerekmesin (Bölüm 15).

## Sunucu sahibinden şikâyet geldi

**Belirti:** "Saniyede yüzlerce istek atıyorsunuz."
**Neden:** `503` alınca beklemeden döngüde yeniden denenmiş.
**Tepki:** Yeniden denemede bekle ve süreyi katla; üst sınır koy; `Retry-After`'a
uy.

## Aynı sipariş üç kez oluşmuş

**Belirti:** Veritabanında kopya kayıtlar.
**Neden:** `POST` zaman aşımında otomatik yeniden denenmiş; istekler aslında
sunucuya ulaşmış.
**Tepki:** `POST`'u otomatik yeniden deneme. Gerekirse önce `GET` ile kaydın
oluşup oluşmadığına bak.

## Hata hiç düzelmiyor

**Belirti:** Beş denemenin beşi de `404`.
**Neden:** `4xx` geçici değil; beklemek bir şey değiştirmez.
**Tepki:** `4xx`'te yeniden deneme; adresi, kimliği, gövdeyi düzelt.
