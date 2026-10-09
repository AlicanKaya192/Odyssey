In the lesson the confidence threshold was 0.5; that threshold never shows
rules with lift below 1. Yet when generating the data we tied tea to coffee
the **opposite** way: tea is less likely when coffee is present. Let us read
this relation directly from the frequent sets (with the lesson's `freq` and
`baskets`):

```python
coffee, tea = frozenset(["coffee"]), frozenset(["tea"])
both = freq[coffee | tea]
conf = both / freq[coffee]
print(round(freq[tea], 3), round(conf, 3), round(conf / freq[tea], 2))
no_coffee = [b for b in baskets if "coffee" not in b]
print(round(sum("tea" in b for b in no_coffee) / len(no_coffee), 3))
```

```text
0.301 0.14 0.46
0.397
```

Tea is in 30.1% of all baskets, but in only 14% of those with coffee: lift
0.46. Among those without coffee the share is 39.7%. The two replace each
other (substitutes).

This rule is useful information too: recommending tea to coffee buyers is
probably wasted, and a promotion plan should take into account that the two
items replace each other. A rule miner filtering by confidence never shows it; rules with lift
**below** 1 need a separate look.
