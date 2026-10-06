score = 85

# This code prints D for 85; it should print B. The problem is the order.
if score >= 50:
    grade = "D"
elif score >= 70:
    grade = "C"
elif score >= 80:
    grade = "B"
elif score >= 90:
    grade = "A"
else:
    grade = "F"

print(grade)
