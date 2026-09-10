1006 numaralı siparişi **tamamen** sil: hem siparişin kendisini hem
de ona ait kalemleri.

Sonuçta dokuz sipariş ve on dokuz sipariş kalemi kalmalı.

İki komut yazacaksın. **Sırası önemli: önce kalemler, sonra sipariş.**

Sipariş silinip kalemleri kalırsa ortada hiçbir siparişe bağlanmayan
satırlar kalıyor. `order_items` içindeki `1006` artık var olmayan bir
şeyi işaret ediyor ve bu satırları bir daha kimse fark etmiyor — çünkü
onları bulmanın yolu, olmayan siparişi aramaktan geçiyor.

Bu veritabanında bağlar **tanımlı değil**, o yüzden sunucu ters sıraya
da izin veriyor: yanlış sırayla silsen hata almazsın. Bir sonraki bölümde
bağları tanımlamayı öğrenecek ve sunucunun bu sırayı kendiliğinden
zorunlu kıldığını göreceksin.
