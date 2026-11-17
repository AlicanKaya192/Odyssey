## Bu modülden sonra

Bu modülün bütün ağları **tam bağlıydı**: her girdi sayısı bir sonraki
katmanın her nöronuna bağlı. Düz bir özellik listesi için doğal bir seçim,
ama resim, ses ve metin gibi **yapısı olan** verinin yapısını kullanmıyor.
Sonraki iki modül bu yapıyı kullanan ağları anlatıyor:

- **Bilgisayarlı Görü:** evrişim (convolution) ile resmin komşu piksellerini
  birlikte işleyen ağlar, veri artırma, hazır modellerle aktarımlı öğrenme
  (bu modülde gördüğün `strict=False` ve dondurma burada iş görür), nesne
  algılama ve bölütleme.
- **Diziler, Üretken Modeller ve Dağıtım:** sıralı veri için yinelemeli
  ağlar ve Transformer (gradyan kırpma ve LayerNorm burada her yerde),
  otomatik kodlayıcılar ve üretken modeller, eğitilmiş bir modeli
  hızlandırmak, küçültmek ve sunmak.

## Kendi başına denemek için

- Rakam sınıflandırıcısının gizli katmanını 16, 64 ve 256 nöronla dene;
  doğrulama kaybı ve parametre sayısı nasıl değişiyor?
- Bitirme projesinde dropout'u kaldır, sonra `weight_decay` ekle; erken
  durdurma kaçıncı turda devreye giriyor?
- Tablo verisinde öğrenme oranını 0,001'den 1'e kadar onar kat büyüterek
  dene ve her birinde tek kümeyi ezberletme denemesini yap.
- Kendi seçtiğin küçük bir CSV veri setini `Dataset` sınıfıyla yükle ve
  Hızlı Başvuru'daki `fit` iskeletiyle eğit.

## Akılda kalacak üç şey

- Önce sayılara bak: şekil, tür, başlangıç kaybı.
- Doğrulama kümesi seçim için, test kümesi bir kez ve en sonda.
- Bir model dosyasını yalnızca `weights_only=True` ile yükle.
