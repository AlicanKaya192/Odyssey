XSS savunmasında yapılan hataların çoğu, doğru aracı yanlış yerde
kullanmaktan çıkar.

## Girdiyi kaydederken kodlamak

Yorumu veritabanına `html.escape` ile kaydetmek ilk bakışta güvenli
görünür ama iki sorun doğurur: aynı metin bir JSON cevabına ya da e-postaya
giderken `&lt;` gibi garip karakterlerle çıkar, ve bir gün kodlanmadan
kaydedilmiş eski bir kayıt kodlanmadan ekrana gelir. Veri olduğu gibi
saklanır, **gittiği yere yazılırken** o yerin kurallarına göre kodlanır.

## Kara liste süzgeci

`<script>` kelimesini silen ya da reddeden bir süzgeç XSS'i durdurmaz:
betik çalıştırmanın tek yolu `<script>` etiketi değildir ve tarayıcılar
yazımdaki birçok farkı hoş görür. Kara liste hep bir şeyi unutur; çıktı
kodlama ise bütün işaretleri etkisizleştirir.

## Yalnızca HTML gövdesini düşünmek

`html.escape` bir öznitelik değerinde, değer tırnaksız yazılmışsa yetmez;
bağlantı adresinde şemayı denetlemez; betik bloğunun içinde hiç uygun
değildir. Önce "bu değer sayfada nereye gidiyor?" sorulur.

## Kodlamayı kapatan işaretler

Şablon motorlarının "bu değer güvenli, kodlama" anlamına gelen işaretleri
yalnızca **geliştiricinin kendi yazdığı** HTML için kullanılır.
Kullanıcıdan gelen bir değere bu işaretin konduğu her satır incelemede
soru işareti alır.

## CSP'ye güvenip kodlamayı bırakmak

CSP ikinci katmandır. `'unsafe-inline'` eklenmiş, her yerden betiğe izin
veren ya da hiç `script-src` içermeyen bir politika koruma sağlamaz; doğru
bir politika bile her açığı kapatmaz.

## İncelemede bakılacaklar

- [ ] Kullanıcı verisi HTML'e f-string ya da `+` ile mi giriyor?
- [ ] Şablonda kodlamayı kapatan bir işaret var mı, neye konmuş?
- [ ] `href` ve `src` değerlerinde şema denetleniyor mu?
- [ ] Sayfanın JavaScript'i adresten ya da girdiden aldığı metni HTML
  olarak mı yazıyor (DOM tabanlı)?
- [ ] CSP başlığı var mı, `'unsafe-inline'` içeriyor mu?
- [ ] Oturum çerezi `HttpOnly` mi?
