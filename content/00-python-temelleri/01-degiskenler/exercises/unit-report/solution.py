raw_height = "180"
raw_weight = "75.5"
name = "Ada"

height = int(raw_height)
weight = float(raw_weight)

meters = height / 100
bmi = round(weight / (meters * meters), 2)

print(f"{name} is {meters} m and {weight} kg, bmi {bmi}")
