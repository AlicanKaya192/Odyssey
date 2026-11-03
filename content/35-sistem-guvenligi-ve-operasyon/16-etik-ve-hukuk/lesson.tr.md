# Etik ve Hukuk

Bu patikada öğrendiklerinin çoğu iki yöne de kullanılabilir. Bir açığın
nasıl oluştuğunu bilen biri onu kapatabilir de, kötüye de kullanabilir.
Güvenlik bilgisini savunma tarafında tutan şey teknik değil, iki çizgidir:
**izin** ve **etik**. Bu bölüm o çizgileri ve onları günlük işe dökmenin
yollarını anlatıyor.

Bu bölüm **hukuki tavsiye değildir.** Yasalar ülkeden ülkeye değişir ve
zamanla güncellenir; somut bir durumda yasanın kendisine ve bir hukukçuya
başvurulur. Bütün kişiler, adresler ve sistemler uydurmadır.

## İzin: test ile saldırı arasındaki çizgi

Bir güvenlik testi ile bir saldırı teknik olarak aynı adımlardan
oluşabilir. Aralarındaki fark tek bir belgedir: sistemin **sahibinin yazılı
izni**. İzin yoksa niyet iyi olsa bile ("yalnızca merak ettim", "açığı
gösterip uyaracaktım") çoğu ülkede bir bilişim sistemine izinsiz girmek
suçtur. Türkiye'de Türk Ceza Kanunu'nun bilişim alanındaki suçları
düzenleyen hükümleri, Avrupa'da ve başka ülkelerde de benzer yasalar
vardır.

Bir başkasının sistemine izinsiz bakmanın "hafif" bir yolu yoktur. Bir
web sitesinin, okulun ağının ya da bir arkadaşın bilgisayarının güvenliğini
"denemek" için de sahibinin izni gerekir. Öğrenmenin yolu kendi kurduğun
ortamdır.

## Angajman kuralları

Yetkili bir test, başlamadan önce yazılı **angajman kurallarıyla** (rules of
engagement) çerçevelenir. Bu belge en az şunları söyler:

| Alan | Neden? |
|---|---|
| Yazılı izin | Testin yasal dayanağı |
| İzni veren | Sistemin sahibi ya da sahibi adına yetkili kişi |
| Kapsam | Hangi adresler, hangi sistemler; açıkça hariç tutulanlar |
| Zaman penceresi | Test hangi günler ve saatlerde yapılabilir |
| Acil durum iletişimi | Bir şey ters giderse kim aranır |
| Veri işleme | Testte görülen veriye ne olacak |

Belgenin eksiksiz olduğunu bir listeyle denetleyebiliriz:

```python
REQUIRED = ["written_permission", "signed_by", "scope", "window",
            "emergency_contact", "data_handling"]
plan = {
    "written_permission": True,
    "signed_by": "Eve (owner)",
    "scope": ["10.20.0.0/24"],
    "window": ["2026-11-10", "2026-11-14"],
}
missing = [name for name in REQUIRED if not plan.get(name)]
print("missing:", missing)
print("ready" if not missing else "not ready")
```

```text
missing: ['emergency_contact', 'data_handling']
not ready
```

İki alan eksik olduğu için plan hazır değil. Eksik bir alan "nasılsa
sorun çıkmaz" diye geçilmez: acil durum iletişimi olmayan bir testte bir
hizmet durursa kimse kime haber vereceğini bilmez.

## Kapsam ve zaman penceresi

İzin her şeye değil, **yazılan şeye** verilir. Kapsamdaki bir ağın içinde
bile bazı makineler açıkça hariç tutulabilir (canlı bir veritabanı gibi) ve
izin yalnızca belirli günler için geçerlidir. Her işlemden önce hedef bu
üç soruya karşı denetlenir:

```python
import ipaddress
from datetime import date

SCOPE = [ipaddress.ip_network("10.20.0.0/24")]
EXCLUDED = {ipaddress.ip_address("10.20.0.5")}
WINDOW = (date(2026, 11, 10), date(2026, 11, 14))


def check(target, day):
    address = ipaddress.ip_address(target)
    if not WINDOW[0] <= day <= WINDOW[1]:
        return "outside the window"
    if address in EXCLUDED:
        return "excluded"
    if not any(address in net for net in SCOPE):
        return "out of scope"
    return "in scope"


for target, day in [("10.20.0.17", date(2026, 11, 11)),
                    ("10.20.0.5", date(2026, 11, 11)),
                    ("10.30.0.8", date(2026, 11, 11)),
                    ("10.20.0.17", date(2026, 11, 20))]:
    print(target, day, check(target, day))
```

```text
10.20.0.17 2026-11-11 in scope
10.20.0.5 2026-11-11 excluded
10.30.0.8 2026-11-11 out of scope
10.20.0.17 2026-11-20 outside the window
```

Aynı adres (`10.20.0.17`) bir gün kapsamda, başka bir gün kapsam dışı.
Hariç tutulan makine kapsamdaki ağın içinde olsa da test edilmez. Bu kod
hiçbir yere bağlanmıyor; yalnızca adresleri ve tarihleri karşılaştırıyor.

## İzni kim verebilir?

İzni veren kişinin o sistem üzerinde **yetkisi** olmalı. Bir sisteme
erişimi olmak, onun test edilmesine izin verebilmek demek değildir: bir
çalışan kendi kullandığı sunucuyu bile, sahibinin onayı olmadan test
ettiremez. Bulut hizmetlerinde sağlayıcının kendi test kuralları da ayrıca
geçerlidir.

```python
OWNERS = {"shop.example.org": "Eve", "db.example.org": "Eve",
          "mail.example.org": "Bob"}
permission = {"signed_by": "Bob",
              "targets": ["shop.example.org", "mail.example.org"]}
for target in permission["targets"]:
    owner = OWNERS.get(target)
    if owner == permission["signed_by"]:
        print(target, "ok")
    else:
        print(target, "needs", owner)
```

```text
shop.example.org needs Eve
mail.example.org ok
```

Bob'un imzası kendi sistemi için geçerli, Eve'in sistemi için değil.

## Testte görülen veri

Yetkili bir testte bile kişisel veriyle karşılaşılabilir. Etik kural
basittir: **gerekenden fazlasına bakılmaz, kopyalanmaz, paylaşılmaz.**
Bir açığın varlığını göstermek için bir kaydın varlığı yeter; bütün
tabloyu indirmek gerekmez. Rapora giren örnekler maskelenir (Gizlilik ve
Veri Koruma bölümündeki veri en aza indirme):

```python
import re

finding = "Login page leaks ada@example.org and bob@example.org in an error."


def mask(match):
    user, domain = match.group(0).split("@")
    return user[0] + "***@" + domain


print(re.sub(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+", mask, finding))
```

```text
Login page leaks a***@example.org and b***@example.org in an error.
```

Rapor açığın ne olduğunu hâlâ açıkça anlatıyor ama kimin e-postası olduğunu
söylemiyor. Test bitince kapsamda toplanan veri anlaşmadaki gibi silinir.

## Meslek etiği

Güvenlik işinde çalışanların uyduğu ilkeler hemen her meslek kuruluşunda
aynı temele dayanır:

- **Zarar verme.** Test sistemi durdurmamalı, veriyi bozmamalı.
- **Gizliliği koru.** Gördüğün sırları ve verileri kimseyle paylaşma.
- **Dürüst raporla.** Bulduğunu küçültme ya da büyütme; bulamadığını
  bulmuş gibi gösterme.
- **Yetkinin sınırında kal.** Bilmediğin bir işi biliyormuş gibi üstlenme.
- **Çıkar çatışmasını söyle.** Test ettiğin şirketin rakibiyle de
  çalışıyorsan bunu açıkça belirt.

## Özet

- Test ile saldırıyı ayıran şey sahibinin **yazılı iznidir**; izinsiz
  erişim çoğu ülkede suçtur.
- Yetkili test **angajman kurallarıyla** başlar: izin, izni veren, kapsam,
  zaman penceresi, acil durum iletişimi, veri işleme.
- Her işlemden önce hedef **kapsam, hariç tutulanlar ve zaman penceresine**
  karşı denetlenir.
- İzni yalnızca sistem üzerinde **yetkisi olan** verebilir.
- Testte görülen veri en aza indirilir ve raporda **maskelenir**.
- Bu bölüm hukuki tavsiye değildir.
