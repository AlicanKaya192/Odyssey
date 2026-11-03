Bir web sitesini yayına almadan önce HTTP ve HTTPS tarafında bakılacaklar.

## Taşıma

- [ ] Site yalnızca HTTPS'ten sunuluyor; düz HTTP yalnızca `301` ile
  HTTPS'e yönlendiriyor.
- [ ] Yönlendirme yolu ve sorguyu koruyor, başka bir alan adına
  götürmüyor.
- [ ] `Strict-Transport-Security` başlığı var; `max-age` en az bir yıl.
  Bütün alt alanlar HTTPS'e hazırsa `includeSubDomains`.
- [ ] Sertifika geçerli, süresi dolmadan yenileniyor (otomatik yenileme).
- [ ] Sayfadaki her betik, stil ve resim `https://` ile yükleniyor.

## İstekler

- [ ] Durum değiştiren hiçbir iş `GET` ile yapılmıyor.
- [ ] Sunucu istekteki hiçbir alana (gizli form alanı, başlık, çerez)
  doğrulamadan güvenmiyor.
- [ ] Parola, jeton gibi gizli değerler **URL'de** taşınmıyor: adresler
  tarayıcı geçmişine, sunucu kayıtlarına ve başka sitelere giden
  `Referer` başlığına yazılır. Gövdede ya da başlıkta taşınır.

## Cevaplar

- [ ] Hata sayfaları yığın dökümü, dosya yolu, SQL sorgusu göstermiyor.
- [ ] `Server` gibi başlıklar sürüm numarası vermiyor.
- [ ] Başkasına ait bir kaynak istendiğinde varlığını ele vermemek için
  404 dönüyor.

## Sık yanlışlar

- **"Kilit var, güvenli":** kilit bağlantıyı anlatır; oltalama sitesinin
  de kilidi olur.
- **"Giriş sayfası HTTPS, gerisi HTTP olabilir":** oturum çerezi düz HTTP
  sayfalarında yolda okunur. Bütün site HTTPS.
- **"HSTS'yi bir dakikalık denedik":** kısa `max-age` korumaz; önce kısa
  süreyle denenip sonra uzatılır.
