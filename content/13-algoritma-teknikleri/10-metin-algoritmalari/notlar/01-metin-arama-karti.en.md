## Which method?

| Method | Cost | When? |
|---|---|---|
| Naive search | `O(n · m)` in the worst case | a short pattern, a single search |
| KMP | `O(n + m)` | the pattern repeats itself, the worst case matters |
| Rabin-Karp | `O(n + m)` on average | many patterns, finding copied pieces |
| Trie | as long as the prefix | prefix search, autocomplete |
| Python `in`, `str.find` | written in C | the first choice for one pattern |

## The KMP prefix table

`table[i]`: the length of the longest piece that is both a prefix and a suffix
of `pattern[:i + 1]` (not the piece itself).

| Pattern | Table |
|---|---|
| `abacab` | `0 0 1 0 1 2` |
| `aaaa` | `0 1 2 3` |
| `abcd` | `0 0 0 0` |

## Rolling hash

- New window = (old − leaving letter × `base^(m−1)`) × `base` + entering
  letter, all with `mod`.
- An equal hash **does not mean a match**: compare the letters as well.
- `mod` is chosen as a large prime; a small `mod` increases collisions.

## Common mistakes

- Running the naive search loop up to `len(text)` instead of
  `len(text) - len(pattern) + 1`: an index outside the text.
- Resetting `k` to zero after a match in KMP: overlapping matches (`"aa"` twice
  in `"aaa"`) are missed; the right way is `k = table[k - 1]`.
- Counting equal hashes directly as a match in Rabin-Karp.
- Not marking the end of a word in a trie: after adding `data`, asking for
  `dat` takes `dat` for a word too.
