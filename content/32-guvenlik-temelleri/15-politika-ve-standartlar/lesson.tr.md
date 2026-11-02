# Güvenlik Politikası ve Standartlar

Şimdiye kadar tek tek önlemleri gördük: parola kuralları, en az yetki,
yedek, çok faktörlü doğrulama. Bir kurumda bu önlemlerin **yazılı**,
**onaylı** ve **herkes için aynı** olması gerekir; yoksa her ekip kendi
bildiğini yapar. Bu bölüm güvenliğin yönetim tarafını anlatıyor: belgeler,
verinin sınıflandırılması, uluslararası standartlar ve "denetimden geçtik"
ile "güvendeyiz" arasındaki fark.

## Belgelerin katmanları

Güvenlik belgeleri yukarıdan aşağıya dört katmandır; üstteki "ne ve
neden"i, alttaki "nasıl"ı söyler.

| Belge | Ne söyler? | Örnek | Zorunlu mu? |
|---|---|---|---|
| **Politika** (policy) | Amaç ve ilke; üst yönetim onaylar | "Kurumun bilgilerine yalnızca yetkili kişiler erişir." | Evet |
| **Standart** (standard) | Ölçülebilir kural | "Parolalar en az 12 karakter; uzaktan erişimde çok faktörlü doğrulama." | Evet |
| **Prosedür** (procedure) | Adım adım nasıl yapılır | "Yeni çalışana hesap açma: 1. ... 2. ... 3. ..." | Evet |
| **Kılavuz** (guideline) | Öneri, iyi uygulama | "Parola yöneticisi kullanmanız önerilir." | Hayır |

Politika kısa ve kalıcıdır; teknoloji değişince değişmez. Standart ve
prosedür daha sık güncellenir. Politika **üst yönetimin** onayını taşır:
güvenlik yalnızca bilgi işlem ekibinin işi değil, kurumun kararıdır.
Belgeler yılda en az bir kez ve büyük bir değişiklikten sonra gözden
geçirilir.

## Verinin sınıflandırılması

Her veriyi aynı sıkılıkta korumak hem pahalıdır hem de gereksiz. Bu
yüzden veri **sınıflandırılır** (data classification) ve her sınıfın
nasıl saklanacağı, kiminle paylaşılacağı yazılır. Yaygın dört düzey:

| Düzey | Örnek | Kural |
|---|---|---|
| **Genel** (public) | Web sitesindeki duyuru | Herkes görebilir |
| **İç** (internal) | Toplantı notları | Yalnızca çalışanlar |
| **Gizli** (confidential) | Müşteri listesi, sözleşmeler | Bilmesi gerekenler; şifreli aktarım |
| **Çok gizli** (restricted) | Sağlık verisi, maaşlar, anahtarlar | Adı belirli kişiler; şifreli saklama, her erişim kayıtlı |

Düzeyler sıralıdır; bir kanal belirli bir düzeye kadar veri taşıyabilir.
Bu kuralı küçük bir fonksiyonla yazalım:

```python
LEVELS = ["public", "internal", "confidential", "restricted"]
channel_max = {
    "website": "public",
    "team-chat": "internal",
    "encrypted-mail": "confidential",
}


def can_share(level, channel):
    if channel not in channel_max:
        return False
    return LEVELS.index(level) <= LEVELS.index(channel_max[channel])


for level in LEVELS:
    chat = can_share(level, "team-chat")
    mail = can_share(level, "encrypted-mail")
    print(f"{level:<13} {chat!s:<5} {mail}")
```

```text
public        True  True
internal      True  True
confidential  False True
restricted    False False
```

İki ayrıntı var. Listede olmayan kanal (bilinmeyen bir dosya paylaşım
sitesi) **reddedilir**: varsayılan ret (Güvenlik İlkeleri). Çok gizli veri
ise hiçbir kanaldan serbestçe gönderilmez; onun için ayrı, onaylı bir
süreç vardır. Verinin bir **sahibi** (data owner) olur ve sınıfını o
belirler.

## Standartlar ve çerçeveler

Kurumlar güvenliği sıfırdan icat etmez; herkesin kabul ettiği
**standartları** ve **çerçeveleri** (framework) kullanır.

| Ad | Ne? |
|---|---|
| **ISO/IEC 27001** | Bilgi güvenliği yönetim sisteminin (BGYS, ISMS) şartları. Kurum bağımsız denetimden geçerse **sertifika** alır. Ekinde kontrol listesi var. |
| **ISO/IEC 27002** | 27001'deki kontrollerin nasıl uygulanacağını anlatan rehber. |
| **NIST CSF** | Siber Güvenlik Çerçevesi; sürüm 2.0 altı işlevle düzenler: **Govern, Identify, Protect, Detect, Respond, Recover** (yönet, tanımla, koru, tespit et, müdahale et, kurtar). |
| **CIS Controls** | Öncelik sırasına konmuş, uygulamaya dönük kontrol listesi; küçük kurumlar için iyi başlangıç. |
| **PCI DSS** | Kart verisi işleyen herkesin uyması gereken sektör standardı. |

Bir de **yasalar** var. Kişisel verilerin korunması için Türkiye'de
**KVKK** (6698 sayılı Kanun), Avrupa Birliği'nde **GDPR**. İkisi de kişisel
veriyi işleyen kurumlara yükümlülük getirir: verinin hangi amaçla
işlendiğini bildirmek, gereğinden fazla veri toplamamak, güvenliğini
sağlamak ve bir veri ihlalini yetkili kuruma süresi içinde bildirmek.
Standart isteğe bağlıdır; yasa değildir.

## Kontrolleri işlevlere dağıtmak

NIST CSF'nin altı işlevi bir kontrol listesindeki boşlukları görmeyi
kolaylaştırır. Her kontrolü bir işleve bağlayıp sayalım:

```python
FUNCTIONS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]
controls = [
    ("asset inventory", "Identify"),
    ("mfa for staff", "Protect"),
    ("disk encryption", "Protect"),
    ("log monitoring", "Detect"),
    ("backup restore test", "Recover"),
]
counts = {f: 0 for f in FUNCTIONS}
for name, function in controls:
    counts[function] += 1
for f in FUNCTIONS:
    mark = " <- gap" if counts[f] == 0 else ""
    print(f"{f:<9} {counts[f]}{mark}")
```

```text
Govern    0 <- gap
Identify  1
Protect   2
Detect    1
Respond   0 <- gap
Recover   1
```

Bu kurum korumaya yatırım yapmış ama iki işlevde hiçbir şeyi yok:
güvenliği kimin yönettiği (rol, politika, risk kararı) yazılı değil ve bir
olay olunca ne yapılacağını bilen yok. Önlemlerin hepsi "olmasın" diye;
"olursa" sorusunun cevabı yok.

## Boşluk analizi

**Boşluk analizi** (gap analysis), bir standardın istediği kontrollerle
kurumda gerçekten uygulananları karşılaştırır. Sonuç yapılacak işlerin
listesidir.

```python
required = ["access-control", "mfa", "backup", "logging", "patching"]
status = {
    "access-control": "yes",
    "mfa": "partial",
    "backup": "yes",
    "logging": "no",
}

done = [c for c in required if status.get(c) == "yes"]
missing = [c for c in required if status.get(c, "no") == "no"]
partial = [c for c in required if status.get(c) == "partial"]
print(f"coverage: {100 * len(done) / len(required):.0f}%")
print("missing:", missing)
print("partial:", partial)
```

```text
coverage: 40%
missing: ['logging', 'patching']
partial: ['mfa']
```

`patching` durum listesinde hiç yok: kimse sormamış. `status.get(c, "no")`
bilinmeyeni "yok" sayıyor; "bilmiyoruz" bir kontrolün var olduğu anlamına
gelmez. Yarım uygulanan `mfa` kapsama sayılmıyor: yalnızca bazı
hesaplarda açık olan çok faktörlü doğrulama, açık olmayan hesaptan girene
bir şey yapmaz.

## Uyumluluk güvenlik değildir

<figure class="fig"><div class="versus">
  <div class="no"><h4>Uyumluluk (compliance)</h4>Denetçinin listesindeki kutular işaretli. "Parola politikamız var, yedek alıyoruz." Denetim günü bir anlık fotoğraftır.</div>
  <div class="ok"><h4>Güvenlik</h4>Kontroller gerçekten çalışıyor ve sürekli ölçülüyor. Politika uygulanıyor mu, yedek geri yükleniyor mu, kayıtlara biri bakıyor mu?</div>
</div><figcaption>Sertifikası olan kurumlar da ihlal yaşar; standart bir başlangıç noktasıdır, bitiş değil.</figcaption></figure>

Yine de standartların değeri büyüktür: unutulan konuları hatırlatır, ortak
bir dil sağlar ve müşteriye, iş ortağına güven verir.

## Politika istisnaları

Her kural her durumda uygulanamaz: eski bir makine çok faktörlü
doğrulamayı desteklemiyor olabilir. Bu durumda kural sessizce çiğnenmez;
yazılı bir **istisna** (exception) açılır. İyi bir istisnanın dört şeyi
vardır:

- bir **sahibi** (riski kabul eden kişi),
- bir **gerekçesi**,
- bir **bitiş tarihi** (süresiz istisna, kalıcı açık demektir),
- bir **telafi edici kontrol** (compensating control): o makine ayrı bir
  ağ bölümüne alınır, erişimi kayda geçirilir.

Süresi dolan istisna ya yeniden onaylanır ya da kapatılır.

## Özet

- Belge katmanları: **politika** (ne ve neden) → **standart** (ölçülebilir
  kural) → **prosedür** (nasıl) → **kılavuz** (öneri).
- Veri **sınıflandırılır**: genel, iç, gizli, çok gizli; her kanal belirli
  bir düzeye kadar veri taşır, bilinmeyen kanal reddedilir.
- **ISO/IEC 27001** yönetim sistemi ve sertifika, **NIST CSF** altı işlev,
  **CIS Controls** öncelikli liste, **PCI DSS** kart verisi; yasalar
  **KVKK** ve **GDPR**.
- **Boşluk analizi** istenenle uygulananı karşılaştırır; bilinmeyen "yok"
  sayılır.
- **Uyumluluk güvenlik değildir**; istisnalar sahipli, süreli ve telafi
  edici kontrollü olur.
