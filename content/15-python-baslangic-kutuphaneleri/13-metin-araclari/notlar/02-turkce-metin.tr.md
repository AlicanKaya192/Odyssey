Python'un metin işlemleri **dil bilmez**: Unicode'un genel kurallarına göre
çalışır. İngilizce için bu yeterli, Türkçe için iki yerde yetmiyor:
büyük/küçük harf ve abece sırası.

## Sıralama

```python
words = ["çay", "zeytin", "ıhlamur", "ispanak", "elma", "şeker", "Üzüm", "armut"]
print(sorted(words))
ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"


def tr_key(word):
    lowered = word.replace("I", "ı").replace("İ", "i").lower()
    return [ALPHABET.find(ch) for ch in lowered]


print(sorted(words, key=tr_key))
print("ILIK".lower(), "ILIK".replace("I", "ı").lower())
```

```text
['armut', 'elma', 'ispanak', 'zeytin', 'Üzüm', 'çay', 'ıhlamur', 'şeker']
['armut', 'çay', 'elma', 'ıhlamur', 'ispanak', 'şeker', 'Üzüm', 'zeytin']
ilik ılık
```

- `sorted` harfleri **Unicode numaralarına** göre dizer: `ç`, `ı`, `ş`, `Ü`
  İngilizce harflerin hepsinden sonra gelir ve büyük harf küçükten önce
  (`Üzüm`, `çay`'dan önce). Sonuç Türkçe okura karışık görünür.
- **Kendi sıra anahtarın:** abeceyi bir metin olarak yaz, her harfin oradaki
  yerini (`find`) anahtar yap. `key=` ile verilen fonksiyon her kelime için
  bir kez çağrılır, sayılar listesi karşılaştırılır.
- Anahtarın başında Türkçe küçük harf çevirisi var: önce `I` → `ı`,
  `İ` → `i`, sonra `lower()`. Yalnızca `lower()` `ILIK`'ı `ilik` yaptı.

İşletim sisteminin dil ayarını kullanan `locale` modülü de Türkçe sıralama
yapabilir, ama sonuç programın çalıştığı bilgisayarın ayarına bağlıdır;
yukarıdaki anahtar her bilgisayarda aynı sonucu verir.

## Aramada "katlamak"

Kullanıcı İngilizce klavyeyle `sisli` yazıp `Şişli`'yi bulabilmeli. Bunun
için iki metni de aynı sade biçime **katlarsın** (fold): küçük harf, aksansız,
`ı` → `i`.

```python
import unicodedata


def fold(text):
    text = text.replace("I", "ı").replace("İ", "i").lower().replace("ı", "i")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


places = ["Şişli", "Kadıköy", "Üsküdar", "Beşiktaş", "IĞDIR"]
query = "sisli"
print([p for p in places if fold(query) in fold(p)])
print([fold(p) for p in places])
```

```text
['Şişli']
['sisli', 'kadikoy', 'uskudar', 'besiktas', 'igdir']
```

Önce Türkçe küçük harf, sonra `ı` → `i`, sonra NFD ile aksan atma. Arama
kutularında (bu programın `Ctrl+K` aramasında da) yapılan iş budur: aranan
ve aranılan aynı biçime getirilip karşılaştırılır, kullanıcıya ise özgün
metin gösterilir.

## Kontrol listesi

- Türkçe küçük harf: önce `I` → `ı`, `İ` → `i`, sonra `lower()`.
- Türkçe büyük harf: önce `i` → `İ`, `ı` → `I`, sonra `upper()`.
- Abece sırası için kendi anahtar fonksiyonun.
- Aramada iki tarafı da katla; ekranda özgün metni göster.
