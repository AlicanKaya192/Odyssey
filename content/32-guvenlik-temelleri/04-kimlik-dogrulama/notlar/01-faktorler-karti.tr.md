## Dört adım

| Adım | Soru | Örnek |
|---|---|---|
| **Tanımlama** (identification) | Kim olduğunu söylüyor? | Kullanıcı adı |
| **Kimlik doğrulama** (authentication) | Kanıtlıyor mu? | Parola + telefondaki kod |
| **Yetkilendirme** (authorization) | Ne yapabilir? | Notları görebilir, değiştiremez |
| **Kayıt** (accounting) | Ne yaptı? | "10.05'te notlara baktı" |

## Faktörler

| Faktör | Örnek | Dikkat |
|---|---|---|
| **Bilgi** (know) | Parola, PIN | Başka sitelerde tekrar kullanılmış olabilir |
| **Sahiplik** (have) | Kod uygulaması, donanım anahtarı, SMS | SMS en zayıfı (SIM değiştirme) |
| **Varlık** (are) | Parmak izi, yüz | Değiştirilemez; yanlış kabul / yanlış ret |

**MFA = en az iki farklı faktör.** Parola + PIN MFA değildir; parola +
donanım anahtarı MFA'dır.

## Yöntemlerin gücü (zayıftan güçlüye)

1. Yalnızca parola
2. Parola + SMS kodu
3. Parola + uygulamadaki tek kullanımlık kod (TOTP) ya da bildirim onayı
4. Parola + oltalamaya dayanıklı yöntem (donanım anahtarı gibi)

## TOTP'nin parçaları

- Ortak **sır**: hesap kurulurken bir kez paylaşılır, sonra hiç gönderilmez.
- **Sayaç**: `saat // 30`.
- **HMAC-SHA1** → dinamik kesme → `% 10**6` → `zfill(6)`.
- Sunucu saat kaymasına karşı bir önceki ve bir sonraki adımı da kabul
  edebilir.

## Saldırılar ve cevapları

| Saldırı | Cevap |
|---|---|
| Kod tahmini | Deneme sınırı, giderek uzayan bekleme |
| Gerçek zamanlı oltalama | Oltalamaya dayanıklı doğrulama |
| SIM değiştirme | SMS yerine uygulama ya da donanım anahtarı |
| Onay yorgunluğu | Ekrandaki sayıyı telefona yazdırmak, bildirim sınırı |
| Zayıf kurtarma yolu | Yedek kodlar, ikinci cihaz |
