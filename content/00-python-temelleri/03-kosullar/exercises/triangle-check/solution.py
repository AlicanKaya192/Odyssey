a = 3
b = 4
c = 8

if a + b <= c or a + c <= b or b + c <= a:
    kind = "not a triangle"
elif a == b and b == c:
    kind = "equilateral"
elif a == b or b == c or a == c:
    kind = "isosceles"
else:
    kind = "scalene"

print(kind)
