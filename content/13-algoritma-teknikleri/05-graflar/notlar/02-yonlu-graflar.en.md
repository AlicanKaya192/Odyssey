On social media following goes one way: you can follow someone who does not
follow you. This is a **directed graph**. Each node has two degrees: **in**
(how many people follow them) and **out** (how many they follow).

```python
follows = [("ada", "bora"), ("cem", "bora"), ("deniz", "bora"),
           ("bora", "ece"), ("ada", "ece"), ("ece", "ada")]

followers, following = {}, {}
for a, b in follows:                       # a follows b
    following.setdefault(a, set()).add(b)
    followers.setdefault(b, set()).add(a)

people = sorted(set(followers) | set(following))
for person in people:
    print(person, "followers:", len(followers.get(person, ())),
          "following:", len(following.get(person, ())))

mutual = sorted((a, b) for a, b in follows if a < b and a in following.get(b, ()))
print("mutual:", mutual)
```

```text
ada followers: 1 following: 2
bora followers: 3 following: 1
cem followers: 0 following: 1
deniz followers: 0 following: 1
ece followers: 2 following: 1
mutual: [('ada', 'ece')]
```

- Three people follow `bora`: in this graph they are the most "popular" (in
  degree).
- `ada` and `ece` follow each other: in a directed graph a **mutual edge**,
  the closest thing to undirected friendship.

The web is a directed graph too: pages link to each other. The number of links
into a page and **who** they come from is the idea of PageRank, Google's
first search algorithm; we will write it with NumPy in ALG 3.
