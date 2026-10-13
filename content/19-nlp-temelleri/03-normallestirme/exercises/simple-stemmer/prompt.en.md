`stem(word)` should try the rules in `SUFFIX_RULES` in order. If the word ends
with the suffix and at least **3 letters** remain after cutting it, cut the
suffix, add its replacement and return the result. One exception: the `"s"`
rule is not applied to words ending in `"ss"`. If no rule fits, return the
word unchanged.

**Expected output:**

```
cables cable
replies reply
charging charg
worked work
glass glass
boss boss
is is
slowly slow
```
