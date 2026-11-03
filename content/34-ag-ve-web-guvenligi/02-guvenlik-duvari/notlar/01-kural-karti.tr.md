## Bir kuralın parçaları

| Alan | Örnek | Anlamı |
|---|---|---|
| Eylem | `allow` / `deny` | Ne yapılacak |
| Yön | içeri / dışarı | Hangi trafiğe bakılıyor |
| Protokol | `tcp`, `udp`, `any` | Taşıma protokolü |
| Kaynak | `192.168.1.0/24` | Paketin geldiği adres ya da ağ |
| Hedef | `203.0.113.7/32` | Paketin gittiği adres ya da ağ |
| Port | `443` | Hedef port |
| Kayıt | açık / kapalı | Tutan paket kaydedilsin mi |

`0.0.0.0/0` bütün adresler, `/32` tek bir adres demektir.

## Karar nasıl verilir?

1. Kurallar yukarıdan aşağıya denenir.
2. **İlk tutan kural** kararı verir; gerisine bakılmaz.
3. Hiçbiri tutmazsa **varsayılan**: reddet.

## Türler

| Tür | Neye bakar? | Not |
|---|---|---|
| Durumsuz süzgeç | Tek paketin başlıkları | Cevaplar için geniş delik gerekir |
| Durumlu güvenlik duvarı | Başlıklar + bağlantı tablosu | Bugünkü varsayılan |
| Bilgisayar güvenlik duvarı | O bilgisayarın trafiği | İçeriden gelene de bakar |
| WAF | HTTP isteğinin içeriği (OSI 7) | Ek katman; uygulamadaki açığı kapatmaz |

## Kurallar

- **Varsayılan reddet**; açılacak her şey tek tek, bilinçli açılır.
- Dar kurallar üstte, geniş kurallar altta.
- Yönetim portları (SSH, uzak masaüstü) internete değil, yalnızca
  yönetim ağına açılır.
- **Çıkış da süzülür**; engellenen deneme kaydedilir.
- Her kuralın bir sahibi ve açıklaması olur; hiç tutmayan kural ayıklanır.
