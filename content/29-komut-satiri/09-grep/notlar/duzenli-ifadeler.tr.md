grep'in deseni bir düzenli ifadedir (regular expression). Burada en sık
gerekenler var; konunun tamamı başlı başına bir dil.

## Özel karakterler

| Yazım | Anlamı | Örnek | Uyar |
|---|---|---|---|
| `^` | Satır başı | `'^a'` | ada, alan |
| `$` | Satır sonu | `'e$'` | grace, katherine |
| `.` | Herhangi tek karakter | `'d.sk'` | disk, desk |
| `[abc]` | Köşeli parantezdekilerden biri | `'[0-9]'` | herhangi bir rakam |
| `[^abc]` | Bunların dışında biri | `'[^0-9]'` | rakam olmayan |
| `x*` | x'ten sıfır ya da daha fazla | `'ab*c'` | ac, abc, abbc |
| `.*` | Herhangi bir metin | `'user.*in'` | user ada logged in |

`-E` ile ayrıca:

| Yazım | Anlamı | Örnek |
|---|---|---|
| `x+` | x'ten bir ya da daha fazla | `'[0-9]+%'` |
| `x?` | x olabilir de olmayabilir de | `'colou?r'` |
| <code>A&#124;B</code> | A ya da B | <code>'ERROR&#124;WARN'</code> |
| `( )` | Gruplama | `'(ab)+'` |

## Özel karakterin kendisini aramak

Gerçek bir nokta ya da yıldız aramak için önüne ters bölü koy: `'1\.5'`,
`'a\*b'`. Ya da hiç düzenli ifade istemiyorsan `grep -F` (düz metin).

## Joker karakterlerle farkı

| | Joker (kabuk) | Düzenli ifade (grep) |
|---|---|---|
| Herhangi bir metin | `*` | `.*` |
| Tek karakter | `?` | `.` |
| Neye uygulanır | Dosya adları | Satırların içi |

## Tırnak

Deseni hep tek tırnakla yaz. Tırnaksız `grep a* f` yazarsan kabuk `a*`'ı önce
dosya adlarına genişletir ve grep bambaşka bir desen görür.
