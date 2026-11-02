`stride_property(letter)` bir STRIDE harfinin bozduğu güvenlik özelliğini
İngilizce adıyla döndürsün:

- `S` → `"authenticity"`, `T` → `"integrity"`, `R` → `"non-repudiation"`,
- `I` → `"confidentiality"`, `D` → `"availability"`, `E` → `"authorization"`.

Harf küçük de gelebilir. Tanınmayan harf için `None`.

**Beklenen çıktı:**

```
S authenticity
t integrity
I confidentiality
e authorization
X None
```
