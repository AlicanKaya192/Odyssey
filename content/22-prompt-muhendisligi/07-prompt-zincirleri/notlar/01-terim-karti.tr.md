| Terim | Anlamı |
|---|---|
| **Prompt zinciri** (prompt chaining) | Bir işi adımlara bölüp her adımı ayrı çağrıyla yapmak; bir adımın çıktısı sonrakinin girdisi |
| **Adım doğrulaması** | Her adımın çıktısını sonraki adıma vermeden önce denetlemek |
| **Zinciri durdurmak** | Doğrulanamayan adımda devam etmemek ve nerede durulduğunu kaydetmek |
| **Adım kaydı** | Her adımın adı, sonucu ve token'ı |
| **Koşullu adım** | Önceki adımın çıktısına göre atlanan ya da seçilen adım |
| **Bağlam seçimi** | Her adıma yalnızca gereken bilgiyi (ör. tek bir kural) göndermek |

**Akılda tut:**

- Derste ikinci mesajda ilk adım JSON vermedi; zincir sınıflandırmada
  durdu ve kayıt nerede durduğunu gösterdi.
- Bu örnekte tek prompt bütün kuralları taşıdığı için 412 token, zincirin
  üç çağrısı toplam 215 token tuttu; kurallar kısa olsaydı sonuç tersine
  dönebilirdi.
- Çıkarma adımını gerekmeyen kategorilerde atlamak 10 test mesajında
  çağrı sayısını 30'dan 26'ya indirdi.
- Atlama kararı önceki adımın doğruluğuna bağlıdır.
