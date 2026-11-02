## Terimler

| Terim | Anlamı |
|---|---|
| **En az yetki** (least privilege) | İşe yetecek kadar yetki, fazlası değil |
| **Bilmesi gereken kadar** (need to know) | Düzey yetse de iş gerektirmiyorsa bilgi verilmez |
| **Yetki birikmesi** (privilege creep) | Rol değişikliklerinde eski yetkilerin alınmaması |
| **Erişim gözden geçirme** (access review) | Her yetkinin hâlâ gerekli olup olmadığının düzenli sorulması |
| **Tam zamanında erişim** (just-in-time access) | İstenip onaylanan, kısa süre sonra kendiliğinden düşen yetki |
| **Görev ayrılığı** (separation of duties) | Kötüye kullanılabilecek adımların farklı kişilerde olması |
| **Dört göz ilkesi** (two-person rule) | Önemli işlem için iki kişinin onayı |
| **Acil durum hesabı** (break-glass account) | Kasada duran, kullanılınca alarm çalan, sonradan incelenen hesap |

## Python kalıpları

```python
extra = held - needed
unused = granted - used
has_conflict = set(pair) <= perms
active = date.fromisoformat(until) >= today
```

- `-` küme farkı: birinde olup ötekinde olmayanlar.
- `<=` kümelerde alt küme: hepsi öbüründe mi?
- `date.fromisoformat("2026-11-02")`: metinden tarih.

## Uygulama listesi

- Günlük iş için yönetici olmayan hesap.
- Programların veritabanı kullanıcıları yalnızca gereken tablolarda.
- Rol değişince eski rolün yetkileri **aynı gün** alınır.
- İşten ayrılanın bütün erişimleri **aynı gün** kapatılır.
- Üç ayda bir erişim gözden geçirmesi; kullanılmayan yetkiler önerilir.
- Kısa süreli ihtiyaçlar bitiş tarihiyle verilir.
- Çakışan görev çiftleri yazılıdır ve her rol atamasında denetlenir.
