Bir sosyal medyada takip tek yönlüdür: sen birini takip edebilirsin, o seni
etmeyebilir. Bu bir **yönlü graf**. Her düğümün iki derecesi var: **giren**
(kaç kişi onu takip ediyor) ve **çıkan** (o kaç kişiyi takip ediyor).

```python
follows = [("ada", "bora"), ("cem", "bora"), ("deniz", "bora"),
           ("bora", "ece"), ("ada", "ece"), ("ece", "ada")]

followers, following = {}, {}
for a, b in follows:                       # a, b'yi takip ediyor
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

- `bora`'yı üç kişi takip ediyor: bu grafta en "popüler" o (giren derece).
- `ada` ile `ece` birbirini takip ediyor: yönlü grafta **karşılıklı kenar**,
  yönsüz arkadaşlığa en yakın şey.

Web de yönlü bir graf: sayfalar birbirine bağlantı verir. Bir sayfaya giren
bağlantıların sayısı ve **kimlerden** geldiği, Google'ın ilk arama
algoritması PageRank'in fikri; ML Algoritmaları modülünde NumPy ile yazacağız.
