Oturum hatalarının ortak noktası, oturum kimliğinin parola kadar değerli
olduğunun unutulmasıdır.

## Tahmin edilebilir kimlik

`s1001`, `s1002`... gibi sıralı ya da zamandan üretilen kimlikler bir
sonrakini ele verir. Kimlik yalnızca `secrets` ile üretilir.

## Girişte yenilenmeyen kimlik

Girişten önce verilen kimlik girişten sonra da kullanılırsa oturum
sabitlemeye açılır. Giriş, yetki yükselmesi ve parola değişimi kimliği
yeniler.

## Hiç bitmeyen oturum

"Beni hatırla" seçeneği aylarca geçerli bir oturum kimliği demek değildir.
Uzun süreli giriş için ayrı, geri çağrılabilir bir jeton tutulur ve
önemli işlemlerde (parola değişimi, ödeme) parola yeniden sorulur.

## Yalnızca tarayıcıda biten çıkış

Çıkış düğmesi çerezi silip sunucudaki kaydı bırakırsa, çerezin bir
kopyasına sahip olan biri devam eder. Sunucu tarafında kayıt silinir.

## Eksik öznitelik

- `Secure` yoksa çerez düz HTTP'de yolda okunur.
- `HttpOnly` yoksa sayfaya sızan bir betik çerezi okuyup gönderir.
- `SameSite` yoksa başka bir siteden başlatılan isteğe çerez eklenir.

## Kimliği yanlış yerde taşımak

- URL'de (`/cart?sid=...`): geçmişe, sunucu kayıtlarına ve başka sitelere
  giden `Referer` başlığına yazılır.
- Kayıt dosyasında: kayıtları okuyabilen herkes oturumu ele geçirir.

## İmzasız durum çerezi

`role=user` gibi bir değeri imzasız çerezde tutmak, kullanıcıya rolünü
kendisi seçme izni vermektir. Ya sunucuda tutulur ya da imzalanır.

## Hızlı kontrol

- [ ] Kimlik `secrets` ile, en az 128 bit.
- [ ] Girişte kimlik yenileniyor.
- [ ] Boşta kalma ve mutlak süre var.
- [ ] Çıkış sunucudaki kaydı siliyor.
- [ ] Çerezde `Secure`, `HttpOnly`, `SameSite`.
- [ ] Kimlik URL'de ve kayıtlarda yok.
