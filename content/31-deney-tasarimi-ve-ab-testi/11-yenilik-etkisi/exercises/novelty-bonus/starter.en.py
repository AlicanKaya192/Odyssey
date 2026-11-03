def novelty_bonus(day, start=0.2, half_life=3):
    return round(start * 0.5 ** (day / half_life), 4)


print(novelty_bonus(1))
print(novelty_bonus(4))
