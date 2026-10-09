`sort_letters(word)` fonksiyonunu yaz: yalnızca küçük İngilizce harflerden
(`a`–`z`) oluşan bir kelimenin harflerini alfabetik sırayla bir metin
olarak döndürsün.

- `sort_letters("banana")` → `"aaabnn"`

26 sayaçlık bir liste kullan: `ord(letter) - ord("a")` harfin sırasını
(0–25) verir, `chr(index + ord("a"))` geri harfe çevirir. `sorted` ve
`.sort()` kullanma.

**Beklenen çıktı:**

```
aaabnn
aghilmort
```
