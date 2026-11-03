Güvenlik duvarı kuralı yazarken, ağ bölerken ya da bir kayıttaki adresin
"bizden mi" olduğunu anlarken hep aynı hesap yapılır.

## Adres sayısı

`/n` önekli bir IPv4 ağında `2 ** (32 - n)` adres vardır.

| Önek | Adres | Cihaza kalan |
|---|---|---|
| `/16` | 65536 | 65534 |
| `/24` | 256 | 254 |
| `/26` | 64 | 62 |
| `/30` | 4 | 2 |
| `/32` | 1 | Tek cihaz |

"Cihaza kalan" sayısında ilk adres (ağın kendisi) ve son adres (yayın)
düşülür.

## Bir ağı bölmek

`192.168.1.0/24` dört eşit parçaya bölünürse her parça `/26` olur:

- `192.168.1.0/26`
- `192.168.1.64/26`
- `192.168.1.128/26`
- `192.168.1.192/26`

Bir bit önek eklemek ağı ikiye, iki bit dörde böler. Ağ bölümleme
(VPN ve Ağ Bölümleme bölümü) tam olarak bu hesapla yapılır: misafir
Wi-Fi'si bir parça, sunucular başka bir parça.

## Bir adres hangi ağda?

Adresi ve ağ maskesini bit bit VE'le (AND): sonuç ağ adresidir.
`192.168.1.77` ile `255.255.255.0` → `192.168.1.0`. Python'da bunu
`ip in net` kendisi yapar.

## Sık hatalar

- **"172 ile başlıyorsa özel"**: yanlış; özel aralık `172.16` – `172.31`.
- **Geri döngüyü özel sanmak:** `127.0.0.1` için `is_private` de `True`;
  kaydı "yerel ağdan geldi" diye yorumlama, bu bilgisayardan geldi.
- **`/24`'ü 256 cihaz sanmak:** cihaza 254 adres kalır.
- **Metinle karşılaştırmak:** `"192.168.1.9" < "192.168.1.10"` metin
  olarak `False`; adresleri `ipaddress` nesnesine çevirip karşılaştır.
