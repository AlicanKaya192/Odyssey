# Düzenli İfadeler 1: Kalıplarla Aramak

Bir metindeki bütün telefon numaralarını bulmak, bir ürün kodunun doğru
biçimde yazılıp yazılmadığını denetlemek, kayıt dosyasından tarihleri
çekmek... Bunları `find`, `split`, `isdigit` gibi metin metotlarıyla yapmak
uzun ve kırılgan kod ister. **Düzenli ifade** (regular expression, kısaca
**regex**) aranan şeyin **kalıbını** tek satırda yazmanın dilidir: "üç rakam,
tire, dört rakam" gibi. Python'da bu dil **`re`** modülüyle kullanılır.

Bu bölümde kalıp dilinin temelini, bir sonrakinde gruplarla parça çekmeyi ve
değiştirmeyi görüyoruz.

## İlk örnek

```python
import re

text = "Order 66 shipped 3 items for 120 TL on 2026-03-15"
print(re.findall(r"\d+", text))
```

```text
['66', '3', '120', '2026', '03', '15']
```

`\d` "bir rakam", `+` "bir ya da daha fazla" demek: `\d+` yan yana duran
rakam öbeklerinin hepsini buldu. Metin metotlarıyla aynı iş bir döngü,
`isdigit` ve birkaç değişken isterdi.

Kalıbın başındaki **`r`** (raw, ham metin) önemli; nedeni aşağıda.

## Aramanın dört yolu

```python
import re

text = "Call 555-1234 or 555-9876"
m = re.search(r"\d{3}-\d{4}", text)
print(m.group(), m.start(), m.end())
print(re.match(r"\d{3}", text), re.match(r"Call", text).group())
print(re.fullmatch(r"\d{3}-\d{4}", "555-1234") is not None)
print(re.fullmatch(r"\d{3}-\d{4}", "555-12345"))
print(re.findall(r"\d{3}-\d{4}", text))
```

```text
555-1234 5 13
None Call
True
None
['555-1234', '555-9876']
```

| Fonksiyon | Ne yapar | Bulamazsa |
|---|---|---|
| `re.search(kalıp, metin)` | metnin **herhangi bir yerinde** ilk eşleşme | `None` |
| `re.match(kalıp, metin)` | yalnızca metnin **başında** | `None` |
| `re.fullmatch(kalıp, metin)` | metnin **tamamı** kalıba uymalı | `None` |
| `re.findall(kalıp, metin)` | **bütün** eşleşmeler, liste | `[]` |

- `search`, `match` ve `fullmatch` bir **eşleşme nesnesi** (match object)
  döndürür: `group()` bulunan metin, `start()` / `end()` yeri.
- Metin `Call` ile başladığı için `match(r"\d{3}")` bulamadı (`None`).
- **Doğrulama** (bir kod, bir numara doğru biçimde mi?) için `fullmatch`:
  `"555-12345"` başı uyduğu halde fazladan rakam yüzünden reddedildi.

## Karakter sınıfları

Kalıptaki her parça bir **karakteri** ya da bir **karakter türünü** tarif
eder.

| Yazım | Eşleşir |
|---|---|
| `\d` | bir rakam (0–9) |
| `\w` | harf, rakam ya da `_` (kelime karakteri) |
| `\s` | boşluk, sekme, satır sonu |
| `.` | satır sonu dışında **herhangi bir** karakter |
| `[abc]` | `a`, `b` ya da `c` |
| `[A-Z]`, `[0-9]` | aralık |
| `[^a-z]` | `a`–`z` **dışında** bir karakter |
| `\D`, `\W`, `\S` | büyük harf: tersi (rakam olmayan...) |

```python
import re

text = "id: A7, B12; total = 9.5 kg"
print(re.findall(r"\d", text))
print(re.findall(r"\d+", text))
print(re.findall(r"[A-Z]\d+", text))
print(re.findall(r"\w+", text))
print(re.findall(r"\d+\.\d+", text), re.findall(r"\d.\d", "9.5 9x5"))
print(re.findall(r"[^a-z\s]+", "abc DEF 12 gh!"))
```

```text
['7', '1', '2', '9', '5']
['7', '12', '9', '5']
['A7', 'B12']
['id', 'A7', 'B12', 'total', '9', '5', 'kg']
['9.5'] ['9.5', '9x5']
['DEF', '12', '!']
```

- `\d` her rakamı ayrı buldu; `\d+` öbekleri.
- `[A-Z]\d+`: bir büyük harf ve ardından rakamlar.
- `\w+` kelimeleri buldu; `9.5` iki parçaya bölündü, çünkü nokta kelime
  karakteri değil.
- Ondalık sayıda nokta **`\.`** ile yazılır. Çıplak `.` "herhangi bir
  karakter" olduğu için `9x5`'i de yakaladı.
- `[^a-z\s]+`: küçük harf ve boşluk **olmayan** karakter öbekleri.

## Kaç tane? Nicelikler ve çapalar

| Yazım | Anlamı |
|---|---|
| `?` | 0 ya da 1 (isteğe bağlı) |
| `*` | 0 ya da daha fazla |
| `+` | 1 ya da daha fazla |
| `{3}` | tam 3 |
| `{2,}` / `{2,4}` | en az 2 / 2 ile 4 arası |
| `^` / `$` | metnin başı / sonu |
| `\b` | kelime sınırı |

```python
import re

words = ["color", "colour", "colouur", "flavor"]
print([w for w in words if re.fullmatch(r"colou?r", w)])
print(re.findall(r"\b\w{5}\b", "the quick brown fox jumps over lazy dogs"))
print(re.findall(r"[aeiou]{2,}", "queue cooperate beautiful"))
lines = ["Error: disk full", "No Error"]
print([bool(re.search(r"^Error", line)) for line in lines])
names = ["data.csv", "data.csv.bak"]
print([bool(re.search(r"\.csv$", name)) for name in names])
print(re.findall(r"python", "Python python PYTHON", flags=re.IGNORECASE))
```

```text
['color', 'colour']
['quick', 'brown', 'jumps']
['ueue', 'oo', 'eau']
[True, False]
[True, False]
['Python', 'python', 'PYTHON']
```

- `colou?r`: `u` isteğe bağlı; iki `u` olan reddedildi.
- `\b\w{5}\b`: tam beş harfli kelimeler. `\b` olmasaydı daha uzun
  kelimelerin ilk beş harfi de eşleşirdi (`beautiful` → `beaut`).
- `^Error` yalnızca **başta** `Error` olan satırı, `\.csv$` yalnızca **sonu**
  `.csv` olan adı buldu.
- **`flags=re.IGNORECASE`** büyük/küçük harfi önemsemez.

## r"..." ve özel karakterler

```python
import re

print(len("\b"), len(r"\b"))
print(re.findall("\bcat\b", "cat concat cat"))
print(re.findall(r"\bcat\b", "cat concat cat"))
print(re.findall(r"3.5", "3.5 345 3x5"), re.findall(r"3\.5", "3.5 345 3x5"))
print(re.escape("price (USD)?"))
m = re.search(r"\d+", "no digits here")
print(m)
try:
    print(m.group())
except AttributeError as error:
    print("AttributeError:", error)
```

```text
1 2
[]
['cat', 'cat']
['3.5', '345', '3x5'] ['3.5']
price\ \(USD\)\?
None
AttributeError: 'NoneType' object has no attribute 'group'
```

- Python metninde `\b` tek bir karakterdir (geri silme). `r"\b"` ise iki
  karakter: ters bölü ve `b`; regex'e ulaşan bu. `r` olmadan `\bcat\b`
  hiçbir şey bulamadı. **Kalıpları her zaman `r"..."` ile yaz.**
- `. ? * + ( ) [ ] { } ^ $ | \` regex'te özel anlamlıdır; harf olarak
  aranacaklarsa önlerine `\` konur. Kullanıcıdan gelen bir metni aramak için
  **`re.escape`** hepsini kendisi kaçırır.
- `search` bulamayınca `None` döndürür; `None.group()` **`AttributeError`**
  verir. Önce kontrol et: `if m: ...`.

## Özet

- `re.search` (herhangi bir yerde), `re.match` (başta), `re.fullmatch`
  (tamamı; doğrulama için), `re.findall` (hepsi, liste).
- `\d \w \s .`, `[...]`, `[^...]`; büyük harfli `\D \W \S` tersi.
- `? * + {n} {m,n}`; `^ $ \b`; `flags=re.IGNORECASE`.
- Kalıp her zaman `r"..."`; özel karakter `\` ile ya da `re.escape`.
- Eşleşme yoksa `None`: `.group()`'tan önce kontrol et.
