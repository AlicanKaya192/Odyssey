Bulutta kaynaklar dakikalar içinde açılır ve kapanır. Bu hız, güvenlik
için hem bir fırsat hem de bir zorluktur: yanlış bir yapılandırma da aynı
hızla yayılır. Bu not bulutta görünürlüğü ve hesapların korunmasını
topluyor.

## Hesap, her şeyin anahtarıdır

Bulutta yönetim paneline ya da programlı erişime sahip bir hesap, veri
merkezinin anahtarı gibidir. Bu yüzden:

- **Kök (root) hesap** günlük iş için kullanılmaz; çok faktörlü doğrulamayla
  korunur ve kasada bekler.
- Her kişi ve her uygulama **kendi** hesabıyla, en az yetkiyle çalışır.
- Uzun ömürlü **erişim anahtarları** yerine mümkünse kısa ömürlü kimlik
  bilgileri kullanılır (Sır Yönetimi bölümü); eski anahtarlar düzenli
  yenilenir ya da kaldırılır.
- Anahtarlar koda ve depoya yazılmaz: bulut anahtarı sızan depolar,
  sızıntı tarayıcılarının en çok aradığı şeydir.

## Görünürlük

Bulut sağlayıcıları, hesapta yapılan her yönetim işlemini (kim, ne zaman,
hangi kaynağı değiştirdi) kaydeden **denetim kayıtları** sunar. Bu kayıtlar:

- açık olmalı ve bütün bölgeleri kapsamalıdır,
- değiştirilemeyecek, ayrı bir hesapta ya da alanda saklanmalıdır,
- Kayıt ve İzleme bölümündeki gibi merkezî kayıt sistemine gönderilmelidir.

Bulutta izlenmesi gereken bazı olaylar:

| Olay | Neden önemli? |
|---|---|
| Kök hesabın kullanılması | Neredeyse hiç kullanılmamalı |
| Denetim kaydının kapatılması | Saldırgan izini silmek isteyebilir |
| Bir depolama alanının herkese açılması | Olası sızıntı |
| Yeni bir yönetici yetkisi | Yetki yükseltme olabilir |
| Alışılmadık bölgede kaynak açılması | Ele geçirilmiş hesap belirtisi |

## Sürekli denetim

Bulut yapılandırması sürekli değiştiği için bir kez denetlemek yetmez.
Yapılandırmayı belirli kurallara göre sürekli tarayan araçlar, kural dışı
bir değişiklik olduğunda uyarı üretir ya da onu kendiliğinden geri alır.
Bu, İşletim Sistemi Güvenliği bölümündeki güvenlik taban çizgisinin bulut
karşılığıdır.

## Çıkış planı

Bir sağlayıcıya bağımlı olmak da bir risktir: hizmet kesintisi, fiyat
değişikliği ya da sözleşme sonu. Verinin dışarıya alınabilir biçimde
yedeklenmesi (Yedek ve Felaket Kurtarma bölümü) ve kritik sistemlerin
başka bir bölgeye taşınabilmesi bu riski azaltır.
