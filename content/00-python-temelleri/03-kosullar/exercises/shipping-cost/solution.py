weight = 10
is_member = True

if weight <= 2:
    cost = 30
elif weight <= 5:
    cost = 45
elif weight <= 10:
    cost = 70
else:
    cost = 70 + (weight - 10) * 8

if is_member and cost >= 50:
    cost = cost * 0.8

print("Cost:", cost)
