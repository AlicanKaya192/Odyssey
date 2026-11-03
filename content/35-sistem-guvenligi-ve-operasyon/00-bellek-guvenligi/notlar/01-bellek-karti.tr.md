## Hata ailesi

| Hata | Kısaca | Önlem |
|---|---|---|
| Arabellek taşması | Alanın sonundan öteye yazmak | Yazmadan önce boyu denetle |
| Aşırı okuma | Alanın dışından okumak | Okunacak uzunluğu denetle |
| Off-by-one | Sınırı bir fazla saymak | `range(size)`, `<` ile sınır |
| Tam sayı taşması | Boyut hesabının başa sarması | Hesaptan önce sığıyor mu bak |
| Use-after-free | Geri verilmiş belleği kullanmak | İşaretçiyi boşalt, güvenli dil |
| Double free | Aynı belleği iki kez geri vermek | Sahipliği tek yerde tut |

## C'de tehlikeli ve güvenli karşılıklar

| Tehlikeli | Neden? | Yerine |
|---|---|---|
| `gets` | Satırın boyunu hiç sınırlamaz | `fgets` |
| `strcpy` | Hedefin boyunu bilmez | `strncpy`, `strlcpy` |
| `strcat` | Eklemenin sığacağını bilmez | `strncat`, `strlcat` |
| `sprintf` | Çıktının boyunu bilmez | `snprintf` |

Aramada dikkat: `fgets` içinde `gets`, `snprintf` içinde `printf` geçer.
Bir adı ararken kelime sınırı kullan (`\bgets\s*\(`), yoksa güvenli
karşılık da yakalanır.

## Python kalıpları

- Sınır denetimi: `if len(data) > size: ...` yazmadan **önce**.
- Kırpmak: `data[:size]`.
- 8 bitlik sarmayı taklit etmek: `n & 0xFF`; 16 bit için `n & 0xFFFF`.
- Sığıyor mu: `a + b < 2 ** bits`.

## Akılda tutulacak

- Taşma **sessizdir**: program durmaz, yanlış veriyle devam eder.
- C'de metin sonundaki sıfır bayt da yer kaplar: 8 harf için 9 bayt.
- Dışarıdan gelen her uzunluk (paket, dosya, form) güvenilmezdir; önce
  ölçülür, sonra kullanılır.
