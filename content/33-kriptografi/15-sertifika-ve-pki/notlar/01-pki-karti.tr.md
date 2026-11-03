## Parçalar

| Parça | Görevi |
|---|---|
| Sertifika | Açık anahtarı bir ada bağlar; CA imzalar |
| CA (sertifika otoritesi) | Adın sahibini denetleyip sertifikayı imzalar |
| Kök CA | Güven deposunda önceden bulunan, kendini imzalamış otorite |
| Ara CA | Kökün imzaladığı, siteleri imzalayan otorite |
| Güven deposu | İşletim sisteminin ya da tarayıcının güvendiği kökler |
| CRL / OCSP | İptal edilen sertifikaları duyurur |
| Şeffaflık kayıtları | Verilen her sertifikanın herkese açık kaydı |

## Doğrulama sırası

1. Zinciri kur: site → ara CA → kök.
2. Her halkada: `issuer` bir üstün `subject`'i mi, imza bir üstün açık
   anahtarıyla tutuyor mu?
3. Kök güven deposunda mı?
4. Bugün `not_before` ile `not_after` arasında mı?
5. Ad (SAN listesi) bağlanılan adla eşleşiyor mu? Joker yalnızca tek
   etiket: `*.example.test` → `shop.example.test` evet,
   `a.b.example.test` hayır.
6. İptal edilmiş mi?

Birinde bile düşerse bağlantı **kurulmaz**.

## İmzalanan baytlar

İmza, sertifikanın `signature` dışındaki alanlarının **her seferinde aynı
biçimde** kodlanmış hâlinin üzerinedir. Gerçek sertifikalar bunun için
ASN.1 DER kodlaması kullanır; derste aynı işi `json.dumps(...,
sort_keys=True)` yaptı.
