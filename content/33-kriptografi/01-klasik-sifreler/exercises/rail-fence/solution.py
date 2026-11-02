def rail_fence(text, rails):
    if rails == 1:
        return text
    rows = [""] * rails
    row, step = 0, 1
    for ch in text:
        rows[row] += ch
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return "".join(rows)

print(rail_fence("WEAREDISCOVERED", 3))
print(rail_fence("HELLOWORLD", 4))
print(rail_fence("ABC", 1))
