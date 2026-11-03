## Diffie-Hellman adımları

| Adım | Ada | Açıkta | Can |
|---|---|---|---|
| Ortak değerler | | `p`, `g` | |
| Gizli sayı | `a` | | `b` |
| Açık değer | `A = pow(g, a, p)` | `A`, `B` | `B = pow(g, b, p)` |
| Ortak sır | `pow(B, a, p)` | | `pow(A, b, p)` |

İki ortak sır aynıdır: `g ** (a·b) mod p`. Dinleyen `p`, `g`, `A`, `B`'yi
görür; `a` ya da `b`'yi bulmak ayrık logaritma problemidir.

## Eliptik eğri DH

| | Sayılarla DH | Eğriyle DH |
|---|---|---|
| Ortak değer | `g`, `p` | Nokta `G`, eğri |
| Açık değer | `pow(g, a, p)` | `a·G` (ikile ve topla) |
| Ortak sır | `pow(B, a, p)` | `a·(b·G)` noktasının `x`'i |
| Zor problem | Ayrık logaritma | Eğride ayrık logaritma |
| Tipik boyut | 2048+ bit | 256 bit (X25519, P-256) |

## Nokta toplama (mod `p`)

- Farklı noktalar: `s = (y2 - y1) / (x2 - x1)`.
- Aynı nokta (ikileme): `s = (3·x1² + a) / (2·y1)`.
- `x3 = s² - x1 - x2`, `y3 = s·(x1 - x3) - y1`.
- "Bölme" = tersle çarpma: `pow(payda, -1, p)`.
- `(x, y) + (x, -y)` = sonsuzdaki nokta (toplamanın sıfırı).

## Kurallar

- Ortak sır bir **KDF**'den (HKDF) geçirilmeden anahtar olarak kullanılmaz.
- Gelen açık değer **denetlenir**: sayılarla DH'de `1 < A < p - 1`, eğride
  noktanın eğrinin üstünde olduğu.
- Gizli sayılar her oturumda `secrets` ile yeniden üretilir ve iş bitince
  atılır (**ileri gizlilik**).
- DH kimlik doğrulamaz; açık değerler imzalanır.
