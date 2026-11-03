## Kavramlar

| Kavram | Anlamı |
|---|---|
| Koordineli açıklama | Önce sahibine gizlice bildirmek, düzeltmeyle birlikte duyurmak |
| Tam açıklama | Açığı düzeltme beklemeden herkese duyurmak |
| security.txt | Güvenlik bildirimlerinin nereye gideceğini yazan dosya (RFC 9116) |
| CVE | Duyurulan bir açığın ortak kimliği: `CVE-yıl-sayı` |
| CVSS | Açığın önemini 0–10 arası puanla anlatan sistem |
| Hata ödül programı | Kapsamı ve ödülleri yazılı test daveti (bug bounty) |
| Güvenli liman | Kurallara uyan iyi niyetli araştırmacıya hukuki yola gidilmeyeceği sözü |

## CVSS dereceleri

| Puan | Derece |
|---|---|
| 0.0 | Yok (none) |
| 0.1–3.9 | Düşük (low) |
| 4.0–6.9 | Orta (medium) |
| 7.0–8.9 | Yüksek (high) |
| 9.0–10.0 | Kritik (critical) |

## Bildirmeden önce

- Açığı fark edince durdum mu, başka kayda bakmadım mı?
- Kime bildireceğim: security.txt, güvenlik ekibi adresi, açıklama
  politikası?
- Rapor başkalarının verisini içermiyor mu?
- Yazdığım etki ölçtüğüm kadar mı?
- Bir ödül programı varsa kuralları ve kapsamı okudum mu?

## Python kalıpları

- İlk iki noktada bölmek: `name, value = line.split(":", 1)`.
- Çok değerli alan: `fields.setdefault(name, []).append(value)`.
- `Z` ile biten zaman: `datetime.fromisoformat("2026-12-31T23:59:59Z")`.
- Hangisi önce: `min(deadline, fixed + timedelta(days=14))`.
- Biçim denetimi: `re.fullmatch(r"CVE-[0-9]{4}-[0-9]{4,}", s)`.

## Akılda tutulacak

- Fark etmek ile denemek farklıdır.
- Bildirim gizli kanaldan yapılır; sosyal medyadan değil.
- "Ödemezseniz yayınlarım" bir açıklama değil şantajdır.
- Program kuralları bir izindir; programın olmadığı yerde güvence yoktur.
