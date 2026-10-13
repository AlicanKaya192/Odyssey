The Turkish stemmer in the lesson cut suffixes from a list. Because of
Turkish sound rules, this method can damage the root itself.

## When cutting a suffix damages the root

```python
SUFFIXES = ["ları", "leri", "lar", "ler", "ı", "i", "u", "ü"]


def turkish_root(word):
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) > len(suffix) + 1:
            return word[: -len(suffix)]
    return word


for w in ["kitabı", "ağacı", "kitapları", "evi", "köpeği"]:
    print(w, "->", turkish_root(w))
```

```text
kitabı -> kitab
ağacı -> ağac
kitapları -> kitap
evi -> ev
köpeği -> köpeğ
```

- "kitapları" (their books) → "kitap" (book) is right, but "kitabı" (the
  book) → **"kitab"**: two forms of the same word fell into two different
  roots.
- "ağacı" (the tree) → "ağac", "köpeği" (the dog) → "köpeğ": the root is not
  the dictionary form.

The cause is **consonant softening**: when "kitap" takes a suffix starting
with a vowel it becomes "kitab-ı"; p → b, ç → c, k → ğ. When the suffix is
cut, the softened form is left.

## Turkish rules that make stemming hard

| Rule | Example | Effect on a stemmer |
|---|---|---|
| Vowel harmony | ev-ler, okul-lar; ev-de, okul-da | Every suffix has two or four forms; all must be on the list |
| Consonant assimilation | kitap-ta, ağaç-tan | -de/-da also has the forms -te/-ta |
| Consonant softening | kitap → kitabı, ağaç → ağacı | After cutting the suffix the root stays damaged |
| Buffer letters | araba-y-ı, su-y-u | The inserted letter stays on the root: "araba-y" |
| Suffix order | ev-ler-imiz-den | Suffixes stack up; a loop is needed |
| Roots that end like suffixes | dede, kale, bile | The root gets cut by mistake |

## The real solution

Morphological analysers break a word down suffix by suffix and list every
possible analysis; for "kitabı" the root is "kitap" and the suffix "-ı"
(accusative or possessive). The best known one for Turkish is **Zemberek**.
In simple applications the Turkish Snowball stemmer is also used.

**Subword tokenisation** (BPE), which we meet in the second module, takes
another road: without knowing any rule of the language, it learns letter
sequences that are frequent in the data (for example "ler", "den") as
separate pieces by itself. That is how today's language models cope with
Turkish.
