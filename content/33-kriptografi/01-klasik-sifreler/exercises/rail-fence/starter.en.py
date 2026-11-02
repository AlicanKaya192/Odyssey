def rail_fence(text, rails):
    rows = [""] * rails
    for i, ch in enumerate(text):
        rows[i % rails] += ch
    return "".join(rows)

print(rail_fence("WEAREDISCOVERED", 3))
print(rail_fence("HELLOWORLD", 4))
print(rail_fence("ABC", 1))
