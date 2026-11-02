## Türler

| Tür | Kanal | Kısaca |
|---|---|---|
| **Oltalama** (phishing) | E-posta | Toplu sahte mesaj |
| **Hedefli oltalama** (spear phishing) | E-posta | Kişiye özel hazırlanmış |
| **Balina avı** (whaling) | E-posta | Üst yöneticilere |
| **Smishing** | SMS | Kısa mesajla oltalama |
| **Vishing** | Telefon | Sesli arama ile |
| **Bahane** (pretexting) | Her kanal | İnandırıcı bir hikâye |
| **İş e-postası dolandırıcılığı** (BEC) | E-posta | Ödemeyi başka hesaba yönlendirmek |
| **Yemleme** (baiting) | Fiziksel | Bırakılan USB bellek |
| **Kuyruğa takılma** (tailgating) | Fiziksel | Kartlı kapıdan birinin arkasından girmek |
| **Omuz sörfü** (shoulder surfing) | Fiziksel | Ekrana ya da klavyeye bakmak |

## Kaldıraçlar

Otorite, aciliyet, korku, merak, yardımseverlik, sosyal kanıt, kıtlık.
Hepsi aynı şeyi ister: **hemen** harekete geç.

## Adres okumak

- Adres **sağdan sola** okunur: `a.b.okul.example` okulundur,
  `okul.example.b.test` değildir.
- `@` işaretinden önceki kısım sunucu değildir.
- Tire, nokta, rakam ve benzer harf oyunlarına dikkat: `school-example`,
  `examp1e`, `rn` → `m`.
- Python: `urlsplit(url).hostname`; aitlik için `host == domain or
  host.endswith("." + domain)`.

## Ne yapmalı?

1. Dur: mesaj acele ettiriyor mu?
2. Doğrula: kayıtlı numarayı ara, adresi kendin yaz.
3. Bildir: "oltalama bildir" düğmesi ya da güvenlik ekibi.
4. Tıkladıysan hemen söyle: parolayı değiştir, oturumları kapat.

## Savunma katmanları

İnsan (eğitim, suçlamayan kültür) · süreç (geri arama, kimlik doğrulama) ·
teknik (filtre, SPF/DKIM/DMARC, dış gönderen etiketi, oltalamaya dayanıklı
MFA) · bildirim.
