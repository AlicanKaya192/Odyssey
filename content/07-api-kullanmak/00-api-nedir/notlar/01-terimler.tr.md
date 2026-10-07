Bu bölümde geçen terimler, kısa tanımları ve gündelik karşılıklarıyla.

| Terim | Ne demek | Restoranda |
|---|---|---|
| **API** | Bir programın başka programlara açtığı kapı | Garson + menü |
| **İstemci** (client) | Soruyu soran program | Müşteri |
| **Sunucu** (server) | Soruyu bekleyip cevaplayan program | Mutfak |
| **İstek** (request) | İstemcinin gönderdiği soru | Sipariş |
| **Yanıt** (response) | Sunucunun geri gönderdiği cevap | Gelen tabak |
| **Uç nokta** (endpoint) | API'nin belli bir işi yapan tek kapısı | Menüdeki bir yemek |
| **Belgeler** (documentation) | Hangi uç noktaların olduğunu ve nasıl kullanılacağını anlatan metin | Menü |
| **JSON** | API'lerin veriyi yazdığı düzenli metin biçimi | Tabağın düzeni |
| **REST** | En yaygın API tarzı: kaynaklar + HTTP yöntemleri | Restoranın kuralları |
| **404 Not Found** | "Böyle bir kapı yok" yanıtı | "Bizde o yemek yok" |

## Karıştırılanlar

**API ile sunucu aynı şey değil.** Sunucu çalışan program; API onun dışarıya
açtığı kapıların kuralları. Bir sunucunun birden çok API'si olabilir, bir API
birden çok sunucuda çalışabilir.

**API ile web sitesi aynı şey değil.** İkisi de aynı veriyi sunabilir. Site
insanın okuması için süslenmiş sayfa (HTML); API programın okuması için
düzenli veri (çoğunlukla JSON).

**İstemci illa bir uygulama değil.** Tarayıcın, bir Python betiği, başka bir
sunucu, hatta komut satırındaki tek bir komut istemci olabilir. Soran kimse
istemci odur.

**Sunucu illa uzak bir makine değil.** Kendi bilgisayarında çalışan ve istek
bekleyen bir program da sunucu. API 2'de bunu yapacaksın.

## Akılda kalsın

> İçerisi değişebilir, kapı aynı kalır.

API'nin bütün değeri bu cümlede: istemci sunucunun içini bilmeden, yalnızca
kapının kurallarına uyarak çalışır.
