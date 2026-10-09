Write the function `huffman_bits(text)`: it returns how many bits the text
takes when written with a Huffman code. You do not need to build the codes:
each merge adds as many bits as the sum of the two groups' counts.

1. Count the letters (`collections.Counter` is allowed), put the counts in a
   heap.
2. While the heap holds more than one count, pop the two smallest, add their
   sum to the result and push the sum back.

An empty text is `0`; in a text of a single kind of letter each letter counts
as 1 bit.

**Expected output:**

```
23
21
4
```
