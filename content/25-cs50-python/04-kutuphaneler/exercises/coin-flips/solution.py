import random

n = int(input("Flips: "))
heads = 0
for _ in range(n):
    coin = random.choice(["heads", "tails"])
    print(coin)
    if coin == "heads":
        heads += 1
print(f"{heads} heads")
