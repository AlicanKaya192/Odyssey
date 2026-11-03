Bir ağı bölmeye başlarken sorulacak sorular ve küçük bir örnek plan.

## Adım adım

1. **Varlıkları listele:** hangi cihaz ve sunucular var, hangisi en
   değerli (veritabanı, yedek, yönetim arayüzleri)?
2. **Bölgelere ayır:** aynı güven düzeyindeki ve aynı işi yapan cihazlar
   aynı bölgeye. İnternete hizmet veren DMZ'ye, misafirler ayrı bölgeye.
3. **Akışları yaz:** hangi bölge hangi bölgeye, **hangi portla** konuşmak
   zorunda? Her satırın bir gerekçesi olsun.
4. **Varsayılan reddet:** listede olmayan her akış kapalı.
5. **İzle:** bölgeler arası reddedilen denemeler kaydedilir; bir
   çalışan bilgisayarının sunucu bölgesinde tarama yapması bir olaydır.

## Örnek plan

| Bölge | Ağ | Kim |
|---|---|---|
| DMZ | `10.10.0.0/24` | Web sunucusu |
| Sunucular | `10.20.0.0/24` | Veritabanı |
| Çalışanlar | `10.30.0.0/24` | Dizüstüler |
| Misafir | `10.99.0.0/24` | Ziyaretçiler |

| Kaynak | Hedef | Port | Gerekçe |
|---|---|---|---|
| İnternet | DMZ | 443 | Web sitesi |
| DMZ | Sunucular | 5432 | Web sunucusu veritabanını okur |
| Çalışanlar | DMZ | 443 | İç kullanıcılar da siteyi açar |
| Misafir | İnternet | 80, 443 | Yalnızca internet |

Geri kalan her şey reddedilir. İnternetten sunuculara, misafirden
çalışanlara yol yoktur.

## Sık hatalar

- **Bölge var, kural yok:** ağlar ayrılmış ama aralarındaki güvenlik
  duvarı "her şeye izin" diyor. Bölümleme kâğıtta kalır.
- **Yönetim arayüzü herkese açık:** bütün bölgelerden yazıcının ya da
  kameranın yönetim sayfasına erişilebiliyor.
- **Yedekler aynı bölgede:** saldırgan sunuculara ulaşınca yedeklere de
  ulaşıyor.
- **VPN'den gelene her şey açık:** VPN bir bölge gibi ele alınır; ondan da
  yalnızca gereken akışlar.
- **Tek yol gözden kaçar:** dar yol (web sunucusu → veritabanı) en çok
  korunacak ve izlenecek yerdir.
