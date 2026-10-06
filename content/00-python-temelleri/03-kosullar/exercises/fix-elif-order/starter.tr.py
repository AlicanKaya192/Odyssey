score = 85

# Bu kod 85 için D yazıyor; B yazmalı. Sorun koşulların sırasında.
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
