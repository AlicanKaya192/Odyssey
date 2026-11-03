## Türler

| Tür | Örnek | Eksik olan |
|---|---|---|
| Yatay | Başka müşterinin faturasını görmek | Sahiplik denetimi |
| Dikey | Sıradan kullanıcının yönetici işlemi yapması | Rol denetimi |

## Sebep → önlem

| Sebep | Önlem |
|---|---|
| Nesne numarayla, sahibine bakılmadan getiriliyor | `invoice["owner"] == user` her istekte |
| İstekteki her alan kayda yazılıyor (toplu atama) | İzin listesi: `if key in ALLOWED` |
| Ayrıcalıklı görevin betiği başkasınca yazılabilir | Betik yönetici hesabına ait, `mode & 0o022 == 0` |
| Beklenmedik setuid program | setuid izin listesi, düzenli envanter |
| Yamalanmamış yazılım | Yama yönetimi |
| Ortak ya da paylaşılan yönetici parolası | Kişiye özel hesap, en az yetki |

## Tespit işaretleri

- Aynı kullanıcının kısa sürede art arda reddedilen yetki istekleri.
- Yönetici grubuna yeni üye eklenmesi.
- Yeni ortaya çıkan setuid dosya ya da yeni zamanlanmış görev.
- Sıradan bir hesabın daha önce hiç yapmadığı yönetici işlemleri.

## Python kalıpları

- setuid biti: `mode & stat.S_ISUID` (`0o4000`).
- Grup ve diğerleri yazabiliyor mu: `mode & 0o022`.
- `key=value` alanlarını sözlüğe çevirmek: `dict(p.split("=") for p in parts)`.
- Sayım: `collections.Counter`; eşik: `count >= threshold`.
- İki anlık görüntünün farkı: `set(after) - set(before)`.

## Akılda tutulacak

- Kimliği doğrulanmış olmak her nesneye erişebilmek değildir.
- Başkasının nesnesine "bulunamadı" demek, hangi nesnelerin var olduğunu
  da gizler.
- Rol ve yetki alanları istemciden gelen veriyle değişmez.
