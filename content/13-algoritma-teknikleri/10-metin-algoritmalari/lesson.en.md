# String Algorithms

Searching for a word in a text, finding copied paragraphs among thousands of
documents, suggesting words from the letters typed into a search box: all are
algorithms working on text. Python's `in` and `str.find` do the job, but
knowing the ideas behind them lets you choose the right tool where a ready
function is not enough (many patterns, prefix search, similar documents).

In this section the **text** has length `n` and the searched **pattern** has
length `m`.

## Naive search: try every position

The simplest way: place the pattern at every position of the text and compare
letter by letter.

```python
def naive_search(text, pattern):
    found, checks = [], 0
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern):
            checks += 1                     # one letter comparison
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == len(pattern):
            found.append(i)
    return found, checks


print(naive_search("abracadabra", "abra"))
```

```text
([0, 7], 16)
```

Two matches (positions 0 and 7) and 16 comparisons. If most positions are
ruled out at the first letter, naive search is fast. But in the worst case
almost the whole pattern is compared at every position: `O(n · m)`.

## KMP: move forward without going back

On a mismatch, naive search goes back in the text and reads again the letters
it has just read. **KMP (Knuth–Morris–Pratt)** does not: it writes the
repetition inside the pattern into a table beforehand. Cell `i` of the table is
the length of the longest piece that is both a **prefix** and a **suffix** of
the pattern's first `i + 1` letters.

<figure class="fig">
<div><svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">pattern</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">b</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">c</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">a</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">b</text>
</svg></div><div><svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">table</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<rect class="curve" x="256" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<rect class="curve" x="302" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">2</text>
</svg></div>
<figcaption>The table for <code>abacab</code>. The last cell is 2: <code>ab</code> is both the leading and the trailing piece. On a mismatch the pattern continues from letter 2, not from the start.</figcaption>
</figure>

On a mismatch the table answers "how much of the pattern can already count as
matched"; the text is never read backwards.

```python
def prefix_table(pattern):
    table = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = table[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        table[i] = k
    return table


def kmp_search(text, pattern):
    table = prefix_table(pattern)
    found, checks, k = [], 0, 0            # k: letters matched right now
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            checks += 1
            k = table[k - 1]               # step back in the pattern, not the text
        checks += 1
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - k + 1)
            k = table[k - 1]
    return found, checks


print(prefix_table("abacab"))
print(kmp_search("abracadabra", "abra"))
```

```text
[0, 0, 1, 0, 1, 2]
([0, 7], 13)
```

The same matches, 13 comparisons. The difference shows in the worst case:
let us search for fifty `a`s and a `b` inside ten thousand `a`s and a `b`.

```python
text = "a" * 10_000 + "b"
pattern = "a" * 50 + "b"
print(naive_search(text, pattern)[1], kmp_search(text, pattern)[1])
```

```text
507501 19951
```

Naive search made more than half a million comparisons, KMP about twenty
thousand: `O(n + m)`, at most two comparisons per text letter.

## Rabin-Karp: the window's fingerprint

Instead of comparing the letters of every window one by one, **Rabin-Karp**
computes a **hash** (fingerprint). When the window slides by one letter the
hash is not computed from scratch: the leaving letter's contribution is taken
out and the entering letter's is added (**rolling hash**). If the hashes are
equal the letters are still checked, because the hashes of two different texts
can collide, however rarely.

```python
def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    m = len(pattern)
    if m > len(text):
        return []
    high = pow(base, m - 1, mod)           # the leaving letter's weight
    target = window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % mod
        window = (window * base + ord(text[i])) % mod
    found = []
    for i in range(len(text) - m + 1):
        if window == target and text[i:i + m] == pattern:
            found.append(i)
        if i + m < len(text):
            window = (window - ord(text[i]) * high) % mod
            window = (window * base + ord(text[i + m])) % mod
    return found


print(rabin_karp("abracadabra", "abra"))
```

```text
[0, 7]
```

Rabin-Karp's real strength is **many patterns** and **finding copies**: the
hashes of all patterns go into a set, and each window's hash is looked up in
the set. Plagiarism checks and finding documents that contain the same
paragraph work on this idea.

## Trie: the prefix tree

When the search box gets "dat", it suggests `data`, `database`, `dataset`,
`date`. Trying every word with `startswith` grows with the number of words. A
**trie (prefix tree)** puts the words letter by letter into a tree: common
prefixes are stored once, and going down to the prefix's node takes as many
steps as the prefix is long.

<figure class="fig">
<svg viewBox="0 0 232 312" width="232" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="58.1" y1="182.0" x2="29.1" y2="236.0"/>
<line class="line" x1="87.1" y1="236.0" x2="87.1" y2="290.0"/>
<line class="line" x1="58.1" y1="182.0" x2="87.1" y2="236.0"/>
<line class="line" x1="101.6" y1="128.0" x2="58.1" y2="182.0"/>
<line class="line" x1="145.1" y1="182.0" x2="145.1" y2="236.0"/>
<line class="line" x1="101.6" y1="128.0" x2="145.1" y2="182.0"/>
<line class="line" x1="101.6" y1="74.0" x2="101.6" y2="128.0"/>
<line class="line" x1="152.3" y1="20.0" x2="101.6" y2="74.0"/>
<line class="line" x1="203.1" y1="182.0" x2="203.1" y2="236.0"/>
<line class="line" x1="203.1" y1="128.0" x2="203.1" y2="182.0"/>
<line class="line" x1="203.1" y1="74.0" x2="203.1" y2="128.0"/>
<line class="line" x1="152.3" y1="20.0" x2="203.1" y2="74.0"/>
<rect class="box" x="129.2" y="6.0" width="46.2" height="28" rx="7"/>
<text class="ink" x="152.3" y="24.6" font-size="13" text-anchor="middle">root</text>
<rect class="box" x="89.8" y="60.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="101.6" y="78.5" font-size="13" text-anchor="middle">c</text>
<rect class="box" x="89.8" y="114.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="101.6" y="132.6" font-size="13" text-anchor="middle">a</text>
<rect class="box" x="46.3" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="58.1" y="186.6" font-size="13" text-anchor="middle">r</text>
<rect class="box" x="17.3" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="29.1" y="240.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="75.3" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="87.1" y="240.6" font-size="13" text-anchor="middle">t</text>
<rect class="box" x="75.3" y="276.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="87.1" y="294.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="133.3" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="145.1" y="186.6" font-size="13" text-anchor="middle">t</text>
<rect class="box" x="133.3" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="145.1" y="240.6" font-size="13" text-anchor="middle">✓</text>
<rect class="box" x="191.3" y="60.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="203.1" y="78.5" font-size="13" text-anchor="middle">d</text>
<rect class="box" x="191.3" y="114.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="203.1" y="132.6" font-size="13" text-anchor="middle">o</text>
<rect class="box" x="191.3" y="168.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="203.1" y="186.6" font-size="13" text-anchor="middle">g</text>
<rect class="box" x="191.3" y="222.0" width="23.5" height="28" rx="7"/>
<text class="ink" x="203.1" y="240.6" font-size="13" text-anchor="middle">✓</text>
</svg>
<figcaption>A trie holding <code>car</code>, <code>cart</code>, <code>cat</code>, <code>dog</code>. The prefix <code>ca</code> is stored once; ✓ marks where a word ends (the <code>'$'</code> key in the code).</figcaption>
</figure>

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True                   # a word ends here

    def complete(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]
        words, stack = [], [(node, prefix)]
        while stack:
            node, word = stack.pop()
            for ch, child in node.items():
                if ch == "$":
                    words.append(word)
                else:
                    stack.append((child, word + ch))
        return sorted(words)


trie = Trie()
for w in ["data", "database", "date", "dataset", "deep", "model"]:
    trie.insert(w)
print(trie.complete("dat"))
print(trie.complete("x"))
```

```text
['data', 'database', 'dataset', 'date']
[]
```

## In machine learning

- **Tokenisation:** finding the longest matching piece in a language model's
  vocabulary is a prefix question; a trie is the natural structure for it.
- **Copies and similar documents:** fingerprints of pieces (n-grams) with a
  rolling hash to find repeated pieces in training data; MinHash in section 13
  scales this up.
- **Spelling correction:** the candidates in the dictionary are narrowed with a
  trie, and the one with the smallest edit distance (DP 2) among them is
  chosen.

## Summary

- Naive search is `O(n · m)`; slow in the worst case.
- KMP: with the prefix table, `O(n + m)` without going back in the text.
- Rabin-Karp: rolling hash; strong for many patterns and finding copies,
  checking the letters on equal hashes is essential.
- Trie: a tree sharing common prefixes; autocomplete and dictionary search.
