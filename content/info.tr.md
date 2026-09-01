# Odyssey nedir?

Odyssey, veri bilimi ve makine öğrenmesini yapılandırılmış bir müfredat
üzerinden öğreten, çevrimdışı çalışan bir masaüstü uygulamasıdır.

Amacı, dağınık kaynaklar arasında gezinmek yerine tek bir yerde ilerleyen ve
ölçülebilir bir öğrenme akışı sunmaktır: her konunun nerede başlayıp nerede
bittiği bellidir, ilerleme kaydedilir, öğrenilenin sınandığı bir adım vardır.

## Nasıl işliyor?

Her bölüm dört parçadan oluşur: konu anlatımı, ders notları, sınav ve kod
alıştırmaları. Bölüm ancak sınav geçildiğinde ve alıştırmalar çözüldüğünde
tamamlanmış sayılır.

Bölümler sırayla açılır. Bir bölüme geçebilmek için bir öncekinin
tamamlanmış olması gerekir; böylece müfredat, üzerine inşa edildiği temel
olmadan ilerlemez.

Kodu uygulamanın içinde yazarsınız. Çalıştırdığınızda program kodu kendi
ortamında yürütür, çıktısını ve ürettiği değişkenleri denetler, hangi
koşulun sağlandığını ve hangisinin sağlanmadığını tek tek gösterir.

## İlkeler

**Değerlendirme deterministiktir.** Alıştırmalar önceden tanımlanmış
kurallarla denetlenir: çıktı karşılaştırması, değişken ve fonksiyon
denetimleri, kodun yapısına bakan kontroller. Aynı kod her çalıştırmada aynı
sonucu verir. Uygulamada dil modeli, API çağrısı veya ağ bağlantısı
bulunmaz.

**Verileriniz cihazınızda kalır.** İlerleme, yazdığınız kod ve ayarlar
`%APPDATA%\Odyssey` klasöründeki yerel bir veritabanında tutulur. Hiçbir veri
dışarı aktarılmaz. Yeni sürüme geçildiğinde bu klasöre dokunulmaz; ilerleme
korunur.

**Açık kaynaktır.** Uygulama MIT lisansıyla dağıtılır; kaynak kodu
incelenebilir, değiştirilebilir ve yeniden dağıtılabilir.

## Şu an nerede?

Erken geliştirme aşamasındadır. Uygulama uçtan uca çalışır durumdadır:
öğrenme yolu, konu anlatımı, ders notları, sınavlar, kod alıştırmaları,
kademeli ipuçları, ilerleme kaydı, Türkçe/İngilizce arayüz ve açık/koyu tema
hazırdır.

Müfredat genişlemeye devam ediyor. Şu an Python Temelleri modülü yayında;
hedef 23 modüldür. Rozetler, kişisel not alanı ve uygulama içi güncelleme
sistemi yol haritasında yer alıyor.

Hangi değişikliğin hangi sürümde geldiğini **Sürüm Notları** ekranından
izleyebilirsiniz.
