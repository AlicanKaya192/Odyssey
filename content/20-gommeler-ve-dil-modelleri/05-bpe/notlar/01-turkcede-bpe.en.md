Turkish is an agglutinative language: hundreds of forms such as "evler"
(houses), "evlerde" (in the houses) and "evlerimizden" (from our houses) grow
from a single root. At word level every form is a separate word, and most are
rare. Let us see whether BPE finds the suffixes by itself, with the lesson's
`learn_bpe` and `encode`, on a small word list:

```python
words = Counter({"ev": 30, "evler": 20, "evlerde": 8, "evlerden": 6,
                 "evimiz": 5, "kitap": 25, "kitaplar": 15, "kitaplarda": 6,
                 "kitaplardan": 5, "okul": 20, "okullar": 12, "okullarda": 7,
                 "okuldan": 6, "kalem": 15, "kalemler": 10, "kalemlerden": 4})
turkish = learn_bpe(words, 24)
for start in range(0, 24, 4):
    print(turkish[start:start + 4])
for word in ["evlerimizden", "okullardan", "kalemlerde", "masalar"]:
    print(word, encode(word, turkish))
```

```text
[('l', 'e'), ('e', 'v'), ('r', '</w>'), ('t', 'a')]
[('ta', 'p'), ('k', 'i'), ('ki', 'tap'), ('u', 'l')]
[('o', 'k'), ('ok', 'ul'), ('l', 'a'), ('r', 'd')]
[('ev', 'le'), ('ev', '</w>'), ('le', 'm'), ('k', 'a')]
[('ka', 'lem'), ('la', 'r</w>'), ('kitap', '</w>'), ('n', '</w>')]
[('okul', '</w>'), ('evle', 'r</w>'), ('rd', 'e'), ('rd', 'a')]
evlerimizden ['evle', 'r', 'i', 'm', 'i', 'z', 'd', 'e', 'n</w>']
okullardan ['okul', 'la', 'rda', 'n</w>']
kalemlerde ['kalem', 'le', 'rde', '</w>']
masalar ['m', 'a', 's', 'a', 'lar</w>']
```

- The first rules build roots ("kitap", "okul", "kalem"): in this list these
  are the most frequent letter sequences.
- Suffixes appear too, but not where grammar would cut. `lar</w>` is a real
  suffix; but "okullardan" is split as `okul + la + rda + n</w>`, while the
  right split would be `okul + lar + dan`. BPE knows no grammar; it only
  merges frequent pieces.
- The root "masalar" (tables) is not in the list: the root is split into
  letters but the `lar</w>` suffix is recognised.
- "evlerimizden" was split mostly into letters: "imiz" appears in the list
  only in "evimiz", so it did not become a rule. With a larger corpus these
  suffixes could become pieces too.
- Unlike the rule-based suffix splitting of section 03, BPE can cut in the
  wrong place; but it needs no language-specific rules and works the same
  way in every language.
