# Yetkilendirme

Kimlik doğrulama "sen kimsin?" sorusunu cevapladı. **Yetkilendirme**
(authorization) ikinci soruyu cevaplar: "bunu yapmana izin var mı?" Ada'nın
kim olduğunu bilmek, onun bordroları görüp göremeyeceğini söylemez. Bu
bölüm bir izin kararının nelerden oluştuğunu, izinlerin nasıl tutulduğunu ve
yetkilendirmenin en sık nerede bozulduğunu anlatıyor.

## Bir kararın parçaları

Her yetkilendirme kararının üç parçası var:

- **Özne** (subject): işi yapmak isteyen. Bir kullanıcı, bir program, bir
  hizmet.
- **Nesne** ya da **kaynak** (object, resource): üzerinde iş yapılmak
  istenen şey. Bir dosya, bir tablo, bir fatura.
- **Eylem** (action): yapılmak istenen iş. Okumak, yazmak, silmek, onaylamak.

Karar şu cümleye cevaptır: "**Özne**, **nesne** üzerinde **eylemi**
yapabilir mi?" Örneğin "Alan, `payroll` dosyasını okuyabilir mi?"

## Erişim denetim matrisi

Bütün kararları bir tabloya yazabiliriz: satırlar özneler, sütunlar
nesneler, hücreler izin verilen eylemler. Buna **erişim denetim matrisi**
(access control matrix) denir:

```python
matrix = {
    "ada": {"grades": {"read", "write"}, "payroll": set()},
    "alan": {"grades": {"read"}, "payroll": {"read"}},
    "grace": {"grades": set(), "payroll": {"read", "write"}},
}
objects = ["grades", "payroll"]
print(f"{'':<6}", *[f"{o:<11}" for o in objects])
for subject, row in matrix.items():
    cells = [",".join(sorted(row[o])) or "-" for o in objects]
    print(f"{subject:<6}", *[f"{c:<11}" for c in cells])
```

```text
       grades      payroll    
ada    read,write  -          
alan   read        read       
grace  -           read,write
```

Matris kavramı anlamak için mükemmeldir, ama gerçek bir sistemde binlerce
kullanıcı ve milyonlarca dosya olur; hücrelerin neredeyse hepsi boştur.
Bu yüzden matris iki farklı biçimde saklanır.

## Erişim listesi ve yetenek listesi

**Erişim denetim listesi** (access control list, ACL) matrisi
**sütun sütun** saklar: her nesnenin yanında, ona kimlerin ne yapabileceği
yazar. Dosya sistemlerindeki izinler böyle çalışır.

```python
acl = {}
for subject, row in matrix.items():
    for obj, actions in row.items():
        if actions:
            acl.setdefault(obj, {})[subject] = sorted(actions)
print(acl["grades"])
print(acl["payroll"])
```

```text
{'ada': ['read', 'write'], 'alan': ['read']}
{'alan': ['read'], 'grace': ['read', 'write']}
```

**Yetenek listesi** (capability list) ise matrisi **satır satır** saklar:
her öznenin yanında, neye ne yapabileceği yazar. Bir giriş jetonunun "bu
kişi şunları yapabilir" diye taşıdığı bilgi buna benzer.

```python
caps = {s: {o: sorted(a) for o, a in row.items() if a} for s, row in matrix.items()}
print(caps["alan"])
print(caps["grace"])
```

```text
{'grades': ['read'], 'payroll': ['read']}
{'payroll': ['read', 'write']}
```

İkisi de aynı bilgiyi tutar ama farklı soruları kolaylaştırır:

| Soru | ACL | Yetenek listesi |
|---|---|---|
| "Bu dosyaya kimler erişebilir?" | Kolay: dosyanın listesine bak | Zor: herkesin listesini tara |
| "Alan nelere erişebilir?" | Zor: bütün dosyaları tara | Kolay: Alan'ın listesine bak |
| Bir nesnenin bütün izinlerini kaldırmak | Kolay | Zor |
| Bir kişinin bütün izinlerini kaldırmak | Zor | Kolay |

İşten ayrılan birinin bütün yetkilerini kaldırmak, ACL kullanan bir
sistemde her nesneye tek tek bakmayı gerektirir. Bu yüzden gerçek
sistemler çoğu zaman roller gibi ara katmanlar kullanır (bir sonraki
bölüm).

## Karar nerede verilir?

Yetkilendirmenin en önemli kuralı: **karar sunucuda verilir.** Ekranda bir
düğmeyi gizlemek yetkilendirme değildir. Kullanıcı düğmeyi görmese de
isteği elle gönderebilir. Arayüz yalnızca kullanıcıya kolaylık sağlar;
asıl denetim, isteği alan kodun içinde, her istekte (tam aracılık) yapılır.

İkinci kural: denetim **nesne düzeyinde** yapılır. "Fatura görme izni
var" demek yetmez; "**bu** faturayı görme izni var mı?" diye sorulmalı.
Bu soru unutulunca ortaya çıkan açığın adı **güvensiz doğrudan nesne
başvurusu** (insecure direct object reference, IDOR): adres çubuğundaki
`/invoices/101`'i `102` yapan kullanıcı başkasının faturasını görür.

```python
invoices = {101: "ada", 102: "alan", 103: "ada"}


def can_view_bad(user, invoice_id):
    return invoice_id in invoices


def can_view(user, role, invoice_id):
    owner = invoices.get(invoice_id)
    if owner is None:
        return False
    return owner == user or role == "accountant"


tests = [("ada", "customer", 101), ("ada", "customer", 102),
         ("bob", "accountant", 102), ("ada", "customer", 999)]
for user, role, invoice_id in tests:
    print(user, invoice_id, can_view_bad(user, invoice_id),
          can_view(user, role, invoice_id))
```

```text
ada 101 True True
ada 102 True False
bob 102 True True
ada 999 False False
```

Kötü sürüm yalnızca faturanın **var olup olmadığına** bakıyor: Ada,
Alan'ın 102 numaralı faturasını görebiliyor. İyi sürüm sahibini soruyor;
muhasebeci (`accountant`) rolü ise herkesin faturasını görebiliyor. Olmayan
fatura için iki sürüm de `False` diyor, ama iyi sürüm bunu açıkça
"varsayılan olarak reddet" diye yapıyor.

## Yatay ve dikey yetki aşımı

Yetkilendirme hataları iki yöne doğru olur:

<figure class="fig"><div class="versus">
  <div><h4>Yatay (horizontal)</h4>Aynı düzeydeki <b>başka bir kullanıcının</b> verisine ulaşmak. Ada'nın Alan'ın faturasını görmesi.</div>
  <div><h4>Dikey (vertical)</h4>Sahip olmadığı <b>daha yüksek bir yetkiyi</b> kullanmak. Sıradan bir kullanıcının yönetici sayfasındaki "kullanıcı sil" işlemini çalıştırması.</div>
</div><figcaption>İkisi de sunucudaki denetimin eksik ya da yanlış olmasından doğar.</figcaption></figure>

Dikey aşmaya **yetki yükseltme** (privilege escalation) de denir; sistem
düzeyindeki hâli Sistem Güvenliği modülünde ayrıca anlatılıyor.

## İyi bir yetkilendirme kodu

- **Tek yer:** izin kararı tek bir fonksiyonda verilir; her uç nokta o
  fonksiyonu çağırır. Kararlar koda dağılırsa birini unutmak kolaylaşır.
- **Varsayılan ret:** kuralda yazmayan her şey reddedilir.
- **Sunucuda, her istekte:** istemciden gelen "ben yöneticiyim" bilgisine
  güvenilmez; rol sunucudaki kayıttan okunur.
- **Nesne düzeyinde:** yalnızca "bu türden nesne" değil "bu nesne" sorulur.
- **Kayıt:** reddedilen istekler kayda geçirilir; birinin art arda farklı
  fatura numaraları denediği oradan görülür.

## Özet

- Yetkilendirme "özne, nesne üzerinde eylemi yapabilir mi?" sorusudur.
- **Erişim denetim matrisi** bütün kararları tek tabloda gösterir;
  **ACL** sütun sütun, **yetenek listesi** satır satır saklar.
- Karar sunucuda, her istekte ve nesne düzeyinde verilir; düğme gizlemek
  yetkilendirme değildir.
- Nesne düzeyindeki denetim unutulunca **IDOR** doğar.
- **Yatay** aşım başka kullanıcının verisine, **dikey** aşım daha yüksek
  yetkiye ulaşmaktır.
