def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def lookalikes(names, protected):
    found = []
    # for each name look at its distance to the protected names
    return found

PROTECTED = ["example.com", "example.org"]
names = ["examp1e.com", "example.org", "exarnple.com",
         "sample.net", "exampel.org"]
for name in lookalikes(names, PROTECTED):
    print(name)
