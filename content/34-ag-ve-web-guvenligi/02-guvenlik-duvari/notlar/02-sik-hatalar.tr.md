Güvenlik duvarı hatalarının çoğu teknik değil, alışkanlık hatasıdır: bir
kural "şimdilik" eklenir ve yıllarca kalır.

## Her yere her şey

`allow any any` gibi bir kural (her kaynaktan her porta) güvenlik
duvarını kapatmakla aynıdır. Çoğu zaman bir sorunu çözmek için geçici
eklenir. Geçici kurala bir **bitiş tarihi** yazılır ve o tarihte
kaldırılır.

## Gölgelenen kural

Geniş bir izin, altındaki dar bir reddi işe yaramaz kılar. Okuyan, listede
"23 kapalı" satırını görüp güvende sanır. Kural listesi her
değişiklikten sonra "bu kurala hiç paket ulaşabilir mi?" sorusuyla okunur;
araçlar her kuralın kaç pakete tuttuğunu sayar.

## Yönetim portunu internete açmak

SSH (22) ya da uzak masaüstü (3389) `0.0.0.0/0`'a açılırsa, internetteki
her otomatik tarayıcı onu bulur ve parola dener. Bu portlar yalnızca
yönetim ağına ya da VPN'den gelenlere açılır (VPN ve Ağ Bölümleme
bölümü).

## Yalnızca girişi süzmek

Giriş kuralları sağlam, çıkış "her şeye izin" ise ele geçirilmiş bir
bilgisayar rahatça dışarıya bağlanır ve veri gönderir. Çıkışta da izin
listesi kullanılır.

## Kayıt tutmamak

Reddedilen paket kaydedilmezse saldırı girişimi görünmez; kabul edilen
önemli bağlantılar kaydedilmezse olaydan sonra ne olduğu bulunamaz.

## Güvenlik duvarına fazla güvenmek

"Güvenlik duvarının arkasındayız" demek, içerideki her bilgisayara güvenmek
demektir. İçeride başlayan bir saldırıyı ağ güvenlik duvarı görmez. Bu
yüzden ağ bölünür, her bilgisayarın kendi güvenlik duvarı açık tutulur ve
uygulamalar kimlik doğrulamadan vazgeçmez.

## Gözden geçirme listesi

- Varsayılan karar `deny` mi?
- Her kuralın sahibi, gerekçesi ve (geçiciyse) bitiş tarihi var mı?
- Hiç tutmayan ya da gölgelenen kural var mı?
- Yönetim portları internete kapalı mı?
- Çıkış süzülüyor ve kaydediliyor mu?
