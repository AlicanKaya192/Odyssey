Bir giriş sayfası kimlik doğrulamanın en çok saldırı alan yeridir. Kendi
yazdığın ya da incelediğin bir giriş sayfasında şunlara bak.

## Hata mesajları

- "Kullanıcı bulunamadı" ve "parola yanlış" diye **iki ayrı mesaj** verme.
  Saldırgan bu farkla hangi kullanıcı adlarının var olduğunu öğrenir; buna
  **kullanıcı adı numaralandırma** (user enumeration) denir.
- Tek mesaj yeter: "Kullanıcı adı ya da parola yanlış."
- Aynı fark cevap süresinde de olmasın: var olmayan kullanıcıda hiç hesap
  yapılmazsa cevap daha hızlı döner ve yine aynı bilgiyi verir.

## Deneme sınırı

- Art arda yanlış denemeleri hem **hesap başına** hem de **kaynak başına**
  say.
- Kalıcı kilit yerine giderek uzayan bekleme (1 sn, 2 sn, 4 sn...) kullan;
  böylece saldırgan gerçek kullanıcıyı kilitleyemez.
- Kilitlenen ya da çok sayıda yanlış alan hesapları kayda geçir; tespit
  edici önlem.

## Parola sıfırlama

- Sıfırlama bağlantısı tek kullanımlık ve kısa ömürlü olsun.
- "Bu e-posta kayıtlı değil" deme; "kayıtlıysa bağlantı gönderildi" de.
- Parola değişince açık oturumları kapat.

## MFA

- MFA'yı yalnızca girişte değil, e-posta ya da parola değiştirmek gibi
  hassas işlemlerde de iste.
- Yedek kodları bir kez göster, özet (hash) olarak sakla ve her birini
  tek kullanımlık yap.
- Kullanıcının MFA'yı kapatması da yeniden doğrulama gerektirsin.

## Taşıma

- Giriş sayfası yalnızca şifreli bağlantı (HTTPS) üzerinden açılsın.
  Parola düz bağlantıda giderse yoldaki herkes okuyabilir (Ağ ve Web
  Güvenliği modülü).
