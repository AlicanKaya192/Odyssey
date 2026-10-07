import json

with open("users.json", encoding="utf-8") as file:
    users = json.load(file)

no_email = 0
ages = []
for user in users:
    email = user.get("email", "-")
    print(user["name"], email)
    if email == "-":
        no_email += 1
    age = user.get("age")
    if age is not None:
        ages.append(age)

average_age = sum(ages) // len(ages)

print(no_email)
print(average_age)
