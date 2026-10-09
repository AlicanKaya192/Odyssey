`group_anagrams(words)` fonksiyonunu yaz: aynı harflerden oluşan kelimeleri
gruplasın ve grupları bir liste olarak döndürsün. Gruplar, **ilk kelimelerinin
listede göründüğü sırayla**; grup içindeki kelimeler de girdideki sırayla.

- `["tea", "eat", "tan", "ate", "nat", "bat"]` →
  `[["tea", "eat", "ate"], ["tan", "nat"], ["bat"]]`

Anahtar: kelimenin sıralı harfleri (`"".join(sorted(word))`). Python sözlüğü
ekleme sırasını koruduğu için grupların sırası kendiliğinden doğru çıkar.

**Beklenen çıktı:**

```
['tea', 'eat', 'ate']
['tan', 'nat']
['bat']
[]
```
