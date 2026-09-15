`order_items.order_id` sütununu `orders.id`'ye bağlayan bir yabancı
anahtar ekle.

Tablo zaten var ve içinde veri duruyor — yeniden kurma, `ALTER TABLE` ile
bağı ekle.

Önceki bölümde 1006 numaralı siparişi kalemleriyle silerken sıranın
önemli olduğunu, ama sunucunun ters sıraya da izin verdiğini görmüştün:
bağ tanımlı değildi. Bağ eklenince bu değişiyor.

Kontrol iki şeye bakıyor: bağın doğru sütundan doğru tabloya kurulup
kurulmadığına ve 1006 numaralı siparişi silmeyi denediğinde sunucunun
bunu **reddedip reddetmediğine**.
