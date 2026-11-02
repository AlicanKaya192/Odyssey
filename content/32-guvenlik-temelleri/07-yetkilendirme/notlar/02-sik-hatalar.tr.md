Yetkilendirme hataları çoğu zaman tek satırdır ve test ederken fark
edilmez: test eden kişi zaten kendi verisine bakıyordur. Sık görülenler:

## Yalnızca arayüzde denetlemek

Yönetici menüsü sıradan kullanıcıdan gizlenmiş, ama menünün çağırdığı
adres herkese açık. Kullanıcı isteği elle gönderince işlem yapılıyor.
**Düzeltme:** denetimi isteği işleyen koda koy; arayüzdeki gizleme yalnızca
kolaylık.

## İstemciye güvenmek

İstekle birlikte gelen `role=admin` alanı, gizli bir form alanı ya da
çerezde düz yazılmış bir rol değeri kullanılıyor. Bunların hepsini
kullanıcı değiştirebilir. **Düzeltme:** rolü sunucudaki kullanıcı
kaydından oku.

## Nesne sahibini sormamak (IDOR)

`/orders/5512` adresi siparişi getiriyor, ama siparişin bu kullanıcıya ait
olup olmadığı sorulmuyor. **Düzeltme:** sorguya sahibi de ekle ("bu
kullanıcının 5512 numaralı siparişi") ve bulunamazsa "yok" de.

Sıra numarası yerine tahmin edilemeyen kimlikler (uzun rastgele değerler)
kullanmak işi zorlaştırır ama denetimin **yerine geçmez**; kimlik bir
bağlantıda paylaşılınca yine açılır.

## Toplu işlemleri unutmak

Tek kayıt silme denetleniyor, "seçilenleri sil" denetlenmiyor. Ya da
listeleme sayfası filtreliyor ama dışa aktarma (CSV indir) her şeyi
veriyor. **Düzeltme:** aynı karar fonksiyonunu her yolda çağır.

## Varsayılan izin

Yeni eklenen bir uç noktada denetim yazılmamış, çünkü "sonra eklenecek".
**Düzeltme:** çatı (framework) düzeyinde varsayılanı "giriş ve izin
gerekir" yap; herkese açık olacak uç nokta açıkça işaretlensin.

## Hata mesajıyla bilgi vermek

Başkasının faturası istenince "yetkiniz yok", olmayan fatura istenince
"bulunamadı" demek, hangi numaraların var olduğunu söyler. **Düzeltme:**
ikisine de aynı cevabı ver ("bulunamadı").
