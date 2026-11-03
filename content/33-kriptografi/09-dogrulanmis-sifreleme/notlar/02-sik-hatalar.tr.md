Doğrulanmış şifrelemenin hataları çoğu zaman algoritmada değil, onun
çevresindeki kodda olur.

| Hata | Neden sorun | Doğrusu |
|---|---|---|
| Etiketi doğrulamadan çözmek | Değiştirilmiş veri işlenir | Önce `compare_digest`, sonra çöz |
| Etiketi `==` ile karşılaştırmak | Karşılaştırma süresi bilgi sızdırabilir | `hmac.compare_digest` |
| Etiketi yalnızca şifreli metinden almak, nonce'u katmamak | Nonce değiştirilirse fark edilmez | Etiket nonce + şifreli metin üzerinden |
| Aynı anahtarı şifreleme ve MAC için kullanmak | İki işlem birbirini zayıflatabilir | Ayrı anahtarlar, tek ana sırdan türetilmiş |
| AAD'yi etikete katmamak | Başlık değiştirilebilir | AAD uzunluğuyla birlikte etikete girer |
| Kütüphanenin "etiket tutmadı" hatasını yutmak | Bütün koruma boşa gider | Hata olursa veri atılır, kullanılmaz |
| Nonce'u tekrarlamak | GCM'de gizlilik ve doğrulama bozulur | Her mesajda benzersiz nonce |
| Kendi birleşimini yazmak | Sıralama ve sınır hataları kolay | Denenmiş bir AEAD kütüphanesi |

## Reddederken ne söylenir

- Etiket tutmadığında kullanıcıya ya da gönderene **neden** reddedildiğini
  ayrıntılı söyleme ("etiket şu baytta farklı" gibi). Tek bir genel
  "geçersiz mesaj" yeter.
- Reddedilen paketin içeriğini kayıtlara yazma; ama reddin kendisini kaydet
  (Güvenlik İlkeleri bölümündeki güvenli başarısızlık).

## Bu derste ne kaldı

Oyuncak şifre ve elle kurulan önce şifrele, sonra MAC yalnızca fikri
göstermek içindi. Gerçek bir programda AES-GCM ya da ChaCha20-Poly1305,
denenmiş bir kütüphaneden ve tek bir çağrıyla kullanılır.
