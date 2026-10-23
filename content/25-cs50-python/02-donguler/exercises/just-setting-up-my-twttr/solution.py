text = input("Input: ")
result = ""
for c in text:
    if c.lower() not in "aeiou":
        result += c
print(result)
