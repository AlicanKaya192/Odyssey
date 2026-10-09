In the lesson we found the codes for `abracadabra`. Turning a text into a bit
string with these codes is easy; the interesting part is **decoding**: there
are no separators between the bits, so how do we know where a letter ends?

The answer is the prefix property: no code is the start of another code.
Reading the bits from the left, as soon as the piece you have gathered equals
a code, that letter is **certain**; it cannot be the start of a longer code.

```python
codes = {"a": "0", "b": "110", "c": "100", "d": "101", "r": "111"}

def encode(text):
    return "".join(codes[ch] for ch in text)

def decode(bits):
    reverse = {code: ch for ch, code in codes.items()}
    out, current = [], ""
    for bit in bits:
        current += bit
        if current in reverse:            # a code is complete
            out.append(reverse[current])
            current = ""
    return "".join(out)

bits = encode("abracadabra")
print(bits, len(bits))
print(decode(bits))
```

```text
01101110100010101101110 23
abracadabra
```

If the prefix property were broken (say `a = 0`, `b = 01`), the string `01`
could be "a then something" or "b".

## Why is it the best?

If the two rarest letters are put deepest in the tree, as siblings, the total
number of bits does not grow (the exchange argument). Merging them into a
single "letter" leaves the same problem with one letter fewer. Since this is
done at every step, the result is the best **prefix code**.

**Note:** you do not even need the codes to find the total number of bits:
each merge adds as many bits as the sum of the two groups' counts. You will
use this in the exercise.
