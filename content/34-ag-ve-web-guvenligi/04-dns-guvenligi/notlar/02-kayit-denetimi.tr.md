Bir alanın DNS kayıtları zamanla birikir: denenip bırakılan hizmetler,
eski sunucular, artık kimsenin hatırlamadığı alt adlar. Düzenli bir
gözden geçirme şu soruları sorar.

## Her kayıt için

- **Bu ad hâlâ kullanılıyor mu?** Kullanılmayan alt ad silinir.
- **CNAME hedefi hâlâ bizim mi?** Hedef bir dış hizmetteyse, o hizmette
  hesap ve kaynak hâlâ duruyor mu? Durmuyorsa kayıt sahipsizdir ve hemen
  silinir (alt alan devralma).
- **A kaydının adresi hâlâ bizim mi?** Bulutta bırakılan bir adres başka
  bir müşteriye verilmiş olabilir.
- **TTL makul mü?** Çok uzun TTL, bir değişikliğin ya da yanlış bir kaydın
  geç düzelmesi demektir. Taşıma öncesinde TTL kısaltılır.

## Alan adının kendisi için

- Alan adının kayıtlı olduğu hesapta **MFA** açık mı, kimlerin erişimi var?
- Alanın süresi dolmak üzere mi? Süresi dolan ad başkası tarafından
  alınabilir; otomatik yenileme açık tutulur.
- DNSSEC açık mı?

## Kurum ağında

- Bilgisayarlar hangi çözümleyiciyi kullanıyor? Beklenmeyen bir
  çözümleyiciye giden sorgular ayar ele geçirmenin işareti olabilir.
- Çok uzun ve rastgele görünen alt adlara çok sayıda sorgu
  (`x7f3k9q2.example` gibi) DNS'in veri kaçırmak için kullanıldığını gösterebilir; bu
  sorgular kaydedilir ve incelenir.

## Örnek bulgu

| Kayıt | Sorun | Yapılacak |
|---|---|---|
| `shop.example.com` CNAME eski bir dükkân hizmetine | Hizmet hesabı kapatılmış | Kaydı sil |
| `test.example.com` A eski bir bulut adresine | Adres artık bizim değil | Kaydı sil |
| `example.com` NS | Alan hesabında MFA yok | MFA aç |
