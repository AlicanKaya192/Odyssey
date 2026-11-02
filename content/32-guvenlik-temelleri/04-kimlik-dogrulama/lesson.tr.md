# Kimlik Doğrulama ve MFA

Bir sisteme girdiğinde önce kim olduğunu söylersin, sonra bunu
kanıtlarsın. Ancak ondan sonra sistem ne yapabileceğine karar verir. Bu üç
adım sık karıştırılır, ama her biri ayrı bir iştir ve her birinin ayrı
açıkları vardır.

<figure class="fig"><div class="flow">
  <span class="node">Tanımlama</span><span class="arrow">→</span>
  <span class="node acc">Kimlik doğrulama</span><span class="arrow">→</span>
  <span class="node">Yetkilendirme</span><span class="arrow">→</span>
  <span class="node">Kayıt</span>
</div><figcaption>"Ben Ada'yım" → "kanıtı bu" → "Ada notları görebilir" → "Ada 10.05'te notlara baktı".</figcaption></figure>

- **Tanımlama** (identification): kim olduğunu **söylemek**. Kullanıcı
  adı, e-posta adresi, öğrenci numarası. Herkes herhangi bir ad yazabilir;
  tanımlama tek başına hiçbir şey kanıtlamaz.
- **Kimlik doğrulama** (authentication): söylediğini **kanıtlamak**.
  Parola, telefondaki kod, parmak izi.
- **Yetkilendirme** (authorization): kimliği doğrulanan kişinin **neyi
  yapabileceğine** karar vermek. Kendi bölümleri var (Yetkilendirme,
  Erişim Denetimi Modelleri).
- **Kayıt** (accounting): kimin ne yaptığını yazmak; hesap
  verebilirliğin temeli.

Bu bölüm ikinci adımla, kimlik doğrulamayla ilgileniyor.

## Üç tür kanıt: faktörler

Kim olduğunu kanıtlamanın üç temel yolu var. Her birine **faktör** (factor)
denir:

| Faktör | Soru | Örnekler | Zayıf yanı |
|---|---|---|---|
| **Bilgi** (something you know) | Ne biliyorsun? | Parola, PIN, güvenlik sorusu | Tahmin edilir, çalınır, başka sitede de kullanılmıştır |
| **Sahiplik** (something you have) | Neyin var? | Telefon, kod üreten uygulama, donanım anahtarı | Kaybolur, çalınır |
| **Varlık** (something you are) | Nesin? | Parmak izi, yüz, ses | Değiştirilemez; sızarsa yenisi yoktur |

Biyometrik doğrulamanın ayrı bir sorunu var: kusursuz değildir. Bazen
yabancıyı kabul eder (**yanlış kabul**, false accept), bazen sahibini
reddeder (**yanlış ret**, false reject). Birini azaltmak ötekini artırır.
Ayrıca bir parola sızarsa değiştirilir; parmak izi değiştirilemez. Bu
yüzden biyometri çoğu zaman cihazın kilidini açmak gibi yerel işlerde, tek
başına değil başka bir faktörle birlikte kullanılır.

## Çok faktörlü kimlik doğrulama

**Çok faktörlü kimlik doğrulama** (multi-factor authentication, MFA), en
az **iki farklı türden** faktör istemektir. İki faktörlüsüne **2FA** da
denir. Önemli kelime "farklı": iki parola istemek MFA değildir, çünkü aynı
saldırı (örneğin sahte bir giriş sayfası) ikisini birden çalabilir.
Parola ve telefon ise ayrı saldırılar ister.

```python
FACTORS = {"password": "know", "pin": "know", "sms_code": "have",
           "app_code": "have", "security_key": "have", "fingerprint": "are"}

for methods in [["password"], ["password", "pin"], ["password", "app_code"],
                ["security_key", "fingerprint"]]:
    kinds = {FACTORS[m] for m in methods}
    print(methods, "MFA" if len(kinds) >= 2 else "not MFA")
```

```text
['password'] not MFA
['password', 'pin'] not MFA
['password', 'app_code'] MFA
['security_key', 'fingerprint'] MFA
```

`kinds` bir küme (set): aynı tür ikinci kez eklenince küme büyümez. Parola
ve PIN iki ayrı yöntem ama ikisi de "bilgi"; küme tek elemanlı kaldı.

## Tek kullanımlık kodlar nasıl üretilir?

Telefondaki kod üreten uygulamalar her 30 saniyede bir değişen altı haneli
bir kod gösterir. Bu kodlar internet bağlantısı olmadan da üretilir. Nasıl
oluyor da sunucu aynı kodu bilir? Hesap kurulurken sunucu ile telefon
ortak bir **sır** (secret) paylaşır. Sonra ikisi de aynı hesabı yapar.

Bu yöntemin adı **HOTP** (HMAC-based one-time password). HMAC, bir sır ile
bir mesajdan sabit uzunlukta bir değer üreten yapı; Kriptografi modülünde
ayrıntısıyla göreceğiz. Burada adımlarına bakalım. Sır, standardın kendi
deneme değeri:

```python
import hashlib
import hmac

secret = b"12345678901234567890"
counter = 0
digest = hmac.new(secret, counter.to_bytes(8, "big"), hashlib.sha1).digest()
offset = digest[-1] & 0x0F
number = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
print("digest bytes:", len(digest))
print("offset:", offset)
print("code:", str(number % 10**6).zfill(6))
```

```text
digest bytes: 20
offset: 0
code: 755224
```

Adım adım:

1. Sayaç (counter) 8 baytlık bir sayıya çevrilir ve sır ile birlikte
   HMAC'ten geçirilir; 20 baytlık bir sonuç çıkar.
2. Son baytın son 4 biti (`& 0x0F`) 0 ile 15 arasında bir **konum** verir.
   Sonucun o konumdan başlayan 4 baytı alınır; buna "dinamik kesme"
   (dynamic truncation) denir.
3. Bu 4 bayt bir sayıya çevrilir, en üst bit atılır (`& 0x7FFFFFFF`) ve
   son altı basamak alınır. Kod `0` ile başlayabilir; `zfill(6)` baştaki
   sıfırları korur.

Bu kod, standardın sayaç 0 için yazdığı değerle aynı: `755224`.

**TOTP** (time-based one-time password) aynı hesaptır, tek farkla: sayaç
olarak saat kullanılır. Saat (1970'ten beri geçen saniye) 30'a bölünür ve
tam kısmı alınır; böylece sayaç her 30 saniyede bir artar:

```python
for seconds in [0, 29, 30, 59, 60]:
    print(seconds, "->", seconds // 30)
```

```text
0 -> 0
29 -> 0
30 -> 1
59 -> 1
60 -> 2
```

Telefon ile sunucunun saati biraz farklı olabilir. Bu yüzden sunucular
çoğu zaman bir önceki ve bir sonraki adımın kodunu da kabul eder.

## Kod kısa, deneme sayısı sınırlı olmalı

Altı haneli bir kodun bir milyon olası değeri var. Az görünmez, ama
saldırgan sınırsız deneyebilirse sorun olur. Her 30 saniyelik pencerede 5
deneme yapılabilen bir sistemi bir gün boyunca denemek:

```python
codes = 10**6
tries_per_window = 5
windows_per_day = 24 * 60 * 2
miss_all = (1 - tries_per_window / codes) ** windows_per_day
print(f"one day:  {1 - miss_all:.4f}")
print(f"one year: {1 - miss_all ** 365:.4f}")
```

```text
one day:  0.0143
one year: 0.9948
```

Bir günde yüzde 1'den biraz fazla, ama bir yılda neredeyse kesin. Kodun
gücü, deneme sayısını sınırlayan önlemle birlikte anlamlıdır: art arda
belli sayıda yanlıştan sonra **kilitlemek** (lockout) ya da bekletmek
(rate limiting).

Kilitlemenin de bir bedeli var: saldırgan bilerek yanlış deneyip gerçek
kullanıcının hesabını kilitleyebilir (bu da bir erişilebilirlik saldırısı).
Bu yüzden kalıcı kilit yerine çoğu zaman giderek uzayan bekleme süreleri
kullanılır.

## MFA da aşılabilir

MFA bir hesabı ele geçirmeyi çok zorlaştırır, ama sihir değildir:

- **Gerçek zamanlı oltalama** (real-time phishing): sahte giriş sayfası
  hem parolayı hem kodu alıp hemen gerçek siteye iletir. Kod 30 saniye
  geçerli olduğu için bu süre yeter.
- **SMS kodları:** telefon hattı başka bir SIM karta taşınabilir (SIM
  değiştirme, SIM swap); kodlar saldırgana gider.
- **Onay yorgunluğu** (MFA fatigue): telefona art arda "giriş onaylansın
  mı?" bildirimi gönderilir; bıkan kullanıcı sonunda "onayla"ya basar.

Bunlara karşı en güçlü yöntem **oltalamaya dayanıklı** (phishing-resistant)
doğrulamadır: donanım anahtarı gibi yöntemler kodu kullanıcıya göstermez,
girişin yapıldığı sitenin adresini de hesaba katar. Sahte sitede üretilen
cevap gerçek sitede işe yaramaz.

## Zayıf halka: kurtarma

Parolasını unutan ya da telefonunu kaybeden biri hesabına geri dönebilmeli.
Ama **hesap kurtarma** (account recovery) yolu, giriş kapısından zayıfsa
saldırgan o yolu kullanır. Annenin kızlık soyadı gibi güvenlik soruları
çoğu zaman sosyal medyadan bulunabilir. İyi kurtarma yolları: hesap
açılırken verilen ve güvenli yerde saklanan **yedek kodlar**, ikinci bir
kayıtlı cihaz ya da kimliğin yüz yüze doğrulanması.

## Özet

- **Tanımlama** söylemek, **kimlik doğrulama** kanıtlamak,
  **yetkilendirme** izin vermektir.
- Üç faktör: **bilgi**, **sahiplik**, **varlık**. MFA en az iki **farklı**
  faktör ister; iki parola MFA değildir.
- HOTP/TOTP kodları ortak bir sır ve bir sayaçtan (ya da saatten) HMAC ile
  üretilir.
- Kısa kodlar ancak deneme sayısı sınırlıysa güçlüdür; kilitleme ölçülü
  olmalı.
- MFA oltalanabilir; en güçlüsü oltalamaya dayanıklı yöntemlerdir.
  Kurtarma yolu da giriş kadar güçlü olmalı.
