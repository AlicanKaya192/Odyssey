## Kavramlar

| Kavram | Anlamı |
|---|---|
| Kişisel veri | Belirlenebilir bir gerçek kişiye dair her bilgi |
| Özel nitelikli veri | Sağlık, biyometrik, genetik, din, siyasi görüş gibi hassas veri |
| İlgili kişi | Verisi işlenen kişi |
| Veri sorumlusu | Amaca ve yönteme karar veren |
| Veri işleyen | Sorumlu adına işleyen |
| Takma ad | Doğrudan tanıtıcının yerine konan değer; veri yine kişiseldir |
| Anonim veri | Hiçbir ek bilgiyle kimseyi belirlemeyen veri |
| Dolaylı tanıtıcı | Birleşince kişiyi gösteren alanlar: yaş, posta kodu, cinsiyet |

## İlkeden koda

| İlke | Kodda |
|---|---|
| Veri en aza indirme | Amaç başına izin verilen alan listesi |
| Saklama sınırlaması | Amaç başına süre; süresi dolanı silen düzenli iş |
| Takma ad | `hmac.new(anahtar, deger, sha256)`; anahtar sır kasasında |
| Anonimlik denetimi | k-anonimlik: en küçük grup boyu |
| Erişim hakkı | Veri envanteri + kişiye göre arama |
| Silme hakkı | Bütün tablolarda ve yedek planında silme |

## Python kalıpları

- Alan süzmek: `{k: v for k, v in kayit.items() if k in izinli}`.
- Anahtarlı özet: `hmac.new(key, value.encode(), hashlib.sha256).hexdigest()`.
- Genelleştirme: `yas // 10 * 10`, `posta[:3] + "**"`.
- k değeri: `min(Counter(gruplar).values())`.

## Akılda tutulacak

- Toplanmayan veri sızdırılamaz.
- Düz özet takma ad için yetmez; olası değerler denenerek geri bulunur.
- Adı silmek anonimleştirmek değildir.
- Süresi dolan veri silinir; "belki lazım olur" bir amaç değildir.
- Bu kart hukuki tavsiye değildir; ayrıntı için yasanın kendisine ve
  uzmana başvurulur.
