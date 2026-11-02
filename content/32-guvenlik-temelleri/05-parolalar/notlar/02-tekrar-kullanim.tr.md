Bir parolanın ne kadar güçlü olduğu, **başka bir yerde** kullanılmışsa
önemini yitirir. Aynı parolayı on sitede kullanan biri, o on siteden en
zayıf korunanı kadar güvendedir.

## Nasıl olur?

1. Parolaları kötü saklayan küçük bir site sızıntıya uğrar.
2. Kullanıcı adı (çoğu zaman e-posta adresi) ve parola çiftleri bir listeye
   girer ve paylaşılır.
3. Otomatik araçlar bu çiftleri e-posta, banka, alışveriş sitelerinde dener.
   Başarı oranı küçüktür ama liste milyonlarca satırdır.

Saldırgan hiçbir şeyi "kırmaz"; yalnızca başka bir yerde açık kalan anahtarı
dener. Buna **kimlik bilgisi doldurma** (credential stuffing) denir.

## Kullanıcı olarak

- Her site için ayrı parola. Bunun tek pratik yolu bir **parola
  yöneticisi** (password manager): parolaları üretir, şifreli bir kasada
  saklar, giriş sayfasına doldurur.
- Parola yöneticisinin **ana parolası** uzun bir parola cümlesi olsun ve
  hesabında MFA açık olsun.
- E-posta hesabını özellikle koru: öteki hesapların "parolamı unuttum"
  bağlantıları oraya gider.

## Sistem yazan olarak

- Kayıtta ve parola değiştirmede, parolayı **bilinen sızıntı listelerine**
  karşı denetle. Bunu yaparken parolayı başkasına göndermeden denetleyen
  yöntemler kullanılır (yalnızca özetin ilk birkaç karakteri sorulur).
- Bir kullanıcının parolası başka bir sızıntıda göründüyse ondan
  değiştirmesini iste.
- Aynı kaynaktan çok sayıda farklı kullanıcı adına giriş denemesi gelmesi
  doldurma saldırısının işaretidir; kayda geçir ve yavaşlat.
- MFA, doldurma saldırısına karşı en etkili önlemdir: doğru parola tek
  başına yetmez.

## Parola yöneticisi tek nokta değil mi?

Evet, bütün parolalar tek bir kasada. Ama kasa şifreli, ana parola başka
hiçbir yerde kullanılmıyor ve MFA ile korunuyor. Bunun alternatifi aynı
parolanın on yerde durmasıdır; o durumda tek nokta zaten var, üstelik on
farklı sitenin elinde.
