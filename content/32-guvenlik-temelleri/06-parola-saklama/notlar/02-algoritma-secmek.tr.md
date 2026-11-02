Parola saklama algoritması seçerken üç soruya bakılır: tuz kendiliğinden
var mı, ne kadar yavaş ayarlanabiliyor ve bellek harcıyor mu?

| Algoritma | Ayar | Bellek harcar mı? | Not |
|---|---|---|---|
| **PBKDF2** | Yineleme sayısı | Hayır | Standart kütüphanede (`hashlib.pbkdf2_hmac`); yaygın ve onaylı |
| **bcrypt** | Maliyet (cost) çarpanı | Az | Uzun yıllardır kullanılıyor; parolanın ilk 72 baytına bakar |
| **scrypt** | `n`, `r`, `p` | Evet | `hashlib.scrypt` ile gelir |
| **Argon2id** | Zaman, bellek, paralellik | Evet | Yeni sistemlerde genelde ilk öneri |

## Neden bellek?

Parola denemek için çok sayıda basit çekirdeği olan donanım kullanılır.
Her çekirdek kendi denemesini yapar. Algoritma her deneme için bir miktar
bellek isterse çekirdek sayısı belleğe takılır; saldırı pahalılaşır.
PBKDF2 yalnızca zaman harcar, bu yüzden yineleme sayısı yüksek tutulur.

## Parametreleri seçmek

- Sunucunun bir girişte kabul edebileceği süreyi belirle (örneğin birkaç
  yüz milisaniye) ve parametreleri bu süreye göre ayarla.
- Önerilen değerler donanım hızlandıkça yükselir. Güncel değerler için
  OWASP'ın parola saklama kılavuzuna bak.
- Parametreler her kayıtta yazılı olduğu için değiştirmek eski kayıtları
  bozmaz.

## Eski kayıtları yükseltmek

Kullanıcının parolası yalnızca girişte açık olarak elinde. Bu yüzden:

1. Giriş doğrulanınca kaydın algoritmasına ve parametrelerine bak.
2. Eskiyse parolayı yeni algoritma ve parametrelerle yeniden özetle.
3. Yeni kaydı eskisinin yerine yaz.

Uzun süredir giriş yapmayan kullanıcıların düz SHA-256 gibi zayıf
kayıtları kaldıysa, eski özeti yeni algoritmanın içine sarmak (özetin
özeti) bir geçiş yoludur; böylece giriş beklemeden hepsi korunur.

## Yapma

- Kendi "akıllı" özet düzenini uydurma (iki kez SHA-256, tersten yazma).
- Tuzu bütün kullanıcılar için aynı yapma.
- Parolayı kayıt (log) dosyalarına, hata mesajlarına yazma.
- Parola uzunluğunu sınırlarken çok kısa kesme; yavaş özet uzun parolada
  da aynı sürede çalışır (bcrypt'in 72 bayt sınırı hariç).
