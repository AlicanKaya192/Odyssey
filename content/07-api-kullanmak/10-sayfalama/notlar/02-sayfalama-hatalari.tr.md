Sayfalama döngülerinde sık görülen hatalar ve belirtileri.

| Belirti | Neden | Düzeltme |
|---|---|---|
| Döngü hiç bitmiyor | Durma koşulu yanlış (`next` yerine başka bir alana bakılıyor) | Koşulu belgeye göre yaz; üst sınırlı `for` kullan |
| Hep aynı sayfa geliyor | `page` artırılmıyor ya da `params`'a konmuyor | `page += 1` döngünün içinde; `r.url`'ye bak |
| Son kayıtlar eksik | Son sayfa eklenmeden önce `break` | Önce `extend`, sonra durma denetimi |
| İlk sayfa iki kez | Döngü 1'den, önceden de ilk sayfa alınmış | İlk sayfayı ya döngüde ya dışarıda al, ikisinde birden değil |
| Listede `[[...], [...]]` | `extend` yerine `append` | Sayfanın öğelerini eklemek için `extend` |
| 20'den fazla istedin, 20 geldi | Sunucunun sayfa boyu sınırı | `meta.per_page`'e bak, sınırı kabul et |
| Bağlantıyla gidince süzme kayboluyor | `next` yerine elle `?page=` kuruldu | Sunucunun verdiği `next` adresini olduğu gibi kullan |

## `append` ile `extend` farkı

```python
books = []
books.append(["Emma", "Dune"])   # [['Emma', 'Dune']]   -> bir öğe: liste
books = []
books.extend(["Emma", "Dune"])   # ['Emma', 'Dune']     -> iki öğe
```

## Kaç istek attığını say

Bir sayfalama döngüsünün kaç istek atacağını önceden hesaplayabilirsin:
`toplam / sayfa_boyu`, yukarı yuvarlanmış. 23 kitap, 5'erli sayfa → 5 istek;
20'li sayfa → 2 istek. Çok istek atan bir döngü görürsen önce sayfa boyunu
büyütmeyi dene.
