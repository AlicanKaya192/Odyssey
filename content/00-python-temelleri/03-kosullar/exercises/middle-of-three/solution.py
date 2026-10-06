a = 17
b = 42
c = 29

if b <= a <= c or c <= a <= b:
    middle = a
elif a <= b <= c or c <= b <= a:
    middle = b
else:
    middle = c

print(middle)
