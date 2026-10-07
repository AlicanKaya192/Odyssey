## Biçim

```text
Fix crash when the cart is empty            ← başlık: ≤ 50 karakter, emir kipi

The total was divided by the item count,     ← boş satırdan sonra: neden
which is zero for an empty cart. Return 0
instead and show the "empty" message.

Fixes #42                                    ← varsa issue bağlantısı
```

Terminalde: `git commit -m "Başlık" -m "Açıklama" -m "Fixes #42"` (her `-m`
bir paragraf).

## Başlık kalıpları

| Fiil | Ne zaman |
|---|---|
| `Add` | Yeni dosya, özellik, test. |
| `Fix` | Hata düzeltmesi. |
| `Remove` | Silme. |
| `Update` | Var olanı güncellemek (bağımlılık sürümü, metin). |
| `Rename` / `Move` | Ad ya da yer değişikliği. |
| `Refactor` | Davranışı değiştirmeden kodu düzenlemek. |
| `Improve` | Hız, okunabilirlik. |

## Kendine sor

- Bu mesajı altı ay sonra okusam ne yapıldığını ve **neden** yapıldığını
  anlar mıyım?
- Başlıkta "and" var mı? Varsa muhtemelen iki commit.
- Başlık dosya adını mı söylüyor? Fark onu zaten gösteriyor; işi anlat.

## Türkçe mi, İngilizce mi?

Git ikisini de kabul eder. Açık kaynak ve uluslararası ekiplerde İngilizce
yaygın; tek dilde ve tutarlı olmak, dilin kendisinden önemli. Ekibin neyi
kullanıyorsa onu kullan.

## Commit'ten sonra fark ettim

| Durum | Çözüm |
|---|---|
| Mesajda yazım hatası, henüz push etmedim | `git commit --amend -m "..."` |
| Birkaç küçük commit tek olmalıydı, push etmedim | `git reset --soft HEAD~n` + commit, ya da `git rebase -i` |
| Çoktan push ettim | Bırak; bir dahakine dikkat et (geçmişi yeniden yazma) |
